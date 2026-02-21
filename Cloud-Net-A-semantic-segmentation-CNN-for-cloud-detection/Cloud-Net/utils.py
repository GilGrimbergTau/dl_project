import keras
import keras.backend as K
from sklearn.metrics import jaccard_score, precision_score, recall_score
from tqdm import tqdm
import os
import matplotlib.pyplot as plt
import shutil
import re
from pathlib import Path
import numpy as np
import inspect
import raw_dataset_info  # The file containing dataset1, dataset2, etc.
from raw_dataset_info import Dataset # The class definition
import json
from PIL import Image
from global_params import GEN_TEST,GEN_TRAIN,GEN_VAL
import cv2

class ADAMLearningRateTracker(keras.callbacks.Callback):
    """It prints out the last used learning rate after each epoch (useful for resuming a training)
    original code: https://github.com/keras-team/keras/issues/7874#issuecomment-329347949
    """

    def __init__(self, end_lr):
        super(ADAMLearningRateTracker, self).__init__()
        self.end_lr = end_lr

    def on_epoch_end(self, epoch, logs={}):  # works only when decay in optimizer is zero
        optimizer = self.model.optimizer
        # t = K.cast(optimizer.iterations, K.floatx()) + 1
        # lr_t = K.eval(optimizer.lr * (K.sqrt(1. - K.pow(optimizer.beta_2, t)) /
        #                               (1. - K.pow(optimizer.beta_1, t))))
        # print('\n***The last Actual Learning rate in this epoch is:', lr_t,'***\n')
        print('\n***The last Basic Learning rate in this epoch is:', optimizer.learning_rate.numpy(), '***\n')
        # stops the training if the basic lr is less than or equal to end_learning_rate
        if optimizer.learning_rate.numpy() <= self.end_lr:
            print("training is finished")
            self.model.stop_training = True

################### arranging the Dataset ###################

def cut_dataset_to_patches(input_base_dir, output_base_dir):
    # Constants
    TARGET_W, TARGET_H = 1024, 768
    PATCH_W, PATCH_H = 384, 288
    
    # Calculate centering offsets
    start_x = (TARGET_W - (PATCH_W * 2)) // 2  # 128
    start_y = (TARGET_H - (PATCH_H * 2)) // 2  # 96

    input_root = Path(input_base_dir).resolve()
    output_root = Path(output_base_dir).resolve()

     # retrieve all the frames with a numeric name (e.g 3452.tif etc.)
    numeric_pattern = re.compile(r'^\d+\.tif$')
    image_files = [f for f in Path(input_base_dir).rglob("*.tif") if numeric_pattern.match(f.name) and "demo" not in f.parts]
    for img_path in image_files:
        mask_path = img_path.parent / "no_land_no_water.tif"
        if not os.path.exists(mask_path):
            mask_path = img_path.parent / "no_water_no_land.tif"
        try:
            img = Image.open(img_path)
            mask = Image.open(mask_path)
            # 2. MIRROR LOGIC:
            # Get the path of the folder containing the image, relative to input_base_dir
            relative_folder = img_path.parent.relative_to(input_root)
            # 3. Patching
            img_base_name = img_path.stem 
            mask_base_name = mask_path.stem 
            # 1. Shape check
            if img.size != (TARGET_W, TARGET_H) or mask.size != (TARGET_W, TARGET_H):
                print(f'image or mask sizes do not correspond to the expected size: expected: {TARGET_W, TARGET_H} and got : {img.size} and {mask.size}')
                save_dir = output_root / Path(str(relative_folder))
                # Create the folders if they don't exist
                save_dir.mkdir(parents=True, exist_ok=True)
                # Saving to the mirrored directory
                img_patch_name = f"{img_base_name}.tif"
                mask_patch_name = f"{mask_base_name}.tif"
                img.save(save_dir / img_patch_name)
                mask.save(save_dir / mask_patch_name)
                continue

            for row in range(2):
                for col in range(2):
                    left = start_x + (col * PATCH_W)
                    top = start_y + (row * PATCH_H)
                    
                    img_patch = img.crop((left, top, left + PATCH_W, top + PATCH_H))
                    mask_patch = mask.crop((left, top, left + PATCH_W, top + PATCH_H))
                    
                    # Combine that with the output_base_dir to recreate the tree
                    save_dir = output_root / Path(str(relative_folder) + f"_{row*2 + col}")
                    # Create the folders if they don't exist
                    save_dir.mkdir(parents=True, exist_ok=True)
                    # Saving to the mirrored directory
                    img_patch_name = f"{img_base_name}_{row*2 + col}.tif"
                    mask_patch_name = f"{mask_base_name}_{row*2 + col}.tif"
                    img_patch.save(save_dir / img_patch_name)
                    mask_patch.save(save_dir / mask_patch_name)

        except Exception as e:
            print(f"Skipping {img_path.name}: {e}")

def remove_folders_by_text_file(file_path):
    # 1. Check if the txt file exists
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} was not found.")
        return

    with open(file_path, 'r') as f:
        # Read lines and strip whitespace/newlines
        paths = [line.strip() for line in f]
    print(f'About to remove {len(paths)} files...')
    for folder_path in paths:
        # 2. Safety check: Does the folder actually exist?
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            try:
                # 3. Remove the folder and everything inside it
                shutil.rmtree(folder_path)
            except Exception as e:
                print(f"Failed to delete {folder_path}. Reason: {e}")
        else:
            print(f"Skipping: {folder_path} (Path does not exist or is not a directory)")


def get_excluded_subfolders(base_root_folder, datasets_list):
    """
    a function that given a root folder with multiple subfolders containing all the raw dataset (namely the images with .tif extensions)
    and a list of datasets objects with details about the excluded frames ranges, creates a txt file with the list of paths to all the excluded frames.
    
    :param base_root_folder: path to base folder
    :param datasets_list: list of "Dataset" objects from "raw_dataset_info.py"
    """
    excluded_folders = []
    
    # 1. Create a lookup map for datasets by their name
    dataset_map = {ds.Name: ds for ds in datasets_list}
    
    # 2. retrieve all the frames with a numeric name (e.g 3452.tif etc.)
    numeric_pattern = re.compile(r'^\d+\.tif$')
    image_files = [f for f in Path(base_root_folder).rglob("*.tif") if numeric_pattern.match(f.name) and "demo" not in f.parts]
        
    if not image_files:
        print(f'failed to find images with a numeric name!')
        return excluded_folders
    # sort the images list
    image_files.sort()
    for frame_path in image_files:
        # 3. Identify which dataset this folder belongs to
        # We check if any dataset name exists in the current path string
        current_dataset = None
        for name in dataset_map:
            if name in frame_path.parts:
                current_dataset = dataset_map[name]
                break
        
        if not current_dataset:
            print(f'frame {frame_path} does not belong to any of the given datasets!')
            continue

        # 4. Extract frame numbers and check against excluded ranges
        is_excluded = False
        # Extract numeric value from filename (e.g., "frame_20575.tif" -> 20575)
        frame_num = frame_path.parts[-1]
        frame_num = int(frame_num.split(".")[0])
        # Check if this frame is in any of the excluded ranges
        for start, end in current_dataset.Excluded_frame_ranges_list:
            if start <= frame_num <= end:
                is_excluded = True
                break
        
        # 5. Add folder to list if an excluded frame was found
        if is_excluded:
            # add the path to the folder in which the current frame is
            frame_folder = os.path.dirname(frame_path)
            excluded_folders.append(frame_folder)
            
    with open(os.path.join(base_root_folder,"excluded_frames.txt"),'w') as ex_f:
        for folder in excluded_folders:
            ex_f.write(f'{folder}\n')
    return list(excluded_folders)

def generate_dataset_stats(base_root_folder, datasets_list, output_file='dataset_cloud_stats.json'):
    # 1. Initialize the results structure
    stats = {}
    for ds in datasets_list:
        stats[ds.Name] = {
            "ground_images_count": 0,
            "cloudy_images_count": 0,
            "total_pixels_zero": 0,
            "total_pixels_not_zero": 0,
            "percent_cloudy_pixels": 0.0  # Placeholder for the final calculation
        }

    # 2. Walk through the directory tree
    for root, dirs, files in os.walk(base_root_folder):
        # Look specifically for the cloud mask file
        if "no_land_no_water.tif" in files:
            
            # Identify which dataset this folder belongs to
            current_ds_name = None
            for ds in datasets_list:
                if ds.Name in root:
                    current_ds_name = ds.Name
                    break
            
            if not current_ds_name:
                continue

            file_path = os.path.join(root, "no_land_no_water.tif")
            
            try:
                with Image.open(file_path) as img:
                    img_array = np.array(img)
                    
                    # Count non-zero (clouds) vs zero (ground)
                    num_not_zero = np.count_nonzero(img_array)
                    num_zero = img_array.size - num_not_zero
                    
                    # Update image counts
                    if num_not_zero == 0:
                        stats[current_ds_name]["ground_images_count"] += 1
                    else:
                        stats[current_ds_name]["cloudy_images_count"] += 1
                    
                    # Aggregate pixel counts (cast to int for JSON compatibility)
                    stats[current_ds_name]["total_pixels_zero"] += int(num_zero)
                    stats[current_ds_name]["total_pixels_not_zero"] += int(num_not_zero)
            except Exception as e:
                print(f"Could not process {file_path}: {e}")

    # 3. Compute Percentages
    for ds_name, data in stats.items():
        total_pixels = data["total_pixels_zero"] + data["total_pixels_not_zero"]
        
        if total_pixels > 0:
            # Percentage of cloud pixels (non-zero) out of total pixels
            cloud_percentage = (data["total_pixels_not_zero"] / total_pixels) * 100
            stats[ds_name]["percent_cloudy_pixels"] = round(cloud_percentage, 4)
        else:
            stats[ds_name]["percent_cloudy_pixels"] = 0.0

    # 4. Save to JSON
    with open(output_file, 'w') as jf:
        json.dump(stats, jf, indent=4)
        
    print(f"Statistics successfully saved to {output_file}")
    return stats

def get_split_paths(target_dir, gen_type=GEN_TRAIN):
    """
    Retrieves sorted lists of file paths for images and masks from a specific split.

    Args:
        target_dir (str): The root path of the processed dataset.
        if_train (bool): True for "train" Flase for "test".

    Returns:
        tuple: (image_paths, mask_paths) where each is a list of Path objects.
    """
    # Define the paths to the specific split folders
    if gen_type == GEN_TRAIN:
        split_path = Path(target_dir) / "train"
    elif gen_type == GEN_VAL:
        split_path = Path(target_dir) / "val"
    else:
        split_path = Path(target_dir) / "test"

    images_dir = split_path / "images"
    masks_dir = split_path / "masks"

    # Check if directories exist to avoid errors
    if not images_dir.exists() or not masks_dir.exists():
        print(f"Error: {gen_type} directory structure not found in {target_dir}")
        return [], []

    # Get all .tif files and sort them to ensure matching indices
    image_paths = sorted(list(images_dir.glob("*.tif")))
    mask_paths = sorted(list(masks_dir.glob("*.tif")))

    # Simple validation to ensure parity
    if len(image_paths) != len(mask_paths):
        print(f"Warning: Mismatch in {gen_type} set! "
              f"Images: {len(image_paths)}, Masks: {len(mask_paths)}")
        return [], []

    return image_paths, mask_paths

def get_input_image_names(data_folder_path, gen_type=GEN_TRAIN):

    list_img, list_msk =  get_split_paths(data_folder_path, gen_type)
    return list_img, list_msk
    
    # return list_img, list_test_ids


def sort_dataset(source_dir, target_dir, test_list_file, val_list_file):
    """
    Recursively traverses a source directory to identify pairs of numeric image files and their 
    corresponding masks. It splits these pairs into "train" and "test" sets based on a provided text 
    file and renames them using a global index and the yaaf name to ensure uniqueness and 
    compatibility with deep learning data loaders.
    
    :param source_dir: The root path containing subfolders of images and masks.
    :param target_dir: The destination path where the train/ and test/ folders will be created.
    :param test_list_file: Path to a .txt file containing names of subfolders (one per line) that belong to the test set.
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    # Helper to read lists safely
    def read_list(file_path):
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if (not line.startswith("#") and line.strip())]

    # Read the split lists
    test_folders = read_list(test_list_file)
    val_folders = read_list(val_list_file)

    # Create target directory structure for all three splits
    for split in ['train', 'test', 'val']:
        for folder in ['images', 'masks']:
            (target_path / split / folder).mkdir(parents=True, exist_ok=True)

    # Find and sort all numeric .tif files
    mask_files = [f for f in source_path.rglob("*.tif") if f.name.__contains__("no_land")]
    mask_files.sort() # Ensure consistent indexing order
    
    print(f"Found {len(mask_files)} potential images. Processing...")

    # Manual counter to ensure continuous indexing for successful pairs
    current_index = 0

    for mask_path in mask_files:
        # Ignore any file if "demo" is in its folder path
        if "demo" in mask_path.parts:
            continue
        # Determine split: test if any parent folder is in the test_folders list
        # Check if any parent folder is in test list, then check validation list, else train
        if any(part in test_folders for part in mask_path.parts):
            split = 'test'
        elif any(part in val_folders for part in mask_path.parts):
            split = 'val'
        else:
            split = 'train'
        
        if mask_path.exists():
            # Get the folder name TWO levels upstream
            try:
                upstream_folder = mask_path.parent
                yaaf_name = mask_path.parents[1].name
            except IndexError:
                yaaf_name = "unknown"

            for file in upstream_folder.iterdir():
                if not "no_land" in str(file):
                    image_path = file
                    break
            # Construct filenames using the manual counter
            new_filename = f"{current_index:06d}_{yaaf_name}.tif"

            # Define destinations
            dest_img = target_path / split / 'images' / new_filename
            dest_mask = target_path / split / 'masks' / new_filename

            # Copy files
            shutil.copy2(image_path, dest_img)
            shutil.copy2(mask_path, dest_mask)
            
            # ONLY increment index if copy was successful
            current_index += 1
        else:
            # If mask is missing, we skip this image and the index does NOT increase
            print(f"Skipping: Mask missing for {mask_path}")

    print(f"Process complete. Total paired files copied: {current_index}")


def normalize_dataset_polarity(root_path, scenario_txt, output_path):
    # 1. Parse the scenario text file
    with open(scenario_txt, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    black_hot_list = []
    current_section = None
    for line in lines:
        if line.lower() == "#white-hot":
            current_section = "white"
        elif line.lower() == "#black-hot":
            current_section = "black"
        elif current_section == "black":
            black_hot_list.append(line)

    print(f"Loaded {len(black_hot_list)} Black-Hot scenarios.")

    modified_images = []
    root = Path(root_path)
    output_root = Path(output_path)

    # 2. Walk through the directory tree
    # We only care about 'images' folders; masks usually don't need polarity flips
    for subdir in ['train', 'val', 'test']:
        img_dir = root / subdir / 'images'
        mask_dir = root / subdir / 'masks'
        
        # Define output paths
        out_img_dir = output_root / subdir / 'images'
        out_mask_dir = output_root / subdir / 'masks'
        
        # Ensure output directories exist
        out_img_dir.mkdir(parents=True, exist_ok=True)
        out_mask_dir.mkdir(parents=True, exist_ok=True)

        if not img_dir.exists():
            continue

        for img_file in img_dir.glob('*.tif'):
            # Check if image name contains any black-hot scenario keywords
            is_black_hot = any(scenario in img_file.name for scenario in black_hot_list)
            
            if is_black_hot:
                # 16-bit inversion
                 # Load the image
                img_data = cv2.imread(str(img_file),cv2.IMREAD_UNCHANGED)
                img_data = np.max(img_data) + np.min(img_data) - img_data
                modified_images.append(str(img_file.relative_to(root)))
                cv2.imwrite(str(out_img_dir / img_file.name), img_data.astype(np.uint16))
            else:
                # copy image as is
                shutil.copy(str(img_file),str(out_img_dir / img_file.name))
            
            # Copy masks as-is (they are just labels 0/1)
            # You can also use shutil.copy for speed here
            mask_file = mask_dir / img_file.name
            if mask_file.exists():
                shutil.copy(str(mask_file),str(out_mask_dir / img_file.name))
            else:
                print(f'mask path could not be found! {str(mask_file)}')

    # 3. Save the log of modified images
    with open(output_root / 'modified_images_log.txt', 'w') as log_file:
        log_file.write("\n".join(modified_images))
    
    print(f"Processing complete. {len(modified_images)} images were flipped.")

def analyze_mask_folder(folder_path):
    # Initialize counters
    total_images = 0
    total_zero_pixels = 0
    total_nonzero_pixels = 0
    
    # Supported image extensions
    valid_extensions = ('.tif', '.tiff', '.png', '.jpg', '.jpeg', '.bmp')

    # Iterate through folder
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]
    total_images = len(files)

    if total_images == 0:
        print(f"No valid mask files found in {folder_path}")
        return

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        
        # Load image (IMREAD_UNCHANGED is crucial for 16-bit or special masks)
        mask = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        
        if mask is None:
            continue

        # Count pixels
        # np.count_nonzero is very fast
        nonzero_count = np.count_nonzero(mask)
        zero_count = mask.size - nonzero_count
        
        total_nonzero_pixels += nonzero_count
        total_zero_pixels += zero_count

    # Calculate percentages
    total_pixels = total_zero_pixels + total_nonzero_pixels
    percent_zero = (total_zero_pixels / total_pixels) * 100 if total_pixels > 0 else 0
    percent_nonzero = (total_nonzero_pixels / total_pixels) * 100 if total_pixels > 0 else 0

    # Print Results
    print(f"--- Analysis Results for: {folder_path} ---")
    print(f"Total number of masks:      {total_images}")
    print(f"Total pixels processed:      {total_pixels:,}")
    print("-" * 40)
    print(f"Pixels with value 0:         {total_zero_pixels:,} ({percent_zero:.2f}%)")
    print(f"Pixels with value > 0:       {total_nonzero_pixels:,} ({percent_nonzero:.2f}%)")
    print("-" * 40)


def find_best_worst_predictions(y_true_all, y_pred_all,orig_images_paths, mask_paths, output_folder, metrics=["jaccard"], n=10):
    """
    y_true_all: (N, H, W, 1) ground truth masks
    y_pred_all: (N, H, W, 1) model probability outputs
    """
    for metric in metrics:
        scores = []
        
        for i in range(len(y_true_all)):
            # Binarize prediction (using 0.5 threshold)
            pred_mask = y_pred_all[i].flatten()
            true_mask = y_true_all[i].flatten()
            
            # Calculate Jaccard (IoU) for this specific frame
            if metric == "jaccard":
                score = jaccard_score(true_mask, pred_mask, zero_division=1)
                if score == 0.0:
                    continue
            elif metric == "precision":
                score = precision_score(true_mask, pred_mask, zero_division=0.0)
                if score == 0.0:
                    continue
            elif metric == "recall":
                score = recall_score(true_mask, pred_mask)
            else:
                print(f'illegal metric given {metric}!')
                exit(1)
            if score < 1: # ignore "perfect" scores since they not necessarily reflect how good the model really is (precision can be 1 even though we missed some clouds) 
                scores.append((i, score))
        
        # Sort by score ascending (lowest first)
        sorted_scores = sorted(scores, key=lambda x: x[1])
        
        # create new folder within the Prediction folder
        best_folder = os.path.join(output_folder, "best_predictions",f'{metric}')
        worst_folder = os.path.join(output_folder, "worst_predictions",f'{metric}')
        Path(best_folder).mkdir(parents=True, exist_ok=True)
        Path(worst_folder).mkdir(parents=True, exist_ok=True)
        # print(f"Top {n} Worst Predictions (by Jaccard Score):")
        # for idx, score in worst_indices:
        #     print(f"Index: {idx:4d} | Jaccard Score: {score:.4f}")
            
        # 2. Plotting
        # for i, (idx, score) in enumerate(worst_indices):
        for i in range(n):
            # Image
            bad_idx, bad_score = sorted_scores[i]
            good_idx, good_score = sorted_scores[-i-1]
            
            display_best_worst_predictions(y_true_all, y_pred_all, orig_images_paths, metric, i, worst_folder, bad_idx, bad_score)
            display_best_worst_predictions(y_true_all, y_pred_all, orig_images_paths, metric, i, best_folder, good_idx, good_score)

def display_best_worst_predictions(y_true_all, y_pred_all, orig_images_paths, metric, i, folder, idx, score):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
    orig_bad_image = cv2.imread(orig_images_paths[idx],cv2.IMREAD_UNCHANGED)
    axes[0].imshow(orig_bad_image, cmap="gray")
    axes[0].set_title(f"Index: {idx}\nFile: {str(orig_images_paths[idx]).split('/')[-1]}")
    axes[0].axis('off')
        
        # Ground Truth
    axes[1].imshow(y_true_all[idx].squeeze(), cmap='gray', vmin=0, vmax=1)
    axes[1].set_title("Ground Truth")
    axes[1].axis('off')
        
        # Prediction
    axes[2].imshow(y_pred_all[idx].squeeze(), cmap='gray', vmin=0, vmax=1)
    axes[2].set_title(f"Prediction ({metric}: {score})")
    axes[2].axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(folder,f'pred_{i}'),dpi=200, bbox_inches='tight')
    plt.close()
        
    # plt.tight_layout()
    # plt.show()
#####################################

def save_history_plots(history, output_path):
    # 1. Identify unique metrics (removing the 'val_' prefix)
    # This gives us ['loss', 'accuracy', 'recall', 'precision', ...]
    metrics = [key for key in history.history.keys() if not key.startswith('val_')]
 
    for metric in metrics:
        plt.figure(figsize=(8, 5))
        # Plot training metric
        plt.plot(history.history[metric], label=f'Train {metric.capitalize()}')
        # Plot validation metric if it exists
        val_key = f'val_{metric}'
        if val_key in history.history:
            plt.plot(history.history[val_key], label=f'Val {metric.capitalize()}')
        plt.title(f'Model {metric.capitalize()} over Epochs')
        plt.xlabel('Epochs')
        plt.ylabel(metric.capitalize())
        plt.legend()
        plt.grid(True, alpha=0.3)
        # Save as an image file (e.g., "metric_recall.png")
        filename = os.path.join(output_path,f"metric_{metric}.png")
        plt.savefig(filename)
        plt.close() # Important: close the figure to free up memory
        print(f"Saved: {filename}")

if __name__ == "__main__":

    # # Get all members of the module
    members = inspect.getmembers(raw_dataset_info)

    # Filter for objects that are instances of Dataset
    dataset_list = [obj for name, obj in members if isinstance(obj, Dataset)]

    # print(f"Found {len(dataset_list)} datasets.")

    # get_excluded_subfolders(r'/opt/DL_project/raw_dataset/',dataset_list)
    # generate_dataset_stats(r'/opt/DL_project/raw_dataset/', dataset_list, output_file=r'/opt/DL_project/raw_dataset/dataset_cloud_stats.json')
    # sort_dataset(r"/opt/DL_project/cut_dataset/",r"/opt/DL_project/sorted_dataset_cut/",r"/opt/DL_project/cut_dataset/test_yaafs_list.txt",r"/opt/DL_project/cut_dataset/val_yaafs_list.txt")
    # analyze_mask_folder(r'/opt/DL_project/sorted_dataset_cut/val/masks/')

    # normalize_dataset_polarity("/opt/DL_project/sorted_dataset_cut/","/opt/DL_project/sensors_list.txt","/opt/DL_project/sorted_dataset_cut_same_polarity/")
import keras
import keras.backend as K
from tqdm import tqdm
import os

import shutil
import re
from pathlib import Path
import numpy as np
import inspect
import raw_dataset_info  # The file containing dataset1, dataset2, etc.
from raw_dataset_info import Dataset # The class definition

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


def get_split_paths(target_dir, if_train):
    """
    Retrieves sorted lists of file paths for images and masks from a specific split.

    Args:
        target_dir (str): The root path of the processed dataset.
        if_train (bool): True for "train" Flase for "test".

    Returns:
        tuple: (image_paths, mask_paths) where each is a list of Path objects.
    """
    # Define the paths to the specific split folders
    split_path = Path(target_dir) / "train" if if_train else Path(target_dir) / "test"
    images_dir = split_path / "images"
    masks_dir = split_path / "masks"

    # Check if directories exist to avoid errors
    if not images_dir.exists() or not masks_dir.exists():
        print(f"Error: {if_train} directory structure not found in {target_dir}")
        return [], []

    # Get all .tif files and sort them to ensure matching indices
    image_paths = sorted(list(images_dir.glob("*.tif")))
    mask_paths = sorted(list(masks_dir.glob("*.tif")))

    # Simple validation to ensure parity
    if len(image_paths) != len(mask_paths):
        print(f"Warning: Mismatch in {if_train} set! "
              f"Images: {len(image_paths)}, Masks: {len(mask_paths)}")
        return [], []

    return image_paths, mask_paths

def get_input_image_names(data_folder_path, if_train=True):

    list_img, list_msk =  get_split_paths(data_folder_path, if_train)
    return list_img, list_msk
    
    # return list_img, list_test_ids


def sort_dataset(source_dir, target_dir, test_list_file):
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
    
    # Read the test list
    with open(test_list_file, 'r') as f:
        test_folders = {line.strip() for line in f if line.strip()}

    # Create target directory structure
    for split in ['train', 'test']:
        for folder in ['images', 'masks']:
            (target_path / split / folder).mkdir(parents=True, exist_ok=True)

    # Find and sort all numeric .tif files
    numeric_pattern = re.compile(r'^\d+\.tif$')
    image_files = [f for f in source_path.rglob("*.tif") if numeric_pattern.match(f.name)]
    image_files.sort() # Ensure consistent indexing order
    
    print(f"Found {len(image_files)} potential images. Processing...")

    # Manual counter to ensure continuous indexing for successful pairs
    current_index = 0

    for file_path in image_files:
        # Ignore any file if "demo" is in its folder path
        if "demo" in file_path.parts:
            continue
        # Determine split: test if any parent folder is in the test_folders list
        is_test = any(part in test_folders for part in file_path.parts)
        split = 'test' if is_test else 'train'
        
        # Look for the mask in the SAME folder as the image
        mask_path = file_path.parent / "no_land_no_water.tif"
        
        if mask_path.exists():
            # Get the folder name TWO levels upstream
            try:
                upstream_folder = file_path.parents[1].name
            except IndexError:
                upstream_folder = "unknown"

            # Construct filenames using the manual counter
            new_filename = f"{current_index:06d}_{upstream_folder}.tif"

            # Define destinations
            dest_img = target_path / split / 'images' / new_filename
            dest_mask = target_path / split / 'masks' / new_filename

            # Copy files
            shutil.copy2(file_path, dest_img)
            shutil.copy2(mask_path, dest_mask)
            
            # ONLY increment index if copy was successful
            current_index += 1
        else:
            # If mask is missing, we skip this image and the index does NOT increase
            print(f"Skipping: Mask missing for {file_path}")

    print(f"Process complete. Total paired files copied: {current_index}")



def get_cloud38_cdf(folder_path="/opt/DL_project/cloud38_dataset/", cdf_filename="cloud38_test_cdf_normalized"):
    cdf_path = os.path.join(folder_path, cdf_filename + ".npy")
    if os.path.isfile(cdf_path):
        cdf_normalized = np.load(cdf_path)
        return cdf_normalized
    else:
        print(f'cdf_path does not exist: {cdf_path}')
        exit(1)
 
def match_to_cdf(source_img, reference_cdf):
    # 1. Calculate source histogram and normalized CDF
    # We use 65536 bins for 16-bit depth
    src_values, src_unique_indices, src_counts = np.unique(source_img.ravel(),
                                                         return_inverse=True,
                                                         return_counts=True)
    src_cdf = np.cumsum(src_counts).astype(np.float64)
    src_cdf /= src_cdf[-1]  # <--- Normalized to 1.0
   
    # 2. Reference X-axis (all possible 16-bit values)
    ref_values = np.arange(len(reference_cdf))
   
    # 3. Map!
    # We look up where the src_cdf values would fall on the reference_cdf
    # reference_cdf must also be normalized (0.0 to 1.0)
    matched_values = np.interp(src_cdf, reference_cdf, ref_values)
   
    # 4. Reconstruct the image
    return matched_values[src_unique_indices].reshape(source_img.shape).astype(np.uint16)



# # Get all members of the module
# members = inspect.getmembers(raw_dataset_info)

# # Filter for objects that are instances of Dataset
# dataset_list = [obj for name, obj in members if isinstance(obj, Dataset)]

# print(f"Found {len(dataset_list)} datasets.")

# get_excluded_subfolders(r'/opt/DL_project/raw_dataset/',dataset_list)
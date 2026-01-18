import keras
import keras.backend as K
from tqdm import tqdm
import os

import shutil
import re
from pathlib import Path
import numpy as np

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
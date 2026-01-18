import keras
import keras.backend as K
from tqdm import tqdm
import os

import glob
import numpy as np
import os
import tifffile as tiff

def get_global_histogram(files_list, bins=65536):
    global_hist = np.zeros(bins)
    
    for f in files_list:
        img = tiff.imread(f)
        # Calculate histogram for this image
        hist, _ = np.histogram(img, bins=bins, range=(0, bins-1))
        global_hist += hist
        
    # Convert to a cumulative distribution function (CDF)
    cdf = global_hist.cumsum()
    cdf_normalized = cdf / cdf.max()
    return cdf_normalized


def create_and_save_global_histogram(folder_path="/opt/DL_project/cloud38_dataset/Test/", save_path="/opt/DL_project/cloud38_dataset/Test/cdf_normalized", bins=65536):
    subfolders = ["test_red", "test_green", "test_blue", "test_nir"]
    all_tifs = []
    for folder in subfolders:
        # This creates a path like: /path/to/dataset/red/*.tif
        pattern = os.path.join(folder_path, folder, "*.TIF")
        all_tifs.extend(glob.glob(pattern))
        
    cdf_normalized = get_global_histogram(all_tifs, bins)
    np.save(save_path, cdf_normalized)
    print(f"Global histogram saved to {save_path}")
    return cdf_normalized

def get_cloud38_cdf(folder_path="/opt/DL_project/cloud38_dataset/Test/", cdf_filename="cdf_normalized.npy", bins=65536):
    cdf_path = cdf_filename + ".npy"
    if os.path.isfile(cdf_path):
        cdf_normalized = np.load(cdf_path)
        return cdf_normalized
    else:
        return create_and_save_global_histogram(folder_path, cdf_filename, bins)

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
        print('\n***The last Basic Learning rate in this epoch is:', K.eval(optimizer.lr), '***\n')
        # stops the training if the basic lr is less than or equal to end_learning_rate
        if K.eval(optimizer.lr) <= self.end_lr:
            print("training is finished")
            self.model.stop_training = True


def get_input_image_names(list_names, directory_name, if_train=True):
    list_img = []
    list_msk = []
    list_test_ids = []

    for filenames in tqdm(list_names, miniters=1000):

        if if_train:
            dir_type_name = "train"
            fl_img = []
            nmask = 'gt_' + filenames
            fl_msk = directory_name + '/train_gt/' + '{}.TIF'.format(nmask)

        else:
            dir_type_name = "test"
            fl_img = []
            fl_id = os.path.basename(filenames)

        fl_img_red = filenames
        fl_img_green = filenames
        fl_img_blue = filenames
        fl_img_nir = filenames
        fl_img.append(fl_img_red)
        fl_img.append(fl_img_green)
        fl_img.append(fl_img_blue)
        fl_img.append(fl_img_nir)

        if os.path.isfile(fl_img[0]) and os.path.isfile(fl_img[1]) and os.path.isfile(fl_img[2]) and os.path.isfile(
                fl_img[3]):
            if if_train:
                list_msk.append(fl_msk)
                list_img.append(fl_img)
            else:
                list_test_ids.append(fl_id)

            list_img.append(fl_img)

    if if_train:
        return list_img, list_msk
    else:
        return list_img, list_test_ids


if __name__ == "__main__":
    # Example usage:
    create_and_save_global_histogram()
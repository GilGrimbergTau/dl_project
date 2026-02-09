import numpy as np
import os


def percentile_stretch_16bit(img, p_low=2, p_high=98):
    img = img.astype(np.float32)

    lo, hi = np.percentile(img, (p_low, p_high))
    img = np.clip(img, lo, hi)

    stretched = (img - lo) / (hi - lo)
    stretched = stretched * 65535.0

    return stretched.astype(np.uint16)

def percentile_clip(img, p_low=2, p_high=98):
    img = img.astype(np.float32)

    lo, hi = np.percentile(img, (p_low, p_high))
    img = np.clip(img, lo, hi)

    return img

######### CDF matching approach #########
def get_cloud38_cdf(folder_path="/opt/DL_project/cloud38_dataset/", cdf_filename="cloud38_test_cdf_normalized"):
    cdf_path = os.path.join(folder_path, cdf_filename + ".npy")
    if os.path.isfile(cdf_path):
        cdf_normalized = np.load(cdf_path)
        return cdf_normalized
    else:
        print(f'cdf_path does not exist: {cdf_path}')
        exit(1)
 
def get_cloud38_4_channels_cdfs(folder_path="/opt/DL_project/cloud38_dataset/", cdf_filenames=["cdf_red",
                                                                                             "cdf_green",
                                                                                             "cdf_blue",
                                                                                             "cdf_nir"]):
    cdfs = []
    for cdf_filename in cdf_filenames:
        cdf_path = os.path.join(folder_path, cdf_filename + ".npy")
        if os.path.isfile(cdf_path):
            cdf_normalized = np.load(cdf_path)
            cdfs.append(cdf_normalized)
        else:
            print(f'cdf_path does not exist: {cdf_path}')
            exit(1)

    return cdfs

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

def match_to_4_channels_cdf(source_img, reference_cdfs):
    # 1. Use list comprehension to handle matching
    matched_channels = [match_to_cdf(source_img, ref_cdf) for ref_cdf in reference_cdfs]

    # 2. Stack the list directly 
    return np.stack(matched_channels, axis=-1)


def match_histogram_preprocess(num_of_channels, max_possible_input_value, cdf, image):
    # clip outliers
    image = percentile_clip(image)
    
    if num_of_channels == 4:
        image = match_to_4_channels_cdf(image, cdf)
    elif num_of_channels == 1:
        image = match_to_cdf(image, cdf)
    else:
        print(f"Got illegal number of channels: {num_of_channels}! Exiting")
        exit(1)
    image = image.astype(np.float32)
    image /= max_possible_input_value
    return image

####################################

######### normalizations ###########

def per_image_normalize(img, num_of_channels):
    # Convert to float32 to prevent overflow/clipping during math
    img = img.astype(np.float32)
    # Calculate mean and variance across all pixels for each channel
    # axis=(0, 1) calculates stats per channel regardless of how many exist
    mean = np.mean(img, axis=(0, 1))
    std = np.std(img, axis=(0, 1))
    # Standardize: (x - mean) / std
    # We add a tiny epsilon (1e-8) to avoid division by zero if an image is a solid color
    normalized_img = (img - mean) / (std + 1e-8)
    
    if len(img.shape) == 2 and num_of_channels>1:
        # only 1 channel, stack images according to num_of_channels
        normalized_channels = [normalized_img for i in range(num_of_channels)]
        normalized_img = np.stack(normalized_channels, axis=-1)

    return normalized_img

# import cv2
# image = cv2.imread("/opt/DL_project/sorted_dataset_cut/train/images/014883_CaptiveC8_Night_2017_05_15Station_3F07_3_DS_netofa3_STPT_00302_UTC_19_35_45.tif", cv2.IMREAD_UNCHANGED)
# per_image_normalize(image,1)
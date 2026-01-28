import random
from skimage.io import imread
from skimage.transform import resize
import numpy as np
from augmentation import flipping_img_and_msk, rotate_cclk_img_and_msk, rotate_clk_img_and_msk, zoom_img_and_msk
from preprocess import get_cloud38_cdf, get_cloud38_4_channels_cdfs,match_histogram_preprocess, per_image_normalize
import cv2

from global_params import GEN_TRAIN, GEN_VAL, GEN_TEST, MAX_BIT, FINE_TUNE_NUM_OF_CHANNELS, PREPROC_NORM, PREPROC_MATCH_CDF
"""
Some lines borrowed from https://www.kaggle.com/petrosgk/keras-vgg19-0-93028-private-lb
"""


def mybatch_generator(zip_list, img_rows, img_cols, batch_size, num_of_channels=FINE_TUNE_NUM_OF_CHANNELS, gen_type=GEN_TRAIN,shuffle=True, max_possible_input_value=MAX_BIT, preprocess_type=PREPROC_MATCH_CDF):
    if preprocess_type == PREPROC_MATCH_CDF:
        if num_of_channels == 4:
            cdf = get_cloud38_4_channels_cdfs()
        elif num_of_channels == 1:
            cdf = get_cloud38_cdf()
        else:
            print(f"Got illegal number of channels: {num_of_channels}! Exiting")
            exit(1)
    
    number_of_batches = np.ceil(len(zip_list) / batch_size)
    if gen_type != GEN_TEST and shuffle:
        random.shuffle(zip_list)
    counter = 0
    
    while True:
        # if gen_type == GEN_TRAIN and shuffle:
        #     random.shuffle(zip_list)
        batch_files = zip_list[batch_size * counter:batch_size * (counter + 1)]
        image_list = []
        mask_list = []

        for file, mask in batch_files:
            image = cv2.imread(file,cv2.IMREAD_UNCHANGED)
            # if num_of_channels == 4:
            #     image_red = image_green = image_blue = image_nir = image
            #     image = np.stack((image_red, image_green, image_blue, image_nir), axis=-1)
            # elif num_of_channels == 1:
            #     pass
            # else:
            #     print(f"Got illegal number of channels: {num_of_channels}! Exiting")
            #     exit(1)
            mask = cv2.imread(mask, cv2.IMREAD_UNCHANGED)

            image = resize(image, (img_rows, img_cols), preserve_range=True, mode='symmetric')
            mask = resize(mask, (img_rows, img_cols), preserve_range=True, mode='symmetric')

            if gen_type == GEN_TRAIN:
                rnd_flip = np.random.randint(2, dtype=int)
                rnd_rotate_clk = np.random.randint(2, dtype=int)
                rnd_rotate_cclk = np.random.randint(2, dtype=int)
                rnd_zoom = np.random.randint(2, dtype=int)

                if rnd_flip == 1:
                    image, mask = flipping_img_and_msk(image, mask)

                if rnd_rotate_clk == 1:
                    image, mask = rotate_clk_img_and_msk(image, mask)

                if rnd_rotate_cclk == 1:
                    image, mask = rotate_cclk_img_and_msk(image, mask)

                if rnd_zoom == 1:
                    image, mask = zoom_img_and_msk(image, mask)

            mask = mask[..., np.newaxis]
            mask /= 255
            mask = (mask > 0.5).astype(np.float32)
            # image /= max_possible_input_value
            # image = percentile_stretch_16bit(image)
            if preprocess_type == PREPROC_MATCH_CDF:
                image = match_histogram_preprocess(num_of_channels, max_possible_input_value, cdf, image)
            elif preprocess_type == PREPROC_NORM:
                image = per_image_normalize(image, num_of_channels)
            else:
                print(f'unknown type of preprocessing was given: {preprocess_type}')
                exit(1)
            image_list.append(image)
            mask_list.append(mask)

        counter += 1
        image_list = np.array(image_list)
        mask_list = np.array(mask_list)
        yield (image_list, mask_list)

        if counter == number_of_batches:
            if gen_type == GEN_TRAIN and shuffle:
                random.shuffle(zip_list)
            counter = 0


# def mybatch_generator_validation(zip_list, img_rows, img_cols, batch_size, shuffle=False, max_possible_input_value=MAX_BIT):
#     number_of_batches = np.ceil(len(zip_list) / batch_size)
#     if shuffle:
#         random.shuffle(zip_list)
#     counter = 0

#     while True:

#         batch_files = zip_list[batch_size * counter:batch_size * (counter + 1)]
#         image_list = []
#         mask_list = []

#         for file, mask in batch_files:
#             image_red = cv2.imread(file,cv2.IMREAD_UNCHANGED)
#             image_green = cv2.imread(file,cv2.IMREAD_UNCHANGED)
#             image_blue = cv2.imread(file,cv2.IMREAD_UNCHANGED)
#             image_nir = cv2.imread(file,cv2.IMREAD_UNCHANGED)

#             mask = imread(mask)

#             image = np.stack((image_red, image_green, image_blue, image_nir), axis=-1)

#             image = resize(image, (img_rows, img_cols), preserve_range=True, mode='symmetric')
#             mask = resize(mask, (img_rows, img_cols), preserve_range=True, mode='symmetric')

#             mask = mask[..., np.newaxis]
#             mask /= 255
#             # image /= max_possible_input_value
#             image = percentile_stretch_16bit(image)
#             image_list.append(image)
#             mask_list.append(mask)

#         counter += 1
#         image_list = np.array(image_list)
#         mask_list = np.array(mask_list)
#         yield (image_list, mask_list)

#         if counter == number_of_batches:
#             counter = 0


def percentile_stretch_16bit(img, p_low=2, p_high=98):
    img = img.astype(np.float32)

    lo, hi = np.percentile(img, (p_low, p_high))
    img = np.clip(img, lo, hi)

    stretched = (img - lo) / (hi - lo)
    stretched = stretched * 65535.0

    return stretched.astype(np.uint16)

# def mybatch_generator_prediction(tstfiles, img_rows, img_cols, batch_size, max_possible_input_value=MAX_BIT):
#     number_of_batches = np.ceil(len(tstfiles) / batch_size)
#     counter = 0

#     while True:

#         beg = batch_size * counter
#         end = batch_size * (counter + 1)
#         batch_files = tstfiles[beg:end]
#         image_list = []

#         for file in batch_files:

#             image_red = cv2.imread(file[0],cv2.IMREAD_UNCHANGED)
#             image_green = cv2.imread(file[1],cv2.IMREAD_UNCHANGED)
#             image_blue = cv2.imread(file[2],cv2.IMREAD_UNCHANGED)
#             image_nir = cv2.imread(file[3],cv2.IMREAD_UNCHANGED)

#             image = np.stack((image_red, image_green, image_blue, image_nir), axis=-1)

#             image = resize (image, ( img_rows, img_cols), preserve_range=True, mode='symmetric')


#             # image /= max_possible_input_value
#             image = percentile_stretch_16bit(image)
#             image_list.append(image)

#         counter += 1
#         # print('counter = ', counter)
#         image_list = np.array(image_list)

#         yield (image_list,)

#         if counter == number_of_batches:
#             counter = 0


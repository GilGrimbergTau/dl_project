
from __future__ import print_function
import os
import numpy as np
import cloud_net_model
# from generators import mybatch_generator_prediction
from generators import mybatch_generator
import tifffile as tiff
import pandas as pd
from utils import get_input_image_names

from global_params import BATCH_SIZE, IN_ROWS, IN_COLS, FINE_TUNE_NUM_OF_CHANNELS, NUM_OF_CLASSES, MAX_BIT, GLOBAL_PATH, GEN_TEST

import cv2

def prediction():
    model = cloud_net_model.model_arch(input_rows=IN_ROWS,
                                       input_cols=IN_COLS,
                                       num_of_channels=FINE_TUNE_NUM_OF_CHANNELS,
                                       num_of_classes=NUM_OF_CLASSES)
    model.load_weights(weights_path)

    print("\nExperiment name: ", experiment_name)
    print("Prediction started... ")
    print("Input image size = ", (IN_ROWS, IN_COLS))
    print("Number of input spectral bands = ", FINE_TUNE_NUM_OF_CHANNELS)
    print("Batch size = ", BATCH_SIZE)

    imgs_mask_test = model.predict(
        mybatch_generator(list(zip(test_imgs, test_masks)), IN_ROWS, IN_COLS, BATCH_SIZE,num_of_channels=FINE_TUNE_NUM_OF_CHANNELS, max_possible_input_value=MAX_BIT, gen_type=GEN_TEST, shuffle=False),
        steps=np.int32(np.ceil(len(test_imgs) / BATCH_SIZE)))

    print("Saving predicted cloud masks on disk... \n")

    pred_dir = "sorted_dataset"
    if not os.path.exists(os.path.join(PRED_FOLDER, pred_dir)):
        os.mkdir(os.path.join(PRED_FOLDER, pred_dir))

    for pred_image, gt_mask  in zip(imgs_mask_test, test_masks):
        pred_image = (pred_image[:, :, 0]).astype(np.float32)
        image_name = os.path.basename(gt_mask).split(".")[0]
        cv2.imwrite(os.path.join(PRED_FOLDER, pred_dir, image_name + "_pred.tif"), pred_image)




# experiment_name = "Cloud-Net_trained_on_38-Cloud_training_patches"
experiment_name = "first_time_full_data_cut"
PRED_FOLDER = os.path.join(GLOBAL_PATH,'trained_models',experiment_name,'Predictions')
weights_path = os.path.join(GLOBAL_PATH,'trained_models',experiment_name, experiment_name + '.h5')


# getting input images names
# test_patches_csv_name = 'test_patches_38-cloud.csv'
# df_test_img = pd.read_csv(os.path.join(TEST_FOLDER, test_patches_csv_name))
dataset_folder = r"/opt/DL_project/sorted_dataset_cut/"
test_imgs, test_masks = get_input_image_names(dataset_folder, gen_type=GEN_TEST)

prediction()

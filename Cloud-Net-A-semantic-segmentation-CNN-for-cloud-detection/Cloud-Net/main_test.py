
from __future__ import print_function
import os
import numpy as np
import cloud_net_model
# from generators import mybatch_generator_prediction
from generators import mybatch_generator, GEN_TEST
import tifffile as tiff
import pandas as pd
from utils import get_input_image_names

import cv2

def prediction():
    model = cloud_net_model.model_arch(input_rows=in_rows,
                                       input_cols=in_cols,
                                       num_of_channels=num_of_channels,
                                       num_of_classes=num_of_classes)
    model.load_weights(weights_path)

    print("\nExperiment name: ", experiment_name)
    print("Prediction started... ")
    print("Input image size = ", (in_rows, in_cols))
    print("Number of input spectral bands = ", num_of_channels)
    print("Batch size = ", batch_sz)

    imgs_mask_test = model.predict(
        mybatch_generator(list(zip(test_imgs, test_masks)), in_rows, in_cols, batch_sz, max_possible_input_value=max_bit, gen_type=GEN_TEST, shuffle=False),
        steps=np.int32(np.ceil(len(test_imgs) / batch_sz)))

    print("Saving predicted cloud masks on disk... \n")

    pred_dir = "raw_dataset"
    if not os.path.exists(os.path.join(PRED_FOLDER, pred_dir)):
        os.mkdir(os.path.join(PRED_FOLDER, pred_dir))

    for pred_image, gt_mask  in zip(imgs_mask_test, test_masks):
        pred_image = (pred_image[:, :, 0]).astype(np.float32)
        image_name = os.path.basename(gt_mask).split(".")[0]
        cv2.imwrite(os.path.join(PRED_FOLDER, pred_dir, image_name + "_pred"), pred_image)

GLOBAL_PATH = '/opt/DL_project/cloud38_dataset/'
TRAIN_FOLDER = os.path.join(GLOBAL_PATH, 'Training')
TEST_FOLDER = os.path.join(GLOBAL_PATH, 'Test')
PRED_FOLDER = os.path.join(GLOBAL_PATH, 'Predictions')


in_rows = 384
in_cols = 384
num_of_channels = 4
num_of_classes = 1
batch_sz = 1
max_bit = 65535  # maximum gray level in landsat 8 images
experiment_name = "Cloud-Net_trained_on_38-Cloud_training_patches"
weights_path = os.path.join(GLOBAL_PATH, experiment_name + '.h5')


# getting input images names
test_patches_csv_name = 'test_patches_38-cloud.csv'
# df_test_img = pd.read_csv(os.path.join(TEST_FOLDER, test_patches_csv_name))
df_test_img = ["/opt/DL_project/raw_dataset/00018900.tif"]
test_imgs, test_masks = get_input_image_names(df_test_img, TEST_FOLDER, if_train=False)

prediction()

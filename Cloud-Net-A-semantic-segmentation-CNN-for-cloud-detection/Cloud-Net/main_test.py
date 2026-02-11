
from __future__ import print_function
import os
import numpy as np
import cloud_net_model
# from generators import mybatch_generator_prediction
from generators import mybatch_generator
import tifffile as tiff
import pandas as pd
from utils import get_input_image_names, find_worst_predictions
from skimage.transform import resize
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, jaccard_score

from global_params import BATCH_SIZE, IN_ROWS, IN_COLS, FINE_TUNE_NUM_OF_CHANNELS, NUM_OF_CLASSES, MAX_BIT, GLOBAL_PATH, GEN_TEST, PREPROC_MATCH_CDF, PREPROC_PER_IMAGE_NORM
import datetime
import cv2

def get_masks(masks_path_list, batch_size, img_rows, img_cols):
    counter = 0
    number_of_batches = np.ceil(len(masks_path_list) / batch_size)
    masks_list = []
    batch_files = masks_path_list[batch_size * counter:batch_size * (counter + 1)]    
    while (counter < number_of_batches):
        for mask_path in batch_files:
            mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
            mask = resize(mask, (img_rows, img_cols), preserve_range=True, mode='symmetric')
            mask = mask[..., np.newaxis]
            mask /= 255
            mask = (mask > 0.5).astype(np.float32)
            masks_list.append(mask)
        counter += 1
        batch_files = masks_path_list[batch_size * counter:batch_size * (counter + 1)]    

    masks_list = np.array(masks_list)
    return masks_list

def prediction(preprocess = PREPROC_MATCH_CDF):
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

    predicted_masks = model.predict(
        mybatch_generator(list(zip(test_imgs, test_masks)), IN_ROWS, IN_COLS, BATCH_SIZE,num_of_channels=FINE_TUNE_NUM_OF_CHANNELS, max_possible_input_value=MAX_BIT, gen_type=GEN_TEST, shuffle=False, preprocess_type=preprocess),
        steps=np.int32(np.ceil(len(test_imgs) / BATCH_SIZE)))
    
    if not os.path.exists(PRED_FOLDER):
        os.mkdir(PRED_FOLDER)
    # model.evaluate(mybatch_generator(list(zip(test_imgs, test_masks)), IN_ROWS, IN_COLS, BATCH_SIZE,num_of_channels=FINE_TUNE_NUM_OF_CHANNELS, max_possible_input_value=MAX_BIT, gen_type=GEN_TEST, shuffle=False))
    # Convert lists to numpy arrays for easier handling
    y_true = get_masks(test_masks, BATCH_SIZE, IN_ROWS, IN_COLS)

    y_pred = (predicted_masks > 0.5).astype(np.float32)

    # Find worst predictions
    find_worst_predictions(y_true,y_pred,test_imgs,test_masks,PRED_FOLDER,metric="precision",n=10)
    
    # Flatten the arrays to compute pixel-wise metrics
    y_true_flat = y_true.flatten()
    y_pred_flat = y_pred.flatten()

    # Compute Precision, Recall, and F1-Score
    precision = precision_score(y_true_flat, y_pred_flat)
    recall = recall_score(y_true_flat, y_pred_flat)
    specificity = recall_score(y_true_flat, y_pred_flat, pos_label=0)
    accuracy = accuracy_score(y_true_flat, y_pred_flat)
    f1 = f1_score(y_true_flat, y_pred_flat)
    jaccard = jaccard_score(y_true_flat, y_pred_flat, zero_division=1)

    print("Saving metrics to file (accuracy, precision, recall, etc.)\n\n")
    with open(os.path.join(PRED_FOLDER,f'test_performance_{datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")}.txt') ,'w') as metrics_file:
        metrics_file.write(f'Metrics of test predictions for model {experiment_name}:\n\n')
        metrics_file.write(f'Accuracy = {accuracy}\n')
        metrics_file.write(f'Precision = {precision}\n')
        metrics_file.write(f'Recall = {recall}\n')
        metrics_file.write(f'Specificity = {specificity}\n')
        metrics_file.write(f'F1 score = {f1}\n')
        metrics_file.write(f'Jaccard score = {jaccard}\n')
    print("Saving predicted cloud masks on disk... \n")
    for pred_image, gt_mask  in zip(predicted_masks, test_masks):
        pred_image = (pred_image[:, :, 0]).astype(np.float32)
        image_name = os.path.basename(gt_mask).split(".")[0]
        cv2.imwrite(os.path.join(PRED_FOLDER, image_name + "_pred.tif"), pred_image)


dataset_folder = r"/opt/DL_project/sorted_dataset_cut/"

for experiment_name in ["data_cut_loss_Jaccard_Bce_Combined_0_1_preprocess_standardizations_4_ch_pretrained"]:
    # experiment_name = "Cloud-Net_trained_on_38-Cloud_training_patches"
    PRED_FOLDER = os.path.join(GLOBAL_PATH,'trained_models',experiment_name,'Predictions')
    weights_path = os.path.join(GLOBAL_PATH,'trained_models',experiment_name, experiment_name + '.h5')


    # getting input images names
    # test_patches_csv_name = 'test_patches_38-cloud.csv'
    # df_test_img = pd.read_csv(os.path.join(TEST_FOLDER, test_patches_csv_name))
    test_imgs, test_masks = get_input_image_names(dataset_folder, gen_type=GEN_TEST)

    prediction(preprocess=PREPROC_PER_IMAGE_NORM)

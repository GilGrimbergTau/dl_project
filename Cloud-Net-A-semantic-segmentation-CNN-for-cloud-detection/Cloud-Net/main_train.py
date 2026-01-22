
from __future__ import print_function
from sklearn.model_selection import train_test_split
import os
import numpy as np
from utils import ADAMLearningRateTracker
import cloud_net_model
from losses import jacc_coef
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, CSVLogger
# from generators import mybatch_generator_train, mybatch_generator_validation
from generators import mybatch_generator
import pandas as pd
from utils import get_input_image_names
from keras import models,layers
import tensorflow as tf
from pathlib import Path

from global_params import BATCH_SIZE, IN_ROWS, IN_COLS, PRETRAINED_NUM_OF_CHANNELS,FINE_TUNE_NUM_OF_CHANNELS, NUM_OF_CLASSES, MAX_BIT, STARTING_LAERNING_RATE, END_LEARNING_RATE, MAX_NUM_OF_EPOCHS, MAX_NUM_OF_EPOCHS_FIRST_LAYER_ONLY, VAL_RATIO, PATIENCE, DACEY_FACTOR, GLOBAL_PATH, GEN_TRAIN, GEN_VAL, GEN_TEST


def check_trainability(model):
    trainable_count = np.sum([tf.keras.backend.count_params(w) for w in model.trainable_weights])
    non_trainable_count = np.sum([tf.keras.backend.count_params(w) for w in model.non_trainable_weights])
    print(f"Trainable params: {trainable_count:,}")
    print(f"Non-trainable params: {non_trainable_count:,}")


def train():
    model = cloud_net_model.model_arch(input_rows=IN_ROWS,
                                       input_cols=IN_COLS,
                                       num_of_channels=PRETRAINED_NUM_OF_CHANNELS,
                                       num_of_classes=NUM_OF_CLASSES)
    # model.summary()

    model_checkpoint = ModelCheckpoint(new_weights_path, monitor='val_loss', save_best_only=True)
    lr_reducer = ReduceLROnPlateau(factor=DACEY_FACTOR, cooldown=0, patience=PATIENCE, min_lr=END_LEARNING_RATE, verbose=1)
    csv_logger = CSVLogger(experiment_name + '_log_1.log')

    # train_img_split, val_img_split, train_msk_split, val_msk_split = train_test_split(train_img, train_msk,
    #                                                                                   test_size=VAL_RATIO,
    #                                                                                   random_state=42, shuffle=True)

    if train_resume:
        model.load_weights(trained_weights_path)
        print("\nTraining resumed...")
        # 2. Extract weights from the original first conv layer
        # Usually index 1 if index 0 is the InputLayer
        old_first_layer = model.layers[1] 
        weights, biases = old_first_layer.get_weights()

        # weights shape is (h, w, 4, filters)
        # We need to transform it to (h, w, 1, filters)
        # Strategy: Averaging the weights across the channel axis
        new_weights = np.mean(weights, axis=2, keepdims=True)

        new_model = cloud_net_model.model_arch(input_rows=IN_ROWS, input_cols=IN_COLS, num_of_channels=FINE_TUNE_NUM_OF_CHANNELS)

        # Set the transformed weights to the first Conv2D layer of the new model
        new_model.layers[1].set_weights([new_weights, biases])

        # Copy all other weights for the remaining layers
        # We skip the first layer (index 1) because we just set it manually
        for i in range(2, len(new_model.layers)):
            new_model.layers[i].set_weights(model.layers[i].get_weights())

        model = new_model
        print("Weights successfully transferred to 1-channel model.")
        # 1. Freeze all layers
        model.trainable = True # Start with everything enabled
        for layer in model.layers:
            layer.trainable = False

        # 2. Unfreeze only the first Conv2D layer
        # index 0 is Input, index 1 is the first Conv2D
        model.layers[1].trainable = True
        # 3. Compile the model (Crucial: changes to 'trainable' require re-compiling)
        model.compile(optimizer=Adam(learning_rate=STARTING_LAERNING_RATE), loss=jacc_coef, metrics=[jacc_coef])
        check_trainability(model)
        # 4. Train for a few epochs
        model.fit(
        mybatch_generator(list(zip(train_img_split, train_msk_split)), IN_ROWS, IN_COLS, BATCH_SIZE,num_of_channels=FINE_TUNE_NUM_OF_CHANNELS, max_possible_input_value=MAX_BIT, gen_type=GEN_TRAIN),
        steps_per_epoch=np.int32(np.ceil(len(train_img_split) / BATCH_SIZE)), epochs=MAX_NUM_OF_EPOCHS_FIRST_LAYER_ONLY, verbose=1,
        validation_data=mybatch_generator(list(zip(val_img_split, val_msk_split)), IN_ROWS, IN_COLS, BATCH_SIZE,num_of_channels=FINE_TUNE_NUM_OF_CHANNELS, max_possible_input_value=MAX_BIT, gen_type=GEN_VAL),
        validation_steps=np.int32(np.ceil(len(val_img_split) / BATCH_SIZE)),
        callbacks=[model_checkpoint, lr_reducer, ADAMLearningRateTracker(END_LEARNING_RATE), csv_logger])
        # 1. Unfreeze everything
        for layer in model.layers:
            layer.trainable = True

        # 2. Re-compile
        model.compile(optimizer=Adam(learning_rate=STARTING_LAERNING_RATE), loss=jacc_coef, metrics=[jacc_coef])
        check_trainability(model)
    else:
        print("\nTraining started from scratch... ")
        model.compile(optimizer=Adam(learning_rate=STARTING_LAERNING_RATE), loss=jacc_coef, metrics=[jacc_coef])
        check_trainability(model)
    print("Experiment name: ", experiment_name)
    print("Input image size: ", (IN_ROWS, IN_COLS))
    print("Number of input spectral bands: ", FINE_TUNE_NUM_OF_CHANNELS)
    print("Learning rate: ", STARTING_LAERNING_RATE)
    print("Batch size: ", BATCH_SIZE, "\n")

    
    model.fit(
        mybatch_generator(list(zip(train_img_split, train_msk_split)), IN_ROWS, IN_COLS, BATCH_SIZE,num_of_channels=FINE_TUNE_NUM_OF_CHANNELS, max_possible_input_value=MAX_BIT, gen_type=GEN_TRAIN),
        steps_per_epoch=np.int32(np.ceil(len(train_img_split) / BATCH_SIZE)), epochs=MAX_NUM_OF_EPOCHS, verbose=1,
        validation_data=mybatch_generator(list(zip(val_img_split, val_msk_split)), IN_ROWS, IN_COLS, BATCH_SIZE,num_of_channels=FINE_TUNE_NUM_OF_CHANNELS, max_possible_input_value=MAX_BIT, gen_type=GEN_VAL),
        validation_steps=np.int32(np.ceil(len(val_img_split) / BATCH_SIZE)),
        callbacks=[model_checkpoint, lr_reducer, ADAMLearningRateTracker(END_LEARNING_RATE), csv_logger])


# TRAIN_FOLDER = os.path.join(GLOBAL_PATH, 'Training')
# TEST_FOLDER = os.path.join(GLOBAL_PATH, 'Test')


experiment_name = "first_time_full_data_cut"
# create folder in trained_models
experiment_folder = Path(os.path.join(GLOBAL_PATH,"trained_models",experiment_name))
experiment_folder.mkdir(parents=True, exist_ok=True)

new_weights_path = os.path.join(experiment_folder._str,f"{experiment_name}.h5")
trained_weights_path = os.path.join(GLOBAL_PATH, "cloud38_dataset/Cloud-Net_trained_on_38-Cloud_training_patches.h5")
train_resume = True

# getting input images names
# train_patches_csv_name = 'training_patches_38-cloud.csv'
# df_train_img = pd.read_csv(os.path.join(TRAIN_FOLDER, train_patches_csv_name))
dataset_folder = os.path.join(GLOBAL_PATH,r'sorted_dataset_cut')
train_img_split, train_msk_split = get_input_image_names(dataset_folder, gen_type=GEN_TRAIN)
val_img_split, val_msk_split = get_input_image_names(dataset_folder, gen_type=GEN_VAL)

train()

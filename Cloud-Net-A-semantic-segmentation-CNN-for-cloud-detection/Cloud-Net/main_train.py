
from __future__ import print_function
from sklearn.model_selection import train_test_split
import os
import numpy as np
from utils import ADAMLearningRateTracker, save_history_plots
import cloud_net_model
from losses import jacc_coef, filtered_jaccard_loss_v1, filtered_jaccard_loss_v1_no_weights, filtered_jaccard_loss_v1_no_exp, filtered_jaccard_loss_small_m, jacc_bce_combined
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, CSVLogger
# from generators import mybatch_generator_train, mybatch_generator_validation
from generators import mybatch_generator
import pandas as pd
from utils import get_input_image_names
from keras import models,layers
import tensorflow as tf
from pathlib import Path
import datetime
import sys

from global_params import BATCH_SIZE, IN_ROWS, IN_COLS, PRETRAINED_NUM_OF_CHANNELS,FINE_TUNE_NUM_OF_CHANNELS, NUM_OF_CLASSES, MAX_BIT, STARTING_LAERNING_RATE, END_LEARNING_RATE, MAX_NUM_OF_EPOCHS, PATIENCE, DACEY_FACTOR, GLOBAL_PATH, GEN_TRAIN, GEN_VAL, TRAINED_WEIGHTS_PATH, TRAIN_RESUME, EARLY_STOP_PATIENCE


def check_trainability(model):
    trainable_count = np.sum([tf.keras.backend.count_params(w) for w in model.trainable_weights])
    non_trainable_count = np.sum([tf.keras.backend.count_params(w) for w in model.non_trainable_weights])
    print(f"Trainable params: {trainable_count:,}")
    print(f"Non-trainable params: {non_trainable_count:,}")


def train(loss_fn, first_layer_max_epochs,experiment_folder,experiment_name,new_weights_path,train_img_split, train_msk_split,val_img_split, val_msk_split):
    model = cloud_net_model.model_arch(input_rows=IN_ROWS,
                                       input_cols=IN_COLS,
                                       num_of_channels=PRETRAINED_NUM_OF_CHANNELS,
                                       num_of_classes=NUM_OF_CLASSES)
    # model.summary()

    model_checkpoint = ModelCheckpoint(new_weights_path, monitor='val_loss', save_best_only=True)
    lr_reducer = ReduceLROnPlateau(factor=DACEY_FACTOR, cooldown=0, patience=PATIENCE, min_lr=END_LEARNING_RATE, verbose=1)
    csv_logger = CSVLogger(os.path.join(experiment_folder._str,experiment_name + '.log'))
    # Define metrics
    metrics = [jacc_coef,
        tf.metrics.BinaryAccuracy(name='accuracy'),
        tf.metrics.Precision(name='precision'),
        tf.metrics.Recall(name='recall')
    ]
    if TRAIN_RESUME and FINE_TUNE_NUM_OF_CHANNELS==1:
        model.load_weights(TRAINED_WEIGHTS_PATH)
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
        model.compile(optimizer=Adam(learning_rate=STARTING_LAERNING_RATE), loss=loss_fn, metrics=metrics)
        check_trainability(model)
        # Create a log directory
        first_layer_logdir = os.path.join(experiment_folder,"logs/first_layer_logs/","loss_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        csv_first_layer_logger = CSVLogger(os.path.join(experiment_folder._str,'_first_layer_only.log'))
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=first_layer_logdir)
        # 4. Train for a few epochs
        first_layer_history = model.fit(
            mybatch_generator(list(zip(train_img_split, train_msk_split)), IN_ROWS, IN_COLS, BATCH_SIZE,num_of_channels=FINE_TUNE_NUM_OF_CHANNELS, max_possible_input_value=MAX_BIT, gen_type=GEN_TRAIN),
            steps_per_epoch=np.int32(np.ceil(len(train_img_split) / BATCH_SIZE)), epochs=first_layer_max_epochs, verbose=1,
            validation_data=mybatch_generator(list(zip(val_img_split, val_msk_split)), IN_ROWS, IN_COLS, BATCH_SIZE,num_of_channels=FINE_TUNE_NUM_OF_CHANNELS, max_possible_input_value=MAX_BIT, gen_type=GEN_VAL, shuffle=False),
            validation_steps=np.int32(np.ceil(len(val_img_split) / BATCH_SIZE)),
            callbacks=[model_checkpoint, lr_reducer, ADAMLearningRateTracker(END_LEARNING_RATE), csv_first_layer_logger, tensorboard_callback])
        # save history
        save_history_plots(first_layer_history,first_layer_logdir)
        # Unfreeze everything
        for layer in model.layers:
            layer.trainable = True


    elif TRAIN_RESUME and FINE_TUNE_NUM_OF_CHANNELS==4:
        model.load_weights(TRAINED_WEIGHTS_PATH)
        print("\nTraining resumed...")

    else:
        print("\nTraining started from scratch... ")

    model.compile(optimizer=Adam(learning_rate=STARTING_LAERNING_RATE), loss=loss_fn, metrics=metrics)
    check_trainability(model)
    print("Experiment name: ", experiment_name)
    print("Input image size: ", (IN_ROWS, IN_COLS))
    print("Number of input spectral bands: ", FINE_TUNE_NUM_OF_CHANNELS)
    print("Learning rate: ", STARTING_LAERNING_RATE)
    print("Batch size: ", BATCH_SIZE, "\n")

    # Create a log directory
    logdir = os.path.join(experiment_folder,"logs/all_model_loss/","loss_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)
    earlyStop_callback = tf.keras.callbacks.EarlyStopping(
                monitor='val_loss', 
                patience=EARLY_STOP_PATIENCE, 
                restore_best_weights=True, # Automatically reverts model to best state
                verbose=1
            )
    history = model.fit(
        mybatch_generator(list(zip(train_img_split, train_msk_split)), IN_ROWS, IN_COLS, BATCH_SIZE,num_of_channels=FINE_TUNE_NUM_OF_CHANNELS, max_possible_input_value=MAX_BIT, gen_type=GEN_TRAIN),
        steps_per_epoch=np.int32(np.ceil(len(train_img_split) / BATCH_SIZE)), epochs=MAX_NUM_OF_EPOCHS, verbose=1,
        validation_data=mybatch_generator(list(zip(val_img_split, val_msk_split)), IN_ROWS, IN_COLS, BATCH_SIZE,num_of_channels=FINE_TUNE_NUM_OF_CHANNELS, max_possible_input_value=MAX_BIT, gen_type=GEN_VAL),
        validation_steps=np.int32(np.ceil(len(val_img_split) / BATCH_SIZE)),
        callbacks=[model_checkpoint, lr_reducer, ADAMLearningRateTracker(END_LEARNING_RATE), csv_logger, tensorboard_callback, earlyStop_callback])
    # save history
    save_history_plots(history,logdir)
if __name__ == "__main__":

    # getting input images names
    dataset_folder = os.path.join(GLOBAL_PATH,r'sorted_dataset_cut')
    train_img_split, train_msk_split = get_input_image_names(dataset_folder, gen_type=GEN_TRAIN)
    val_img_split, val_msk_split = get_input_image_names(dataset_folder, gen_type=GEN_VAL)
    # Define your hyperparameter sets
    losses = {"Jaccard_Bce_Combined_0_3":jacc_bce_combined,"Jaccard": jacc_coef}
    if len(sys.argv) > 1:
        loss_name = sys.argv[1]
        loss_fn = losses[loss_name]
    else:
        print("no loss names where given!")
        exit(1)
    # first_layer_epochs_options = [5, 15]
    first_layer_epochs_options = ["4_ch"]
    for first_layer_max_epochs in first_layer_epochs_options:
        experiment_name = f"data_cut_{loss_name}_first_layer_max_epochs_{first_layer_max_epochs}"
        print(f"Start training for experiment {experiment_name}:\n")

        # create folder in trained_models
        experiment_folder = Path(os.path.join(GLOBAL_PATH,"trained_models",experiment_name))
        experiment_folder.mkdir(parents=True, exist_ok=True)

        new_weights_path = os.path.join(experiment_folder._str,f"{experiment_name}.h5")
        try:
            train(loss_fn, first_layer_max_epochs,experiment_folder,experiment_name,new_weights_path,train_img_split, train_msk_split,val_img_split, val_msk_split)
        except Exception as e:
            print(f"Exception raised while training: {experiment_name}.\nThe error: {e}")
            with open(os.path.join(experiment_folder,"crash_log.txt"), 'w') as crash_log:
                crash_log.write(f'exception raised while training. the error:{e}')
        
        print(f"Training for experiment {experiment_name} is done.\n")
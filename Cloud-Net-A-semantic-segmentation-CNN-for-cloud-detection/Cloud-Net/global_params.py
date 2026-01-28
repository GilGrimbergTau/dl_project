import os

IN_ROWS = 192
IN_COLS = 192
PRETRAINED_NUM_OF_CHANNELS = 4
FINE_TUNE_NUM_OF_CHANNELS = 4
NUM_OF_CLASSES = 1
STARTING_LAERNING_RATE = 1e-4
END_LEARNING_RATE = 1e-8
MAX_NUM_OF_EPOCHS = 500  # just a huge number. The actual training should not be limited by this value
# MAX_NUM_OF_EPOCHS_FIRST_LAYER_ONLY = 5
VAL_RATIO = 0.2
PATIENCE = 15
EARLY_STOP_PATIENCE = 100
DACEY_FACTOR = 0.7
BATCH_SIZE = 12
MAX_BIT = 65535  # maximum gray level in landsat 8 images
GLOBAL_PATH = '/opt/DL_project/'

# Cloud-Net pretrained weights
TRAINED_WEIGHTS_PATH = os.path.join(GLOBAL_PATH, "cloud38_dataset/Cloud-Net_trained_on_38-Cloud_training_patches.h5")
# resuming the last training (Cloud-Net best model)
TRAIN_RESUME = True

GEN_TRAIN = "gen_train"
GEN_VAL = "gen_val"
GEN_TEST = "gen_test"

PREPROC_NORM = "preprocess_standardizations"
PREPROC_MATCH_CDF = "preprocess_match_cdf"
# TOTAL_SUM_OF_CLOUDS_PIXELS = 93314867
# TOATL_SUM_OF_BACKGROUND_PIXELS = 1612124365
# TOTAL_SUM_OF_PIXELS = TOTAL_SUM_OF_CLOUDS_PIXELS + TOATL_SUM_OF_BACKGROUND_PIXELS
# clouds_weight = TOTAL_SUM_OF_PIXELS/(2*TOTAL_SUM_OF_CLOUDS_PIXELS)
# background_weight = TOTAL_SUM_OF_PIXELS/(2*TOATL_SUM_OF_BACKGROUND_PIXELS)

# weights for cut images
CLOUDS_WEIGHT = 9.138089603664119
BACKGROUND_WEIGHT = 0.5289415844788128

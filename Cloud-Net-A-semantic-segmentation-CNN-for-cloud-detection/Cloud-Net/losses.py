from keras import backend as K
import tensorflow as tf
from global_params import CLOUDS_WEIGHT, BACKGROUND_WEIGHT
smooth = 0.0000001


def jacc_coef(y_true, y_pred):
    y_true_f = tf.keras.layers.Flatten()(y_true)
    y_pred_f = tf.keras.layers.Flatten()(y_pred)
    intersection = tf.reduce_sum(y_true_f * y_pred_f)
    return 1 - ((intersection + smooth) / (tf.reduce_sum(y_true_f) + tf.reduce_sum(y_pred_f) - intersection + smooth))
 
def inv_jacc_coef(y_true, y_pred):
    return jacc_coef(1.0 - y_true, 1.0 - y_pred)

# FJL Version 1: Multiplicative (Equation 6)
# Penalizes the combination of foreground and background Jaccard indices.
def filtered_jaccard_loss_v1(y_true, y_pred, k_g=1, k_j=1, m=1000, p_c=0.5):
    s = tf.reduce_sum(y_true)
    
    g_l_numerator = k_g * inv_jacc_coef(y_true, y_pred)
    j_l_numerator = k_j * jacc_coef(y_true, y_pred)
    
    g_l_denominator = 1 + tf.exp(m*(s-p_c))
    j_l_denominator = 1 + tf.exp(m*(-s+p_c))

    fjl = BACKGROUND_WEIGHT * (g_l_numerator/g_l_denominator) + CLOUDS_WEIGHT * (j_l_numerator/j_l_denominator)
    return fjl

def filtered_jaccard_loss_v1_no_weights(y_true, y_pred, k_g=1, k_j=1, m=1000, p_c=0.5):
    s = tf.reduce_sum(y_true)
    
    g_l_numerator = k_g * inv_jacc_coef(y_true, y_pred)
    j_l_numerator = k_j * jacc_coef(y_true, y_pred)
    
    g_l_denominator = 1 + tf.exp(m*(s-p_c))
    j_l_denominator = 1 + tf.exp(m*(-s+p_c))

    fjl = g_l_numerator/g_l_denominator + j_l_numerator/j_l_denominator
    return fjl

def filtered_jaccard_loss_v1_no_exp(y_true, y_pred, k_g=1, k_j=1, m=1000, p_c=0.5):
    s = tf.reduce_sum(y_true)
    
    g_l_numerator = k_g * inv_jacc_coef(y_true, y_pred)
    j_l_numerator = k_j * jacc_coef(y_true, y_pred)
    
    # g_l_denominator = 1 + tf.exp(m*(s-p_c))
    # j_l_denominator = 1 + tf.exp(m*(-s+p_c))

    fjl = BACKGROUND_WEIGHT * g_l_numerator + CLOUDS_WEIGHT * j_l_numerator
    return fjl

def filtered_jaccard_loss_small_m(y_true, y_pred):
    return filtered_jaccard_loss_v1(y_true,y_pred, m=10)




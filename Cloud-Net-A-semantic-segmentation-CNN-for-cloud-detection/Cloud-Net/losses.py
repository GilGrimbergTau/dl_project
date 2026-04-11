from keras import backend as K
import tensorflow as tf
from global_params import CLOUDS_WEIGHT, BACKGROUND_WEIGHT
smooth = 0.0000001

def focal_loss_func(y_true, y_pred, alpha=0.25, gamma=2.0):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    # Binary Cross Entropy base
    bce = tf.keras.losses.BinaryCrossentropy()(y_true, y_pred)
    
    # Calculate modulating factor
    p_t = (y_true * y_pred) + ((1 - y_true) * (1 - y_pred))
    alpha_factor = y_true * alpha + (1 - y_true) * (1 - alpha)

    focal = alpha_factor * tf.pow((1 - p_t), gamma) * bce
    focal_loss = tf.reduce_mean(focal)
    return focal_loss

def jacc_coef(y_true, y_pred):
    y_true_f = tf.keras.layers.Flatten()(y_true)
    y_pred_f = tf.keras.layers.Flatten()(y_pred)
    intersection = tf.reduce_sum(y_true_f * y_pred_f)
    return 1 - ((intersection + smooth) / (tf.reduce_sum(y_true_f) + tf.reduce_sum(y_pred_f) - intersection + smooth))
 
def inv_jacc_coef(y_true, y_pred):
    return jacc_coef(1.0 - y_true, 1.0 - y_pred)

def jacc_bce_combined(y_true, y_pred, alpha = 0.1):
    # Standard Binary Cross Entropy
    bce = tf.keras.losses.BinaryCrossentropy()(y_true, y_pred)
    jacc = jacc_coef(y_true, y_pred)

    return alpha*bce + (1-alpha)*jacc

def hybrid_cloud_loss(alpha=0.25, gamma=2.0, jaccard_weight=0.5):
    """
    Hybrid Loss: Combined Focal Loss and Soft Jaccard Loss.
    
    Args:
        alpha: Weight for the cloud class (0.25 is standard, increase if missing clouds).
        gamma: Focusing parameter (2.0 is standard, increase for noisier labels).
        jaccard_weight: How much to favor Jaccard vs Focal. 0.5 is a good balance.
    """
    def loss(y_true, y_pred):

        # focal loss
        focal_loss = focal_loss_func(y_true, y_pred, alpha, gamma)
        # jaccard
        jaccard_loss = jacc_coef(y_true, y_pred)
        # Weighted sum of both losses
        return (1 - jaccard_weight) * focal_loss + (jaccard_weight * jaccard_loss)

    return loss

# # FJL Version 1: Multiplicative (Equation 6)
# # Penalizes the combination of foreground and background Jaccard indices.
# def filtered_jaccard_loss_v1(y_true, y_pred, k_g=1, k_j=1, m=1000, p_c=0.5):
#     s = tf.reduce_sum(y_true)
    
#     g_l_numerator = k_g * inv_jacc_coef(y_true, y_pred)
#     j_l_numerator = k_j * jacc_coef(y_true, y_pred)
    
#     g_l_denominator = 1 + tf.exp(m*(s-p_c))
#     j_l_denominator = 1 + tf.exp(m*(-s+p_c))

#     fjl = BACKGROUND_WEIGHT * (g_l_numerator/g_l_denominator) + CLOUDS_WEIGHT * (j_l_numerator/j_l_denominator)
#     return fjl

# def filtered_jaccard_loss_v1_no_weights(y_true, y_pred, k_g=1, k_j=1, m=1000, p_c=0.5):
#     s = tf.reduce_sum(y_true)
    
#     g_l_numerator = k_g * inv_jacc_coef(y_true, y_pred)
#     j_l_numerator = k_j * jacc_coef(y_true, y_pred)
    
#     g_l_denominator = 1 + tf.exp(m*(s-p_c))
#     j_l_denominator = 1 + tf.exp(m*(-s+p_c))

#     fjl = g_l_numerator/g_l_denominator + j_l_numerator/j_l_denominator
#     return fjl

# def filtered_jaccard_loss_v1_no_exp(y_true, y_pred, k_g=1, k_j=1, m=1000, p_c=0.5):
#     s = tf.reduce_sum(y_true)
    
#     g_l_numerator = k_g * inv_jacc_coef(y_true, y_pred)
#     j_l_numerator = k_j * jacc_coef(y_true, y_pred)
    
#     # g_l_denominator = 1 + tf.exp(m*(s-p_c))
#     # j_l_denominator = 1 + tf.exp(m*(-s+p_c))

#     fjl = BACKGROUND_WEIGHT * g_l_numerator + CLOUDS_WEIGHT * j_l_numerator
#     return fjl

# def filtered_jaccard_loss_small_m(y_true, y_pred):
#     return filtered_jaccard_loss_v1(y_true,y_pred, m=10)




import numpy as np
import keras.backend as K


def vgg_perceptual_mse_loss(loss_model, weights=[1.0, 1.0]):

    def vgg_perceptual_mse(y_true, y_pred):
        epsilon = 1e-6
        epsilon_sqr = K.constant(epsilon ** 2)
        y1 = loss_model(y_pred)
        y2 = loss_model(y_true)
        loss_vgg = K.mean(K.square(y1 - y2), axis=[1, 2, 3])
        loss_mse = K.mean(
            K.sqrt(K.square(y_pred - y_true) + epsilon_sqr), axis=[1, 2, 3])
        return K.constant(weights[0])*loss_vgg + K.constant(weights[1])*loss_mse

    return vgg_perceptual_mse

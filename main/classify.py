from matplotlib.pyplot import step
from main.windowing import get_window

import tensorflow.compat.v1 as tf
import keras.backend as K

import numpy as np

from tensorflow.python.framework.ops import disable_eager_execution
disable_eager_execution()

K.clear_session()

session = tf.Session()

K.set_session(session)

PATH = 'assets/model/weights.hdf5'
SHAPE_IN = tf.keras.Input(shape = (256,256,3))

def rgb_to_grayscale(input):
    """Average out each pixel across its 3 RGB layers resulting in a grayscale image"""
    return K.mean(input, axis=3)

def rgb_to_grayscale_output_shape(input_shape):
    return input_shape[:-1]

# Create Model
def create_model():    
    base_model = tf.keras.applications.Xception(weights = None, include_top = False, input_tensor = SHAPE_IN)
    x = base_model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    cnn_bottleneck = tf.keras.layers.Dense(1024,activation='relu')(x)

    #Creating RNN
    x = tf.keras.layers.Lambda(rgb_to_grayscale, rgb_to_grayscale_output_shape)(SHAPE_IN)
    x = tf.keras.layers.Reshape((64, 1024))(x)
    x = tf.keras.layers.GRU(512, return_sequences=True, dropout = 0.2, reset_after=True)(x)
    rnn_output = tf.keras.layers.GRU(512, reset_after=True)(x)
    rnn_output = tf.keras.layers.Dense(1024,activation='relu')(rnn_output)
    x = tf.keras.layers.Multiply()([cnn_bottleneck , rnn_output])
    
    x = tf.keras.layers.Dropout(0.15)(x)
    y_pred = tf.keras.layers.Dense(6, activation = 'sigmoid')(x)

    return tf.keras.models.Model(inputs = base_model.input, outputs = y_pred)

with session.as_default():
    MODEL = create_model()
    MODEL.load_weights(PATH)
    MODEL._make_predict_function()

def get_classification(image):
    with session.as_default():
        result = MODEL.predict(np.expand_dims(image, axis=0), steps=None)
    result = np.round(result)
    result = str(list(result))
    print("Prediction", result)
    return result
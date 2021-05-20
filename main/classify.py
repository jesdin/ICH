# from main.windowing import get_window

# import keras.backend as K
# from keras.applications import Xception
# from keras.layers import Dense, Dropout, GlobalAveragePooling2D, Bidirectional
# from keras.models import Model, load_model
# from keras.layers import Lambda
# from keras.layers import Reshape
# from keras.layers import GRU

# import numpy as np
# import tensorflow as tf

# def rgb_to_grayscale(input):
#     """Average out each pixel across its 3 RGB layers resulting in a grayscale image"""
#     return K.mean(input, axis=3)

# def rgb_to_grayscale_output_shape(input_shape):
#     return input_shape[:-1]

# # Create Model
# def create_model():    
#     base_model = Xception(weights = 'imagenet', include_top = False, input_tensor = SHAPE_IN)
#     x = base_model.output
#     x = GlobalAveragePooling2D()(x)
#     cnn_bottleneck = Dense(1024,activation='relu')(x)

#     #Creating RNN
#     x = Lambda(rgb_to_grayscale, rgb_to_grayscale_output_shape)(SHAPE_IN)
#     x = Reshape((64, 1024))(x)
#     x = GRU(512, return_sequences=True, dropout = 0.2)(x)
#     rnn_output = GRU(512)(x)
#     rnn_output = Dense(1024,activation='relu')(rnn_output)
#     x = tf.keras.layers.Multiply()([cnn_bottleneck , rnn_output])
    
    
#     x = Dropout(0.15)(x)
#     y_pred = Dense(6, activation = 'sigmoid')(x)

#     return Model(inputs = base_model.input, outputs = y_pred)

# MODEL = create_model()

# model = load_model('assetes\\model\\weights.h5')

# def get_classification(path):
#     image = get_window(path)
#     result = model.predict(tf.expand_dims(image, axis=0))
#     result = np.round(result)
#     return result
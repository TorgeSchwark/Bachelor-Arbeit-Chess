import os
import math
import random
import numpy as np
import tensorflow as tf
import glob
from matplotlib import pyplot as plt
import matplotlib
from tensorflow.python.client import device_lib 
import time
from train_variables import *
from data_parser import data_generator_threaded
from multiprocessing import Pool

def setup_model_mlp():
  
  input = tf.keras.layers.Input(shape=(SEQ_LEN_PAST, NUM_INPUT_PARAMETERS), name='input')

  dp = 0.0
  x = tf.keras.layers.Flatten()(input)
  x = tf.keras.layers.Dense(200, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(200, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(200, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(200, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(200, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(200, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(200, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(200, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(200, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(200, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(200, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(200, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(200, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(200, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(200, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(200, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(SEQ_LEN_FUTURE * NUM_OUTPUT_PARAMETERS, activation='linear')(x)
  x = tf.keras.layers.Reshape((SEQ_LEN_FUTURE, NUM_OUTPUT_PARAMETERS))(x)

  model = tf.keras.models.Model(input, x)
  return model

def train(model_path, model, lr, from_checkpoint=False):
  batch_size = BATCH_SIZE

  train_gen = data_generator_threaded(batch_size, True) 
  val_gen = data_generator_threaded(batch_size, False)

  opt = tf.keras.optimizers.Adam(learning_rate=lr)
  checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(model_path + 'model-{epoch:03d}-mae{val_mae:.4f}.h5', verbose=1, monitor='val_mae', save_best_only=True, mode='auto')
  model.compile(loss='mse', optimizer=opt, metrics=["mse", "mae"])
  model.summary()

  history = model.fit(train_gen, steps_per_epoch=STEPS_PER_EPOCH, validation_steps=VALIDATION_STEPS, epochs=EPOCHS, 
                      validation_data=val_gen, callbacks=[checkpoint_callback], 
                      shuffle=True, verbose='auto')
  

def run():
  physical_devices = tf.config.list_physical_devices('GPU')
  print("\nGPUs: {}\n".format(physical_devices))

  model = setup_model_mlp()

  train("test", model, 0.00001)

if __name__== "__main__":
  run()
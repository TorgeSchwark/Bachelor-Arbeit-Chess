import os
import tensorflow as tf
from tensorflow.python.client import device_lib 
from train_variables import *
from data_parser import data_generator_threaded, data_generator_kd, select_data_kd
from setup_models_variable import *
from setup_models import *
from multiprocessing import Pool
import datetime
import numpy as np

def test_train_kd(model_path, model, lr):

    train_gen = data_generator_kd(BATCH_SIZE, False)
    val_gen = data_generator_kd(BATCH_SIZE, True)

    opt = tf.keras.optimizers.Adam(learning_rate=lr)

    model.compile(loss='mse', optimizer=opt, metrics=["mse", "mae"])
    model.summary()

    history = model.fit(
        train_gen,
        steps_per_epoch=STEPS_PER_EPOCH,
        validation_steps=VALIDATION_STEPS,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=[],  
        shuffle=True,
        verbose='auto'
    )


import os
import tensorflow as tf
from multiprocessing import Pool
import time
# Annahme, dass diese Konstanten definiert sind
BATCH_SIZE = 200
STEPS_PER_EPOCH = 300
VALIDATION_STEPS = 20
EPOCHS = 500


# Definieren Sie die Lernratenplanungsfunktion
def scheduler(epoch, lr):
    print(lr)
    return lr * 0.995

def train(model_path, arch_name, model, lr, from_checkpoint=False):
    """ the main train method defining the callbacks and starting the data_generators and finally the training """
    batch_size = BATCH_SIZE
    pool_train = Pool(10)
    pool_val = Pool(10)

    log_dir = os.path.join("./logs", arch_name, os.path.basename(model_path))
    os.makedirs(log_dir, exist_ok=True)

    train_gen = data_generator_threaded(batch_size, True, pool_train) 
    val_gen = data_generator_threaded(batch_size, False, pool_val)

    opt = tf.keras.optimizers.Adam(learning_rate=lr)

    early_stopping_callback = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',  
        patience=30,  
        verbose=1, 
        restore_best_weights=True  
    )
    
    # Lernratenscheduler-Callback
    lr_scheduler_callback = tf.keras.callbacks.LearningRateScheduler(scheduler)

    model.compile(loss='mse', optimizer=opt, metrics=["mse", "mae"])
    model.summary()
    
    history = model.fit(
        train_gen,
        steps_per_epoch=STEPS_PER_EPOCH,
        validation_steps=VALIDATION_STEPS,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=[early_stopping_callback, lr_scheduler_callback],  # Fügen Sie den Scheduler-Callback hier hinzu
        shuffle=True,
        verbose='auto'
    )

    pool_train.close()
    pool_train.join()
    pool_val.close()
    pool_val.join()

def test_kd():

    model = setup_model_kd()
    test_train_kd("models/test", model,  0.0008)


def test_speed():
    physical_devices = tf.config.list_physical_devices('GPU')
    print("\nGPUs: {}\n".format(physical_devices))
    model = test_model_small()
    train("test_smal_model", "lstm", model, 0.0001)

def run():
    physical_devices = tf.config.list_physical_devices('GPU')
    print("\nGPUs: {}\n".format(physical_devices))
    test_kd()
    #loop_train()
    

if __name__== "__main__":
    test_speed()
import os
import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow.python.client import device_lib 
from train_variables import *
from data_parser import data_generator_threaded
from setup_models import *
from multiprocessing import Pool
import datetime

def train(model_path, arch_name, model, lr, from_checkpoint=False):
    batch_size = BATCH_SIZE

    train_gen = data_generator_threaded(batch_size, True) 
    val_gen = data_generator_threaded(batch_size, False)

    opt = tf.keras.optimizers.Adam(learning_rate=lr)
    #eg: conv_mlp_big/logs/fit/lr:0.0004bz500
    log_dir = model_path+ "/logs/fit/" + arch_name
  
    tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir=log_dir,
    histogram_freq=1,  # Aufzeichnung von Histogrammen bei jeder Epoche
    write_graph=True,  # Zeichne den Graph des Modells
    write_images=True,  # Zeichne Grafiken von Aktivierungen und Gradienten
    update_freq='epoch',  # Aktualisieren der Daten am Ende jeder Epoche
    profile_batch=5  # Verwende Batch 5 für das Profiling
)
    
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        os.path.join(log_dir, 'best_model.h5'),
        verbose=1, monitor='val_mae', save_best_only=True, mode='auto')
    model.compile(loss='mse', optimizer=opt, metrics=["mse", "mae"])
    model.summary()

    history = model.fit(train_gen, steps_per_epoch=STEPS_PER_EPOCH, validation_steps=VALIDATION_STEPS, epochs=EPOCHS, 
                        validation_data=val_gen, callbacks=[checkpoint_callback, tensorboard_callback], 
                        shuffle=True, verbose='auto')

    # Laden des besten Modells und Hinzufügen des TensorBoard-Rückrufs
    best_model_path = os.path.join(log_dir, 'best_model.h5')
    best_model = tf.keras.models.load_model(best_model_path)
    best_model.compile(loss='mse', optimizer=opt, metrics=["mse", "mae"])

    # Verwenden Sie die Methode evaluate(), um das Modell zu bewerten
    best_model.evaluate(val_gen, steps=VALIDATION_STEPS)

def loop_train():
    train_setup_model_conv_mlp_big()

def train_setup_model_conv_mlp_big():

def run():
    physical_devices = tf.config.list_physical_devices('GPU')
    print("\nGPUs: {}\n".format(physical_devices))

    model = setup_model_conv_mlp_big()

    # Pfad für die Modelle
    model_path = "models/"

    #loop_train()
    train(model_path, , model, 0.000007)

if __name__== "__main__":
    run()
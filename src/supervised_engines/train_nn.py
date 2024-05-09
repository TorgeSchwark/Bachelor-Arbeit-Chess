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
    log_dir = os.path.join(model_path, "logs/fit", arch_name)

    tensorboard_callback =tf.keras.callbacks.TensorBoard(
        log_dir=log_dir,
        histogram_freq=1,
        write_graph=True,
        write_images=True,
        update_freq='epoch',
        profile_batch=5
    )

    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        os.path.join(log_dir, 'best_model.h5'),
        verbose=1,
        monitor='val_mae',
        save_best_only=True,
        mode='auto'
    )

    # Definieren des Early Stopping Callbacks
    early_stopping_callback = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',  # Überwachen Sie die Validierungsverluste
        patience=15,  # Anzahl der Epochen ohne Verbesserung, bevor das Training gestoppt wird
        verbose=1, 
        restore_best_weights=True  # Stellen Sie die Gewichte des besten Modells wieder her
    )

    model.compile(loss='mse', optimizer=opt, metrics=["mse", "mae"])
    model.summary()

    history = model.fit(
        train_gen,
        steps_per_epoch=STEPS_PER_EPOCH,
        validation_steps=VALIDATION_STEPS,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=[checkpoint_callback, tensorboard_callback, early_stopping_callback],  # Fügen Sie den Early Stopping Callback hinzu
        shuffle=True,
        verbose='auto'
    )

    # Laden des besten Modells und Bewerten des Modells
    best_model_path = os.path.join(log_dir, 'best_model.h5')
    best_model = tf.keras.models.load_model(best_model_path)
    best_model.compile(loss='mse', optimizer=opt, metrics=["mse", "mae"])

    best_model.evaluate(val_gen, steps=VALIDATION_STEPS)
def loop_train():
    train_setup_model_conv_mlp_big()

def train_setup_model_conv_mlp_big():
    lr = [0.000005,0.00001, 0.000015]
    dp = [0, 0.05]
    for d in dp:
        model = setup_model_conv_mlp_big(d)
        for i in lr:
            train("conv_mlp_big", str(i), model, i)


def run():
    physical_devices = tf.config.list_physical_devices('GPU')
    print("\nGPUs: {}\n".format(physical_devices))

    model = setup_model_conv_mlp_big()

    # Pfad für die Modelle
    model_path = "models/"

    #loop_train()
    train(model_path, "test", model, 0.000008)

if __name__== "__main__":
    run()
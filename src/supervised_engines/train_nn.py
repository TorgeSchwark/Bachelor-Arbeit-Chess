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
BATCH_SIZE = 80
STEPS_PER_EPOCH = 300
VALIDATION_STEPS = 20
EPOCHS = 500


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

    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir=log_dir,
        histogram_freq=1,
        write_graph=True,
        write_images=True,
        update_freq='epoch',
        profile_batch=5
    )

    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        os.path.join(log_dir, 'best_model.keras'),
        verbose=1,
        monitor='val_mae',
        save_best_only=True,
        mode='auto'
    )

    early_stopping_callback = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',  
        patience=30,  
        verbose=1, 
        restore_best_weights=True  
    )

    model.compile(loss='mse', optimizer=opt, metrics=["mse", "mae"])
    model.summary()
    
    history = model.fit(
        train_gen,
        steps_per_epoch=STEPS_PER_EPOCH,
        validation_steps=VALIDATION_STEPS,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=[checkpoint_callback, tensorboard_callback, early_stopping_callback],  
        shuffle=True,
        verbose='auto'
    )

    # TensorFlow Lite Converter
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    tflite_model_path = os.path.join(log_dir, 'best_model.tflite')
    with open(tflite_model_path, 'wb') as f:
        f.write(tflite_model)

    # Laden des TensorFlow Lite-Modells in den Interpreter
    interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
    interpreter.allocate_tensors()

    # Testdaten für die Inferenz erzeugen
    n = 10000000  # Anzahl der Vorhersagen, die du testen möchtest
    input_shape = (73,)  # Beispielhafte Eingabeform, passe sie an dein Modell an
    test_data = np.random.random((n, *input_shape)).astype(np.float32)

    # Führe Vorhersagen durch und messe die Zeit
    start_time = time.time()
    for i in range(n):
        interpreter.set_tensor(interpreter.get_input_details()[0]['index'], test_data[i:i+1])
        interpreter.invoke()
    end_time = time.time()

    # Berechne die Zeit pro Vorhersage
    total_time = end_time - start_time
    time_per_prediction = total_time / n

    print(f"Total time for {n} predictions: {total_time:.4f} seconds")
    print(f"Average time per prediction: {time_per_prediction:.6f} seconds")

    # Weitere Verarbeitung wie das Speichern von Metriken oder Plotten der Verlustkurve

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
    model = setup_model_lstm()
    train("test_smal_model", "lstm", model, 0.0001)

def run():
    physical_devices = tf.config.list_physical_devices('GPU')
    print("\nGPUs: {}\n".format(physical_devices))
    test_kd()
    #loop_train()
    

if __name__== "__main__":
    test_speed()
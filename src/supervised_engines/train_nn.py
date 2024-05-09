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
        patience=20,  # Anzahl der Epochen ohne Verbesserung, bevor das Training gestoppt wird
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

    val_loss, val_mse, val_mae = best_model.evaluate(val_gen, steps=VALIDATION_STEPS)

    # Speichern des MAE in einer Textdatei
    with open(os.path.join(log_dir, 'best_model_mae.txt'), 'w') as f:
        f.write(f'Validation MAE of the best model: {val_mae}')

    # Diagramm des Trainings- und Validierungsverlusts erstellen und speichern
    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig(os.path.join(log_dir, 'loss_plot.png'))
    
def loop_train():
    train_setup_model_conv_mlp_big()
    train_setup_model_cov_mlp_small()
    train_setup_model_mlp_mlp_small()
    train_setup_model_mlp_mlp_deep()
    train_setup_model_lstm()
    train_setup_model_transformer()


def train_setup_model_transformer():
    lr = [0.0001, 0.0005, 0.001]
    model = setup_model_transformer()
    for i in lr:
        train("transformer", "lr"+str(i)+",patience20", model, i) 

def train_setup_model_lstm():
    lr = [0.0001, 0.0005, 0.001]
    model = setup_model_lstm()
    for i in lr:
        train("lstm", "lr"+str(i)+",patience20", model, i) 

def train_setup_model_mlp_mlp_deep():
    lr = [0.0001, 0.0005, 0.001]
    model = setup_model_mlp_mlp_deep()
    for i in lr:
        train("mlp_mlp_deep", "lr"+str(i)+",patience20", model, i) 

def train_setup_model_mlp_mlp_small():
    lr = [0.0001, 0.0005, 0.001]
    model = setup_model_mlp_mlp_small()
    for i in lr:
        train("mlp_mlp_small", "lr"+str(i)+",patience20", model, i) 

def train_setup_model_cov_mlp_small():
    lr = [0.00005, 0.00015, 0.001]
    model = setup_model_conv_mlp_small()
    for i in lr:
        train("conv_mlp_small", "lr"+str(i)+",patience20", model, i) 

def train_setup_model_conv_mlp_big():
    lr = [0.00005, 0.00015, 0.001]
    model = setup_model_conv_mlp_big()
    for i in lr:
        train("conv_mlp_big", "lr"+str(i)+",patience20", model, i)


def run():
    physical_devices = tf.config.list_physical_devices('GPU')
    print("\nGPUs: {}\n".format(physical_devices))

    model = setup_model_transformer()

    # Pfad für die Modelle
    model_path = "models/"

    #loop_train()
    train(model_path, "test", model, 0.001)

if __name__== "__main__":
    run()
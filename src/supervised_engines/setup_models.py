import tensorflow as tf
from train_variables import *

# sets up some test models for training

def build_model(hp):
    input = layers.Input(shape=(SIMPLE_INPUT,), name='input')
    white_input = input[:, :(SIMPLE_INPUT // 2)]
    black_input = input[:, (SIMPLE_INPUT // 2):]

    # Hyperparameter für Layer-Größe und Aktivierungsfunktion
    hp_units_white = hp.Int('units_white', min_value=32, max_value=512, step=32)
    hp_units_black = hp.Int('units_black', min_value=32, max_value=512, step=32)
    hp_activation = hp.Choice('activation', values=['relu', 'tanh', 'sigmoid'])

    mlp_white = layers.Dense(hp_units_white, activation=hp_activation)(white_input)
    mlp_black = layers.Dense(hp_units_black, activation=hp_activation)(black_input)

    combined = layers.Concatenate()([mlp_white, mlp_black])

    mlp = layers.Dense(hp.Int('units_layer1', min_value=16, max_value=128, step=16), activation=hp_activation)(combined)
    mlp = layers.Dense(hp.Int('units_layer2', min_value=16, max_value=128, step=16), activation=hp_activation)(mlp)
    mlp = layers.Dense(1, activation='linear')(mlp)

    model = models.Model(inputs=input, outputs=mlp)
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(hp.Float('learning_rate', min_value=1e-4, max_value=1e-2, sampling='LOG', default=1e-3)),
        loss='mse',
        metrics=['mae']
    )
    return model


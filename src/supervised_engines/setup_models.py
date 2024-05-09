import tensorflow as tf
from train_variables import *

def setup_model_conv_mlp_big():
    input = tf.keras.layers.Input(shape=(SEQ_LEN_PAST, NUM_INPUT_PARAMETERS), name='input')

    # Convolutional-Teil
    conv_input = input[:, :64, :]
    x_conv_1 = tf.keras.layers.Reshape((8, 8, 1))(conv_input)
    x_conv_1 = tf.keras.layers.Conv2D(256, kernel_size=(3, 3), activation='relu', padding='same')(x_conv_1)
    x_conv_1 = tf.keras.layers.MaxPooling2D((2, 2))(x_conv_1)
    x_conv_1 = tf.keras.layers.Conv2D(256, kernel_size=(3, 3), activation='relu', padding='same')(x_conv_1)
    x_conv_1 = tf.keras.layers.MaxPooling2D((2, 2))(x_conv_1)
    x_conv_1 = tf.keras.layers.Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same')(x_conv_1)
    x_conv_1 = tf.keras.layers.MaxPooling2D((2, 2))(x_conv_1)
    x_conv_1 = tf.keras.layers.Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same')(x_conv_1)

    x_conv_2 = tf.keras.layers.Reshape((8, 8, 1))(conv_input)
    x_conv_2 = tf.keras.layers.Conv2D(256, kernel_size=(5, 5), activation='relu', padding='same')(x_conv_2)
    x_conv_2 = tf.keras.layers.Conv2D(128, kernel_size=(5, 5), activation='relu', padding='same')(x_conv_2)

    # MLP-Teil
    mlp_input = input[:, 64:, :]
    x_mlp = tf.keras.layers.Flatten()(mlp_input)
    x_mlp = tf.keras.layers.Dense(200, activation='relu')(x_mlp)
    x_mlp = tf.keras.layers.BatchNormalization()(x_mlp)
    x_mlp = tf.keras.layers.Dense(200, activation='relu')(x_mlp)
    x_mlp = tf.keras.layers.BatchNormalization()(x_mlp)
    x_mlp = tf.keras.layers.Dense(200, activation='relu')(x_mlp)

    # Kombinierte Ausgabe der Convolutional- und MLP-Teile
    combined = tf.keras.layers.Concatenate()([tf.keras.layers.Flatten()(x_conv_1), 
                                              tf.keras.layers.Flatten()(x_conv_2), 
                                              x_mlp])

    # Fully-Connected-Layer
    x = tf.keras.layers.Dense(400, activation='relu')(combined)
    x = tf.keras.layers.Dropout(0.5)(x)
    x = tf.keras.layers.Dense(200, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.5)(x)
    x = tf.keras.layers.Dense(SEQ_LEN_FUTURE * NUM_OUTPUT_PARAMETERS, activation='linear')(x)
    x = tf.keras.layers.Reshape((SEQ_LEN_FUTURE, NUM_OUTPUT_PARAMETERS))(x)

    model = tf.keras.models.Model(input, x)
    return model

def setup_model_conv_mlp_small():
  
  input = tf.keras.layers.Input(shape=(SEQ_LEN_PAST, NUM_INPUT_PARAMETERS), name='input')
  dp = 0
  conv_input = input[:, :64, :]  
  x_conv_1 = tf.keras.layers.Reshape((8, 8, 1))(conv_input)  
  x_conv_1 = tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same')(x_conv_1)
  x_conv_1 = tf.keras.layers.Dropout(dp)(x_conv_1)
  x_conv_1 = tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same')(x_conv_1)
  x_conv_1 = tf.keras.layers.Dropout(dp)(x_conv_1)
  x_conv_1 = tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same')(x_conv_1)
  x_conv_1 = tf.keras.layers.Dropout(dp)(x_conv_1)
  x_conv_1 = tf.keras.layers.Flatten()(x_conv_1)


  x_conv_2 = tf.keras.layers.Reshape((8, 8, 1))(conv_input)  
  x_conv_2 = tf.keras.layers.Conv2D(32, kernel_size=(5, 5), activation='relu', padding='same')(x_conv_2)
  x_conv_2 = tf.keras.layers.Dropout(dp)(x_conv_2)
  x_conv_2 = tf.keras.layers.Conv2D(32, kernel_size=(5, 5), activation='relu', padding='same')(x_conv_2)
  x_conv_2 = tf.keras.layers.Dropout(dp)(x_conv_2)
  x_conv_2 = tf.keras.layers.Flatten()(x_conv_2)

  mlp_input = input[:, 64:, :]  
  x_mlp = tf.keras.layers.Flatten()(mlp_input)
  x_mlp = tf.keras.layers.Dense(50, activation='relu')(x_mlp)
  x_mlp = tf.keras.layers.Dropout(dp)(x_mlp)
  x_mlp = tf.keras.layers.Dense(50, activation='relu')(x_mlp)
  x_mlp = tf.keras.layers.Dropout(dp)(x_mlp)
  x_mlp = tf.keras.layers.Dense(50, activation='relu')(x_mlp)
  x_mlp = tf.keras.layers.Dropout(dp)(x_mlp)

  combined = tf.keras.layers.Concatenate()([x_conv_1, x_mlp, x_conv_2])

  x = tf.keras.layers.Dense(100, activation='relu')(combined)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(100, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(100, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(SEQ_LEN_FUTURE * NUM_OUTPUT_PARAMETERS, activation='linear')(x)
  x = tf.keras.layers.Reshape((SEQ_LEN_FUTURE, NUM_OUTPUT_PARAMETERS))(x)

  model = tf.keras.models.Model(input, x)
  return model

def setup_model_mlp_mlp_small():
  
  input = tf.keras.layers.Input(shape=(SEQ_LEN_PAST, NUM_INPUT_PARAMETERS), name='input')
  dp = 0
  mlp_board_input = input[:, :64, :] 
  mlp_board_input = tf.keras.layers.Flatten()(mlp_board_input)

  mlp_1 = tf.keras.layers.Dense(200, activation='relu')(mlp_board_input)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)
  mlp_1 = tf.keras.layers.Dense(200, activation='relu')(mlp_1)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)
  mlp_1 = tf.keras.layers.Dense(200, activation='relu')(mlp_1)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)

  mlp_2 = tf.keras.layers.Dense(200, activation='relu')(mlp_board_input)
  mlp_2 = tf.keras.layers.Dropout(dp)(mlp_2)
  mlp_2 = tf.keras.layers.Dense(200, activation='relu')(mlp_2)
  mlp_2 = tf.keras.layers.Dropout(dp)(mlp_2)

  mlp_input = input[:, 64:, :]  
  x_mlp = tf.keras.layers.Flatten()(mlp_input)
  x_mlp = tf.keras.layers.Dense(500, activation='relu')(x_mlp)
  x_mlp = tf.keras.layers.Dropout(dp)(x_mlp)
  x_mlp = tf.keras.layers.Dense(500, activation='relu')(x_mlp)
  x_mlp = tf.keras.layers.Dropout(dp)(x_mlp)
  x_mlp = tf.keras.layers.Dense(500, activation='relu')(x_mlp)
  x_mlp = tf.keras.layers.Dropout(dp)(x_mlp)

  combined = tf.keras.layers.Concatenate()([mlp_1, x_mlp, mlp_2])

  x = tf.keras.layers.Dense(100, activation='relu')(combined)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(100, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(100, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(SEQ_LEN_FUTURE * NUM_OUTPUT_PARAMETERS, activation='linear')(x)
  x = tf.keras.layers.Reshape((SEQ_LEN_FUTURE, NUM_OUTPUT_PARAMETERS))(x)

  model = tf.keras.models.Model(input, x)
  return model

def setup_model_mlp_mlp_deep():
  
  input = tf.keras.layers.Input(shape=(SEQ_LEN_PAST, NUM_INPUT_PARAMETERS), name='input')
  dp = 0
  mlp_board_input = input[:, :64, :]  
  mlp_board_input = tf.keras.layers.Flatten()(mlp_board_input)
  mlp_1 = tf.keras.layers.Dense(200, activation='relu')(mlp_board_input)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)
  mlp_1 = tf.keras.layers.Dense(200, activation='relu')(mlp_1)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)
  mlp_1 = tf.keras.layers.Dense(200, activation='relu')(mlp_1)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)
  mlp_1 = tf.keras.layers.Dense(200, activation='relu')(mlp_1)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)
  mlp_1 = tf.keras.layers.Dense(200, activation='relu')(mlp_1)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)
  mlp_1 = tf.keras.layers.Dense(200, activation='relu')(mlp_1)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)
  mlp_1 = tf.keras.layers.Dense(200, activation='relu')(mlp_1)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)
  mlp_1 = tf.keras.layers.Dense(200, activation='relu')(mlp_1)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)
  mlp_1 = tf.keras.layers.Dense(200, activation='relu')(mlp_1)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)
  mlp_1 = tf.keras.layers.Dense(200, activation='relu')(mlp_1)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)
  mlp_1 = tf.keras.layers.Dense(200, activation='relu')(mlp_1)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)

  

  mlp_input = input[:, 64:, :]  
  x_mlp = tf.keras.layers.Flatten()(mlp_input)
  x_mlp = tf.keras.layers.Dense(500, activation='relu')(x_mlp)
  x_mlp = tf.keras.layers.Dropout(dp)(x_mlp)
  x_mlp = tf.keras.layers.Dense(500, activation='relu')(x_mlp)
  x_mlp = tf.keras.layers.Dropout(dp)(x_mlp)
  x_mlp = tf.keras.layers.Dense(500, activation='relu')(x_mlp)
  x_mlp = tf.keras.layers.Dropout(dp)(x_mlp)

  combined = tf.keras.layers.Concatenate()([mlp_1, x_mlp])

  x = tf.keras.layers.Dense(100, activation='relu')(combined)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(100, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(100, activation='relu')(x)
  x = tf.keras.layers.Dropout(dp)(x)
  x = tf.keras.layers.Dense(SEQ_LEN_FUTURE * NUM_OUTPUT_PARAMETERS, activation='linear')(x)
  x = tf.keras.layers.Reshape((SEQ_LEN_FUTURE, NUM_OUTPUT_PARAMETERS))(x)

  model = tf.keras.models.Model(input, x)
  return model

def setup_model_lstm():
  
  input = tf.keras.layers.Input(shape=(SEQ_LEN_PAST, NUM_INPUT_PARAMETERS), name='input')

  x = tf.keras.layers.LSTM(200, return_sequences=True)(input)
  x = tf.keras.layers.LSTM(200, return_sequences=True)(x)
  x = tf.keras.layers.LSTM(200, return_sequences=True)(x)
  x = tf.keras.layers.LSTM(200, return_sequences=True)(x)
  x = tf.keras.layers.LSTM(200, return_sequences=True)(x)
  x = tf.keras.layers.LSTM(200)(x)

  x = tf.keras.layers.Dense(2000, activation='relu')(x)
  x = tf.keras.layers.Dense(1000, activation='relu')(x)
  x = tf.keras.layers.Dense(700, activation='relu')(x)
  x = tf.keras.layers.Dense(55, activation='relu')(x)

  x = tf.keras.layers.Dense(SEQ_LEN_FUTURE * NUM_OUTPUT_PARAMETERS, activation='linear')(x)
  x = tf.keras.layers.Reshape((SEQ_LEN_FUTURE, NUM_OUTPUT_PARAMETERS))(x)

  model = tf.keras.models.Model(input, x)
  return model  

def setup_model_transformer(dropout=0, num_transformer_blocks=8, mlp_units=[256]):
    inputs = tf.keras.Input(shape=(SEQ_LEN_PAST, NUM_INPUT_PARAMETERS))
    x = inputs

    for _ in range(num_transformer_blocks):
        x = transformer_encoder(x, dropout=dropout)

    x = tf.keras.layers.GlobalAveragePooling1D(data_format="channels_first")(x)

    for dim in mlp_units:
        x = tf.keras.layers.Dense(dim, activation="relu")(x)
        x = tf.keras.layers.Dropout(dropout)(x)

    outputs = tf.keras.layers.Dense(SEQ_LEN_FUTURE * NUM_OUTPUT_PARAMETERS)(x)
    outputs = tf.keras.layers.Reshape((SEQ_LEN_FUTURE, NUM_OUTPUT_PARAMETERS))(outputs)

    return tf.keras.Model(inputs, outputs)

def transformer_encoder(inputs, dropout=0, head_size=1000, num_heads=16, ff_dim=2):
    x = tf.keras.layers.LayerNormalization(epsilon=1e-6)(inputs)
    
    x = tf.keras.layers.MultiHeadAttention(
        key_dim=head_size, num_heads=num_heads, dropout=dropout
    )(x, x)
    x = tf.keras.layers.Dropout(dropout)(x)
    res = tf.keras.layers.Add()([inputs, x])

    x = tf.keras.layers.LayerNormalization(epsilon=1e-6)(res)
    x = tf.keras.layers.Conv1D(filters=ff_dim, kernel_size=1, activation="relu")(x)
    x = tf.keras.layers.Dropout(dropout)(x)
    x = tf.keras.layers.Conv1D(filters=inputs.shape[-1], kernel_size=1)(x)
    return tf.keras.layers.Add()([res, x])

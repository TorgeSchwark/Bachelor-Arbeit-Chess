import tensorflow as tf
from train_variables import *

def setup_model_conv_mlp_small_vari(arch_conv, arch_mlp, arch_combined, dp_conv, dp_mlp, dp_compined):
  
  input = tf.keras.layers.Input(shape=(SEQ_LEN_PAST, NUM_INPUT_PARAMETERS), name='input')

  conv_input = input[:, :64, :]  
  x_conv_1 = tf.keras.layers.Reshape((8, 8, 1))(conv_input)  
  for i in arch_conv:
    x_conv_1 = tf.keras.layers.Conv2D(i[0], kernel_size=(i[1], i[1]), activation='relu', padding='same')(x_conv_1)
    x_conv_1 = tf.keras.layers.Dropout(dp_conv)(x_conv_1)
  x_conv_1 = tf.keras.layers.Flatten()(x_conv_1)
  

  mlp_input = input[:, 64:, :] 
  x_mlp = tf.keras.layers.Flatten()(mlp_input)
  for i in arch_mlp:
    x_mlp = tf.keras.layers.Dense(i, activation='relu')(x_mlp)
    x_mlp = tf.keras.layers.Dropout(dp_mlp)(x_mlp)

  combined = tf.keras.layers.Concatenate()([x_conv_1, x_mlp])

  x = tf.keras.layers.Dense(arch_combined[0], activation='relu')(combined)
  x = tf.keras.layers.Dropout(dp_compined)(x)

  for i in arch_combined[1:]:
    x = tf.keras.layers.Dense(i, activation='relu')(x)
    x = tf.keras.layers.Dropout(dp_compined)(x)
  
  x = tf.keras.layers.Dense(SEQ_LEN_FUTURE * NUM_OUTPUT_PARAMETERS, activation='linear')(x)
  x = tf.keras.layers.Reshape((SEQ_LEN_FUTURE, NUM_OUTPUT_PARAMETERS))(x)

  model = tf.keras.models.Model(input, x)
  return model

def setup_no_split_lstm():
  input = tf.keras.layers.Input(shape=(SEQ_LEN_PAST, NUM_INPUT_PARAMETERS), name='input')
  
  lstm_input = input[:, :64, :] 
  lstm_board = tf.keras.layers.LSTM(50, return_sequences=True)(lstm_input)
  lstm_board = tf.keras.layers.LSTM(50, return_sequences=True)(lstm_board)
  lstm_board = tf.keras.layers.LSTM(50)(lstm_board)

  mlp_input2 = input[:, 64:, :] 
  lstm_meta = tf.keras.layers.LSTM(50, return_sequences=True)(mlp_input2)
  lstm_meta = tf.keras.layers.LSTM(50, return_sequences=True)(lstm_meta)
  lstm_meta = tf.keras.layers.LSTM(50)(lstm_meta)

  combined = tf.keras.layers.Concatenate()([lstm_meta, lstm_board])
  mlp_combine = tf.keras.layers.Dense(100, activation='relu')(combined)
  mlp_combine = tf.keras.layers.Dense(100, activation='relu')(mlp_combine)
  mlp_combine = tf.keras.layers.Dense(100, activation='relu')(mlp_combine)

  x = tf.keras.layers.Dense(SEQ_LEN_FUTURE * NUM_OUTPUT_PARAMETERS, activation='linear')(mlp_combine)
  x = tf.keras.layers.Reshape((SEQ_LEN_FUTURE, NUM_OUTPUT_PARAMETERS))(x)

  model = tf.keras.models.Model(input, x)
  return model 

def no_split_transformer(dropout=0, num_transformer_blocks=4, mlp_units=[64]):
    
    input = tf.keras.layers.Input(shape=(SEQ_LEN_PAST, NUM_INPUT_PARAMETERS), name='input')
    x = input
    dp = 0

    for _ in range(num_transformer_blocks):
        x = transformer_encoder(x, dropout=dropout)

    x = tf.keras.layers.Flatten(data_format="channels_first")(x)

    for dim in mlp_units:
        x = tf.keras.layers.Dense(dim, activation="relu")(x)
        x = tf.keras.layers.Dropout(dropout)(x)

    x = tf.keras.layers.Dense(200, activation='relu')(x)
    x = tf.keras.layers.Dropout(dp)(x)
    x = tf.keras.layers.Dense(200, activation='relu')(x)
    x = tf.keras.layers.Dropout(dp)(x)
    x = tf.keras.layers.Dense(200, activation='relu')(x)
    x = tf.keras.layers.Dropout(dp)(x)
    x = tf.keras.layers.Dense(SEQ_LEN_FUTURE * NUM_OUTPUT_PARAMETERS, activation='linear')(x)
    x = tf.keras.layers.Reshape((SEQ_LEN_FUTURE, NUM_OUTPUT_PARAMETERS))(x)

    return tf.keras.Model(input, x)

def transformer_encoder(inputs, dropout=0, head_size=30, num_heads=8, ff_dim=2):
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


def setup_no_split_mlp():
  input = tf.keras.layers.Input(shape=(SEQ_LEN_PAST, NUM_INPUT_PARAMETERS), name='input')
  dp = 0
  
  mlp_1 = tf.keras.layers.Flatten()(input)
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


  mlp_1 = tf.keras.layers.Dense(100, activation='relu')(mlp_1)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)
  mlp_1 = tf.keras.layers.Dense(100, activation='relu')(mlp_1)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)
  mlp_1 = tf.keras.layers.Dense(100, activation='relu')(mlp_1)
  mlp_1 = tf.keras.layers.Dropout(dp)(mlp_1)
  mlp_1 = tf.keras.layers.Dense(SEQ_LEN_FUTURE * NUM_OUTPUT_PARAMETERS, activation='linear')(mlp_1)
  mlp_1 = tf.keras.layers.Reshape((SEQ_LEN_FUTURE, NUM_OUTPUT_PARAMETERS))(mlp_1)

  model = tf.keras.models.Model(input, mlp_1)
  return model

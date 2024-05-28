SEQ_LEN_FUTURE = 1
NUM_OUTPUT_PARAMETERS = 1
SEQ_LEN_PAST = 73
NUM_INPUT_PARAMETERS = 1

KD_INPUT = 64*64*10
SIMPLE_INPUT = 64*6*2

GPU_STRING = '/gpu:0'
BATCH_SIZE = 20
MODEL_NAME = "Mlp"
EPOCHS = 500
STEPS_PER_EPOCH = 100 # 30
VALIDATION_STEPS = 100
THREADS = 10
SPLIT = 0.7

SIZE_X = 64
SIZE_Y = 64
SIZE_Z = 10

#DATA_PATH = ".\src\supervised_engines\stockfish_DB.db"
DATA_PATH = ".\src\supervised_engines\stockfish_depth16_DB.db"
DATA_PATH_KD = ".\src\supervised_engines\half_kp.db"
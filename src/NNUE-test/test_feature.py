import ctypes
import numpy as np
import chess
import torch

# Load the shared library
lib = ctypes.CDLL('./src/chess_implementationC/test.so')

# Define the argument and return types for the test_start function
lib.test_start.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)]
lib.test_start.restype = None

# Define constants
NUM_SQ = 64
NUM_PT = 12
NUM_PLANES = (NUM_SQ * NUM_PT + 1)

# Implement the Python version of get_active_features
def orient(is_white_pov: bool, sq: int):
    return (56 * (not is_white_pov)) ^ sq

def halfka_idx(is_white_pov: bool, king_sq: int, sq: int, p: chess.Piece):
    p_idx = (p.piece_type - 1) * 2 + (p.color != is_white_pov)
    return 1 + orient(is_white_pov, sq) + p_idx * NUM_SQ + king_sq * NUM_PLANES

def get_active_features(board: chess.Board):
    def piece_features(turn):
        indices = torch.zeros(NUM_PLANES * NUM_SQ)
        for sq, p in board.piece_map().items():
            indices[halfka_idx(turn, orient(turn, board.king(turn)), sq, p)] = 1.0
        return indices
    
    white_features = piece_features(chess.WHITE)
    black_features = piece_features(chess.BLACK)
    
    return (white_features, black_features)

# Prepare the features arrays for C function
features_c_white = (ctypes.c_float * (NUM_PLANES * NUM_SQ))()
features_c_black = (ctypes.c_float * (NUM_PLANES * NUM_SQ))()

# Call the C function
lib.test_start(features_c_white, features_c_black)

# Convert the C arrays to numpy arrays for comparison
features_c_array_white = np.ctypeslib.as_array(features_c_white)
features_c_array_black = np.ctypeslib.as_array(features_c_black)
features_c_array = np.concatenate((features_c_array_white, features_c_array_black))

# Initialize the board and get features using the Python implementation
board = chess.Board()
white_features, black_features = get_active_features(board)

# Combine white and black features into a single array for comparison
features_py = torch.cat((white_features, black_features)).numpy()

# Compare the results
comparison = np.allclose(features_c_array, features_py)

print("Comparison result:", comparison)
if not comparison:
    print("Differences found:")
    for i in range(len(features_c_array)):
        if features_c_array[i] != features_py[i]:
            print(f"Index {i}: C={features_c_array[i]} Python={features_py[i]}")

import math
import random
from train_variables import *
import numpy as np
import glob
import pandas as pd
from multiprocessing import Pool

import sqlite3

def select_data(batch_size, is_train, split_index):
    
    conn = sqlite3.connect(DATA_PATH)
    cursor = conn.cursor()
    if is_train:
        cursor.execute(f"SELECT * FROM ChessData LIMIT {batch_size}")
    else:
        cursor.execute(f"SELECT * FROM ChessData LIMIT {batch_size}")
    data = cursor.fetchall()
    conn.close()
    
    selected_inputs = np.array([[[int(value)] for value in row[0].split()] for row in data])
    selected_labels = np.array([[[row[1]]] for row in data])
    return selected_inputs, selected_labels

def data_generator_threaded(batch_size, is_train, num_threads=5):
    path = DATA_PATH
    conn = sqlite3.connect(path)
    data_size = pd.read_sql_query("SELECT COUNT(*) FROM ChessData", conn).iloc[0, 0]
    print("size" , data_size)
    chunk_size = math.ceil(((data_size) / 10) / num_threads)
    split_index = int(0.7 * chunk_size)

    pool = Pool(num_threads)
    print("done data")

    while True:
        args_list = [(batch_size, is_train, split_index) for _ in range(num_threads)]
        results = pool.starmap(select_data, args_list)
        for result in results:
            yield result
    
    pool.close()
    pool.join()

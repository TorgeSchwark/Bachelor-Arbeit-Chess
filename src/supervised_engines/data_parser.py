import math
import random
from train_variables import *
import numpy as np
import glob
import pandas as pd
from multiprocessing import Pool

import sqlite3

def get_data():
    path = DATA_PATH
    conn = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM ChessData", conn)
    if not df.empty:
        # Konvertierung der Daten in das richtige Format
        df['board'] = df['board'].apply(lambda x: [[int(value)] for value in x.split()])
        df['value'] = df['value'].apply(lambda x: [[x]])
    return df

def select_data(batch_size, data, is_train, split_index):
    if is_train:
        random_indices = np.random.choice(split_index, size=batch_size, replace=False)
    else:
        random_indices = np.random.choice(np.arange(split_index, len(data)), size=batch_size, replace=False)

    selected_inputs = np.array(data['board'].iloc[random_indices])
    selected_labels = np.array(data['value'].iloc[random_indices])
    return selected_inputs, selected_labels

def data_generator_threaded(batch_size, is_train, num_threads=15):
    data = get_data()
    split_index = int(0.7 * len(data))
    pool = Pool(num_threads)
    print("done data")
    
    while True:
        args_list = [(batch_size, data, is_train, split_index) for _ in range(num_threads)]
        results = pool.map(select_data, args_list)
        for result in results:
            yield result
    
    pool.close()
    pool.join()

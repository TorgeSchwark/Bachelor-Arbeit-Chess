import math
import random
from train_variables import *
import numpy as np
import glob
import pandas as pd
from multiprocessing import Pool

import sqlite3

def select_data(batch_size, min_rowid, max_rowid):
    
    conn = sqlite3.connect(DATA_PATH)
    cursor = conn.cursor()
    random_rowids = [random.randint(min_rowid, max_rowid) for _ in range(batch_size)]

    # SQL-Abfrage zusammenstellen, um Zeilen mit den zufälligen ROWIDs abzurufen
    placeholders = ','.join(['?'] * len(random_rowids))
    query = f"SELECT * FROM ChessData WHERE ROWID IN ({placeholders})"
    cursor.execute(query, random_rowids)
    
    data = cursor.fetchall()
    conn.close()
    
    selected_inputs = np.array([[[int(value)] for value in row[0].split()] for row in data])
    selected_labels = np.array([[[row[1]]] for row in data])
    return selected_inputs, selected_labels

def data_generator_threaded(batch_size, is_train, num_threads_train=15, num_threads_val=5):
    path = DATA_PATH
    conn = sqlite3.connect(path)
    data_size = pd.read_sql_query("SELECT COUNT(*) FROM ChessData", conn).iloc[0, 0]

    if is_train:
        max_ind = int(SPLIT* data_size)
        min_ind = 1
        pool = Pool(num_threads_train)
        num_threads = num_threads_train
    else:
        min_ind = int(SPLIT * data_size)
        max_ind = data_size
        pool = Pool(num_threads_val)
        num_threads = num_threads_val

    while True:
        args_list = [(batch_size, min_ind, max_ind) for _ in range(num_threads)]
        results = pool.starmap(select_data, args_list)
        for result in results:
            yield result
    
    pool.close()
    pool.join()

import math
import random
from train_variables import *
import numpy as np
import glob
import pandas as pd
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import time
import sqlite3

def select_data(batch_size, min_rowid, max_rowid):
    """ generates batch_size random indices in the range between min_rowid and max_rowid and queries those rows from the database """
    conn = sqlite3.connect(DATA_PATH)
    cursor = conn.cursor()
    
    random_rowids = [random.randint(min_rowid, max_rowid) for _ in range(batch_size)]

    placeholders = ','.join(['?'] * len(random_rowids))
    query = f"SELECT * FROM ChessData WHERE ROWID IN ({placeholders})"
    cursor.execute(query, random_rowids)
    
    data = cursor.fetchall()
    conn.close()
    
    selected_inputs = np.array([[[int(value)] for value in row[0].split()] for row in data])
    selected_labels = np.array([[[row[1]]] for row in data])
    return selected_inputs, selected_labels

def data_generator_threaded(batch_size, is_train, pool, num_threads_train=15, num_threads_val=5):
    """ querries the data from the database therefore utilizes all threads in the pool """
    path = DATA_PATH
    conn = sqlite3.connect(path)
    data_size = pd.read_sql_query("SELECT COUNT(*) FROM ChessData", conn).iloc[0, 0]

    if is_train:
        max_ind = int(SPLIT* data_size)
        min_ind = 1
        num_threads = num_threads_train
    else:
        min_ind = int(SPLIT * data_size)
        max_ind = data_size
        num_threads = num_threads_val

    while True:
        args_list = [(batch_size, min_ind, max_ind) for _ in range(num_threads)]
        results = pool.starmap(select_data, args_list)
        for result in results:
            yield result

def select_data_kd(path=DATA_PATH_KD, data_size=0, batch_size=BATCH_SIZE):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    data_size = pd.read_sql_query("SELECT COUNT(*) FROM ChessData", conn).iloc[0, 0]
    
    # Generiere zufällige Zeilen-IDs
    random_rowids = [random.randint(1, data_size) for _ in range(batch_size)]
    
    placeholders = ','.join(['?'] * len(random_rowids))
    query = f"SELECT board, value FROM ChessData WHERE ROWID IN ({placeholders})"
    cursor.execute(query, random_rowids)
    
    data = cursor.fetchall()
    conn.close()
    
    # Konvertiere die abgerufenen Byte-Arrays in numpy-Arrays vom Typ bool
    bool_arrays = np.array([np.frombuffer(row[0], dtype=bool) for row in data])
    selected_labels = np.array([row[1] for row in data])  # Kein Einbetten in ein 3D-Array
    
    return bool_arrays, selected_labels

def data_generator_kd(batch_size):
    path = DATA_PATH_KD
    conn = sqlite3.connect(path)
    data_size = pd.read_sql_query("SELECT COUNT(*) FROM ChessData", conn).iloc[0, 0]
    while True:
        yield select_data_kd(path, data_size)




def test_dataloader_per_second(num_seconds):
    """ tests the speed of the Dataloader for num_seconds of time returns the speed in rows per second """
    dataloader = data_generator_threaded(BATCH_SIZE, True)
    start_time = time.time()
    end_time = start_time + num_seconds
    total_data_generated = 0

    while time.time() < end_time:
        batch_inputs, batch_labels = next(dataloader)
        total_data_generated += len(batch_inputs)

    duration = time.time() - start_time
    data_per_second = total_data_generated / duration
    return data_per_second


# if __name__ == "__main__":
#     print(test_dataloader_per_second(20))
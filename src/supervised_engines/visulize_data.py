import sqlite3
import pandas as pd
import numpy as np
from train_variables import *
from multiprocessing import Pool
from train_variables import *
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

DB_SF = ".\src\supervised_engines\stockfish_depth16_DB.db"
DB_AB = ".\src\supervised_engines\lpha_beta_DB.db"

def show_table_attributes(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # SQLite-Metadaten-Abfrage, um alle Tabellen in der Datenbank abzurufen
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Iteriere über alle Tabellen
    for table in tables:
        table_name = table[0]
        print(f"Attributes of table '{table_name}':")
        
        # Abfrage, um alle Spaltennamen und deren Datentypen für die aktuelle Tabelle abzurufen
        cursor.execute(f"PRAGMA table_info('{table_name}')")
        columns = cursor.fetchall()
        
        # Ausgabe der Spaltennamen und Datentypen
        for column in columns:
            column_name = column[1]
            data_type = column[2]
            print(f"- {column_name}: {data_type}")

    conn.close()

def visuals():
    # Verbindung zu den Datenbanken herstellen
    conn_sf = sqlite3.connect(DB_SF)
   

    try:
        # Daten aus den Datenbanken abrufen
        df_sf = pd.read_sql_query("SELECT * FROM ChessData", conn_sf)
        
        # Graph für die Spalte "depth" erstellen
        plt.figure(figsize=(10, 6))
        plt.hist(df_sf['depth'], bins=20, alpha=0.5, label='SF depth16', color='blue')
        
        plt.xlabel('Depth')
        plt.ylabel('Frequency')
        plt.title('Graph of Depth')
        plt.legend()
        plt.show()

        # Graph für die Spalte "value" mit Abweichung größer als Standardabweichung und Varianz
        std_sf = df_sf['value'].std() # Berechnung der Varianz
        mean_sf = df_sf['value'].mean()

        custom_x_labels = custom_x_labels = [-1000, -600,mean_sf-std_sf, 0,mean_sf+std_sf, 600, 1000]

        plt.figure(figsize=(10, 6))
        plt.hist(df_sf['value'], bins=200, alpha=0.5, label='SF depth16', color='blue')
        
        plt.xticks(custom_x_labels)

        plt.xlabel('Evaluation')
        plt.ylabel('Frequency')
        plt.title('Graph of Evaluation')
        plt.axvline(mean_sf, color='red', linestyle='--', label='Mean SF')
        plt.axvline(mean_sf + std_sf, color='purple', linestyle='-.', label='Mean + StdDev SF')
        plt.axvline(mean_sf - std_sf, color='purple', linestyle='-.', label='Mean - StdDev SF')

        

        # Begrenzen Sie die x-Achse von -1200 bis 1200
        plt.xlim(-1200, 1200)

        plt.legend()
        plt.show()
    except Exception as e:
        print("Fehler beim Erstellen der Graphen:", e)

    finally:
        # Verbindungen schließen
        conn_sf.close()
        
def accuracy():
    # Daten definieren
    x = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    y = [191.52996238844185, 158.8586663217344, 116.6347261643704, 99.89033854511892, 115.08342104244252, 86.60550885336559, 75.91655015547958, 74.57825246250638, 59.18389642737793, 55.29444349550812, 28.10272188721334, 0]

    # Diagramm erstellen
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, marker='o', linestyle='-')
    plt.xticks(list(range(1, 17)))

    # Achsenbeschriftungen und Titel hinzufügen
    plt.xlabel('SF Depth')
    plt.ylabel('deviation in centipawn')
    plt.title('Accuracy of SF compared to SF of depth 16')

    # Gitterlinien hinzufügen
    plt.grid(True)

    # Diagramm anzeigen
    plt.show()

if __name__ == "__main__":
    visuals()

python_aproach = 125000
python_with_numpy_int8 = 60000
python_after_optimizing = 145000
python_multithreaded = 1200000
c_one_tread = 20000000


import matplotlib.pyplot as plt

# Die gegebenen Werte
labels = ['Python Normal', 'Python with NumPy int8', 'Python after optimisation', 'Python with multithreading', 'C one thread']
values = [125000, 60000, 145000, 1200000, 20000000]

# Erstellen des Balkendiagramms
plt.figure(figsize=(10, 6))
plt.bar(labels, values, color=['blue', 'orange', 'green', 'red', 'purple'])

# Hinzufügen von Titel und Beschriftungen
plt.title('Nodes per Second different implementations')
plt.xlabel('Aproaches')
plt.ylabel('Nodes per Second')

# Anzeigen des Diagramms
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


labels = ['Python Normal', 'Python with NumPy int8', 'Python after optimisation', 'Python with multithreading']
values = [125000, 60000, 145000, 1200000]

# Erstellen des Balkendiagramms
plt.figure(figsize=(10, 6))
plt.bar(labels, values, color=['blue', 'orange', 'green', 'red'])

# Hinzufügen von Titel und Beschriftungen
plt.title('Nodes per Second different implementations')
plt.xlabel('Aproaches')
plt.ylabel('Nodes per Second')

# Anzeigen des Diagramms
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

x = [1700, 1800, 1900, 2000, 2100, 2200]
y = [7.5, 7, 5.5, 8, 5.5, 3.5]

# Erstellen des Linienplots
plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o', color='blue', linestyle='-')

# Hinzufügen von Titel und Beschriftungen
plt.title('Alpha Beta vs Stockfish')
plt.xlabel('Stockfish Elo')
plt.ylabel('Won out of 10')

# Festlegen der Achsenbegrenzungen
plt.xlim(1700, 2200)
plt.ylim(0, 10)

# Anzeigen des Diagramms
plt.tight_layout()
plt.show()
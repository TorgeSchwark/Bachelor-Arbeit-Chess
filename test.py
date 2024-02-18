import numpy as np

# Definiere eine einfache Klasse
class MyClass:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"MyClass({self.value})"

# Initialisiere das leere NumPy-Array
my_array = np.empty(0, dtype=object)

# Erstelle eine Instanz der Klasse
instance = MyClass(42)

# Füge die Instanz dem NumPy-Array hinzu
my_array = np.append(my_array, instance)

# Zeige das Array an
print("NumPy-Array nach dem Hinzufügen:")
print(my_array)
print(my_array[0].value)
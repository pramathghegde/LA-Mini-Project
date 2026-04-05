import numpy as np

users = ["Aman", "Riya", "Karan", "Neha", "Arjun"]
products = ["Laptop", "Phone", "Shoes", "Watch"]

default_A = np.array([
    [5, 3, 0, 1],
    [4, 0, 0, 1],
    [1, 1, 0, 5],
    [0, 0, 5, 4],
    [0, 1, 5, 4],
])

def get_default_data():
    return default_A.copy()

def update_matrix_from_input(entry_matrix):
    new_matrix = []
    for i in range(len(users)):
        row = []
        for j in range(len(products)):
            val = entry_matrix[i][j].get()
            row.append(int(val) if val != "" else 0)
        new_matrix.append(row)
    return np.array(new_matrix)
import csv
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "ratings.csv")

DEFAULT_PRODUCTS = ["Laptop", "Phone", "Shoes", "Watch"]
DEFAULT_USERS = ["Aman", "Riya", "Karan", "Neha", "Arjun"]
DEFAULT_MATRIX = np.array([
    [5, 3, 0, 1],
    [4, 0, 0, 1],
    [1, 1, 0, 5],
    [0, 0, 5, 4],
    [0, 1, 5, 4]
])

def create_default_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User"] + DEFAULT_PRODUCTS)
            for i in range(len(DEFAULT_USERS)):
                writer.writerow([DEFAULT_USERS[i]] + list(DEFAULT_MATRIX[i]))

def load_data():
    create_default_csv()
    users, products = [], []
    with open(CSV_FILE, mode="r", newline="") as file:
        rows = list(csv.reader(file))
        if not rows:
            raise ValueError("ratings.csv is empty!")
        products = rows[0][1:]
        matrix_data = []
        for row in rows[1:]:
            if not row:
                continue

            user = row[0].strip()
            values = [x.strip() for x in row[1:]]

            while len(values) < len(products):
                values.append("0")

            users.append(user)
            matrix_data.append([int(x) if x != "" else 0 for x in values[:len(products)]])
    return users, products, np.array(matrix_data)

def get_default_data():
    users, products, matrix = load_data()
    return users, products, matrix.copy()

def update_matrix_from_input(entry_matrix):
    return np.array([
        [int(e.get().strip()) if e.get().strip() != "" else 0 for e in row]
        for row in entry_matrix
    ])

def save_data(users, products, matrix):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["User"] + products)
        for i in range(len(users)):
            writer.writerow([users[i]] + list(matrix[i]))

def add_new_user_to_csv(new_user, ratings, products):
    users, existing_products, matrix = load_data()
    if new_user in users:
        return False, "User already exists!"
    if existing_products != products:
        return False, "Product mismatch!"
    new_row = [int(x) if str(x).strip() != "" else 0 for x in ratings]
    matrix = np.array([new_row]) if matrix.size == 0 else np.vstack([matrix, new_row])
    users.append(new_user)
    save_data(users, products, matrix)
    return True, "New user added and saved to CSV!"

def delete_user_from_csv(user_to_delete):
    users, products, matrix = load_data()
    if user_to_delete not in users:
        return False, "User not found!"
    if len(users) <= 1:
        return False, "Cannot delete the last remaining user!"
    idx = users.index(user_to_delete)
    users.pop(idx)
    matrix = np.delete(matrix, idx, axis=0)
    save_data(users, products, matrix)
    return True, f"{user_to_delete} deleted successfully!"

def add_new_product_to_csv(new_product):
    users, products, matrix = load_data()
    if new_product.strip() == "":
        return False, "Product name cannot be empty!"
    if new_product in products:
        return False, "Product already exists!"
    products.append(new_product)
    new_col = np.zeros((matrix.shape[0], 1), dtype=int)
    matrix = np.hstack([matrix, new_col]) if matrix.size else new_col
    save_data(users, products, matrix)
    return True, f"Product '{new_product}' added successfully!"

def delete_product_from_csv(product_to_delete):
    users, products, matrix = load_data()
    if product_to_delete not in products:
        return False, "Product not found!"
    if len(products) <= 1:
        return False, "Cannot delete the last remaining product!"
    idx = products.index(product_to_delete)
    products.pop(idx)
    if matrix.size:
        matrix = np.delete(matrix, idx, axis=1)
    save_data(users, products, matrix)
    return True, f"Product '{product_to_delete}' deleted successfully!"

def save_current_matrix_to_csv(users, products, matrix):
    save_data(users, products, matrix)
    return True, "Current matrix saved permanently to CSV!"

import csv
import os
import numpy as np

# -------------------------------
# FILE LOCATION
# -------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "ratings.csv")

# -------------------------------
# DEFAULT DATA
# -------------------------------

DEFAULT_PRODUCTS = ["Laptop", "Phone", "Shoes", "Watch"]
DEFAULT_USERS = ["Aman", "Riya", "Karan", "Neha", "Arjun"]

DEFAULT_MATRIX = np.array([
    [5, 3, 0, 1],
    [4, 0, 0, 1],
    [1, 1, 0, 5],
    [0, 0, 5, 4],
    [0, 1, 5, 4]
])

# -------------------------------
# CREATE CSV IF MISSING
# -------------------------------

def create_default_csv():
    """
    Creates ratings.csv with default data if the file does not exist.
    """
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)

            # Header row
            writer.writerow(["User"] + DEFAULT_PRODUCTS)

            # Data rows
            for i in range(len(DEFAULT_USERS)):
                writer.writerow([DEFAULT_USERS[i]] + list(DEFAULT_MATRIX[i]))

# -------------------------------
# LOAD DATA
# -------------------------------

def load_data():
    """
    Loads users, products, and matrix from ratings.csv.
    If the file does not exist, it creates it first.
    """
    create_default_csv()

    users = []
    products = []

    with open(CSV_FILE, mode="r", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

        if len(rows) == 0:
            raise ValueError("ratings.csv is empty!")

        # First row = product headers
        products = rows[0][1:]   # skip "User"

        # Remaining rows = user + ratings
        matrix_data = []
        for row in rows[1:]:
            if len(row) < len(products) + 1:
                continue  # skip incomplete rows

            users.append(row[0])
            ratings = [int(x) if x.strip() != "" else 0 for x in row[1:]]
            matrix_data.append(ratings)

    return users, products, np.array(matrix_data)

# -------------------------------
# GET DEFAULT DATA COPY
# -------------------------------

def get_default_data():
    """
    Returns a fresh copy of data loaded from CSV.
    """
    users, products, matrix = load_data()
    return users, products, matrix.copy()

# -------------------------------
# GUI MATRIX INPUT → NUMPY MATRIX
# -------------------------------

def update_matrix_from_input(entry_matrix):
    """
    Reads values from GUI entries and returns a NEW matrix copy.
    Does NOT save to CSV.
    """
    new_matrix = []
    for i in range(len(entry_matrix)):
        row = []
        for j in range(len(entry_matrix[i])):
            val = entry_matrix[i][j].get().strip()
            row.append(int(val) if val != "" else 0)
        new_matrix.append(row)

    return np.array(new_matrix)

# -------------------------------
# SAVE FULL DATA TO CSV
# -------------------------------

def save_data(users, products, matrix):
    """
    Overwrites the CSV file with given data.
    """
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["User"] + products)

        for i in range(len(users)):
            writer.writerow([users[i]] + list(matrix[i]))

# -------------------------------
# ADD NEW USER
# -------------------------------

def add_new_user_to_csv(new_user, ratings, products):
    """
    Adds a new user permanently to CSV.
    """
    users, existing_products, matrix = load_data()

    if new_user in users:
        return False, "User already exists!"

    if existing_products != products:
        return False, "Product mismatch!"

    users.append(new_user)
    new_row = [int(x) if str(x).strip() != "" else 0 for x in ratings]

    if matrix.size == 0:
        matrix = np.array([new_row])
    else:
        matrix = np.vstack([matrix, new_row])

    save_data(users, products, matrix)
    return True, "New user added and saved to CSV!"

# -------------------------------
# DELETE USER
# -------------------------------

def delete_user_from_csv(user_to_delete):
    """
    Permanently removes a user from CSV.
    """
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

# -------------------------------
# SAVE CURRENT EDITED MATRIX
# -------------------------------

def save_current_matrix_to_csv(users, products, matrix):
    """
    Permanently saves current GUI-edited matrix to CSV.
    """
    save_data(users, products, matrix)
    return True, "Current matrix saved permanently to CSV!"
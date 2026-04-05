import numpy as np
import tkinter as tk
from tkinter import ttk, scrolledtext

# -------------------------------
# DATA
# -------------------------------

users = ["Aman", "Riya", "Karan", "Neha", "Arjun"]
products = ["Laptop", "Phone", "Shoes", "Watch"]

default_A = np.array([
    [5, 3, 0, 1],
    [4, 0, 0, 1],
    [1, 1, 0, 5],
    [0, 0, 5, 4],
    [0, 1, 5, 4],
])

A = default_A.copy()

# -------------------------------
# CORE FUNCTIONS
# -------------------------------

def fill_missing_with_mean(matrix):
    filled = matrix.copy().astype(float)
    for col in range(matrix.shape[1]):
        non_zero = matrix[:, col][matrix[:, col] != 0]
        mean = np.mean(non_zero) if len(non_zero) > 0 else 0
        for row in range(matrix.shape[0]):
            if filled[row, col] == 0:
                filled[row, col] = mean
    return filled


def compute_all(matrix):
    output = ""

    # MATRIX DISPLAY
    output += "===== USER-PRODUCT MATRIX =====\n\n"
    header = "User".ljust(10)
    for p in products:
        header += p.ljust(10)
    output += header + "\n"

    for i in range(len(users)):
        row = users[i].ljust(10)
        for j in range(len(products)):
            row += str(matrix[i][j]).ljust(10)
        output += row + "\n"

    # FILL
    A_filled = fill_missing_with_mean(matrix)
    output += "\n===== FILLED MATRIX =====\n\n" + str(A_filled) + "\n"

    # NORMALIZE
    user_means = np.mean(A_filled, axis=1, keepdims=True)
    A_norm = A_filled - user_means
    output += "\n===== NORMALIZED MATRIX =====\n\n" + str(A_norm) + "\n"

    # SIMILARITY
    similarity = A_norm @ A_norm.T
    output += "\n===== USER SIMILARITY MATRIX =====\n\n" + str(similarity) + "\n"

    # PREDICTION
    pred = np.zeros(matrix.shape)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] == 0:
                weights = similarity[i].copy()
                ratings = matrix[:, j]
                weights[i] = 0
                if np.sum(np.abs(weights)) != 0:
                    pred[i, j] = np.dot(weights, ratings) / np.sum(np.abs(weights))
                else:
                    pred[i, j] = 0
            else:
                pred[i, j] = matrix[i, j]

    output += "\n===== PREDICTED RATINGS MATRIX =====\n\n"

    header = "User".ljust(10)
    for p in products:
        header += p.ljust(12)
    output += header + "\n"

    for i in range(len(users)):
        row = users[i].ljust(10)
        for j in range(len(products)):
            row += f"{pred[i][j]:.2f}".ljust(12)
        output += row + "\n"

    # SELECTED USER
    selected = user_dropdown.get()
    if selected in users:
        idx = users.index(selected)
        unrated = np.where(matrix[idx] == 0)[0]
        output += "\n===== SELECTED USER RECOMMENDATION =====\n\n"
        if len(unrated) > 0:
            best = unrated[np.argmax(pred[idx, unrated])]
            output += f"{selected} → {products[best]} ({pred[idx][best]:.2f})\n"
        else:
            output += "All products rated\n"

    # ALL RECOMMENDATIONS
    output += "\n===== FINAL RECOMMENDATIONS =====\n\n"
    for i in range(len(users)):
        unrated = np.where(matrix[i] == 0)[0]
        if len(unrated) > 0:
            best = unrated[np.argmax(pred[i, unrated])]
            output += f"{users[i]} → {products[best]} ({pred[i][best]:.2f})\n"

    # EIGEN
    cov_matrix = A_norm.T @ A_norm
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

    output += "\n===== EIGENVALUES =====\n\n" + str(eigenvalues) + "\n"
    output += "\n===== EIGENVECTORS =====\n\n" + str(eigenvectors) + "\n"

    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, output)


# -------------------------------
# APPLY CUSTOM INPUT FOR ALL USERS
# -------------------------------

def apply_custom_values():
    global A
    try:
        new_matrix = []

        for i in range(len(users)):
            row = []
            for j in range(len(products)):
                val = entry_matrix[i][j].get()
                row.append(int(val) if val != "" else 0)
            new_matrix.append(row)

        A = np.array(new_matrix)
        compute_all(A)

    except:
        text_area.insert(tk.END, "\nInvalid Input!\n")


def reset_default():
    global A
    A = default_A.copy()

    # refill GUI fields
    for i in range(len(users)):
        for j in range(len(products)):
            entry_matrix[i][j].delete(0, tk.END)
            entry_matrix[i][j].insert(0, str(A[i][j]))

    compute_all(A)


# -------------------------------
# GUI SETUP
# -------------------------------

root = tk.Tk()
root.title("Advanced Recommendation System")
root.geometry("1000x700")

# Dropdown
tk.Label(root, text="Select User:", font=("Arial", 10)).pack()
user_dropdown = ttk.Combobox(root, values=users)
user_dropdown.set(users[0])
user_dropdown.pack(pady=5)

tk.Button(root, text="Generate Output", command=lambda: compute_all(A)).pack(pady=5)

# MATRIX INPUT GRID
tk.Label(root, text="Edit Ratings (0 = Not Rated)", font=("Arial", 10, "bold")).pack()

frame = tk.Frame(root)
frame.pack()

entry_matrix = []

# Header
for j, product in enumerate(products):
    tk.Label(frame, text=product).grid(row=0, column=j+1)

# Rows
for i, user in enumerate(users):
    tk.Label(frame, text=user).grid(row=i+1, column=0)
    row_entries = []
    for j in range(len(products)):
        entry = tk.Entry(frame, width=5)
        entry.grid(row=i+1, column=j+1)
        entry.insert(0, str(A[i][j]))
        row_entries.append(entry)
    entry_matrix.append(row_entries)

# Buttons
tk.Button(root, text="Apply Custom Matrix", command=apply_custom_values).pack(pady=5)
tk.Button(root, text="Reset Default", command=reset_default).pack(pady=5)

# Output area
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 10))
text_area.pack(expand=True, fill='both')

# Initial output
compute_all(A)

root.mainloop()
import tkinter as tk
from tkinter import ttk, scrolledtext

from data_handler import users, products, get_default_data, update_matrix_from_input
from recommender import compute_all
from display import format_matrix, format_recommendations, format_eigen

# -------------------------------
# INITIAL DATA
# -------------------------------

A = get_default_data()

# -------------------------------
# MAIN FUNCTION
# -------------------------------

def generate_output():
    global A

    # Get updated matrix from GUI
    A = update_matrix_from_input(entry_matrix)

    # Compute all matrices
    A_filled, A_norm, similarity, pred, eigenvalues, eigenvectors = compute_all(A)

    # ---------------- TERMINAL OUTPUT ----------------

    print("\n===== USER-PRODUCT MATRIX =====\n")

    header = "User".ljust(10)
    for p in products:
        header += p.ljust(10)
    print(header)

    for i in range(len(users)):
        row = users[i].ljust(10)
        for j in range(len(products)):
            row += str(A[i][j]).ljust(10)
        print(row)

    print("\n===== FILLED MATRIX =====\n")
    print(A_filled)

    print("\n===== NORMALIZED MATRIX =====\n")
    print(A_norm)

    print("\n===== USER SIMILARITY MATRIX =====\n")
    print(similarity)

    print("\n===== PREDICTED RATINGS MATRIX =====\n")

    header = "User".ljust(10)
    for p in products:
        header += p.ljust(12)
    print(header)

    for i in range(len(users)):
        row = users[i].ljust(10)
        for j in range(len(products)):
            row += f"{pred[i][j]:.2f}".ljust(12)
        print(row)

    # Selected user recommendation
    selected = user_dropdown.get()

    print("\n===== SELECTED USER RECOMMENDATION =====\n")

    idx = users.index(selected)
    unrated = [i for i, v in enumerate(A[idx]) if v == 0]

    if unrated:
        best = max(unrated, key=lambda x: pred[idx][x])
        print(f"{selected} → {products[best]} ({pred[idx][best]:.2f})")
    else:
        print("All products rated")

    # Final recommendations
    print("\n===== FINAL RECOMMENDATIONS =====\n")

    for i in range(len(users)):
        unrated = [j for j, v in enumerate(A[i]) if v == 0]
        if unrated:
            best = max(unrated, key=lambda x: pred[i][x])
            print(f"{users[i]} → {products[best]} ({pred[i][best]:.2f})")

    # Eigenvalues
    print("\n===== EIGENVALUES =====\n")
    print(eigenvalues)

    print("\n===== EIGENVECTORS =====\n")
    print(eigenvectors)

    # ---------------- GUI OUTPUT ----------------

    output = ""
    output += format_matrix(users, products, A)
    output += format_recommendations(users, products, A, pred, selected)
    output += format_eigen(eigenvalues, eigenvectors)

    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, output)


# -------------------------------
# GUI SETUP
# -------------------------------

root = tk.Tk()
root.title("Modular Recommendation System")
root.geometry("1000x700")

# Dropdown
tk.Label(root, text="Select User", font=("Arial", 10)).pack()

user_dropdown = ttk.Combobox(root, values=users)
user_dropdown.set(users[-1])
user_dropdown.pack(pady=5)

# Button
tk.Button(root, text="Generate Output", command=generate_output).pack(pady=10)

# Matrix Input Grid
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

# Output Area
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 10))
text_area.pack(expand=True, fill='both')

# Run GUI
root.mainloop()
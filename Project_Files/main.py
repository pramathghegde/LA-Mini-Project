import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from data_handler import (
    get_default_data,
    update_matrix_from_input,
    add_new_user_to_csv,
    delete_user_from_csv,
    save_current_matrix_to_csv
)
from recommender import compute_all
from display import format_matrix, format_recommendations, format_eigen

# -------------------------------
# LOAD STORED DATA FROM CSV
# -------------------------------

stored_users, stored_products, stored_A = get_default_data()

# Working copy
users = stored_users[:]
products = stored_products[:]
A = stored_A.copy()

entry_matrix = []

# -------------------------------
# REFRESH MATRIX GRID
# -------------------------------

def rebuild_matrix_grid():
    global entry_matrix, users, products, A

    for widget in frame.winfo_children():
        widget.destroy()

    entry_matrix = []

    # Header
    tk.Label(frame, text="User", font=("Arial", 10, "bold")).grid(row=0, column=0)
    for j, product in enumerate(products):
        tk.Label(frame, text=product, font=("Arial", 10, "bold")).grid(row=0, column=j+1)

    # Rows
    for i, user in enumerate(users):
        tk.Label(frame, text=user).grid(row=i+1, column=0)
        row_entries = []
        for j in range(len(products)):
            entry = tk.Entry(frame, width=6)
            entry.grid(row=i+1, column=j+1, padx=2, pady=2)
            entry.insert(0, str(A[i][j]))
            row_entries.append(entry)
        entry_matrix.append(row_entries)

    # Refresh dropdowns only if they already exist
    if "user_dropdown" in globals():
        user_dropdown["values"] = users
        if users:
            user_dropdown.set(users[0])

    if "delete_dropdown" in globals():
        delete_dropdown["values"] = users
        if users:
            delete_dropdown.set(users[0])

# -------------------------------
# GENERATE OUTPUT
# -------------------------------

def generate_output():
    global A

    try:
        A = update_matrix_from_input(entry_matrix)

        A_filled, A_norm, similarity, pred, eigenvalues, eigenvectors = compute_all(A)

        selected = user_dropdown.get()

        output = ""
        output += format_matrix(users, products, A)
        output += "\n===== FILLED MATRIX =====\n\n" + str(A_filled) + "\n"
        output += "\n===== NORMALIZED MATRIX =====\n\n" + str(A_norm) + "\n"
        output += "\n===== USER SIMILARITY MATRIX =====\n\n" + str(similarity) + "\n"
        output += "\n===== PREDICTED RATINGS MATRIX =====\n\n" + str(pred) + "\n"
        output += format_recommendations(users, products, A, pred, selected)
        output += format_eigen(eigenvalues, eigenvectors)

        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, output)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter only numbers in the rating boxes.")


# -------------------------------
# RESET TO CSV
# -------------------------------

def reset_to_csv_data():
    global users, products, A

    users, products, A = get_default_data()
    rebuild_matrix_grid()

    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, "Reloaded original data from CSV.\n")


# -------------------------------
# SAVE CURRENT GUI MATRIX TO CSV
# -------------------------------

def save_current_changes():
    global A

    try:
        A = update_matrix_from_input(entry_matrix)
        success, msg = save_current_matrix_to_csv(users, products, A)

        if success:
            messagebox.showinfo("Saved", msg)
        else:
            messagebox.showerror("Error", msg)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter only numbers before saving.")


# -------------------------------
# ADD NEW USER
# -------------------------------

def add_user():
    global users, products, A

    new_name = new_user_entry.get().strip()

    if new_name == "":
        messagebox.showerror("Error", "Please enter a user name.")
        return

    try:
        ratings = []
        for entry in new_user_ratings:
            val = entry.get().strip()
            ratings.append(int(val) if val != "" else 0)

        success, msg = add_new_user_to_csv(new_name, ratings, products)

        if success:
            messagebox.showinfo("Success", msg)

            users, products, A = get_default_data()
            rebuild_matrix_grid()

            new_user_entry.delete(0, tk.END)
            for entry in new_user_ratings:
                entry.delete(0, tk.END)

        else:
            messagebox.showerror("Error", msg)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter only numbers for the new user's ratings.")


# -------------------------------
# DELETE USER
# -------------------------------

def delete_user():
    global users, products, A

    user_to_delete = delete_dropdown.get().strip()

    if user_to_delete == "":
        messagebox.showerror("Error", "Please select a user to delete.")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to permanently delete '{user_to_delete}'?"
    )

    if not confirm:
        return

    success, msg = delete_user_from_csv(user_to_delete)

    if success:
        messagebox.showinfo("Deleted", msg)

        users, products, A = get_default_data()
        rebuild_matrix_grid()

    else:
        messagebox.showerror("Error", msg)


# -------------------------------
# GUI SETUP
# -------------------------------

root = tk.Tk()
root.title("Recommendation System (CSV + Admin Controls)")
root.geometry("1150x850")

# -------------------------------
# TOP CONTROLS
# -------------------------------

top_frame = tk.Frame(root)
top_frame.pack(pady=10)

tk.Label(top_frame, text="Select User", font=("Arial", 10)).grid(row=0, column=0, padx=5)

user_dropdown = ttk.Combobox(top_frame, values=users, width=15)
user_dropdown.grid(row=0, column=1, padx=5)

tk.Button(top_frame, text="Generate Output", command=generate_output).grid(row=0, column=2, padx=10)
tk.Button(top_frame, text="Reset to CSV Data", command=reset_to_csv_data).grid(row=0, column=3, padx=10)
tk.Button(top_frame, text="Save Current Matrix to CSV", command=save_current_changes).grid(row=0, column=4, padx=10)

# -------------------------------
# MATRIX INPUT GRID
# -------------------------------

frame = tk.Frame(root)
frame.pack(pady=10)

rebuild_matrix_grid()

# -------------------------------
# ADD USER SECTION
# -------------------------------

tk.Label(root, text="Add New User", font=("Arial", 12, "bold")).pack(pady=10)

add_user_frame = tk.Frame(root)
add_user_frame.pack()

tk.Label(add_user_frame, text="Name").grid(row=0, column=0, padx=5)
new_user_entry = tk.Entry(add_user_frame, width=12)
new_user_entry.grid(row=1, column=0, padx=5)

new_user_ratings = []
for j, product in enumerate(products):
    tk.Label(add_user_frame, text=product).grid(row=0, column=j+1, padx=5)
    entry = tk.Entry(add_user_frame, width=6)
    entry.grid(row=1, column=j+1, padx=5)
    new_user_ratings.append(entry)

tk.Button(root, text="Add User to CSV", command=add_user).pack(pady=10)

# -------------------------------
# DELETE USER SECTION
# -------------------------------

tk.Label(root, text="Delete Existing User", font=("Arial", 12, "bold")).pack(pady=10)

delete_frame = tk.Frame(root)
delete_frame.pack()

tk.Label(delete_frame, text="Select User to Delete").grid(row=0, column=0, padx=5)

delete_dropdown = ttk.Combobox(delete_frame, values=users, width=15)
delete_dropdown.grid(row=0, column=1, padx=5)

tk.Button(delete_frame, text="Delete User", command=delete_user).grid(row=0, column=2, padx=10)

# -------------------------------
# OUTPUT AREA
# -------------------------------

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 10))
text_area.pack(expand=True, fill='both', padx=10, pady=10)

root.mainloop()
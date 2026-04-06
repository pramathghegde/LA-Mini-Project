import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from data_handler import (
    get_default_data,
    update_matrix_from_input,
    add_new_user_to_csv,
    delete_user_from_csv,
    add_new_product_to_csv,
    delete_product_from_csv,
    save_current_matrix_to_csv
)
from recommender import compute_all
from display import format_matrix, format_recommendations, format_eigen

# -------------------------------
# LOAD DATA
# -------------------------------

users, products, A = get_default_data()
entry_matrix = []

# -------------------------------
# REBUILD MATRIX GRID
# -------------------------------

def rebuild_matrix_grid():
    global entry_matrix, users, products, A

    for widget in frame.winfo_children():
        widget.destroy()

    entry_matrix = []

    tk.Label(frame, text="User", font=("Arial", 10, "bold")).grid(row=0, column=0)
    for j, product in enumerate(products):
        tk.Label(frame, text=product, font=("Arial", 10, "bold")).grid(row=0, column=j+1)

    for i, user in enumerate(users):
        tk.Label(frame, text=user).grid(row=i+1, column=0)
        row_entries = []
        for j in range(len(products)):
            entry = tk.Entry(frame, width=6)
            entry.grid(row=i+1, column=j+1, padx=2, pady=2)
            entry.insert(0, str(A[i][j]))
            row_entries.append(entry)
        entry_matrix.append(row_entries)

    if "user_dropdown" in globals():
        user_dropdown["values"] = users
        if users:
            user_dropdown.set(users[0])

    # Refresh the dynamic actions panel too
    update_ui()

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
# RESET
# -------------------------------

def reset_to_csv_data():
    global users, products, A
    users, products, A = get_default_data()
    rebuild_matrix_grid()
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, "Reloaded original data from CSV.\n")

# -------------------------------
# SAVE MATRIX
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
# DYNAMIC UI (radio-button driven)
# -------------------------------

def update_ui():
    for w in dynamic_frame.winfo_children():
        w.destroy()

    act = action.get()   # "add" or "delete"
    tgt = mode.get()     # "user" or "product"

    if act == "add":
        if tgt == "user":
            # Name field
            tk.Label(dynamic_frame, text="User Name").grid(row=0, column=0, padx=5)
            user_entry = tk.Entry(dynamic_frame, width=12)
            user_entry.grid(row=0, column=1, padx=5)

            # One rating entry per product
            rating_entries = []
            for i, p in enumerate(products):
                tk.Label(dynamic_frame, text=p).grid(row=0, column=i+2, padx=3)
                e = tk.Entry(dynamic_frame, width=5)
                e.grid(row=1, column=i+2, padx=3)
                rating_entries.append(e)

            def do_add_user():
                name = user_entry.get().strip()
                if not name:
                    messagebox.showerror("Error", "Please enter a user name.")
                    return
                try:
                    ratings = [int(e.get().strip() or 0) for e in rating_entries]
                except ValueError:
                    messagebox.showerror("Error", "Ratings must be numbers.")
                    return
                global users, products, A
                success, msg = add_new_user_to_csv(name, ratings, products)
                if success:
                    users, products, A = get_default_data()
                    rebuild_matrix_grid()
                else:
                    messagebox.showerror("Error", msg)

            tk.Button(dynamic_frame, text="Add User", command=do_add_user)\
                .grid(row=0, column=len(products)+2, padx=10)

        else:  # add product
            tk.Label(dynamic_frame, text="Product Name").grid(row=0, column=0, padx=5)
            product_entry = tk.Entry(dynamic_frame, width=15)
            product_entry.grid(row=0, column=1, padx=5)

            def do_add_product():
                name = product_entry.get().strip()
                if not name:
                    messagebox.showerror("Error", "Please enter a product name.")
                    return
                global users, products, A
                success, msg = add_new_product_to_csv(name)
                if success:
                    users, products, A = get_default_data()
                    rebuild_matrix_grid()
                else:
                    messagebox.showerror("Error", msg)

            tk.Button(dynamic_frame, text="Add Product", command=do_add_product)\
                .grid(row=0, column=2, padx=10)

    else:  # delete
        tk.Label(dynamic_frame, text="Select").grid(row=0, column=0, padx=5)

        delete_dropdown = ttk.Combobox(dynamic_frame, width=15)
        delete_dropdown.grid(row=0, column=1, padx=5)

        if tgt == "user":
            delete_dropdown["values"] = users
            if users:
                delete_dropdown.set(users[0])
        else:
            delete_dropdown["values"] = products
            if products:
                delete_dropdown.set(products[0])

        def do_delete():
            target = delete_dropdown.get().strip()
            if not target:
                messagebox.showerror("Error", "Nothing selected.")
                return
            if not messagebox.askyesno("Confirm", f"Permanently delete '{target}'?"):
                return
            global users, products, A
            if tgt == "user":
                success, msg = delete_user_from_csv(target)
            else:
                success, msg = delete_product_from_csv(target)
            if success:
                users, products, A = get_default_data()
                rebuild_matrix_grid()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(dynamic_frame, text="Delete", command=do_delete)\
            .grid(row=0, column=2, padx=10)

# ===============================
# GUI LAYOUT
# ===============================

root = tk.Tk()
root.title("Recommendation System")
root.geometry("1150x850")

# --- TOP CONTROLS ---
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

tk.Label(top_frame, text="Select User", font=("Arial", 10)).grid(row=0, column=0, padx=5)
user_dropdown = ttk.Combobox(top_frame, values=users, width=15)
user_dropdown.grid(row=0, column=1, padx=5)

tk.Button(top_frame, text="Generate Output",    command=generate_output).grid(row=0, column=2, padx=10)
tk.Button(top_frame, text="Reset to CSV Data",  command=reset_to_csv_data).grid(row=0, column=3, padx=10)
tk.Button(top_frame, text="Save Matrix to CSV", command=save_current_changes).grid(row=0, column=4, padx=10)

# --- MATRIX GRID ---
frame = tk.Frame(root)
frame.pack(pady=10)

# --- RADIO BUTTONS ---
action = tk.StringVar(value="add")
mode   = tk.StringVar(value="user")

mode_frame = tk.Frame(root)
mode_frame.pack(pady=5)

# Row 1 — Add / Delete
action_frame = tk.Frame(mode_frame)
action_frame.pack()
tk.Radiobutton(action_frame, text="Add",    variable=action, value="add",    command=update_ui).pack(side=tk.LEFT, padx=10)
tk.Radiobutton(action_frame, text="Delete", variable=action, value="delete", command=update_ui).pack(side=tk.LEFT, padx=10)

# Row 2 — User / Product
target_frame = tk.Frame(mode_frame)
target_frame.pack()
tk.Radiobutton(target_frame, text="User",    variable=mode, value="user",    command=update_ui).pack(side=tk.LEFT, padx=10)
tk.Radiobutton(target_frame, text="Product", variable=mode, value="product", command=update_ui).pack(side=tk.LEFT, padx=10)

# --- DYNAMIC ACTIONS PANEL ---
dynamic_frame = tk.LabelFrame(root, text="Actions", padx=10, pady=10)
dynamic_frame.pack(pady=5, fill="x", padx=20)

# --- OUTPUT AREA ---
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 10), height=15)
text_area.pack(expand=True, fill="both", padx=10, pady=10)

# --- INIT ---
rebuild_matrix_grid()

if users:
    user_dropdown["values"] = users
    user_dropdown.set(users[0])

update_ui()

root.mainloop()

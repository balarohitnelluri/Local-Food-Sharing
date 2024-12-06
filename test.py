import tkinter as tk
from tkinter import ttk

def load_edit_window(existing_value):
    # Create the edit window
    edit_window = tk.Toplevel(root)
    edit_window.geometry("400x200")
    edit_window.title("Edit Entry")

    # Function to handle focus out
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, "Enter new value here")

    # Function to clear placeholder on focus in
    def on_focus_in(event):
        if entry.get() == "Enter new value here":
            entry.delete(0, tk.END)

    # Entry field
    entry = ttk.Entry(edit_window, width=40)
    entry.pack(pady=20)

    # Populate the entry field with existing value if present
    if existing_value:
        entry.insert(0, existing_value)
    else:
        entry.insert(0, "Enter new value here")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    # Save button
    save_button = ttk.Button(edit_window, text="Save", command=lambda: save_value(entry.get()))
    save_button.pack(pady=10)

def save_value(new_value):
    print(f"Saved Value: {new_value}")

# Root window
root = tk.Tk()
root.geometry("300x100")
root.title("Main Window")

# Sample existing value from the database
existing_value = "Existing data"

# Edit button
edit_button = ttk.Button(root, text="Edit Entry", command=lambda: load_edit_window(existing_value))
edit_button.pack(pady=30)

root.mainloop()
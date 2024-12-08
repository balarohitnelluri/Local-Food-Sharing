import tkinter as tk
from tkinter import ttk

def get_text():
    print("Entry Text:", entry.get())
    print("Label Text:", label.cget("text"))
    print("OptionMenu Value:", option_var.get())
    print("Combobox Value:", combobox.get())

root = tk.Tk()

# Entry
entry = tk.Entry(root)
entry.pack()
entry.insert(0, "Hello Entry!")

# Label
label = tk.Label(root, text="Hello Label!")
label.pack()

# OptionMenu
option_var = tk.StringVar(value="Option 1")
option_menu = tk.OptionMenu(root, option_var, "Option 1", "Option 2", "Option 3")
option_menu.pack()

# Combobox
combobox = ttk.Combobox(root, values=["Combo 1", "Combo 2", "Combo 3"])
combobox.pack()

# Button
button = tk.Button(root, text="Get Text", command=get_text)
button.pack()

root.mainloop()
import tkinter as tk

def adjust_button_position():
    # Update geometry and fetch email label's width
    root.update_idletasks()
    email_label_width = email_label.winfo_width()
    # Position the button dynamically based on label width
    change_button.place(x=email_label.winfo_x() + email_label_width + 10, y=50)

# Create main window
root = tk.Tk()
root.geometry("500x200")

# Email label
email_text = "nelluri.venugopal8172@gmail.com"
email_label = tk.Label(root, text=email_text, font=("Arial", 12, "bold"))
email_label.place(x=50, y=50)

# "Change" button
change_button = tk.Button(root, text="Change", font=("Arial", 12), fg="blue", cursor="hand2")
change_button.place(x=200, y=50)  # Initial position

# Adjust button position dynamically
adjust_button_position()

# Run the application
root.mainloop()
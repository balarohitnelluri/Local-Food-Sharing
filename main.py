import tkinter as tk
from gui.login.gui import loginWindow
from gui.main_window.main import mainWindow
from utils import executeScriptsFromFile

def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

# Main function to integrate UI and database
def main():
    try:
        # Execute database scripts
        executeScriptsFromFile("create_tables.sql")  # Initialize the database tables
    except Exception as e:
        print(f"Error initializing database: {e}")

    # Initialize the Tkinter root window
    root = tk.Tk()
    

    root.withdraw()  # Hide the root window initially

    # Launch the login window
    user_id = loginWindow()  # Get the logged-in user ID
    if user_id:
        # If login is successful, launch the main application window with the user ID
        mainWindow(user_id)
    
    root.mainloop()

# Entry point
if __name__ == "__main__":
    main()
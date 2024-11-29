import tkinter as tk
from gui.login.gui import loginWindow
from gui.main_window.main import mainWindow
from utils import executeScriptsFromFile

# Main function to integrate UI and database
def main():
    try:
        # Execute database scripts
        executeScriptsFromFile("drop_tables.sql")
        executeScriptsFromFile("create_tables.sql")  # Initialize the database tables
        executeScriptsFromFile("insert_sample_data.sql")
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
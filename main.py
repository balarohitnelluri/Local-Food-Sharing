import tkinter as tk
from user_gui.loading_window.gui import loadingwindow
from utils import executeScriptsFromFile

# Main function to integrate UI and database
def main():
    
        # Execute database scripts
        # executeScriptsFromFile("drop_tables.sql")
        # executeScriptsFromFile("create_tables.sql")  # Initialize the database tables
        # executeScriptsFromFile("insert_sample_data.sql")
    # except Exception as e:
    #     print(f"Error initializing database: {e}")

    # Initialize the Tkinter root window
        root = tk.Tk()
        root.withdraw()  # Hide the root window initially

    # Instantiate the loading screen
        loadingwindow()
    
        root.mainloop()

# Entry point
if __name__ == "__main__":
    main()
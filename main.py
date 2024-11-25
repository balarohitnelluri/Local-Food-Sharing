import tkinter as tk
from gui.login.gui import loginWindow
from gui.main_window.main import mainWindow
from utils import connect_to_database

# Function to create the required database tables and insert initial values if the tables are empty
def create_tables():
    """
    Creates tables for the Local Food Sharing App: 'users', 'food_listings', 'pickups', and optional 'reports'.
    Inserts initial data if the tables are empty.
    """
    create_users_table_query = """CREATE TABLE IF NOT EXISTS users (
        user_id INT NOT NULL AUTO_INCREMENT,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id)
    );"""

    create_food_listings_table_query = """CREATE TABLE IF NOT EXISTS food_listings (
        listing_id INT NOT NULL AUTO_INCREMENT,
        food_type VARCHAR(100) NOT NULL,
        quantity INT NOT NULL,
        expiration_date DATE NOT NULL,
        location VARCHAR(255) NOT NULL,
        pincode VARCHAR(10) NOT NULL,
        user_id INT NOT NULL,
        date_listed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (listing_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );"""

    create_pickups_table_query = """CREATE TABLE IF NOT EXISTS pickups (
        pickup_id INT NOT NULL AUTO_INCREMENT,
        user_id INT NOT NULL,
        listing_id INT NOT NULL,
        pickup_time VARCHAR(100) NOT NULL,
        status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
        date_scheduled TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (pickup_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (listing_id) REFERENCES food_listings(listing_id)
    );"""

    create_reports_table_query = """CREATE TABLE IF NOT EXISTS reports (
        report_id INT NOT NULL AUTO_INCREMENT,
        report_name VARCHAR(100),
        generated_by INT NOT NULL,
        date_generated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (report_id),
        FOREIGN KEY (generated_by) REFERENCES users(user_id)
    );"""

    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute(create_users_table_query)
        cursor.execute(create_food_listings_table_query)
        cursor.execute(create_pickups_table_query)
        cursor.execute(create_reports_table_query)
        conn.commit()
        print("Database tables created successfully.")
        
        # Check if tables are empty and insert initial data if needed
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO users (first_name, last_name, email, password)
                VALUES 
                ('John', 'Doe', 'john.doe@example.com', SHA2('password123', 256)),
                ('Jane', 'Smith', 'jane.smith@example.com', SHA2('mypassword', 256))
            """)
            conn.commit()
            print("Initial data inserted into 'users' table.")
        
        cursor.execute("SELECT COUNT(*) FROM food_listings")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO food_listings (food_type, quantity, expiration_date, location, pincode, user_id)
                VALUES 
                ('Apples', 10, '2024-12-31', '123 Main Street', '10001', 1),
                ('Bananas', 20, '2024-12-25', '456 Market Street', '10002', 2)
            """)
            conn.commit()
            print("Initial data inserted into 'food_listings' table.")

        cursor.execute("SELECT COUNT(*) FROM pickups")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO pickups (user_id, listing_id, pickup_time, status)
                VALUES 
                (1, 1, '2024-11-25 10:00', 'pending'),
                (2, 2, '2024-11-26 14:00', 'approved')
            """)
            conn.commit()
            print("Initial data inserted into 'pickups' table.")
        
        cursor.execute("SELECT COUNT(*) FROM reports")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO reports (report_name, generated_by)
                VALUES 
                ('Monthly Report - November', 1),
                ('Yearly Summary - 2024', 2)
            """)
            conn.commit()
            print("Initial data inserted into 'reports' table.")
        
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

# Main function to integrate UI and database
def main():
    create_tables()  # Initialize the database tables and insert initial data if needed

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

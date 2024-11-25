from tkinter import PhotoImage
from PIL import Image, ImageTk
from config import config
import mysql.connector



# Connect to the database
def connect_to_database():
    conn = mysql.connector.connect(
        host=config.get("DB_HOST"),
        user=config.get("DB_USER"),
        password=config.get("DB_PASSWORD"),
        database=config.get("DB_NAME")
    )
    return conn


# Style class to maintain consistent styling
class Style:
    page_heading = ('San Francisco', 25, 'bold')
    page_heading_color = '#6A0032'
    subheading_color = '#424242'
    subheading = ('San Francisco', 12, 'bold')
    caption = ('Arial', 10)
    level_one_subheading_color = '#424242'
    level_one_subheading = ('Poppins', 15, 'bold')
    level_three_subheading = ('Poppins', 13)


# Function to resize images for Tkinter
def resize_image(size, image_url):
    """Function to resize an image for Tkinter.

    Args:
        size (tuple): Size of the image (width, height).
        image_url (str): URL or path of the image.

    Returns:
        tk_image: Resized image for Tkinter.
    """
    original_image = Image.open(f'{image_url}')
    resized_image = original_image.resize((size[0], size[1]))
    tk_image = ImageTk.PhotoImage(resized_image)
    return tk_image



# Fetch food listings based on search criteria
def fetch_food_listings(food_type_filter, pincode_filter, expiration_filter):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    query = """
    SELECT listing_id, food_type, quantity, expiration_date, location, pincode
    FROM food_listings
    WHERE food_type LIKE %s AND pincode = %s AND expiration_date >= %s
    ORDER BY expiration_date ASC
    """
    cursor.execute(query, (f"%{food_type_filter}%", pincode_filter, expiration_filter))
    results = cursor.fetchall()
    conn.close()
    
    return results

# Function to save a new user (donor or recipient) into the database
def save_user(first_name, last_name, role, email, password):
    """Save user information (donor or recipient) to the database."""
    
    # Connect to the database
    conn = connect_to_database()
    cursor = conn.cursor()

    # Check if the user already exists
    select_query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(select_query, (email,))
    user = cursor.fetchone()
    if user:
        return (False, f"User with email {email} already exists")

    # Insert the new user
    insert_query = """
        INSERT INTO users (first_name, last_name, role, email, password) 
        VALUES (%s, %s, %s, %s, %s)
    """
    user_info = (
        first_name.lower(),
        last_name.lower(),
        role.lower(),
        email.lower(),
        password
    )
    cursor.execute(insert_query, user_info)
    conn.commit()
    conn.close()
    return (True, f"User with email {email} has been created")


# Authenticate the user during login
def authenticate_user(email, password):
    """Authenticate user credentials."""
    
    # Connect to the database
    conn = connect_to_database()
    cursor = conn.cursor()

    # Check if email exists in the database
    select_query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(select_query, (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        saved_password = user[4]
        if password == "":
            return (False, "Empty Password")
        if saved_password != password:
            return (False, "Incorrect Password")
        return (True, "Logged In")
    else:
        return (False, "Invalid Email")

def checkUser(email, hashed_password):
    """
    Validates user credentials.

    Args:
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.

    Returns:
        bool: True if the user exists and credentials match, False otherwise.
    """
    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Query to check if the email and hashed password match
        query = "SELECT user_id FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, hashed_password))

        # Fetch the result
        result = cursor.fetchone()

        # Return True if a match is found, else False
        return result is not None

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False

    finally:
        if conn:
            conn.close()
            
# Retrieve user information by email
def get_user_info(email):
    """Fetch user details by email."""
    
    # Connect to the database
    conn = connect_to_database()
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user_info = cursor.fetchone()
    conn.close()
    return user_info


# Fetch all available food listings
def get_food_listings():
    """Fetch all food listings from the database."""
    
    # Connect to the database
    conn = connect_to_database()
    cursor = conn.cursor()

    query = "SELECT food_type, quantity, expiration_date FROM food_listings"
    cursor.execute(query)
    listings = cursor.fetchall()
    conn.close()
    return listings


# Save new food listing by a donor
def save_food_listing(donor_id, food_type, quantity, expiration_date, location):
    """Save a new food listing to the database."""
    
    # Connect to the database
    conn = connect_to_database()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO food_listings (donor_id, food_type, quantity, expiration_date, location)
        VALUES (%s, %s, %s, %s, %s)
    """
    listing_info = (donor_id, food_type, quantity, expiration_date, location)
    cursor.execute(insert_query, listing_info)
    conn.commit()
    conn.close()
    return True


# Schedule a food pickup by a recipient
def schedule_pickup(recipient_id, listing_id, pickup_time):
    """Schedule a food pickup for a recipient."""
    
    # Connect to the database
    conn = connect_to_database()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO pickups (recipient_id, listing_id, pickup_time)
        VALUES (%s, %s, %s)
    """
    pickup_info = (recipient_id, listing_id, pickup_time)
    cursor.execute(insert_query, pickup_info)
    conn.commit()
    conn.close()
    return True


# Fetch all scheduled pickups for a user
def get_scheduled_pickups(user_id):
    """Retrieve all pickups scheduled for a recipient."""
    
    # Connect to the database
    conn = connect_to_database()
    cursor = conn.cursor()

    query = "SELECT * FROM pickups WHERE recipient_id = %s"
    cursor.execute(query, (user_id,))
    pickups = cursor.fetchall()
    conn.close()
    return pickups


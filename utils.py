from tkinter import PhotoImage,messagebox
from PIL import Image, ImageTk
from config import config
import mysql.connector
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from CTkMessagebox import CTkMessagebox
import re
import sqlite3
from sqlite3 import OperationalError
from cryptography.fernet import Fernet
import os
from datetime import datetime,date



# Connect to the database
def connect_to_database():
    conn = mysql.connector.connect(
        host=config.get("DB_HOST"),
        user=config.get("DB_USER"),
        password=config.get("DB_PASSWORD"),
        database=config.get("DB_NAME")
    )
    return conn

# Generate or load encryption key
KEY_FILE = "key.key"
PREFERENCES_FILE = "preferences.txt"

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

# Ensure encryption key exists
generate_key()
encryption_key = load_key()
cipher_suite = Fernet(encryption_key)

def save_preferences(self, username, password):
    """Save the username and encrypted password to a file."""
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()  # Encrypt password
    with open(PREFERENCES_FILE, "w") as file:
        file.write(f"{username}\n")
        file.write(f"{encrypted_password}\n")
        file.write(f"{self.remember_var.get()}")  # Save the checkbox state

def load_preferences(self):
        try:
            with open(PREFERENCES_FILE, "r") as file:
                lines = file.readlines()
                username = lines[0].strip()
                encrypted_password = lines[1].strip()
                remember_me = int(lines[2].strip())

                # Populate the fields with decrypted data
                self.username_entry.insert(0, username)
                decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
                self.password_entry.insert(0, decrypted_password)
                self.remember_var.set(remember_me)
        except (FileNotFoundError, IndexError):
            # If no preferences file exists or it's corrupted, do nothing
            pass

def clear_preferences(self):
    with open(PREFERENCES_FILE, "w") as file:
        file.truncate()  # Empty the file



def center_test(win):
    win.update_idletasks()
    screen_width = win.winfo_width()
    screen_height = win.winfo_height()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    position_x = (screen_width // 2) - (screen_width // 2)
    position_y = (screen_height // 2) - (screen_height // 2)
    win.geometry(f"{screen_width}x{screen_height}+{position_x}+{position_y}")




def center_window(root, width, height):
 
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the position for the window to be centered
    position_x = (screen_width // 2) - (width // 2)
    position_y = (screen_height // 2) - (height // 2)

    # Set the geometry of the window
    root.geometry(f"{width}x{height}+{position_x}+{position_y}")


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

# Retrieve user information by email
def get_user_info_id(id):
    
    # Connect to the database
    conn = connect_to_database()
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE user_id = %s"
    cursor.execute(query, (id,))
    user_info = cursor.fetchone()
    conn.close()
    return user_info

def update_users_table(query_from, values):
    conn = connect_to_database()  # Get the connection
    cursor = conn.cursor()  # Create the cursor object

    query = query_from
    
    try:
        cursor.execute(query, values)  # Execute the query
        conn.commit()  # Commit the transaction using the connection object
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()  # Always close the cursor
        conn.close()  # Always close the connection


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

def send_email(email,subject,body):
        
        # Email details
        sender_email = "localfoodsharing@gmail.com"  # Replace with your email
        sender_password = "qdis uprp jcfr qslt"     # Replace with your email password
        recipient_email = email

        # Compose the email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        # Send the email using SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)  # For Gmail
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()



def validation(**kwargs):
    for key,value in kwargs.items():
        email=kwargs.get('email',None)
        password=kwargs.get('password',None)
        name=kwargs.get('name',None)
        phone=kwargs.get('phone', None)
        date_input=kwargs.get('date',None)
        gender=kwargs.get('gender',None)
        address1=kwargs.get('address1',None)
        city=kwargs.get('city',None)
        state=kwargs.get('state',None)
        zipcode=kwargs.get('zipcode',None)
        country=kwargs.get('country',None)
        

    #Email Validation
    if email is not None:
        email_valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        try:
            if email_valid is None:
                raise ValueError("Invalid email address!")
        except ValueError as email_error:
            return email_error
    
    #Password validation

    if password is not None:
        password_valid = re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$",password)
        try:
            if password_valid is None:
                raise ValueError("(Please choose strong password)")
        except ValueError as weak_pass:
            return weak_pass

    #Name Validation
    if name is not None:
        name_validation=re.match("^[a-zA-Z\s]+$", name.strip())
        try:
            if name_validation is None :
                raise ValueError("Please enter only 'Alphabets'") 
            if name==None or name=="":
                raise NameError("Shouldn't be empty, please enter your Name")
        except NameError as empty_value:
            return empty_value
        except ValueError as invalid_name:
            return  invalid_name
    
    #Phone number validation
    if phone is not None:
        pattern = re.compile(r"^\d{10}$")  # E.164 format: +123456789 or 123456789
        try:
            if pattern.fullmatch(phone) is None:
                raise ValueError("Please enter valid phone number")
            elif phone==None or phone=="":
                 raise NameError("Please enter a phone number") 
        except NameError as empty_value:
            return empty_value
        except ValueError as invalid_name:
            return  invalid_name
    
    if date_input is not None:
        date_format = "%m-%d-%Y"
        try:
            # Ensure the input is a string; if it's a `date`, format it
            if isinstance(date_input, date):  # `date` is correctly referenced
                date_input = date_input.strftime(date_format)

            # Attempt to parse the date
            datetime.strptime(date_input, date_format)
            return None  # Date is valid
        except ValueError:
            return "Please select a valid date"

        

    #gender Validation    
    if gender is not None:
        gender_list=["Male","Female","Other"]
        try:
            if gender not in gender_list:
                raise ValueError("Please select gender")
        except ValueError as gender_notselected:
            return gender_notselected
        
    #Address1 Validation
    if address1 is not None:
        if not address1 or len(address1) < 3:
            return "Invalid Address #1. Must be at least 3 characters."
    
    #city Validation
    if city is not None:
        if not re.match(r"^[A-Za-z\s]+$", city):
            return "Invalid city. Use only letters and spaces."
        
    #state Validation
    if state is not None:
        if not re.match(r"^[A-Za-z\s]{2,}$", state):
            return "Invalid state. Use only letters (2+ characters)." 
    
    #country Validation
    if country is not None:
        if not re.match(r"^[A-Za-z\s]+$", country):
            return "Invalid country. Use only letters and spaces."
        
    #Zipcode Validation
    if zipcode is not None:
        if not re.match(r"^\d{5}(-\d{4})?$", zipcode):
            return "Invalid zip code. Use format: 12345 or 12345-6789."
    

        

def executeScriptsFromFile(filename):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        fd = open(f"sql/{filename}", 'r')
        sqlFile = fd.read()
        fd.close()

        # Split SQL commands
        sqlCommands = sqlFile.split(';')

        # Execute every command
        for command in sqlCommands:
            if command.strip():  # Skip empty commands
                try:
                    cursor.execute(command)
                    conn.commit()
                except OperationalError as msg:
                    print(f"Command skipped: {msg}")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    except FileNotFoundError:
        print("SQL file not found!")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
            
        
        



        


    
    
    

    

    
    







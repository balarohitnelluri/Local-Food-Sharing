import mysql.connector
import os
import matplotlib.pyplot as pt
from PIL import Image 

# Configurations
from config import config
from dotenv import load_dotenv

load_dotenv()  # Imports environemnt variables from the '.env' file

# ===================SQL Connectivity=================

# SQL Connection
connection = mysql.connector.connect(
    host=config.get("DB_HOST"),
    user=config.get("DB_USER"),
    password=config.get("DB_PASSWORD"),
    database=config.get("DB_NAME"),
    port="3306",
    autocommit=config.get("DB_AUTOCOMMIT"),
)

cursor = connection.cursor(buffered=True)

# SQL functions


def checkUser(username, password=None):
    """
    Checks if a user exists in the 'users' table with the given username (email) and password.
    Returns the user_id if a match is found.
    """
    try:
        # Use a parameterized query to securely check the user
        if password:
            cmd = "SELECT user_id FROM users WHERE email = %s AND BINARY password = %s"
            cursor.execute(cmd, (username, password))
            user_id = cursor.fetchone()
            return user_id[0] if user_id else None
        else:
            cmd = "SELECT COUNT(*) FROM users WHERE email = %s"
            cursor.execute(cmd, (username,))
            exists = cursor.fetchone()
            return exists[0] > 0
    except Exception as e:
        print(f"Error checking user: {e}")
        return None
    

def get_unique_pincodes(user_id):
    """
    Fetches all unique pincodes from the food_listings table.

    Returns:
        list: A list of unique pincodes.
    """
    try:
        query = "SELECT DISTINCT pincode FROM food_listings where user_id != %s"
        cursor.execute(query,(user_id))
        results = cursor.fetchall()

        # Convert fetched results into a simple list of pincodes
        pincodes = [row[0] for row in results]
        return pincodes

    except Exception as e:
        print(f"Error fetching pincodes: {e}")
        return []


def get_food_items(user_id=None):
    """
    Fetches food items from the food_listings table. If user_id is provided,
    fetches food items specific to the user.

    Args:
        user_id (int, optional): The ID of the user to filter food items by.

    Returns:
        list: A list of dictionaries where each dictionary represents a food item.
    """
    try:
        if user_id:
            query = """
            SELECT listing_id, food_type, quantity, location, expiration_date, pincode, date_listed
            FROM food_listings
            WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
        else:
            query = """
            SELECT listing_id, food_type, quantity, location, expiration_date, pincode, date_listed
            FROM food_listings
            """
            cursor.execute(query)

        food_items = cursor.fetchall()

        return food_items
    except Exception as e:
        print(f"Error retrieving food items: {e}")
        return []
    
def request_pickup(user_id, listing_id, pickup_date, pickup_time):
    """
    Saves a pickup request to the pickups table.

    Args:
        user_id (int): The ID of the user requesting the pickup.
        listing_id (int): The ID of the food listing to be picked up.
        pickup_date (str): The date for the pickup in 'YYYY-MM-DD' format.
        pickup_time (str): The time for the pickup in 'HH:MM' format.

    Returns:
        bool: True if the pickup request is successfully saved, False otherwise.
    """
    try:
        # Insert pickup request into the database
        query = """
        INSERT INTO pickups (user_id, listing_id, pickup_time, status, date_scheduled)
        VALUES (%s, %s, %s, %s, NOW())
        """
        full_pickup_time = f"{pickup_date} {pickup_time}"  # Combine date and time
        cursor.execute(query, (user_id, listing_id, full_pickup_time, "pending"))
        return True

    except Exception as e:
        print(f"Error saving pickup request: {e}")
        return False

import mysql.connector

def add_food_items_bulk(food_items, user_id):
    """
    Adds multiple food items to the database in a single transaction.

    Args:
        food_items (list): List of dictionaries containing food item details.
        user_id (int): The ID of the user adding the items.

    Returns:
        bool: True if items were added successfully, False otherwise.
    """
    try:

        # SQL query to insert food items
        query = """
            INSERT INTO food_listings (food_type, quantity, expiration_date, location, pincode, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Prepare the values for bulk insertion
        values = [
            (
                item["food_type"],  # Food Type
                item["quantity"],  # Quantity
                item["expiry_date"],  # Expiry Date
                item["location"],  # Location
                item["zipcode"],  # Zipcode
                user_id,  # User ID
            )
            for item in food_items
        ]

        # Execute the query in bulk
        cursor.executemany(query, values)

        return True  # Items added successfully
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return False

def get_listing_details(user_id):
    """
    Fetch food listing details for a specific pincode, excluding listings by the current user.

    Args:
        user_id (int): The ID of the current user.
        pincode (str): The selected pincode.

    Returns:
        dict: A dictionary where the keys are food types and values are tuples of (listing_id, address).
    """
    try:
        query = """
            SELECT food_type, listing_id, location
            FROM food_listings
            WHERE user_id != %s
        """
        cursor.execute(query, ( user_id))
        results = cursor.fetchall()

        # Populate the dictionary with food type as key and (listing_id, location) as value
        listings = {row[0]: (row[1], row[2]) for row in results}
        return listings
    
    except Exception as e:
        print(f"Error fetching listing details: {e}")



def get_request_details(user_id):
    """
    Fetch details of all pickup requests made by the current user.

    Args:
        user_id (int): The ID of the current user.

    Returns:
        list: A list of dictionaries where each dictionary represents a request with
              details like listing_id, food_type, location, and pickup_time.
    """

    try:
        query = """
            SELECT p.listing_id, fl.food_type, fl.location, p.pickup_time, p.status
            FROM pickups AS p
            JOIN food_listings AS fl ON p.listing_id = fl.listing_id
            WHERE p.user_id = %s
        """
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

        # Structure the data into a list of dictionaries
        requests = [
            {
                "listing_id": row[0],
                "food_type": row[1],
                "location": row[2],
                "pickup_time": row[3],
                "status": row[4],
            }
            for row in results
        ]

    except Exception as e:
        print(f"Error fetching request details: {e}")

    return requests




def create_user(first_name, last_name, email, password):
    try:
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, email, password))

        return True
    except Exception as e:
        print(f"Error adding User: {e}")
        return False
    


def add_food_item(food_type, quantity, location, zipcode, expiry_date, user_id):
    """
    Adds a new food item to the food_listings table.

    Args:
        food_type (str): Type of the food (e.g., Vegetables, Fruits, etc.).
        quantity (int): Quantity of the food.
        location (str): Location where the food is available.
        zipcode (str): The pincode of the location.
        expiry_date (str): The expiration date of the food item (YYYY-MM-DD).
        user_id (int): ID of the user adding the food item.

    Returns:
        bool: True if the item was successfully added, False otherwise.
    """
    try:
        query = """
            INSERT INTO food_listings (food_type, quantity, expiration_date, location, pincode, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (food_type, quantity, expiry_date, location, zipcode, user_id))
        return True
    except Exception as e:
        print(f"Error adding food item: {e}")
        return False

    

def available_food_count():
    """
    Retrieves the total available food quantity from the 'food_listings' table.
    """
    try:
        cmd = """
        SELECT SUM(quantity) 
        FROM food_listings 
        WHERE listing_id NOT IN (SELECT listing_id FROM pickups WHERE status = 'approved')
        """
        cursor.execute(cmd)
        result = cursor.fetchone()[0]
        return result if result else 0

    except Exception as e:
        print(f"Error retrieving available food count: {e}")
        return 0

def donated_food_count():
    """
    Retrieves the total donated food quantity from the 'food_listings' table.
    """
    try:
        cmd = "SELECT SUM(quantity) FROM food_listings"
        cursor.execute(cmd)
        result = cursor.fetchone()[0]
        return result if result else 0

    except Exception as e:
        print(f"Error retrieving donated food count: {e}")
        return 0


def get_total_donation_value(average_value_per_unit=5):
    """
    Calculates the total monetary value of donated food.
    Assumes an average value per unit is provided as a parameter.
    """
    try:
        total_donated = donated_food_count()
        total_value = total_donated * average_value_per_unit
        return total_value

    except Exception as e:
        print(f"Error calculating total donation value: {e}")
        return 0

def meals_distributed():
    """
    Retrieves the total meals distributed based on approved pickups in the 'pickups' table.
    """
    try:
        cmd = """
        SELECT SUM(f.quantity) 
        FROM food_listings f 
        INNER JOIN pickups p ON f.listing_id = p.listing_id
        WHERE p.status = 'approved'
        """
        cursor.execute(cmd)
        result = cursor.fetchone()[0]
        return result if result else 0

    except Exception as e:
        print(f"Error retrieving meals distributed: {e}")
        return 0


def human_format(num):
    if num < 1000:
        return num

    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000
    return "%.1f%s" % (num, ["", "K", "M", "G", "T", "P"][magnitude])


def updatePassword(email, password):
    cmd = f"update users set password='{password}' where email='{email}' limit 1;"
    cursor.execute(cmd)
    cmd = f"select count(email) from users where email='{email}' and password='{password}';"
    cursor.execute(cmd)
    return cursor.fetchone()[0] >= 1


def updateUsername(oldusername, password, newusername):
    cmd = f"update login set username='{newusername}' where username='{oldusername}' and password='{password}' limit 1;"
    cursor.execute(cmd)
    cmd = f"select count(username) from login where username='{newusername}' and password='{password}''"
    cursor.execute(cmd)
    return cursor.fetchone()[0] >= 1



def find_g_id(name):
    cmd = f"select g_id from guests where name = '{name}'"
    cursor.execute(cmd)
    out = cursor.fetchone()[0]
    return out


def checkin(g_id):
    cmd = f"select * from reservations where g_id = '{g_id}';"
    cursor.execute(cmd)
    reservation = cursor.fetchall()
    if reservation != []:
        subcmd = f"update reservations set check_in = curdate() where g_id = '{g_id}' "
        cursor.execute(subcmd)
        return "successful"
    else:
        return "No reservations for the given Guest"



def checkout(id):
    cmd = f"update reservations set check_out=current_timestamp where id={id} limit 1;"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


# ============Python Functions==========


def acceptable(*args, acceptables):
    """
    If the characters in StringVars passed as arguments are in acceptables return True, else returns False
    """
    for arg in args:
        for char in arg:
            if char.lower() not in acceptables:
                return False
    return True



# Get all guests
def get_guests():
    cmd = "select id, name, address, email_id, phone, created_at from guests;"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return cursor.fetchall()


# Add a guest
def add_guest(name, address, email_id, phone):
    cmd = f"insert into guests(name,address,email_id,phone) values('{name}','{address}','{email_id}',{phone});"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


# add a room
def add_room(room_no, price, room_type):
    cmd = f"insert into rooms(room_no,price,room_type) values('{room_no}',{price},'{room_type}');"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


# Get All rooms
def get_rooms():
    cmd = "select id, room_no, room_type, price, created_at from rooms;"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return cursor.fetchall()


# Get all reservations
def get_reservations():
    cmd = "select id, g_id, r_id, check_in, check_out, meal from reservations;"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return cursor.fetchall()


# Add a reservation
def add_reservation(g_id, meal, r_id, check_in="now"):
    cmd = f"insert into reservations(g_id,check_in,r_id, meal) values('{g_id}',{f'{chr(39) + check_in + chr(39)}' if check_in != 'now' else 'current_timestamp'},'{meal}','{r_id}');"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


# Get all room count
def get_total_rooms():
    cmd = "select count(room_no) from rooms;"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return cursor.fetchone()[0]


# Check if a room is vacant
def booked():
    cmd = f"select count(ros.id) from reservations rs, rooms ros where rs.r_id = ros.id and rs.check_out is Null;"
    cursor.execute(cmd)

    return cursor.fetchone()[0]


def vacant():
    return get_total_rooms() - booked()


def bookings():
    cmd = f"select count(rs.id) from reservations rs , rooms ros where rs.r_id = ros.id and ros.room_type = 'D';"
    cursor.execute(cmd)
    deluxe = cursor.fetchone()[0]

    cmd1 = f"select count(rs.id) from reservations rs , rooms ros where rs.r_id = ros.id and ros.room_type = 'N';"
    cursor.execute(cmd1)
    Normal = cursor.fetchone()[0]

    return [deluxe, Normal]


# Get total hotel value
def get_total_hotel_value():
    cmd = "select sum(price) from rooms;"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    value = cursor.fetchone()[0]

    return human_format(value)


def delete_reservation(id):
    cmd = f"delete from reservations where id='{id}';"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


def delete_room(id):
    cmd = f"delete from rooms where id='{id}';"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


def delete_guest(id):
    cmd = f"delete from guests where id='{id}';"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


def update_rooms(id, room_no, room_type, price):
    cmd = f"update rooms set room_type = '{room_type}',price= {price}, room_no = {room_no} where id = {id};"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


def update_guests(name, address, id, phone):

    cmd = f"update guests set address = '{address}',phone = {phone} , name = '{name}' where id = {id};"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


def update_reservations(
    g_id, check_in, room_id, reservation_date, check_out, meal, type, id
):
    cmd = f"update reservations set check_in = '{check_in}',check_out = '{check_out}',g_id = {g_id}, \
        r_date = '{reservation_date}',meal = {meal},r_type='{type}', r_id = {room_id} where id= {id};"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True


def meals():
    cmd = f"select sum(meal) from reservations;"
    cursor.execute(cmd)
    meals = cursor.fetchone()[0]

    return human_format(meals)


def update_reservation(id, g_id, check_in, room_id, check_out, meal):
    cmd = f"update reservations set check_in = '{check_in}', check_out = '{check_out}', g_id = {g_id}, meal = '{meal}', r_id = '{room_id}' where id= '{id}';"
    cursor.execute(cmd)
    if cursor.rowcount == 0:
        return False
    return True

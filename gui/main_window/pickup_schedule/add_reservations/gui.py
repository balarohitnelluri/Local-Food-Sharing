import customtkinter as ctk
from tkinter import ttk, messagebox, Frame
from tkcalendar import DateEntry
from utils import connect_to_database


class SchedulePickup(Frame):
    def __init__(self, parent, user_id, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.user_id = user_id
        self.food_type_mapping = {}  # Dictionary to map food type to listing_id
        self.selected_listing_address = None  # Store the selected listing's address

        # Outer tkinter Frame for wrapping
        self.configure(bg="#EDEDED")

        # Central CTKFrame to hold all fields
        central_frame = ctk.CTkFrame(
            self,
            width=800,
            height=500,
            corner_radius=20,
            fg_color="#F4F4F4",
        )
        central_frame.place(relx=0.35, rely=0.45, anchor="center")

        # Title
        title_label = ctk.CTkLabel(
            central_frame,
            text="Schedule a Pickup",
            font=("Montserrat Bold", 24),
            text_color="#5E95FF",
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Pincode Frame
        pincode_frame = ctk.CTkFrame(central_frame, fg_color="#FFFFFF", corner_radius=10)
        pincode_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        pincode_label = ctk.CTkLabel(
            pincode_frame,
            text="Select Pincode",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        pincode_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.pincode_var = ctk.StringVar(value="Select Pincode")
        self.pincode_dropdown = ttk.Combobox(
            pincode_frame, textvariable=self.pincode_var, state="readonly", width=27
        )
        self.pincode_dropdown.grid(row=1, column=0, padx=10, pady=10)
        self.populate_pincode_dropdown()

        # Food Type Frame
        food_type_frame = ctk.CTkFrame(central_frame, fg_color="#FFFFFF", corner_radius=10)
        food_type_frame.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        food_type_label = ctk.CTkLabel(
            food_type_frame,
            text="Select Food Type",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        food_type_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.food_type_var = ctk.StringVar(value="Select Food Type")
        self.food_type_dropdown = ttk.Combobox(
            food_type_frame, textvariable=self.food_type_var, state="readonly", width=27
        )
        self.food_type_dropdown.grid(row=1, column=0, padx=10, pady=10)

        # Bind the pincode selection to populate food type dropdown
        self.pincode_dropdown.bind("<<ComboboxSelected>>", self.populate_food_type_dropdown)

        # Date and Time Frame
        date_time_frame = ctk.CTkFrame(central_frame, fg_color="#FFFFFF", corner_radius=10)
        date_time_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        date_label = ctk.CTkLabel(
            date_time_frame,
            text="Pickup Date",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        date_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.date_picker = DateEntry(
            date_time_frame,
            date_pattern="yyyy-mm-dd",
            font=("Montserrat", 14),
            background="#5E95FF",
            foreground="white",
            borderwidth=2,
        )
        self.date_picker.grid(row=0, column=1, padx=10, pady=10)

        time_label = ctk.CTkLabel(
            date_time_frame,
            text="Pickup Time (HH:MM)",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        time_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.time_entry = ctk.CTkEntry(
            date_time_frame, placeholder_text="HH:MM", font=("Montserrat", 14)
        )
        self.time_entry.grid(row=1, column=1, padx=10, pady=10)

        # Button Frame
        button_frame = ctk.CTkFrame(central_frame, fg_color="#FFFFFF", corner_radius=10)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        add_button = ctk.CTkButton(
            button_frame,
            text="Request Pickup",
            font=("Montserrat Bold", 16),
            fg_color="#5E95FF",
            corner_radius=10,
            command=self.schedule_pickup,
        )
        add_button.grid(row=0, column=0, pady=10)

    def populate_pincode_dropdown(self):
        """Populate the pincode dropdown with options from the database."""
        conn = connect_to_database()
        cursor = conn.cursor()
        try:
            query = """
                SELECT DISTINCT pincode
                FROM food_listings
                WHERE user_id != %s
            """
            cursor.execute(query, (self.user_id,))
            pincodes = cursor.fetchall()
            self.pincode_dropdown["values"] = [str(row[0]) for row in pincodes]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load pincodes: {e}")
        finally:
            conn.close()

    def populate_food_type_dropdown(self, event):
        """Populate the food type dropdown based on the selected pincode."""
        selected_pincode = self.pincode_var.get()
        conn = connect_to_database()
        cursor = conn.cursor()
        try:
            query = """
                SELECT food_type, listing_id, location
                FROM food_listings
                WHERE pincode = %s AND user_id != %s
            """
            cursor.execute(query, (selected_pincode, self.user_id))
            listings = cursor.fetchall()

            # Store food types and their corresponding listing IDs in a dictionary
            self.food_type_mapping = {row[0]: (row[1], row[2]) for row in listings}
            self.food_type_dropdown["values"] = list(self.food_type_mapping.keys())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load food types: {e}")
        finally:
            conn.close()

    def schedule_pickup(self):
        """Schedule a pickup based on the selected options."""
        pincode = self.pincode_var.get()
        food_type = self.food_type_var.get()
        pickup_date = self.date_picker.get()
        pickup_time = self.time_entry.get()

        if pincode == "Select Pincode" or food_type == "Select Food Type":
            messagebox.showerror("Error", "Please select a valid pincode and food type.")
            return

        if not pickup_time:
            messagebox.showerror("Error", "Please enter a valid time.")
            return

        conn = connect_to_database()
        cursor = conn.cursor()
        try:
            # Retrieve the listing_id and address for the selected food type
            listing_id, listing_address = self.food_type_mapping[food_type]
            sql = """
                INSERT INTO pickups (user_id, listing_id, pickup_time, status, date_scheduled)
                VALUES (%s, %s, %s, %s, NOW())
            """
            cursor.execute(
                sql, (self.user_id, listing_id, f"{pickup_date} {pickup_time}", "pending")
            )
            conn.commit()

            messagebox.showinfo("Success", f"Pickup request sent!\nAddress: {listing_address}")
            self.pincode_var.set("Select Pincode")
            self.food_type_var.set("Select Food Type")
            self.time_entry.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()

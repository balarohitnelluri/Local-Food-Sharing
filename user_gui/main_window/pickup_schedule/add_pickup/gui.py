import customtkinter as ctk
from tkinter import ttk, messagebox, Frame
from tkcalendar import DateEntry
from utils import connect_to_database


class SchedulePickup(Frame):
    def __init__(self, parent, user_id, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.user_id = user_id
        self.food_type_mapping = {}  # Dictionary to map food type to listing_id and expiration_date

        # Outer tkinter Frame for wrapping
        self.configure(bg="#FFFFFF")

        # Central CTKFrame to hold all fields
        self.central_frame = ctk.CTkFrame(
            self,
            width=700,
            height=400,
            corner_radius=15,
            fg_color="#F4F4F4",
        )
        self.central_frame.place(relx=0.4, rely=0.42, anchor="center")
        self.central_frame.pack_propagate(False)
        self.central_frame.grid_propagate(False)

        self.central_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.central_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Pincode Dropdown
        pincode_label = ctk.CTkLabel(
            self.central_frame,
            text="Select Pincode",
            font=("Montserrat Bold", 12),
            text_color="#5E95FF",
        )
        pincode_label.grid(row=0, column=0, padx=15, pady=5, sticky="e")

        self.pincode_var = ctk.StringVar(value="Select Pincode")
        self.pincode_dropdown = ttk.Combobox(
            self.central_frame, textvariable=self.pincode_var, state="readonly", width=27
        )
        self.pincode_dropdown.grid(row=0, column=1, padx=15, pady=5, sticky="w")
        self.populate_pincode_dropdown()

        # Food Type Dropdown
        food_type_label = ctk.CTkLabel(
            self.central_frame,
            text="Select Food Type",
            font=("Montserrat Bold", 12),
            text_color="#5E95FF",
        )
        food_type_label.grid(row=1, column=0, padx=15, pady=5, sticky="e")

        self.food_type_var = ctk.StringVar(value="Select Food Type")
        self.food_type_dropdown = ttk.Combobox(
            self.central_frame, textvariable=self.food_type_var, state="readonly", width=27
        )
        self.food_type_dropdown.grid(row=1, column=1, padx=15, pady=5, sticky="w")
        self.pincode_dropdown.bind("<<ComboboxSelected>>", self.populate_food_type_dropdown)

        # Date Picker
        date_label = ctk.CTkLabel(
            self.central_frame,
            text="Pickup Date",
            font=("Montserrat Bold", 12),
            text_color="#5E95FF",
        )
        date_label.grid(row=2, column=0, padx=15, pady=5, sticky="e")

        self.date_picker = DateEntry(
            self.central_frame,
            date_pattern="yyyy-mm-dd",
            font=("Montserrat", 12),
            background="#5E95FF",
            foreground="white",
            borderwidth=2,
        )
        self.date_picker.grid(row=2, column=1, padx=15, pady=5, sticky = "w")

        # Time Picker Dropdowns
        time_label = ctk.CTkLabel(
            self.central_frame,
            text="Pickup Time (HH:MM)",
            font=("Montserrat Bold", 12),
            text_color="#5E95FF",
        )
        time_label.grid(row=3, column=0, padx=15, pady=5, sticky="e")

        self.hour_var = ctk.StringVar(value="HH")
        self.hour_dropdown = ttk.Combobox(
            self.central_frame, textvariable=self.hour_var, state="readonly", width=5,
            values=[f"{i:02}" for i in range(24)],
        )
        self.hour_dropdown.grid(row=3, column=1, padx=15, pady=5, sticky="w")

        self.minute_var = ctk.StringVar(value="MM")
        self.minute_dropdown = ttk.Combobox(
            self.central_frame, textvariable=self.minute_var, state="readonly", width=5,
            values=[f"{i:02}" for i in range(0, 60, 5)],
        )
        self.minute_dropdown.grid(row=3, column=1, padx=80, pady=5, sticky="w")

        # Schedule Button
        schedule_button = ctk.CTkButton(
            self.central_frame,
            text="Request Pickup",
            font=("Montserrat Bold", 14),
            fg_color="#5E95FF",
            corner_radius=10,
            command=self.schedule_pickup,
        )
        schedule_button.grid(row=4, column=0, columnspan=3, pady=10)

        # Table for displaying requested pickups
        self.create_requested_items_table(self.central_frame)

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
                SELECT food_type, listing_id, expiration_date
                FROM food_listings
                WHERE pincode = %s AND user_id != %s
            """
            cursor.execute(query, (selected_pincode, self.user_id))
            listings = cursor.fetchall()

            self.food_type_mapping = {row[0]: (row[1], row[2]) for row in listings}
            self.food_type_dropdown["values"] = list(self.food_type_mapping.keys())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load food types: {e}")
        finally:
            conn.close()

    def create_requested_items_table(self, parent):
        table_frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=10)
        table_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.table = ttk.Treeview(
            table_frame,
            columns=("Food Type", "Quantity", "Pickup Date", "Pickup Time", "Status"),
            show="headings",
            height = 5,
        )
        self.table.grid(row=0, column=0, sticky="nsew")

        # Configure column headings
        self.table.heading("Food Type", text="Food Type")
        self.table.heading("Quantity", text="Quantity")
        self.table.heading("Pickup Date", text="Pickup Date")
        self.table.heading("Pickup Time", text="Pickup Time")
        self.table.heading("Status", text="Status")

        # Set column widths
        self.table.column("Food Type", anchor="center", width=100)
        self.table.column("Quantity", anchor="center", width=80)
        self.table.column("Pickup Date", anchor="center", width=100)
        self.table.column("Pickup Time", anchor="center", width=100)
        self.table.column("Status", anchor="center", width=80)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.populate_requested_items_table()

    def populate_requested_items_table(self):
        """Populate the table with user-requested pickup items."""
        conn = connect_to_database()
        cursor = conn.cursor()
        try:
            query = """
                SELECT food_type, quantity, DATE_FORMAT(pickup_time, '%Y-%m-%d'), 
                       TIME_FORMAT(pickup_time, '%H:%i'), status
                FROM pickups
                JOIN food_listings ON pickups.listing_id = food_listings.listing_id
                WHERE pickups.user_id = %s
            """
            cursor.execute(query, (self.user_id,))
            rows = cursor.fetchall()
            self.table.delete(*self.table.get_children())  # Clear existing rows
            for row in rows:
                self.table.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load requested items: {e}")
        finally:
            conn.close()

    def schedule_pickup(self):
        pincode = self.pincode_var.get()
        food_type = self.food_type_var.get()
        pickup_date = self.date_picker.get()
        pickup_time = f"{self.hour_var.get()}:{self.minute_var.get()}"

        if pincode == "Select Pincode" or food_type == "Select Food Type":
            messagebox.showerror("Error", "Please select a valid pincode and food type.")
            return

        if self.hour_var.get() == "HH" or self.minute_var.get() == "MM":
            messagebox.showerror("Error", "Please select a valid pickup time.")
            return

        listing_id, expiration_date = self.food_type_mapping[food_type]
        if pickup_date >= expiration_date.strftime("%Y-%m-%d"):
            messagebox.showerror("Error", "Pickup date must be before the item's expiration date.")
            return

        conn = connect_to_database()
        cursor = conn.cursor()
        try:
            sql = """
                INSERT INTO pickups (user_id, listing_id, pickup_time, status, date_scheduled)
                VALUES (%s, %s, %s, %s, NOW())
            """
            cursor.execute(sql, (self.user_id, listing_id, f"{pickup_date} {pickup_time}", "pending"))
            conn.commit()
            messagebox.showinfo("Success", "Pickup request scheduled successfully!")
            self.populate_requested_items_table()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()

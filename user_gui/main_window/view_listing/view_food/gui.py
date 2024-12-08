from tkinter import Frame, StringVar, ttk
import customtkinter as ctk
from tkcalendar import DateEntry
from utils import connect_to_database
from CTkMessagebox import CTkMessagebox


class FindFood(Frame):
    def __init__(self, parent, user_id, *args, **kwargs):
        """
        Initializes the FindFood frame.
        :param parent: Parent container.
        :param user_id: The ID of the currently logged-in user.
        """
        Frame.__init__(self, parent, *args, **kwargs)
        self.user_id = user_id  # Store user_id for user-specific operations
        self.selected_zip_code = StringVar()
        self.selected_date = StringVar()

        self.configure(bg="#FFFFFF")
        self.pack_propagate(False)  # Prevent resizing
        self.pack(fill="both", expand=False)

        # Main Frame
        self.central_frame = ctk.CTkFrame(
            self, width=700, height=400, corner_radius=15, fg_color="#F4F4F4"
        )
        self.central_frame.place(relx=0.4, rely=0.42, anchor="center")
        self.central_frame.pack_propagate(False)  # Prevent resizing
        self.central_frame.grid_propagate(False)

        # Input Fields
        self.create_input_fields()

        # Call the function to populate the zip code dropdown
        self.populate_zip_code_dropdown()

        # Search Button
        self.search_button = ctk.CTkButton(
            self.central_frame,
            text="Search Food",
            command=self.search_food,
            width=140,
            corner_radius=8,
            fg_color="#5E95FF",
        )
        self.search_button.grid(row=3, column=4, columnspan=2, pady=10)

        # Results Table
        self.create_results_table()

        # Configure grid weights for consistent layout
        self.central_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    def create_input_fields(self):
        """Create input fields for searching food items."""
        # Zip Code Dropdown
        self.zip_code_label = ctk.CTkLabel(
            self.central_frame, text="Select Zip Code:", font=("Montserrat", 12)
        )
        self.zip_code_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.zip_code_dropdown = ctk.CTkOptionMenu(
            self.central_frame,
            variable=self.selected_zip_code,
            values=[],
            width=150,
        )
        self.zip_code_dropdown.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Date Picker
        self.date_label = ctk.CTkLabel(
            self.central_frame, text="Select Date:", font=("Montserrat", 12)
        )
        self.date_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.date_picker = DateEntry(
            self.central_frame,
            textvariable=self.selected_date,
            date_pattern="yyyy-mm-dd",
            font=("Montserrat", 10),
            background="#5E95FF",
            foreground="white",
            borderwidth=2,
        )
        self.date_picker.grid(row=1, column=2, padx=5, pady=5, sticky="w")

    def create_results_table(self):
        """Create a table using ttk.Treeview to display search results."""
        self.results_table = ttk.Treeview(
            self.central_frame,
            columns=("Listing ID", "Food Type", "Quantity", "Location", "Date Listed"),
            show="headings",
        )
        self.results_table.grid(row=4, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

        # Configure column headings
        self.results_table.heading("Listing ID", text="Listing ID")
        self.results_table.heading("Food Type", text="Food Type")
        self.results_table.heading("Quantity", text="Quantity")
        self.results_table.heading("Location", text="Location")
        self.results_table.heading("Date Listed", text="Date Listed")

        # Set column widths
        self.results_table.column("Listing ID", anchor="center", width=80)
        self.results_table.column("Food Type", anchor="center", width=120)
        self.results_table.column("Quantity", anchor="center", width=100)
        self.results_table.column("Location", anchor="center", width=180)
        self.results_table.column("Date Listed", anchor="center", width=120)

        # Add a scrollbar to the table
        self.scrollbar = ttk.Scrollbar(
            self.central_frame, orient="vertical", command=self.results_table.yview
        )
        self.results_table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=4, column=6, sticky="ns")

    def populate_zip_code_dropdown(self):
        """
        Fetch unique zip codes from the database and populate the dropdown.
        """
        conn = connect_to_database()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT DISTINCT pincode FROM food_listings")
            zip_codes = cursor.fetchall()
            zip_code_list = [str(row[0]) for row in zip_codes]
            self.zip_code_dropdown.configure(values=zip_code_list)
            if zip_code_list:
                self.selected_zip_code.set(zip_code_list[0])  # Set the first value as default
            else:
                self.selected_zip_code.set("No Zip Codes Available")
        except Exception as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="error")
        finally:
            conn.close()

    def search_food(self):
        """
        Search and display food items by selected zip code and date.
        """
        selected_zip_code = self.selected_zip_code.get()
        selected_date = self.selected_date.get()

        if not selected_zip_code or selected_zip_code == "No Zip Codes Available":
            CTkMessagebox(title="Validation Error", message="Please select a valid zip code to search.", icon="warning")
            return

        if not selected_date:
            CTkMessagebox(title="Validation Error", message="Please select a date to filter.", icon="warning")
            return

        # Clear existing results
        for item in self.results_table.get_children():
            self.results_table.delete(item)

        conn = connect_to_database()
        cursor = conn.cursor()

        try:
            query = """
            SELECT listing_id, food_type, quantity, location, date_listed
            FROM food_listings
            WHERE pincode = %s AND date_listed >= %s AND expiration_date >= CURDATE() AND listing_id NOT IN (
                SELECT listing_id FROM pickups WHERE status = 'approved'
            )
            """
            cursor.execute(query, (selected_zip_code, selected_date))
            results = cursor.fetchall()

            if results:
                for row in results:
                    self.results_table.insert("", "end", values=row)
                CTkMessagebox(title="Success", message="Results fetched successfully!", icon="check")
            else:
                CTkMessagebox(title="No Results", message="No food listings found for the selected criteria.", icon="info")
        except Exception as e:
            CTkMessagebox(title="Database Error", message=f"An error occurred: {e}", icon="error")
        finally:
            conn.close()

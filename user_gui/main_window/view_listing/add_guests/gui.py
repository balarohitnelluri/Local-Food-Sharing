from tkinter import Frame, StringVar, messagebox, ttk
import customtkinter as ctk
from tkcalendar import DateEntry
from utils import connect_to_database


class FindFood(Frame):
    def __init__(self, parent, user_id, *args, **kwargs):
        """
        Initializes the FindFood frame.
        :param parent: Parent container.
        :param user_id: The ID of the currently logged-in user.
        """
        Frame.__init__(self, parent, *args, **kwargs)
        self.user_id = user_id  # Store user_id for user-specific operations
        self.selected_pincode = StringVar()
        self.selected_date = StringVar()

        # Main Frame to hold all components
        self.main_frame = ctk.CTkFrame(
            self,
            width=800,
            height=500,
            corner_radius=15,
            fg_color="#F4F4F4",
        )
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Pincode Dropdown
        pincode_frame = ctk.CTkFrame(self.main_frame, fg_color="#FFFFFF", corner_radius=10)
        pincode_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        pincode_label = ctk.CTkLabel(
            pincode_frame,
            text="Select Pincode",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        pincode_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        self.pincode_dropdown = ctk.CTkOptionMenu(
            pincode_frame,
            variable=self.selected_pincode,
            values=[],
            font=("Montserrat", 14),
            width=200,
        )
        self.pincode_dropdown.grid(row=1, column=0, padx=(10, 10), pady=(0, 10))
        self.populate_pincode_dropdown()

        # Date Picker
        date_frame = ctk.CTkFrame(self.main_frame, fg_color="#FFFFFF", corner_radius=10)
        date_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        date_label = ctk.CTkLabel(
            date_frame,
            text="Select Date",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        date_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        self.date_picker = DateEntry(
            date_frame,
            textvariable=self.selected_date,
            date_pattern="yyyy-mm-dd",
            font=("Montserrat", 14),
            background="#5E95FF",
            foreground="white",
            borderwidth=2,
        )
        self.date_picker.grid(row=1, column=0, padx=(10, 10), pady=(0, 10))

        # Search Button
        search_button = ctk.CTkButton(
            self.main_frame,
            text="Search Food",
            command=self.search_food,
            width=150,
            height=40,
            font=("Montserrat Bold", 14),
            corner_radius=10,
            fg_color="#5E95FF",
            hover_color="#417BFF",
        )
        search_button.grid(row=1, column=0, columnspan=2, pady=(20, 10))

        # Results Table
        results_frame = ctk.CTkFrame(self.main_frame, fg_color="#FFFFFF", corner_radius=10)
        results_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(20, 10), sticky="nsew")

        self.tree = ttk.Treeview(
            results_frame,
            columns=("Listing ID", "Food Type", "Quantity", "Location", "Date Listed"),
            show="headings",
            height=10,
        )
        self.tree.heading("Listing ID", text="Listing ID")
        self.tree.heading("Food Type", text="Food Type")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Date Listed", text="Date Listed")
        self.tree.column("Listing ID", anchor="center", width=100)
        self.tree.column("Food Type", anchor="center", width=150)
        self.tree.column("Quantity", anchor="center", width=100)
        self.tree.column("Location", anchor="center", width=200)
        self.tree.column("Date Listed", anchor="center", width=150)
        self.tree.pack(fill="both", expand=True)

    def populate_pincode_dropdown(self):
        """
        Fetch unique pincodes from the database and populate the dropdown.
        """
        conn = connect_to_database()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT DISTINCT pincode FROM food_listings")
            pincodes = cursor.fetchall()
            pincode_list = [str(row[0]) for row in pincodes]
            self.pincode_dropdown.configure(values=pincode_list)
            self.selected_pincode.set(pincode_list[0] if pincode_list else "Select Pincode")
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def search_food(self):
        """
        Search and display food items by selected pincode and date.
        """
        selected_pincode = self.selected_pincode.get()
        selected_date = self.selected_date.get()

        if not selected_pincode or selected_pincode == "Select Pincode":
            messagebox.showerror("Error", "Please select a pincode to search.")
            return

        if not selected_date:
            messagebox.showerror("Error", "Please select a date to filter.")
            return

        # Clear existing results
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = connect_to_database()
        cursor = conn.cursor()

        try:
            query = """
            SELECT listing_id, food_type, quantity, location, date_listed
            FROM food_listings
            WHERE pincode = %s AND date_listed >= %s AND user_id != %s
            """
            cursor.execute(query, (selected_pincode, selected_date, self.user_id))
            results = cursor.fetchall()

            if results:
                for row in results:
                    self.tree.insert("", "end", values=row)
            else:
                messagebox.showinfo("No Results", "No food listings found for the selected criteria.")
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

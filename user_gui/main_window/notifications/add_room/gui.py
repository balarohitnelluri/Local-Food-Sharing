from pathlib import Path
from tkinter import Frame, ttk, messagebox
import customtkinter as ctk
from utils import connect_to_database

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class ViewRequests(Frame):
    def __init__(self, parent, user_id, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.user_id = user_id  # Current user ID
        self.configure(bg="#FFFFFF")

        # Outer Frame
        outer_frame = ctk.CTkFrame(
            self,
            width=800,
            height=400,
            corner_radius=20,
            fg_color="#F4F4F4",
        )
        outer_frame.place(relx=0.05, rely=0.1)

        # Title
        title_label = ctk.CTkLabel(
            outer_frame,
            text="View Requests",
            font=("Montserrat Bold", 20),
            text_color="#5E95FF",
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Tabs for Requests Raised and Received
        tab_frame = ctk.CTkFrame(outer_frame, fg_color="#FFFFFF", corner_radius=10)
        tab_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        raised_button = ctk.CTkButton(
            tab_frame,
            text="Requests Raised",
            command=self.view_raised_requests,
            fg_color="#5E95FF",
            corner_radius=10,
        )
        raised_button.grid(row=0, column=0, padx=10, pady=10)

        received_button = ctk.CTkButton(
            tab_frame,
            text="Requests Received",
            command=self.view_received_requests,
            fg_color="#5E95FF",
            corner_radius=10,
        )
        received_button.grid(row=0, column=1, padx=10, pady=10)

        # Table to Display Requests
        self.tree_frame = ctk.CTkFrame(outer_frame, fg_color="#FFFFFF", corner_radius=10)
        self.tree_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("Request ID", "Food Type", "Pickup Time", "Status", "Address"),
            show="headings",
            height=10,
        )
        self.tree.heading("Request ID", text="Request ID")
        self.tree.heading("Food Type", text="Food Type")
        self.tree.heading("Pickup Time", text="Pickup Time")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Address", text="Address")

        self.tree.column("Request ID", anchor="center", width=80)
        self.tree.column("Food Type", anchor="center", width=150)
        self.tree.column("Pickup Time", anchor="center", width=150)
        self.tree.column("Status", anchor="center", width=100)
        self.tree.column("Address", anchor="center", width=200)

        self.tree.pack(fill="both", expand=True)

        # Load raised requests by default
        self.view_raised_requests()

    def view_raised_requests(self):
        """
        Fetch and display requests raised by this user to others.
        """
        self.clear_table()
        conn = connect_to_database()
        cursor = conn.cursor()

        try:
            query = """
                SELECT p.pickup_id, f.food_type, p.pickup_time, p.status, f.location 
                FROM pickups p
                INNER JOIN food_listings f ON p.listing_id = f.listing_id
                WHERE p.user_id = %s
            """
            cursor.execute(query, (self.user_id,))
            results = cursor.fetchall()

            for row in results:
                self.tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def view_received_requests(self):
        """
        Fetch and display requests raised by others to this user.
        """
        self.clear_table()
        conn = connect_to_database()
        cursor = conn.cursor()

        try:
            query = """
                SELECT p.pickup_id, f.food_type, p.pickup_time, p.status, f.location 
                FROM pickups p
                INNER JOIN food_listings f ON p.listing_id = f.listing_id
                WHERE f.user_id = %s
            """
            cursor.execute(query, (self.user_id,))
            results = cursor.fetchall()

            for row in results:
                self.tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def clear_table(self):
        """
        Clears the table content.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

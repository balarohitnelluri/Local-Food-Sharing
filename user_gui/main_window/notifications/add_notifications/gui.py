import os
import pandas as pd
from pathlib import Path
from tkinter import Frame, ttk, messagebox
import customtkinter as ctk
from utils import connect_to_database

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
REPORTS_FOLDER = OUTPUT_PATH / Path("./reports")


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
            width=700,
            height=400,
            corner_radius=15,
            fg_color="#F4F4F4",
        )
        outer_frame.place(relx=0.4, rely=0.42, anchor="center")
        outer_frame.grid_propagate(False)

        # Tabs for Requests Raised and Received
        tab_frame = ctk.CTkFrame(outer_frame, fg_color="#FFFFFF", corner_radius=10)
        tab_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.raised_button = ctk.CTkButton(
            tab_frame,
            text="Requests Raised",
            command=self.view_raised_requests,
            fg_color="#5E95FF",
            corner_radius=10,
        )
        self.raised_button.grid(row=0, column=0, padx=10, pady=10)

        self.received_button = ctk.CTkButton(
            tab_frame,
            text="Requests Received",
            command=self.view_received_requests,
            fg_color="#5E95FF",
            corner_radius=10,
        )
        self.received_button.grid(row=0, column=1, padx=10, pady=10)

        # Table to Display Requests
        self.tree_frame = ctk.CTkFrame(outer_frame, fg_color="#FFFFFF", corner_radius=10, width=700, height=300)
        self.tree_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

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
        self.tree.column("Food Type", anchor="center", width=120)
        self.tree.column("Pickup Time", anchor="center", width=150)
        self.tree.column("Status", anchor="center", width=120)
        self.tree.column("Address", anchor="center", width=200)

        self.tree.pack(fill="both", expand=True)

        # Action Buttons
        self.action_frame = ctk.CTkFrame(outer_frame, fg_color="#F4F4F4", corner_radius=10)
        self.action_frame.grid(row=2, column=0, columnspan=2, pady=(10, 20))
        self.action_frame.grid_remove()  # Hidden by default

        self.accept_button = ctk.CTkButton(
            self.action_frame,
            text="Accept Request",
            fg_color="#4CAF50",
            command=lambda: self.update_selected_request_status("approved"),
            corner_radius=10,
            width=150,
            height=40,
        )
        self.accept_button.grid(row=0, column=0, padx=10, pady=10)

        self.decline_button = ctk.CTkButton(
            self.action_frame,
            text="Decline Request",
            fg_color="#F44336",
            command=lambda: self.update_selected_request_status("rejected"),
            corner_radius=10,
            width=150,
            height=40,
        )
        self.decline_button.grid(row=0, column=1, padx=10, pady=10)

        # Generate Report Button
        self.generate_report_button = ctk.CTkButton(
            outer_frame,
            text="Generate Report",
            fg_color="#5E95FF",
            command=self.generate_report,
            corner_radius=10,
            width=200,
            height=40,
        )
        self.generate_report_button.grid(row=3, column=0, columnspan=2, pady=(10, 20))

        # Load raised requests by default
        self.view_raised_requests()

    def view_raised_requests(self):
        """
        Fetch and display requests raised by this user to others.
        """
        self.action_frame.grid_remove()  # Hide action buttons
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

    def generate_report(self):
        """
        Generate an Excel report by joining all primary tables.
        """
        if not os.path.exists(REPORTS_FOLDER):
            os.makedirs(REPORTS_FOLDER)

        conn = connect_to_database()
        cursor = conn.cursor(dictionary=True)

        try:
            # Query to fetch donor and recipient information, along with food details
            query = """
                SELECT 
                    donors.user_id AS donor_id,
                    CONCAT(donors.first_name, ' ', donors.last_name) AS donor_name,
                    recipients.user_id AS recipient_id,
                    CONCAT(recipients.first_name, ' ', recipients.last_name) AS recipient_name,
                    f.food_type,
                    f.quantity,
                    f.expiration_date,
                    f.location,
                    f.pincode,
                    p.pickup_time,
                    p.status
                FROM pickups p
                INNER JOIN food_listings f ON p.listing_id = f.listing_id
                INNER JOIN users donors ON f.user_id = donors.user_id
                INNER JOIN users recipients ON p.user_id = recipients.user_id
                WHERE donors.user_id = %s OR recipients.user_id = %s
            """
            cursor.execute(query, (self.user_id, self.user_id))
            results = cursor.fetchall()

            if not results:
                messagebox.showinfo("Info", "No data available to generate a report.")
                return

            # Save to Excel
            df = pd.DataFrame(results)
            report_path = REPORTS_FOLDER / f"report_user{self.user_id}.xlsx"
            df.to_excel(report_path, index=False)

            # Add entry to the reports table
            cursor.execute(
                "INSERT INTO reports (report_name, generated_by) VALUES (%s, %s)",
                (f"report_user{self.user_id}", self.user_id),
            )
            conn.commit()

            messagebox.showinfo("Success", f"Report generated and saved to {report_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
        finally:
            conn.close()


    def view_received_requests(self):
        """
        Fetch and display requests raised by others to this user.
        """
        self.action_frame.grid()  # Show action buttons
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

    def update_selected_request_status(self, status):
        """
        Update the status of the selected request in the database.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a request to update.")
            return

        request_id = self.tree.item(selected_item)["values"][0]
        conn = connect_to_database()
        cursor = conn.cursor()

        try:
            query = """
                UPDATE pickups
                SET status = %s
                WHERE pickup_id = %s
            """
            cursor.execute(query, (status, request_id))
            conn.commit()

            messagebox.showinfo("Success", f"Request {status.capitalize()} successfully!")
            self.view_received_requests()  # Refresh table

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

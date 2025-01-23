from pathlib import Path
from tkinter import Frame, StringVar
import customtkinter as ctk
from tkcalendar import DateEntry,Calendar
from utils import center_window,validation,get_user_info_id,update_users_table,send_email
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
from tkinter import Frame
from controller import *
import customtkinter as ctk
from pathlib import Path
from tkinter import (
    Toplevel,
    Frame,
    StringVar,
    ttk,
    Frame,
    
)


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class AddFoodForm(Frame):
    def __init__(self, parent, user_id, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.user_id = user_id  
        self.data = {
            "food_type": StringVar(),
            "quantity": StringVar(),
            "location": StringVar(),
            "zipcode": StringVar(),
            "expiry_date": StringVar(),
        }

        self.configure(bg="white")

        self.side_frame = ctk.CTkFrame(
            self,
            width=169,
            height=506,
            fg_color="white",
            bg_color="white",
        )
        self.side_frame.place(x=0, y=112)

        # Sidebar title
        donate_label = ctk.CTkLabel(
            self,
            text="Donate Food",
            font=("Montserrat Bold", 36,"bold"),
            text_color="#B3B3B3",
        )
        donate_label.place(x=25 , y=39)

        #Donate button
        self.donate_btn = ctk.CTkButton(
            self.side_frame,
            text="Donate",
            width=169,
            height=50,
            corner_radius=0,
            fg_color="#F2F2F2",
            text_color="#B3B3B3",
            border_color="#D2D2D2",
            border_width=1,
            font=("Montserrat Bold", 16,"bold"),
            command=self.donate_ui,
            state="disabled",
        )
        self.donate_btn.place(x=0, y=0)


        self.my_listings_btn = ctk.CTkButton(
            self.side_frame,
            text="My Listing",
            command=self.load_my_listings,
            width=169,
            height=50,
            corner_radius=0,
            fg_color="#FFFFFF",
            text_color="#B3B3B3",
            hover_color="#F2F2F2",
            border_color="#D2D2D2",
            border_width=1,
            font=("Montserrat Bold", 16,"bold"),
        )
        self.my_listings_btn.place(x=0, y=50)

        self.requests_btn = ctk.CTkButton(
            self.side_frame,
            text="Pick Up Requests",
            command=self.pickup_requests,
            width=169,
            height=50,
            corner_radius=0,
            fg_color="#FFFFFF",
            text_color="#B3B3B3",
            border_color="#D2D2D2",
            border_width=1,
            hover_color="#F2F2F2",
            font=("Montserrat Bold", 16,"bold"),
            state="disabled"
        )
        self.requests_btn.place(x=0, y=100)

        self.error_label=ctk.CTkLabel(
            self,
            text="*Error",
            font=("Montserrat Bold", 14,),
            text_color="white",
        )
        self.error_label.place(x=350, y=79)
    
        self.donate_ui()

        self.scrollable_frame.update_idletasks()

    def donate_ui(self):

        self.donate_btn.configure(fg_color="#F2F2F2",state="disabled")
        self.my_listings_btn.configure(fg_color="#FFFFFF",state="enable")
        self.requests_btn.configure(fg_color="#FFFFFF",state="enable")


        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            width=733,
            height=370,
            fg_color="white",
            border_color="#D2D2D2",
            border_width=1,
        )
        self.scrollable_frame.place(x=169, y=113)

        self.scrollable_frame.grid_columnconfigure(0, weight=1) 
        self.scrollable_frame.grid_columnconfigure(1, weight=0)  
        self.scrollable_frame.grid_columnconfigure(2, weight=1)  
        self.scrollable_frame.grid_columnconfigure(3, weight=1)  

        # Title Label
        title_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Create Food Listing",
            font=("Montserrat Bold", 20, "bold"),
            text_color="#848484",
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=15, sticky="ew")  



        category_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Food Type:*",
            font=("Montserrat Bold", 16, "bold"),
            text_color="#B3B3B3",
        )
        category_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")


        self.category_list=["Fruits", "Vegetables", "Grains", "Dairy", "Protein", "Snacks", "Beverages", "Sweets/Desserts", "Prepared Meals", "Others"]
        self.category_entry =  ctk.CTkOptionMenu(
            self.scrollable_frame,
            values=self.category_list,
            width=110,
            height=18,
            fg_color="white",
            font=("Montserrat", 12),
            corner_radius=5,
            text_color="black",
            button_color="#6C9FFF"
        )
        self.category_entry.set("Select a category")
        self.category_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Quantity
        quantity_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Quantity:*",
            font=("Montserrat Bold", 16, "bold"),
            text_color="#B3B3B3",
        )
        quantity_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.quantity_var = ctk.StringVar(value="Select Quantity")  
        self.quantity_list = [str(i) for i in range(1, 10)] + ["10+"]  

        self.quantity_entry = ctk.CTkOptionMenu(
            self.scrollable_frame,
            values=self.quantity_list,
            variable=self.quantity_var,
            width=110,
            height=18,
            fg_color="white",
            font=("Montserrat", 12),
            corner_radius=5,
            text_color="black",
            button_color="#6C9FFF"
        )
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Expiration Date
        expiration_date_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Expiration Date:*",
            font=("Montserrat Bold", 16, "bold"),
            text_color="#B3B3B3",
        )
        expiration_date_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")


        self.expiration_selected_date="Select Expiration"
        self.expiration_date_picker = ctk.CTkButton(
            self.scrollable_frame,
            text=self.expiration_selected_date,
            width=110,
            height=18,
            fg_color="white",
            text_color="black",
            hover_color="#D2D2D2",
            border_color="#B3B3B3",
            border_width=1,
            corner_radius=5,
            command=self.open_calendar,
            font=("Montserrat Bold", 12,),
        )
        self.expiration_date_picker.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Pincode
        location_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Location:*",
            font=("Montserrat Bold", 16, "bold"),
            text_color="#B3B3B3",
        )
        location_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.location_entry = ctk.CTkEntry(
            self.scrollable_frame,
            placeholder_text="Enter Location",
            font=("Montserrat Bold", 12),
            width=225,
            height=25,
            border_color="#B3B3B3",
            border_width=1,
            corner_radius=5
        )
        self.location_entry.grid(row=4, column=1, padx=10, pady=10,sticky="w")

        # Pincode
        pincode_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Zipcode:*",
            font=("Montserrat Bold", 16, "bold"),
            text_color="#B3B3B3",
        )
        pincode_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.pincode_entry = ctk.CTkEntry(
            self.scrollable_frame,
            placeholder_text="Enter pincode",
            font=("Montserrat Bold", 12),
            width=110,
            height=25,
            border_color="#B3B3B3",
            border_width=1,
            corner_radius=5
        )
        self.pincode_entry.grid(row=5, column=1, padx=10, pady=10,sticky="w")

        # Submit Button
        submit_button = ctk.CTkButton(
            self.scrollable_frame,
            text="Submit Listing",
            command=self.submit_listing,
            font=("Montserrat Bold", 16, "bold"),
            fg_color="#5E95FF",
            text_color="white",
            hover_color="#417BFF",
            width=150,
            height=39,
            corner_radius=10,
        )
        submit_button.grid(row=6, column=1, pady=15, padx=10, sticky="") 

        # Update the scrollable frame
        self.scrollable_frame.update_idletasks()

    def open_calendar(self):
        # Create a Toplevel winqdow
        top = Toplevel(self.scrollable_frame)
        top.title("Select Date")
        top.geometry("300x200")  
        center_window(top,300,200)

        # Define the maximum selectable date
        max_date = date.today() - relativedelta(years=18)  

        min_date = date.today() - relativedelta(years=18) 

        # Create a custom ttk style for the calendar
        style = ttk.Style(self.scrollable_frame)
        style.theme_use("default")  
        style.configure(
            "Treeview",
            background="lightgrey",  
            foreground="black",      
            fieldbackground="lightgrey",  
            rowheight=25,            
        )
        style.map(
            "Treeview",
            background=[("selected", "#6C9FFF")],  
            foreground=[("selected", "white")], 
        )

        # Create the Calendar widget
        self.calendar = Calendar(
            top,
            selectmode="day",
            #maxdate=max_date,
            mindate=date.today(),
            date_pattern="yyyy-mm-dd",
        )
        self.calendar.place(x=50, y=25)

        def select_date():
            self.expiration_selected_date = self.calendar.get_date()  
            self.expiration_date_picker.configure(text=self.expiration_selected_date,font=("Montserrat", 12))  
            top.destroy()  

        select_button = ctk.CTkButton(
        top,
        text="Select",
        command=select_date,
        width=75,
        height=25,
        corner_radius=5,
        fg_color="#6C9FFF",
        text_color="white",
        hover_color="#5E95FF",
        border_color="#6C9FFF",
        border_width=1,
        font=("Montserrat Bold", 10,"bold"),
        )
        select_button.place(x=125, y=170)

    def submit_listing(self):
        # Extract data from entries

        self.category= self.category_entry.get()
        self.quantity=self.quantity_entry.get()
        self.expiration_date=self.expiration_selected_date
        self.location=self.location_entry.get().strip()
        self.pincode= self.pincode_entry.get().strip()
  
 
        #Category validation
        if self.category not in self.category_list:
            self.category_entry.configure(text_color="red")
            self.error_label.configure(text=f"*Error: Please select Category!.",text_color="red")
            return
        else:
            self.category_entry.configure(text_color="black")
            self.error_label.configure(text_color="white")

        #Quantity validation
        if self.quantity not in self.quantity_list:
            self.quantity_entry.configure(text_color="red")
            self.error_label.configure(text=f"*Error: Please select Quantity!.",text_color="red")
            return
        else:
            self.quantity_entry.configure(text_color="black")
            self.error_label.configure(text_color="white")
        
        #expiration Date
        if self.expiration_date =="Select Expiration":
            self.expiration_date_picker.configure(font=("Montserrat", 11),text_color="red",border_color="red")
            self.error_label.configure(text=f"*Error: Please select Expiration date!.",text_color="red")
            return
        else:
            self.expiration_date_picker.configure(font=("Montserrat", 11),text_color="Black",border_color="#D2D2D2")
            self.error_label.configure(text_color="white")

        #location validation
        location=self.location.split()
        if len(location)<3  or self.location=="":
            self.location_entry.configure(font=("Montserrat", 11),text_color="red",border_color="red")
            self.error_label.configure(text=f"*Error: Location should be min 3 words",text_color="red")
            return
        else:
            self.location_entry.configure(font=("Montserrat", 11),text_color="Black",border_color="#D2D2D2")
            self.error_label.configure(text=f"*Error: .",text_color="white")


        #Zipcode validation
        zipcode_validation=validation(zipcode=self.pincode)
        if  zipcode_validation is not None:
            self.pincode_entry.configure(font=("Montserrat", 11),text_color="red",border_color="red")
            self.error_label.configure(text=f"*Error: {zipcode_validation}.",text_color="red")
            return
        else:
            self.pincode_entry.configure(font=("Montserrat", 11),text_color="Black",border_color="#D2D2D2")
            self.error_label.configure(text_color="white")



        self.load_data()
        self.error_label.configure(text=f"Sucessfully added!",text_color="green")
        
    def load_data(self):
        query = """
        INSERT INTO food_listings (food_type, quantity, expiration_date, location, pincode, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (self.category,  
                self.quantity,  
                self.expiration_date,  
                self.location,  
                self.pincode,  
                self.user_id)  

        try:
            execute_queries(query,values)
        except:
            print("Ops Issue occured to load data")
        else:
            print("Sucessfully! Loaded the data")
            self.donation_window=ctk.CTkToplevel(self.scrollable_frame, width=600, height=100, fg_color= 'white'

            )
            self.donation_window.title("Add Listing")
            self.donation_window.geometry("300X100")
            center_window(self.donation_window, 300, 100)

            completion_label = ctk.CTkLabel(
                self.donation_window,
                text="Sucessfully updated!",
                font=("Montserrat Bold", 14,"bold"),
                text_color="#848484",
            )
            completion_label.place(x=80, y=15)
            
            
            
            lets_go_button = ctk.CTkButton(
            self.donation_window,
            text="Let’s do it!",
            width=70,
            height=30,
            corner_radius=5,
            fg_color="#6C9FFF",
            text_color="white",
            hover_color="#7FE186",
            border_color="#6C9FFF",
            border_width=1,
            command=self.destroy_window,
            font=("Montserrat Bold", 11,"bold"),
            )
            lets_go_button.place(x=115, y=60)

    def destroy_window(self):
        self.donation_window.destroy()
        self.clear_of_entries()


    

    def clear_of_entries(self):
        self.category_entry.set("Select Category")  # Reset dropdown (if using OptionMenu)
        self.quantity_entry.set("Select Quantity")  # Reset the dropdown to its default state # Clear text in Entry widget
        self.expiration_date_picker.configure(text="Select Expiration")  # Reset date picker
        self.pincode_entry.delete(0, "end")  # Clear text in Entry widget
        self.error_label.configure(text="")  # Clear any error messages
        self.location_entry.delete(0, "end")


  

    def load_my_listings(self):
        self.error_label.configure(text=f"Sucessfully added!",text_color="white")
        self.donate_btn.configure(fg_color="#FFFFFF",state="enable")
        self.my_listings_btn.configure(fg_color="#F2F2F2",state="disabled")
        self.requests_btn.configure(fg_color="#FFFFFF",state="enable")


        self.listings_scrollable_frame = ctk.CTkScrollableFrame(
            self,
            width=733,
            height=370,
            fg_color="white",
            border_color="#D2D2D2",
            border_width=1,
        )
        self.listings_scrollable_frame.place(x=169, y=113)

        # Clear the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Fetch listings
        listings = fetch_listings_query(self.user_id)
        

        if not listings:
            # No listings found
            no_listings_label = ctk.CTkLabel(
                self.listings_scrollable_frame,
                text="No Listings Found!",
                font=("Montserrat Bold", 16, "bold"),
                text_color="#B3B3B3",
            )
            no_listings_label.grid(row=0, column=0, columnspan=4, pady=15, sticky="ew")
            return

        # Display listings
        
        for idx, listing in enumerate(listings):
            listing_id, food_type, quantity, expiration_date, location, pincode = listing

            # Display each listing as a row
            ctk.CTkLabel(
                self.listings_scrollable_frame,
                text=f"Food Type: {food_type}",
                font=("Montserrat", 14),
                text_color="black",
            ).grid(row=idx * 2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

            ctk.CTkLabel(
                self.listings_scrollable_frame,
                text=f"Category: {pincode}, Quantity: {quantity}, Expiry: {expiration_date}",
                font=("Montserrat", 12),
                text_color="#848484",
            ).grid(row=idx * 2 + 1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

            delete_button = ctk.CTkButton(
                self.listings_scrollable_frame,
                text="Delete",
                command=lambda l=listing: self.delete_listing(listing_id),
                font=("Montserrat Bold", 12),
                fg_color="#C51518",
                hover_color="#A41417", 
                width=80,
                height=30,
                corner_radius=5,
            )
            delete_button.grid(row=idx * 2, column=3, padx=10, pady=5, sticky="e")

            edit_button = ctk.CTkButton(
                self.listings_scrollable_frame,
                text="Edit",
                command=lambda: self.edit_listing(listing_id, food_type, quantity, expiration_date, location, pincode),
                font=("Montserrat Bold", 12),
                fg_color="#2E8A34",
                hover_color="#36A63D",
                width=80,
                height=30,
                corner_radius=5,
            )
            edit_button.grid(row=idx * 2, column=4, padx=10, pady=5, sticky="e")
    
    def delete_listing(self, listing_id):

        query = "DELETE FROM food_listings WHERE listing_id = %s"
        value = (listing_id,)
        
        try:
            # Call execute_queries function
            execute_queries(query, value)
            print(f"Listing with ID {listing_id} has been deleted.")
            self.load_my_listings()
        except Exception as e:
            print(f"Error deleting listing: {e}")


    def edit_listing(self, listing_id, food_type, quantity, expiration_date, location, pincode):
        self.donate_ui()

        self.category_entry.set(food_type)  
        self.quantity_entry.set(quantity)  
        self.expiration_selected_date = expiration_date
        self.expiration_date_picker.configure(text=expiration_date)  
        self.location_entry.delete(0, "end")
        self.location_entry.insert(0, location)  
        self.pincode_entry.delete(0, "end")
        self.pincode_entry.insert(0, pincode) 

        update_button = ctk.CTkButton(
            self.scrollable_frame,
            text="Update Listing",
            command=lambda: self.update_listing(listing_id),
            font=("Montserrat Bold", 16, "bold"),
            fg_color="#2E8A34",
            text_color="white",
            hover_color="#36A63D",
            width=150,
            height=39,
            corner_radius=10,
        )
        update_button.grid(row=6, column=1, pady=15, padx=10, sticky="") 


    def update_listing(self, listing_id):
        # Extract updated data from entries
        food_type = self.category_entry.get()
        quantity = self.quantity_entry.get()
        expiration_date = self.expiration_selected_date
        location = self.location_entry.get().strip()
        pincode = self.pincode_entry.get().strip()
        query = """
        UPDATE food_listings
        SET food_type = %s, quantity = %s, expiration_date = %s, location = %s, pincode = %s
        WHERE listing_id = %s
        """
        values = (food_type, quantity, expiration_date, location, pincode, listing_id)

        try:
            execute_queries(query, values)
            print(f"Listing with ID {listing_id} has been updated.")
            self.error_label.configure(text="Listing updated successfully!", text_color="green")
            self.clear_of_entries()
            self.load_my_listings()  
        except Exception as e:
            print(f"Error updating listing: {e}")
            self.error_label.configure(text=f"Error: {e}", text_color="red")

    def pickup_requests(self):

        self.requests_btn.configure(fg_color="#F2F2F2",state="disabled")
        self.my_listings_btn.configure(fg_color="#FFFFFF",state="enable")
        self.donate_btn.configure(fg_color="#FFFFFF",state="enable")


        self.scrollable_frame.destroy()  
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            width=733,
            height=370,
            fg_color="white",
            border_color="#D2D2D2",
            border_width=1,
        )
        self.scrollable_frame.place(x=169, y=113)

        query = """
        SELECT 
            p.pickup_id,
            fl.food_type,
            fl.quantity,
            p.pickup_time,
            u.first_name,
            u.last_name,
            p.status,
            p.date_scheduled
        FROM 
            pickups p
        JOIN 
            food_listings fl ON p.listing_id = fl.listing_id
        JOIN 
            users u ON p.user_id = u.user_id
        WHERE 
            fl.user_id = %s
        ORDER BY 
            p.date_scheduled DESC;
        """
        values = (self.user_id,)  
        requests = search_execute_query(query, values)

        if not requests:
            ctk.CTkLabel(
                self.scrollable_frame,
                text="No Pickup Requests Found!",
                font=("Montserrat Bold", 16),
                text_color="#B3B3B3",
            ).grid(row=0, column=0, pady=10)
            return

        # Display requests
   # Display requests
        for idx, request in enumerate(requests):
            pickup_id, food_type, quantity, pickup_time, first_name, last_name, status, _ = request

            # Request details
            ctk.CTkLabel(
                self.scrollable_frame,
                text=f"Food: {food_type}, Quantity: {quantity}, Pickup Time: {pickup_time}",
                font=("Montserrat", 12),
                text_color="black",
            ).grid(row=idx * 2, column=0, columnspan=4, padx=10, pady=5, sticky="w")

            ctk.CTkLabel(
                self.scrollable_frame,
                text=f"Requested by: {first_name} {last_name}",
                font=("Montserrat", 12),
                text_color="#848484",
            ).grid(row=idx * 2 + 1, column=0, columnspan=4, padx=10, pady=5, sticky="w")

            # Status display
            status_button = ctk.CTkButton(
                self.scrollable_frame,
                text=status.capitalize(),
                font=("Montserrat Bold", 12),
                fg_color={
                    "pending": "#E7A603",
                    "approved": "#2E8A34",
                    "rejected": "#C51518",
                }.get(status, "gray"),
                text_color="white",
                width=100,
                height=30,
                corner_radius=5,
                text_color_disabled="white",
                state="disabled",  # Disabled as it's for display only
            )
            status_button.grid(row=idx * 2 + 1, column=4, columnspan=2, padx=5, pady=5)

            if status == "pending":  # Show buttons only for pending requests
                # Approve button
                approve_button = ctk.CTkButton(
                    self.scrollable_frame,
                    text="Approve",
                    font=("Montserrat Bold", 12),
                    fg_color="#2E8A34",
                    hover_color="#36A63D",
                    text_color="white",
                    text_color_disabled="white",
                    width=100,
                    height=30,
                    corner_radius=5,
                    command=lambda pid=pickup_id: self.update_pickup_status(pid, "approved"),
                )
                approve_button.grid(row=idx * 2, column=4, padx=5, pady=5)

                # Reject button
                reject_button = ctk.CTkButton(
                    self.scrollable_frame,
                    text="Reject",
                    font=("Montserrat Bold", 12),
                    fg_color="#C51518",
                    hover_color="#A41417",
                    text_color="white",
                    text_color_disabled="white",
                    width=100,
                    height=30,
                    corner_radius=5,
                    command=lambda pid=pickup_id: self.update_pickup_status(pid, "rejected"),
                )
                reject_button.grid(row=idx * 2, column=5, padx=5, pady=5)
    def update_pickup_status(self, pickup_id, new_status):
        """Update the status of a pickup request."""
        query = """
        UPDATE pickups
        SET status = %s
        WHERE pickup_id = %s
        """
        values = (new_status, pickup_id)

        try:
            execute_queries(query, values)
            print(f"Pickup request {pickup_id} updated to {new_status}.")
            self.pickup_requests()  #
        except Exception as e:
            print(f"Error updating pickup status: {e}")

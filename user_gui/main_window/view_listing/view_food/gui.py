from pathlib import Path
from tkinter import Frame, StringVar
import customtkinter as ctk
from tkcalendar import DateEntry,Calendar
from utils import center_window,validation,get_user_info_id,update_users_table,send_email,connect_to_database
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


class FindFood(Frame):
    def __init__(self, parent, user_id, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.user_id = user_id  
        self.selected_zip_code = StringVar()
        self.selected_date = StringVar()

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
        heading_label = ctk.CTkLabel(
            self,
            text="Search & Pick Up",
            font=("Montserrat Bold", 36,"bold"),
            text_color="#B3B3B3",
        )
        heading_label.place(x=25 , y=39)

        #search button
        self.search_btn = ctk.CTkButton(
            self.side_frame,
            text="Search & Pick Up",
            width=169,
            height=50,
            corner_radius=0,
            fg_color="#F2F2F2",
            text_color="#B3B3B3",
            border_color="#D2D2D2",
            border_width=1,
            font=("Montserrat Bold", 16,"bold"),
            command=self.search_ui,
            state="disabled",
        )
        self.search_btn.place(x=0, y=0)


        #requests button
        self.my_requests_btn = ctk.CTkButton(
            self.side_frame,
            text="My Requests",
            width=169,
            height=50,
            corner_radius=0,
            fg_color="#FFFFFF",
            text_color="#B3B3B3",
            border_color="#D2D2D2",
            hover_color="#F2F2F2",
            border_width=1,
            font=("Montserrat Bold", 16,"bold"),
            command=self.myrequests,
        )
        self.my_requests_btn.place(x=0, y=50)
        self.search_ui()

        self.error_label=ctk.CTkLabel(
            self.search_frame,
            text="*Error",
            font=("Montserrat Bold", 14,),
            text_color="white",
        )
        self.error_label.place(x=275, y=170)
        

    def widget_caller(self,label_widget):
    
        self.label_text = label_widget.cget("text")
        self.open_calendar()


    def search_ui(self):
   

        self.my_requests_btn.configure(fg_color="#FFFFFF",state="enable")
        self.search_btn.configure(fg_color="#F2F2F2",state="disabled")

        self.search_frame=  ctk.CTkFrame(
            self,
            width=733,
            height=506,
            fg_color="white",
            border_color="#D2D2D2",
            border_width=1,
        )
        self.search_frame.place(x=169, y=113)
        
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            width=711,
            height=197,
            fg_color="white",
            border_color="#D2D2D2",
            border_width=1,
        )
        self.scrollable_frame.place(x=169, y=306)

        # Title Label
        title_label = ctk.CTkLabel(
            self.search_frame,
            text="Search listing",
            font=("Montserrat Bold", 24, "bold"),
            text_color="#848484",
        )
        title_label.place(x=235,y=5)

        category_label = ctk.CTkLabel(
            self.search_frame,
            text="Select ZIPCode:*",
            font=("Montserrat Bold", 16, "bold"),
            text_color="#B3B3B3",
        )
        category_label.place(x=180, y=58)

      
        self.zipcode_entry =  ctk.CTkOptionMenu(
            self.search_frame,
            #values=self.zipcode_entry,
            width=110,
            height=18,
            variable=self.selected_zip_code,
            fg_color="white",
            font=("Montserrat", 12),
            corner_radius=5,
            text_color="black",
            button_color="#6C9FFF"
        )
        self.zipcode_entry.set("Select ZIPCode")
        self.zipcode_entry.place(x=360,y=63)
        self.populate_zip_code_dropdown()

        # Expiration Date
        expiration_date_label = ctk.CTkLabel(
            self.search_frame,
            text="Expiration Date:",
            font=("Montserrat Bold", 16, "bold"),
            text_color="#B3B3B3",
        )
        expiration_date_label.place(x=180,y=93)


        self.selected_date="Select Expiration"
        self.expiration_date_picker = ctk.CTkButton(
            self.search_frame,
            text=self.selected_date,
            width=110,
            height=18,
            fg_color="white",
            text_color="black",
            hover_color="#D2D2D2",
            border_color="#B3B3B3",
            border_width=1,
            corner_radius=5,
            command=lambda:self.widget_caller(self.expiration_date_picker),
            font=("Montserrat Bold", 12,),
        )
        self.expiration_date_picker.place(x=360,y=100)

        # Submit Button
        search_button = ctk.CTkButton(
            self.search_frame,
            text="Search",
           command=self.searchfunc,
            font=("Montserrat Bold", 16, "bold"),
            fg_color="#5E95FF",
            text_color="white",
            hover_color="#417BFF",
            width=110,
            height=27,
            corner_radius=10,
        )
        search_button.place(x=290,y=140)

    def populate_zip_code_dropdown(self):
  
   
        query="""SELECT DISTINCT pincode FROM food_listings where user_id != %s AND expiration_date >= CURDATE()"""
        value=(self.user_id,)
        result=search_execute_query(query,value)
        zip_code_list = [str(row[0]) for row in result]
        self.zipcode_entry.configure(values=zip_code_list)
       

  

    def open_calendar(self):
        # Create a Toplevel winqdow
        top = Toplevel(self.search_frame)
        top.title("Select Date")
        top.geometry("300x200")  
        top.resizable(False, False)
        center_window(top,300,200)

        # Define the maximum selectable date
        max_date = date.today() - relativedelta(years=18)  

        min_date = date.today() - relativedelta(years=18) 

        # Create a custom ttk style for the calendar
        style = ttk.Style(top)
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
            if self.label_text=="Pick Up date":
                 self.selected_date = self.calendar.get_date()  
                 self.pickup_date_picker.configure(text=self.selected_date,font=("Montserrat", 12))  
            else:
                self.selected_date = self.calendar.get_date()  
                self.expiration_date_picker.configure(text=self.selected_date,font=("Montserrat", 12))  
                
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



    def searchfunc(self):
        self.zipcode=self.zipcode_entry.get()
        self.expiration_date=self.selected_date



        #zipcode validation
        if self.zipcode=="Select ZIPCode":
            self.zipcode_entry.configure(text_color="red")
            self.error_label.configure(text=f"*Error: Please select zipcode!.",text_color="red")
        else:
            self.zipcode_entry.configure(text_color="black")
            self.error_label.configure(text=f"*Error: Please select zipcode!.",text_color="white")
        
        if self.expiration_date=="Select Expiration*":
            self.expiration_date_picker.configure(text_color="red")
            self.error_label.configure(text=f"*Error: Please select Expiration!.",text_color="red")
        
        self.load_my_listings(self.zipcode,self.expiration_date,self.user_id)


    def load_my_listings(self, zipcode, expiration, user_id):
        # Clear the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Fetch listings
        listings = search_listings_query(zipcode, expiration, user_id)
        
        if len(listings)>0:
            self.error_label.configure(text=f"{len(listings)} Found!", text_color="green")
        else: 
            self.error_label.configure(text=f"Ops! 0 Found! Try another location.", text_color="red")

            
        if not listings:
            # No listings found
            no_listings_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="No Listings Found!",
                font=("Montserrat Bold", 16, "bold"),
                text_color="#B3B3B3",
            )
            no_listings_label.grid(row=0, column=0, columnspan=4, pady=15, sticky="ew")
            return

        # Center-align the grid columns
        self.scrollable_frame.grid_columnconfigure(0, weight=1)  
        self.scrollable_frame.grid_columnconfigure(1, weight=0)  
        self.scrollable_frame.grid_columnconfigure(2, weight=1)  

        # Display listings
        for idx, listing in enumerate(listings):
            listing_id,self.food_type, quantity, expiration_date, location, pincode, lister_user_id = listing

            listing_frame = ctk.CTkFrame(
                self.scrollable_frame,
                fg_color="white",
                border_color="#D2D2D2",
                border_width=1,
                corner_radius=10,
            )
            listing_frame.grid(row=idx, column=1, padx=10, pady=10, sticky="ew")

            listing_frame.grid_columnconfigure(0, weight=3)  # Labels
            listing_frame.grid_columnconfigure(1, weight=1)  # Buttons

            # Food Type Label
            ctk.CTkLabel(
                listing_frame,
                text=f"Food Type: {self.food_type}",
                font=("Montserrat", 14),
                text_color="black",
            ).grid(row=0, column=0, padx=10, pady=5, sticky="w")

            # Location Label
            ctk.CTkLabel(
                listing_frame,
                text=f"Location: {location}, {pincode}",
                font=("Montserrat", 12),
                text_color="#848484",
            ).grid(row=1, column=0, padx=10, pady=5, sticky="w")

            # Quantity and Expiry Label
            ctk.CTkLabel(
                listing_frame,
                text=f"Location:{pincode}, Quantity: {quantity}, Expiry: {expiration_date or 'N/A'}",
                font=("Montserrat", 12),
                text_color="#848484",
            ).grid(row=2, column=0, padx=10, pady=5, sticky="w")

            # Create a horizontal frame for buttons
            button_frame = ctk.CTkFrame(
                listing_frame,
                fg_color="white",
            )
            button_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="e")

            # Request for Pick Up Button
            request_button = ctk.CTkButton(
                button_frame,
                text="Request for Pick Up",
                font=("Montserrat Bold", 12),
                fg_color="green",
                hover_color="#7FE186",
                width=120,
                height=30,
                corner_radius=5,
                command=lambda l=listing_id: self.request_pickup( l),
            )
            request_button.pack(side="left", padx=5)

    
    
    def request_pickup(self,listing_id):
        self.listing_id=listing_id
       

        query ="""select * from food_listings where listing_id = %s"""
        values=(self.listing_id,)
        result=search_execute_query(query,values)
        for idx, item in enumerate(result, start=1):  # 'start=1' makes enumeration start at 1
            self.listing_id, self.food_type, self.quantity, self.expiration_date, self.location, self.pincode, self.lister_user_id, date_added = item
 
        # Create a Toplevel winqdow
        self.top = Toplevel(self.search_frame,bg="white")
        self.top.title("PickUp Request")
        self.top.geometry("400x300")  
        self.top.resizable(False, False)
        center_window(self.top,400,300)

        pickup_label = ctk.CTkLabel(
            self.top,
            text="Schedule Pick-Up",
            font=("Montserrat Bold", 24,"bold"),
            text_color="#848484",
        )
        pickup_label.place(x=100,y=10)

        food_type_label=ctk.CTkLabel(
            self.top,
            text="Food Type:",
            font=("Montserrat Bold", 16,"bold"),
            text_color="#CACACA",
        )
        food_type_label.place(x=100,y=58)


        food_type_label_data=ctk.CTkLabel(
            self.top,
           text=f"{self.food_type}",
            font=("Montserrat Bold", 16),
            text_color="#848484",
        )
        food_type_label_data.place(x=200,y=58)


                # Time Picker Dropdowns
        pickup_date_label = ctk.CTkLabel(
            self.top,
            text="Pickup date",
            font=("Montserrat Bold", 16),
            text_color="#CACACA",
        )
        pickup_date_label.place(x=100,y=100)



        self.selected_date= "Pick Up date"
        self.pickup_date_picker = ctk.CTkButton(
            self.top,
            text=self.selected_date,
            width=110,
            height=18,
            fg_color="white",
            text_color="#848484",
            hover_color="#D2D2D2",
            border_color="#B3B3B3",
            border_width=1,
            corner_radius=5,
            command=lambda : self.widget_caller(self.pickup_date_picker),
            font=("Montserrat Bold", 12,),
        )
        self.pickup_date_picker.place(x=200,y=100)
        self.pickup_date_picker.configure(text=self.selected_date,font=("Montserrat", 12)) 
       

          # Time Picker Dropdowns
        time_label = ctk.CTkLabel(
            self.top,
            text="Pickup Time (HH:MM)",
            font=("Montserrat Bold", 14),
            text_color="#CACACA",
        )
        time_label.place(x=40,y=130)

        self.hour_var = ctk.StringVar(value="HH")
        self.hour_entry =  ctk.CTkOptionMenu(
            self.top,
            variable=self.hour_var,
            values=[f"{i:02}" for i in range(24)],
            width=40,
            height=18,
            fg_color="white",
            font=("Montserrat", 12),
            corner_radius=5,
            text_color="black",
            button_color="#6C9FFF"
        )
        self.hour_entry.place(x=200,y=140)

        self.minute_var = ctk.StringVar(value="MM")
        self.minute_entry =  ctk.CTkOptionMenu(
            self.top,
            variable=self.minute_var,
            values=[f"{i:02}" for i in range(24)],
            width=40,
            height=18,
            fg_color="white",
            font=("Montserrat", 12),
            corner_radius=5,
            text_color="black",
            button_color="#6C9FFF"
        )
        self.minute_entry.place(x=250,y=140)

    
        # Schedule Button
        schedule_button = ctk.CTkButton(
            self.top,
            text="Schedule",
            font=("Montserrat Bold", 14),
            fg_color="green",
            hover_color="#7FE186",

            corner_radius=10,
            command=self.schedule_pickup,
        )
        schedule_button.place(x=130,y=180)

        # viewmore Button
        view_button = ctk.CTkButton(
            self.top,
            text="Maybe later",
            font=("Montserrat Bold", 14),
            fg_color="#5E95FF",
            corner_radius=10,
            command=self.top.destroy,
        )
        view_button.place(x=130,y=220)

        self.error1_label =  ctk.CTkLabel(
            self.top,
            text="error",
            font=("Montserrat Bold", 12),
            text_color="white",
        )
        self.error1_label.place(x=100,y=260)




    def schedule_pickup(self):
        self.pickup_date=self.selected_date
        self.hour_time=self.hour_entry.get()
        self.minute_time=self.minute_entry.get()
        self.listing_id
        self.user_id

        if self.selected_date=="Pick Up date" or self.pickup_date=="":
            self.pickup_date_picker.configure(text_color="red")
            self.error1_label.configure(text=f"*Error! Pickup date is required",text_color="red")
            return
        else:

            self.pickup_date_picker.configure(text_color="black")
            self.error1_label.configure(text=f"*Error: Please select zipcode!.",text_color="white")
        
        #Hour Validation
        if self.hour_time =="HH" or self.minute_entry=="MM":
            self.minute_entry.configure(text_color="red")
            self.hour_entry.configure(text_color="red")
            self.error1_label.configure(text=f"*Error: Please select Pickup Time!.",text_color="red")
            return
        else:

            self.minute_entry.configure(text_color="black")
            self.hour_entry.configure(text_color="black")
            self.error1_label.configure(text=f"*Error: Please select Pickup Time!.",text_color="white")  


        pickuptime = datetime.strptime(self.pickup_date, "%Y-%m-%d")
        desired_date_time=f"{self.pickup_date} {self.hour_time} {self.minute_time}"
        datetime_obj = datetime.strptime(desired_date_time, "%Y-%m-%d %H %M")
        self.formatted_date_time = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")    

   
        if pickuptime.date()>self.expiration_date :
            self.pickup_date_picker.configure(text_color="red")
            self.error1_label.configure(text=f"*Error! Pick up date should be earlier than Exp date",text_color="red")
            return
        else:
            self.pickup_date_picker.configure(text_color="black")
            self.error1_label.configure(text=f"*Error: Please select zipcode!.",text_color="white")
        

        


        self.load_pickup_date() 



    def load_pickup_date(self):
        query = """
    INSERT INTO pickups (user_id, listing_id, pickup_time)
    VALUES (%s, %s, %s)
    """
        values=(self.user_id,self.listing_id,self.formatted_date_time,)

        try:   
               execute_queries(query,values)
        except:
            print("Pickup insert failed!")
        else:
            self.error_label.configure(text="Sucessfully requested for PickUp!",text_color="green")
            self.top.destroy()
        



    def load_pickup_data(self, user_id, listing_id):

        # Create a Toplevel winqdow
        top = Toplevel(self.search_frame)
        top.title("Request for PickUp")
        top.geometry("500x500")  
        center_window(top,500,500)

        
        pickup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "pending"  # Default status

        query = """
        INSERT INTO pickups (user_id, listing_id, pickup_time, status)
        VALUES (%s, %s, %s, %s);
        """
        values = (user_id, listing_id, pickup_time, status)

        try:
            execute_queries(query, values)
            print(f"Pick-up request for Listing ID {listing_id} has been submitted.")
            self.display_success_message("Pick-up request submitted successfully!")
        except Exception as e:
            print(f"Error while requesting pick-up: {e}")
            self.display_error_message("An error occurred while submitting the pick-up request.")

    def display_success_message(self, message):
        """Show a success message to the user."""
        success_label = ctk.CTkLabel(
            self.scrollable_frame,
            text=message,
            font=("Montserrat Bold", 14),
            text_color="green",
        )
        success_label.grid(row=0, column=0, columnspan=4, pady=10)

    def display_error_message(self, message):
        """Show an error message to the user."""
        error_label = ctk.CTkLabel(
            self.scrollable_frame,
            text=message,
            font=("Montserrat Bold", 14),
            text_color="white",
        )
        error_label.grid(row=0, column=0, columnspan=4, pady=10)

    
    # My Requests
    def myrequests(self):
        self.scrollable_frame .place_forget()
        self.search_frame.place_forget()

        self.requests_scrollable_frame = ctk.CTkScrollableFrame(
            self,
            width=711,
            height=400,
            fg_color="white",
            border_color="#D2D2D2",
            border_width=1,
        )
        self.requests_scrollable_frame.place(x=168, y=112)
        self.show_my_requests()

    def show_my_requests(self):
        self.my_requests_btn.configure(fg_color="#F2F2F2",state="disabled")
        self.search_btn.configure(fg_color="#FFFFFF",state="enable")
        query = """
        SELECT 
            p.pickup_id,
            fl.food_type,
            fl.quantity,
            fl.expiration_date,
            fl.location,
            fl.pincode,
            p.pickup_time,
            p.status
        FROM 
            pickups p
        JOIN 
            food_listings fl ON p.listing_id = fl.listing_id
        WHERE 
            p.user_id = %s
        ORDER BY 
            p.date_scheduled DESC;
         """
        values=(self.user_id,)
      

        requests = search_execute_query(query,values)

        for widget in self.requests_scrollable_frame.winfo_children():
            widget.destroy()

        if not requests:
            no_requests_label = ctk.CTkLabel(
                self.requests_scrollable_frame,
                text="No Requests Found!",
                font=("Montserrat Bold", 16),
                text_color="#B3B3B3",
            )
            no_requests_label.pack(pady=15)
            return

        for idx, request in enumerate(requests):
            pickup_id = request[0]
            food_type = request[1]
            quantity = request[2]
            expiration_date = request[3]
            location = request[4]
            pincode = request[5]

            # Try parsing pickup_time with fallback formats
            try:
                pickup_time = datetime.strptime(request[6], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                pickup_time = datetime.strptime(request[6], "%Y-%m-%d %H:%M")

            status = request[7]

            # Determine if the request is expired
            now = datetime.now()
            is_expired = pickup_time < now

            # Status display
            if is_expired:
                status_text = "Expired"
                status_color = "gray"
            else:
                status_text = status.capitalize()
                status_color = {
                    "pending": "orange",
                    "approved": "green",
                    "rejected": "red",
                }.get(status, "gray")  # Default to gray if status is unknown

            ctk.CTkLabel(
                self.requests_scrollable_frame,
                text=f"Food: {food_type}, Quantity: {quantity}, Pickup Time: {pickup_time.strftime('%Y-%m-%d %H:%M:%S')}",
                font=("Montserrat", 12),
                text_color="#000",
            ).grid(row=idx * 2, column=0, columnspan=3, pady=5, padx=10, sticky="w")

            ctk.CTkLabel(
                self.requests_scrollable_frame,
                text=f"Location: {location}, {pincode}",
                font=("Montserrat", 12),
                text_color="#848484",
            ).grid(row=idx * 2 + 1, column=0, columnspan=3, pady=5, padx=10, sticky="w")

            # Status button
            status_button = ctk.CTkButton(
                self.requests_scrollable_frame,
                text=status_text,
                font=("Montserrat Bold", 12),
                fg_color=status_color,
                hover_color="#D3D3D3",
                text_color_disabled="white",
                width=100,
                height=30,
                corner_radius=5,
                state="disabled",
            )
            status_button.grid(row=idx * 2, column=3, pady=5, padx=10, sticky="e")
                
    def get_status_button_properties(self, status):

        if status == "pending":
            return "#E7A603", "Pending"  
        elif status == "approved":
            return "#2E8A34", "Approved"  
        elif status == "rejected":
            return "#C51518", "Rejected"  
        return "#B3B3B3", "Unknown"  





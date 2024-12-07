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
        self.user_id = user_id  # Store user_id for user-specific operations
        self.data = {
            "food_type": StringVar(),
            "quantity": StringVar(),
            "location": StringVar(),
            "zipcode": StringVar(),
            "expiry_date": StringVar(),
        }

        self.configure(bg="white")



        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            width=733,
            height=370,
            fg_color="white",
            border_color="#D2D2D2",
            border_width=1,
        )
        self.scrollable_frame.place(x=169, y=113)

            # Sidebar in the settings page (if needed)
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
            #command=self.account_ui,
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
            #command=self.account_ui,
            width=169,
            height=50,
            corner_radius=0,
            fg_color="#FFFFFF",
            text_color="#B3B3B3",
            border_color="#D2D2D2",
            border_width=1,
            hover_color="#F2F2F2",
            font=("Montserrat Bold", 16,"bold"),
        )
        self.requests_btn.place(x=0, y=100)

        self.error_label=ctk.CTkLabel(
            self,
            text="*Error",
            font=("Montserrat Bold", 14,),
            text_color="white",
        )
        self.error_label.place(x=350, y=79)
    
        # Call the function to populate the UI
        self.donate_ui()

        # Update the scrollregion whenever widgets are added
        self.scrollable_frame.update_idletasks()

    def donate_ui(self):
        # Configure columns for the scrollable frame
        self.scrollable_frame.grid_columnconfigure(0, weight=1)  # Left spacer
        self.scrollable_frame.grid_columnconfigure(1, weight=0)  # Labels
        self.scrollable_frame.grid_columnconfigure(2, weight=1)  # Entries
        self.scrollable_frame.grid_columnconfigure(3, weight=1)  # Right spacer

        # Title Label
        title_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Create Food Listing",
            font=("Montserrat Bold", 20, "bold"),
            text_color="#848484",
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=15, sticky="ew")  # Span across all columns

        # Food Name (Label and Entry in the same row)
        food_name_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Food Name:*",
            font=("Montserrat Bold", 16, "bold"),
            text_color="#B3B3B3",
        )
        food_name_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.food_name_entry = ctk.CTkEntry(
            self.scrollable_frame,
            placeholder_text="Enter food name",
            font=("Montserrat Bold", 12),
            width=200,
            height=25,
            border_color="#B3B3B3",
            border_width=1,
            corner_radius=5,
        )
        self.food_name_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="w")

        # Similarly update other fields (e.g., Category, Quantity)
        # Example for Category:
        category_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Category:*",
            font=("Montserrat Bold", 16, "bold"),
            text_color="#B3B3B3",
        )
        category_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")


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
        self.category_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Quantity
        quantity_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Quantity:*",
            font=("Montserrat Bold", 16, "bold"),
            text_color="#B3B3B3",
        )
        quantity_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

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
        self.quantity_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Serving Size
        serving_size_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Serving Size:(Optional)",
            font=("Montserrat Bold", 16, "bold"),
            text_color="#B3B3B3",
        )
        serving_size_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.serving_var=ctk.StringVar(value="Select Serving") 
        self.serving_list = [str(i) for i in range(1, 10)] + ["10+ (Party is on!)"]  

        self.serving_size_entry = ctk.CTkOptionMenu(
            self.scrollable_frame,
            values=self.serving_list,
            variable=self.serving_var,
            width=110,
            height=18,
            fg_color="white",
            font=("Montserrat", 12),
            corner_radius=5,
            text_color="black",
            button_color="#6C9FFF"
        )
        self.serving_size_entry.grid(row=4, column=1,padx=10, pady=10, sticky="w")


        # Prepared Date
        
        prepared_date_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Prepared Date:(Optional)",
            font=("Montserrat Bold", 16, "bold"),
            text_color="#B3B3B3",
        )
        prepared_date_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.prepered_date_data="Prepared Date"
        self.prepared_date_picker = ctk.CTkButton(
            self.scrollable_frame,
            text=self.prepered_date_data,
            width=110,
            height=18,
            fg_color="white",
            text_color="black",
            hover_color="#D2D2D2",
            border_color="#B3B3B3",
            border_width=1,
            corner_radius=5,
            command=lambda: self.widget_callback(self.prepared_date_picker),
            font=("Montserrat Bold", 12),
        )
        self.prepared_date_picker.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Expiration Date
        expiration_date_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Expiration Date:*",
            font=("Montserrat Bold", 16, "bold"),
            text_color="#B3B3B3",
        )
        expiration_date_label.grid(row=6, column=0, padx=10, pady=10, sticky="e")


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
            command=lambda: self.widget_callback(self.expiration_date_picker),
            font=("Montserrat Bold", 12,),
        )
        self.expiration_date_picker.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        # Pincode
        pincode_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Zipcode:*",
            font=("Montserrat Bold", 16, "bold"),
            text_color="#B3B3B3",
        )
        pincode_label.grid(row=7, column=0, padx=10, pady=10, sticky="e")

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
        self.pincode_entry.grid(row=7, column=1, padx=10, pady=10,sticky="w")

        # Description
        description_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Description:*",
            font=("Montserrat Bold", 16, "bold"),
            text_color="#B3B3B3",
        )
        description_label.grid(row=8, column=0, padx=10, pady=10, sticky="e")

        self.description_entry = ctk.CTkTextbox(
            self.scrollable_frame,
            height=134,
            width=340,
            font=("Montserrat", 12),
            corner_radius=10,
            border_color="#B3B3B3",
            border_width=1,

        )
        self.description_entry.grid(row=8, column=1, padx=10, pady=10,sticky="w")

        # Special Notes
        special_notes_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Special Notes:(Optional)",
            font=("Montserrat Bold", 16, "bold"),
            text_color="#B3B3B3",
        )
        special_notes_label.grid(row=9, column=0, padx=10, pady=10, sticky="e")

        self.special_notes_entry = ctk.CTkTextbox(
            self.scrollable_frame,
            height=134,
            width=340,
            font=("Montserrat", 12),
            corner_radius=10,
            border_color="#B3B3B3",
            border_width=1,

        )
        self.special_notes_entry.grid(row=9, column=1, padx=10, pady=10,sticky="w")

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
        submit_button.grid(row=10, column=1, pady=15, padx=10, sticky="") 

        # Update the scrollable frame
        self.scrollable_frame.update_idletasks()

    def widget_callback(self, widget):
        print(f"Function called from: {widget}")
        print(f"Widget text: {widget.cget('text')}")  # Get text of the button
        self.call_from=widget.cget('text')
        self.open_calendar()

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
            if self.call_from==self.expiration_selected_date:
                self.expiration_selected_date = self.calendar.get_date()  
                self.expiration_date_picker.configure(text=self.expiration_selected_date,font=("Montserrat", 12))  
            elif self.call_from==self.prepered_date_data:
                self.prepered_date_data=self.calendar.get_date()
                self.prepared_date_picker.configure(text=self.prepered_date_data,font=("Montserrat", 12))

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
        select_button.place(x=130, y=165)

    def submit_listing(self):
        # Extract data from entries
        self.food_name=self.food_name_entry.get().strip()
        self.category= self.category_entry.get()
        self.quantity=self.quantity_entry.get()
        self.serving_size= self.serving_size_entry.get()
        self.expiration_date=self.expiration_selected_date,
        self.preperation_date= self.prepered_date_data,
        self.zipcode= self.pincode_entry.get().strip()
        self.description=self.description_entry.get("1.0", "end-1c").strip()
        self.special_notes= self.special_notes_entry.get("1.0", "end-1c").strip()

        #Food name validation
        food_name_validation=validation(name=self.food_name)
        if food_name_validation is not None:
            self.food_name_entry.configure(font=("Montserrat", 11),text_color="red",border_color="red")
            self.error_label.configure(text=f"*Error: {food_name_validation}.",text_color="red")
            return
        else:
            self.food_name_entry.configure(font=("Montserrat", 11),text_color="Black",border_color="#D2D2D2")
            self.error_label.configure(text_color="white")

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

        #Zipcode validation
        zipcode_validation=validation(zipcode=self.zipcode)
        if  zipcode_validation is not None:
            self.pincode_entry.configure(font=("Montserrat", 11),text_color="red",border_color="red")
            self.error_label.configure(text=f"*Error: {zipcode_validation}.",text_color="red")
            return
        else:
            self.pincode_entry.configure(font=("Montserrat", 11),text_color="Black",border_color="#D2D2D2")
            self.error_label.configure(text_color="white")

        #Description Validation
        description_validation=self.description.split()
        if len(description_validation)<5 or description_validation=='':
            self.description_entry.configure(font=("Montserrat", 11),text_color="red",border_color="red")
            self.error_label.configure(text=f"*Error: Description should be minumum of 6 words!.",text_color="red")
            return
        else:
            self.description_entry.configure(font=("Montserrat", 11),text_color="Black",border_color="#D2D2D2")
            self.error_label.configure(text_color="white")

        self.serving_size = None if self.serving_size == "Select Serving" else self.serving_size
        self.prepared_date = None if self.preperation_date == "Prepared Date" else self.preperation_date
        
        self.load_data()
        
    def load_data(self):
# Create the INSERT query
        query = """
        INSERT INTO food_listings 
            (user_id,food_name, category, quantity, serving_size, prepared_date,expiration_date, zipcode, description, special_notes) 
        VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        # Collect data
        values = (
            self.user_id,
            self.food_name, 
            self.category if self.category else None,  # Optional, will insert NULL if empty
            self.quantity if self.quantity else None,  # Optional, will insert NULL if empty
            self.serving_size,  # Optional, will insert NULL if empty
            self.prepared_date,
            self.expiration_date if self.expiration_date else None,  # Optional, will insert NULL if empty
            self.zipcode,  # Required
            self.description if self.description else None,  # Optional, will insert NULL if empty
            self.special_notes if self.special_notes else None,  # Optional, will insert NULL if empty
        )

        try:
            insert_food_listing(values)
        except:
            print("Ops Issue occured to load data")
        else:
            print("Sucessfully! Loaded the data")









        
        

        
        
     




    """ # Food Type Frame
        food_type_frame = ctk.CTkFrame(central_frame, fg_color="#FFFFFF", corner_radius=10)
        food_type_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        food_type_label = ctk.CTkLabel(
            food_type_frame,
            text="Food Type",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        food_type_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        food_type_dropdown = ctk.CTkOptionMenu(
            food_type_frame,
            variable=self.data["food_type"],
            values=["Fruits", "Dairy", "Vegetables", "Fast Food", "Soft Drinks", "Grains", "Snacks", "Other"],
            font=("Montserrat", 14),
            width=150,
        )
        food_type_dropdown.grid(row=1, column=0, padx=(10, 10), pady=(0, 10))
        food_type_dropdown.set("Fruits")

        # Quantity Frame
        quantity_frame = ctk.CTkFrame(central_frame, fg_color="#FFFFFF", corner_radius=10)
        quantity_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        quantity_label = ctk.CTkLabel(
            quantity_frame,
            text="Quantity",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        quantity_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        quantity_entry = ctk.CTkEntry(
            quantity_frame,
            textvariable=self.data["quantity"],
            width=150,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter quantity",
        )
        quantity_entry.grid(row=1, column=0, padx=(10, 10), pady=(0, 10))

        # Expiry Date Frame
        expiry_date_frame = ctk.CTkFrame(central_frame, fg_color="#FFFFFF", corner_radius=10)
        expiry_date_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        expiry_date_label = ctk.CTkLabel(
            expiry_date_frame,
            text="Expiry Date",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        expiry_date_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        expiry_date_picker = DateEntry(
            expiry_date_frame,
            textvariable=self.data["expiry_date"],
            date_pattern="yyyy-mm-dd",
            font=("Montserrat", 14),
            background="#5E95FF",
            foreground="white",
            borderwidth=2,
        )
        expiry_date_picker.grid(row=1, column=0, padx=(10, 10), pady=(0, 10))

        # Address Frame
        address_frame = ctk.CTkFrame(central_frame, fg_color="#FFFFFF", corner_radius=10)
        address_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        address_label = ctk.CTkLabel(
            address_frame,
            text="Address",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        address_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        address_entry = ctk.CTkEntry(
            address_frame,
            textvariable=self.data["location"],
            width=300,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter address",
        )
        address_entry.grid(row=1, column=0, padx=(10, 10), pady=(0, 10))

        # Zipcode Frame
        zipcode_frame = ctk.CTkFrame(central_frame, fg_color="#FFFFFF", corner_radius=10)
        zipcode_frame.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        zipcode_label = ctk.CTkLabel(
            zipcode_frame,
            text="Zipcode",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        zipcode_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        zipcode_entry = ctk.CTkEntry(
            zipcode_frame,
            textvariable=self.data["zipcode"],
            width=150,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter zipcode",
        )
        zipcode_entry.grid(row=1, column=0, padx=(10, 10), pady=(0, 10))

        # Add Button
        add_button = ctk.CTkButton(
            central_frame,
            text="Add",
            command=self.save,
            width=200,
            height=40,
            font=("Montserrat Bold", 14),
            corner_radius=10,
            fg_color="#5E95FF",
            hover_color="#417BFF",
        )
        add_button.grid(row=2, column=0, columnspan=3, pady=(20, 10))

    def save(self):
        for field, val in self.data.items():
            if val.get().strip() == "":
                messagebox.showerror("Error", f"Please fill in the {field.replace('_', ' ').capitalize()} field")
                return

        result = db_controller.add_food_item(
            food_type=self.data["food_type"].get().strip(),
            quantity=self.data["quantity"].get().strip(),
            location=self.data["location"].get().strip(),
            zipcode=self.data["zipcode"].get().strip(),
            expiry_date=self.data["expiry_date"].get().strip(),
            user_id=self.user_id,
        )

        if result:
            messagebox.showinfo("Success", "Food item added successfully!")
            for key in self.data:
                self.data[key].set("")  # Clear all fields after saving
        else:
            messagebox.showerror("Error", "Failed to add food item. Please try again!")
"""
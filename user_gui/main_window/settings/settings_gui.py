from tkcalendar import Calendar
from utils import center_window,validation,get_user_info_id,update_users_table
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
from tkinter import Frame
import customtkinter as ctk
from pathlib import Path
from tkinter import (
    Toplevel,
    Frame,
    Canvas,
    PhotoImage,
    StringVar,
    ttk,
    Frame,
    
)



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def start_gui():
    Settings_GUI()

class Settings_GUI(Frame):
    def __init__(self, parent, user_id,mainwindow, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)  # Attach to parent
        self.user_id = user_id
        self.parent=parent
        self.mainwindow=mainwindow
        self.user_details=self.update_data()
        self.configure(bg="white")  # Debug background for visibility
        print(self.user_details)


        # Sidebar in the settings page (if needed)
        self.side_frame = ctk.CTkFrame(
            self,
            width=168,
            height=506,
            fg_color="white",
            bg_color="white",
            border_color="#D2D2D2",
        )
        self.side_frame.place(x=0, y=0)

        # Sidebar title
        settings_label = ctk.CTkLabel(
            self.side_frame,
            text="Settings",
            font=("Montserrat Bold", 36,"bold"),
            text_color="#B3B3B3",
        )
        settings_label.place(x=10, y=30)

 

        #profile button
        self.profile_selected=PhotoImage(file=relative_to_assets("profile_button_selected.png"))
        self.profile_unselected = PhotoImage(file=relative_to_assets("profile_button_unselected.png"))
        self.profile_btn = ctk.CTkButton(
            self.side_frame,
            text="Profile",
            #command=self.loginFunc,
            width=168,
            height=50,
            corner_radius=0,
            fg_color="#FFFFFF",
            text_color="#B3B3B3",
            hover_color="#F2F2F2",
            font=("Montserrat Bold", 16,"bold"),
            command=self.profile_gui
        )
        self.profile_btn.place(x=0, y=112)

        # self.account_selected=PhotoImage(file=relative_to_assets("account_button_selected.png"))
        # self.account_unselected = PhotoImage(file=relative_to_assets("account_button_unselected.png"))
        self.account_btn = ctk.CTkButton(
            self.side_frame,
            text="Account",
            command=self.account_gui,
            width=168,
            height=50,
            corner_radius=0,
            fg_color="#FFFFFF",
            text_color="#B3B3B3",
            hover_color="#F2F2F2",
            font=("Montserrat Bold", 16,"bold"),
        )
        self.account_btn.place(x=0, y=162)
        self.profile_gui()

    def profile_gui(self):

        #Center frame
        self.center_frame= ctk.CTkFrame(
            self,
            width=768,
            height=394,
            fg_color="white",
            bg_color="white",
            border_color="#D2D2D2",
            border_width=1, 
            corner_radius=10,
        )
        self.center_frame.place(x=168, y=113)


        self.top_info_ui()
        self.personal_information_ui()
        self.address_information_ui()


    def top_info_ui(self):
        
        #First Profile information frame
        self.first_profile_frame = ctk.CTkFrame(
            self.center_frame,
            width=706,
            height=66,
            fg_color="white",
            bg_color="white",
            border_width=1, 
            border_color="#D2D2D2",
            corner_radius=10,
        )
        self.first_profile_frame.place(x=30, y=10)


        #profile
        # Create a canvas to design the round button
        self.profile = Canvas(self.first_profile_frame, width=35, height=35, bg="white", highlightthickness=0,)
        self.profile.place(x=20, y=18)
        self.user_firstname=self.user_details[1]

        # Create the round button
        self.round_button = self.profile.create_oval(0, 0, 35, 35, fill="#0078D7", outline="")
        self.profile.create_text(17.5, 17.5, text=f"{self.user_firstname[0]}", fill="white", font=("Arial", 12, "bold"))

        self.full_name_data=f"{self.user_details[1]} {self.user_details[2]}"
        #Required Data File
        name_label = ctk.CTkLabel(
            self.first_profile_frame,
            text=self.full_name_data,
            font=("Montserrat Bold", 16, "bold"),
            text_color="#5E95FF",
   
        )
        name_label.place(x=71, y=14)

        self.location_data=f"{self.user_details[9]}, {self.user_details[10]}, {self.user_details[11]}"
        #Required Data File
        location_label = ctk.CTkLabel(
            self.first_profile_frame,
            text=self.location_data,
            font=("Montserrat Bold", 11, "bold"),
            text_color="#B3B3B3",
        )
        location_label.place(x=70, y=37)

        since_label = ctk.CTkLabel(
            self.first_profile_frame,
            text="Since:",
            font=("Montserrat Bold", 11, "bold"),
            text_color="#B3B3B3",
   
        )
        since_label.place(x=474, y=1)

        formatted_date = self.user_details[15].strftime("%B %d, %Y")
        #Required Data File
        sincel_full_label = ctk.CTkLabel(
            self.first_profile_frame,
            text=formatted_date,
            font=("Montserrat Bold", 11, "bold"),
            text_color="#5E95FF",
   
        )
        sincel_full_label.place(x=516, y=1)

    def personal_information_ui(self):

        #Second Profile information frame
        self.second_profile_frame = ctk.CTkFrame(
            self.center_frame,
            width=706,
            height=157,
            fg_color="white",
            bg_color="white",
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=10,
        )
        self.second_profile_frame.place(x=30, y=83)


        personalinfo_full_label = ctk.CTkLabel(
            self.second_profile_frame,
            text="Personal Information",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#848484",
   
        )
        personalinfo_full_label.place(x=20, y=10)

        # Second frame
        self.error1_label = ctk.CTkLabel(
            self.second_profile_frame,
            text="*Error:",
            font=("Montserrat Bold", 12,),
            text_color="white",
   
        )
        self.error1_label.place(x=198, y=10)

        #Seconf edit button
        edit_second_button = ctk.CTkButton(
            self.second_profile_frame,
            text="Edit",
            #command=self.loginFunc,
            width=45,
            height=25,
            corner_radius=10,
            fg_color="#FFFFFF",
            text_color="#B3B3B3",
            hover_color="#F2F2F2",
            border_color="#D2D2D2",
            border_width=1,
            command=self.personal_information_edit_gui,
        
            font=("Montserrat Bold", 10,"bold"),
        )
        edit_second_button.place(x=651, y=18)

        #firstname_Label
        self.first_name_label = ctk.CTkLabel(
            self.second_profile_frame,
            text="First Name",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        self.first_name_label.place(x=20, y=38)

        self.first_name_data=self.user_details[1].title()
        self.first_name = ctk.CTkLabel(
            self.second_profile_frame,
            text=self.first_name_data,
            font=("Montserrat Bold", 14, "bold"),
            text_color="#B3B3B3",
   
        )
        self.first_name.place(x=20, y=61)

        #last_name_label
        self.last_name_label = ctk.CTkLabel(
            self.second_profile_frame,
            text="Last Name",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        self.last_name_label.place(x=198, y=38)

        self.last_name_data=self.user_details[2].title()
        #last_name_Data
        self.last_name = ctk.CTkLabel(
            self.second_profile_frame,
            text=self.last_name_data,
            font=("Montserrat Bold", 14, "bold"),
            text_color="#B3B3B3",
   
        )
        self.last_name.place(x=198, y=61)

        #gender_label
        self.gender_label = ctk.CTkLabel(
            self.second_profile_frame,
            text="Gender",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        self.gender_label.place(x=20, y=87)

        self.gender_data=self.user_details[4]
       #gender_Data
        self.gender = ctk.CTkLabel(
            self.second_profile_frame,
            text=self.gender_data,
            font=("Montserrat Bold", 14, "bold"),
            text_color="#B3B3B3",
   
        )
        self.gender.place(x=20, y=110)
        
        #age_label
        self.age_label = ctk.CTkLabel(
            self.second_profile_frame,
            text="Date of Birth",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        self.age_label.place(x=198, y=87)

        self.dob_data=self.user_details[5]
        #age_Data
        self.age = ctk.CTkLabel(
            self.second_profile_frame,
            text=self.dob_data,
            font=("Montserrat Bold", 14, "bold"),
            text_color="#B3B3B3",
        )
        self.age.place(x=198, y=110)

        #age_Data
        self.phone_label = ctk.CTkLabel(
            self.second_profile_frame,
            text="Phone Number",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#B3B3B3",
        )
        self.phone_label.place(x=340, y=87)  

       #phone_Data
        self.phone_number_data=self.user_details[6]
        self.phone = ctk.CTkLabel(
            self.second_profile_frame,
            text=self.phone_number_data,
            font=("Montserrat Bold", 14, "bold"),
            text_color="#B3B3B3",
   
        )
        self.phone.place(x=340, y=110)


    def personal_information_edit_gui(self):


        self.first_name_entry = ctk.CTkEntry(
            self.second_profile_frame,
            width=110,
            height=18,
            font=("Montserrat", 12),
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
            
        )
        self.first_name_entry.place(x=19, y=63)
        self.first_name_entry.insert(0,self.first_name_data)


        #last_name_entry
        self.last_name_entry = ctk.CTkEntry(
            self.second_profile_frame,
            width=110,
            height=18,
            font=("Montserrat", 12),
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
        )
        self.last_name_entry.place(x=191, y=63)
        self.last_name_entry.insert(0,self.last_name_data)

        # Define gender options
        gender_options = ["Male", "Female", "Other"]
        
        # Create the CTkOptionMenu
        self.gender_dropdown = ctk.CTkOptionMenu(
            master=self.second_profile_frame,
            values=gender_options,
            width=110,
            height=18,
            fg_color="white",
            font=("Montserrat", 12),
            corner_radius=5,
            text_color="black",
            button_color="#6C9FFF"
        )
        self.gender_dropdown.set(self.gender_data)  # Default value
        self.gender_dropdown.place(x=20, y=115)
       
        self.selected_date=(self.dob_data)  
        # Create the button to open the calendar
        self.calender_button = ctk.CTkButton(
            self.second_profile_frame,
            text=self.selected_date,
            width=110,
            height=18,
            fg_color="white",
            text_color="black",
            hover_color="#D2D2D2",
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            command=self.open_calendar,
            font=("Montserrat Bold", 10,),
        )
        self.calender_button.place(x=193, y=115)
        self.phone.place_forget()

        #Phone_number_entry
        self.phone_number_entry = ctk.CTkEntry(
            self.second_profile_frame,
            width=110,
            height=18,
            font=("Montserrat", 12),
            placeholder_text="9892897242*",
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
        )
        self.phone_number_entry.place(x=323, y=114)
        self.phone_number_entry.insert(0,self.phone_number_data)

        save_button = ctk.CTkButton(
            self.second_profile_frame,
            text="Save",
            #command=self.loginFunc,
            width=45,
            height=25,
            corner_radius=5,
            fg_color="#6C9FFF",
            text_color="white",
            hover_color="#5E95FF",
            border_color="#6C9FFF",
            border_width=1,
            command=self.personal_info_verification,
            font=("Montserrat Bold", 10,"bold"),
        )
        save_button.place(x=650, y=18)

    def address_information_ui(self):

       #third Profile information frame
        self.third_profile_frame = ctk.CTkFrame(
            self.center_frame,
            width=706,
            height=135,
            fg_color="white",
            bg_color="white",
            border_color="#D2D2D2",
            border_width=1, 
            corner_radius=10,
        )
        self.third_profile_frame.place(x=30, y=247)

        # Second frame
        self.error2_label = ctk.CTkLabel(
            self.third_profile_frame,
            text="*Error:",
            font=("Montserrat Bold", 12,),
            text_color="white",
   
        )
        self.error2_label.place(x=198, y=5)

        #address Label
        Address_full_label = ctk.CTkLabel(
            self.third_profile_frame,
            text="Address",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#848484",
   
        )
        Address_full_label.place(x=20, y=5)

        
        #Street #1 label
        self.street_one_label = ctk.CTkLabel(
            self.third_profile_frame,
            text="Address #1",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        self.street_one_label.place(x=20, y=33)

        self.address_1_data=self.user_details[7]
        #street #1 data
        self.street_one_data = ctk.CTkLabel(
            self.third_profile_frame,
            text=self.address_1_data,
            font=("Montserrat Bold", 14, "bold"),
            text_color="#B3B3B3",
   
        )
        self.street_one_data.place(x=20, y=56)

        if self.user_details[8]:
            self.address_2_data=self.user_details[8]
        else:
            self.address_2_data="N/A"

        #Street #2 label
        self.street_two_label = ctk.CTkLabel(
            self.third_profile_frame,
            text="Address #2 (Optional)",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        self.street_two_label.place(x=198, y=33)

        #street #2 data
        self.street_two_data = ctk.CTkLabel(
            self.third_profile_frame,
            text=self.address_2_data,
            font=("Montserrat Bold", 14, "bold"),
            text_color="#B3B3B3",
   
        )
        self.street_two_data.place(x=198, y=56)


        #City
        self.city_label = ctk.CTkLabel(
            self.third_profile_frame,
            text="City",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        self.city_label.place(x=20, y=82)

       #city_Data
        self.city_data=self.user_details[9]
        self.city_data = ctk.CTkLabel(
            self.third_profile_frame,
            text=self.city_data,
            font=("Montserrat Bold", 14, "bold"),
            text_color="#B3B3B3",
   
        )
        self.city_data.place(x=20, y=105)


        #Country_label
        self.country_label = ctk.CTkLabel(
            self.third_profile_frame,
            text="Country",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        self.country_label.place(x=198, y=82)

       #Country_Data
        self.country_data=self.user_details[11]
        self.country_data = ctk.CTkLabel(
            self.third_profile_frame,
            text=self.country_data,
            font=("Montserrat Bold", 14, "bold"),
            text_color="#B3B3B3",
   
        )
        self.country_data.place(x=198, y=105)

        #State Label
        self.state_label=ctk.CTkLabel(
            self.third_profile_frame,
            text="State",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        self.state_label.place(x=370, y=82)

        self.state_data=self.user_details[10]
        self.state= ctk.CTkLabel(
            self.third_profile_frame,
            text=self.state_data,
            font=("Montserrat Bold", 14, "bold"),
            text_color="#B3B3B3",
   
        )
        self.state.place(x=370, y=105)


        #zipcode_label
        self.zipcode_label = ctk.CTkLabel(
            self.third_profile_frame,
            text="ZIPCode",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        self.zipcode_label.place(x=480, y=82)

       #zipcide_Data
        self.zipcode_data=self.user_details[12]
        self.zipcode = ctk.CTkLabel(
            self.third_profile_frame,
            text= self.zipcode_data,
            font=("Montserrat Bold", 14, "bold"),
            text_color="#B3B3B3",
   
        )
        self.zipcode.place(x=480, y=105)

        edit_third_button = ctk.CTkButton(
            self.third_profile_frame,
            text="Edit",
            #command=self.loginFunc,
            width=45,
            height=25,
            corner_radius=10,
            fg_color="#FFFFFF",
            text_color="#B3B3B3",
            hover_color="#F2F2F2",
            border_color="#D2D2D2",
            border_width=1,
            command=self.address_entry_edit,
        
            font=("Montserrat Bold", 10,"bold"),
        )
        edit_third_button.place(x=655, y=18)



    def address_entry_edit(self):

        #street1_entry
        self.street1_entry = ctk.CTkEntry(
            self.third_profile_frame,
            width=150,
            height=20,
            font=("Montserrat", 12),
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
        )
        self.street1_entry.place(x=20, y=58)
        self.street1_entry.insert(0,self.address_1_data)

        #street2_entry
        self.street2_entry = ctk.CTkEntry(
            self.third_profile_frame,
            width=150,
            height=20,
            font=("Montserrat", 12),
            placeholder_text="APT E4*",
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
        )
        self.street2_entry.place(x=198, y=58)
        self.street2_entry.insert(0,self.address_2_data)

        #City_entry
        self.city_data=self.user_details[9]
        self.city_entry = ctk.CTkEntry(
            self.third_profile_frame,
            width=150,
            height=20,
            font=("Montserrat", 12),
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
        )
        self.city_entry.place(x=20, y=108)
        self.city_entry.insert(0,self.city_data)

        self.country_data=self.user_details[11]
        #Country_entry
        self.country_entry = ctk.CTkEntry(
            self.third_profile_frame,
            width=150,
            height=20,
            font=("Montserrat", 12),
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
        )
        self.country_entry.place(x=198, y=108)
        self.country_entry.insert(0,self.country_data)

      #state_entry
        self.state_entry = ctk.CTkEntry(
            self.third_profile_frame,
            width=75,
            height=20,
            font=("Montserrat", 12),
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
        )
        self.state_entry.place(x=369, y=108)
        self.state_entry.insert(0,self.state_data)

      #zipcode_entry
        self.zipcode_entry = ctk.CTkEntry(
            self.third_profile_frame,
            width=75,
            height=20,
            font=("Montserrat", 12),
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
        )
        self.zipcode_entry.place(x=480, y=105)
        self.zipcode_entry.insert(0,self.zipcode_data)

        save_button = ctk.CTkButton(
            self.third_profile_frame,
            text="Save",
            #command=self.loginFunc,
            width=45,
            height=25,
            corner_radius=5,
            fg_color="#6C9FFF",
            text_color="white",
            hover_color="#5E95FF",
            border_color="#6C9FFF",
            border_width=1,
            command=self.address_info_verification,
            font=("Montserrat Bold", 10,"bold"),
        )
        save_button.place(x=655, y=18)


    def open_calendar(self):
            # Create a Toplevel winqdow
            top = Toplevel(self.second_profile_frame)
            top.title("Select Date")
            top.geometry("300x200")  
            center_window(top,300,200)

            # Define the maximum selectable date
            max_date = date.today() - relativedelta(years=18)  

            # Create a custom ttk style for the calendar
            style = ttk.Style(self.second_profile_frame)
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
                maxdate=max_date,
                date_pattern="mm-dd-yyyy",
            )
            self.calendar.place(x=50, y=25)

            def select_date():
                self.selected_date = self.calendar.get_date()  
                self.calender_button.configure(text=self.selected_date,font=("Montserrat", 12))  
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
            select_button.place(x=130, y=160)

    


    def personal_info_verification(self):
        self.first_name_data=self.first_name_entry.get().strip()
        self.last_name_data=self.last_name_entry.get().strip()
        self.gender_data=self.gender_dropdown.get()
        self.dob_data=self.selected_date
        self.phone_number_data=self.phone_number_entry.get().strip()

        first_name_verification=validation(name=self.first_name_data)
        if first_name_verification is not None:
            self.first_name_entry.configure(font=("Montserrat", 11),text_color="red",border_color="red")
            self.error1_label.configure(text=f"Error: {first_name_verification}",text_color="red")
            return
        else:
            self.first_name_entry.configure(font=("Montserrat", 11),text_color="Black",border_color="#D2D2D2")
            self.error1_label.configure(text_color="white")
        
        #Lastname validation
        last_name_verification=validation(name=self.last_name_data)
        if last_name_verification is not None:
            self.last_name_entry.configure(font=("Montserrat", 11),text_color="red",border_color="red")
            self.error1_label.configure(text=f"Error: {last_name_verification}",text_color="red")
            return
        else:
            self.last_name_entry.configure(font=("Montserrat", 11),text_color="Black",border_color="#D2D2D2")
            self.error1_label.configure(text_color="white")


        #gender validation
        gender_validation=validation(gender=self.gender_data)
        if gender_validation is not None:
            self.gender_dropdown.configure(text_color="red")
            self.error1_label.configure(text=f"Error: Please select gender",text_color="red")
            return
        else:
              self.gender_dropdown.configure(text_color="black")
              self.error1_label.configure(text_color="white")


        dob_validation=validation(date=self.dob_data)
        if dob_validation is not None:
             self.calender_button.configure(font=("Montserrat", 11),border_color="red",text_color="red")
             self.error1_label.configure(text="Error: Please select date",text_color="red")
             return
        else:
              self.calender_button.configure(font=("Montserrat", 11),border_color="black",text_color="black")
              self.error1_label.configure(text_color="white")
        
        phone_validation=validation(phone=self.phone_number_data)

        if phone_validation is not None:
            self.phone_number_entry.configure(font=("Montserrat", 11),text_color="red",border_color="red")
            self.error1_label.configure(text=f"*Error: {phone_validation}",text_color="red")
            return
        else:
              self.phone_number_entry.configure(font=("Montserrat", 12),text_color="black",border_color="#D2D2D2")
              self.error1_label.configure(text_color="white")

        # Format to SQL-compatible YYYY-MM-DD format
        sql_date = self.dob_data.strftime("%Y-%m-%d")

        query = """UPDATE users SET first_name = %s, last_name = %s, gender = %s,dob = %s,phone = %s WHERE user_id = %s;"""
        values = (
                self.first_name_data,
                self.last_name_data,
                self.gender_data,
                sql_date,
                self.phone_number_data,

                self.user_details[0] 
            )

        update_users_table(query,values)
        self.update_data()
        self.mainwindow.update_data()
        self.personal_information_ui()
        self.top_info_ui()


    def address_info_verification(self):
        self.address_1_data=self.street1_entry.get().strip()
        self.address_2_data=self.street2_entry.get().strip()
        self.city_data=self.city_entry.get().strip()
        self.country_data=self.country_entry.get().strip()
        self.state_data=self.state_entry.get().strip()
        self.zipcode_data=self.zipcode_entry.get().strip()

        address1_validation=validation(address1=self.address_1_data)
        if address1_validation is not None:
            self.street1_entry.configure(font=("Montserrat", 11),border_color="red",text_color="red")
            self.error2_label.configure(text=address1_validation,text_color="red")
            return
        else:
             self.street1_entry.configure(font=("Montserrat", 11),border_color="#D2D2D2",text_color="black")
             self.error2_label.configure(text=address1_validation,text_color="white")

        city_validation=validation(city=self.city_data)
        if city_validation is not None:
             self.city_entry.configure(font=("Montserrat", 11),border_color="red",text_color="red")
             self.error2_label.configure(text=city_validation,text_color="red")
             return
        else:
             self.city_entry.configure(font=("Montserrat", 11),border_color="#D2D2D2",text_color="black")
             self.error2_label.configure(text_color="white")

        country_validation=validation(country=self.country_data)
        if country_validation is not None:
             self.country_entry.configure(font=("Montserrat", 11),border_color="red",text_color="red")
             self.error2_label.configure(text=country_validation,text_color="red")
             return
        else:
             self.country_entry.configure(font=("Montserrat", 11),border_color="#D2D2D2",text_color="black")
             self.error2_label.configure(text_color="white")

        
        state_validation=validation(state=self.state_data)
        if state_validation is not None:
             self.state_entry.configure(font=("Montserrat", 11),border_color="red",text_color="red")
             self.error2_label.configure(text=state_validation,text_color="red")
             return
        else:
            self.state_entry.configure(font=("Montserrat", 11),border_color="#D2D2D2",text_color="black")
            self.error2_label.configure(text_color="white")
        
        zipcode_validation=validation(zipcode=self.zipcode_data)
        if zipcode_validation is not None:
             self.zipcode_entry.configure(font=("Montserrat", 11),border_color="red",text_color="red")
             self.error2_label.configure(text=zipcode_validation,text_color="red")
             return
        else:
            self.zipcode_entry.configure(font=("Montserrat", 11),border_color="#D2D2D2",text_color="black")
            self.error2_label.configure(text=zipcode_validation,text_color="white")

        print(self.address_2_data)

        if self.address_2_data is None or self.address_2_data == "":

            query = """UPDATE users 
                    SET address_1 = %s, address_2 = %s, city = %s, state = %s, country = %s, zipcode = %s 
                    WHERE user_id = %s;"""

            values = (
                self.address_1_data,
                None,  
                self.city_data,
                self.state_data,
                self.country_data,
                self.zipcode_data,
                self.user_details[0],
            )

        else:
            query = """UPDATE users SET address_1 = %s,address_2 = %s,city = %s,state=%s,country = %s,zipcode = %s WHERE user_id = %s;"""
            values = (

                self.address_1_data,
                self.address_2_data,
                self.city_data,
                self.state_data,
                self.country_data,
                self.zipcode_data,
                self.user_details[0] 
            )
        update_users_table(query,values)
        self.update_data()
        self.top_info_ui()
        self.address_information_ui()

    def update_data(self):
        self.user_details=get_user_info_id(self.user_id)
        return self.user_details
    






        

        

    
    def account_gui(self):
        self.first_profile_frame.place_forget()
        self.second_profile_frame.place_forget()
        self.third_profile_frame.place_forget()
        # self.profile_btn.configure(state="enable",fg_color="#FFFFFF", text_color="#B3B3B3",hover_color="#F2F2F2")


    



















        
















        




  
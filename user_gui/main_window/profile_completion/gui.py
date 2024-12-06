from tkcalendar import Calendar
from utils import center_window,validation,update_users_table
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
    Profile_Completion()
    

class Profile_Completion(Frame):
    def __init__(self, parent, user_details, main_window):
        super().__init__(parent, )  # Attach to parent
        self.parent=parent
        self.user_details=user_details
        self.main_window = main_window
        self.configure(bg="white")  # Debug background for visibility

        # Create a container frame in MainWindow
        self.sub_container = Frame(self, bg="white", width=937, height=506)
        self.sub_container.place(x=0, y=0)  # Positioned next to the sidebar

        welcome_label = ctk.CTkLabel(
            self,
            text="Thanks for Joining!",
            font=("Montserrat Bold", 36,"bold"),
            text_color="#848484",
        )
        welcome_label.place(x=273, y=20)


        self.step1_ui()

    def step1_ui(self):

        self.completion_label = ctk.CTkLabel(
            self,
            text="Let's complete your profile",
            font=("Montserrat Bold", 20,"bold"),
            text_color="#CACACA",
        )
        self.completion_label.place(x=303, y=75)

        self.data_frame= ctk.CTkFrame(
                self.sub_container,
                width=881,
                height=339,
                fg_color="white",
                bg_color="white",
                border_width=1, 
                border_color="#D2D2D2",
                corner_radius=10,
            )
        self.data_frame.place(x=30,y=126)


        self.profile = Canvas(self.data_frame, width=35, height=35, bg="white", highlightthickness=0,)
        self.profile.place(x=397, y=15) 

        # Create the round button
        self.round_button = self.profile.create_oval(0, 0, 35, 35, fill="#7FE186", outline="")
        self.profile.create_text(17.5, 17.5, text="1", fill="white", font=("Arial", 12, "bold"))
       

        personal_details_label = ctk.CTkLabel(
            self.data_frame,
            text="Personal Details",
            font=("Montserrat Bold", 14,"bold"),
            text_color="#848484",
        )
        personal_details_label.place(x=363, y=50)
        
        #error_label
        self.error_text="Error"
        self.error_label = ctk.CTkLabel(
            self.data_frame,
            text=self.error_text,
            font=("Montserrat Bold", 11,),
            text_color="white",
   
        )
        self.error_label.place(x=363, y=75)

        #firstname_Label
        first_name_label = ctk.CTkLabel(
            self.data_frame,
            text="First Name",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        first_name_label.place(x=310, y=95)
        firstname_data=self.user_details[1]
        #First_name_Data
        first_name = ctk.CTkLabel(
            self.data_frame,
            text=firstname_data,
            font=("Montserrat Bold", 14, "bold"),
            text_color="#B3B3B3",
            anchor="center",
   
        )
        first_name.place(x=320, y=115)

        #lastname_Label
        last_name_label = ctk.CTkLabel(
            self.data_frame,
            text="First Name",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        last_name_label.place(x=453, y=95)
        lastname_data=self.user_details[2]
        #First_name_Data
        last_name = ctk.CTkLabel(
            self.data_frame,
            text=lastname_data,
            font=("Montserrat Bold", 14, "bold"),
            text_color="#B3B3B3",
            anchor="center",
   
        )
        last_name.place(x=463, y=115)

       #gender_label
        self.gender_label = ctk.CTkLabel(
            self.data_frame,
            text="Gender*",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        self.gender_label.place(x=310, y=152)

        # Define gender options
        self.gender_options = ["Male", "Female", "Other"]

        # Create the CTkOptionMenu
        self.gender_dropdown = ctk.CTkOptionMenu(
            master=self.data_frame,
            values=self.gender_options,
            width=80,
            height=18,
            fg_color="white",
            font=("Montserrat", 11),
            corner_radius=5,
            text_color="black",
            button_color="#6C9FFF"
        )
        self.gender_dropdown.set("Select Gender")  # Default value
        self.gender_dropdown.place(x=310, y=182)


        #age_label
        dob_label = ctk.CTkLabel(
            self.data_frame,
            text="Date Of Birth",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        dob_label.place(x=453, y=152)
        

        self.selected_date=("Select a date")  
        # Create the button to open the calendar
        self.calender_button = ctk.CTkButton(
            self.data_frame,
            text=self.selected_date,
            width=80,
            height=18,
            fg_color="white",
            text_color="black",
            hover_color="#D2D2D2",
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            command=self.open_calendar,
            font=("Montserrat Bold",11,),
        )
        self.calender_button.place(x=453, y=182)

        #phone_label
        self.phone_label = ctk.CTkLabel(
            self.data_frame,
            text="Phone Number*",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        self.phone_label.place(x=360, y=215)    

        #Phone_number_entry
        self.phone_number_entry = ctk.CTkEntry(
            self.data_frame,
            width=125,
            height=18,
            font=("Montserrat", 11),
            placeholder_text="Enter your Phone No",
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
        )
        self.phone_number_entry.place(x=360, y=245)

        next_button = ctk.CTkButton(
            self.data_frame,
            text="Next",
            width=108,
            height=39,
            corner_radius=10,
            fg_color="#6C9FFF",
            text_color="white",
            hover_color="#5E95FF",
            border_color="#6C9FFF",
            border_width=1,
            command=self.step1_verification,
            font=("Montserrat Bold", 10,"bold"),
        )
        next_button.place(x=362, y=280)

    def open_calendar(self):
            # Create a Toplevel winqdow
            top = Toplevel(self.data_frame)
            top.title("Select Date")
            top.geometry("300x200")  
            center_window(top,300,200)

            # Define the maximum selectable date
            max_date = date.today() - relativedelta(years=18)  

            # Create a custom ttk style for the calendar
            style = ttk.Style(self.data_frame)
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
            corner_radius=10,
            fg_color="#6C9FFF",
            text_color="white",
            hover_color="#5E95FF",
            border_color="#6C9FFF",
            border_width=1,
            font=("Montserrat Bold", 10,"bold"),
            )
            select_button.place(x=125, y=170)
    
    def step1_verification(self):
        self.dob=self.selected_date
        self.phone_number=self.phone_number_entry.get().strip()
        self.gender=self.gender_dropdown.get()
        gender_validation=validation(gender=self.gender)

        if gender_validation is not None:
            self.gender_dropdown.configure(text_color="red")
            self.error_label.configure(text=f"Please select gender",text_color="red")
            return
        else:
              self.gender_dropdown.configure(text_color="black")
              self.error_label.configure(text_color="white")

        dob_validation=validation(date=self.dob)

        if dob_validation is not None:
             self.calender_button.configure(font=("Montserrat", 11),border_color="red",text_color="red")
             self.error_label.configure(text="Please select date",text_color="red")
             return
        else:
              self.calender_button.configure(font=("Montserrat", 11),border_color="black",text_color="black")
              self.error_label.configure(text_color="white")
        
        phone_validation=validation(phone=self.phone_number)

        if phone_validation is not None:
            self.phone_number_entry.configure(font=("Montserrat", 11),text_color="red",border_color="red")
            self.error_label.configure(text=f"*{phone_validation}",text_color="red")
            return
        else:
              self.phone_number_entry.configure(font=("Montserrat", 12),text_color="black",border_color="#D2D2D2")
              self.error_label.configure(text_color="white")

        self.data_frame.place_forget()
        self.completion_label.place_forget()
        self.step2_ui()


    def step2_ui(self):
         
        self.completion_label.configure(text="Almost There!")
        self.completion_label.place_configure(x=363, y=68)

        
        self.data_frame= ctk.CTkFrame(
                self.sub_container,
                width=881,
                height=339,
                fg_color="white",
                bg_color="white",
                border_width=1, 
                border_color="#D2D2D2",
                corner_radius=10,
            )
        self.data_frame.place(x=30,y=126)

        self.profile = Canvas(self.data_frame, width=35, height=35, bg="white", highlightthickness=0,)
        self.profile.place(x=397, y=15) 

        # Create the round button
        self.round_button = self.profile.create_oval(0, 0, 35, 35, fill="#7FE186", outline="")
        self.profile.create_text(17.5, 17.5, text="2", fill="white", font=("Montserrat Bold", 12, "bold"))
       

        address_details_label = ctk.CTkLabel(
            self.data_frame,
            text="Address Information",
            font=("Montserrat Bold", 14,"bold"),
            text_color="#848484",
        )
        address_details_label.place(x=353, y=50)

   #error_label
        self.error_text="Error"
        self.error_label = ctk.CTkLabel(
            self.data_frame,
            text=self.error_text,
            font=("Montserrat Bold", 11,),
            text_color="white",
   
        )
        self.error_label.place(x=300, y=75)

        #address label
        address1_label = ctk.CTkLabel(
            self.data_frame,
            text="Address #1*",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        address1_label.place(x=255, y=95)

        #address1_entry
        self.address1_entry = ctk.CTkEntry(
            self.data_frame,
            width=175,
            height=18,
            font=("Montserrat", 11),
            placeholder_text="Enter Address #1",
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
        )
        self.address1_entry.place(x=220, y=120)


        #address2_Label
        address2_label = ctk.CTkLabel(
            self.data_frame,
            text="Address #2 (Optional)",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        address2_label.place(x=470, y=95)


        #address2_entry
        self.address2_entry = ctk.CTkEntry(
            self.data_frame,
            width=175,
            height=18,
            font=("Montserrat", 11),
            placeholder_text="Enter Address #2",
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
        )
        self.address2_entry.place(x=470, y=120)
    

       #city_label
        city_label = ctk.CTkLabel(
            self.data_frame,
            text="City*",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        city_label.place(x=280, y=152)

        #city_entry
        self.city_entry = ctk.CTkEntry(
            self.data_frame,
            width=110,
            height=18,
            font=("Montserrat", 11),
            placeholder_text="Enter City",
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
        )
        self.city_entry.place(x=250, y=182)


        #state_label
        state_label = ctk.CTkLabel(
            self.data_frame,
            text="State*",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        state_label.place(x=515, y=152)
        

        #state_entry
        self.state_entry = ctk.CTkEntry(
            self.data_frame,
            width=110,
            height=18,
            font=("Montserrat", 11),
            placeholder_text="Enter State",
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
        )
        self.state_entry.place(x=490, y=182)

        #zipcode_label
        zipcode_label = ctk.CTkLabel(
            self.data_frame,
            text="ZIPCode*",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        zipcode_label.place(x=270, y=215)    

        #zipcode_entry
        self.zipcode_entry = ctk.CTkEntry(
            self.data_frame,
            width=110,
            height=18,
            font=("Montserrat", 10),
            placeholder_text="Enter ZIPCode",
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
        )
        self.zipcode_entry.place(x=250, y=245)

        #country_label
        country_label = ctk.CTkLabel(
            self.data_frame,
            text="Country*",
            font=("Montserrat Bold", 14, "bold"),
            text_color="#CACACA",
   
        )
        country_label.place(x=510, y=215)
        

        #country_entry
        self.country_entry = ctk.CTkEntry(
            self.data_frame,
            width=110,
            height=18,
            font=("Montserrat", 11),
            placeholder_text="Enter Country",
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
        )
        self.country_entry.place(x=490, y=245)


        next_button = ctk.CTkButton(
            self.data_frame,
            text="Let's Go!",
            width=108,
            height=39,
            corner_radius=10,
            fg_color="#6C9FFF",
            text_color="white",
            hover_color="#5E95FF",
            border_color="#6C9FFF",
            border_width=1,
            command=self.step2_verification,
            font=("Montserrat Bold", 10,"bold"),
        )
        next_button.place(x=372, y=280)


        # Convert to datetime object
        date_obj = datetime.strptime(self.dob, '%m-%d-%Y')

        # Format as YYYY-MM-DD
        self.dob = date_obj.strftime('%Y-%m-%d')

    def step2_verification(self):
        self.address1=self.address1_entry.get().strip()
        self.address2=self.address2_entry.get().strip()
        self.city=self.city_entry.get().strip()
        self.country=self.country_entry.get().strip()
        self.zipcode=self.zipcode_entry.get().strip()
        self.state=self.state_entry.get().strip()
        

        address1_validation=validation(address1=self.address1)
        if address1_validation is not None:
            self.address1_entry.configure(font=("Montserrat", 11),border_color="red",text_color="red")
            self.error_label.configure(text=address1_validation,text_color="red")
            return
        else:
             self.address1_entry.configure(font=("Montserrat", 11),border_color="#D2D2D2",text_color="black")
             self.error_label.configure(text=address1_validation,text_color="white")

        city_validation=validation(city=self.city)
        if city_validation is not None:
             self.city_entry.configure(font=("Montserrat", 11),border_color="red",text_color="red")
             self.error_label.configure(text=city_validation,text_color="red")
             return
        else:
             self.city_entry.configure(font=("Montserrat", 11),border_color="#D2D2D2",text_color="black")
             self.error_label.configure(text_color="white")

        
        state_validation=validation(state=self.state)
        if state_validation is not None:
             self.state_entry.configure(font=("Montserrat", 11),border_color="red",text_color="red")
             self.error_label.configure(text=state_validation,text_color="red")
             return
        else:
            self.state_entry.configure(font=("Montserrat", 11),border_color="#D2D2D2",text_color="black")
            self.error_label.configure(text_color="white")
        
        zipcode_validation=validation(zipcode=self.zipcode)
        if zipcode_validation is not None:
             self.zipcode_entry.configure(font=("Montserrat", 11),border_color="red",text_color="red")
             self.error_label.configure(text=zipcode_validation,text_color="red")
             return
        else:
            self.zipcode_entry.configure(font=("Montserrat", 11),border_color="#D2D2D2",text_color="black")
            self.error_label.configure(text=zipcode_validation,text_color="white")

        country_validation=validation(country=self.country)
        if country_validation is not None:
             self.country_entry.configure(font=("Montserrat", 11),border_color="red",text_color="red")
             self.error_label.configure(text=country_validation,text_color="red")
             return
        else:
             self.country_entry.configure(font=("Montserrat", 11),border_color="#D2D2D2",text_color="black")
             self.error_label.configure(text_color="white")

        if self.address2 is None or self.address2=="":

            query = """UPDATE users SET gender = %s,dob = %s,phone = %s,address_1 = %s,city = %s,state=%s,country = %s,zipcode = %s, profile_completion = %s WHERE user_id = %s;"""
            
            values = (
                self.gender,
                self.dob,
                self.phone_number,
                self.address1,
                self.city,
                self.state,
                self.country,
                self.zipcode,
                1,
                self.user_details[0] 
            )
        else:
            query = """UPDATE users SET gender = %s,dob = %s,phone = %s,address_1 = %s,address_2 = %s,city = %s,state=%s,country = %s,zipcode = %s, profile_completion = %s WHERE user_id = %s;"""
            values = (
                self.gender,
                self.dob,
                self.phone_number,
                self.address1,
                self.address2,
                self.city,
                self.state,
                self.country,
                self.zipcode,
                1,
                self.user_details[0] 
            )

            update_users_table(query,values)
        
        self.profile_completion_window=ctk.CTkToplevel(self.data_frame, width=600, height=100, fg_color= 'white'

        )
        self.profile_completion_window.title("Profile Completion")
        self.profile_completion_window.geometry("300X100")
        center_window(self.profile_completion_window, 300, 100)

        completion_label = ctk.CTkLabel(
            self.profile_completion_window,
            text="Sucessfully updated!",
            font=("Montserrat Bold", 14,"bold"),
            text_color="#848484",
        )
        completion_label.place(x=80, y=15)
        
        lets_go_button = ctk.CTkButton(
        self.profile_completion_window,
        text="Let’s do it!",
        width=70,
        height=30,
        corner_radius=5,
        fg_color="#6C9FFF",
        text_color="white",
        hover_color="#5E95FF",
        border_color="#6C9FFF",
        border_width=1,
        command=self.return_to_dashboard,
        font=("Montserrat Bold", 11,"bold"),
        )
        lets_go_button.place(x=115, y=60)
        
    def return_to_dashboard(self):
        # Use the main_window reference to go back to the Dashboard
        self.destroy()
        self.main_window.handle_btn_press(self.main_window.dashboard_btn, "dash")
        
        

             
             
             




         

    





         
             
            
             
             

        
from tkcalendar import Calendar
from utils import center_window,validation,get_user_info_id,update_users_table,send_email
from datetime import date,datetime
import datetime
from dateutil.relativedelta import relativedelta
from tkinter import Frame
from controller import *
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
    messagebox
    
)
from tkinter import PhotoImage, Label
from PIL import ImageTk, Image
import hashlib
import random



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def start_gui():
    Support_Gui()

class Support_Gui(Frame):
    def __init__(self, parent, user_id,mainwindow, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)  # Attach to parent
        self.user_id = user_id
        self.parent=parent
        self.mainwindow=mainwindow
        self.user_details=get_user_info_id(self.user_id)

        self.config(bg="white")

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
        support_label = ctk.CTkLabel(
            self.side_frame,
            text="Support",
            font=("Montserrat Bold", 36,"bold"),
            text_color="#B3B3B3",
        )
        support_label.place(x=15, y=30)

 
        self.profile_btn = ctk.CTkButton(
            self.side_frame,
            text="Raise a Request",
            #command=self.loginFunc,
            width=168,
            height=50,
            corner_radius=0,
            fg_color="#D9D9D9",
            text_color="#B3B3B3",
            hover_color="#F2F2F2",
            font=("Montserrat Bold", 16,"bold")
        )
        self.profile_btn.place(x=0, y=112)

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
    
       # wish title
        wish_label = ctk.CTkLabel(
            self.center_frame,
            text=f"Hello {self.user_details[1]}, what do you need help with?",
            font=("Montserrat Bold", 16,"bold"),
            text_color="#B3B3B3",
        )
        wish_label.place(x=165, y=3)

        self.error_label = ctk.CTkLabel(
            self.center_frame,
            text_color="white",
            font=("Montserrat Bold", 12,"bold"),
        )
        self.error_label.place(x=245, y=350)

        email_label = ctk.CTkLabel(
            self.center_frame,
            text=f"Email:",
            font=("Montserrat Bold", 16,"bold"),
            text_color="#B3B3B3",
        )
        email_label.place(x=198, y=38)

        email_data_label= ctk.CTkLabel(
            self.center_frame,
            text=f"{self.user_details[3]}",
            font=("Montserrat Bold", 16,"bold"),
            text_color="black",
        )
        email_data_label.place(x=280, y=38)

        subject_label= ctk.CTkLabel(
            self.center_frame,
            text="Subject*:",
            font=("Montserrat Bold", 16,"bold"),
            text_color="#B3B3B3",
        )
        subject_label.place(x=198, y=102)

        self.subject_entry = ctk.CTkEntry(
            self.center_frame,
            width=243,
            height=35,
            font=("Montserrat", 14),
            border_color="#D2D2D2",
            border_width=1,
            corner_radius=5,
            placeholder_text_color="black"
            
        )
        self.subject_entry.place(x=292, y=100)

        request_label= ctk.CTkLabel(
            self.center_frame,
            text="Tell us, how we can help you?*",
            font=("Montserrat Bold", 16,"bold"),
            text_color="#B3B3B3",
        )
        request_label.place(x=198, y=167)

        self.query = ctk.CTkTextbox(
            self.center_frame,
            height=134,
            width=340,
            font=("Montserrat", 14),
            corner_radius=10,
            border_color="#B3B3B3",
            border_width=1,

        )
        self.query.place(x=200, y=207)

        self.save_button = ctk.CTkButton(
            self.center_frame,
            text="Send Request",
            #command=self.loginFunc,
            width=120,
            height=39,
            corner_radius=5,
            fg_color="#6C9FFF",
            text_color="white",
            hover_color="#5E95FF",
            border_color="#6C9FFF",
            border_width=1,
            command=self.submit_request,
            font=("Montserrat Bold", 14,"bold"),
        )
        self.save_button.place(x=600, y=260)

    def submit_request(self):
        body=self.query.get("1.0", "end-1c")
        subject=self.subject_entry.get().strip()
        ct = datetime.datetime.now()
        ticket_number = str(random.randint(100000, 999999))
        self.email=self.user_details[3]
        self.first_name=self.user_details[1]
        self.last_name=self.user_details[2]
        self.full_name=f"{self.user_details[1]} {self.user_details[2]}"
        

        
        #Minmum word length
        body_words = body.split()
        subject_words=subject.split()
        
        if len(subject_words)<=2 or subject=='':
            self.subject_entry.configure(border_color="red",text_color="red")
            self.error_label.configure(text="*Error: Subject shouldn't be empty or minimum 2 words",text_color="red",font=("Montserrat", 12)) 
            return
        if len(body_words)<=10 or body=='':
            self.subject_entry.configure(border_color="#D2D2D2",text_color="black")
            self.error_label.configure(text="*Error: Subject shouldn't be empty or minimum 2 words",text_color="white",font=("Montserrat", 12)) 
            self.query.configure(border_color="red",text_color="red")
            self.error_label.configure(text="Error: Message shouldn't be empty or minimum 10 words",text_color="red",font=("Montserrat", 12))  
            return

        else:
            self.query.configure(border_color="#D2D2D2",text_color="black")
            self.error_label.configure(text_color="white",font=("Montserrat", 12))

    
    
        try:
        

            user_subject="Thanks for contacting us."
            
            user_body = f"""
            Hi {self.full_name},

            Ticket ID: {ticket_number},
            Thanks for contacting TFS Support. We will get back to you within 24 Hours.

            Thanks,
            Local Food Sharing App
            """
            tech_subject=f"{self.subject_entry.get()} #{ticket_number} - {ct}"
            tech_body=f"""
            
            First Name: {self.first_name}
            Last Name: {self.last_name}
            Email:{self.email}
            Time_Requested: {ct}
            Request:
                    {body}

            Thanks,
            Local Food Sharing App
            """

            user_emaail=send_email(self.email,user_subject,user_body)
            tech_email=send_email("localfoodsharing@gmail.com",tech_subject,tech_body)
        
        except:

            # Notify the user
            self.error_label.configure(text="Request Submited! Typically recieve email within 24hrs",text_color="green",font=("Montserrat", 12))  
            self.save_button.configure(
            text="Request Sent!",
            text_color="white",
            fg_color="green",
            )
            self.save_button.configure(state="disabled")










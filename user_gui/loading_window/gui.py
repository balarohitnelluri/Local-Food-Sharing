import customtkinter as ctk
from tkinter import (
    Toplevel,
    Frame,
    Canvas,
    Button,
    PhotoImage,
    messagebox,
    StringVar,
)
import sys
import os
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from user_gui.login.gui import loginWindow
from user_gui.main_window.main import mainWindow
from utils import center_window


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def loadingwindow():
    LoadingWindow()

class LoadingWindow(Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure window
        self.title("Login - Local Food Sharing App")
        self.geometry("508x625")
        self.configure(bg="#5E95FF")
        center_window(self,508,608)

       # Left Section with Canvas
        self.window_canvas = Canvas(
            self,
            bg="#5E95FF",
            height=625,
            width=508,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.window_canvas.place(x=0, y=0)

        self.logo_image = PhotoImage(file=relative_to_assets("Logo_Label.png"))  # Replace with your image path
        self.window_canvas.create_image(73, 75, anchor="nw", image=self.logo_image)

        self.background_image = PhotoImage(file=relative_to_assets("Loading_Logo.png"))  # Replace with your image path
        self.window_canvas.create_image(164, 175, anchor="nw", image=self.background_image)

    
        copyright_label=ctk.CTkLabel(
            self,
            text='"Copyright 2024 Local Food Sharing Inc - All Rights Received"',
            font=("Montserrat Bold", 13,"bold"),  
            text_color="white",
        )
        copyright_label.place(x=55, y=580)

        self.status_label=ctk.CTkLabel(
            self,
            text='Please Wait...',
            font=("Montserrat Bold", 13,"bold"),  
            text_color="white",
        )
        self.status_label.place(x=80, y=435)

        self.percentage_label=ctk.CTkLabel(
            self,
            text='Please Wait...',
            font=("Montserrat Bold", 13,"bold"),  
            text_color="white",
        )
        self.percentage_label.place(x=415, y=435)


        self.progress_bar = ctk.CTkProgressBar(self, width=356,height=10, fg_color="lightgrey", progress_color="White")
        self.progress_bar.place(x=80, y=465)
        self.progress_bar.set(0)  # Initialize progress to 0%
        self.loading_messages = [
        "Initializing...",
        "Loading Resources...",
        "Connecting to Database...",
        "Fetching Data...",
        "Validating Files...",
        "Setting Up Environment...",
        "Optimizing Performance...",
        "Almost Done...",
        "Finalizing...",
        "Loading Complete!"
    ]

        self.start_loading()



    def start_loading(self):
        """Start the loading process."""
        self.progress_bar.set(0)  # Reset progress bar
        self.update_progress(0)


    def update_progress(self, value):
        if value <= 1:  # Progress bar values range from 0 to 1
            self.progress_bar.set(value)  # Update progress bar
            percentage = int(value * 100)
            # Update loading message based on progress
            message_index = int(value * (len(self.loading_messages) - 1))
            self.status_label.configure(text=f"{self.loading_messages[message_index].ljust(100)}")
            self.percentage_label.configure(text=f"{percentage}%")
            
            self.after(50, self.update_progress, value + 0.01)  # Increment progress by 1% every 50ms
        else:
            self.destroy()
            user_id = loginWindow()  # Get the logged-in user ID
            if user_id:
                # If login is successful, launch the main application window with the user ID
                
                mainWindow(user_id)
    
    
        
    

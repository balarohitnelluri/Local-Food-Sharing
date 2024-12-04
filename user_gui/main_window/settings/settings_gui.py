from pathlib import Path
from tkinter import Frame, Canvas, Entry, Text, Button, PhotoImage, messagebox
from controller import *
import customtkinter as ctk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def start_settings_gui():
        Settings_Gui()
        ()

class Settings_Gui(Frame):
    def __init__(self, user_id, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.user_id = user_id

        # Outer tkinter Frame for wrapping
        self.configure(bg="#EDEDED")

        # Central CTKFrame to hold all fields
        central_frame = ctk.CTkFrame(
            self,
            width=769,
            height=393,
            fg_color="white",
            border_color="D2D2D2"
        )
        central_frame.place(x=243,y=133)

        self.side_frame=ctk.CTkFrame(
            self,
            width=769,
            height=393,
            fg_color="white",
            border_color="D2D2D2"
        )
        central_frame.place(x=74,y=112)

        # Title
        settings_label = ctk.CTkLabel(
            central_frame,
            text="Settings",
            font=("Montserrat Bold", 36),
            text_color="#B3B3B3",
        )
        settings_label.place(x=91, y=38)

        self.mainloop()

        






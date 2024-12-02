from pathlib import Path

from tkinter import Frame, Canvas, Entry, Text, Button, PhotoImage, messagebox
from controller import *
import controller as db_controller

from .add_reservations.gui import SchedulePickup

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def Pickup_schedule():
    Pickup_schedule()


class Pickup_schedule(Frame):
    def __init__(self, parent, user_id, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.selected_rid = None
        self.reservation_data = db_controller.get_listing_details(user_id = user_id)

        self.configure(bg="#FFFFFF")

        # Loop through windows and place them
        self.windows = {
            "add": SchedulePickup(self, user_id = user_id),
        }

        self.current_window = self.windows["add"]
        self.current_window.place(x=0, y=0, width=1013.0, height=506.0)

        self.current_window.tkraise()

    def navigate(self, name):
        # Hide all screens
        for window in self.windows.values():
            window.place_forget()

        # Show the screen of the button pressed
        self.windows[name].place(x=0, y=0, width=1013.0, height=506.0)

    def refresh_entries(self):
        self.reservation_data = db_controller.get_reservations()
        self.windows.get("view").handle_refresh()

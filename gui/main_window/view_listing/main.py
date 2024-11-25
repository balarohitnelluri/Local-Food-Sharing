from pathlib import Path
from tkinter import Frame
import controller as db_controller
from .add_guests.gui import FindFood

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def SearchFood():
    SearchFood()


class SearchFood(Frame):
    def __init__(self, parent, user_id, *args, **kwargs):
        """
        Initialize the SearchFood frame.
        :param parent: Parent container.
        :param user_id: ID of the currently logged-in user.
        """
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.user_id = user_id  # Save user_id for user-specific operations
        self.selected_rid = None  # Placeholder for selected record
        self.guest_data = db_controller.get_food_items(user_id=user_id)

        self.configure(bg="#FFFFFF")

        # Define the screen components and pass user_id to FindFood
        self.windows = {
            "add": FindFood(self, user_id=self.user_id),
        }

        self.current_window = self.windows["add"]
        self.current_window.place(x=0, y=0, width=1013.0, height=506.0)
        self.current_window.tkraise()

    def navigate(self, name):
        """
        Navigate between screens.
        :param name: The key name of the screen to show.
        """
        # Hide all screens
        for window in self.windows.values():
            window.place_forget()

        # Show the selected screen
        self.windows[name].place(x=0, y=0, width=1013.0, height=506.0)

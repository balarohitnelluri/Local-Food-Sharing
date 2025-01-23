from pathlib import Path
from tkinter import Frame
import controller as db_controller
from .add_food.gui import AddFoodForm

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def AddFoodItem():
    AddFoodItem()


class AddFoodItem(Frame):
    def __init__(self, parent, user_id, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.user_id = user_id  # Store user_id for user-specific operations
        self.selected_food_id = None  # For tracking selected food item
        self.food_data = db_controller.get_food_items(user_id=user_id)  # Fetch user-specific food items

        self.configure(bg="#FFFFFF")

        # Define screens for adding and viewing food items
        self.screens = {
            "add": AddFoodForm(self, user_id=user_id),  # Pass user_id to AddFoodForm
        }

        # Set the default screen to the Add Food Form
        self.current_screen = self.screens["add"]
        self.current_screen.place(x=0, y=0, width=1013.0, height=506.0)

        # Bring the current screen to the front
        self.current_screen.tkraise()

    def navigate(self, name):
        """
        Navigate between screens (Add Food Form and View Food Items).
        """
        # Hide all screens
        for screen in self.screens.values():
            screen.place_forget()

        # Show the selected screen
        self.screens[name].place(x=0, y=0, width=1013.0, height=506.0)

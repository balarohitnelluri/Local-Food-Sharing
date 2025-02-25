from pathlib import Path
from tkinter import (
    Toplevel,
    Frame,
    Canvas,
    Button,
    PhotoImage,
    messagebox,
    StringVar,
)
from controller import *
from user_gui.main_window.dashboard.gui import Dashboard
from user_gui.main_window.pickup_schedule.add_pickup.gui import SchedulePickup

from user_gui.main_window.notifications.main import Notification
from user_gui.main_window.add_listing.main import AddFoodItem
from user_gui.main_window.view_listing.main import SearchFood
from user_gui.main_window.settings.settings_gui import Settings_GUI
from user_gui.main_window.profile_completion.gui import Profile_Completion
from user_gui.main_window.support.gui import Support_Gui
import customtkinter as ctk  


from .. import login
from utils import center_window,get_user_info_id
from PIL import Image,ImageTk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def mainWindow(user_id):
    MainWindow(user_id)


class MainWindow(Toplevel):
    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # User-specific information
        self.user_id = user_id
        self.user_details=self.update_data()
        self.profile_completion=bool(self.user_details[14])
        
        # Configure main window
        self.title("Local Food Sharing")
        self.geometry("1012x506")
        self.configure(bg="#FFFFFF")
        center_window(self,1012,506)
        

        # Create canvas layout
        self.canvas = Canvas(
            self,
            bg="#5E95FF",
            height=506,
            width=1012,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)
        self.canvas.bind("<Enter>", self.expand_sidebar)
        self.canvas.bind("<Leave>", self.collapse_sidebar)
        
        
        # Background rectangle for content
        self.canvas.create_rectangle(
            215, 0.0, 1012.0, 506.0, fill="#FFFFFF", outline=""
        )

        # Sidebar indicator
        self.sidebar_indicator = Frame(self, background="#FFFFFF")
        self.sidebar_indicator.place(x=0, y=133, height=47, width=7)

        # Create a container frame in MainWindow
        self.container = Frame(self, bg="white", width=937, height=506)
        self.container.place(x=75, y=0)  # Positioned next to the sidebar

        self.account_settings_icon= PhotoImage(file=relative_to_assets("Settings_button.png"))
        self.support_icon=PhotoImage(file=relative_to_assets("support.png"))
        self.logout_icon=PhotoImage(file=relative_to_assets("logout.png"))
        self.collaped_logo=PhotoImage(file=relative_to_assets("logo_collapsed.png"))
        self.logo_with_label=PhotoImage(file=relative_to_assets("logo_with_label.png"))
        
        self.logo_btn = Button(
            self.canvas,
            image=self.collaped_logo,
            borderwidth=0,
            highlightthickness=0,
            #background="#5E95FF",
            command=lambda: self.handle_btn_press(self.dashboard_btn, "dash"),
            cursor='hand2', #activebackground="#5E95FF",
            relief="flat",
        )
        self.logo_btn.place(x=2,y=13,width=75,height=75)
        self.logo_btn.bind("<Enter>", self.expand_sidebar)
        self.logo_btn.bind("<Leave>", self.collapse_sidebar)

        self.dashboard_icon_extended = PhotoImage(file=relative_to_assets("dashboard_icon_extended.png"))
        self.dashboard_icon_collapsed = PhotoImage(file=relative_to_assets("dashboard_icon_collapsed.png"))
        self.dashboard_btn = Button(
            self.canvas,
            image=self.dashboard_icon_extended,
            borderwidth=0,
            highlightthickness=0,
            background="#5E95FF",
            command=lambda: self.handle_btn_press(self.dashboard_btn, "dash"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )    
        self.dashboard_btn.place(x=29, y=116, width=167, height=36)
        self.dashboard_btn.bind("<Enter>", self.expand_sidebar)
        self.dashboard_btn.bind("<Leave>", self.collapse_sidebar)

        self.donate_extended=PhotoImage(file=relative_to_assets("donate_extended.png"))
        self.donate_icon_collapsed = PhotoImage(file=relative_to_assets("donate_icon_collapsed.png"))
        self.add_listing_btn = Button(
            self.canvas,
            image=self.donate_extended,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press(self.add_listing_btn, "adi"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.add_listing_btn.place(x=29, y=182, width=167, height=36)
        self.add_listing_btn.bind("<Enter>", self.expand_sidebar)
        self.add_listing_btn.bind("<Leave>", self.collapse_sidebar)

        self.pickup_extended = PhotoImage(file=relative_to_assets("pickup_extended.png"))
        self.pickup_icon_collapsed = PhotoImage(file=relative_to_assets("pickup_icon_collapsed.png"))
        self.schedule_pickup_btn = Button(
            self.canvas,
            image=self.pickup_extended,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press(self.schedule_pickup_btn, "spu"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )

        self.schedule_pickup_btn.place(x=24, y=245, width=167, height=56.0)
        self.schedule_pickup_btn.bind("<Enter>", self.expand_sidebar)
        self.schedule_pickup_btn.bind("<Leave>", self.collapse_sidebar)

        self.community_icon_extended=PhotoImage(file=relative_to_assets("Community_Extended.png"))
        self.community_Icon_collapsed = PhotoImage(file=relative_to_assets("community_Icon_collapsed.png"))
        self.community_btn = Button(
            self.canvas,
            image=self.community_icon_extended,
            borderwidth=0,
            command=self.community,
            highlightthickness=0,
            relief="flat",
        )

        self.community_btn.place(x=31, y=335, width=167, height=32)
        self.community_btn.bind("<Enter>", self.expand_sidebar)
        self.community_btn.bind("<Leave>", self.collapse_sidebar)    
        
        
        self.notifications_icon_extended= PhotoImage(file=relative_to_assets("notifications_icon_extended.png"))
        self.notifications_icon_collapsed = PhotoImage(file=relative_to_assets("notification_icon_collapsed.png"))
        self.notifications_btn = Button(
            self.canvas,
            image=self.notifications_icon_extended,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press(self.notifications_btn, "not"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.notifications_btn.place(x=32, y=417, width=167, height=26)
        self.notifications_btn.bind("<Enter>", self.expand_sidebar)
        self.notifications_btn.bind("<Leave>", self.collapse_sidebar) 

        # Loop through windows and pass user_id
        self.windows = {
            "dash": Dashboard(self.container,self.user_id),
            "adi": AddFoodItem(self.container, self.user_id),
            "gue": SchedulePickup(self.container, self.user_id),
            "not": Notification(self.container, self.user_id),
            "spu": SearchFood(self.container, self.user_id),



        }

        # Load the background image
        self.bg_image_user = ImageTk.PhotoImage(Image.open(relative_to_assets("user_toggle.png")))  # Path to "User" rectangle image
        self.bg_image_admin = ImageTk.PhotoImage(Image.open(relative_to_assets("admin_toggle.png")))  # Path to "Admin" rectangle image

        # Create a canvas to display the toggle
        self.toggle_canvas = Canvas(self, width=100,height=46, highlightthickness=0,background="white")
        #self.toggle_canvas.place(x=821, y=0)
        # Add the initial background image
        self.bg_item = self.toggle_canvas.create_image(65, 28, image=self.bg_image_user)
        # Add the toggle circle
        self.toggle_circle = self.toggle_canvas.create_oval(32, 16, 55, 40, fill="white", outline="lightgrey")



        # Bind the toggle functionality
        self.toggle_canvas.tag_bind(self.bg_item, "<Button-1>", self.toggle)
        self.toggle_canvas.tag_bind(self.toggle_circle, "<Button-1>", self.toggle)

        if self.profile_completion is False:
            if "pr" not in self.windows:
                self.windows["pr"] = Profile_Completion(self.container, self.user_details,self)
                self.sidebar_indicator.place_forget()
                self.windows["pr"].place(x=0, y=0, width=937, height=506.0)
        else:
            self.handle_btn_press(self.dashboard_btn, "dash")

        #self.collapse_sidebar("leave")

        #Initial Navbar position
        self.sidebar_indicator.place(x=0, y=116)

        # Main window setup
        self.resizable(False, False)
        self.show_profile_icon()
        self.hide_dropdown()
        self.mainloop()

    

    def show_dropdown(self, event=None):
        if not self.dropdown_menu:
            self.dropdown_menu = Frame(self, bg="white", relief="flat", bd=2)
            self.dropdown_menu.place(x=850, y=70, width=150)

            self.account_settings_button = Button(
            self.dropdown_menu,
            image=self.account_settings_icon,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press(self.account_settings_button, "set"),
            cursor='hand2', activebackground="white",
            relief="flat",
        )
            self.account_settings_button.pack(fill="x",padx=12, pady=0)

            self.support_button = Button(
            self.dropdown_menu,
            image=self.support_icon,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press(self.support_button, "sup"), 
            cursor='hand2', activebackground="white",
            relief="flat",
        )
            self.support_button.pack(fill="x",padx=12, pady=0)

            self.logout_button = Button(
            self.dropdown_menu,
            image=self.logout_icon,
            borderwidth=0,
            highlightthickness=0,
            command=self.logout,
            cursor='hand2', activebackground="white",
            relief="flat",
        )
            self.logout_button.pack(fill="x",padx=12, pady=0)

            # Bind hover events to the dropdown menu
            self.dropdown_menu.bind("<Enter>", self.cancel_hide_dropdown_timer)
            self.dropdown_menu.bind("<Leave>", self.start_hide_dropdown_timer)

    def show_profile_icon(self):
        #profile
        # Create a canvas to design the round button
        self.user_firstname=self.user_details[1]
        self.profile = Canvas(self, width=35, height=35, bg="white", highlightthickness=0,)
        self.profile.place(x=925, y=30)

        # Create the round button
        self.round_button = self.profile.create_oval(0, 0, 35, 35, fill="#0078D7", outline="")
        self.profile.create_text(17.5, 17.5, text=f"{self.user_firstname[0].upper()}", fill="white", font=("Arial", 12, "bold"))

         # Bind hover events
        self.profile.bind("<Enter>", self.show_dropdown)
        self.profile.bind("<Leave>", self.start_hide_dropdown_timer)

        # Dropdown menu container
        self.dropdown_menu = None

    def start_hide_dropdown_timer(self, event=None):
        """Start a timer to hide the dropdown after a delay."""
        self.cancel_hide_dropdown_timer()  # Cancel any existing timer
        self.hide_timer = self.after(500, self.hide_dropdown)  # Adjust delay as needed

    def cancel_hide_dropdown_timer(self, event=None):
        if hasattr(self, 'hide_timer') and self.hide_timer:
            self.after_cancel(self.hide_timer)
            self.hide_timer = None

    def hide_dropdown(self):
        """Hide the dropdown menu."""
        if self.dropdown_menu:
            self.dropdown_menu.destroy()
            self.dropdown_menu = None
        self.hide_timer = None  # Reset the timer reference

    def logout(self):
        confirm = messagebox.askyesno("Confirm log-out", "Do you really want to log out?")
        if confirm:
            self.destroy()
            login.gui.loginWindow()

    def check_mouse_position(self, event=None):

        widget_under_mouse = self.winfo_containing(self.winfo_pointerx(), self.winfo_pointery())
        if widget_under_mouse != self.dropdown_menu and widget_under_mouse != self.canvas:
            self.hide_dropdown()

    def keep_dropdown_open(self, event=None):
        pass  # Do nothing to keep the dropdown open

    def handle_btn_press(self, caller, name):
    # Check if caller is valid
        if caller and hasattr(caller, "winfo_y"):
            self.sidebar_indicator.place(x=0, y=caller.winfo_y())
        else:
            # Handle cases where caller is None
            print(f"Caller is invalid: {caller}")
            self.sidebar_indicator.place_forget()
         
        if self.profile_completion is False:
            self.sidebar_indicator.place_forget()
            self.profile_completion_window=ctk.CTkToplevel(self, width=600, height=100, fg_color= 'white'
            )
            self.profile_completion_window.title("Profile Completion")
            self.profile_completion_window.geometry("600X100")
            center_window(self.profile_completion_window, 600, 100)

            completion_label = ctk.CTkLabel(
                self.profile_completion_window,
                text="We know you’re in a hurry, but even superheroes fill out their profiles first.",
                font=("Montserrat Bold", 12,"bold"),
                text_color="#848484",
            )
            completion_label.place(x=70, y=25)
            
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
            command=self.profile_completion_window.destroy,
            font=("Montserrat Bold", 11,"bold"),
            )
            lets_go_button.place(x=250, y=60)
            return

        # Hide all current windows
        for window in self.windows.values():
            if window and window.winfo_exists():
                window.place_forget()

        # Lazy-load screens if not already loaded
        if name not in self.windows:
            if name == "dash":
                self.windows["dash"] = Dashboard(self.container,self.user_id)
            elif name == "adi":
                self.windows["adi"] = AddFoodItem(self.container, self.user_id)
            elif name == "gue":
                self.windows["gue"] = SchedulePickup(self.container, self.user_id)
            elif name == "not":
                self.windows["not"] = Notification(self.container, self.user_id)
            elif name == "spu":
                self.windows["spu"] = SearchFood(self.container, self.user_id)
            elif name == "set":
                self.windows["set"] = Settings_GUI(self.container, self.user_id,self,self.windows.get("dash"))
                self.sidebar_indicator.place_forget()
            elif name == "sup":
                self.windows['sup'] = Support_Gui(self.container,self.user_id,self)
                self.sidebar_indicator.place_forget()
            else:
                print(f"Unknown window name: {name}")
                return

        # Set and display the current window
        self.current_window = self.windows.get(name)
        if self.current_window:
            self.current_window.place(x=0, y=0, width=937, height=506.0)
        else:
            print(f"Failed to load window: {name}")
   
    def update_data(self):
        self.user_details=get_user_info_id(self.user_id)
        self.show_profile_icon()
        return self.user_details


    def update_profile_completion(self):
        self.profile_completion=self.user_details[14]
        self.handle_btn_press(self.dashboard_btn, "dash")

    def support(self):
        
        self.hide_dropdown()

    def community(self):
        self.profile_completion_window=ctk.CTkToplevel(self, width=600, height=100, fg_color= 'white'
        )
        self.profile_completion_window.title("Profile Completion")
        self.profile_completion_window.geometry("600X100")
        center_window(self.profile_completion_window, 600, 100)

        completion_label = ctk.CTkLabel(
            self.profile_completion_window,
            text="Hold On! we know you're in hurry to explore, we will get this feature soon!",
            font=("Montserrat Bold", 12,"bold"),
            text_color="#848484",
        )
        completion_label.place(x=70, y=25)
        
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
        command=self.profile_completion_window.destroy,
        font=("Montserrat Bold", 11,"bold"),
        )
        lets_go_button.place(x=250, y=60)
        return

    def expand_sidebar(self, event):
        for button in [self.dashboard_btn, self.add_listing_btn, self.schedule_pickup_btn, self.notifications_btn, self.community_btn,]:
            self.canvas.configure(width=215)
            self.logo_btn.place_configure(x=2,y=13,width=212,height=60,)
            self.logo_btn.config(image=self.logo_with_label)
            self.container.lower()

            #Buttons
            self.dashboard_btn.place_configure(x=29, y=116, width=167, height=36)
            self.dashboard_btn.config(image=self.dashboard_icon_extended)

            self.add_listing_btn.place_configure(x=25, y=182, width=167, height=36)
            self.add_listing_btn.config(image=self.donate_extended)

            self.schedule_pickup_btn.place_configure(x=23, y=250, width=167, height=56.0)
            self.schedule_pickup_btn.config(image=self.pickup_extended)

            self.community_btn.place_configure(x=31, y=335, width=167, height=32)
            self.community_btn.config(image=self.community_icon_extended)

            self.notifications_btn.place_configure(x=32, y=415, width=167, height=26)
            self.notifications_btn.config(image=self.notifications_icon_extended)  

    def collapse_sidebar(self, event):
        for button in [self.dashboard_btn, self.add_listing_btn, self.schedule_pickup_btn, self.notifications_btn,self.community_btn,]:
            self.canvas.configure(width=75)
            self.logo_btn.place_configure(x=0, y=0, width=75, height=75)
            self.logo_btn.config(image=self.collaped_logo)

            #Buttons
            self.dashboard_btn.place_configure(x=19.5, y=115, width=35, height=35)
            self.dashboard_btn.config(image=self.dashboard_icon_collapsed)

            self.add_listing_btn.place_configure(x=19.5, y=182, width=36, height=36)
            self.add_listing_btn.config(image=self.donate_icon_collapsed)
            
            self.schedule_pickup_btn.place_configure(x=9.5, y=250, width=56, height=56.0)
            self.schedule_pickup_btn.config(image=self.pickup_icon_collapsed)

            self.community_btn.place_configure(x=21, y=326, width=32, height=32)
            self.community_btn.config(image=self.community_Icon_collapsed)

            self.notifications_btn.place_configure(x=24.5, y=420, width=26, height=26)
            self.notifications_btn.config(image=self.notifications_icon_collapsed)

    def toggle(self, event=None):
        """Toggle between states."""
        self.state = not self.state  # Switch state

        if self.state:  # Admin state
            # Update to "Admin" background image
            self.toggle_canvas.itemconfig(self.bg_item, image=self.bg_image_admin)

            # Move the toggle circle to the right (Admin position)
            self.toggle_canvas.coords(self.toggle_circle, 76, 16, 98, 40)  # Adjusted for 24x24 circle

        else:  # User state
            # Update to "User" background image
            self.toggle_canvas.itemconfig(self.bg_item, image=self.bg_image_user)

            # Move the toggle circle to the left (User position)
            self.toggle_canvas.coords(self.toggle_circle, 32, 16, 55, 40)  # Adjusted for 24x24 circle
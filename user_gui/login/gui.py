from pathlib import Path
from tkinter import Toplevel, Canvas, Entry, Button, PhotoImage, messagebox, Label,IntVar
from tkinter import PhotoImage, Label
from PIL import ImageTk, Image
from controller import *
from ..main_window.main import mainWindow
import hashlib
import customtkinter as ctk  
import random
from utils import send_email,validation,get_user_info,center_window
import datetime
from cryptography.fernet import Fernet
import os
import threading
import time


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

KEY_FILE = "key.key"
PREFERENCES_FILE = "preferences.txt"


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def loginWindow():

    Login()

def toggle_password_visibility(entry, icon_label):
    # Preload images using CTkImage
    eye_closed_image = ctk.CTkImage(light_image=Image.open(relative_to_assets("eye_closed.png")),
                                    dark_image=Image.open(relative_to_assets("eye_closed.png")), size=(20, 20))
    eye_open_image = ctk.CTkImage(light_image=Image.open(relative_to_assets("eye_open.png")),
                                dark_image=Image.open(relative_to_assets("eye_open.png")), size=(20, 20))
    """Toggle password visibility."""
    if entry.cget("show") == "•":
        entry.configure(show="")  # Show password
        icon_label.configure(image=eye_open_image)  # Switch to open eye
    else:
        entry.configure(show="•")  # Hide password
        icon_label.configure(image=eye_closed_image)  # Switch to closed eye

class Login(Toplevel):

    global user

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.title("Login - Local Food Sharing App")
        self.geometry("1012x506")
        self.configure(bg="#5E95FF")
        center_window(self,1012,506)


        def generate_key():
            if not os.path.exists(KEY_FILE):
                key = Fernet.generate_key()
                with open(KEY_FILE, "wb") as key_file:
                    key_file.write(key)

        def load_key():
            with open(KEY_FILE, "rb") as key_file:
                return key_file.read()

        # Ensure encryption key exists
        generate_key()
        encryption_key = load_key()
        self.cipher_suite = Fernet(encryption_key)

        # Left Section with Canvas
        self.left_canvas = Canvas(
            self,
            bg="#5E95FF",
            height=506,
            width=506,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.left_canvas.place(x=0, y=0)

        self.background_image = PhotoImage(file=relative_to_assets("logo.png"))  # Replace with your image path
        self.left_canvas.create_image(150, 75, anchor="nw", image=self.background_image)

        # Text for typing effect
        self.full_text = "Local Food Sharing"
        self.text_index = 0
        self.displayed_text = ""

        # Placeholder for typing effect text
        self.canvatext1 = self.left_canvas.create_text(
            170.0,
            50.0,
            anchor="nw",
            text=self.displayed_text,
            fill="#FFFFFF",
            font=("Montserrat Bold", 25 * -1, "bold"),
        )

        # Static text lines
        self.static_text_lines = [
            "The Local Food Sharing App connects communities enabling the",
            "distribution of excess food to those in need. Manage food do-",
            "-nations, pickups, and notifications through an easy-to-use",
            "platform."
        ]
        self.current_line = 0
        self.static_text_y = 350  # Starting Y position for static text

        # Start typing effect for heading
        self.typing_effect()

         # Right Section
        self.right_frame = ctk.CTkFrame(self, width=506, height=506, corner_radius=0, fg_color= '#5E95FF')
        #'#5E95FF'
        self.right_frame.place(x=506, y=0)

        self.display_login()

        # Essentials
        self.resizable(False, False)
        self.mainloop()

    def typing_effect(self):
        # Typing effect for the main title
        if self.text_index < len(self.full_text):
            # Add the next character to the displayed text
            self.displayed_text += self.full_text[self.text_index]
            self.text_index += 1

            # Update the text on the canvas
            self.left_canvas.itemconfig(self.canvatext1, text=self.displayed_text)

            # Schedule the next character to appear
            self.after(10, self.typing_effect)  # Adjust delay for typing speed
        else:
            # Once typing effect for the title is done, start typing static text lines
            self.current_line = 0  # Initialize the current line index
            self.static_typing_text = ""  # Initialize empty string for typing static lines
            self.char_index = 0  # Initialize character index for static lines
            self.after(500, self.show_static_text_line_by_line)  # Small delay before static text

    def show_static_text_line_by_line(self):
        # Typing effect for static lines
        if self.current_line < len(self.static_text_lines):
            line = self.static_text_lines[self.current_line]

            if self.char_index < len(line):
                # Add the next character to the displayed line
                self.static_typing_text += line[self.char_index]
                self.char_index += 1

                # Update the text on the canvas
                if self.char_index == 1:  # Create text only for the first character
                    self.text_id = self.left_canvas.create_text(
                        70.0,
                        self.static_text_y,
                        anchor="nw",
                        text=self.static_typing_text,
                        fill="#FFFFFF",
                        font=("Montserrat Regular", 14 * -1),
                    )
                else:  # Update the existing line
                    self.left_canvas.itemconfig(self.text_id, text=self.static_typing_text)

                # Schedule the next character
                self.after(5, self.show_static_text_line_by_line)  # Typing speed
            else:
                # Move to the next line
                self.current_line += 1
                self.static_text_y += 29  # Adjust Y position for the next line
                self.static_typing_text = ""  # Reset typed text for the next line
                self.char_index = 0  # Reset character index
                self.after(50, self.show_static_text_line_by_line)  # Delay before next line
        else:
            pass

    def generate_key():
        if not os.path.exists(KEY_FILE):
            key = Fernet.generate_key()
            with open(KEY_FILE, "wb") as key_file:
                key_file.write(key)

    def load_key():
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    
    def display_login(self):
        """Render the Login view."""
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Add a fixed background frame
        background_frame = ctk.CTkFrame(
            self.right_frame,
            width=450,
            height=450,
            corner_radius=25,
            fg_color="#FFFFFF",

        )
        background_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        login_title = ctk.CTkLabel(
            background_frame,
            text="Welcome to the Community!",
            font=("Montserrat Bold", 22,"bold"),
            text_color="#5E95FF",
        )
        login_title.place(relx=0.5, y=45, anchor="center")

        # Subtitle
        login_subtitle = ctk.CTkLabel(
            background_frame,
            text="Join us in sharing, giving, and making a difference!",
            font=("Montserrat", 12, "bold"),
            text_color="#333333",
        )
        login_subtitle.place(relx=0.5, y=80, anchor="center")

        login_sub_subtitle = ctk.CTkLabel(
            background_frame,
            text="Please continue Login or SignUp",
            font=("Montserrat", 12),
            text_color="#666666",
        )
        login_sub_subtitle.place(relx=0.5, y=115, anchor="center")

        # Email entry
        self.email_label = ctk.CTkLabel(
            background_frame,
            text="Email*",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.email_label.place(x=70, y=130)

        self.username = ctk.CTkEntry(
            background_frame,
            width=300,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter your email",
        )
        self.username.place(x=70, y=165)

        # Password entry
        self.password_label = ctk.CTkLabel(
            background_frame,
            text="Password*",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.password_label.place(x=70, y=200)

        self.password = ctk.CTkEntry(
            background_frame,
            width=300,  # Adjusted width for eye icon placement
            font=("Montserrat", 14),
            corner_radius=10,
            show="•",
            placeholder_text="Enter your password",
        )
        self.password.place(x=70, y=225)

        # Preload images using CTkImage
        eye_closed_image = ctk.CTkImage(light_image=Image.open(relative_to_assets("eye_closed.png")),
                                        dark_image=Image.open(relative_to_assets("eye_closed.png")), size=(20, 20))
        eye_open_image = ctk.CTkImage(light_image=Image.open(relative_to_assets("eye_open.png")),
                                    dark_image=Image.open(relative_to_assets("eye_open.png")), size=(20, 20))

        # Eye icon for toggling password visibility
        eye_icon = ctk.CTkLabel(
            background_frame,
            image=eye_closed_image,  # Use preloaded CTkImage for the closed eye
            text="",  # No text for the label
        )
        eye_icon.place(x=380, y=225)  # Place beside the password entry

        # Bind toggle function to the eye icon
        eye_icon.bind("<Button-1>", lambda e: toggle_password_visibility(self.password, eye_icon))

        # Forgot Password Link
        forgot_password_link = ctk.CTkLabel(
            background_frame,
            text="Forgot Password?",
            font=("Montserrat", 12),
            text_color="#007BFF",
            cursor="hand2",
        )
        forgot_password_link.place(x=70, y=255)
        forgot_password_link.bind("<Button-1>", lambda e: self.display_forgot_password())
        
        self.remember_var = IntVar() 
        self.remember_me=ctk.CTkCheckBox(
            background_frame,
            text='',
            checkmark_color="white",
            border_color="grey" ,
            checkbox_width=20,  
            checkbox_height=20,  
            border_width=2,
            variable=self.remember_var
        )
        self.remember_me.place(x=70, y=290)

        remeber_me_label = ctk.CTkLabel(
            background_frame,
            text="Remember Me",
            font=("Montserrat", 12),
            text_color="#007BFF",
        )
        remeber_me_label.place(x=100, y=287)

        # Login button
        self.login_button = ctk.CTkButton(
            background_frame,
            text="Login",
            command=self.loginFunc,
            width=300,
            height=40,
            corner_radius=20,
            fg_color="#5E95FF",
            hover_color="#417BFF",
            font=("Montserrat Bold", 14),
        )
        self.login_button.place(x=70, y=327)

        # Signup link
        signup_link = ctk.CTkLabel(
            background_frame,
            text="Don't have an account? Sign Up",
            font=("Montserrat", 12),
            text_color="#007BFF",
            cursor="hand2",
        )
        signup_link.place(x=125, y=370)
        signup_link.bind("<Button-1>", lambda e: self.display_signup())

        # Contact Support
        contactus_link = ctk.CTkLabel(
            background_frame,
            text="Still facing trouble? Contact Us!",
            font=("Montserrat Bold", 12),  
            text_color="#007BFF",
            cursor="hand2",
        )
        contactus_link.place(x=125, y=400)
        contactus_link.bind("<Button-1>", lambda e: self.contactus())

        copyright_label=ctk.CTkLabel(
            background_frame,
            text="Copyright 2024 Local Food Sharing Inc - All Rights Recieved",
            font=("Montserrat", 10),  
            text_color="grey",
        )
        copyright_label.place(x=75, y=425)

        # Load Preferences
        self.load_preferences()

    def load_preferences(self):
        try:
            with open(PREFERENCES_FILE, "r") as file:
                lines = file.readlines()
                username = lines[0].strip()
                encrypted_password = lines[1].strip()
                remember_me = int(lines[2].strip())

                # Populate the fields with decrypted data
                self.username.insert(0, username)
                decrypted_password = self.cipher_suite.decrypt(encrypted_password.encode()).decode()
                self.password.insert(0, decrypted_password)
                self.remember_var.set(remember_me)
        except (FileNotFoundError, IndexError):
            pass

    def save_preferences(self, username, password):
        """Save the username and encrypted password to a file."""
        encrypted_password = self.cipher_suite.encrypt(password.encode()).decode()  # Encrypt password
        with open(PREFERENCES_FILE, "w") as file:
            file.write(f"{username}\n")
            file.write(f"{encrypted_password}\n")
            file.write(f"{self.remember_var.get()}")  # Save the checkbox state

    def clear_preferences(self):
        """Clear the preferences file."""
        with open(PREFERENCES_FILE, "w") as file:
            file.truncate()  # Empty the file

    def send_otp_func(self):
        email = self.forgot_email.get().strip()
        get_user=get_user_info(email)
        email_validate=validation(email=email)
        if email_validate=="Invalid email address!" or email=="":
            self.forgot_email.configure(border_color="red",text_color="red")
            self.email_label.configure(text=f"Email ({email_validate})",text_color="red",font=("Montserrat", 12))
            return
        
        elif get_user is None:
            self.forgot_email.configure(border_color="red",text_color="red")
            self.email_label.configure(text=f"Email (Ops! User not found! Try again or Sign up)",text_color="red",font=("Montserrat", 12))
            return

    
        try:
            # Generate a 6-digit OTP
            otp = str(random.randint(100000, 999999))

            # Store OTP in memory for later validation
            self.generated_otp = otp
            subject = "Your OTP for Password Reset"

            body = f"""
            Hi,

            Your One-Time Password (OTP) for resetting your password is: {otp}

            If you did not request this, please ignore this email.

            Regards,
            Local Food Sharing App
            """
            
            send_email(email,subject,body) 

            # Notify the user
            self.forgot_email.configure(border_color="green",text_color="black",state="disabled",fg_color="lightgrey")
            self.email_label.configure(text=f"Email",text_color="green",font=("Montserrat", 14))
            self.send_otp_button.configure(text="OTP Sent!",fg_color="green",state="disabled")
            self.confirm_otp_button.configure(state="enable")
            self.otp_entry.configure(fg_color="white",state="normal",placeholder_text="Enter OTP")

            
        except Exception as e:
            print(f"Error sending OTP: {e}")
            messagebox.showerror("Error", "Failed to send OTP. Please try again later.")

    def confirm_otp_func(self):
        otp = self.otp_entry.get().strip()
        if not otp:
            self.email_label.configure(text=f"Email",text_color="#5E95FF",font=("Montserrat", 14))
            self.otp_entry.configure(border_color="red",text_color="red")
            self.otp_label.configure(text_color="red",font=("Montserrat", 12))
            self.send_otp_button.configure(text="Resend OTP",state="enable",fg_color="#5E95FF")
            return
        elif otp != getattr(self, "generated_otp", None):
            self.otp_entry.configure(border_color="red",text_color="red")
            self.email_label.configure(text=f"Email",text_color="#5E95FF",font=("Montserrat", 14))
            self.otp_label.configure(text_color="red",font=("Montserrat", 12))
            self.send_otp_button.configure(text="Resend OTP",state="enable",fg_color="#5E95FF")
            return
        self.otp_entry.configure(border_color="green",text_color="black",state="disabled",fg_color="lightgrey")
        self.otp_label.configure(text="OTP Verifed!.",text_color="green",font=("Montserrat", 12))
        self.confirm_otp_button.configure(text="Verified!",fg_color="green",state="disabled")
        self.reset_password_button.configure(state="enable")
        self.confirm_password.configure(state="normal",fg_color="white",placeholder_text="Enter Confirm Password")
        self.new_password.configure(state="normal",fg_color="white",placeholder_text="Enter New Password")
        
    def reset_password_func(self):
        email=self.forgot_email.get()
        new_password = self.new_password.get().strip()
        confirm_password = self.confirm_password.get().strip()
        validated_password=validation(password=new_password)
        if email=="":
            self.forgot_email.configure(border_color="red",text_color="red")
            self.email_label.configure(text=f"Email (Required)*",text_color="red",font=("Montserrat", 12))
            return
        if validated_password is not None or validated_password=="":
            self.new_password.configure(border_color="red",text_color="red")
            self.new_password_label.configure(text=f"New Password {validated_password}",text_color="red",font=("Montserrat", 12))
            return
        elif not confirm_password:
            self.confirm_password.configure(border_color="red",text_color="red")
            self.confirm_password_label.configure(text_color="red",font=("Montserrat", 12))
        if new_password != confirm_password:
            self.confirm_password.configure(border_color="red",text_color="red")
            self.confirm_password_label.configure(text="Confirm Pasword  (Didn't Match! Try again)",text_color="red",font=("Montserrat", 12))
            return
        self.hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        updatePassword(email,self.hashed_password)
        # Simulate password reset logic (replace with actual backend logic)
        messagebox.showinfo("Password Reset", "Your password has been reset successfully!")
        self.display_login()

    def display_forgot_password(self):
        """Render the Forgot Password view with OTP and password reset functionality."""
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Add a fixed background frame
        background_frame = ctk.CTkFrame(
            self.right_frame,
            width=450,
            height=450,
            corner_radius=15,
            fg_color="white",
        )
        background_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Back Button
        #button for back to login page
        back_image = ctk.CTkImage(light_image=Image.open(relative_to_assets("left_arrow.png")),
                                    dark_image=Image.open(relative_to_assets("left_arrow.png")), size=(40, 40))
        back_icon = ctk.CTkLabel(
            background_frame,
            image=back_image,  
            text="",  
        )
        back_icon.place(x=25, y=15)
        back_icon.bind("<Button-1>", lambda e: self.display_login()) # Bind Back function to the Back icon

        # Title
        forgot_title = ctk.CTkLabel(
            background_frame,
            text="Reset Password",
            font=("Montserrat Bold", 26),
            text_color="#333333",
        )
        forgot_title.place(relx=0.5, y=35, anchor="center")

        # Email entry
        self.email_label = ctk.CTkLabel(
            background_frame,
            text="Email",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.email_label.place(x=50, y=70)

        self.forgot_email = ctk.CTkEntry(
            background_frame,
            width=200,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter your email",
        )
        self.forgot_email.place(x=50, y=100)

        self.send_otp_button = ctk.CTkButton(
            background_frame,
            text="Send OTP",
            command=self.send_otp_func,
            width=120,
            height=40,
            corner_radius=10,
            fg_color="#5E95FF",
            hover_color="#417BFF",
            font=("Montserrat Bold", 12),
        )
        self.send_otp_button.place(x=260, y=96)

        # OTP entry
        self.otp_label = ctk.CTkLabel(
            background_frame,
            text="Enter (One Time Passcode)",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.otp_label.place(x=50, y=140)

        self.otp_entry = ctk.CTkEntry(
            background_frame,
            width=200,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter OTP",
            state="disabled",
            fg_color="lightgrey"
        )
        self.otp_entry.place(x=50, y=170)

        self.confirm_otp_button = ctk.CTkButton(
            background_frame,
            text="Confirm OTP",
            command=self.confirm_otp_func,
            width=120,
            height=40,
            corner_radius=10,
            fg_color="#5E95FF",
            hover_color="#417BFF",
            font=("Montserrat Bold", 12),
            state="disabled"
        )
        self.confirm_otp_button.place(x=260, y=165)

        # New password entry
        self.new_password_label = ctk.CTkLabel(
            background_frame,
            text="New Password",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.new_password_label.place(x=50, y=220)

        self.new_password = ctk.CTkEntry(
            background_frame,
            width=300,
            font=("Montserrat", 14),
            corner_radius=10,
            show="•",
            placeholder_text="Enter new password",
            state="disabled",
            fg_color="lightgrey"
        )
        self.new_password.place(x=50, y=250)

        #Show Password images 
        eye_closed_image = ctk.CTkImage(light_image=Image.open(relative_to_assets("eye_closed.png")),
                                        dark_image=Image.open(relative_to_assets("eye_closed.png")), size=(20, 20))
        eye_open_image = ctk.CTkImage(light_image=Image.open(relative_to_assets("eye_open.png")),
                                    dark_image=Image.open(relative_to_assets("eye_open.png")), size=(20, 20))

        # Eye icon for toggling new password visibility
        eye_icon_new = ctk.CTkLabel(
            background_frame,
            image=eye_closed_image,  # Use preloaded CTkImage for the closed eye
            text="",  # No text for the label
        )
        eye_icon_new.place(x=360, y=250)  # Place beside the password entry

        # Bind toggle function to the eye icon
        eye_icon_new.bind("<Button-1>", lambda e: toggle_password_visibility(self.new_password, eye_icon_new))

        self.confirm_password_label = ctk.CTkLabel(
            background_frame,
            text="Confirm Password",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.confirm_password_label.place(x=50, y=290)

        self.confirm_password = ctk.CTkEntry(
            background_frame,
            width=300,
            font=("Montserrat", 14),
            corner_radius=10,
            show="•",
            placeholder_text="Re-enter new password",
            state="disabled",
            fg_color="lightgrey"
        )
        self.confirm_password.place(x=50, y=320)

        # Eye icon for toggling confirm password visibility
        eye_icon_confirm = ctk.CTkLabel(
            background_frame,
            image=eye_closed_image,  # Use preloaded CTkImage for the closed eye
            text="",  # No text for the label
        )
        eye_icon_confirm.place(x=360, y=320)  # Place beside the password entry

        # Bind toggle function to the eye icon
        eye_icon_confirm.bind("<Button-1>", lambda e: toggle_password_visibility(self.confirm_password, eye_icon_confirm))

        self.reset_password_button = ctk.CTkButton(
            background_frame,
            text="Reset Password",
            command=self.reset_password_func,
            width=300,
            height=40,
            corner_radius=20,
            fg_color="#5E95FF",
            hover_color="#417BFF",
            font=("Montserrat Bold", 14),
            state="disabled"
        )
        self.reset_password_button.place(x=50, y=370)
        
        copyright_label=ctk.CTkLabel(
            background_frame,
            text="Copyright 2024 Local Food Sharing Inc - All Rights Recieved",
            font=("Montserrat", 10),  
            text_color="grey",
        )
        copyright_label.place(x=75, y=425)

    def display_signup(self):
        """Render the Sign Up view."""
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Add a fixed background frame
        background_frame = ctk.CTkFrame(
            self.right_frame,
            width=450,
            height=450,
            corner_radius=15,
            fg_color="white",
        )
        background_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Back Button
        #button for back to login page
        back_image = ctk.CTkImage(light_image=Image.open(relative_to_assets("left_arrow.png")),
                                    dark_image=Image.open(relative_to_assets("left_arrow.png")), size=(40, 40))
        back_icon = ctk.CTkLabel(
            background_frame,
            image=back_image,  
            text="",  
        )
        back_icon.place(x=25, y=15)
        back_icon.bind("<Button-1>", lambda e: self.display_login()) # Bind Back function to the Back icon


        # Title
        signup_title = ctk.CTkLabel(
            background_frame,
            text="Create Your Account",
            font=("Montserrat Bold", 26),
            text_color="#333333",
        )
        signup_title.place(relx=0.5, y=50, anchor="center")

        # First Name
        self.first_name_label = ctk.CTkLabel(
            background_frame,
            text="First Name*",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.first_name_label.place(x=70, y=80)

        self.first_name = ctk.CTkEntry(
            background_frame,
            width=140,
            font=("Montserrat", 12),
            corner_radius=10,
            placeholder_text="Enter your first name",
        )
        self.first_name.place(x=70, y=110)

        # Last Name
        self.last_name_label = ctk.CTkLabel(
            background_frame,
            text="Last Name*",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.last_name_label.place(x=240, y=80)

        self.last_name = ctk.CTkEntry(
            background_frame,
            width=140,
            font=("Montserrat", 12),
            corner_radius=10,
            placeholder_text="Enter your last name",
        )
        self.last_name.place(x=240, y=110)

        # Email
        self.email_label = ctk.CTkLabel(
            background_frame,
            text="Email*",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.email_label.place(x=70, y=150)

        self.username = ctk.CTkEntry(
            background_frame,
            width=300,
            font=("Montserrat", 12),
            corner_radius=10,
            placeholder_text="Enter your email",
        )
        self.username.place(x=70, y=180)

        # Password
        self.password_label = ctk.CTkLabel(
            background_frame,
            text="Password*",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.password_label.place(x=70, y=220)

        self.password = ctk.CTkEntry(
            background_frame,
            width=300,
            font=("Montserrat", 12),
            corner_radius=10,
            show="•",
            placeholder_text="Enter your password",
        )
        self.password.place(x=70, y=250)

        # Preload images using CTkImage
        eye_closed_image = ctk.CTkImage(light_image=Image.open(relative_to_assets("eye_closed.png")),
                                        dark_image=Image.open(relative_to_assets("eye_closed.png")), size=(20, 20))
        eye_open_image = ctk.CTkImage(light_image=Image.open(relative_to_assets("eye_open.png")),
                                    dark_image=Image.open(relative_to_assets("eye_open.png")), size=(20, 20))

        # Eye icon for toggling password visibility
        eye_icon = ctk.CTkLabel(
            background_frame,
            image=eye_closed_image,  # Use preloaded CTkImage for the closed eye
            text="",  # No text for the label
        )
        eye_icon.place(x=375, y=250)  # Place beside the password entry

        # Bind toggle function to the eye icon
        eye_icon.bind("<Button-1>", lambda e: toggle_password_visibility(self.password, eye_icon))

        
        self.terms_checkbox=ctk.CTkCheckBox(
            background_frame,
            text='',
            checkmark_color="white",
            border_color="grey" ,
            state="disable"
        )
        self.terms_checkbox.place(x=70, y=300)

        
        self.terms_label = ctk.CTkLabel(
            background_frame,
            text="Yes, I agree to the",
            font=("Montserrat Bold", 12),
            text_color="black",
        )
        self.terms_label.place(x=110, y=300)

        terms_link= ctk.CTkLabel(
            background_frame,
            text="Terms of service.",
            font=("Montserrat", 12),
            text_color="#007BFF",
            cursor="hand2",
        )
        terms_link.place(x=220, y=300)
        terms_link.bind("<Button-1>", lambda e: self.termsfunc())

        # Signup button
        signup_button = ctk.CTkButton(
            background_frame,
            text="Sign Up",
            command=self.signupFunc,
            width=300,
            height=40,
            corner_radius=20,
            fg_color="#5E95FF",
            hover_color="#417BFF",
            font=("Montserrat Bold", 14),
        )
        signup_button.place(x=70, y=340)
        # Back to login link
        login_link = ctk.CTkLabel(
            background_frame,
            text="Already have an account? Login",
            font=("Montserrat", 12),
            text_color="#007BFF",
            cursor="hand2",
        )
        login_link.place(x=120, y=390)
        login_link.bind("<Button-1>", lambda e: self.display_login())

        copyright_label=ctk.CTkLabel(
            background_frame,
            text="Copyright 2024 Local Food Sharing Inc - All Rights Recieved",
            font=("Montserrat", 10),  
            text_color="grey",
        )
        copyright_label.place(x=75, y=425)

    def hash_password(self, password):
        """
        Hashes a password using SHA-256 for secure storage and comparison.
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    
    def termsfunc(self):

        self.terms_window=ctk.CTkToplevel(self, width=706, height=450, fg_color= 'white'

        )
        self.terms_window.title("Terms and Conditions")
        self.terms_window.geometry("506X350")
        
        center_window(self.terms_window, 706, 450)
            # Add text for Terms and Conditions
        terms_text = ctk.CTkTextbox(
        self.terms_window,
        wrap="word",  # Enable text wrapping
        height=350,
        fg_color="white",
        width=606,
        font=("Montserrat", 12),
        )
        terms_text.pack(pady=20, padx=20)

            # Terms and Conditions Content
        terms_content = """
                                                                TERMS AND CONDITIONS

Last Updated: November 28, 2024

Welcome to Local Food Sharing!

These terms and conditions outline the rules and regulations for the use of Local Food Sharing's services, available through the application operated by LFG. By accessing or using our services, you accept these terms and conditions in full. Do not continue to use Local Food Sharing if you do not agree to all the terms and conditions stated here.

1. DEFINITIONS
- "Application" refers to Local Food Sharing, including all its content, features, and services.
- "User" refers to any individual or entity accessing or using the application.
- "We", "Us", and "Our" refer to LFG.

2. USER RESPONSIBILITIES
- Eligibility: You must be at least 18 years of age or have the permission of a legal guardian to use our application.
- Account Information: You are responsible for maintaining the confidentiality of your account credentials. Any activity under your account is your responsibility.
- Prohibited Activities: Users are prohibited from:
    - Uploading harmful, malicious, or illegal content.
    - Attempting to hack, disrupt, or interfere with the application's functionality.
    - Violating the rights of others, including intellectual property and privacy rights.

3. PRIVACY POLICY
By using our application, you agree to our Privacy Policy, which outlines how we collect, use, and protect your personal information. You can contact us for more information.

4. INTELLECTUAL PROPERTY
All content and features available on the application, including text, graphics, logos, icons, and software, are the property of LFG or its licensors and are protected by applicable copyright, trademark, and other intellectual property laws. Unauthorized use of this content is strictly prohibited.

5. LIMITATION OF LIABILITY
To the maximum extent permitted by law:
- LFG shall not be held responsible for any damages, losses, or liabilities arising from the use of the application.
- The application is provided "as is," without any warranties, express or implied, including fitness for a particular purpose or non-infringement.

6. TERMINATION OF USE
We reserve the right to terminate or suspend your access to the application at any time, without prior notice, for conduct that we believe violates these Terms and Conditions or is otherwise harmful to other users or the application.

7. CHANGES TO TERMS
We may revise these Terms and Conditions at any time. Users will be notified of updates, and continued use of the application constitutes acceptance of the revised terms.

8. GOVERNING LAW
These terms shall be governed by and interpreted in accordance with the laws of the USA, Michigan. Any disputes arising from these terms shall be resolved exclusively in the courts of Michigan.

9. CONTACT US
If you have any questions about these Terms and Conditions, you can contact us at:

- Email: localfoodsharing@gmail.com

AGREEMENT

By clicking "Accept" or using the application, you confirm that you have read, understood, and agree to these Terms and Conditions.
        """

        # Insert content into the textbox
        terms_text.insert("1.0", terms_content)
        terms_text.configure(state="disabled")  # Make the text read-only

        accept_button = ctk.CTkButton(
            self.terms_window,
            text="Accept",
            command=self.terms_accepted,
            width=100,
            height=40,
            corner_radius=20,
            fg_color="#5E95FF",
            hover_color="#417BFF",
            font=("Montserrat Bold", 14),
        )
        accept_button.place(x=570, y=380)

        decline_button = ctk.CTkButton(
            self.terms_window,
            text="Decline",
            command=self.terms_declined,
            width=100,
            height=40,
            corner_radius=20,
            fg_color="#5E95FF",
            hover_color="#417BFF",
            font=("Montserrat Bold", 14),
        )
        decline_button.place(x=50, y=380)

    def terms_accepted(self):
        self.terms_checkbox.select()
        self.terms_window.withdraw()
        
    def terms_declined(self):

        self.terms_window.withdraw()
        self.terms_checkbox.deselect()
        self.terms_checkbox.configure(border_color='red')

    def loginFunc(self):
        """Handles the user login logic."""
        global user
        try:
            # Retrieve and validate the email and password
            email = self.username.get().strip()
            raw_password = self.password.get().strip()
            remember_me=self.remember_var.get()

        # Validate email format
            get_user=get_user_info(email)
            email_validate=validation(email=email)
            if email_validate=="Invalid email address!" or email=="":
                self.username.configure(border_color="red",text_color="red")
                self.email_label.configure(text=f"Email ({email_validate})",text_color="red",font=("Montserrat", 12))
                return
            
            elif get_user is None:
                self.username.configure(border_color="red",text_color="red")
                self.email_label.configure(text=f"Email (Ops! User not found! Try again or Sign up.)",text_color="red",font=("Montserrat", 12))
                return
            else:
                self.username.configure(border_color="grey",text_color="black")
                self.email_label.configure(text="Email*",text_color="#5E95FF",font=("Montserrat", 14))

            if raw_password=="" or raw_password is None:
                self.password.configure(border_color="red",text_color="red")
                self.password_label.configure(text="Password*",text_color="red",font=("Montserrat", 12))
                return
            # Hash the entered password for comparison
            hashed_password = self.hash_password(raw_password)

            # Check the user in the database
            self.user_id = checkUser(email.lower(), hashed_password)
            if self.user_id:
                if remember_me:
                    self.save_preferences(email, raw_password)  # Save preferences if "Remember Me" is checked
                else:
                    self.clear_preferences()  # Clear preferences if "Remember Me" is unchecked

                self.loading_animation_running = False  # Tracks animation state
                self.loading_dots = ""  # Dots for animation

                self.start_loading()
                # Threading ensures the mainWindow loads in the background
                threading.Thread(target=self.load_main_window, daemon=True).start()

            else:
                self.password.configure(border_color="red",text_color="red")
                self.password_label.configure(text="Password  ('Forget Password?')",text_color="red",font=("Montserrat", 12))
                
        except Exception as e:
            messagebox.showerror(
                title="Login Error",
                message=f"An error occurred during login: {e}"
            )
    
    def start_loading(self):
        self.login_button.configure(state="disabled", text="Signing In...")
        self.loading_animation_running = True
        self.animate_dots()

    def animate_dots(self):
        if self.loading_animation_running:
            self.loading_dots = "." if self.loading_dots == "..." else self.loading_dots + "."
            self.login_button.configure(text=f"Signing In{self.loading_dots}", text_color_disabled="white")
            self.after(500, self.animate_dots)

    def load_main_window(self):
        try:
            time.sleep(2)  
            self.loading_animation_running = False  
            self.after(0, self.open_main_window)  #
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load main window: {e}")

    def open_main_window(self):
        self.destroy()  
        mainWindow(self.user_id)
        self.after(500, self.animate_dots)

    def signupFunc(self):
        """Handles the user signup logic."""
        first_name = self.first_name.get().strip()
        last_name = self.last_name.get().strip()
        email = self.username.get().strip()
        password = self.password.get().strip()
        terms=self.terms_checkbox.get()

        # Validate input fields
        name_validate=validation(name=first_name)
        if name_validate is not None:
            self.first_name.configure(border_color="red",text_color="red")
            self.first_name_label.configure(text_color="red",font=("Montserrat", 12))
            return
        else:
            self.first_name.configure(border_color="grey", text_color="black")
            self.first_name_label.configure(text_color="#5E95FF",font=("Montserrat", 14))
        #Last name validation
        name_validate=validation(name=last_name) 
        if name_validate is not None:
            self.last_name.configure(border_color="red",text_color="red")
            self.last_name_label.configure(text_color="red",font=("Montserrat", 12))
            return
        else:
            self.last_name.configure(border_color="grey", text_color="black")
            self.last_name_label.configure(text_color="#5E95FF",font=("Montserrat", 14))

        # Validate email format
        get_user=get_user_info(email)
        email_validate=validation(email=email)
        if email_validate is not None:
            self.username.configure(border_color="red",text_color="red")
            self.email_label.configure(text=f"Email ({email_validate})",text_color="red",font=("Montserrat", 12))
            return
        
        elif get_user is not None:
            self.username.configure(border_color="red",text_color="red")
            self.email_label.configure(text=f"Email (Email already exits, Try resetting Password)",text_color="red",font=("Montserrat", 12))
            return
        else:
            self.username.configure(border_color="grey",text_color="black")
            self.email_label.configure(text="Email*",text_color="#5E95FF",font=("Montserrat", 14))
        
        validated_password=validation(password=password)
        if validated_password is not None or validated_password=="":
            self.password.configure(border_color="red",text_color="red")
            self.password_label.configure(text=f"Password {validated_password}",text_color="red",font=("Montserrat", 12))
            return
        else:
           self.password.configure(border_color="grey",text_color="black")
           self.password_label.configure(text="Password*",text_color="#5E95FF",font=("Montserrat", 14))

        if not terms:
            self.terms_checkbox.configure(border_color='red')
            return

        # Hash the password before storing it in the database
        self.hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.user_verification(email,first_name,last_name,self.hashed_password)
        
    def resetPasswordFunc(self):
        """Handle the reset password functionality."""
        otp_type="Resetting_Password"
        
    def contactus(self):
        """Render the contact us view."""
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Add a fixed background frame
        background_frame = ctk.CTkFrame(
            self.right_frame,
            width=450,
            height=450,
            corner_radius=15,
            fg_color="white",
        )
        background_frame.place(relx=0.5, rely=0.5, anchor="center")

        #button for back to login page
        back_image = ctk.CTkImage(light_image=Image.open(relative_to_assets("left_arrow.png")),
                                    dark_image=Image.open(relative_to_assets("left_arrow.png")), size=(40, 40))
        back_icon = ctk.CTkLabel(
            background_frame,
            image=back_image,  
            text="",  
        )
        back_icon.place(x=25, y=15)  
        back_icon.bind("<Button-1>", lambda e: self.display_login()) # Bind Back function to the Back icon

        # Title
        contactus_title = ctk.CTkLabel(
            background_frame,
            text="Contact Us!",
            font=("Montserrat Bold", 26),
            text_color="#333333",
        )
        contactus_title.place(relx=0.5, y=30, anchor="center")
        
        # First Name
        self.first_name_label = ctk.CTkLabel(
            background_frame,
            text="First Name*",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.first_name_label.place(x=70, y=70)

        self.first_name = ctk.CTkEntry(
            background_frame,
            width=140,
            font=("Montserrat", 12),
            corner_radius=10,
            placeholder_text="Enter your first name",
        )
        self.first_name.place(x=70, y=100)

        # Last Name
        self.last_name_label = ctk.CTkLabel(
            background_frame,
            text="Last Name*",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.last_name_label.place(x=240, y=70)

        self.last_name = ctk.CTkEntry(
            background_frame,
            width=140,
            font=("Montserrat", 12),
            corner_radius=10,
            placeholder_text="Enter your last name",
        )
        self.last_name.place(x=240, y=100)

        # Email
        self.email_label = ctk.CTkLabel(
            background_frame,
            text="Email*",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.email_label.place(x=70, y=130)

        #Email Entry
        self.username = ctk.CTkEntry(
            background_frame,
            width=300,
            font=("Montserrat", 12),
            corner_radius=10,
            placeholder_text="Enter your email",
        )
        self.username.place(x=70, y=160)

        #Subject
        self.subject = ctk.CTkLabel(
            background_frame,
            text="Subject (Minimum 5 Words)*",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.subject.place(x=70, y=190)

        #Subject Entry
        self.subject_entry = ctk.CTkEntry(
            background_frame,
            width=300,
            font=("Montserrat", 12),
            corner_radius=10,
            placeholder_text="Enter your subject",
        )
        self.subject_entry.place(x=70, y=220)

        # Query
        self.query_label = ctk.CTkLabel(
            background_frame,
            text="What you want to tell us? (Minumum 15 words)*",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF"
         )
        self.query_label.place(x=70, y=250)

        self.query = ctk.CTkTextbox(
            background_frame,
            height=100,
            width=300,
            font=("Montserrat", 12),
            corner_radius=10,
            border_color="grey",
            border_width=2,

        )
        self.query.place(x=70, y=280)

        # Submit button
        submit = ctk.CTkButton(
            background_frame,
            text="Submit",
            command=self.submit_request,
            width=300,
            height=40,
            corner_radius=20,
            fg_color="#5E95FF",
            hover_color="#417BFF",
            font=("Montserrat Bold", 14),
        )
        submit.place(x=70, y=385)
        
        copyright_label=ctk.CTkLabel(
            background_frame,
            text="Copyright 2024 Local Food Sharing Inc - All Rights Recieved",
            font=("Montserrat", 8),  
            text_color="grey",
        )
        copyright_label.place(x=100, y=425)

    def submit_request(self):
        first_name=self.first_name.get().strip()
        last_name=self.last_name.get().strip()
        email=self.username.get().strip()
        body=self.query.get("1.0", "end-1c")
        subject=self.subject_entry.get().strip()
        ct = datetime.datetime.now()
        ticket_number = str(random.randint(100000, 999999))

        #NameValidation
        name_validation=validation(name=first_name)
        if name_validation is not None:
            self.first_name.configure(border_color="red",text_color="red")
            self.first_name_label.configure(text_color="red",font=("Montserrat", 12))  
            return  
        else:
            self.first_name.configure(border_color="grey", text_color="black")
            self.first_name_label.configure(text_color="#5E95FF",font=("Montserrat", 14))

        name_validation=validation(name=last_name)
        if name_validation is not None:
            self.last_name.configure(border_color="red",text_color="red")
            self.last_name_label.configure(text_color="red",font=("Montserrat", 12))  
            return  
        else:
            self.last_name.configure(border_color="grey", text_color="black")
            self.last_name_label.configure(text_color="#5E95FF",font=("Montserrat", 14))
        

        #Email Validation
        email_validation=validation(email=email)
        if email_validation is not None:
            self.username.configure(border_color="red",text_color="red")
            self.email_label.configure(text=f"Email ({email_validation})",text_color="red",font=("Montserrat", 12))
            return
        else:
            self.username.configure(border_color="grey",text_color="black")
            self.email_label.configure(text="Email*",text_color="#5E95FF",font=("Montserrat", 14))
        
        #Minmum word length
        body_words = body.split()
        subject_words=subject.split()
        
        if len(subject_words)<=5 or subject=='':
            self.subject_entry.configure(border_color="red",text_color="red")
            self.subject.configure(text_color="red",font=("Montserrat", 12)) 
            return
        elif len(body_words)<=10 or body=='':
            self.subject_entry.configure(border_color="grey",text_color="black")  
            self.subject.configure(text_color="black",font=("Montserrat", 12)) 
            self.query.configure(border_color="red",text_color="red")
            self.query_label.configure(text="What you want to tell us?* (Minumum 10 words)",text_color="red",font=("Montserrat", 12))  
            return

        else:
            self.query.configure(border_color="grey",text_color="black")
            self.query_label.configure(text="What you want to tell us?*",text_color="black",font=("Montserrat", 12))

        

        user_subject="Thanks for contacting us."
        
        user_body = f"""
        Hi {first_name} {last_name},

        Ticket ID: {ticket_number},
        Thanks for contacting TFS Support. We will get back to you within 24 Hours.

        Thanks,
        Local Food Sharing App
        """
        tech_subject=f"{self.subject_entry.get()} #{ticket_number} - {ct}"
        tech_body=f"""
        
        First Name: {first_name}
        Last Name: {last_name}
        Email:{email}
        Time_Requested: {ct}
        Request:
                {body}

        Thanks,
        Local Food Sharing App
        """

        user_emaail=send_email(email,user_subject,user_body)
        tech_email=send_email("localfoodsharing@gmail.com",tech_subject,tech_body)

        # Notify the user
        messagebox.showinfo('Sent!',"Request Submited! Typically recieve email within 24hrs")
        self.display_login()

    def user_verification(self, email,first_name,last_name,password):
        """Render the OTP verification view."""
        otp_type="Account_Verification"
        self.email = email  # Store the email for reuse
        self.first_name=first_name
        self.last_name=last_name
        self.password=self.hash_password(password)
        self.send_otp(otp_type,self.email)
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Add a fixed background frame
        background_frame = ctk.CTkFrame(
            self.right_frame,
            width=450,
            height=450,
            corner_radius=15,
            fg_color="white",
        )
        background_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Back Button
        #button for back to login page
        back_image = ctk.CTkImage(light_image=Image.open(relative_to_assets("left_arrow.png")),
                                    dark_image=Image.open(relative_to_assets("left_arrow.png")), size=(40, 40))
        back_icon = ctk.CTkLabel(
            background_frame,
            image=back_image,  
            text="",  
        )
        back_icon.place(x=25, y=15)
        back_icon.bind("<Button-1>", lambda e: self.display_signup()) # Bind Back function to the Back icon

        self.intro_image=Image.open("gui/login/assets/email.png")
        self.intro_image=self.intro_image.resize((120,120),Image.Resampling.LANCZOS)
        self.reference_intro_image=ImageTk.PhotoImage(self.intro_image)
        intro_label=Label(background_frame,image=self.reference_intro_image,justify='center',bg='white')
        intro_label.place(x=160, y=40)

        otp_heading_label1 = ctk.CTkLabel(
            background_frame,
            text="Enter your",
            font=("Montserrat Bold", 26),
            text_color="#333333",
        )
        otp_heading_label1.place(relx=0.5, y=170, anchor="center")

        otp_heading_label1 = ctk.CTkLabel(
            background_frame,
            text="Verification code",
            font=("Montserrat Bold", 26),
            text_color="#333333",
        )
        otp_heading_label1.place(relx=0.5, y=200, anchor="center")
    
        # OTP Label
        otp_label1 = ctk.CTkLabel(
            background_frame,
            text=f"We have send you One Time Passcode",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        otp_label1.place(x=90, y=235)
        otp_label2 = ctk.CTkLabel(
            background_frame,
            text=f"to this {email} email address",
            font=("Montserrat Bold", 13),
            text_color="#5E95FF",
        )
        otp_label2.place(x=100, y=255)

        # OTP Entry
        self.otp_entry = ctk.CTkEntry(
            background_frame,
            width=200,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter OTP",
        )
        self.otp_entry.place(x=130, y=300)

        # Send OTP Button
        send_otp_button = ctk.CTkButton(
            background_frame,
            text="Verify OTP",
            command=self.confirm_otp_func1,  # Reuse the same email
            width=120,
            height=40,
            corner_radius=10,
            fg_color="#5E95FF",
            hover_color="#417BFF",
            font=("Montserrat Bold", 12),
        )
        send_otp_button.place(x=160, y=340)

        # Resend OTP Button
        reset_otp_button = ctk.CTkButton(
            background_frame,
            text="Resend OTP",
            command=lambda: self.send_otp(otp_type,self.email),  # Resend OTP using the same email
            width=120,
            height=40,
            corner_radius=10,
            fg_color="#FF0000",  # Red color
            hover_color="#CC0000",
            font=("Montserrat Bold", 12),
        )
        reset_otp_button.place(x=160, y=390)

    def send_otp(self,type,email):
        self.type=type
        self.email=email
        try:
            # Generate a 6-digit OTP
            otp = str(random.randint(100000, 999999))

            # Store OTP in memory for later validation
            self.generated_otp = otp
            subject = f"Hurray! Your OTP for {self.type}"

            body = f"""
            Hi,

            Your One-Time Password (OTP) for {self.type} is: {otp}

            If you did not request this, please ignore this email.

            Regards,
            Local Food Sharing App
            """
            
            # Send the email using the stored email
            sending_email = send_email(email, subject, body)

        except Exception as e:
            print(f"Error sending OTP: {e}")
            messagebox.showerror("Error", "Failed to send OTP. Please try again later.")
        
    def confirm_otp_func1(self):
        otp = self.otp_entry.get().strip()
        if not otp:
            self.otp_entry.configure(border_color="red",text_color="red")
            return
        if otp != getattr(self, "generated_otp", None):
            self.otp_entry.configure(border_color="red",text_color="red")
            return
        messagebox.showinfo("OTP Verified", "OTP verified successfully!")
        if create_user(self.first_name, self.last_name, self.email, self.password):
            messagebox.showinfo("Sign Up", "Account Created Successfully!")
            self.display_login()
        else:
            messagebox.showerror("Error", "Failed to create account. Please try again!")

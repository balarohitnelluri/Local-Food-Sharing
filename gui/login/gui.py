from pathlib import Path
from tkinter import Toplevel, Canvas, Entry, Button, PhotoImage, messagebox, Label
from tkinter import PhotoImage, Label
from PIL import ImageTk, Image
from controller import *
from ..main_window.main import mainWindow
import hashlib
import customtkinter as ctk  # Install via pip install customtkinter
from CTkMessagebox import CTkMessagebox
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils import send_email,validation,get_user_info
import datetime


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

        # Left Section
        self.left_canvas = Canvas(
            self,
            bg="#1976D2",
            height=506,
            width=506,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.left_canvas.place(x=0, y=0)

        self.left_canvas.create_text(
            85.0,
            77.0,
            anchor="nw",
            text="Local Food Sharing",
            fill="#FFFFFF",
            font=("Montserrat Bold", 30 * -1),
        )
        self.left_canvas.create_text(
            85.0,
            150.0,
            anchor="nw",
            text="The Local Food Sharing App connects ",
            fill="#FFFFFF",
            font=("Montserrat Regular", 14 * -1),
        )
        self.left_canvas.create_text(
            85.0,
            179.0,
            anchor="nw",
            text="communities, enabling the distribution of ",
            fill="#FFFFFF",
            font=("Montserrat Regular", 14 * -1),
        )
        self.left_canvas.create_text(
            85.0,
            208.0,
            anchor="nw",
            text="excess food to those in need.Manage food ",
            fill="#FFFFFF",
            font=("Montserrat Regular", 14 * -1),
        )
        self.left_canvas.create_text(
            85.0,
            237.0,
            anchor="nw",
            text="donations, pickups, and notifications through",
            fill="#FFFFFF",
            font=("Montserrat Regular", 14 * -1),
        )

        self.left_canvas.create_text(
            85.0,
            266.0,
            anchor="nw",
            text=" an easy-to-use platform.",
            fill="#FFFFFF",
            font=("Montserrat Regular", 14 * -1),
        )

        image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        image_1 = self.left_canvas.create_image(460.0, 331.0, image=image_image_1)

        # Right Section
        self.right_frame = ctk.CTkFrame(self, width=506, height=506, corner_radius=0, fg_color= '#1976D2')
        #'#5E95FF'
        self.right_frame.place(x=506, y=0)

        self.display_login()

        # Essentials
        self.resizable(False, False)
        self.mainloop()

 

    def display_login(self):
        """Render the Login view."""
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

        # Title
        login_title = ctk.CTkLabel(
            background_frame,
            text="Welcome",
            font=("Montserrat Bold", 26),
            text_color="#333333",
        )
        login_title.place(relx=0.5, y=50, anchor="center")

        # Subtitle
        login_subtitle = ctk.CTkLabel(
            background_frame,
            text="Please log in to continue or Sign up",
            font=("Montserrat", 14),
            text_color="#666666",
        )
        login_subtitle.place(relx=0.5, y=90, anchor="center")

        # Email entry
        self.email_label = ctk.CTkLabel(
            background_frame,
            text="Email*",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.email_label.place(x=55, y=135)

        self.username = ctk.CTkEntry(
            background_frame,
            width=300,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter your email",
        )
        self.username.place(x=55, y=165)

        # Password entry
        self.password_label = ctk.CTkLabel(
            background_frame,
            text="Password*",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.password_label.place(x=55, y=200)

        self.password = ctk.CTkEntry(
            background_frame,
            width=300,  # Adjusted width for eye icon placement
            font=("Montserrat", 14),
            corner_radius=10,
            show="•",
            placeholder_text="Enter your password",
        )
        self.password.place(x=55, y=230)

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
        eye_icon.place(x=365, y=230)  # Place beside the password entry

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
        forgot_password_link.place(x=55, y=260)
        forgot_password_link.bind("<Button-1>", lambda e: self.display_forgot_password())

        # Login button
        login_button = ctk.CTkButton(
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
        login_button.place(x=55, y=300)

        # Signup link
        signup_link = ctk.CTkLabel(
            background_frame,
            text="Don't have an account? Sign Up",
            font=("Montserrat", 12),
            text_color="#007BFF",
            cursor="hand2",
        )
        signup_link.place(x=120, y=350)
        signup_link.bind("<Button-1>", lambda e: self.display_signup())

        # Contact Support
        contactus_link = ctk.CTkLabel(
            background_frame,
            text="Still facing trouble? Contact Us!",
            font=("Montserrat Bold", 12),  
            text_color="#007BFF",
            cursor="hand2",
        )
        contactus_link.place(x=120, y=390)
        contactus_link.bind("<Button-1>", lambda e: self.contactus())

    def send_otp_func(self):
        """Generate and send OTP to the provided email."""        
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
            self.forgot_email.configure(border_color="green",text_color="black")
            self.email_label.configure(text=f"Email",text_color="green",font=("Montserrat", 14))
            self.send_otp_button.configure(text="OTP Sent!",fg_color="green",state="disabled")

        except Exception as e:
            print(f"Error sending OTP: {e}")
            messagebox.showerror("Error", "Failed to send OTP. Please try again later.")

    def confirm_otp_func(self):
        otp = self.otp_entry.get().strip()
        if not otp:
            self.otp_entry.configure(border_color="red",text_color="red")
            self.otp_label.configure(text_color="red",font=("Montserrat", 12))
            return
        if otp != getattr(self, "generated_otp", None):
            self.otp_entry.configure(border_color="red",text_color="red")
            self.otp_label.configure(text_color="red",font=("Montserrat", 12))
            return
        self.otp_entry.configure(border_color="green",text_color="black")
        self.otp_label.configure(text="OTP Verifed!.",text_color="green",font=("Montserrat", 12))
        self.confirm_otp_button.configure(text="Verified!",fg_color="green",state="disabled")
        

    def reset_password_func(self):
        email=self.forgot_email.get()
        new_password = self.new_password.get().strip()
        confirm_password = self.confirm_password.get().strip()
        validated_password=validation(password=new_password)
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

        reset_password_button = ctk.CTkButton(
            background_frame,
            text="Reset Password",
            command=self.reset_password_func,
            width=300,
            height=40,
            corner_radius=20,
            fg_color="#5E95FF",
            hover_color="#417BFF",
            font=("Montserrat Bold", 14),
        )
        reset_password_button.place(x=50, y=370)

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
        self.first_name_label.place(x=50, y=80)

        self.first_name = ctk.CTkEntry(
            background_frame,
            width=140,
            font=("Montserrat", 12),
            corner_radius=10,
            placeholder_text="Enter your first name",
        )
        self.first_name.place(x=50, y=110)

        # Last Name
        self.last_name_label = ctk.CTkLabel(
            background_frame,
            text="Last Name*",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.last_name_label.place(x=220, y=80)

        self.last_name = ctk.CTkEntry(
            background_frame,
            width=140,
            font=("Montserrat", 12),
            corner_radius=10,
            placeholder_text="Enter your last name",
        )
        self.last_name.place(x=220, y=110)

        # Email
        self.email_label = ctk.CTkLabel(
            background_frame,
            text="Email*",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.email_label.place(x=50, y=150)

        self.username = ctk.CTkEntry(
            background_frame,
            width=300,
            font=("Montserrat", 12),
            corner_radius=10,
            placeholder_text="Enter your email",
        )
        self.username.place(x=50, y=180)

        # Password
        self.password_label = ctk.CTkLabel(
            background_frame,
            text="Password*",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        self.password_label.place(x=50, y=230)

        self.password = ctk.CTkEntry(
            background_frame,
            width=300,
            font=("Montserrat", 12),
            corner_radius=10,
            show="•",
            placeholder_text="Enter your password",
        )
        self.password.place(x=50, y=260)

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
        eye_icon.place(x=360, y=260)  # Place beside the password entry

        # Bind toggle function to the eye icon
        eye_icon.bind("<Button-1>", lambda e: toggle_password_visibility(self.password, eye_icon))

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
        signup_button.place(x=50, y=340)
        # Back to login link
        login_link = ctk.CTkLabel(
            background_frame,
            text="Already have an account? Login",
            font=("Montserrat", 12),
            text_color="#007BFF",
            cursor="hand2",
        )
        login_link.place(x=110, y=390)
        login_link.bind("<Button-1>", lambda e: self.display_login())

    def hash_password(self, password):
        """
        Hashes a password using SHA-256 for secure storage and comparison.
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def loginFunc(self):
        """Handles the user login logic."""
        global user
        try:
            # Retrieve and validate the email and password
            email = self.username.get().strip()
            raw_password = self.password.get().strip()

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
            user_id = checkUser(email.lower(), hashed_password)
            if user_id:
                user = email.lower()  # Save the user's email globally
                messagebox.showinfo(
                    title="Login Successful",
                    message=f"Welcome {user}!"
                )
                self.destroy()

                mainWindow(user_id)  # Pass the user_id to the main window
            else:
                self.password.configure(border_color="red",text_color="red")
                self.password_label.configure(text="Password  ('Forget Password?')",text_color="red",font=("Montserrat", 12))
                
        except Exception as e:
            messagebox.showerror(
                title="Login Error",
                message=f"An error occurred during login: {e}"
            )

    def signupFunc(self):
        """Handles the user signup logic."""
        first_name = self.first_name.get().strip()
        last_name = self.last_name.get().strip()
        email = self.username.get().strip()
        password = self.password.get().strip()

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
            text="Subject (Minimum 5 Words)",
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
            text="What you want to tell us?* (Minumum 20 words)",
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
        submit.place(x=70, y=390)

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

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
            bg="#5E95FF",
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
            90.0,
            150.0,
            anchor="nw",
            text="The Local Food Sharing App connects ",
            fill="#FFFFFF",
            font=("Montserrat Regular", 14 * -1),
        )
        self.left_canvas.create_text(
            90.0,
            179.0,
            anchor="nw",
            text="communities, enabling the distribution of ",
            fill="#FFFFFF",
            font=("Montserrat Regular", 14 * -1),
        )
        self.left_canvas.create_text(
            90.0,
            208.0,
            anchor="nw",
            text="excess food to those in need.Manage food ",
            fill="#FFFFFF",
            font=("Montserrat Regular", 14 * -1),
        )
        self.left_canvas.create_text(
            90.0,
            237.0,
            anchor="nw",
            text="donations, pickups, and notifications through",
            fill="#FFFFFF",
            font=("Montserrat Regular", 14 * -1),
        )

        self.left_canvas.create_text(
            90.0,
            266.0,
            anchor="nw",
            text=" an easy-to-use platform.",
            fill="#FFFFFF",
            font=("Montserrat Regular", 14 * -1),
        )

        image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        image_1 = self.left_canvas.create_image(452.0, 330.0, image=image_image_1)

        # Right Section
        self.right_frame = ctk.CTkFrame(self, width=506, height=506, corner_radius=0, fg_color= '#5E95FF')
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
            text="Welcome Back!",
            font=("Montserrat Bold", 26),
            text_color="#333333",
        )
        login_title.place(relx=0.5, y=50, anchor="center")

        # Subtitle
        login_subtitle = ctk.CTkLabel(
            background_frame,
            text="Please log in to continue",
            font=("Montserrat", 14),
            text_color="#666666",
        )
        login_subtitle.place(relx=0.5, y=90, anchor="center")

        # Email entry
        email_label = ctk.CTkLabel(
            background_frame,
            text="Email",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        email_label.place(x=50, y=150)

        self.username = ctk.CTkEntry(
            background_frame,
            width=300,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter your email",
        )
        self.username.place(x=50, y=180)

        # Password entry
        password_label = ctk.CTkLabel(
            background_frame,
            text="Password",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        password_label.place(x=50, y=230)

        self.password = ctk.CTkEntry(
            background_frame,
            width=300,  # Adjusted width for eye icon placement
            font=("Montserrat", 14),
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

        # Forgot Password Link
        forgot_password_link = ctk.CTkLabel(
            background_frame,
            text="Forgot Password?",
            font=("Montserrat", 12),
            text_color="#007BFF",
            cursor="hand2",
        )
        forgot_password_link.place(x=50, y=290)
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
        login_button.place(x=50, y=340)

        # Signup link
        signup_link = ctk.CTkLabel(
            background_frame,
            text="Don't have an account? Sign Up",
            font=("Montserrat", 12),
            text_color="#007BFF",
            cursor="hand2",
        )
        signup_link.place(x=110, y=390)
        signup_link.bind("<Button-1>", lambda e: self.display_signup())

    def send_otp_func(self):
        """Generate and send OTP to the provided email."""
        email = self.forgot_email.get().strip()
        
        if not email:
            messagebox.showerror("Error", "Please enter your email address!")
            return

        # Validate email format
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address!")
            return

        try:
            # Generate a 6-digit OTP
            otp = str(random.randint(100000, 999999))

            # Store OTP in memory for later validation
            self.generated_otp = otp

            # Email details
            sender_email = "venkat2834.p@gmail.com"  # Replace with your email
            sender_password = "palla19102"     # Replace with your email password
            recipient_email = email
            subject = "Your OTP for Password Reset"

            # Compose the email
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject

            body = f"""
            Hi,

            Your One-Time Password (OTP) for resetting your password is: {otp}

            If you did not request this, please ignore this email.

            Regards,
            Local Food Sharing App
            """
            msg.attach(MIMEText(body, "plain"))

            # Send the email using SMTP
            server = smtplib.SMTP("smtp.gmail.com", 587)  # For Gmail
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()

            # Notify the user
            messagebox.showinfo("OTP Sent", f"An OTP has been sent to {email}. Please check your inbox.")

        except Exception as e:
            print(f"Error sending OTP: {e}")
            messagebox.showerror("Error", "Failed to send OTP. Please try again later.")


    def confirm_otp_func(self):
        otp = self.otp_entry.get().strip()
        if not otp:
            messagebox.showerror("Error", "Please enter the OTP!")
            return
        if otp != getattr(self, "generated_otp", None):
            messagebox.showerror("Error", "Invalid OTP!")
            return
        messagebox.showinfo("OTP Verified", "OTP verified successfully!")

    def reset_password_func(self):
        new_password = self.new_password.get().strip()
        confirm_password = self.confirm_password.get().strip()
        if not new_password or not confirm_password:
            messagebox.showerror("Error", "All fields are required!")
            return
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
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
        back_button = ctk.CTkButton(
            background_frame,
            text="Back",
            command=self.display_login,
            width=80,
            height=30,
            corner_radius=10,
            fg_color="#CCCCCC",
            font=("Montserrat Bold", 12),
        )
        back_button.place(x=10, y=10)

        # Title
        forgot_title = ctk.CTkLabel(
            background_frame,
            text="Reset Password",
            font=("Montserrat Bold", 26),
            text_color="#333333",
        )
        forgot_title.place(relx=0.5, y=50, anchor="center")

        # Email entry
        email_label = ctk.CTkLabel(
            background_frame,
            text="Email",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        email_label.place(x=50, y=70)

        self.forgot_email = ctk.CTkEntry(
            background_frame,
            width=200,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter your email",
        )
        self.forgot_email.place(x=50, y=100)

        send_otp_button = ctk.CTkButton(
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
        send_otp_button.place(x=260, y=100)

        # OTP entry
        otp_label = ctk.CTkLabel(
            background_frame,
            text="Enter OTP",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        otp_label.place(x=50, y=140)

        self.otp_entry = ctk.CTkEntry(
            background_frame,
            width=200,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter OTP",
        )
        self.otp_entry.place(x=50, y=170)

        confirm_otp_button = ctk.CTkButton(
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
        confirm_otp_button.place(x=260, y=170)

        # New password entry
        new_password_label = ctk.CTkLabel(
            background_frame,
            text="New Password",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        new_password_label.place(x=50, y=220)

        self.new_password = ctk.CTkEntry(
            background_frame,
            width=300,
            font=("Montserrat", 14),
            corner_radius=10,
            show="•",
            placeholder_text="Enter new password",
        )
        self.new_password.place(x=50, y=250)

        confirm_password_label = ctk.CTkLabel(
            background_frame,
            text="Confirm Password",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        confirm_password_label.place(x=50, y=290)

        self.confirm_password = ctk.CTkEntry(
            background_frame,
            width=300,
            font=("Montserrat", 14),
            corner_radius=10,
            show="•",
            placeholder_text="Re-enter new password",
        )
        self.confirm_password.place(x=50, y=320)

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

        # Title
        signup_title = ctk.CTkLabel(
            background_frame,
            text="Create Your Account",
            font=("Montserrat Bold", 26),
            text_color="#333333",
        )
        signup_title.place(relx=0.5, y=50, anchor="center")

        # First Name
        first_name_label = ctk.CTkLabel(
            background_frame,
            text="First Name",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        first_name_label.place(x=50, y=80)

        self.first_name = ctk.CTkEntry(
            background_frame,
            width=140,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter your first name",
        )
        self.first_name.place(x=50, y=110)

        # Last Name
        last_name_label = ctk.CTkLabel(
            background_frame,
            text="Last Name",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        last_name_label.place(x=220, y=80)

        self.last_name = ctk.CTkEntry(
            background_frame,
            width=140,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter your last name",
        )
        self.last_name.place(x=220, y=110)

        # Email
        email_label = ctk.CTkLabel(
            background_frame,
            text="Email",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        email_label.place(x=50, y=150)

        self.username = ctk.CTkEntry(
            background_frame,
            width=300,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter your email",
        )
        self.username.place(x=50, y=180)

        # Password
        password_label = ctk.CTkLabel(
            background_frame,
            text="Password",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        password_label.place(x=50, y=230)

        self.password = ctk.CTkEntry(
            background_frame,
            width=300,
            font=("Montserrat", 14),
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

            if not email or not raw_password:
                messagebox.showerror("Error", "All fields are required!")
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
                print(f"Username Entry: {email}")
                print(f"Password Entry: {raw_password}")

                mainWindow(user_id)  # Pass the user_id to the main window
            else:
                messagebox.showerror(
                    title="Invalid Credentials",
                    message="The email and password don't match."
                )
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
        if not all([first_name, last_name, email, password]):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Validate email format
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Invalid email format!")
            return

        # Hash the password before storing it in the database
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Attempt to create the user in the database
        if create_user(first_name, last_name, email, hashed_password):
            messagebox.showinfo("Sign Up", "Account Created Successfully!")
            self.display_login()
        else:
            messagebox.showerror("Error", "Failed to create account. Please try again!")

    def resetPasswordFunc(self):
        """Handle the reset password functionality."""
        try:
            email = self.forgot_email.get().strip()

            # Validate email input
            if not email:
                CTkMessagebox(
                    title="Empty Field",
                    message="Please enter your email address."
                )
                return

            if "@" not in email or "." not in email:
                CTkMessagebox(
                    title="Invalid Email",
                    message="Please enter a valid email address."
                )
                return

            # Simulate checking if the email exists in the database
            # if not self.check_email_exists(email):
            #     CTkMessagebox(
            #         title="Email Not Found",
            #         message="This email is not registered. Please try again."
            #     )
            #     return

            # Generate OTP and store it in memory (or database)
            self.generated_otp = self.generate_otp()
            self.otp_email = email

            # Simulate sending the OTP to the user's email
            if self.send_otp_func(email, self.generated_otp):
                CTkMessagebox(
                    title="OTP Sent",
                    message=f"An OTP has been sent to {email}. Please check your inbox."
                )
                self.display_enter_otp()  # Show OTP entry screen
            else:
                CTkMessagebox(
                    title="Error",
                    message="Failed to send OTP. Please try again later."
                )
        except Exception as e:
            messagebox.showerror(
                title="Error",
                message=f"An error occurred: {e}"
            )

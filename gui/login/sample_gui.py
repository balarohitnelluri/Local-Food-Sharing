from pathlib import Path
from tkinter import Toplevel, Tk, Canvas, Entry, Button, PhotoImage, messagebox, Label
from controller import *
from ..main_window.main import mainWindow
import hashlib

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def loginWindow():
    Login()

# def SingupWindow():
#     Signup()

class Login(Toplevel):

    global user

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.title("Login - Local Food Sharing App")
        self.geometry("1012x506")
        self.configure(bg="#5E95FF")

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
        self.canvas.create_rectangle(
            469.0, 0.0, 1012.0, 506.0, fill="#FFFFFF", outline=""
        )

        entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(736.0, 331.0, image=entry_image_1)
        entry_1 = Entry(self.canvas, bd=0, bg="#EFEFEF", highlightthickness=0)
        entry_1.place(x=568.0, y=294.0, width=336.0, height=0)

        entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        entry_bg_2 = self.canvas.create_image(736.0, 229.0, image=entry_image_2)
        entry_2 = Entry(self.canvas, bd=0, bg="#EFEFEF", highlightthickness=0)
        entry_2.place(x=568.0, y=192.0, width=336.0, height=0)

        self.canvas.create_text(
            573.0,
            306.0,
            anchor="nw",
            text="Password",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.canvas.create_text(
            573.0,
            204.0,
            anchor="nw",
            text="Email",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.canvas.create_text(
            553.0,
            66.0,
            anchor="nw",
            text="Enter your login details",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(
            self.canvas,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.loginFunc,
            relief="flat",
        )
        button_1.place(x=641.0, y=412.0, width=190.0, height=48.0)

        # Sign Up clickable text
        self.signup_text = Label(
            self.canvas,
            text="Don't have an account? Sign Up",
            fg="#007BFF",
            bg="#FFFFFF",
            font=("Montserrat", 12, "bold"),
            cursor="hand2"
        )
        self.signup_text.place(x=615, y=467)
        self.signup_text.bind("<Button-1>", lambda e: self.display_signup())

        self.canvas.create_text(
            85.0,
            77.0,
            anchor="nw",
            text="Local Food Sharing",
            fill="#FFFFFF",
            font=("Montserrat Bold", 30 * -1),
        )

        self.canvas.create_text(
            553.0,
            109.0,
            anchor="nw",
            text="Enter the credentials provided during registration",
            fill="#CCCCCC",
            font=("Montserrat Bold", 16 * -1),
        )

        self.canvas.create_text(
            90.0,
            150.0,
            anchor="nw",
            text="The Local Food Sharing App connects communities,",
            fill="#FFFFFF",
            font=("Montserrat Regular", 14 * -1),
        )

        self.canvas.create_text(
            90.0,
            179.0,
            anchor="nw",
            text="enabling the distribution of excess food to those in need.",
            fill="#FFFFFF",
            font=("Montserrat Regular", 14 * -1),
        )

        self.canvas.create_text(
            90.0,
            208.0,
            anchor="nw",
            text="Manage food donations, pickups, and notifications",
            fill="#FFFFFF",
            font=("Montserrat Regular", 14 * -1),
        )

        self.canvas.create_text(
            90.0,
            237.0,
            anchor="nw",
            text="through an easy-to-use platform.",
            fill="#FFFFFF",
            font=("Montserrat Regular", 14 * -1),
        )

        entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
        entry_bg_3 = self.canvas.create_image(736.0, 241.0, image=entry_image_3)
        self.username = Entry(
            self.canvas,
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            font=("Montserrat Bold", 16 * -1),
            foreground="#777777",
        )
        self.username.place(x=573.0, y=229.0, width=326.0, height=22.0)

        entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
        entry_bg_4 = self.canvas.create_image(736.0, 342.0, image=entry_image_4)
        self.password = Entry(
            self.canvas,
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            font=("Montserrat Bold", 16 * -1),
            foreground="#777777",
            show="•",
        )
        self.password.place(x=573.0, y=330.0, width=326.0, height=22.0)

        image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        image_1 = self.canvas.create_image(472.0, 326.0, image=image_image_1)

        # Bind enter to form submit
        self.username.bind("<Return>", lambda x: self.loginFunc())
        self.password.bind("<Return>", lambda x: self.loginFunc())

        # Essentials
        self.resizable(False, False)
        self.mainloop()

    def hash_password(self, password):
        """
        Hashes a password using SHA-256 for secure storage and comparison.
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def loginFunc(self):
        global user
        try:
            # Hash the entered password for comparison (assuming the database stores hashed passwords)
            hashed_password = self.hash_password(self.password.get())

            # Check if the user exists with the provided email and password
            if checkUser(self.username.get().lower(), hashed_password):
                user = self.username.get().lower()
                messagebox.showinfo(
                    title="Login Successful",
                    message=f"Welcome, {user}!"
                )
                self.destroy()
                mainWindow()  # Proceed to the main window
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

    def display_signup(self):
        self.canvas.delete("all") 
        # Code to handle the signup logic or display a signup window
        messagebox.showinfo("Sign Up", "Sign Up functionality coming soon!")
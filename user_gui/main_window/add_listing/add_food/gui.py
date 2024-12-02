from pathlib import Path
from tkinter import Frame, messagebox, StringVar
import customtkinter as ctk
from tkcalendar import DateEntry
import controller as db_controller

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class AddFoodForm(Frame):
    def __init__(self, parent, user_id, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.user_id = user_id  # Store user_id for user-specific operations
        self.data = {
            "food_type": StringVar(),
            "quantity": StringVar(),
            "location": StringVar(),
            "zipcode": StringVar(),
            "expiry_date": StringVar(),
        }

        self.configure(bg="#FFFFFF")

        # Central Frame to hold all fields
        central_frame = ctk.CTkFrame(
            self,
            width=600,
            height=400,
            corner_radius=15,
            fg_color="#F4F4F4",
        )
        central_frame.place(relx=0.1, rely=0.15)

        # Food Type Frame
        food_type_frame = ctk.CTkFrame(central_frame, fg_color="#FFFFFF", corner_radius=10)
        food_type_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        food_type_label = ctk.CTkLabel(
            food_type_frame,
            text="Food Type",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        food_type_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        food_type_dropdown = ctk.CTkOptionMenu(
            food_type_frame,
            variable=self.data["food_type"],
            values=["Fruits", "Dairy", "Vegetables", "Fast Food", "Soft Drinks", "Grains", "Snacks", "Other"],
            font=("Montserrat", 14),
            width=150,
        )
        food_type_dropdown.grid(row=1, column=0, padx=(10, 10), pady=(0, 10))
        food_type_dropdown.set("Fruits")

        # Quantity Frame
        quantity_frame = ctk.CTkFrame(central_frame, fg_color="#FFFFFF", corner_radius=10)
        quantity_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        quantity_label = ctk.CTkLabel(
            quantity_frame,
            text="Quantity",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        quantity_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        quantity_entry = ctk.CTkEntry(
            quantity_frame,
            textvariable=self.data["quantity"],
            width=150,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter quantity",
        )
        quantity_entry.grid(row=1, column=0, padx=(10, 10), pady=(0, 10))

        # Expiry Date Frame
        expiry_date_frame = ctk.CTkFrame(central_frame, fg_color="#FFFFFF", corner_radius=10)
        expiry_date_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        expiry_date_label = ctk.CTkLabel(
            expiry_date_frame,
            text="Expiry Date",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        expiry_date_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        expiry_date_picker = DateEntry(
            expiry_date_frame,
            textvariable=self.data["expiry_date"],
            date_pattern="yyyy-mm-dd",
            font=("Montserrat", 14),
            background="#5E95FF",
            foreground="white",
            borderwidth=2,
        )
        expiry_date_picker.grid(row=1, column=0, padx=(10, 10), pady=(0, 10))

        # Address Frame
        address_frame = ctk.CTkFrame(central_frame, fg_color="#FFFFFF", corner_radius=10)
        address_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        address_label = ctk.CTkLabel(
            address_frame,
            text="Address",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        address_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        address_entry = ctk.CTkEntry(
            address_frame,
            textvariable=self.data["location"],
            width=300,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter address",
        )
        address_entry.grid(row=1, column=0, padx=(10, 10), pady=(0, 10))

        # Zipcode Frame
        zipcode_frame = ctk.CTkFrame(central_frame, fg_color="#FFFFFF", corner_radius=10)
        zipcode_frame.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        zipcode_label = ctk.CTkLabel(
            zipcode_frame,
            text="Zipcode",
            font=("Montserrat Bold", 14),
            text_color="#5E95FF",
        )
        zipcode_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        zipcode_entry = ctk.CTkEntry(
            zipcode_frame,
            textvariable=self.data["zipcode"],
            width=150,
            font=("Montserrat", 14),
            corner_radius=10,
            placeholder_text="Enter zipcode",
        )
        zipcode_entry.grid(row=1, column=0, padx=(10, 10), pady=(0, 10))

        # Add Button
        add_button = ctk.CTkButton(
            central_frame,
            text="Add",
            command=self.save,
            width=200,
            height=40,
            font=("Montserrat Bold", 14),
            corner_radius=10,
            fg_color="#5E95FF",
            hover_color="#417BFF",
        )
        add_button.grid(row=2, column=0, columnspan=3, pady=(20, 10))

    def save(self):
        for field, val in self.data.items():
            if val.get().strip() == "":
                messagebox.showerror("Error", f"Please fill in the {field.replace('_', ' ').capitalize()} field")
                return

        result = db_controller.add_food_item(
            food_type=self.data["food_type"].get().strip(),
            quantity=self.data["quantity"].get().strip(),
            location=self.data["location"].get().strip(),
            zipcode=self.data["zipcode"].get().strip(),
            expiry_date=self.data["expiry_date"].get().strip(),
            user_id=self.user_id,
        )

        if result:
            messagebox.showinfo("Success", "Food item added successfully!")
            for key in self.data:
                self.data[key].set("")  # Clear all fields after saving
        else:
            messagebox.showerror("Error", "Failed to add food item. Please try again!")

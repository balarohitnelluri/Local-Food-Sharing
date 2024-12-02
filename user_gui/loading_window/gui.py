import customtkinter as ctk
import time
from utils import center_window


class LoadingBarApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Loading Bar Example")
        self.geometry("500x500")
        center_window(self,500,500)

        # Create a label for status
        self.status_label = ctk.CTkLabel(self, text="Loading...", font=("Arial", 16))
        self.status_label.pack(pady=20)

        # Create a progress bar
        self.progress_bar = ctk.CTkProgressBar(self, width=300)
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)  # Initialize progress to 0%

        # Start button
        self.start_button = ctk.CTkButton(self, text="Start Loading", command=self.start_loading)
        self.start_button.pack(pady=20)

    def start_loading(self):
        self.start_button.configure(state="disabled")  # Disable button during loading
        self.progress_bar.set(0)  # Reset progress
        self.update_progress(0)

    def update_progress(self, value):
        if value <= 1:  # Progress bar values range from 0 to 1
            self.progress_bar.set(value)  # Update progress bar
            self.after(50, self.update_progress, value + 0.01)  # Increment progress by 1% every 50ms
        else:
            self.status_label.configure(text="Loading Complete!")  # Update status label
            self.start_button.configure(state="normal")  # Re-enable button after loading
    
        
    

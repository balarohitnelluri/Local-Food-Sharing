import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("400x300")

        # Create multiple buttons
        self.button1 = ctk.CTkButton(
            self, text="Button 1", command=lambda: self.widget_callback(self.button1)
        )
        self.button1.pack(pady=20)

        self.button2 = ctk.CTkButton(
            self, text="Button 2", command=lambda: self.widget_callback(self.button2)
        )
        self.button2.pack(pady=20)

        self.button3 = ctk.CTkButton(
            self, text="Button 3", command=lambda: self.widget_callback(self.button3)
        )
        self.button3.pack(pady=20)

    def widget_callback(self, widget):
        print(f"Function called from: {widget}")
        print(f"Widget text: {widget.cget('text')}")  # Get text of the button


if __name__ == "__main__":
    app = App()
    app.mainloop()
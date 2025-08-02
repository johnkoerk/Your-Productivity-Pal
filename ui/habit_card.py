import customtkinter as ctk
from logic.habit import Habit

class HabitCard(ctk.CTkFrame):
    def __init__(self, parent, habit: Habit):
        super().__init__(parent)

        self.dropdown_visible = False # dropdown always starts off hidden

        self.habit = habit

        # creates and packs nested frame
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(fill="x", pady=2) #expand horizontally with vertical padding

        # creates and packs title label
        self.title_label = ctk.CTkLabel(self.top_frame, text=self.habit.title, font=ctk.CTkFont(size=16))
        self.title_label.pack(side="left", padx=10)

        # creates and packs dropdown toggle button all the way to the right
        self.toggle_button = ctk.CTkButton(
            self.top_frame,
            text="˅",
            width=30,
            command=self.toggle_dropdown
        )
        self.toggle_button.pack(side="right", padx=10)

        self.dropdown_frame = ctk.CTkFrame(self) #creates dropdown frame

        # fills dropdown frame with habit details
        self.dropdown_info = ctk.CTkLabel(self.dropdown_frame, text=self.habit.description, wraplength=400)
        self.dropdown_info.pack(padx=10, pady=5)


    def toggle_dropdown(self):
        # unpacks dropdown frame if visible and changes button text
        if self.dropdown_visible:
            self.dropdown_frame.pack_forget()
            self.toggle_button.configure(text="˅")
        # packs dropdown frame if not visible and changes button text
        else:
            self.dropdown_frame.pack(fill="x")
            self.toggle_button.configure(text="-")
        self.dropdown_visible = not self.dropdown_visible # toggles visibility state

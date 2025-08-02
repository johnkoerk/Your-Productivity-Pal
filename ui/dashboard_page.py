import customtkinter as ctk
from logic.habit_manager import HabitManager
from ui.habit_card import HabitCard

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent) #initializes basic setup of app window inside parent (container)
        self.controller = controller

        # creates and sets text label
        label = ctk.CTkLabel(self, text="Habit Overview", font=("Arial", 24))
        label.pack(pady=20)

        # creates and sets navigation bar
        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(pady=10)

        # creates and sets navigation bar buttons
        ctk.CTkButton(nav_frame, text="Calendar", command=lambda: controller.show_frame("Calendar")).pack(side="left", padx=10)
        ctk.CTkButton(nav_frame, text="Chatbot", command=lambda: controller.show_frame("Chatbot")).pack(side="left", padx=10)

        # creates and sets frame for habit cards
        self.habit_cards_frame = ctk.CTkFrame(self)
        self.habit_cards_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.habit_manager = HabitManager()

        self.refresh_habits() #habits are loaded and displayed on initialization

    def refresh_habits(self):
        self.habit_manager.load_habits()
        # clears all displayed habit cards
        for widget in self.habit_cards_frame.winfo_children():
            widget.destroy()
        # freshly creates and displays all habit cards
        for habit in self.habit_manager.get_all_habits():
            card = HabitCard(self.habit_cards_frame, habit)
            card.pack(fill="x", pady=5, padx=5)

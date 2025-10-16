import customtkinter as ctk
from PIL import Image
from logic.habit_manager import HabitManager
from ui.habit_card import HabitCard
from ui.habit_creation_page import HabitCreation

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent) #initializes basic setup of app window inside parent (container)
        self.controller = controller
        self.parent = parent

        #creates and sets text label
        label = ctk.CTkLabel(self, text="Habit Overview", font=("Arial", 24))
        label.pack(pady=20)

        #creates and sets frame for habit cards
        self.habit_cards_frame = ctk.CTkFrame(self)
        self.habit_cards_frame.pack(fill="both", expand=True, padx=20, pady=10)

        #creates and sets add habit button with plus icon
        self.plus_icon = ctk.CTkImage(light_image=Image.open("assets/plus.png"), size=(32, 32))
        add_button = ctk.CTkButton(self, text="", image=self.plus_icon, width=50, height=50, corner_radius=8,
                                   command=self.display_habit_creation) #command creates habit creation page upon pressing
        add_button.pack(pady=10)

        self.habit_manager = HabitManager()

        self.refresh_habits() #habits are loaded and displayed on initialization

    def refresh_habits(self):
        self.habit_manager.load_habits()
        self.habit_manager.ensure_no_missing_days()
        #clears all displayed habit cards
        for widget in self.habit_cards_frame.winfo_children():
            widget.destroy()

        #sorts habits to show today's habits first
        habits = self.habit_manager.get_all_habits()
        today_habits = [h for h in habits if h.is_scheduled_for_today()]
        other_habits = [h for h in habits if not h.is_scheduled_for_today()]
        sorted_habits = today_habits + other_habits

        #freshly creates and displays all habit cards
        for habit in sorted_habits:
            card = HabitCard(self.habit_cards_frame, habit, self.habit_manager, self)
            card.pack(fill="x", pady=5, padx=5)

    #creates and displays new habit creation page
    def display_habit_creation(self):
        habit_creation_page = HabitCreation(parent=self.parent, controller=self)
        habit_creation_page.grid(row=0, column=0, sticky="nsew")
        habit_creation_page.tkraise()

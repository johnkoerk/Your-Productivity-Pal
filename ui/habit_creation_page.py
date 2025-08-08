import customtkinter as ctk
from datetime import date
from logic.habit import Habit

class HabitCreation(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # creates and sets entry for title
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Title")
        self.title_entry.pack(pady=10)

        # creates and sets entry for description
        self.description_entry = ctk.CTkEntry(self, placeholder_text="Description (optional)")
        self.description_entry.pack(pady=10)

        # creates and sets entry for start date
        self.start_date_entry = ctk.CTkEntry(self, placeholder_text="Start Date (YYYY-MM-DD)")
        self.start_date_entry.pack(pady=10)

        # creates and sets checkboxes for days of the week
        self.days_selected = []
        days_frame = ctk.CTkFrame(self)
        days_frame.pack(pady=10)
        self.days_vars = {}
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(days_frame, text=day, variable=var)
            checkbox.pack(anchor="w")
            self.days_vars[day] = var #dictionary to track boolean variables for each day
        
        # creates and sets entry for consistency goal
        self.goal_entry = ctk.CTkEntry(self, placeholder_text="Consistency Goal (optional)")
        self.goal_entry.pack(pady=10)

        # creates and sets create button
        create_button = ctk.CTkButton(self, text="Create", command=self.create_habit)
        create_button.pack(pady=10)

        # creates and sets cancel button
        cancel_button = ctk.CTkButton(self, text="Cancel", command=self.destroy())
        cancel_button.pack(pady=10)

    def create_habit(self):
        # gathers input data and stores them in variables
        title = self.title_entry.get()
        description = self.description_entry.get()
        start_date = self.start_date_entry.get()
        goal = self.goal_entry.get()

        # attempts to convert start date string to date object
        try:
            start_date = date.fromisoformat(start_date)
        except ValueError: # catches invalid date format
            print("Invalid date format. Use YYYY-MM-DD.")
            return
        
        selected_days = [day for day, var in self.days_vars.items() if var.get()] #gathers just selected days from checkboxes into list

        # ensures all required fields are filled out    
        if not title or not selected_days or not start_date:
            print("Please fill in all required fields :)")
            return

        # creates new Habit object and adds it to habit manager
        habit = Habit(
            title=title,
            description=description,
            days=selected_days,
            start_date=start_date,
            consistency_goal=int(goal) if goal else None
        )
        self.controller.habit_manager.add_habit(habit)

        # refreshes habit cards on dashboard and destroys creation page upon successful habit creation
        self.controller.refresh_habits()
        self.destroy()
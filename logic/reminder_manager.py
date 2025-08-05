import os
import json
from datetime import datetime
import customtkinter as ctk
from logic.habit_manager import HabitManager

reminder_file = 'storage/reminder.json'

class ReminderManager:
    def __init__(self, root, habit_manager: HabitManager):
        self.root = root
        self.habit_manager = habit_manager
        self.last_shown = self.load_last_shown()

    def load_last_shown(self):
        # if reminder file doesn't exist, displays reminder popup
        if not os.path.exists(reminder_file):
            return None
        # reads last_shown string from json file and converts to date object
        try:
            with open(reminder_file, "r") as file:
                data = json.load(file)
                date = data.get("last_shown")
                return datetime.strptime(date, "%Y-%m-%d").date() if date else None
        # catches any errors reading the file and displays reminder popup
        except Exception as e:
            print("Failed to load reminder state:", e)
            return None
        
    def save_last_shown(self, date):
        # ensures storage folder exists before writing last_shown string to it
        try:
            os.makedirs(os.path.dirname(reminder_file), exist_ok=True)
            with open(reminder_file, "w") as file:
                json.dump({"last_shown": date.strftime("%Y-%m-%d")}, file)
        # catches any errors writing to the file
        except Exception as e:
            print("Failed to save reminder state:", e)

    def show_daily_reminder(self):
        # if last_shown variable has been updated to today, does not show reminder popup
        today = datetime.now().date()
        if self.last_shown == today:
            return
        
        # retrieves list of habits for today and fails to show reminder if none for today
        habits_today = self.habit_manager.get_habits_due_today()
        if not habits_today:
            return
        
        # creates and formats reminder popup window
        reminder = ctk.CTkToplevel(self.root)
        reminder.title("Daily Habit Reminder")
        reminder.geometry("400x300")
        reminder.resizable(False, False)

        # creates and sets reminder popup title
        title = ctk.CTkLabel(reminder, text="Today's Habits", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=10)

        # cycles through habits for today and lists each in reminder popup
        for habit in habits_today:
            label = ctk.CTkLabel(reminder, text=f"- {habit.title}", wraplength=380, anchor="w", justify="left")
            label.pack(anchor="w", padx=20)

        # creates and sets "Don't show again" checkbox
        dont_show = ctk.BooleanVar()
        dont_show_check = ctk.CTkCheckBox(reminder, text="Don't show again", variable=dont_show)
        dont_show_check.pack(pady=10)

        # updates last_shown variable if checkbox is checked before destroying popup
        def on_close():
            if dont_show.get():
                self.save_last_shown(today)
            reminder.destroy()

        # creates and sets close button linked to on_close function
        close_btn = ctk.CTkButton(reminder, text="Close", command=on_close)
        close_btn.pack(pady=10)
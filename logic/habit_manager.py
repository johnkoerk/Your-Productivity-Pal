import json
import os
from datetime import date, datetime, timedelta
from logic.habit import Habit

data_file = 'storage/data.json' #FIXME may change file name
history_file = 'storage/history.json'

class HabitManager:
    def __init__(self):
        self.habits = []
        self.daily_history = {}
        self.load_habits() #fills habits list with previously saved habits upon initialization
        self.load_history() #fills daily_history with previously saved history upon initialization

    def add_habit(self, habit):
        self.habits.append(habit) #adds habit to list
        self.save_habits() #saves habit list after each new habit added
        self.update_history(date.today())

    def save_habits(self):
        os.makedirs('storage', exist_ok=True) #ensures storage folder exists before writing to it
        with open(data_file, 'w') as file:
            json.dump([habit.to_dict() for habit in self.habits], file, indent=2) #converts habits to dictionaries to be written in json file

    def load_habits(self):
        try:
            with open(data_file, 'r') as file:
                self.habits = [Habit.from_dict(data) for data in json.load(file)] #reads data from json file and converts habits back to Habit objects
        except FileNotFoundError:
            self.habits = [] #habits list remains empty if previous data does not exist

    def delete_habit(self, habit):
        self.habits = [h for h in self.habits if h.title != habit.title] #recreates list of habits excluding habit being deleted
        self.save_habits()

    def get_all_habits(self):
        return self.habits #returns full list of habits
    
    def get_habits_due_today(self):
        self.load_habits()
        return [habit for habit in self.habits if habit.is_scheduled_for_today()] #returns list of habits to be performed today

    def get_habits_for_date(self, target_date):
        date_str = target_date.isoformat()
        habits_for_date = {}

        if date_str in self.daily_history: #if history already contains entry for date, return stored information
            habits_for_date = self.daily_history[date_str]

        else: #otherwise, determine habits for date based on their schedule
            weekday_name = target_date.strftime("%A")
            for habit in self.habits:
                if weekday_name in habit.days:
                    habits_for_date[habit.title] = False

        return habits_for_date
    
    #determines if a day is marked as fully complete (green button)
    def all_habits_completed(self, target_date): 
        date_str = target_date.isoformat()

        if date_str not in self.daily_history or not self.daily_history[date_str]: #checks for no habits scheduled that day
            return False
        
        return all(self.daily_history[date_str].values())

    def save_history(self):
        os.makedirs('storage', exist_ok=True) #ensures storage folder exists before writing to it
        with open(history_file, 'w') as file:
            json.dump(self.daily_history, file, indent=2)

    def load_history(self):
        try:
            with open(history_file, 'r') as file:
                self.daily_history = json.load(file)
        except FileNotFoundError:
            self.daily_history = {} #history list remains empty if previous data does not exist

    def update_history(self, target_date):
        date_str = target_date.isoformat()
        if date_str not in self.daily_history:
            self.daily_history[date_str] = {} #creates new entry for date if one does not already exist
        weekday_name = target_date.strftime("%A")
        for habit in self.habits:
            if weekday_name in habit.days and habit.title not in self.daily_history[date_str]:
                self.daily_history[date_str][habit.title] = False #populates new habit entries as incomplete by default
        self.save_history() #overrides previous history data with updated information

    def mark_habit_complete_in_history(self, habit_title, target_date):
        date_str = target_date.isoformat()
        if date_str not in self.daily_history:
            self.update_history(target_date) #ensures date entry exists before marking habit complete
        if habit_title in self.daily_history[date_str]:
            self.daily_history[date_str][habit_title] = True
            self.save_history() #saves updated history after marking habit complete

    def ensure_no_missing_days(self): #fills in gaps between last stored day and today
        if not self.habits:
            self.load_habits()

        if not self.daily_history:
            self.update_history(date.today())
            return
    
        last_recorded_day = max(date.fromisoformat(d) for d in self.daily_history.keys())
        today = date.today()
        current_day = last_recorded_day + timedelta(days=1)

        while current_day <= today: #loops through each day between last recorded day and today while updating history
            self.update_history(current_day)
            current_day += timedelta(days=1)
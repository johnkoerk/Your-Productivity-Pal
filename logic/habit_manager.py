import json
import os
from logic.habit import Habit

data_file = 'storage/data.json' #FIXME may change file name

class HabitManager:
    def __init__(self):
        self.habits = [] #initializes empty habits list to be used by other class functions

    def add_habit(self, habit):
        self.habits.append(habit) #adds habit to list
        self.save_habits() #saves habit list after each new habit added

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

    def get_all_habits(self):
        return self.habits #returns full list of habits
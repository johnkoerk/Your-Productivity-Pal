from datetime import date

class Habit:
    # initializes information for new Habit
    # FIXME return here to edit automatic initialization
    def __init__(self, title, days, start_date=date.today(), description=''): 
        self.title = title
        self.description = description
        self.days = days
        self.start_date = start_date
        self.completions = [] #list of dates habit was marked complete, always starts empty

    # function for recording completions when habit is marked complete
    def mark_complete(self, completion_date=None):
        completion_date = completion_date or date.today() #records today's date if date isn't provided
        if completion_date not in self.completions:
            self.completions.append(completion_date) #adds date to list of completions if not already present

    # FIXME will be used to calculate habit points if I decide to add this feature
    def get_points(self):
        pass

    # used to convert Habit info to usable format for json.dump()
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'days': self.days,
            'start_date': self.start_date.isoformat(), #date is converted to standard YYYY-MM-DD format
            'completions': [completion.isoformat() for completion in self.completions] #converts all completion dates to standard format
        }

    # used to rebuild Habit object from JSON file
    def from_dict(data):
        habit = Habit(
            title = data['title'],
            description = data['description'],
            start_date = date.fromisoformat(data['start_date']), #converts date from standard YYYY-MM-DD format to date object
            days = data['days']
        )
        habit.completions = [date.fromisoformat(completion) for completion in data['completions']] #converts all completion dates from standard format
        return habit
    
    # checks if habit is scheduled for today
    def is_scheduled_for_today(self):
        today_name = date.today().strftime("%A")
        return today_name in self.days
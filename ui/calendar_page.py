import customtkinter as ctk
import calendar
from datetime import datetime

class Calendar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent) #initializes basic setup of app window inside parent (container)
        self.controller = controller

        # creates and sets text label
        label = ctk.CTkLabel(self, text="Calendar", font=("Arial", 24))
        label.pack(pady=20)

        # creates and sets Home button
        ctk.CTkButton(self, text="Home", command=lambda: controller.show_frame("Dashboard")).pack(pady=10)

        # prepares year and month in preparation for calendar display
        self.current_date = datetime.now()
        self.year = self.current_date.year
        self.month = self.current_date.month

        # creates and sets calendar frame
        self.calendar_frame = ctk.CTkFrame(self)
        self.calendar_frame.pack(pady=10)

        self.create_calendar()

    def create_calendar(self):
        # clears calendar for fresh display
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # creates and sets day labels
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            label = ctk.CTkLabel(self.calendar_frame, text=day, font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=i, padx=5, pady=5)

        # creates a calendar object used to establish layout for the month
        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(self.year, self.month)

        # fills calendar frame with day labels and sets them
        for row, week in enumerate(month_days, start=1):
            for col, day in enumerate(week):
                if day == 0: #days labeled 0 are absent and thus left unlabeled
                    label = ctk.CTkLabel(self.calendar_frame, text="")
                else: #days labeled with a number are displayed accordingly
                    label = ctk.CTkLabel(self.calendar_frame, text=str(day), width=4)
                label.grid(row=row, column=col, padx=5, pady=5)
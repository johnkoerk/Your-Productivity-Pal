import customtkinter as ctk
import calendar
from datetime import datetime, date
from logic.habit_manager import HabitManager

class Calendar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent) #initializes basic setup of app window inside parent (container)
        self.controller = controller
        self.habit_manager = HabitManager()

        #creates and sets text label
        label = ctk.CTkLabel(self, text="Calendar", font=("Arial", 24))
        label.pack(pady=20)

        #prepares year and month in preparation for calendar display
        self.current_date = datetime.now()
        self.year = self.current_date.year
        self.month = self.current_date.month

        #creates and sets navigation frame
        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(fill="x", pady=(5, 10))

        #configures grid layout for navigation frame
        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=0)
        nav_frame.grid_columnconfigure(2, weight=1)

        #creates and sets previous month button
        prev_btn = ctk.CTkButton(nav_frame, text="<", width=40, command=self.prev_month)
        prev_btn.grid(row=0, column=0, sticky="w", padx=10)

        #creates and sets month label
        self.month_label = ctk.CTkLabel(nav_frame, text="", font=("Arial", 28, "bold"))
        self.month_label.grid(row=0, column=1, padx=10)

        #creates and sets next month button
        next_btn = ctk.CTkButton(nav_frame, text=">", width=40, command=self.next_month)
        next_btn.grid(row=0, column=2, sticky="e", padx=10)

        #creates and sets calendar frame
        self.calendar_frame = ctk.CTkFrame(self)
        self.calendar_frame.pack(pady=10)

        self.create_calendar()

    def open_day_modal(self, date_str):
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        habits_for_date = self.habit_manager.get_habits_for_date(target_date)

        #creates and sets modal for daily habit details
        modal = ctk.CTkToplevel(self)
        modal.title(f"Habits for {date_str}")
        modal.geometry("300x400")
        modal.grab_set()

        #displays habits and their completion status for the selected date
        if not habits_for_date:
            ctk.CTkLabel(modal, text="No habits scheduled").pack(pady=10)
        else:
            for habit, completed in habits_for_date.items():
                status = "✅ Complete" if completed else "❌ Incomplete"
                ctk.CTkLabel(modal, text=f"{habit}: {status}").pack(pady=5)
        
        ctk.CTkButton(modal, text="Close", command=modal.destroy).pack(pady=10)

    def update_month_label(self):
        month_name = calendar.month_name[self.month]
        self.month_label.configure(text=f"{month_name} {self.year}")

    def create_calendar(self):
        #clears calendar for fresh display
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.update_month_label()

        #creates and sets day labels
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            label = ctk.CTkLabel(
                self.calendar_frame,
                text=day,
                font=ctk.CTkFont(weight="bold"),
                padx=15,
                pady=15
            )
            label.grid(row=0, column=i, padx=10, pady=10)

        #creates a calendar object used to establish layout for the month
        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(self.year, self.month)

        today = datetime.now().date()
        #fills calendar frame with day labels and sets them
        for row, week in enumerate(month_days, start=1):
            for col, day in enumerate(week):
                if day == 0: #days labeled 0 are absent and thus left unlabeled
                    label = ctk.CTkLabel(self.calendar_frame, text="", width=4)
                    continue

                    #days labeled with a number are displayed accordingly
                date_obj = datetime(self.year, self.month, day).date()

                btn_color = None
                if date_obj <= today and self.habit_manager.all_habits_completed(date_obj):
                    btn_color = "green"

                #creates and sets button for each day with appropriate color
                btn = ctk.CTkButton(
                    self.calendar_frame,
                    text=str(day),
                    command=lambda d=day: self.open_day_modal(f"{self.year}-{self.month:02d}-{d:02d}"),
                    width=50,
                    height=50,
                    fg_color=btn_color
                )
                btn.grid(row=row, column=col, padx=10, pady=10)

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -=1
        else:
            self.month -=1
        self.create_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.create_calendar()
import customtkinter as ctk
from PIL import Image
from logic.habit_manager import HabitManager
from logic.reminder_manager import ReminderManager
from ui.dashboard_page import Dashboard
from ui.calendar_page import Calendar
from ui.chatbot_page import Chatbot

class Framework(ctk.CTk):
    def __init__(self):
        super().__init__() #initializes basic setup of app window
        # sets title, size, and resizing functionality of window
        self.title("Personal AI Buddy")
        self.geometry("900x600")
        self.resizable(False, False)

        self.habit_manager = HabitManager()
        self.reminder_manager = ReminderManager(self, self.habit_manager)

        # creates navigation bar frame and sets it to fill left side of window
        self.navbar = ctk.CTkFrame(self, width=50)
        self.navbar.pack(side="left", fill="y")

        # creates navigation bar icons to be used for buttons
        self.dashboard_icon = ctk.CTkImage(light_image=Image.open("assets/dashboard.png"), size=(32, 32))
        self.calendar_icon = ctk.CTkImage(light_image=Image.open("assets/calendar.png"), size=(32, 32))
        self.chatbot_icon = ctk.CTkImage(light_image=Image.open("assets/chatbot.png"), size=(32, 32))

        # creates and sets dashboard button in nav bar
        self.dashboard_button = ctk.CTkButton(
            self.navbar, text="", image=self.dashboard_icon, font=("Arial", 20), width=50, height=50,
            command=lambda: self.show_frame("Dashboard") 
        )
        self.dashboard_button.pack(pady=10)

        # creates and sets calendar button in nav bar
        self.calendar_button = ctk.CTkButton(
            self.navbar, text="", image=self.calendar_icon, font=("Arial", 20), width=50, height=50,
            command=lambda: self.show_frame("Calendar")
        )
        self.calendar_button.pack(pady=10)

        # creates and sets chatbot button in nav bar
        self.chatbot_button = ctk.CTkButton(
            self.navbar, text="", image=self.chatbot_icon, font=("Arial", 20), width=50, height=50,
            command=lambda: self.show_frame("Chatbot")
        )
        self.chatbot_button.pack(pady=10)

        # creates container frame for pages and sets it to fill whole window
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        # configures grid weight to allow resizing
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {} #creates dictionary for pages

        # this loop creates a page for each class, stores them in the dict, and stacks them
        for page in (Dashboard, Calendar, Chatbot):
            page_name = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Dashboard") #initializes Dashboard page to front

        self.after(500, self.reminder_manager.show_daily_reminder)

    # switches to the selected page to display in front
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "Dashboard":
            frame.refresh_habits() #habits are refreshed when returning to Dashboard
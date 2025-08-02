import customtkinter as ctk
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

    # switches to the selected page to display in front
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "Dashboard":
            frame.refresh_habits() #habits are refreshed when returning to Dashboard
import customtkinter as ctk
from logic.habit import Habit

class HabitCard(ctk.CTkFrame):
    def __init__(self, parent, habit: Habit, habit_manager, dashboard):
        super().__init__(parent)
        self.habit = habit
        self.habit_manager = habit_manager
        self.dashboard = dashboard

        self.dropdown_visible = False # dropdown always starts off hidden

        # creates and sets nested frame
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(fill="x", pady=2) #expand horizontally with vertical padding

        # creates and sets title label
        self.title_label = ctk.CTkLabel(self.top_frame, text=self.habit.title, font=ctk.CTkFont(size=16))
        self.title_label.pack(side="left", padx=10)

        # creates and sets dropdown toggle button all the way to the right
        self.toggle_button = ctk.CTkButton(
            self.top_frame,
            text="˅",
            width=30,
            command=self.toggle_dropdown
        )
        self.toggle_button.pack(side="right", padx=(0, 5))

        # creates and sets delete button left of the toggle button
        self.delete_button = ctk.CTkButton(
            self.top_frame,
            text="X",
            width=30,
            fg_color="red",
            hover_color="#aa0000",
            command=self.confirm_delete
        )
        self.delete_button.pack(side="right", padx=(0, 5))

        self.dropdown_frame = ctk.CTkFrame(self) #creates dropdown frame

        # fills dropdown frame with habit details
        self.dropdown_info = ctk.CTkLabel(self.dropdown_frame, text=self.habit.description, wraplength=400)
        self.dropdown_info.pack(padx=10, pady=5)

    def toggle_dropdown(self):
        # unpacks dropdown frame if visible and changes button text
        if self.dropdown_visible:
            self.dropdown_frame.pack_forget()
            self.toggle_button.configure(text="˅")
        # sets dropdown frame if not visible and changes button text
        else:
            self.dropdown_frame.pack(fill="x")
            self.toggle_button.configure(text="-")
        self.dropdown_visible = not self.dropdown_visible #toggles visibility state

    def confirm_delete(self):
        # creates confirmation popup for habit deletion
        self.confirm_popup = ctk.CTkToplevel(self)
        self.confirm_popup.geometry("350x150")
        self.confirm_popup.title("Confirm Deletion")
        
        # sets popup to be modal, meaning it must be closed before interacting with the main window
        self.confirm_popup.transient(self.winfo_toplevel())
        self.confirm_popup.focus_set()
        self.confirm_popup.grab_set()

        # creates and sets centered confirmation message
        label = ctk.CTkLabel(
            self.confirm_popup,
            text=f"Are you sure you want to delete the habit '{self.habit.title}'?",
            wraplength=300,
            justify="center",
            font=ctk.CTkFont(size=14)
        )
        label.pack(pady=(20, 10), padx=20)

        # creates and sets buttons frame for delete and cancel buttons
        buttons_frame = ctk.CTkFrame(self.confirm_popup)
        buttons_frame.pack(pady=10)

        # creates and sets delete button using delete_and_close function
        delete_button = ctk.CTkButton(
            buttons_frame,
            text="Delete",
            fg_color="red",
            hover_color="#aa0000",
            width=100,
            command=self.delete_and_close
        )
        delete_button.pack(side="left", padx=10)

        # creates and sets cancel button to close popup without deleting habit
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            width=100,
            command=self.confirm_popup.destroy
        )
        cancel_button.pack(side="right", padx=10)

    def delete_and_close(self):
        # deletes habit, gets rid of habit card, and destroys confirmation popup
        self.habit_manager.delete_habit(self.habit)
        self.destroy()
        self.dashboard.refresh_habits()
        self.confirm_popup.destroy()
import os
from openai import OpenAI
import customtkinter as ctk
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #retrieves private API key from .env file

class Chatbot(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent) #initializes basic setup of app window inside parent (container)
        self.controller = controller
        self.chat_history = [ #initializes chat history for multi-turn conversation with AI
            {"role": "system", "content": "You are a friendly and humorous productivity assistant named Buddy that aims to uplift and encourage."}
        ] 

        # creates and sets text label
        label = ctk.CTkLabel(self, text="Chatbot", font=("Arial", 24))
        label.pack(pady=20)

        # creates and sets Home button
        ctk.CTkButton(self, text="Home", command=lambda: controller.show_frame("Dashboard")).pack(pady=10)

        # creates and sets chat display
        self.chat_display = ctk.CTkTextbox(self, height=400, state="disabled", wrap="word") #user can't type in it and long text wraps
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=10)

        # cretes and sets user input area
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=10, pady=(0,10)) #margin only on bottom

        # creates and sets user input textbox
        self.chat_input = ctk.CTkTextbox(input_frame, height=30, wrap="word")
        self.chat_input.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=5) #creats texbox on left side with padding for button

        # creates and sets send button
        send_button = ctk.CTkButton(input_frame, text="Send", command=self.send_message)
        send_button.pack(side="right", pady=5)

    def send_message(self):
        message = self.chat_input.get("1.0", "end-1c").strip()
        if not message:
            return #will not send empty messages
        
        # enables display, inserts message, then disables display again
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"You: {message}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end") #scrolls to bottom of chat
        self.chat_input.delete("1.0", "end") #clears input box

        self.chat_history.append({"role": "user", "content": message}) #appends user message to chat history

        try:
            response = client.chat.completions.create( #makes request to OpenAI API with "chat-style completion"
                model="gpt-3.5-turbo", #specifies model to use
                messages=self.chat_history #gives chat history to API for context
            )
            reply = response.choices[0].message.content.strip() #stores content of first API output in response object
            self.chat_history.append({"role": "assistant", "content": reply}) #appends AI reply to chat history
        # handles errors that occur while calling API
        except Exception as e:
            reply = f"Error: {e}"

        # enables display, inserts reply, then disables display again
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"Buddy: {reply}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
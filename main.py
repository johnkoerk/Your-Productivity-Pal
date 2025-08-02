from ui.framework import Framework
import customtkinter as ctk

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = Framework()
    app.mainloop()
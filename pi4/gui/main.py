import tkinter as tk
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.wm_title("Pi Deck: Touchscreen Client")
        # self.
    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
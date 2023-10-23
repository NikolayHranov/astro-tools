import tkinter as tk
from tkinter import ttk


APP_NAME = "Astro Tools"


class Styles(ttk.Style):
    def __init__(self):
        super().__init__()
        self.configure("Title.TLabel", font=("Arial", 26), background="#21212e", foreground="white")


class MainWin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(bg="#21212e")
        self.title(APP_NAME)

        self.appinfoFrame = tk.Frame(self)
        self.appinfoFrame.pack(padx=10, pady=10, anchor="nw")
        self.appinfoFrame.title = ttk.Label(self.appinfoFrame, text=APP_NAME, style="Title.TLabel")
        self.appinfoFrame.title.pack()

        self.navigationFrame = tk.Frame(self)
        self.navigationFrame.pack(padx=20, pady=20, anchor="ne")
        self.navigationFrame.button_stack = ttk.Button(self.navigationFrame, text="Stack images", width=20, command=lambda:self.navigate("stacking"))
        self.navigationFrame.button_stack.pack()
    def navigate(self, location):
        match location:
            case "stacking":
                pass


class StackWin(tk.Toplevel):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    app = MainWin()
    styles = Styles()
    

    app.mainloop()
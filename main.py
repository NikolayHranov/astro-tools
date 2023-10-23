import tkinter as tk
from tkinter import ttk


APP_NAME = "AnlysIMG"


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
        self.appinfoFrame.pack(anchors="nw", padx=10, pady=10)
        self.appinfoFrame.title = ttk.Label(self.appinfoFrame, text=APP_NAME, style="Title.TLabel")
        self.appinfoFrame.title.pack()

        self.navigationFrame = tk.Frame(self)
        self.navigationFrame.pack(anchor="ne", padx=10, pady=10)
        self.navigationFrame.button = ttk.Button(self.navigationFrame, text="Button")
        self.navigationFrame.button.pack()


if __name__ == "__main__":
    app = MainWin()
    styles = Styles()
    

    app.mainloop()
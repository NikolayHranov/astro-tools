import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
import glob
import re
import os


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
        self.navigationFrame.button_stack = ttk.Button(self.navigationFrame, text="Stack images", width=20, command=lambda: self.navigate("stacking"))
        self.navigationFrame.button_stack.pack()
    def navigate(self, location):
        match location:
            case "stacking":
                global stacking_win
                stacking_win = StackWin()
                

class StackWin(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.config(bg="#21212e")
        self.title("AutoStacker")

        self.t = ttk.Label(self, text=APP_NAME, style="Title.TLabel")
        self.t.pack()

        self.stack_button = ttk.Button(self, text="Start stacking", width=20, command=lambda: self.stack())
        self.stack_button.pack()

    
    def stack(self):
        global main_path
        main_path = fd.askdirectory()
        filters = ["R", "B", "V"]
        paths = {"darks": "DARKS", "flats": "FLATS", "darkflats": "DARKFLATS", "lights": "LIGHTS"}
        print("Stacking...\n\n")
        for filter in filters:
            darks = self.get(paths["darks"], filter)
            flats = self.get(paths["flats"], filter)
            darkflats = self.get(paths["darkflats"], filter)
            lights = self.get(paths["lights"], filter)
        
            print(f'''
                Stacking for filter {filter}:
                -----------

                Darks:
                {darks}

                Darkflats:
                {darkflats}

                Flats:
                {flats}

                Lights:
                {lights}
                ''')
    
            mDarks = self.medianfr(darks)
            mDarkflats = self.medianfr(darkflats)

            mFlats = self.substractfr(flats, mDarkflats)
            dLights = self.substractfr(lights, mDarks)

            processed = self.dividefr(dLights, mFlats)

            print(processed)



    '''
    Functions medianfr(), substractfr() and dividefr() needs to be added!!!
    Functionality:
    Either get the median frame, substract frames or devide frames
    Every function should be executed for every frame from the given dictionary
    and the operation should be complited separately for values with different keys
    '''

    def medianfr(self, fr):
        return None

    def subtractfr(self, b, s):
        return None

    def dividefr(self, b, d):
        return None
    
    def get(self, path, filter):
        folder_path = f"{main_path}/images/{path}"
        file_pattern = f"*_{filter}_*_*s_*"
        files = glob.glob(os.path.join(folder_path, file_pattern))
        print(files)

        value_pattern = r"_(\d+)s_"

        values = []

        for file in files:
            match_ = re.search(value_pattern, file)
            if match_:
                second_star_value = match_.group(1)
                values.append(second_star_value)

        file_distribution = {}

        for value in values:
            pattern = f"*_{filter}_*_{value}s_*"
            file_distribution[value] = glob.glob(os.path.join(folder_path, pattern))

        return file_distribution


if __name__ == "__main__":
    app = MainWin()
    styles = Styles()
    

    app.mainloop()

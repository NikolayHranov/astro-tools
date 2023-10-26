import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import os

root = tk.Tk()
root.geometry("500x500")
root.title("photometry NP")

def printtk(text1):
    label = tk.Label(root, text=text1)
    label.pack()

selected_light_directory = None
selected_dark_directory = None
selected_darkflat_directory = None
selected_flat_directory = None
selected_end_directory = None

def select_light_directory():
    global selected_light_directory
    selected_light_directory = filedialog.askdirectory(title="select light directory")
    light = "light: "+selected_light_directory
    printtk(light)

def select_dark_directory():
    global selected_dark_directory
    selected_dark_directory = filedialog.askdirectory(title="select dark directory")
    dark = "dark: "+selected_dark_directory
    printtk(dark)

def select_darkflat_directory():
    global selected_darkflat_directory
    selected_darkflat_directory = filedialog.askdirectory(title="select darkflat directory")
    darkflat = "darkflat: "+selected_darkflat_directory
    printtk(darkflat)

def select_flat_directory():
    global selected_flat_directory
    selected_flat_directory = filedialog.askdirectory(title="select flat directory")
    flat = "flat: "+selected_flat_directory
    printtk(flat)

def select_end_directory():
    global selected_end_directory
    selected_end_directory = filedialog.askdirectory(title="select end directory")
    end = "end: "+selected_end_directory
    printtk(end)

button = tk.Button(root, text="Select light directory", command=select_light_directory)
button.pack()

button = tk.Button(root, text="Select dark directory", command=select_dark_directory)
button.pack()

button = tk.Button(root, text="Select darkflat directory", command=select_darkflat_directory)
button.pack()

button = tk.Button(root, text="Select flat directory", command=select_flat_directory)
button.pack()

button = tk.Button(root, text="Select end directory", command=select_end_directory)
button.pack()




root.mainloop()







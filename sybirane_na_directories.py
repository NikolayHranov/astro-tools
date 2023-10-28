import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import os
import numpy as np
from astropy.io import fits
import statistics as st
def printtk(text1):
        label = tk.Label(root, text=text1)
        label.pack()
def collect_directories():
    global root    
    root = tk.Tk()
    root.geometry("500x500")
    root.title("photometry NP")

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

    directories = []
    return directories

def list_files(directory):
    return os.listdir(directory)    

def creat_master_dark(darks):
    fitsFile=darks[0]
    light = fits.open(fitsFile)
    data1 = light[0].data
    data = np.array(data1)
    dimensions = data.shape
    dimensions3D = (int(len(darks)),) + dimensions
    masterDark3D = np.zeros(dimensions3D)
    z = 0
    for dark in darks:
        dark = fits.open(dark)
        dark = np.array(dark[0].data)
        for x in range(dimensions3D[2]):
            for y in range(dimensions3D[1]):
                masterDark3D[z, y, x] = dark[y, x]
                z += 1
    
    masterDark = np.zeros(dimensions)
    for x in range(dimensions[1]):
        for y in range(dimensions[0]):
            values = []
            for i in range(len(darks)):
                values.append(masterDark3D[i, y, x])
                masterDark[y, x] = st.median(values)

    return masterDark


def after_start():

    lights = list_files(selected_light_directory)
    darks = list_files(selected_dark_directory)
    flats = list_files(selected_flat_directory)
    darkflats = list_files(selected_darkflat_directory)

    print("nfen")
    #master_dark = creat_master_dark(darks)
    #master_darkflat = creat_master_dark(darkflats)

def eror():
    printtk("eror")
def main():
    collect_directories()
    

    if selected_dark_directory!=None and selected_darkflat_directory!=None and selected_end_directory!=None and selected_flat_directory!=None and selected_light_directory!=None:
        command_start = after_start
    else:
        command_start = eror

    button = tk.Button(root, text="start", command=command_start)
    button.pack()
 
    


if __name__=="__main__":
    main()
    
root.mainloop()



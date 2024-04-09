from astropy.io import fits
import numpy as np 
import statistics as st
import os
from os import walk

def creat_master_dark(darks_directory):
    darks1 = os.listdir(darks_directory)

    darks = []

    for dark in darks1:
        directory = "/home/petar-popov/Desktop/darks_venus/" + dark
        darks.append(directory)
    fitsFile=darks[0]
    light = fits.open(fitsFile)
    data1 = light[0].data
    data = np.array(data1)
    dimensions = data.shape
    dimensions3D = (int(len(darks)),) + dimensions
    masterDark3D = np.zeros(dimensions3D)

    for dark in darks:
        z = darks.index(dark)
        dark = fits.open(dark)
        dark = np.array(dark[0].data)
        for x in range(dimensions3D[2]):
            for y in range(dimensions3D[1]):
                masterDark3D[z, y, x] = dark[y, x]
    
    masterDark = np.zeros(dimensions)
    for x in range(dimensions[1]):
        for y in range(dimensions[0]):
            values = []
            for i in range(len(darks)):
                values.append(masterDark3D[i, y, x])
                masterDark[y, x] = st.median(values)

    return masterDark

mdark = creat_master_dark(darks_directory="/home/petar-popov/Desktop/darks_venus")
#darks = os.listdir("/home/petar-popov/Desktop/darks_venus")
#print(darks)
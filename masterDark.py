from astropy import fits
import numpy as np 
import statistics as st
import os
def creat_master_dark(darks_directory):
    darks = os.dirlist(darks_directory)
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
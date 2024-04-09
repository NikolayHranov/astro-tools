import numpy as np
from astropy.io  import fits

def makeDark(darks):

  dark1 = fits.open(darks[0])         #here it opens the first dark frame in order to get the size of the images
  dark1 = np.array(dark1[0].data)
  dimensions = dark1.shape

  dimensions3D= (int(len(darks)),) + dimensions   #combine the darks to a 3d array
  masterDark3D = np.zeros(dimensions3D)
  z = 0
  for dark in darks:
    dark = fits.open(dark)
    dark = np.array(dark[0].data)
    for x in range(dimensions3D[2]):
      for y in range(dimensions3D[1]):
        masterDark3D[z, y, x] = dark[y, x]
    z += 1
  masterDark = np.zeros(dimensions)  #take the median  over the third dimension (the z-axis) and make it to 2d array which is the final master dark
  for x in range(dimensions[1]):
    #if x%100 == 0:
    #  print(str(round((x/dimensions[1]),4)*100)+"%") #just to track progress, not neccery for the code to work
    for y in range(dimensions[0]):
      values = []
      for i in range(len(darks)):
        values.append(masterDark3D[i, y, x])
      masterDark[y, x] = np.median(values)
  return  masterDark
#return the np array 'masterDark' with the median value from each set of dark frames and have to be substracted from the lights


def makeFlat(flats, darkflats):
  darkFlat = makeDark(darkflats)
  
  flat1 = fits.open(flats[0])
  flat1 = np.array(flat1[0].data)
  dimensions = flat1.shape

  dimensions3D = (len(flats),) + dimensions
  masterFlat3D =  np.zeros(dimensions3D)
  z = 0
  for flat in flats:
    flat = fits.open(flat)
    flat= np.array(flat(0).data)
    flat = flat - darkFlat
    for x in range(dimensions3D[2]):
      for y in range(dimensions3D[1]):
        masterFlat3D[z, y, x] = flat[y, x]
    z += 1

  masterFlat = np.zeros(dimensions)

  for x in range(dimensions[1]):
    #if x%100 == 0:
    #  print(str(round((x/dimensions[1]),4)*100)+"%") #just to track progress, not neccery for the code to work
    for y in range(dimensions[0]):
      values = []
      for i in range(len(darks)):
        values.append(masterFlat3D[i, y, x])
      masterFlat[y, x] = np.median(values)

  masterFlat = masterFlat / np.median(masterFlat)
  return masterFlat

def lights(lights, darks, darkflats, flats):
  dark = makeDark(darks)
  flat = makeFlat(flats, darkflats)

  for light in  lights:
    light = fits.open(light)
    light = np.array(light[0].data)
    light = light - dark
    light = light / flat

    


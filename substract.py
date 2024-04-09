import numpy as np
from astropy.io  import fits

darks = [] #list of the directories of the dark frames


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
  if x%100 == 0:
    print(str(round((x/dimensions[1]),4)*100)+"%") #just to track progress, not neccery for the code to work
  for y in range(dimensions[0]):
    values = []
    for i in range(len(darks)):
      values.append(masterDark3D[i, y, x])
    masterDark[y, x] = np.median(values)

#return the np array 'masterDark' with the median value from each set of dark frames and have to be substracted from the lights

#save the master dark frame if you want
'''
hdu = fits.PrimaryHDU(masterDark)
hdu.header['COMMENT'] = 'Master Dark Frame'
hdu.writeto('Master_Dark.fits',overwrite=True)
'''
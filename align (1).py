# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 09:41:44 2021

@author: Tuser
"""

from astropy.io import fits
import astroalign as aa
import numpy as np
import glob
from datetime import datetime

startTime = datetime.now()
# C:/Users/admin/Desktop/Бели брези 2023/Нова папка/OR_And_3/pipelineout1/*Processed_*.fits
target = fits.open(glob.glob('C:/Users/admin/Desktop/Бели брези 2023/Нова папка/OR_And_3/pipelineout1/*Processed_*.fits')[0])[0].data.byteswap().newbyteorder()
for i in range(len(glob.glob('C:/Users/admin/Desktop/Бели брези 2023/Нова папка/OR_And_3/pipelineout1/*Processed_*.fits'))):
    if i == 0:
        hdu_al = fits.PrimaryHDU(fits.open(glob.glob('C:/Users/admin/Desktop/Бели брези 2023/Нова папка/OR_And_3/pipelineout1/*Processed_*.fits')[i])[0].data,\
                                  fits.open(glob.glob('C:/Users/admin/Desktop/Бели брези 2023/Нова папка/OR_And_3/pipelineout1/*Processed_*.fits')[i])[0].header)
        hdu_al.writeto('aligned_' + str(i) + '.fits')
    else:
        source = fits.open(glob.glob('C:/Users/admin/Desktop/Бели брези 2023/Нова папка/OR_And_3/pipelineout1/*Processed_*.fits')[i])[0].data.byteswap().newbyteorder()
        try:
            registered_image, footprint = aa.register(source, target)
            hdu_al = fits.PrimaryHDU(registered_image, fits.open(glob.glob('C:/Users/admin/Desktop/Бели брези 2023/Нова папка/OR_And_3/pipelineout1/*Processed_*.fits')[i])[0].header)
            hdu_al.writeto('aligned_' + str(i) + '.fit')
        except:
            continue
        
        
        
     
print(datetime.now() - startTime)

# import tkinter as tk
# from tkinter import ttk
# import tkinter.filedialog as fd
import glob
from collections import defaultdict
# import re
import os
from astropy.io import fits
import numpy as np

FITS_KEYWORDS = {"imgtype": "IMAGETYP", "exposure": "EXPOSURE", "filter": "FILTER"}
PATHS = {"darks": "DARKS", "flats": "FLATS", "darkflats": "DARKFLATS", "lights": "LIGHTS"}
# value_pattern = r"_(\d+)s_"
# file_pattern = f"*_{filter}_*_*s_*"

class AstroDataBase():
    def __init__(self):
        self.variables = {}
        self.df = {}
        self.images = {}


class AstroImages():
    def __init__(self, *, main_path, paths=PATHS, metakw = FITS_KEYWORDS):
        self.main_path = main_path
        self.paths = paths
        self.metakw = metakw

        self.darks = self.get(paths["darks"])
        self.flats = self.get(paths["flats"])
        self.darkflats = self.get(paths["darkflats"])
        self.lights = self.get(paths["lights"])
    
    def stackall(self):
        self.mDarks = self.mediandarkfr(self.darks)
        self.mDarkflats = self.mediandarkfr(self.darkflats)

        self.sFlats = self.subtractfr(self.flats, self.mDarkflats)
        self.mFlats = self.medianflatfr(self.sFlats)
        
        self.dLights = self.substractfr(self.lights, self.mDarks)
        self.processed = self.dividefr(self.dLights, self.mFlats)
    
    def get(self, path):
        folder_path = f"{self.main_path}/images/{path}"
        file_pattern = f"*.fits"
        files = glob.glob(os.path.join(folder_path, file_pattern))
        print(files)

        # value_pattern = r"_(\d+)s_"

        # values = []
        sorted_frames = {}

        for file in files:
            imgf = fits.open(file)
            exposure = imgf.header[self.metakw["exposure"]]
            filter = imgf.header[self.metakw["filter"]]
            try:
                type(sorted_frames[filter])
            except:
                sorted_frames[filter] = {}
            try:
                type(sorted_frames[filter][exposure])
            except:
                sorted_frames[filter][exposure] = []
            sorted_frames[filter][exposure].append(imgf.data)
                

            # match_ = re.search(value_pattern, file)
            # if match_:
            #     second_star_value = match_.group(1)
            #     values.append(second_star_value)

        # file_distribution = {}

        # for value in values:
        #     pattern = f"*_{filter}_*_{value}s_*"
        #     file_distribution[value] = glob.glob(os.path.join(folder_path, pattern))

        return sorted_frames
    
    def mediandarkfr(self, fr):
        # processed = {}
        # for filter, exposures in fr.items():
        #     processed[filter] = {}
        #     for exposure, frames in exposures.items():
        #         frames_data = [frame.data for frame in frames]
        #         data_stacked = np.stack(frames_data)
        #         processed[filter][exposure] = np.median(data_stacked, axis=0)
        # return processed
        processed = {}
        exposures = defaultdict(list)
        for d in fr.values():
            for key, value in d.items():
                exposures[key].extend(value)
        exposures = dict(exposures)
        for exposure, frames in exposures.items():
            data_stacked = np.stack(frames)
            processed[exposure] = [np.median(data_stacked, axis=0)]

    def medianflatfr(self, fr):
        processed = {}
        for filter, exposures in fr.items():
            # processed[filter] = {}
            frames_data = sum(exposures.value())
            # frames_data = [frame.data for frame in frames]
            data_stacked = np.stack(frames_data)
            processed[filter] = [np.median(data_stacked, axis=0)]
        return processed

    def subtractfr(self, b, s):
        processed = {}
        for filter, exposures in b.items():
            processed[filter] = {}
            for exposure, frames in exposures.items():
                processed[filter][exposure] = []
                for frame in frames:
                    result = frame - s[exposure]
                    processed[filter][exposure].append(result)
        return processed

    def dividefr(self, b, d):
        processed = {}
        for filter, exposures in b.items():
            processed[filter] = {}
            for exposure, frames in exposures.items():
                processed[filter][exposure] = []
                for frame in frames:
                    result = frame / d[filter]
                    processed[filter][exposure].append(result)
        return processed
    
    def save(self, processed, path, imgtype):
        for filter, exposures in processed.items():
            for exposure, frames in exposures.items():
                i = 0
                for frame in frames:
                    i += 1
                    header = {self.metakw["imgtype"]: imgtype, self.metakw["filter"]: filter, self.metakw["exposure"]: exposure}
                    fits.writeto(f"{self.main_path}/images/{path}/{imgtype}_{filter}_{exposure}_.fits", frame, header=header)
                del i



images = AstroImages(main_path=main_path)
images.stackall()
images.save(images.processed, path, "PROCESSED")
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

        self.darks = self.get(self.paths["darks"])
        self.flats = self.get(self.paths["flats"])
        self.darkflats = self.get(self.paths["darkflats"])
        self.lights = self.get(self.paths["lights"])
    
    def stackall(self):
        print("CREATING MASTERDARKS AND MASTERDARKFLATS")
        self.mDarks = self.mediandarkfr(self.darks)
        self.mDarkflats = self.mediandarkfr(self.darkflats)
        print("MASTERDARKS AND MASTERDARKFLATS CREATED")

        print("SUBSTRACTING MASTERDARKFLATS")
        self.sFlats = self.substractfr(self.flats, self.mDarkflats)
        print("MASTERDARKFLATS SUBSTRACTED")
        print("CREATING MASTERFLATS")
        self.mFlats = self.medianflatfr(self.sFlats)
        print("MASTERFLATS CREATED")

        print("CRETING PROCESSED")
        self.processed = self.subdivlightfr(self.lights, self.mDarks, self.mFlats)
        print("IMAGES STACKED")
    
    def get(self, path):
        folder_path = f"{self.main_path}/images/{path}"
        file_pattern = f"*.fits"
        files = glob.glob(os.path.join(folder_path, file_pattern))
        # print(files)

        # value_pattern = r"_(\d+)s_"

        # values = []
        sorted_frames = {}

        for file in files:
            imgf = fits.open(file)
            exposure = imgf[0].header[self.metakw["exposure"]]
            filter = imgf[0].header[self.metakw["filter"]]
            try:
                type(sorted_frames[filter])
            except:
                sorted_frames[filter] = {}
            try:
                type(sorted_frames[filter][exposure])
            except:
                if path == self.paths["lights"]:
                    sorted_frames[filter][exposure] = {"data": [], "header": []}
                else:
                    sorted_frames[filter][exposure] = []
            if path == self.paths["lights"]:
                sorted_frames[filter][exposure]["data"].append(imgf[0].data)
                sorted_frames[filter][exposure]["header"].append(imgf[0].header)
            else:
                sorted_frames[filter][exposure].append(imgf[0].data)
            print(f"{file} loaded!")
            

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
        return processed

    def medianflatfr(self, fr):
        print("Creating masterflats")
        processed = {}
        for filter, exposures in fr.items():
            print(f"Creating masterflat for {filter} filter")
            print(exposures)
            print(exposures.values())
            # processed[filter] = {}
            # frames_data = sum(exposures.values())
            frames_data = [item for sublist in exposures.values() for item in sublist]
            # frames_data = [frame.data for frame in frames]
            data_stacked = np.stack(frames_data)
            processed[filter] = [np.median(data_stacked, axis=0)]
            print(f"Masterflat for {filter} filter created")
        return processed

    def substractfr(self, b, s):
        print("Substracting")
        print(b, s)
        processed = {}
        for filter, exposures in b.items():
            processed[filter] = {}
            for exposure, frames in exposures.items():
                processed[filter][exposure] = []
                for frame in frames:
                    print(frame)
                    result = frame - s[exposure]
                    processed[filter][exposure].append(result)
        return processed

    def subdivlightfr(self, b, s, d):
        print("Dividing")
        print(b, d)
        processed = {}
        for filter, exposures in b.items():
            processed[filter] = {}
            for exposure, frames in exposures.items():
                processed[filter][exposure] = {"data": [], "header": []}
                for frame in frames["data"]:
                    result = (frame - s[exposure])/ d[filter]
                    processed[filter][exposure]["data"].append(result)
                print(f"frames[\"header\"] = {frames['header']}")
                for frame in frames["header"]:
                    print(f"Stupid frame: {type(frame)} = {frame}")
                    header = frame
                    header[self.metakw["imgtype"]] = "PROCESSED"
                    processed[filter][exposure]["header"].append(header)
        return processed
    
    def save(self, path=None):
        print("SAVING FILES")
        processed = self.processed
        for filter, exposures in processed.items():
            for exposure, frames in exposures.items():
                for i in range(len(frames["data"])):
                    imgtype = frames["header"][i][self.metakw["imgtype"]]
                    if path == None:
                        path = imgtype
                    # header = {self.metakw["imgtype"]: imgtype, self.metakw["filter"]: filter, self.metakw["exposure"]: exposure}
                    fits.writeto(f"{self.main_path}/images/{path}/{imgtype}_{filter}_{exposure}_{i}_.fits", frames["data"][i], header=frames["header"][i])
                    print(f"File {frames['header'][i]} saved at {self.main_path}/images/{path}/{imgtype}_{filter}_{exposure}_{i}_.fits")
                del i
        print("ALL FILES SAVED SUCCESSFULLY")



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.table import Table
import photutils.aperture as apr
import photutils.detection as det
from astropy.io import fits
from astropy.stats import mad_std
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backend_tools import ToolBase
from matplotlib.widgets import TextBox

featureNotAvailableMsg = "Feature not available at this veresion"


class PhotometryAnalysis():
    def __init__(self, img):
        self.picked = None
        self.fig, self.ax = plt.subplots()
        self.image, self.source = getSource(img)
        self.ax.imshow(self.image, vmin = 115, vmax = 170)
        self.ax.scatter(self.source["xcentroid"], self.source["ycentroid"], s=1, picker=True, pickradius=1,)
        self.ax.colorbar()

        self.standartsButton = ()

        self.fig.canvas.mpl_connect("pick_event", self.onPick)

    def inputBox(self):
        tbox = TextBox(self.ax, "Standart ID: ")
        std_id = int(tbox.on_submit(lambda text: text))
        return std_id

    def onPick(self, event):
        if isinstance(event.artist, plt.PathCollection):
            ind = event.ind[0]
            x_coord, y_coord = self.ax.collections[0].get_offsets()[ind]
            std_id = self.inputBox()
    


def getSource(img):
    image = fits.getdata(img)
    bg = np.median(image)
    std = mad_std(image)
    find = det.DAOStarFinder(fwhm=5, threshold=10*std)
    sources = find(image - bg)
    return image, sources


def getCoordRT(pC, p0, p1):
    T = pC
    trp0 = p0 + T
    op0 = trp0 - pC
    op1 = p1 - pC
    theta = np.arccos((np.dot(op0, op1))/(np.linalg.norm(op0) * np.linalg.norm(op1)))
    R = np.array[[np.cos(theta), -np.sin(theta)],
                 [np.sin(theta), np.cos(theta)]]
    return T, R


def coordConvertToAx():
    raise NotImplementedError(featureNotAvailableMsg)

def coordConvertToAstro():
    raise NotImplementedError(featureNotAvailableMsg)

def standartStars():
    raise NotImplementedError(featureNotAvailableMsg)


if __name__ == "__main__":
    phot = PhotometryAnalysis()
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.collections as mcl
from astropy.table import Table
from astropy.io.votable import parse
import photutils.aperture as apr
import photutils.detection as det
from astropy.io import fits
from astropy.stats import mad_std
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# from matplotlib.backend_tools import ToolBase
from matplotlib.widgets import TextBox

featureNotAvailableMsg = "Feature not available at this veresion"


class PhotometryAnalysis():
    def __init__(self, img, standards):
        self.deltamag = []
        self.standards = standards
        self.picked = None
        self.fig, self.ax = plt.subplots()
        self.image, self.source = getSource(img)
        print(self.source)
        self.mappable = self.ax.imshow(self.image, vmin = 40, vmax = 1000)
        self.stars = self.ax.scatter(self.source["xcentroid"], self.source["ycentroid"], color="m", s=2, alpha=0.2, picker=True, pickradius=1)
        self.fig.colorbar(self.mappable)

        self.standartsButton = ()

        self.fig.canvas.mpl_connect("pick_event", self.onPick)

    def inputBox(self):
        tbox = TextBox(self.ax, "Standart ID: ")
        print("...box defined...")
        std_id = int(tbox.on_submit(lambda text: text))
        print(f"...leaving function with return {std_id}")
        return std_id

    def onPick(self, event):
        print("Something clicked...")

        if isinstance(event.artist, mcl.PathCollection):
            ind = event.ind[0]
            # self.stars[ind].set_color("red")
            print("...star clicked...")
            x_coord, y_coord = self.ax.collections[0].get_offsets()[ind]
            print(f"...coords: {x_coord, y_coord}...")
            selected_row = self.source[(self.source["xcentroid"] == x_coord) & (self.source["ycentroid"] == y_coord)]
            print("...your row:")
            print(selected_row)
            print("...")
            if event.mouseevent.button == 1:
                mask = ~((self.source["xcentroid"] == x_coord) & (self.source["ycentroid"] == y_coord))
                self.source = self.source[mask]
                self.stars.remove()
                self.stars = self.ax.scatter(self.source["xcentroid"], self.source["ycentroid"], color="m", s=2, alpha=0.2, picker=True, pickradius=1)
                plt.draw()
                print("...star removed!")
            elif event.mouseevent.button == 3:
                print("...prepering input...")
                # std_id = self.inputBox()
                std_id = int(input())
                selected_row["stdmag"] = self.standards[self.standards["recno"] == str(std_id)]["Bmag"]
                self.deltamag.append(self.standards[self.standards["recno"] == std_id]["Bmag"] - selected_row["mag"])
                print(f"...deltamag: {self.deltamag}... star added!")
                print(f"Median : {np.median(self.deltamag)}")


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
    vot = parse("vizier_standards_ngc225.vot")
    votable = vot.get_first_table()
    table = Table(votable.array)
    print(table)
    print("-----------------------------------")
    phot = PhotometryAnalysis("images_225\stackedphotolightb.fits", table)

    plt.show()
    print("list:", phot.deltamag)
    print("median:", np.median(phot.deltamag))
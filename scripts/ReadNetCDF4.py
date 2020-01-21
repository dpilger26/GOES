"""
Reads the image data from a netcdf4 .nc file
"""
# ======================================================================================================================
import netCDF4 as net
import numpy as np
import matplotlib.pyplot as plt


# ======================================================================================================================
def readFile(filename: str, doPlot: bool = False):
    """
    Reads the image data out of a netcdf4 file
    :arg: filename: the full filename to the .nc file
    :arg: doPlot: whether or not to plot the image
    :return: np.ndarray
    """



    if doPlot:
        plt.figure()
        plt.imshow(image)
        plt.grid(b=False)

"""
Reads the image data from a netcdf4 .nc file
"""
# ======================================================================================================================
import datetime
from typing import Tuple

import netCDF4 as net
import numpy as np
import matplotlib.pyplot as plt


# ======================================================================================================================
# Constants
FILL_VALUE = 0x3fff
MAX_VALUE = 4095  # somewhat arbitrary for the SWIR data
EPOCH = [2000, 1, 1, 12, 0, 0]
EPOCH_SECS = (datetime.datetime(*EPOCH) - datetime.datetime.utcfromtimestamp(0)).total_seconds()


# ======================================================================================================================
def readImage(filename: str,
              doPlot: bool = False) -> Tuple[np.ndarray, str]:
    """
    Reads the image data out of a netcdf4 file

    Args:
        filename: the full filename to the .nc file
        doPlot: whether or not to plot the image

    Returns:
         np.ndarray of the image, start of scan time
    """
    data = net.Dataset(filename=filename, mode='r')
    
    if 'Rad' not in data.variables:
        raise RuntimeError(f'This netcdf4 file does not contain any image data.')

    image = np.array(data.variables['Rad'])
    image[image == FILL_VALUE] = np.nan

    startDateTime = data.variables['time_bounds'][0].data.item()
    dateAndTime = datetime.datetime.utcfromtimestamp(startDateTime + EPOCH_SECS).strftime("%m/%d/%Y %H:%M:%S")

    data.close()

    if doPlot:
        plotImage(image=image,
                  dateAndTime=dateAndTime)

    return image, dateAndTime


# ======================================================================================================================
def plotImage(image: np.ndarray,
              dateAndTime: str = None,
              **plotKwargs) -> plt.Figure:
    """
    Plots an image

    Args:
        image: the numpy array of the image, or filepath to the .nc file
        dateAndTime: the date and time of the image
        plotKwargs: the kwargs to pass to matplotlib imshow()

    Returns:
         np.ndarray
    """
    imageMin = np.nanmin(image)
    imageMax = np.nanmax(image)
    ptp = imageMax - imageMin
    cMax = ptp * 0.2 + imageMin

    fig, ax = plt.subplots(1, figsize=[9.5, 9.5])
    ax.imshow(X=image, clim=[imageMin, cMax], cmap='hot', **plotKwargs)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(b=False)
    if dateAndTime is not None:
        plt.title(dateAndTime)
    plt.tight_layout()
    plt.show()

    return fig

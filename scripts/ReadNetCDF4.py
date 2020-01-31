"""
Reads the image data from a netcdf4 .nc file
"""
# ======================================================================================================================
import datetime
from typing import Tuple, Union
import re

import netCDF4 as net
import numpy as np
import matplotlib.pyplot as plt

import DownloadData


# ======================================================================================================================
# Constants
EPOCH = [2000, 1, 1, 12, 0, 0]
EPOCH_SECS = (datetime.datetime(*EPOCH) - datetime.datetime.utcfromtimestamp(0)).total_seconds()
BAND_REGEX_STR = r'.*-RadF-M6C(\d{2})_.*'
BAND_REGEX = re.compile(BAND_REGEX_STR)


# ======================================================================================================================
def readImage(filename: str,
              doPlot: bool = False) -> Tuple[np.ndarray, str, Union[DownloadData.Band, None]]:
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

    startDateTime = data.variables['time_bounds'][0].data.item()
    dateAndTime = datetime.datetime.utcfromtimestamp(startDateTime + EPOCH_SECS).strftime("%m/%d/%Y %H:%M:%S")

    data.close()
    
    bandStr = BAND_REGEX.findall(filename)
    if len(bandStr) == 1:
        band = DownloadData.Band(int(bandStr[0]))
    else:
        print(f'Unable to parse the GEOS band from the filename\n{filename}')
        band = None
        
    if doPlot:
        plotImage(image=image,
                  dateAndTime=dateAndTime,
                  band=band)

    return image, dateAndTime, band


# ======================================================================================================================
def plotImage(image: np.ndarray,
              dateAndTime: str = None,
              band: DownloadData.Band = None,
              **plotKwargs) -> plt.Figure:
    """
    Plots an image

    Args:
        image: the numpy array of the image, or filepath to the .nc file
        dateAndTime: the date and time of the image
        band: the GEOS band
        plotKwargs: the kwargs to pass to matplotlib imshow()

    Returns:
         np.ndarray
    """
    fig, ax = plt.subplots(1, figsize=[9.5, 9.5])
    ax.imshow(X=image, **plotKwargs)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(b=False)
    title = ''
    if band is not None:
        title += f'Band {band.name.replace("_", "-")}    '
    if dateAndTime is not None:
        title += dateAndTime
    plt.title(title)
    plt.tight_layout()
    plt.show()

    return fig

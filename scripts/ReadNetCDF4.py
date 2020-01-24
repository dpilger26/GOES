"""
Reads the image data from a netcdf4 .nc file
"""
# ======================================================================================================================
import netCDF4 as net
import numpy as np
import matplotlib.pyplot as plt


# ======================================================================================================================
# Constants
FILL_VALUE = 0x3fff


# ======================================================================================================================
def readImage(filename: str, doPlot: bool = False) -> np.ndarray:
    """
    Reads the image data out of a netcdf4 file

    Args:
        filename: the full filename to the .nc file
        doPlot: whether or not to plot the image

    Returns:
         np.ndarray
    """
    data = net.Dataset(filename=filename, mode='r')
    
    if 'Rad' not in data.variables:
        raise RuntimeError(f'This netcdf4 file does not contain any image data.')

    image = np.array(data.variables['Rad'])
    data.close()

    image[image == FILL_VALUE] = np.nan
    image -= np.nanmin(image)

    if doPlot:
        # TODO - add timestamp to figure
        imageMin = np.nanmin(image)
        imageMax = np.nanmax(image)
        ptp = imageMax - imageMin
        cMax = ptp * 0.05 + imageMin

        fig, ax = plt.subplots(1)
        ax.imshow(X=image, clim=[imageMin, cMax])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.grid(b=False)
        plt.show()

    return image

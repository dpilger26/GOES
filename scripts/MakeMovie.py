"""
Makes a movie of the previously downloaded GEOS data
"""
import os
import pathlib
from typing import List, Tuple, Union

import numpy as np
import matplotlib.pyplot as plt

import DownloadData
import ReadNetCDF4
import VideoWriter

plt.style.use('myDarkStyle.mplstyle')

# ======================================================================================================================
# Constants
FILL_VALUE = 0x3fff
FILL_VALUE2 = 1023
CMAP = 'hot'
FPS = 12
FIG_SIZE = [16, 9]


# ======================================================================================================================
class MovieFigure:
    """
    A Simple class for holding the figure to made into a movie
    """
    def __init__(self,
                 numImages: int = 1,
                 figsize: Tuple[float, float] = (19.2, 10.8)):
        """
        Constructor

        Args:
            numImages: the number of images wide
            figsize: the overall figure size
        """
        self._fig, self._axes = plt.subplots(nrows=1,
                                             ncols=numImages,
                                             figsize=figsize)
        self._setup()

    # ==================================================================================================================
    @property
    def fig(self) -> plt.Figure:
        """
        Returns the figure handle
        """
        return self._fig

    # ==================================================================================================================
    def updateFigure(self,
                     axisNumber: int,
                     image: np.ndarray,
                     dateAndTime: str,
                     band: DownloadData.Band,
                     **plotKwargs) -> None:
        """
        Updates the figure

        Args:
            axisNumber: the axis number to update
            image: the numpy array of the image, or filepath to the .nc file
            dateAndTime: the date and time of the image
            band: the GEOS band
            plotKwargs: the kwargs to pass to matplotlib imshow()
        """
        if axisNumber >= len(self._axes):
            raise IndexError(f'axisNumber={axisNumber} is out of the range [0, {len(self._axes)})')

        self._axes[axisNumber].imshow(X=image, **plotKwargs)
        title = f'Band {band.name.replace("_", "-")}    {dateAndTime}'
        self._axes[axisNumber].set_title(title)

    # ==================================================================================================================
    def update(self) -> None:
        """
        Updates the figure handle
        """
        self._fig.canvas.draw()

    # ==================================================================================================================
    def _setup(self) -> None:
        """
        Sets up the figure axes
        """
        for axis in self._axes:
            axis.set_xticks([])
            axis.set_yticks([])
            axis.set_yticklabels([])
            axis.set_xticklabels([])
            axis.grid(b=False)
            axis.set_title('')

        plt.tight_layout()


# ======================================================================================================================
def makeMovie(dataDirs: List[str],
              outputDir: str,
              outputName: str,
              cMax: Union[float, List[float]] = None) -> None:
    """
    Makes a movie of the data found in the input directory.  Expects the data to 
    be orginized into day directories under dataDir

    Args:
        dataDirs: the data directory
        outputDir: the output directory to save the movie to
        outputName: the name of the output movie file
        cMax: list of maximum of the clim
    """
    if not os.path.isdir(outputDir):
        # attempt to make the output directory if it doesn't already exist
        os.mkdir(outputDir)

    vw = VideoWriter.VideoWriter(filename=os.path.join(outputDir, outputName),
                                 fps=FPS,
                                 isColor=True)

    allFiles = list()
    for dataDir in dataDirs:
        allFiles.append(getAllImageFiles(dataDir=dataDir))

    numFiles = [len(files) for files in allFiles]
    if numFiles.count(numFiles[0]) != len(numFiles):
        raise RuntimeError(f'Different number of image files in the data directories')

    for fileIdx in range(len(allFiles[0])):
        # matplotlib appears to be a memory hog for some reason, so instantiate a new fig for each set of files
        # instead of simply updating...
        movieFig = MovieFigure(numImages=len(dataDirs),
                               figsize=FIG_SIZE)

        for dirIdx in range(len(allFiles)):
            file = allFiles[dirIdx][fileIdx]
            print(f'Processing File {file}')

            image, dateAndTime, band = ReadNetCDF4.readImage(filename=str(file),
                                                             doPlot=False)

            # a bit of cleanup
            image[image == FILL_VALUE] = np.nan
            image[image == FILL_VALUE2] = np.nan

            cLimMax = None  # get rid of IDE warning
            if cMax is not None:
                if type(cMax) is list:
                    cLimMax = cMax[dirIdx]
                elif type(cMax) is float:
                    cLimMax = cMax
            else:
                cLimMax = np.nanmax(image)

            movieFig.updateFigure(axisNumber=dirIdx,
                                  image=image,
                                  dateAndTime=dateAndTime,
                                  band=band,
                                  clim=[0, cLimMax],
                                  cmap=CMAP)
        movieFig.update()
        vw.addMatplotlibFigureHandle(fig=movieFig.fig,
                                     doPlot=False)


# ======================================================================================================================
def getAllImageFiles(dataDir: str) -> List[pathlib.Path]:
    """
    Return all of the image files in dataDir. Assumes a folder structure of days and hours beneath

    Args:
        dataDir: the data directory

    Returns:
        list of files
    """
    if not os.path.isdir(dataDir):
        raise RuntimeError(f'Input directory can not be found\n\t{dataDir}')

    files = list()
    dayDirs = os.listdir(dataDir)
    for dayDir in dayDirs:
        fullDayDir = os.path.join(dataDir, dayDir)
        if not os.path.isdir(fullDayDir):
            continue

        hourDirs = os.listdir(fullDayDir)
        for hourDir in hourDirs:
            fullHourDir = os.path.join(fullDayDir, hourDir)

            files.extend(pathlib.Path(fullHourDir).glob('*.nc'))

    return files


# ======================================================================================================================
if __name__ == '__main__':
    MOVIE_NAME = 'GOES_16'
    OUTPUT_DIR = os.path.join(pathlib.Path(os.path.abspath(__file__)).parent, '..', 'movie')
    DATA_TOP_DIR = os.path.join(pathlib.Path(os.path.abspath(__file__)).parent, '..', 'data')

    DATA_DIRS = list()
    DATA_DIRS.append(os.path.join(DATA_TOP_DIR, 'BLUE_1'))
    DATA_DIRS.append(os.path.join(DATA_TOP_DIR, 'SWIR_7'))

    CMAX = [600, 4]

    makeMovie(dataDirs=DATA_DIRS,
              outputDir=OUTPUT_DIR,
              outputName=MOVIE_NAME,
              cMax=CMAX)

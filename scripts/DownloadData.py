"""
Simple script for downloading GOES data from AWS
"""
# ======================================================================================================================
import os
import pathlib
from enum import Enum
from typing import List, Union

import s3fs


# ======================================================================================================================
# Constants
AWS_BUCKETS = 's3://noaa-goes{SCID}/ABI-L1b-RadF/{year}/{dayOfYear:03}/{hour:02}/*-M6C{band:02}_*'


# ======================================================================================================================
class SCID(Enum):
    """
    The goes spacecraft id
    """
    SCID_16 = 16
    SCID_17 = 17


# ======================================================================================================================
class Band(Enum):
    """
    The goes detection band
    """
    BLUE_1 = 1
    RED_2 = 2
    VEGGIE_3 = 3
    CIRRUS_4 = 4
    SNOW_ICE_5 = 5
    CLOUD_PARTICLE_6 = 6
    SWIR_7 = 7
    UPPER_TROPOSHERE_8 = 8
    MID_TROPOSHERE_9 = 9
    LOW_TROPOSHERE_10 = 10
    CLOUD_TOP_11 = 11
    OZONE_12 = 12
    CLEAN_LWIR_13 = 13
    LWIR_14 = 14
    DIRTY_LWIR_14 = 15
    CO2_LWIR_16 = 16


# ======================================================================================================================
def download(outputDir: str,
             scid: SCID,
             band: Band,
             year: int,
             dayOfYear: Union[int, List[int]],
             hour: Union[int, List[int]]) -> List[str]:
    """
    Downloads the netcdf4 files from AWS

    Args:
        outputDir: the directory to save the downloaded files.  If the directory does not exist it
                   will attempt to be created
        scid: the spacecraft id
        band: the detection band
        year: the year
        dayOfYear: the day of the year
        hour: the hour of the day

    Returns:
        np.ndarray
    """
    if not os.path.isdir(outputDir):
        os.mkdir(outputDir)

    if type(dayOfYear) is not list:
        dayOfYear = [dayOfYear]

    if type(hour) is not list:
        hour = [hour]

    bandDir = os.path.join(outputDir, f'{band.name}')
    if not os.path.isdir(bandDir):
        os.mkdir(bandDir)

    fs = s3fs.S3FileSystem(anon=True)

    downloadedFiles = list()
    for theDay in dayOfYear:
        if theDay < 0 or theDay > 365:
            print(f'Input dayOfYear={theDay} is not valid. Valid range is [0, 365]')
            continue

        dayDir = os.path.join(bandDir, f'day{theDay:03}')
        if not os.path.isdir(dayDir):
            os.mkdir(dayDir)

        for theHour in hour:
            if theHour < 0 or theHour > 23:
                print(f'input hour={theHour} is not valid. valid range is [0, 23]')
                continue

            hourDir = os.path.join(dayDir, f'hour{theHour:02}')
            if not os.path.isdir(hourDir):
                os.mkdir(hourDir)

            files = fs.glob(AWS_BUCKETS.format(SCID=scid.value,
                                               year=year,
                                               dayOfYear=theDay,
                                               hour=theHour,
                                               band=band.value))

            if len(files) == 0:
                print(f'No data files found for '
                      f'scid={scid.name} '
                      f'year={year} '
                      f'dayOfYear={theDay} '
                      f'hour={theHour} '
                      f'band={band.name}')
                continue

            for file in files:
                path = pathlib.Path(file)
                newName = os.path.join(hourDir, path.name)

                print(f'Downloading {file}...')
                fs.get(file, newName)
                downloadedFiles.append(newName)

    return downloadedFiles


# ======================================================================================================================
if __name__ == '__main__':
    CURRENT_DIR = pathlib.Path(__file__).parent.absolute()
    FILES = download(outputDir=os.path.join(CURRENT_DIR, r'..\data\test'),
                     scid=SCID.SCID_16,
                     band=Band.SWIR_7,
                     year=2019,
                     dayOfYear=list(range(200, 205)),
                     hour=list(range(24)))

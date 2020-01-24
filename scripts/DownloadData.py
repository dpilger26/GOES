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
FILL_VALUE = 0x3fff
AWS_BUCKETS = 's3://noaa-goes{SCID}/ABI-L1b-RadF/{year}/{dayOfYear:03}/{hour:02}'


# ======================================================================================================================
class SCID(Enum):
    """
    The goes spacecraft id
    """
    SCID16 = 16
    SCID17 = 17


# ======================================================================================================================
def download(outputDir: str,
             scid: SCID,
             year: int,
             dayOfYear: Union[int, List[int]],
             hour: Union[int, List[int]]) -> List[str]:
    """
    Downloads the netcdf4 files from AWS

    Args:
        outputDir: the directory to save the downloaded files.  If the directory does not exist it
                   will attempt to be created
        scid: the spacecraft id
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

    fs = s3fs.S3FileSystem(anon=True)

    downloadedFiles = list()
    for theDay in dayOfYear:
        if theDay < 0 or theDay > 365:
            print(f'Input dayOfYear={theDay} is not valid. Valid range is [0, 365]')
            continue

        dayDir = os.path.join(outputDir, f'day{theDay:03}')
        if not os.path.isdir(dayDir):
            os.mkdir(dayDir)

        for theHour in hour:
            if theHour < 0 or theHour > 23:
                print(f'input hour={theHour} is not valid. valid range is [0, 23]')
                continue

            hourDir = os.path.join(dayDir, f'hour{theHour:02}')
            if not os.path.isdir(hourDir):
                os.mkdir(hourDir)

            files = fs.ls(AWS_BUCKETS.format(SCID=scid,
                                             year=year,
                                             dayOfYear=theDay,
                                             hour=theHour))

            if len(files) == 0:
                print(f'No data files found for scid={scid} year={year} dayOfYear={theDay} hour={theHour}')
                continue

            for file in files:
                path = pathlib.Path(file)
                newName = os.path.join(hourDir, path.name)

                print(f'Downloading {file}...')
                fs.get(file, newName)
                downloadedFiles.append(newName)

    return downloadedFiles

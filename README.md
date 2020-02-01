# GOES
Tools for working with data from the [Geostationary Operational Environmental Satellite](https://en.wikipedia.org/wiki/Geostationary_Operational_Environmental_Satellite) system

[![GOES-16](https://raw.githubusercontent.com/dpilger26/GOES/master/thumbnail.png)](https://www.youtube.com/watch?v=zNCElNnWMUA&feature=youtu.be)

## Required Python Packages
[numpy](https://numpy.org/)  
```
pip install numpy
```
[matplotlib](https://matplotlib.org/)  
```
pip install matplotlib
```
[netcdf4](https://unidata.github.io/netcdf4-python/netCDF4/index.html)  
```
pip install netcdf4
```
[s3fs](https://s3fs.readthedocs.io/en/latest/)
```
pip install s3fs
```
[opencv](https://docs.opencv.org/master/)
```
pip install opencv-python
```

## Python Tools/Scripts  
### [DownloadData.py](https://github.com/dpilger26/GOES/blob/master/scripts/DownloadData.py)
A simple tool for downloading GOES netcdf4 files from AWS buckets using Python's s3fs library.  More details can be found from [here](http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/goes16_download.cgi).  

### [ReadNetCDF4.py](https://github.com/dpilger26/GOES/blob/master/scripts/ReadNetCDF4.py)
A simple tool for extracting and plotting the GOES imagery data from the netcdf4 files.

### [VideoWriter.py](https://github.com/dpilger26/GOES/blob/master/scripts/VideoWriter.py)
A basic wrapper class around the OpenCV VideoWriter for writing images to a video.

### [MakeMovie.py](https://github.com/dpilger26/GOES/blob/master/scripts/MakeMovie.py)
The final script for producing a video of some GOES-16 data as seen [here](https://www.youtube.com/watch?v=zNCElNnWMUA&feature=youtu.be).  The video shows 10 days of earth observations starting on 7/19/2019, in both the Blue 0.47 um, and SWIR 3.9 um bands.

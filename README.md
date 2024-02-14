# MAPs
MAPS is a CLI tool for analysing the sensor performance of a *vanilla 3T CMOS Mononlithic Active Pixel Sensor*. It contains functionality to map the following parameters for each individual pixel and compute the sensor average:
* Gain - The relationship between each pixel's photon count and its readout
* Offset - average pixel output at 0 illumination
* Full well capacity - maximum number of photons absorbed before the pixel becomes saturated
* Dynamic range - ratio between the brightest and darkest possible pixel readout

# Requirements
* python3 - version 3.10 or newer
* numpy - version 1.22 or newer
* matplotlib - verson 3.4 or newer
* Scipy - version 1.8.0 or newer

# Useage
Download the codebase naviate to the following file `MAPS/python/src/main2.py`. Update the value of SRC_LOC so that it points to the location of `MAPS/python/src` on your device. Navigate to `src` and using the following command to start MAPS:
```
python3 main2.py
```

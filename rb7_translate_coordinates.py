#!/usr/bin/python
from scipy import *
from pylab import *
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import numpy as np

def METERS_DEGLON(x):
    d2r = math.radians(x)
    return((111415.13 * cos(d2r))- (94.55 * cos(3.0*d2r)) + (0.12 * cos(5.0*d2r)))
def METERS_DEGLAT(x):
    d2r = math.radians(x)
    return(111132.09 - (566.05 * cos(2.0*d2r))+ (1.20 * cos(4.0*d2r)) - (0.002 * cos(6.0*d2r)))
def translate_coordinates(lat0,lon0,lat1,lon1):
    xx = (lon1 - lon0) * METERS_DEGLON(lat0)
    yy = (lat1 - lat0) * METERS_DEGLAT(lat0)
    results = [xx,yy]
    return(results)

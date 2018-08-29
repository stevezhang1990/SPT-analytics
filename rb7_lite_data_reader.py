#!/usr/bin/python
from scipy import *
from pylab import *
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
from matplotlib.colors import LogNorm
import csv
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from spt_toolkits import *
import math as ma

lat0 = 52.378481
lon0 = 4.785418
#several dimensions:
#base dimension: time (filtered) ,player (non-filtered)
#lite data: position,v,a,tackle,IMU,forward/backward,odometer
#define starting time

        
with open("/users/jk/07/xzhang/RB7/game0.csv", 'rb') as f:
    reader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)
    #for line in reader:
        #print line
    headers = reader.next()
data_raw = loadtxt('/users/jk/07/xzhang/RB7/game5.npy',dtype = float)
lite_size = 9
shape1,shape2 = shape(data_raw)
data = np.zeros((shape1,lite_size-1))
#-0-----1------2-----3------4---------5---------6------7-------8----
#time,lat:35,lon:34,vel:9,acc:37,heart rate:36,fwd:3,stride:8,imu:79
data[:,0] = data_raw[:,35]
data[:,1] = data_raw[:,34]
data[:,2] = data_raw[:,9]
data[:,3] = data_raw[:,37]
data[:,4] = data_raw[:,36]
data[:,5] = data_raw[:,3]
data[:,6] = data_raw[:,8]
data[:,7] = data_raw[:,79]
data_player = data_raw[:,0]#[data[:,80] > 0]
data_time = time_convert(data_raw[:,1])
dt = 0.5
t_res = int(1/dt)
size1 = int(np.max(data_player))
size2 = (int(np.max(data_time))+1)*t_res
data_lite_raw = np.zeros((size1,size2,lite_size))
for j in range(size1):
        data_lite_raw[j,:,0] = np.arange(0,int(np.max(data_time))+1,dt)
for i in range(lite_size-1):
    for j in range(size1):
        time_full = player_index_data(data_time,data_player,j+1)
        data_full = player_index_data(data[:,i],data_player,j+1)
        for k in range(size2-1):
            data_dt = data_t_1D(data_full,time_full,data_lite_raw[j,k,0],
                               data_lite_raw[j,k+1,0])
            data_lite_raw[j,k,i+1] = np.mean(data_dt)
            #if ma.isnan(data_lite_raw[j,k,i+1]) == True and len(data_dt)!=0:
                    #print data_dt
critical_time = rb7_critical_time(data_lite_raw[:,:,3],data_lite_raw[:,:,0])
for i in range(size2):
        if data_lite_raw[0,i,0] < critical_time[0]:
                data_lite_raw[:,i,:] = nan
        elif data_lite_raw[0,i,0] >critical_time[1] and \
        data_lite_raw[0,i,0] < critical_time[2]:
                data_lite_raw[:,i,:] = nan
        elif data_lite_raw[0,i,0] > critical_time[3]:
                data_lite_raw[:,i,:] = nan
#data_lite = np.ma.masked_where(data_lite_raw == nan,data_lite_raw)
                
np.save("/users/jk/15/xzhang/RB7/game5_lite.npy",data_lite_raw)
print "done"

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
lat0 = 52.378481
lon0 = 4.785418
#several dimensions:
#base dimension: time (filtered) ,player (non-filtered)
#lite data: position,v,a,tackle,IMU,forward/backward,odometer
#define starting time
#-0-----1------2-----3------4---------5---------6------7-------8----
#time,lat:35,lon:34,vel:9,acc:37,heart rate:36,fwd:3,stride:8,imu:79
data_lite_raw = np.load('/users/jk/15/xzhang/RB7/game3_lite.npy')
data_lite = np.ma.masked_invalid(data_lite_raw)
tackle_team = np.mean(data_lite[:,:,4],axis=0)
tackle = np.zeros_like(data_lite[:,:,0])
len1 = len(data_lite[:,0,0])
time_v_high = np.zeros(len1)
v_high_avg = np.zeros(len1)
half_time = 60*8
for i in range(len1):
    tackle[i,:] = find_tackle(data_lite[i,:,4],tackle_team,data_lite[i,:,3])
    time_v_high[i] = len(data_lite[i,:,0][data_lite[i,:,3]>3])
    v_high_avg[i] = np.mean(data_lite[i,:,3][data_lite[i,:,3]>2])
fig = plt.figure(1,figsize=(12,10))
num_plots=len1-1
time1 = 0
time2 = 1000
colormap = plt.cm.gist_ncar
plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9,num_plots)])
fig.suptitle('Time series charts')
ax = plt.subplot(311)
#$x = np.arange(10)
labels = []
for i in range(num_plots):
    plt.plot(data_lite[i,:,0], data_lite[i,:,3])
    labels.append(r'player%i' % (i+1))
plt.legend(labels)
plt.title(r'v')
#34xx,27xx,part1:299x,286x
xlim([time1, time2])
plt.xticks([])
ax = plt.subplot(312)
plt.title(r'a')
for i in range(num_plots):
    plt.plot(data_lite[i,:,0], data_lite[i,:,4],data_lite[i,:,0], tackle[i,:],'ro')
xlim([time1,time2])
#ylim([0,2])
plt.xticks([])
ax = plt.subplot(313)
plt.title(r'stride')
for i in range(num_plots):
    plt.plot(data_lite[i,:,0], data_lite[i,:,7])
xlim([time1,time2])
#plt.xticks([])
##ax = plt.subplot(614)
##plt.title(r'forward/backward')
##plt.plot(time, fwd)
##xlim([time1,time2])
##plt.xticks([])
##ax = plt.subplot(615)
##plt.title(r'stride')
##plt.plot(time, stride)
##xlim([time1,time2])
##plt.xticks([])
##ax = plt.subplot(616)
##plt.title(r'IMU')
##plt.plot(time, imu)
##xlim([time1,time2])
#ax.get_xaxis().set_ticks([])
plt.xlabel('time of game (min)')

show()

        #columns[h].append(v)



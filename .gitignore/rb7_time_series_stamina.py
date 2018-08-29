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
#read the raw data
#data_lite_raw = np.load('/users/jk/15/xzhang/RB7/game1_lite.npy')
#create arrays
time_v_high = np.zeros((6,12,3))
v_high_avg = np.zeros((6,12,3))
for j in range(6):
    if j == 0:
        data_lite_raw = np.load('/users/jk/15/xzhang/RB7/game1_lite.npy')
    elif j == 1:
        data_lite_raw = np.load('/users/jk/15/xzhang/RB7/game2_lite.npy')
    elif j == 2:
        data_lite_raw = np.load('/users/jk/15/xzhang/RB7/game3_lite.npy')
    elif j == 3:
        data_lite_raw = np.load('/users/jk/15/xzhang/RB7/game4_lite.npy')
    elif j == 4:
        data_lite_raw = np.load('/users/jk/15/xzhang/RB7/game5_lite.npy')
    elif j == 5:
        data_lite_raw = np.load('/users/jk/15/xzhang/RB7/game6_lite.npy')
    #mask all the invalid points
    data_lite = np.ma.masked_invalid(data_lite_raw)
    #data2_lite = np.ma.masked_invalid(data2_lite_raw)
    #???
    tackle_team = np.mean(data_lite[:,:,4],axis=0)
    tackle = np.zeros_like(data_lite[:,:,0])
    #retrieve the length of the data
    len1 = len(data_lite[:,0,0])

    #specify start, half and finishing time
    fin_time = np.max(data_lite[0,:,0])
    ini_time = np.min(data_lite[0,:,0])
    half_time = 0.5*(ini_time+fin_time)
    #two velocity threshold
    v_lvl_1 = 3
    v_lvl_2 = 0
    #compute average high speed, and time maintaining high speed
    for i in range(len1):
        peak_v = find_peak_v(data_lite[i,:,3])
        time_1 = data_t_1D(data_lite[i,:,0],data_lite[i,:,0],ini_time,half_time)
        time_2 = data_t_1D(data_lite[i,:,0],data_lite[i,:,0],half_time,fin_time)
        vel_1 = data_t_1D(data_lite[i,:,3],data_lite[i,:,0],ini_time,half_time)
        vel_1_peak = data_t_1D(peak_v,data_lite[i,:,0],ini_time,half_time)
        vel_2 = data_t_1D(data_lite[i,:,3],data_lite[i,:,0],half_time,fin_time)
        vel_2_peak = data_t_1D(peak_v,data_lite[i,:,0],half_time,fin_time)
        tackle[i,:] = find_tackle(data_lite[i,:,4],tackle_team,data_lite[i,:,3])
        if len(data_lite[i,:,0][data_lite[i,:,3]>v_lvl_2]) > 0:
            time_v_high[j,i,0] = len(data_lite[i,:,0][data_lite[i,:,3]>v_lvl_1])/ \
                               float(len(data_lite[i,:,0][data_lite[i,:,3]>v_lvl_2]))
        v_high_avg[j,i,0] = np.mean(peak_v[peak_v>v_lvl_2])
        if len(time_1[vel_1>v_lvl_2]) > 0:
            time_v_high[j,i,1] = len(time_1[vel_1>v_lvl_1])/float(len(time_1[vel_1>v_lvl_2]))
        if len(time_2[vel_2>v_lvl_2]) > 0:
            time_v_high[j,i,2] = len(time_2[vel_2>v_lvl_1])/float(len(time_2[vel_2>v_lvl_2]))
        v_high_avg[j,i,1] = np.mean(vel_1_peak[vel_1_peak>v_lvl_2])
        v_high_avg[j,i,2] = np.mean(vel_2_peak[vel_2_peak>v_lvl_2])
x = np.arange(1,7,1)
fig = plt.figure(1,figsize=(12,10))
num_plots=len1-1  
time1 = 0
time2 = 1000
colormap = plt.cm.gist_ncar
plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9,num_plots)])
fig.suptitle('high speed portion charts')
ax = plt.subplot(411)
#$x = np.arange(10)
labels = []
for i in range(num_plots):
    plt.plot(x, time_v_high[:,i,0])
    #labels.append(r'player%i' % (i+1))
plt.legend(labels)
plt.title(r'v')
#34xx,27xx,part1:299x,286x
#xlim([time1, time2])
plt.xticks([])
ax = plt.subplot(412)
plt.title(r'a')
for i in range(num_plots):
    plt.plot(x, time_v_high[:,i,1])
#xlim([time1,time2])
#ylim([0,2])
plt.xticks([])
ax = plt.subplot(413)
plt.title(r'stride')
for i in range(num_plots):
    plt.plot(x, time_v_high[:,i,2])
ax = plt.subplot(414)
plt.title(r'stride')
plt.plot(x, np.mean(np.ma.masked_invalid(time_v_high[:,:,0]),axis=1))
#xlim([time1,time2])
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



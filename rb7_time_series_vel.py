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
#from rb7_peak_finding import argrelextrema
with open("/users/jk/07/xzhang/RB7/game0.csv", 'rb') as f:
    reader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)
    #for line in reader:
        #print line
    headers = reader.next()
#print headers
#velocity DPR (GPS doppler based) 9, ACC DPR 37, Heart Rate 36
#forward/backward 3, stride 8, imu 79
#player 3 has the highest mileage of game 1
data = loadtxt('/users/jk/07/xzhang/RB7/game1.npy',dtype = float)
player_index = 2
data_player = data[:,0]
data_time = data[:,1]
time_raw = data_time
def running_average(data,n):
    ret = np.cumsum(data,dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:]/n

for i in range(len(data_time)):
    if data_time[i] < data_time[0] - 20*60:
        time_raw[i] = data_time[i]+3600
data_time = (time_raw - np.min(time_raw))/60.0
data_fwd = data[:,3]
data_stride = data[:,8]
data_vel = data[:,9]
data_acc = data[:,37]
data_hr = data[:,36]
data_imu = data[:,79]
player1 = data_player[data_player == player_index]
time = data_time[data_player == player_index]
rmi = 2
time = time[rmi:len(time)-rmi]
v_raw = data_vel[data_player == player_index]
v = running_average(v_raw,n=2*rmi+1)
a_raw = data_acc[data_player == player_index]
a = running_average(a_raw,n=2*rmi+1)
#data_dec = a[a<0]
#data_dev = v[a<0]
#data_det = time[a<0]
tackle_raw = np.zeros(len(a))
for i in range(5,len(a)-5):
    if a[i] < -1.5 and v[i] > 0:
        for j in range(5):
            for k in range(5):
                if a[i-j-1] > a[i] and a[i+k+1] > a[i]: 
                    tackle_raw[i] = a[i]

    #if a[i-2]>a[i-i] and a[i-1]>a[i] and a[i]<a[i+1] and a[i+1]<a[i+2] and a[i]<0:
    #if a[i-1]>=a[i] and a[i]<a[i+1] and a[i]<0:
            #print "find", i
            #tackle_raw[i] = a[i]
#data_tc = data_dec[argrelextrema(data_dec,np.less)[0]]
#data_tc_v = data_dev[argrelextrema(data_dec,np.less)[0]]
#data_tc_t = data_det[argrelextrema(data_dec,np.less)[0]]
#tackle = data_tc[data_tc_v > 0]
#tc_time = data_tc_t[data_tc_v > 0]
tc_time = time[tackle_raw<0]
tackle = tackle_raw[tackle_raw<0]
#we need function for signal searching and smoothing
hr_raw = data_hr[data_player == player_index]
hr = running_average(hr_raw,n=2*rmi+1)
fwd_raw = data_fwd[data_player == player_index]
fwd = running_average(fwd_raw,n=2*rmi+1)
stride_raw = data_stride[data_player == player_index]
stride = running_average(stride_raw,n=2*rmi+1)
imu_raw = data_imu[data_player == player_index]
imu = running_average(imu_raw,n=2*rmi+1)
time1 = np.min(time)#903/60.0
time2 = np.max(time)#1060/60.0
player1 = player1[time > time1]
time_1 = time[time > time1]
tc_time_1 = tc_time[tc_time > time1]
v = v[time > time1]
a = a[time > time1]
hr = hr[time > time1]
fwd = fwd[time > time1]
stride = stride[time > time1]
imu = imu[time > time1]
tackle = tackle[tc_time > time1]
time_unv = time_1[time_1 < time2]
tc_time_unv = tc_time_1[tc_time_1 < time2]
player1 = player1[time_1 < time2]
v = v[time_1 < time2]
a = a[time_1 < time2]
hr = hr[time_1 < time2]
fwd = fwd[time_1 < time2]
stride = stride[time_1 < time2]
imu = imu[time_1 < time2]
tackle = tackle[tc_time_1 < time2]


fig = plt.figure(1,figsize=(12,10))
fig.suptitle('Time series of player 2 game 1 full')
ax = plt.subplot(611)
plt.title(r'v')
plt.plot(time_unv, v)
#34xx,27xx,part1:299x,286x
xlim([time1,time2])
plt.xticks([])
ax = plt.subplot(612)
plt.title(r'a')
plt.plot(time_unv,a,tc_time_unv,tackle,'ro')
xlim([time1,time2])
#ylim([0,2])
plt.xticks([])
ax = plt.subplot(613)
plt.title(r'heart rate')
plt.plot(time_unv, hr)
xlim([time1,time2])
plt.xticks([])
ax = plt.subplot(614)
plt.title(r'forward/backward')
plt.plot(time_unv, fwd)
xlim([time1,time2])
plt.xticks([])
ax = plt.subplot(615)
plt.title(r'stride')
plt.plot(time_unv, stride)
xlim([time1,time2])
plt.xticks([])
ax = plt.subplot(616)
plt.title(r'IMU')
plt.plot(time_unv, imu)
xlim([time1,time2])
#ax.get_xaxis().set_ticks([])
plt.xlabel('time of game (min)')

show()

        #columns[h].append(v)



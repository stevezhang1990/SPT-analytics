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
from rb7_translate_coordinates import *
#from rb7_peak_finding import argrelextrema
lat0 = 52.378481
lon0 = 4.785418
with open("/users/jk/07/xzhang/RB7/game0.csv", 'rb') as f:
    reader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)
    #for line in reader:
        #print line
    headers = reader.next()
#print headers
#velocity DPR (GPS doppler based) 9, ACC DPR 37, Heart Rate 36
#forward/backward 3, stride 8, imu 79
data = loadtxt('/users/jk/07/xzhang/RB7/game1.npy',dtype = float)
player_index = 3
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
half_time = 0.5*np.max(data_time)
data_vel = data[:,9]
data_acc = data[:,37]
data_lat = data[:,35]
data_lon = data[:,34]

player1 = data_player[data_player == player_index]
time_full = data_time[data_player == player_index]
rmi = 2
time = time_full[rmi:len(time_full)-rmi]
v_raw = data_vel[data_player == player_index]
v = running_average(v_raw,n=2*rmi+1)
a_raw = data_acc[data_player == player_index]
a = running_average(a_raw,n=2*rmi+1)
data_lat = data_lat[data_player == player_index]
data_lon = data_lon[data_player == player_index]
lat = data_lat[data_lat > 0]
lon = data_lon[data_lon > 0]
x = np.zeros(len(lat))
y = np.zeros(len(lon))
for i in range(len(lat)):
    x[i],y[i] = translate_coordinates(lat0,lon0,lat[i],lon[i])
    if time_raw[i] > half_time:
        x[i] = 101 - x[i]
        y[i] = 71 - y[i]
tackle_raw = np.zeros(len(a))
for i in range(5,len(a)-5):
    if a[i] < -1.5 and v[i] > 0:
        for j in range(5):
            for k in range(5):
                if a[i-j-1] > a[i] and a[i+k+1] > a[i]: 
                    tackle_raw[i] = a[i]

latitude = np.linspace(0,71,71)
longitude = np.linspace(0,101,101)
count = np.zeros((len(longitude),len(latitude)))
for i in range((len(lat))):
    for j in range((len(longitude))-1):
        for k in range((len(latitude))-1):
            if x[i]>=longitude[j]:
                if x[i]<longitude[j+1]:
                   if y[i]>=latitude[k]:
                       if y[i]<latitude[k+1]:
                           if v_raw[i] > 0.5:
                                count[j,k] = count[j,k]+1
x_raw = x[rmi:len(time_full)-rmi]
y_raw = y[rmi:len(time_full)-rmi]
tc_time = time[tackle_raw<0]
tackle = tackle_raw[tackle_raw<0]
x_tackle = x_raw[tackle_raw<0]
y_tackle = y_raw[tackle_raw<0]
time1 = np.min(time)#903/60.0
time2 = np.max(time)#1060/60.0
player1 = player1[time > time1]
time_1 = time[time > time1]
tc_time_1 = tc_time[tc_time > time1]
v = v[time > time1]
a = a[time > time1]
tackle = tackle[tc_time > time1]
x_tackle = x_tackle[tc_time > time1]
y_tackle = y_tackle[tc_time > time1]
time_unv = time_1[time_1 < time2]
tc_time_unv = tc_time_1[tc_time_1 < time2]
player1 = player1[time_1 < time2]
v = v[time_1 < time2]
a = a[time_1 < time2]
tackle = tackle[tc_time_1 < time2]
x_tackle = x_tackle[tc_time_1 < time2]
y_tackle = y_tackle[tc_time_1 < time2]

plot_data = count

delta = 1
clevs = np.arange(0,60,delta)
CS = contourf(latitude,longitude,plot_data,clevs,extend='both',cmap=get_cmap("gnuplot2_r"))
plt.colorbar()
plt.scatter(y_tackle,x_tackle)#,marker='+')
plt.title('Heat map player 3 game 1 with tackle')
#player = [float(numeric_string) for numeric_string in data_raw[:,0]]

show()

        #columns[h].append(v)



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

        
with open("/users/jk/07/xzhang/RB7/game0.csv", 'rb') as f:
    reader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)
    #for line in reader:
        #print line
    headers = reader.next()
data_raw = loadtxt('/users/jk/07/xzhang/RB7/game1.npy',dtype = float)
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
                
np.save("/users/jk/15/xzhang/RB7/game1_lite.npy",data_lite_raw)
print "done"
block
half_time = 0.5*np.max(data_time)
#halftime would be determined by a function that tells when many players velocity
# is zero for at least one minute.
# we need a function for heatmap excluding position at rest
#data_time2 = data[:,80][data[:,80] > 0]
# need to think about introducing grid with full starters and mixed rotations
player_index = 3
player1 = data_player[data_player == player_index]
time = data_time[data_player == player_index]
#time2 = data_time2[data_player == player_index]
# project 1, the rugby pitch is skewed. We need to switch the lat lon grid
# to the pitch grid through 2d line functions.
#34 natural lon, 35 natural lat, 81 gps lat, 82 gps lon

#data_lon = data[:,82]
data_lat = data_lat[data_player == player_index]
data_lon = data_lon[data_player == player_index]
v = data_vel[data_player == player_index]
lat = data_lat[data_lat > 0]
lon = data_lon[data_lon > 0]
x = np.zeros(len(lat))
y = np.zeros(len(lon))
for i in range(len(lat)):
    x[i],y[i] = translate_coordinates(lat0,lon0,lat[i],lon[i])
    if time[i] > half_time:
        x[i] = 101 - x[i]
        y[i] = 71 - y[i]
    
#lat = lat[lon > 0]
#lon = lon[lat > 0]
lat_max = 52.37913
lat_min = 52.378482
lon_max = 4.786883
lon_min = 4.785392
latitude = np.linspace(0,71,71)
longitude = np.linspace(0,101,101)
count = np.zeros((len(longitude),len(latitude)))
for i in range((len(lat))):
    for j in range((len(longitude))-1):
        for k in range((len(latitude))-1):
            if x[i]>=longitude[j] and \
               x[i]<longitude[j+1] and \
               y[i]>=latitude[k] and \
               y[i]<latitude[k+1] and \
               v[i] > 0.3:
                count[j,k] = count[j,k]+1
#savetxt("/users/jk/07/xzhang/RB7/count1_2.npy",count)
#savetxt("/users/jk/07/xzhang/RB7/latitude1_2.npy",latitude)
#savetxt("/users/jk/07/xzhang/RB7/longitude1_2.npy",longitude)
plot_data = count
#bond_lat = np.array([lat_max,52.37913,lat_min,52.378503])
#bond_lon = np.array([lon_min,4.786863,4.785413,lon_max])

#print "done"
delta = 1
clevs = np.arange(0,20,delta)
CS = contour(latitude,longitude,plot_data,clevs,extend='both',cmap=get_cmap('hot_r'))
plt.colorbar()
#plt.scatter(bond_lat,bond_lon)
plt.title('Heat map player 10 game 1')
#player = [float(numeric_string) for numeric_string in data_raw[:,0]]
show()

#column = {}
#for h in headers:
    #column[h] = []
#print column
    #for row in reader:
        #for h, v in zip(headers,row):
            #column[h].append(v)
#for row in reader:
    #for (h,v) in row.items():
        #columns[h].append(v)



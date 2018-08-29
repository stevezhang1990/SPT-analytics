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

lat0 = 52.378481
lon0 = 4.785418

with open("/users/jk/07/xzhang/RB7/game0.csv", 'rb') as f:
    reader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)
    #for line in reader:
        #print line
    headers = reader.next()
data = loadtxt('/users/jk/07/xzhang/RB7/game1.npy',dtype = float)

data_player = data[:,0]#[data[:,80] > 0]
data_time = data[:,1]
data_vel = data[:,9]
time_raw = data_time

for i in range(len(data_time)):
    if data_time[i] < data_time[0] - 20*60:
        time_raw[i] = data_time[i]+3600
data_time = time_raw - np.min(time_raw)
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
data_lat = data[:,35]
#data_lat = data[:,81]
data_lon = data[:,34]
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
            if x[i]>=longitude[j] \               
                and x[i]<longitude[j+1] \
                and y[i]>=latitude[k] \
                and y[i]<latitude[k+1]\
                and v[i] > 0.3:
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
plt.title('Heat map player 1 game 1')
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



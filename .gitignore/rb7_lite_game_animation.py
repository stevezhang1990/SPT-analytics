#!/usr/bin/python
from scipy import *
from pylab import *
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
from matplotlib.colors import LogNorm
import csv
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
#-0-----1------2-----3------4---------5---------6------7-------8----
#time,lat:35,lon:34,vel:9,acc:37,heart rate:36,fwd:3,stride:8,imu:79
data_lite_raw = np.load('/users/jk/15/xzhang/RB7/game2_lite.npy')
data_lite = np.ma.masked_invalid(data_lite_raw)

#critical_time = rb7_critical_time(data_lite_raw[:,:,3],data_lite_raw[:,:,0])
half_time = (np.max(data_lite[0,:,0])-np.min(data_lite[0,:,0]))/2.0
x_full = 101
y_full = 71
lat0 = 52.378481
lon0 = 4.785418
len1 = len(data_lite[:,0,0])
len4 = len(data_lite[0,:,0])
len2 = 30
len3 = 20
x_edge = np.linspace(0,x_full,len2)
y_edge = np.linspace(0,y_full,len3)
heat_map = np.zeros((len1,len2,len3))
#for i in range(len1):
    #heat_map[i,:,:] = rb7_heat_map(data_lite_raw[i,:,1],data_lite_raw[i,:,2],
                                   #x_edge,y_edge,
                                   #data_lite_raw[i,:,0],data_lite_raw[i,:,3],
                                   #lat0,lon0,critical_time[1])
x = np.zeros((len1,len4))
y = np.zeros((len1,len4))
player_index = np.arange(len1)
for j in range(len4):
    for i in range(len1):
        x[i,j],y[i,j] =  translate_coordinates(lat0,lon0,data_lite[i,j,1],
                                       data_lite[i,j,2])
        if ma.isnan(x[i,j]) == True:
            x[i,j] = -999
            y[i,j] = -999
def update_plot(dframe,fig,scat):
    data = np.hstack((x[:,50+dframe,np.newaxis],y[:,50+dframe,np.newaxis]))
    scat.set_offsets(data)
    ax.set_title('Game 2 Time: %d' %(0.5*dframe))
    #print ('Time: %d' %(0.5*dframe))
    return scat,
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([-10,110])
ax.set_ylim([-10,80])
# Set up formatting for the movie files
#Writer = animation.writers['ffmpeg']
#writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

scat = plt.scatter(x[:,50],y[:,50],c=player_index)
anim = animation.FuncAnimation(fig,update_plot,frames =1000,fargs=(fig,scat),
                               interval=10)
#plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'
#plot_data = heat_map[0,:,:]
#np.sum(heat_map[1:4,:,:],axis=0)
#anim.save('game2_anim.mp4', writer="ffmpeg")# writer=writer)
#print "done"
#delta = 1
#clevs = np.arange(0,10,delta)
#CS = contourf(y_edge,x_edge,plot_data,clevs,extend='both',cmap=get_cmap('hot_r'))
#plt.colorbar()
#plt.scatter(bond_lat,bond_lon)
#plt.title('Heat map player 10 game 1')
#player = [float(numeric_string) for numeric_string in data_raw[:,0]]
#plt.scatter(x,y,c=player_index)
show()


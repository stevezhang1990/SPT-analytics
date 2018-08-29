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
    if lat1>=-90 and lon1>=-180 and lat0>=-90 and lon0>=-180:
        xx = (lon1 - lon0) * METERS_DEGLON(lat0)    
        yy = (lat1 - lat0) * METERS_DEGLAT(lat0)    
        results = [xx,yy]
    else:
        results = [nan,nan]
    return(results)
#player index data shows the data corresponds to one player
def player_index_data(data_1D,data_player_1D,player_index):
    results = data_1D[data_player_1D == player_index]
    return results
#specify data with the designated time
def data_t_1D(data_1D,time_data,start_time,end_time):
    time_1 = time_data[time_data >= start_time]
    data_1 = data_1D[time_data >= start_time]
    result1 = data_1[time_1 <= end_time]
    return result1
#time_convert: convert natural time to real time
def time_convert(data_time):
    len_time = len(data_time)
    time_raw = np.zeros(len_time)
    for i in range(len_time):
        if data_time[i] < data_time[0] - 25*60:
            time_raw[i] = data_time[i]+3600
        else:
            time_raw[i] = data_time[i]
    result2 = time_raw - np.min(time_raw)
    return result2
def rb7_critical_time(v,time):
    len01,len02 = shape(v)
    v_start = 3
    v_crt = 0
    v_tol = 25
    dt = 0.5
    index_tol = int(v_tol/dt)
    time_ext = np.zeros((len01,3))
    for i in range(len01):
        #v_val = v[i,:][v[i,:] > v_start]
        time_raw = time[i,:][v[i,:] >= v_crt]
        time_act = time[i,:][v[i,:] > v_start]
        if len(time_raw) != 0 and len(time_act) != 0:
            time_ext[i,0] = np.min(time_act)
            time_ext[i,1] = np.max(time_act)
            time_ext[i,2] = np.max(time_raw)
        else:
            time_ext[i,:] = 300
    time_max = np.max(time_ext[:,2])
    time_start = np.mean(np.sort(time_ext[:,0])[0:4])
    time_stop = np.mean(-np.sort(-time_ext[:,1])[0:4])
    #print time_stop
    #print time_start
    ht_min = 0.3*time_max
    ht_max = 0.7*time_max
    ht_start_raw = np.zeros(len01)
    ht_stop_raw = np.zeros(len01)
    for i in range(len01):
        v_val = v[i,:][v[i,:] >= v_crt]
        time_raw = time[i,:][v[i,:] >= v_crt]
        ht_poll = data_t_1D(time_raw,time_raw,ht_min,ht_max)
        #print ht_poll
        v_poll = data_t_1D(v_val,time_raw,ht_min,ht_max)
        #print v_poll
        len3 = len(ht_poll)
        j = index_tol
        while j >=index_tol and j < len3-index_tol:
            if np.sum(v_poll[j:j+index_tol]) == 0:
                ht_start_raw[i] = ht_poll[j]
                j=len3
            else:
                j = j+1
        j = index_tol
        while j >=index_tol and j < len3-index_tol:
            if np.sum(v_poll[-j-index_tol:-j]) == 0:
                ht_stop_raw[i] = ht_poll[-j]
                j=len3
            else:
                j = j+1
    ht_start = np.mean(np.sort(ht_start_raw[ht_start_raw>0])[0:3])
    ht_stop = np.mean(-np.sort(-ht_stop_raw[ht_stop_raw>0])[0:3])
    return np.array([time_start,ht_start,ht_stop,time_stop])
def rb7_heat_map(lat,lon,x_edge,y_edge,time,v,lat0=None,lon0=None,half_time=None,ht_reverse=True,lat_lon_coor=True):
    if lat_lon_coor == True:
        if lat0 == None or lon0 == None:
            print "error when processing heat map, need lat0,lon0"
        else:
            x = np.zeros_like(lat)
            y = np.zeros_like(lon)
            for i in range(len(lat)):
                x[i],y[i] = translate_coordinates(lat0,lon0,lat[i],lon[i])
    else:
        x=lat
        y=lon
    x_full = 101
    y_full = 71
    if ht_reverse == True:
        if half_time == None:
            print "error when processing heat map, need half time"
        else:
            if time[i] > half_time and x[i]>0 and y[i] >0:
                    x[i] = x_full - x[i]
                    y[i] = y_full - y[i]
    v_crt = 0.7
    count = np.zeros((len(x_edge),len(y_edge)))
    for i in range((len(x))):
        for j in range((len(x_edge))-1):
            for k in range((len(y_edge))-1):
                if x[i]>=x_edge[j] \
                    and x[i]<x_edge[j+1] \
                    and y[i]>=y_edge[k] \
                    and y[i]<y_edge[k+1]\
                    and v[i] > v_crt:
                    count[j,k] = count[j,k]+1    
    return count
def find_tackle(a,a_team,v):
    tackle_raw = np.zeros(len(a))
    tol=5#erlance = 5
    for i in range(tol,len(a)-tol):
        if a[i] < -1.5 and v[i] > 0 and a_team[i]<0:
            for j in range(tol):
                if a[i-j-1] > a[i] and a[i+j+1] > a[i]: 
                    tackle_raw[i] = a[i]
    tackle = np.ma.masked_where(tackle_raw==0,tackle_raw)
    return tackle
def find_peak_v(v):
    tol = 5
    peak_v = np.zeros_like(v)
    for i in range(tol,len(v)-tol):
        if v[i] > 3:
            for j in range(tol):
                if v[i-j-1] < v[i] and v[i+j+1] < v[i]:
                    peak_v[i] = v[i]
    results_peak = np.ma.masked_where(peak_v==0,peak_v)
    return results_peak

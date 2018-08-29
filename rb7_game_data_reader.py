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


#f = open('/users/jk/07/xzhang/RB7/game0.csv','rb')
#data_raw = pd.read_csv('/users/jk/07/xzhang/RB7/game3.csv',sep='\s+')
#csv = np.genfromtxt('/users/jk/07/xzhang/RB7/game3.csv',delimiter=",")
line2 = 941295
line3 = 589185
line5 = 885411
column = 90
data_raw = np.empty((line2,column),dtype='|S225')

i = 0
with open("/users/jk/07/xzhang/RB7/game2.csv", 'rU') as f:
    reader = csv.reader(f, delimiter = ',', quoting=csv.QUOTE_NONE)
    for line in reader:
        if len(line) >= column:
            for j in range(column):
                data_raw[i,j] = line[j]
            i = i+1
        else:
            line2 = line2 -1
data_raw = data_raw[0:line2,:]
    #headers = reader.next()
#data_raw= np.loadtxt(r'/users/jk/07/xzhang/RB7/game6.csv',dtype=str,delimiter=',')#,skiprows=0)
data_raw[data_raw==' ..'] = 'Nan'
data_raw[data_raw=='  '] = 'Nan'
data_raw[data_raw==' '] = 'Nan'
len_orbit,len2 = shape(data_raw)
data = np.zeros((len_orbit,len2))
for i in range(len_orbit):
    for j in range(len2):
        #print j
        if j != 1 and j !=80 and j < 83:
            #if j < 5 or j >80:
            data[i,j] = float(data_raw[i,j])
        elif j == 1:
            if data_raw[i,j] == 'Nan':
                data[i,j] = float(data_raw[i,j])
            else:
                time_string = np.array2string(data_raw[i,j])
                time_string = time_string.replace("'","")
                time_data = time_string.split(':')
                minute = float(time_data[0])
                sec = float(time_data[1])
                data[i,j] = 60*minute + sec
        elif j == 80:
            if data_raw[i,j] == 'Nan':
                data[i,j] = float(data_raw[i,j])
            else:
                time_string = np.array2string(data_raw[i,j])
                time_string = time_string.replace("'","")
                time_data = time_string.split(':')
                hour = float(time_data[0])
                minute = float(time_data[1])
                sec = float(time_data[2])
                data[i,j] = 3600*hour + 60*minute + sec
        elif j == 83:
            if data_raw[i,j] == 'Nan':
                data[i,j] = float(data_raw[i,j])
            else:
                gps_string = np.array2string(data_raw[i,j])
                gps_string = gps_string.replace("'","")
                gps_string = gps_string.replace("  "," *")
                gps_group = gps_string.split(' *')
                #gps_group = gps_string.replace("*","")
                for k in range(len(gps_group)-1):
                    gps_temp = gps_group[k+1]
                    gps_temp = gps_temp.replace("[a",",")
                    gps_temp = gps_temp.replace("]","")
                    gps_temp = gps_temp.replace(" e",",")
                    gps_temp = gps_temp.replace(" s",",")
                    gps_temp = gps_temp.split(',')
                    channel = float(gps_temp[0])
                    a = float(gps_temp[1])
                    e = float(gps_temp[2])
                    s = float(gps_temp[3])
        elif j == 84:
            if data_raw[i,j] == 'Nan':
                data[i,j] = float(data_raw[i,j])
            else:
                flag_string = np.array2string(data_raw[i,j])
                flag_string = flag_string.replace("'","")
                flag_string = flag_string.strip()
                flag_string = flag_string.replace("fl:","")
                flag_string = flag_string.replace("e","")
                flag_string = flag_string.replace(" conv","")
                flag_string = flag_string.replace(" vl","")
                flag_string = flag_string.replace(" pos","")
                flag_group = flag_string.split(':')
                fl = float(flag_group[0])
                conv = float(flag_group[1])
                vel = float(flag_group[2])
                pos = float(flag_group[3])
savetxt("/users/jk/07/xzhang/RB7/game2.npy",data)
print "done"




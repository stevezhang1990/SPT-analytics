from scipy import *
from pylab import *
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#dimensions of data
line2 = 5250
column = 27
column2 = 28
#read data
data_raw = np.empty((line2,column2),dtype='|S225')
i = 0
#open raw data
with open('/home/xzhang/SPT_analytics/data/speed_data.csv', 'rU') as f:
    reader = csv.reader(f,delimiter=',',quoting=csv.QUOTE_NONE)
    for line in reader:
        #print line
        #print len(line)
        if len(line) >=column:
            for j in range(column):
                data_raw[i,j] = line[j]
            data_raw[i,column] = i
            i = i+1
        else:
            line2 = line2 - 1
data_raw = data_raw[0:line2-1,:]
data_raw[data_raw==''] = 'Nan'
# categorize data
k1=np.zeros((4,8))
k2=np.zeros((4,8))
k=np.zeros((4,8))
len_orbit,len2 = shape(data_raw)
line3 = len_orbit
#SMM2F is the senior men M2+/M2x final data, SMM2S is the semi-final and heat data
#SMM2 is all the SMM2 data
#-index------0-----1------2-----3
#Order 4 is men, women, LMen, LWomen, L for lightweight
#-index-----0--1--2--3--4--5--6--7
#Order 8 is 1x,2+,2-,2x,4+,4-,4x,8+ 
rowing_final = np.zeros((4,8,len_orbit,len2-7))
rowing_semi = np.zeros((4,8,len_orbit,len2-7))
data_rowing = np.zeros((4,8,len_orbit,len2-7))
rowing_avg = np.zeros((4,8,len_orbit))
for i in range(1,len_orbit):
    #if data_raw[i,1] == 'Senior':
    if data_raw[i,3] == 'M1x':
        j1 = 0
        j2 = 0
    elif data_raw[i,3] == 'W1x':
        j1 = 1
        j2 = 0
    elif data_raw[i,3] == 'LM1x':
        j1 = 2
        j2 = 0
    elif data_raw[i,3] == 'LW1x':
        j1 = 3
        j2 = 0
    elif data_raw[i,3] == 'M2+':
        j1 = 0
        j2 = 1
    elif data_raw[i,3] == 'W2+':
        j1 = 1
        j2 = 1
    elif data_raw[i,3] == 'LM2+':
        j1 = 2
        j2 = 1
    elif data_raw[i,3] == 'LW2+':
        j1 = 3
        j2 = 1
    elif data_raw[i,3] == 'M2-':
        j1 = 0
        j2 = 2
    elif data_raw[i,3] == 'W2-':
        j1 = 1
        j2 = 2
    elif data_raw[i,3] == 'LM2-':
        j1 = 2
        j2 = 2
    elif data_raw[i,3] == 'LW2-':
        j1 = 3
        j2 = 2
    elif data_raw[i,3] == 'M2x':
        j1 = 0
        j2 = 3
    elif data_raw[i,3] == 'W2x':
        j1 = 1
        j2 = 3
    elif data_raw[i,3] == 'LM2x':
        j1 = 2
        j2 = 3
    elif data_raw[i,3] == 'LW2x':
        j1 = 3
        j2 = 3
    elif data_raw[i,3] == 'M4+':
        j1 = 0
        j2 = 4
    elif data_raw[i,3] == 'W4+':
        j1 = 1
        j2 = 4
    elif data_raw[i,3] == 'LM4+':
        j1 = 2
        j2 = 4
    elif data_raw[i,3] == 'LW4+':
        j1 = 3
        j2 = 4
    elif data_raw[i,3] == 'M4-':
        j1 = 0
        j2 = 5
    elif data_raw[i,3] == 'W4-':
        j1 = 1
        j2 = 5
    elif data_raw[i,3] == 'LM4-':
        j1 = 2
        j2 = 5
    elif data_raw[i,3] == 'LW4-':
        j1 = 3
        j2 = 5
    elif data_raw[i,3] == 'M4x':
        j1 = 0
        j2 = 6
    elif data_raw[i,3] == 'W4x':
        j1 = 1
        j2 = 6
    elif data_raw[i,3] == 'LM4x':
        j1 = 2
        j2 = 6
    elif data_raw[i,3] == 'LW4x':
        j1 = 3
        j2 = 6
    elif data_raw[i,3] == 'M8+':
        j1 = 0
        j2 = 7
    elif data_raw[i,3] == 'W8+':
        j1 = 1
        j2 = 7
    elif data_raw[i,3] == 'LM8+':
        j1 = 2
        j2 = 7
    elif data_raw[i,3] == 'LW8+':
        j1 = 3
        j2 = 7
    if data_raw[i,4] == 'Final a' or data_raw[i,4] == 'final a':
        for ii in range(len2-7):
            rowing_final[j1,j2,int(k1[j1,j2]),ii] = float(data_raw[i,7+ii])
        k1[j1,j2] = k1[j1,j2] +1
    else:
        for ii in range(len2-7):
            rowing_semi[j1,j2,int(k2[j1,j2]),ii] = float(data_raw[i,7+ii])
        k2[j1,j2] = k2[j1,j2] + 1
    #print j1, j2
    for ii in range(len2-7):
        data_rowing[j1,j2,int(k[j1,j2]),ii] = float(data_raw[i,7+ii])
        #SMM2[k,len2-7] = data_raw[i,len2-1]
    k[j1,j2] = k[j1,j2] +1

rowing_run = np.zeros((4,8))
rowing_count = np.ones((4,8))
rowing_avg_delta = np.zeros_like(rowing_avg)
rowing_delta = np.zeros_like(data_rowing)
rowing_delta[:,:,:,len2-8] = data_rowing[:,:,:,len2-8]
data_rowing_avg_run = np.zeros(len2-7)
data_rowing_run = np.zeros((4,8,len2-7))
jj = np.zeros((4,8))
for j2 in range(8):
    for j1 in range(4):
        rowing_avg[j1,j2,0:int(k[j1,j2])] = np.mean(data_rowing[j1,j2,0:int(k[j1,j2]),:-1],axis=1)
        rowing_run[j1,j2] = rowing_avg[j1,j2,0]
        data_rowing_run[j1,j2,:-1] = data_rowing[j1,j2,0,:-1]
#calculate delta time for data_rowing
        for i in range(int(k[j1,j2])-1):
            if data_raw[int(data_rowing[j1,j2,i+1,len2-8]),4] == data_raw[int(data_rowing[j1,j2,i,len2-8]),4]:
        #print data_raw[int(SMM2[i+1,len2-8]),4]
        #print data_raw[int(SMM2[i,len2-8]),4]
        #print SMM2[i+1,len2-8]
                rowing_run[j1,j2] = rowing_run[j1,j2] + rowing_avg[j1,j2,i]
                data_rowing_run[j1,j2,:-1] = data_rowing_run[j1,j2,:-1] + data_rowing[j1,j2,i,:-1]
                rowing_count[j1,j2] = rowing_count[j1,j2] + 1
            else:
                rowing_avg_run = rowing_run[j1,j2]/rowing_count[j1,j2]
                data_rowing_avg_run[:-1] = data_rowing_run[j1,j2,:-1]/rowing_count[j1,j2]
                rowing_avg_delta[j1,j2,int(jj[j1,j2]):int(jj[j1,j2])+rowing_count[j1,j2]] = rowing_avg[j1,j2,int(jj[j1,j2]):int(jj[j1,j2])+rowing_count[j1,j2]]-rowing_avg_run
                rowing_delta[j1,j2,int(jj[j1,j2]):int(jj[j1,j2])+rowing_count[j1,j2],:-1] = data_rowing[j1,j2,int(jj[j1,j2]):int(jj[j1,j2])+rowing_count[j1,j2],:-1] -data_rowing_avg_run[:-1]
                jj[j1,j2] = jj[j1,j2]+ rowing_count[j1,j2]
                rowing_run[j1,j2] = rowing_avg[j1,j2,i+1]
                data_rowing_run[j1,j2,:-1] = data_rowing[j1,j2,i+1,:-1]
                rowing_count[j1,j2] = 1
            if i == int(k[j1,j2])-2:
                rowing_avg_run = rowing_run[j1,j2]/rowing_count[j1,j2]
                data_rowing_avg_run[:-1] = data_rowing_run[j1,j2,:-1]/rowing_count[j1,j2]
                rowing_avg_delta[j1,j2,int(jj[j1,j2]):int(jj[j1,j2])+rowing_count[j1,j2]] = rowing_avg[j1,j2,int(jj[j1,j2]):int(jj[j1,j2])+rowing_count[j1,j2]]-rowing_avg_run
                rowing_delta[j1,j2,int(jj[j1,j2]):int(jj[j1,j2])+rowing_count[j1,j2],:-1] = data_rowing[j1,j2,int(jj[j1,j2]):int(jj[j1,j2])+rowing_count[j1,j2],:-1] -data_rowing_avg_run[:-1]
kk = np.zeros((4,8))
kk2 = np.zeros_like(kk)
rowing_high = np.zeros_like(data_rowing)
rowing_low = np.zeros_like(data_rowing)
rowing_std = np.zeros((4,8,len_orbit))
rowing_std_time = np.zeros((4,8,len2-8))
delta_avg_crt = 0.00015
rowing_high_stack = np.zeros((len_orbit,len2-7))
rowing_low_stack = np.zeros((len_orbit,len2-7))
for j2 in range(8):
    for j1 in range(4):
        for i in range(int(k[j1,j2])):
            if rowing_avg_delta[j1,j2,i] > delta_avg_crt:
                rowing_high[j1,j2,kk[j1,j2],:] = rowing_delta[j1,j2,i,:]
                rowing_high_stack[int(np.sum(kk)),:] = rowing_delta[j1,j2,i,:]
                kk[j1,j2] = kk[j1,j2] + 1
            elif rowing_avg_delta[j1,j2,i] < -delta_avg_crt:
                rowing_low[j1,j2,kk2[j1,j2],:] = rowing_delta[j1,j2,i,:]
                rowing_low_stack[int(np.sum(kk2)),:] = rowing_delta[j1,j2,i,:]
                kk2[j1,j2] = kk2[j1,j2] + 1
        rowing_std[j1,j2,0:k[j1,j2]] = np.std(data_rowing[j1,j2,0:k[j1,j2],:-1],axis=1)
        rowing_std_time[j1,j2,:] = np.std(data_rowing[j1,j2,0:k[j1,j2],:-1],axis=0)

    #print data_raw[int(SMM2_high[i,len2-8]),0]
x = np.linspace(100,2000,len2-8)
ax=plt.subplot(2,1,1)
#diff_crt = np.mean((SMM2[:,0:5]-SMM2[:,len2-13:len2-8]),axis=1)
#for i in range(20):
#for i in range(int(np.sum(kk))):
    #if np.mean(SMM2_high[i,0:5])-np.mean(SMM2_high[i,len2-13:len2-8])>0:
plt.plot(x,np.mean(rowing_high_stack[0:int(np.sum(kk)),:-1],axis=0))
ylim(-0.1,0.1)
ax=plt.subplot(2,1,2)
#for i in range(20):
#for i in range(int(np.sum(kk2))):
    #if np.mean(SMM2_low[i,0:5])-np.mean(SMM2_low[i,len2-13:len2-8])>0:
plt.plot(x,np.mean(rowing_low_stack[0:int(np.sum(kk2)),:-1],axis=0))
ylim(-0.1,0.1)
#ax=plt.subplot(5,1,3)
#for i in range(k):
   # plt.plot(x,SMM2[i,:-1])
#ylim(0.8,1.15)
#ax=plt.subplot(5,1,4)
#plt.hist(diff_crt,bins=10)
#ax=plt.subplot(5,1,5)
#plt.plot(x,SMM2_std_time)
show()


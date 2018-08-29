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

for j in range(8):
    for i in range(4):
        print j, i
        print np.mean(rowing_semi[i,j,0:int(k2[i,j]),:-1])

block
SMM2F = SMM2F[0:k1,1:len2-6]
#get the average speed and standard deviation of SMM2F, SMM2S and SMM2
SMM2F_avg = np.mean(SMM2F[:,:-1],axis=1)
SMM2F_std = np.std(SMM2F[:,:-1],axis=1)
SMM2F_high = np.zeros_like(SMM2F)
SMM2S = SMM2S[0:k2,1:len2-6]
SMM2S_avg = np.mean(SMM2S[:,:-1],axis=1)
SMM2S_high = np.zeros_like(SMM2S)
SMM2S_std = np.std(SMM2S[:,:-1],axis=1)
SMM2 = SMM2[0:k,1:len2-6]
SMM2_avg = np.mean(SMM2[:,:-1],axis=1)
SMM2_high = np.zeros_like(SMM2)
SMM2_low = np.zeros_like(SMM2)
SMM2_std = np.std(SMM2[:,:-1],axis=1)
SMM2_std_time = np.std(SMM2[:,:-1],axis=0)
kk=0
kk2=0
SMM2_tot_run = SMM2_avg[0]
SMM2_tot_count = 1
jj=0
SMM2_avg_delta = np.zeros_like(SMM2_avg)
#calculate delta time for SMM2
for i in range(k-1):    
    if data_raw[int(SMM2[i+1,len2-8]),4] == data_raw[int(SMM2[i,len2-8]),4]:
        #print data_raw[int(SMM2[i+1,len2-8]),4]
        #print data_raw[int(SMM2[i,len2-8]),4]
        #print SMM2[i+1,len2-8]
        SMM2_tot_run = SMM2_tot_run + SMM2_avg[i]
        SMM2_tot_count = SMM2_tot_count + 1
    else:
        SMM2_avg_run = SMM2_tot_run/SMM2_tot_count
        SMM2_avg_delta[jj:jj+SMM2_tot_count] = SMM2_avg[jj:jj+SMM2_tot_count]-SMM2_avg_run
        jj = jj+SMM2_tot_count
        SMM2_tot_run = SMM2_avg[i+1]
        SMM2_tot_count = 1
    if i == k-2:
        SMM2_avg_run = SMM2_tot_run/SMM2_tot_count
        SMM2_avg_delta[jj:jj+SMM2_tot_count] = SMM2_avg[jj:jj+SMM2_tot_count]-SMM2_avg_run
#determine high speed group and low speed group
for i in range(k):
    if SMM2_avg_delta[i]>0.00015:
        SMM2_high[kk,:] = SMM2[i,:]
        kk = kk + 1
    elif SMM2_avg_delta[i] < -0.00015:
        SMM2_low[kk2,:] = SMM2[i,:]
        kk2 = kk2+1

SMM2_high = SMM2_high[0:kk,:]
SMM2_low = SMM2_low[0:kk2,:]
#determine the criterial on large high speed and small low speed
SMM2_high_crt = np.mean(SMM2_high[:,len2-13:len2-8])
SMM2_low_crt = np.mean(SMM2_low[:,len2-13:len2-8])
#for i in range(len(SMM2_high[:,len2-8])):
    #print data_raw[int(SMM2_high[i,len2-8]),0]

x = np.linspace(100,2000,len2-8)
ax=plt.subplot(5,1,1)
diff_crt = np.mean((SMM2[:,0:5]-SMM2[:,len2-13:len2-8]),axis=1)

for i in range(kk):
    if np.mean(SMM2_high[i,0:5])-np.mean(SMM2_high[i,len2-13:len2-8])>0:
        plt.plot(x,SMM2_high[i,:-1])
ylim(0.8,1.15)
ax=plt.subplot(5,1,2)
for i in range(kk2):
    if np.mean(SMM2_low[i,0:5])-np.mean(SMM2_low[i,len2-13:len2-8])>0:
        plt.plot(x,SMM2_low[i,:-1])
ylim(0.8,1.15)
ax=plt.subplot(5,1,3)
for i in range(k):
    plt.plot(x,SMM2[i,:-1])
ylim(0.8,1.15)
ax=plt.subplot(5,1,4)
plt.hist(diff_crt,bins=10)
ax=plt.subplot(5,1,5)
plt.plot(x,SMM2_std_time)
show()


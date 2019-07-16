from scipy import *
from pylab import *
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
path1 = '/users/jk/11/xzhang/DAT112/torneo_data/'
data_raw = pd.read_csv(path1+'11_odds_history.csv',sep=',',header='infer')
#row (len1=num of match), column (len2=info) for the table
len1,len2 = shape(data_raw)
#len3: H/D/A
len3 = 3
#len4: odd bins (total 20: 0.1 step from 1-2, 0.2 step from 2-3, 1 step from 3-7)
#first column of mod_en is the actual odd, followed by which bin it falls into
#mod_en_norm is the normalization factor for ensemble members
#len5: 7 bookkeepers, 0:B365,1:BW,2:IW,3:PS,4:WH,5:VC,6:Bet Brain Mod-en
title1 = ['Bet365','Bet & Win', 'Interwetten','Pinnacle','William Hill','BetVictor','Betbrain']
bm_entry = np.array([[22,23,24],[25,26,27],[28,29,30],[31,32,33],[34,35,36],[37,38,39],[42,44,46]])
len5 = 7
xedge = np.arange(95,0,-5)
xcenter = xedge+2.5
len4 = len(xedge)
obs = np.zeros((len1,len3))
mod_en = np.zeros((len1,len5,len3,len4+1))
post_en = np.zeros((len5,len3,len4,5))
header = list(data_raw.columns.values)
cp = np.zeros((len5+1,len3,2))
data_raw["Date_Full"] = ""
data_raw["Season"]=""
print list(data_raw.columns.values)
for i in range(len1):
    if isinstance(data_raw.iat[i,1],float) == False and data_raw.iat[i,1] != 'Date':
        string1 = (data_raw.iat[i,1]).split("/")
        mm = int(string1[1])
        if len(string1[2])>2:
            yyyy = int(string1[2])
        else:
            yyyy = int(string1[2])+2000
        data_raw.iat[i,len2] = str(yyyy)+'-'+str(string1[1])+'-'+str(string1[0])
        if mm>=8:
            data_raw.iat[i,len2+1] = str(yyyy + 0.5)
        else:
            data_raw.iat[i,len2+1] = str(yyyy - 0.5)
data1 = data_raw.sort_values(by=['Div', 'Season'])
block
#data_raw['Date'] = pd.to_datetime(data_date)

###############       Team Statistics       ############################
#Div: League FTHG/HG: Full Time Home Team Goals, FTAG/AG:FTAwayTG 4-5
#FTR/Res: Full Time results (HomeDrawAway)
#Attendance, Referee, HS: Home Shots, AS: Away Shots
#HST: HS on Target, AST: AS on Target,
#HHW/AWH: HT/AT Hit Woodwork
#HC/AC: H/A Corners, HF/AF: HT/AT Foul committed
#HFKC/AFKC: H/A Free Kicks Conceded
#HO/AO: H/A Offsides
#HY/AY, HR/AR: H/A Yellow/Red Card
#HBP/ABP: H/A Booking(Friendship) Points
########################################################################
##############       Odds Statistics        ############################
#H/D/A  : home/draw/away win odds
#>2.5   : over/under 2.5 goals
#AHH/A  : Asian Handicap home/away win odds
#AH(h)  : Size of AH
#CH/D/A : Closing home/draw/away odds
#1X2    ：Ensemble totals for BetBrain win
#Mx/Av  : Maximum/Average win Odds
#OU     : Ensemble totals for BetBrain over/under 2.5
##############       Bookmarkers            ############################
#B365: Bet365 22-24          SO  : Sporting Odds
#BS  : Blue Square       SB  : Sportingbets
#BW  : Bet & Win 25-27        SJ  : Stan James
#GB  : Gamebookers       SY  ：Stanleybet
#IW  : Interwetten 28-30      VC  : BetVictor 37-39
#LB  : Ladbrokes         WH  : William Hill 34-36
#PS/P: Pinnacle 31-33         Bb* : Betbrain ensemble 40-57
for i in range(len1):
    if data_raw.iat[i,4]>=0 and data_raw.iat[i,5]>=0:
        if data_raw.iat[i,4] > data_raw.iat[i,5]:
            obs[i,0] = 1
        elif data_raw.iat[i,4] == data_raw.iat[i,5]:
            obs[i,1] = 1
        else:
            obs[i,2] = 1
    for ii in range(len5):
        if isinstance(data_raw.iat[i,bm_entry[ii,0]],float) == True\
           and data_raw.iat[i,bm_entry[ii,0]]>=1.0\
           and data_raw.iat[i,bm_entry[ii,1]]>=1.0\
           and data_raw.iat[i,bm_entry[ii,2]]>=1.0:
            mod_en_norm = 1/data_raw.iat[i,bm_entry[ii,0]]+1/data_raw.iat[i,bm_entry[ii,1]]+1/data_raw.iat[i,bm_entry[ii,2]]
            mod_en[i,ii,0,0] = data_raw.iat[i,bm_entry[ii,0]]*mod_en_norm
            mod_en[i,ii,1,0] = data_raw.iat[i,bm_entry[ii,1]]*mod_en_norm
            mod_en[i,ii,2,0] = data_raw.iat[i,bm_entry[ii,2]]*mod_en_norm
            for j in range(len3):
                if 100/mod_en[i,ii,j,0]>=xedge[0]:
                    mod_en[i,ii,j,1] = 1
                    post_en[ii,j,0,3] = post_en[ii,j,0,3]+100/mod_en[i,ii,j,0]
                elif 100/mod_en[i,ii,j,0]<=xedge[len4-1]:
                    mod_en[i,ii,j,len4] = 1
                    post_en[ii,j,len4-1,3] = post_en[ii,j,len4-1,3]+100/mod_en[i,ii,j,0]
                elif 100/mod_en[i,ii,j,0]>0:
                    for k in range(len4-2):
                        if 100/mod_en[i,ii,j,0]>=xedge[k+1] and 100/mod_en[i,ii,j,0]<xedge[k]:
                            mod_en[i,ii,j,k+1] = 1
                            post_en[ii,j,k,3] = post_en[ii,j,k,3]+100/mod_en[i,ii,j,0]
                            break

for j in range(len3):
    cp[len5,j,0] = 100*np.sum(obs[:,j])/np.sum(obs)
    for ii in range(len5):
        cp[ii,j,0] = np.mean(np.ma.masked_invalid(100/mod_en[:,ii,j,0]))
        cp[ii,j,1] = np.std(np.ma.masked_invalid(100/mod_en[:,ii,j,0]))

mod_hbias_glob = cp[:,0,0]-cp[:,2,0]
"""
Obsolete manually defined dynamic threshold
            if mod_en[i,j,0]<=3:
                mod_en[i,j,1+int((mod_en[i,j,0]-1)/0.2)] = 1
            elif mod_en[i,j,0]<=4.5:
                mod_en[i,j,11+int((mod_en[i,j,0]-3)/0.3)] = 1
            elif mod_en[i,j,0]<=9.5:
                mod_en[i,j,16+int(mod_en[i,j,0]-4.5)] = 1
            elif mod_en[i,j,0]>9.5:
                mod_en[i,j,20] = 1
"""
for j in range(len3):
    post_en[:,j,:,2] = np.sum(mod_en[:,:,j,1:],axis=0)
    for k in range(len4):
        for ii in range(len5):
            if post_en[ii,j,k,2] >= 0.02*np.sum(mod_en[:,ii,:,1:]):
                post_en[ii,j,k,0] = 100*np.sum(obs[:,j]*mod_en[:,ii,j,k+1])/np.sum(mod_en[:,ii,j,k+1])
                post_en[ii,j,k,4] = post_en[ii,j,k,3]/np.sum(mod_en[:,ii,j,k+1])
"""
        if k<10 and j==0:
            xedge[k] = 1/(1.1+0.2*k)
        elif k<15 and j==0:
            xedge[k] = 1/(3.15+0.3*(k-10))
        elif k>=15 and j==0:
            xedge[k] = 1/(4.5+(k-15))
"""
        
post_en[:,:,:,1] = post_en[:,:,:,0] - post_en[:,:,:,4]
#plot_data = 100*np.mean(np.ma.masked_where(post_en[:,:,2]==0,post_en[:,:,2]),axis=0)
fig = plt.figure(1,figsize=(15,10))
ax=subplot((len5+1)*50+21)
plt.plot(xcenter,post_en[6,0,:,2],xcenter,post_en[6,1,:,2],xcenter,post_en[6,2,:,2],linewidth=2.0)
legend(('Home win','Draw','Away win'),loc='upper right')
plt.gca().invert_xaxis()
title(r'Number of matches categorized into each bin')
for i in range(len5):
    ax=subplot((len5+1)*50+22+i)
    plt.plot(xcenter,post_en[i,0,:,1],xcenter,post_en[i,1,:,1],xcenter,post_en[i,2,:,1],linewidth=2.0)
    legend(('Home win','Draw','Away win'),loc='upper right')
    plt.gca().invert_xaxis()
    if i>=5:
        plt.xlabel(r'Possibilities in 100%')
    title(r'Difference between '+title1[i]+' and obseved possibilities')
show()


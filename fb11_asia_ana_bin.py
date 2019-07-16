from scipy import *
from pylab import *
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
from difflib import SequenceMatcher
path1 = '/users/jk/11/xzhang/DAT112/torneo_data/'
data_raw= pd.read_pickle(path1+'11_odds_history_v2.csv')
#row (len1=num of match), column (len2=info) for the table
len1,len10 = shape(data_raw)
len2 = len10-7
#len3: H/D/A
title3 = ['Home','Draw','Away']
len3 = len(title3)
#len4: odd bins (total 20: 0.1 step from 1-2, 0.2 step from 2-3, 1 step from 3-7)
#first column of mod_en is the actual odd, followed by which bin it falls into
#mod_en_norm is the normalization factor for ensemble members
#len5: 7 bookkeepers, 0:B365,1:BW,2:IW,3:PS,4:WH,5:VC,6:Bet Brain Mod-en
title1 = ['Bet365','Gamebookers','Ladbroke','Betbrain']
len5 = len(title1)
#len8: number of leagues included: D1,E0,F1,I1,NI,SP1
#Bundesliga:'D1', 'D2', Premier League:'E0', 'E1', 'E2', 'E3', Ligue: 'F1', 'F2', 'G1',
#Serie:'I1', 'I2', Eredivisie:'N1', Scotland:'SC0', 'SC1', 'SC2', 'SC3',
#La Liga:'SP1', 'SP2'
title2 = ['Bundesliga','Premier League','Ligue 1','Serie A','Eredivisie','La Liga']
len8 = len(title2)
#Entry index for each bookmarker
bm_entry = np.array([[87,88,89],[81,82,83],[84,85,86],[53,55,57]])
#xedge: categorization of different propabilities
xedge = np.arange(-5,5,0.25)
xcenter = xedge+0.125
len4 = len(xedge)
header = list(data_raw.columns.values)
#len6: max number of matches per league per season
len6 = 400
#len7: max number of seasons from 2001-2020
len7 = 19
#data2_obs: the result of w/d/l based on AHsize of BetBrain
data2_obs = np.zeros((len8,len7,len6,len5,len3))
mod_en = np.zeros((len8,len7,len6,len5,len3,len4+1))
post_en = np.zeros((len8,len7,len5,len3,len4,5))
cp = np.zeros((len8,len7,len5,len3,3))
counter = np.zeros((len8,len7)).astype(int)
team = data_raw.HomeTeam.unique()
#team_att_norm = np.min(data_raw['Team_ATT_Home'])
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
#Manually defined threshold: hot streak: >=9pts in 4 rounds, cold streak: <=5pts in 4 rounds.
#kk is the iterator for home streak or away streak
#ci is the iterator for hot streak or cold streak
for i in range(len1):
    if data_raw.iat[i,0] == 'D1':
        li = 0
    elif data_raw.iat[i,0] == 'E0':
        li = 1
    elif data_raw.iat[i,0] == 'F1':
        li = 2
    elif data_raw.iat[i,0] == 'I1':
        li = 3
    elif data_raw.iat[i,0] == 'N1':
        li = 4
    elif data_raw.iat[i,0] == 'SP1':
        li = 5
    else:
        li = None
    if li != None:
        if data_raw.iat[i,len2+1] != '' and float(data_raw.iat[i,len2+1])>=2000:
            di = int(float(data_raw.iat[i,len2+1])-2000.5)
            counter[li,di] = counter[li,di]+1
        for ii in range(len5):
            if float(data_raw.iat[i,4])>=0 and float(data_raw.iat[i,5])>=0 and abs(float(data_raw.iat[i,bm_entry[ii,0]]))>=0:
                if float(data_raw.iat[i,4]) - float(data_raw.iat[i,5]) + float(data_raw.iat[i,bm_entry[ii,0]]) > 0:
                    data2_obs[li,di,counter[li,di],ii,0] = 1
                elif float(data_raw.iat[i,4]) - float(data_raw.iat[i,5]) + float(data_raw.iat[i,bm_entry[ii,0]])==0:
                    data2_obs[li,di,counter[li,di],ii,1] = 1
                else:
                    data2_obs[li,di,counter[li,di],ii,2] = 1
            if isinstance(data_raw.iat[i,bm_entry[ii,0]],float) == True\
                    and data_raw.iat[i,bm_entry[ii,1]]>=1.0\
                    and data_raw.iat[i,bm_entry[ii,2]]>=1.0:
                mod_en_norm = 1/data_raw.iat[i,bm_entry[ii,1]]+1/data_raw.iat[i,bm_entry[ii,2]]
                mod_en[li,di,counter[li,di],ii,0,0] = data_raw.iat[i,bm_entry[ii,1]]*mod_en_norm
                mod_en[li,di,counter[li,di],ii,2,0] = data_raw.iat[i,bm_entry[ii,2]]*mod_en_norm
                if abs(float(data_raw.iat[i,bm_entry[ii,0]])) <=xedge[0]:
                    mod_en[li,di,counter[li,di],ii,:,1] = 1
                    post_en[li,di,ii,:,0,3] = post_en[li,di,ii,:,0,3]+100/mod_en[li,di,counter[li,di],ii,:,0]                    
                elif abs(float(data_raw.iat[i,bm_entry[ii,0]])) >=xedge[-1]:
                    mod_en[li,di,counter[li,di],ii,:,len4] = 1
                    post_en[li,di,ii,:,len4-1,3] = post_en[li,di,ii,:,len4-1,3]+100/mod_en[li,di,counter[li,di],ii,:,0]
                elif abs(float(data_raw.iat[i,bm_entry[ii,0]])) >0:
                    for k in range(len4-2):
                        if abs(float(data_raw.iat[i,bm_entry[ii,0]]))>=xedge[k] and abs(float(data_raw.iat[i,bm_entry[ii,0]]))<xedge[k+1]:
                            mod_en[li,di,counter[li,di],ii,:,k+1] = 1
                            post_en[li,di,ii,:,k,3] = post_en[li,di,ii,:,k,3]+100/mod_en[li,di,counter[li,di],ii,:,0]
                            break
#cp: statistics on H/D/A between obs and mean/std of model prediction
for li in range(len8):
    for di in range(len7):
        for j in [0,2]:
            for ii in range(len5):
                cp[li,di,ii,j,0] = 100*np.sum(data2_obs[li,di,:counter[li,di],ii,j])/np.sum(data2_obs[li,di,:counter[li,di],ii,:])
                cp[li,di,ii,j,1] = np.mean(np.ma.masked_invalid(100/mod_en[li,di,:counter[li,di],ii,j,0]))
                cp[li,di,ii,j,2] = np.std(np.ma.masked_invalid(100/mod_en[li,di,:counter[li,di],ii,j,0]))

#mod_hbias_glob = cp[:,:,:,0,0]-cp[:,:,:,2,0]
#hbias_filt: year averaged home/away/streak info
'''
hbias = np.mean(np.ma.masked_invalid(cp),axis=4)[:,:,:,:,:,:2]
hbias_filt = np.mean(np.ma.masked_where(hbias<=0,hbias),axis=3)
ind = np.arange(6)
width = 0.35
hbias2 = np.reshape(hbias_filt,(6,len8,len3,2))
title9 = ['Observation','Model']

for ii in range(2):
    fig = plt.figure(6+ii,figsize=(15,10))
    for k in range(len8):
        ax = subplot(len8*50+21+k)
        p1 = plt.bar(ind,hbias2[:,k,0,ii],width,color='g')
        p2 = plt.bar(ind,hbias2[:,k,2,ii],width,bottom=hbias2[:,k,0,ii],color='r')
        plt.ylabel('Probability')
        title(r'Odds on streaks for '+title2[k]+' estimated by '+title9[ii])
        plt.xticks(ind, ('HH','AH','HC','AC','HG','AG'))
        if ii==0 and k==0:
            plt.legend((p1[0],p2[0]),('Home','Away'))
        if ii==1:
            plt.ylim([48,52])
        else:
            plt.ylim([30,100])


for i in range(2):
    for j in range(3):
        fig = plt.figure(3*i+j,figsize=(15,10))
        for k in range(len8): 
            ax = subplot(len8*50+21+k)
            plt.plot(year,hbias[i,j,k,:,0,1],'r^',year,hbias[i,j,k,:,0,0],'b^',
                     year,hbias[i,j,k,:,2,1],'rv',year,hbias[i,j,k,:,2,0],'bv')
            title(r'Odds for '+title6[i]+title5[j]+'streak for '+title2[k])
            plt.gca().set_ylim(bottom=10)
            ylim([30,60])
            #if k==0:
                #legend(('Model Home','Obs Home','Model Draw','Obs Draw','Model Away','Obs Away'),loc='upper right')


year = np.arange(2010.5,2017.5,1)
hbias3 = hbias[0,2,:,:,0,:] - hbias[1,2,:,:,2,:]
fig = plt.figure(0,figsize=(15,10))
for i in range(len8):
    ax=subplot(len8*50+21+i)
    plt.plot(year,hbias3[i,:,1],'ro',year,hbias3[i,:,0],'go')
    title(r'Home-Away win bias for '+title2[i])
    if i==0:
        legend(('Bookmakers','Observations'),loc='upper right')
'''
year = np.arange(2000.5,2019.5,1)    
#post_en includes info on odd of matches in each category between model and obs, and # of obs fall in each category
#row 0: observation odds, row 1: odd diff between model and obs, row 2: number of matches falling into each odd category
#row 3: model odds sum,   row 4: model odds

for li in range(len8):
    for di in range(len7):
        for j in range(len3):
            post_en[li,di,:,j,:,2] = np.sum(mod_en[li,di,:counter[li,di],:,j,1:],axis=0)
            for k in range(len4):
                for ii in range(len5):
                    if post_en[li,di,ii,j,k,2] >= 0.02*np.sum(mod_en[li,di,:,ii,:,1:]):
                        post_en[li,di,ii,j,k,0] = 100*np.sum(data2_obs[li,di,:counter[li,di],ii,j]*\
                                                      mod_en[li,di,:counter[li,di],ii,j,k+1])/np.sum(mod_en[li,di,:counter[li,di],ii,j,k+1])
                        post_en[li,di,ii,j,k,4] = post_en[li,di,ii,j,k,3]/np.sum(mod_en[li,di,:counter[li,di],ii,j,k+1])
        
post_en[:,:,:,:,:,1] = post_en[:,:,:,:,:,0] - post_en[:,:,:,:,:,4]
#diff_en = np.mean(np.ma.masked_invalid(post_en[:,:,:,:,:,1]),axis=2)
data2a = np.ma.masked_where(post_en[:,:,:,:,:,0]<=0,post_en[:,:,:,:,:,1])
data2b = np.ma.masked_where(post_en[:,:,:,:,:,4]<=0,data2a)
data2c = np.ma.masked_where(data2b<=0,data2b)
data2d = np.mean(np.ma.masked_invalid(data2b[:,:,:,:,:]),axis=2)[:,5:,:,5:-2]
data3a = np.ma.masked_where(post_en[:,:,:,:,:,0]<=0,post_en[:,:,:,:,:,2])
data3b = np.ma.masked_where(post_en[:,:,:,:,:,4]<=0,data3a)
data3c = np.ma.masked_where(post_en[:,:,:,:,:,1]<=0,data3b)
data3d = np.mean(np.ma.masked_invalid(data3c[:,:,:,:,:]),axis=2)[:,5:,:,5:-2]

delta = 1
for j in range(len3):
    fig = plt.figure(12+j,figsize=(15,10))
    for li in range(len8):
        ax=subplot(len8*50+21+li)
        clevs = np.arange(-10,10,delta)
        #clevs = np.arange(0,np.max(data2d[li,:,j,:]),delta)
        CS = contourf(year[5:],xcenter[5:-2],np.transpose(data2d[li,:,j,:]),\
                      clevs,animated=True,extend='both',cmap=get_cmap("bwr"))
        title(r'Odd diff (obs-mod) for '+title3[j]+' '+title2[li])
        #title(r'# of observations for '+title3[j]+' '+title2[li])
        plt.colorbar(mappable=None, cax=None, ax=None)
        #plt.gca().invert_yaxis()
            
data4a = np.mean(np.ma.masked_where(post_en[:,4:17,:,:,:,1]==0,post_en[:,4:17,:,:,:,1]),axis=1)

for li in range(len8):
    fig = plt.figure(li,figsize=(15,10))
    ax=subplot((len5+2)*50+21)
    plt.plot(xcenter,np.sum(post_en[li,:,-1,0,:,2],axis=0),xcenter,np.sum(post_en[li,:,-1,2,:,2],axis=0),linewidth=2.0)
    legend(('Home win','Away win'),loc='upper right')
    plt.gca().invert_xaxis()
    title(r'Number of matches categorized into each bin for '+title2[li])
    for i in range(len5):
        ax=subplot((len5+2)*50+22+i)
        plt.plot(xcenter,data4a[li,i,0,:],xcenter,data4a[li,i,2,:],linewidth=2.0)
        legend(('Home win','Away win'),loc='upper right')
        plt.gca().invert_xaxis()
        if i>=len5-1:
            plt.xlabel(r'Possibilities in 100%')
        title(r'Difference between '+title1[i]+' and obseved possibilities')

show()


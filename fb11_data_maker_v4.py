from scipy import *
from pylab import *
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import sqlite3 as sq3
from difflib import SequenceMatcher
import math
path1 = '/users/jk/11/xzhang/DAT112/torneo_data/'
data_raw = pd.read_csv(path1+'11_odds_history.csv',sep=',',header='infer')
database = path1+'database.sqlite'
conn = sq3.connect(database)
c = conn.cursor()
table_list = pd.read_sql("""SELECT * FROM sqlite_master
                        WHERE type='table';""", conn)
len11,len12 = shape(table_list)
team_uni = pd.read_sql('SELECT * FROM Team;', conn)
team_sort = team_uni.sort_values('team_api_id')
len13,len14 = shape(team_sort)
team_att = pd.read_sql('SELECT * FROM Team_Attributes;', conn)
team_att_sort = team_att.sort_values(['team_api_id','date'])
len15,len16 = shape(team_att_sort)
team_att2 = np.zeros((len13,7))
count5 = 0
team_att1 = team_sort['team_long_name']
data_team1 = ["" for x in range(len13)]
for i in range(len13):
    data_team1[i] = team_att1[i].encode('ascii','ignore')
for i in range(len15):
    while team_att_sort.iat[i,2] != team_sort.iat[count5,1]:
        count5 = count5+1
    if team_att_sort.iat[i,2] == team_sort.iat[count5,1]:
        team_att_time = team_att_sort.iat[i,3]
        team_att_year = int(team_att_time.split('-')[0])
        team_att_mon  = int(team_att_time.split('-')[1])
        if team_att_mon >= 7:
            year_i = int(team_att_year-2010)
        else:
            year_i = int(team_att_year-2011)
        team_att_tot = 0
        for j in range(4,len16):
            if j!=5 and j!=7 and j!=9 and j!=10 and j!=12 and j!=14 and\
               j!=16 and j!=17 and j!=19 and j!=21 and j!=23 and j!=24:
                if float(team_att_sort.iat[i,j])>0:
                    team_att_tot = team_att_tot + float(team_att_sort.iat[i,j])
        team_att2[count5,year_i] = team_att_tot
#np.save(path1+'team_name_list.npy',team_att1)
#np.save(path1+'team_att_tot.npy',team_att2)
#row (len1=num of match), column (len2=info) for the table
len1,len2 = shape(data_raw)
#len3: H/D/A
title3 = ['Home','Draw','Away']
len3 = len(title3)
#len4: odd bins (total 20: 0.1 step from 1-2, 0.2 step from 2-3, 1 step from 3-7)
#first column of mod_en is the actual odd, followed by which bin it falls into
#mod_en_norm is the normalization factor for ensemble members
#len5: 7 bookkeepers, 0:B365,1:BW,2:IW,3:PS,4:WH,5:VC,6:Bet Brain Mod-en
title1 = ['Bet365','Bet & Win', 'Interwetten','Pinnacle','William Hill','BetVictor','Betbrain']
len5 = len(title1)
#len8: number of leagues included: D1,E0,F1,I1,NI,SP1
#Bundesliga:'D1', 'D2', Premier League:'E0', 'E1', 'E2', 'E3', Ligue: 'F1', 'F2', 'G1',
#Serie:'I1', 'I2', Eredivisie:'N1', Scotland:'SC0', 'SC1', 'SC2', 'SC3',
#La Liga:'SP1', 'SP2'
title2 = ['Bundesliga','Premier League','Ligue 1','Serie A','Eredivisie','La Liga']
len8 = len(title2)
#Entry index for each bookmarker
bm_entry = np.array([[22,23,24],[25,26,27],[28,29,30],[31,32,33],[34,35,36],[37,38,39],[42,44,46]])
#xedge: categorization of different propabilities
xedge = np.arange(95,0,-5)
xcenter = xedge+2.5
len4 = len(xedge)
header = list(data_raw.columns.values)
#len6: max number of matches per league per season
len6 = 400
#len7: max number of seasons from 2001-2020
len7 = 19
data2_obs = np.zeros((2,2,len8,len7,len6,len3))
mod_en = np.zeros((2,2,len8,len7,len6,len5,len3,len4+1))
post_en = np.zeros((2,2,len8,len7,len5,len3,len4,5))
cp = np.zeros((2,2,len8,len7,len5+1,len3,2))
counter = np.zeros((2,2,len8,len7)).astype(int)
data_raw["Date_Full"] = ""
data_raw["Season"]=""
data_raw["Row_Index"] = np.arange(len1)
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
        if mm>=7:
            data_raw.iat[i,len2+1] = str(yyyy + 0.5)
        else:
            data_raw.iat[i,len2+1] = str(yyyy - 0.5)
data1 = data_raw.sort_values(by=['Div', 'Season','Date_Full'],ascending=[True,False,True])
#len_team: how many teams are included in the dataset
team = data1.HomeTeam.unique()
len_team = len(data1.HomeTeam.unique())
len_sea = 60
data_stk = np.zeros((len_team,len7,len_sea))
data_tmp = np.empty((len1,4))
data_tmp[:,:] = np.nan
team_finder = np.zeros(len13)
for i in range(len_team):
    if isinstance(team[i],basestring)==True and team[i] != 'HomeTeam' and team[i] != 'AwayTeam':
        for cc in range(len13):
            team_finder[cc] = SequenceMatcher(None,team[i],data_team1[cc]).ratio()
        i_team = np.argmax(team_finder)
    #print team[i],data_team1[i_team]
        for j in range(len7):
            data_team = pd.concat([data1.loc[data1['HomeTeam']==team[i]],data1.loc[data1['AwayTeam']==team[i]]],axis=0)
            data2 = data_team.loc[data_team['Season']==str(2000.5+j)]
            len_team1 = shape(data2)[0]
            #if len_team1>0:
            data3=data2.sort_values(by=['Date_Full'],ascending=[True])
            count1 = 0
            for ii in range(len_team1):
                if data3.iat[ii,len2+1] != '' and float(data3.iat[ii,len2+1])>=2000\
                        and data3.iat[ii,4]>=0 and data3.iat[ii,5]>=0:
                    if data3.iat[ii,2]==team[i]:
                        if data3.iat[ii,4]>data3.iat[ii,5]:
                            data_stk[i,j,count1] = 3
                        elif data3.iat[ii,4] == data3.iat[ii,5]:
                            data_stk[i,j,count1] = 1
                        else:
                            data_stk[i,j,count1] = 0
                    elif data3.iat[ii,3]==team[i]:
                        if data3.iat[ii,4]>data3.iat[ii,5]:
                            data_stk[i,j,count1] = 0
                        elif data3.iat[ii,4] == data3.iat[ii,5]:
                            data_stk[i,j,count1] = 1
                        else:
                            data_stk[i,j,count1] = 3
                    if count1 >= 4:
                        if data3.iat[ii,2]==team[i]:
                            data_tmp[data3.iat[ii,len2+2],0] = np.sum(data_stk[i,j,count1-4:count1])
                            if j>=10 and j<=16:
                                data_tmp[data3.iat[ii,len2+2],2] = team_att2[i_team,j-10]
                        elif data3.iat[ii,3]==team[i]:
                            data_tmp[data3.iat[ii,len2+2],1] = np.sum(data_stk[i,j,count1-4:count1])
                            if j>=10 and j<=16:
                                data_tmp[data3.iat[ii,len2+2],3] = team_att2[i_team,j-10]
                    #elif count1 == len_team1-1:
                        #for jj in range(len_team1):
                            #if data3.iat[jj,2]==team[i]:
                                #data_tmp[data3.iat[jj,len2+2],2] = np.sum(data_stk[i,j,:])
                            #elif data3.iat[jj,3]==team[i]:
                                #data_tmp[data3.iat[jj,len2+2],3] = np.sum(data_stk[i,j,:])
                    count1 = count1 + 1 
            
data_raw["4Streak_Home"] = data_tmp[:,0]
data_raw["4Streak_Away"] = data_tmp[:,1]
data_raw["Team_ATT_Home"] = data_tmp[:,2]
data_raw["Team_ATT_Away"] = data_tmp[:,3]
data_raw.to_pickle(path1+'11_odds_history_v2.csv')
print "done"

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
    for kk in range(2):
        if data_tmp[i,kk]>=9:
            ci = 0
        elif data_tmp[i,kk]<=5:
            ci = 1
        else:
            ci = -1
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
        if li != None and ci>=0:
            if data_raw.iat[i,len2+1] != '' and float(data_raw.iat[i,len2+1])>=2000:
                di = int(float(data_raw.iat[i,len2+1])-2000.5)
                counter[kk,ci,li,di] = counter[kk,ci,li,di]+1
            if data_raw.iat[i,4]>=0 and data_raw.iat[i,5]>=0:
                if data_raw.iat[i,4] > data_raw.iat[i,5]:
                    data2_obs[kk,ci,li,di,counter[kk,ci,li,di],0] = 1
                elif data_raw.iat[i,4] == data_raw.iat[i,5]:
                    data2_obs[kk,ci,li,di,counter[li,di],1] = 1
                else:
                    data2_obs[kk,ci,li,di,counter[li,di],2] = 1
            for ii in range(len5):
                if isinstance(data_raw.iat[i,bm_entry[ii,0]],float) == True\
                        and data_raw.iat[i,bm_entry[ii,0]]>=1.0\
                        and data_raw.iat[i,bm_entry[ii,1]]>=1.0\
                        and data_raw.iat[i,bm_entry[ii,2]]>=1.0:
                    mod_en_norm = 1/data_raw.iat[i,bm_entry[ii,0]]+1/data_raw.iat[i,bm_entry[ii,1]]+1/data_raw.iat[i,bm_entry[ii,2]]
                    mod_en[kk,ci,li,di,counter[kk,ci,li,di],ii,0,0] = data_raw.iat[i,bm_entry[ii,0]]*mod_en_norm
                    mod_en[kk,ci,li,di,counter[kk,ci,li,di],ii,1,0] = data_raw.iat[i,bm_entry[ii,1]]*mod_en_norm
                    mod_en[kk,ci,li,di,counter[kk,ci,li,di],ii,2,0] = data_raw.iat[i,bm_entry[ii,2]]*mod_en_norm
                    for j in range(len3):
                        if 100/mod_en[kk,ci,li,di,counter[kk,ci,li,di],ii,j,0]>=xedge[0]:
                            mod_en[kk,ci,li,di,counter[kk,ci,li,di],ii,j,1] = 1
                            post_en[kk,ci,li,di,ii,j,0,3] = post_en[kk,ci,li,di,ii,j,0,3]+100/mod_en[kk,ci,li,di,counter[kk,ci,li,di],ii,j,0]
                        elif 100/mod_en[kk,ci,li,di,counter[kk,ci,li,di],ii,j,0]<=xedge[len4-1]:
                            mod_en[kk,ci,li,di,counter[kk,ci,li,di],ii,j,len4] = 1
                            post_en[kk,ci,li,di,ii,j,len4-1,3] = post_en[kk,ci,li,di,ii,j,len4-1,3]+100/mod_en[kk,ci,li,di,counter[kk,ci,li,di],ii,j,0]
                        elif 100/mod_en[kk,ci,li,di,counter[kk,ci,li,di],ii,j,0]>0:
                            for k in range(len4-2):
                                if 100/mod_en[kk,ci,li,di,counter[kk,ci,li,di],ii,j,0]>=xedge[k+1] and 100/mod_en[kk,ci,li,di,counter[kk,ci,li,di],ii,j,0]<xedge[k]:
                                    mod_en[kk,ci,li,di,counter[kk,ci,li,di],ii,j,k+1] = 1
                                    post_en[kk,ci,li,di,ii,j,k,3] = post_en[kk,ci,li,di,ii,j,k,3]+100/mod_en[kk,ci,li,di,counter[kk,ci,li,di],ii,j,0]
                                    break
#cp: statistics on H/D/A between obs and mean/std of model prediction
for kk in range(2):
    for ci in range(2):
        for li in range(len8):
            for di in range(len7):
                for j in range(len3):
                    cp[kk,ci,li,di,len5,j,0] = 100*np.sum(data2_obs[kk,ci,li,di,:counter[kk,ci,li,di],j])/np.sum(data2_obs[kk,ci,li,di,:counter[kk,ci,li,di],:])
                    for ii in range(len5):
                        cp[kk,ci,li,di,ii,j,0] = np.mean(np.ma.masked_invalid(100/mod_en[kk,ci,li,di,:counter[kk,ci,li,di],ii,j,0]))
                        cp[kk,ci,li,di,ii,j,1] = np.std(np.ma.masked_invalid(100/mod_en[kk,ci,li,di,:counter[kk,ci,li,di],ii,j,0]))
block
mod_hbias_glob = cp[:,:,:,0,0]-cp[:,:,:,2,0]
hbias = np.zeros((len8,len7,2))
hbias[:,:,0] = np.mean(np.ma.masked_invalid(mod_hbias_glob[:,:,:-1]),axis=2)
hbias[:,:,1] = np.ma.masked_invalid(mod_hbias_glob[:,:,-1])
year = np.arange(2000.5,2019.5,1)

'''
fig = plt.figure(0,figsize=(15,10))
for i in range(len8):
    ax=subplot(len8*50+21+i)
    plt.plot(year,hbias[i,:,0],'ro',year,hbias[i,:,1],'go')
    title(r'Home-Away win bias for '+title2[i])
    if i==0:
        legend(('Bookmakers','Observations'),loc='upper right')
'''

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
                        post_en[li,di,ii,j,k,0] = 100*np.sum(data2_obs[li,di,:counter[li,di],j]*\
                                                      mod_en[li,di,:counter[li,di],ii,j,k+1])/np.sum(mod_en[li,di,:counter[li,di],ii,j,k+1])
                        post_en[li,di,ii,j,k,4] = post_en[li,di,ii,j,k,3]/np.sum(mod_en[li,di,:counter[li,di],ii,j,k+1])
"""
        if k<10 and j==0:
            xedge[k] = 1/(1.1+0.2*k)
        elif k<15 and j==0:
            xedge[k] = 1/(3.15+0.3*(k-10))
        elif k>=15 and j==0:
            xedge[k] = 1/(4.5+(k-15))
"""
        
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
            
#plot_data = 100*np.mean(np.ma.masked_where(post_en[:,:,2]==0,post_en[:,:,2]),axis=0)
"""
for li in range(len8):
    fig = plt.figure(li,figsize=(15,10))
    ax=subplot((len5+1)*50+21)
    plt.plot(xcenter,post_en[li,17,6,0,:,2],xcenter,post_en[li,17,6,1,:,2],xcenter,post_en[li,17,6,2,:,2],linewidth=2.0)
    legend(('Home win','Draw','Away win'),loc='upper right')
    plt.gca().invert_xaxis()
    title(r'Number of matches categorized into each bin for '+title2[li])
    for i in range(len5):
        ax=subplot((len5+1)*50+22+i)
        plt.plot(xcenter,post_en[li,17,i,0,:,1],xcenter,post_en[li,17,i,1,:,1],xcenter,post_en[li,17,i,2,:,1],linewidth=2.0)
        legend(('Home win','Draw','Away win'),loc='upper right')
        plt.gca().invert_xaxis()
        if i>=5:
            plt.xlabel(r'Possibilities in 100%')
        title(r'Difference between '+title1[i]+' and obseved possibilities')
"""
show()


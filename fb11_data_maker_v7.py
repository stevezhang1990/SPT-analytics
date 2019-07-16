from scipy import *
from pylab import *
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fb11lib import league_finder
import math
import warnings
warnings.filterwarnings("ignore")
#path of datasets
path1 = '/users/jk/11/xzhang/DAT112/torneo_data/'
data_odds = pd.read_pickle(path1+'f11_odds_history_v3.csv')
odds_obs_raw = np.load(path1+'f11_odds_obs.npy')
xedge = np.arange(95,0,-5)
xcenter = xedge+2.5
# len8-# of leagues, len7-# of seasons from 2001,len5-# of bookmakers,len3-H/D/A, len4-odds category, 
# 5: 0-obs odds, 1-diff between obs-model odds, 2-# of mod in each cate 3- # of obs in each cate
# 4- mod odds
len8b = 5
len7b = 6
len9 = 380
odds_obs1 = odds_obs_raw[[1,5,0,3,2],9:15,:,:,:,0]
odds_obs = odds_obs1[:,:,[0,5],:,:]
len8,len7,len5,len3,len4 = shape(odds_obs)
#data_odds1 = data_odds.loc[(data_odds['Season']=='2010.5') & (data_odds['Div']=='E0')]
data1 = data_odds.loc[(data_odds['5PTS_h'].values>=0) &\
                      (data_odds['DRAT_h'].values>0)  &\
                      (data_odds['DRAT_a'].values>0)  &\
                      (data_odds['PLA_h'].values>0)   &\
                      (data_odds['PLA_a'].values>0)].sort_values(by=['Date_Full'])
header = list(data1.columns.values)
len1,len2 = shape(data1)
#header for different x variables
var_in = ['ORAT_h','DRAT_h','5PTS_h','5PTS_std_h','GOAL_h','GAGN_h','PLA_h',\
         'PLA_std_h','TRAT_h','H/A_h','MODE_h','PACE_h','TACT_h',\
         'ORAT_a','DRAT_a','5PTS_a','5PTS_std_a','GOAL_a','GAGN_a','PLA_a',\
         'PLA_std_a','TRAT_a','H/A_a','MODE_a','PACE_a','TACT_a',\
         'B365H','B365D','B365A','BbAvH','BbAvD','BbAvA','BbAHh']
var_ind = 102
bm_entry = np.array([[17,18,19],[37,39,41]])
#Y output variables: Goal difference (home-away), Odds Home, Odds Draw, Odds Away, W/D/A
var_out = ['GDIF','OHO','ODO','OAO','HW']
xdata_raw = np.zeros((len8b,len7b,len9,len(var_in)))
ydata_raw = np.zeros((len8b,len7b,len9,len(var_out)))
#counter on how many fixtures within each league , each season
counter = np.zeros((len8b,len7b))
#loop around all fixtures
for i in range(len1):
    #find league index
    li = league_finder(data1.iloc[i,0],mode='ind')
    if math.isnan(li)== False:
        #season index
        di = int(float(data1['Season'].iloc[i])-2010.5)
        #compute goal difference
        ydata_raw[li,di,counter[li,di],0] = float(data1['FTHG'].iat[i])-float(data1['FTAG'].iat[i])
        #save x variables
        xdata_raw[li,di,counter[li,di],:26] = data1.iloc[i,var_ind:]
        xdata_raw[li,di,counter[li,di],len(var_in)-1] = data1['BbAHh'].iloc[i]
        #save W/D/A results
        if float(data1['FTHG'].iloc[i])>float(data1['FTAG'].iloc[i]):
            ydata_raw[li,di,counter[li,di],4] = 1
        elif float(data1['FTHG'].iloc[i])==float(data1['FTAG'].iloc[i]):
            ydata_raw[li,di,counter[li,di],4] = 0.5
        elif float(data1['FTHG'].iloc[i])<float(data1['FTAG'].iloc[i]):
            ydata_raw[li,di,counter[li,di],4] = 0
        #compute observed odds
        for ii in range(len5):
            mod_en = np.zeros((2,len3))
            if np.sum(data1.iloc[i,bm_entry[ii,:]])>=3.0:
                #convert odds to probability
                mod_en_norm = 1/float(data1.iat[i,bm_entry[ii,0]])+1/float(data1.iat[i,bm_entry[ii,1]])\
                              +1/float(data1.iat[i,bm_entry[ii,2]])
                #classify matches in each of the odd thresholds.
                for j in range(len3):
                    mod_en[0,j] = float(data1.iat[i,bm_entry[ii,j]])*mod_en_norm
                    xdata_raw[li,di,counter[li,di],26+3*ii+j] = 100/mod_en[0,j]
                    if 100/mod_en[0,j]>=xedge[0]:
                        if odds_obs[li,di,ii,j,len4-1]>0:
                            mod_en[1,j] = odds_obs[li,di,ii,j,0]
                        else:
                            mod_en[1,j] = mod_en[0,j]
                    elif 100/mod_en[0,j]<=xedge[len4-1]:
                        if odds_obs[li,di,ii,j,len4-1]>0:
                            mod_en[1,j]= odds_obs[li,di,ii,j,len4-1]
                        else:
                            mod_en[1,j] = mod_en[0,j]
                    elif 100/mod_en[0,j]>0:
                        for k in range(len4-2):
                            if 100/mod_en[0,j]>=xedge[k+1] and 100/mod_en[0,j]<xedge[k]:
                                if odds_obs[li,di,ii,j,k]>0:
                                    mod_en[1,j] = odds_obs[li,di,ii,j,k]
                                else:
                                    mod_en[1,j] = mod_en[0,j]
                                break
                obs_en_norm = np.sum(mod_en[1,:])                
                ydata_raw[li,di,counter[li,di],1:4] = mod_en[1,:]/obs_en_norm
        counter[li,di] = counter[li,di]+1

#save data
np.save(path1+'xdata_raw.npy',xdata_raw)
np.save(path1+'ydata_raw.npy',ydata_raw)
print np.argwhere(np.isnan(xdata_raw))
print "done"


from scipy import *
from pylab import *
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import sqlite3 as sq3
from fb11lib import * #manual created module

#path of datasets
path1 = '/users/jk/11/xzhang/DAT112/torneo_data/'
################################Dataset loader#################################################
data_odds = pd.read_pickle(path1+'f11_odds_history_v2.csv')
len1,len2 = shape(data_odds)
data_cli = pd.read_pickle(path1+'f11_season_stats.csv')
##In case we need subset##
#data_cli = data_cli1.loc[(data_cli1['season']=='2015-16') & (data_cli1['league']=='Ligue1')]
conn = sq3.connect(path1+'database.sqlite')
c = conn.cursor()
euro_list= pd.read_sql("""SELECT * FROM sqlite_master
                        WHERE type='table';""", conn)
len11,len12 = shape(euro_list)
euro_match = pd.read_sql('SELECT * FROM Match;', conn)
epf1 = pd.read_sql('SELECT * FROM Player_Attributes;', conn)[['player_api_id','date','overall_rating']]
etf = pd.read_sql('SELECT * FROM Team;', conn)[['team_api_id','team_long_name']]
etf1 = etf.sort_values(by=['team_long_name'])
len13 = len(etf1.iloc[:,0])
data_team1 = ["" for x in range(len13)]
for i in range(len13):
    data_team1[i] = (etf1.iat[i,1]).encode('ascii','replace')
################################Header information#############################################
odds_header = list(data_odds.columns.values)
col_del = ['Date','HTHG','HTAG','FTR','HTR','Attendance','HFKC','AFKC','Team_ATT_Home',\
               'Team_ATT_Away','LB','LB.1','LB.2','HO','AO']
#euro_match_header = list(euro_match.columns.values)
#euro_league = pd.read_sql('SELECT * FROM League;', conn)
#team_att = pd.read_sql('SELECT * FROM Team_Attributes;', conn)
#team_att_sort = team_att.sort_values(['team_api_id','date'])
#len15,len16 = shape(team_att_sort)
#list of variables used to calculate season stats:
title8 = ['HS','HST','AF','HC','AY','AR']
title9 = ['AS','AST','HF','AC','HY','HR']
#len3: H/D/A
title3 = ['Home','Draw','Away']
len3 = len(title3)
#len8: number of leagues included: D1,E0,F1,I1,NI,SP1
#Bundesliga:'D1', 'D2', Premier League:'E0', 'E1', 'E2', 'E3', Ligue: 'F1', 'F2', 'G1',
#Serie:'I1', 'I2', Eredivisie:'N1', Scotland:'SC0', 'SC1', 'SC2', 'SC3',
#La Liga:'SP1', 'SP2'
#len_team: how many teams are included in the dataset
team = data_cli['team']
len_team = len(team)
len_sea = 40
#3: each team points, each team five rounds point, each team five rounds point variability 
data_stk = np.zeros((len_team,3,len_sea))
#4: each team's offensive rating or defensive rating, each team's 4 game offensive/defensive rating
data_sta = np.zeros((len_team,6,4,len_sea))
#4: home/away team ORAT, DRAT, score/std, player/std
title5a = ['ORAT_h','DRAT_h','5PTS_h','5PTS_std_h','GOAL_h','GAGN_h','PLA_h',\
           'PLA_std_h','TRAT_h','H/A_h','MODE_h','PACE_h','TACT_h']
title5b = ['ORAT_a','DRAT_a','5PTS_a','5PTS_std_a','GOAL_a','GAGN_a','PLA_a',\
           'PLA_std_a','TRAT_a','H/A_a','MODE_a','PACE_a','TACT_a']
data_tmp = np.empty((len1,13,2))
data_tmp[:,:,:] = np.nan
#2: goal scored, goal committed
team_finder = np.zeros(len13)
#team overall rating, player overall rating, player variability, offensive rating, defensive rating,
#streak(4), home/away parity, last 6 games variability, game odds, asian handicap odds/size,
#game style index, goal last 6 games, goal against last 6 games.
##season average data
################################################################################################
#loop around diff home teams and league
for i in range(len_team):
    #locate league, team and seasons
    lea_odds = league_finder(data_cli['league'].iloc[i])
    data_odds1 = data_odds.loc[data_odds['Div']==lea_odds]
    team_odds = data_odds1.HomeTeam.unique()
    #team matcher: determine index for the same team for different datasets
    odds_i = team_matcher(team.iloc[i],team_odds)
    year0,dummy = (data_cli['season'].iloc[i]).split('-')
    #season convert to year
    year = int(year0)
    year_match = str(year)+'/'+str(year+1)
    if isinstance(team_odds[odds_i],basestring)==True and team_odds[odds_i] != 'HomeTeam' and team_odds[odds_i] != 'AwayTeam':
        euro_i = team_matcher(team_odds[odds_i],data_team1)
        #find all the fixtures for teams for each season
        data1 = pd.concat([data_odds1.loc[data_odds1['HomeTeam']==team_odds[odds_i]], \
                           data_odds1.loc[data_odds1['AwayTeam']==team_odds[odds_i]]],axis=0)
        data_team = data1.loc[data1['Season']==str(year+0.5)]
        len_sea1 = shape(data_team)[0]
        if len_sea1>0:
            data3=data_team.sort_values(by=['Date_Full'],ascending=[True])
        count1 = 0
        for ii in range(len_sea1):
            if data3.iat[ii,-6] != '' and float(data3.iat[ii,-6])>=2010.5\
                    and data3.iat[ii,4]>=0 and data3.iat[ii,5]>=0:
                # if team is the home team
                if data3.iat[ii,2]==team_odds[odds_i]:
                    #locate the match fixture from match dataset
                    euro_j = team_matcher(data3.iat[ii,3],data_team1)
                    euro_ma = euro_match.loc[(euro_match['home_team_api_id']== etf1.iat[euro_i,0]) & \
                                             (euro_match['away_team_api_id']== etf1.iat[euro_j,0]) & \
                                             (euro_match['season']==year_match)]
                    #some incorrect record is still there...
                    if len(euro_ma.iloc[:,0])==0:
                        print 'incorrect record:', data3.iat[ii,2], data3.iat[ii,3], data3['Season'].iloc[ii], \
                              data_team1[euro_i],data_team1[euro_j]
                        data_tmp[data3.iat[ii,-5],6,0], data_tmp[data3.iat[ii,-5],7,0] = np.nan, np.nan
                    else:
                        #locate FIFA player data
                        data_tmp[data3.iat[ii,-5],6,0], data_tmp[data3.iat[ii,-5],7,0] = player_finder(euro_ma,epf1,mode='home')
                    #save goal data
                    data_stk[i,1,count1] = data3.iat[ii,4]
                    data_stk[i,2,count1] = data3.iat[ii,5]
                    #save pts data
                    if data3.iat[ii,4]>data3.iat[ii,5]:
                        data_stk[i,0,count1] = 3
                    elif data3.iat[ii,4] == data3.iat[ii,5]:
                        data_stk[i,0,count1] = 1
                    else:
                        data_stk[i,0,count1] = 0
                    #time series
                    data_sta[i,:len(title8),0,count1] = (data3[title8]).iloc[ii,:]
                    data_sta[i,:len(title9),1,count1] = (data3[title9]).iloc[ii,:]
                # if team is the away team
                elif data3.iat[ii,3]==team_odds[odds_i]:
                    #locate the match fixture from match dataset
                    euro_j = team_matcher(data3.iat[ii,2],data_team1)
                    euro_ma = euro_match.loc[(euro_match['home_team_api_id']== etf1.iat[euro_j,0]) & \
                                             (euro_match['away_team_api_id']== etf1.iat[euro_i,0]) & \
                                             (euro_match['season']==year_match)]
                    #some incorrect record is still there...
                    if len(euro_ma.iloc[:,0])==0:
                        print 'incorrect record:', data3.iat[ii,2], data3.iat[ii,3], data3['Season'].iloc[ii], \
                              data_team1[euro_i],data_team1[euro_j]

                        data_tmp[data3.iat[ii,-5],6,0], data_tmp[data3.iat[ii,-5],7,0] = np.nan, np.nan
                    else:
                        #locate FIFA player data
                        data_tmp[data3.iat[ii,-5],6,1], data_tmp[data3.iat[ii,-5],7,1] = player_finder(euro_ma,epf1,mode='away')
                    #save goal data
                    data_stk[i,1,count1] = data3.iat[ii,5]
                    data_stk[i,2,count1] = data3.iat[ii,4]
                    #save pts data
                    if data3.iat[ii,4]>data3.iat[ii,5]:
                        data_stk[i,0,count1] = 0
                    elif data3.iat[ii,4] == data3.iat[ii,5]:
                        data_stk[i,0,count1] = 1
                    else:
                        data_stk[i,0,count1] = 3
                    #time series
                    data_sta[i,:len(title9),0,count1] = (((data3[title9]).iloc[ii,:]).fillna(0)).astype(float)
                    data_sta[i,:len(title8),1,count1] = (((data3[title8]).iloc[ii,:]).fillna(0)).astype(float)
                #time lagged data
                if count1 >= 5:
                    data_sta[i,:len(title8),2:,count1-5] = np.mean(np.ma.masked_invalid(data_sta[i,:,:2,count1-5:count1]),axis=2)
                count1 = count1+1
        #time lagged mean
        data_sta_mean = np.mean(np.ma.masked_invalid(data_sta[i,:,:2,:]),axis=2)
        if np.sum(data_sta[i,:,:2,:])==0 or np.sum(data_sta_mean)==0:
            print 'wrong team watch', data3.iloc[ii,:], team[i], team_odds[odds_i]
        #team rating
        gamma = RAT_gamma(data_sta[i,:,:2,:],data_sta_mean)
        for ii in range(5,len_sea1):
            if data3.iat[ii,-6] != '' and float(data3.iat[ii,-6])>=2000\
                    and data3.iat[ii,4]>=0 and data3.iat[ii,5]>=0:
                if data3.iat[ii,2]==team_odds[odds_i]:
                    data_tmp[data3.iat[ii,-5],0,0] = gamma[0,ii]*data_cli.iat[i,2]
                    data_tmp[data3.iat[ii,-5],1,0] = gamma[1,ii]*data_cli.iat[i,3]
                    data_tmp[data3.iat[ii,-5],2,0] = np.sum(data_stk[i,0,ii-5:ii])
                    data_tmp[data3.iat[ii,-5],3,0] = np.std(data_stk[i,0,ii-5:ii])
                    data_tmp[data3.iat[ii,-5],4,0] = np.sum(data_stk[i,1,ii-5:ii])
                    data_tmp[data3.iat[ii,-5],5,0] = np.sum(data_stk[i,2,ii-5:ii])
                    data_tmp[data3.iat[ii,-5],8,0] = data_cli.iat[i,1]
                    data_tmp[data3.iat[ii,-5],9,0] = data_cli.iat[i,4]
                    data_tmp[data3.iat[ii,-5],10,0] = data_cli.iat[i,5]
                    data_tmp[data3.iat[ii,-5],11,0] = data_cli.iat[i,7]
                    data_tmp[data3.iat[ii,-5],12,0] = data_cli.iat[i,8]
                elif data3.iat[ii,3]==team_odds[odds_i]:
                    data_tmp[data3.iat[ii,-5],0,1] = gamma[0,ii]*data_cli.iat[i,2]
                    data_tmp[data3.iat[ii,-5],1,1] = gamma[1,ii]*data_cli.iat[i,3]
                    data_tmp[data3.iat[ii,-5],2,1] = np.sum(data_stk[i,0,ii-5:ii])
                    data_tmp[data3.iat[ii,-5],3,1] = np.std(data_stk[i,0,ii-5:ii])
                    data_tmp[data3.iat[ii,-5],4,1] = np.sum(data_stk[i,1,ii-5:ii])
                    data_tmp[data3.iat[ii,-5],5,1] = np.sum(data_stk[i,2,ii-5:ii])
                    data_tmp[data3.iat[ii,-5],8,1] = data_cli.iat[i,1]
                    data_tmp[data3.iat[ii,-5],9,1] = data_cli.iat[i,4]
                    data_tmp[data3.iat[ii,-5],10,1] = data_cli.iat[i,6]
                    data_tmp[data3.iat[ii,-5],11,1] = data_cli.iat[i,7]
                    data_tmp[data3.iat[ii,-5],12,1] = data_cli.iat[i,8]
for i in range(13):
    data_odds[title5a[i]] = data_tmp[:,i,0]
for i in range(13):
    data_odds[title5b[i]] = data_tmp[:,i,1]
data_odds.drop(col_del,axis=1,inplace=True)
data_odds.to_pickle(path1+'f11_odds_history_v3.csv')
print 'done'


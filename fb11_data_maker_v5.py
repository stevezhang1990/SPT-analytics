from scipy import *
from pylab import *
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
from difflib import SequenceMatcher
import math
#data from 2009-2019
#for i in range(len(filename)):
#    data_raw = pd.read_csv(path1+filename[i]+'.csv',sep=',',header='infer')
#    len1,len2 = shape(data_raw)
#    header = list(data_raw.columns.values)
#    print header
# team matcher, try to find the same team name from another name lists
def team_matcher(string1,list2):
    match_mem = np.zeros(len(list2))
    ans = np.nan
    for i in range(len(list2)):
        match_mem[i] = SequenceMatcher(None,string1,list2.iloc[i]).ratio()
        if match_mem[i] >0.82:
            ans = i
            break
        elif string1 in list2.iloc[i]:
            match_mem[i] = match_mem[i]+1
        else:
            if string1[:3] == list2.iloc[i][:3]:
                match_mem[i] = match_mem[i]+0.2
            if string1[:-3] == list2.iloc[i][:-3]:
                match_mem[i] = match_mem[i]+0.2
    if math.isnan(ans)==True:
        ans = np.argmax(match_mem)
    return ans

###########Compute Gamestyle Index################################################
#Mode: Attack, Balance, Defend
#mid: 7000, Att/Def=0.8; mid: 5500, Att/Def=0.52
#passSuccess*possession: 0.41, 0.29
#Pace: Risky, Balance, Boring
#keypass/(passSucc*poss)+0.5*assist, 60&50
#Tactic: None, Pass, Counter, SetPiece
#Pass; keyPassShort/keyPassTotal: 79&73, pass*poss:0.41
#Counter; keyLong/Total: 0.25, pass*poss: 0.32, shotsPerGame: 13.2
#SetPiece: 15
def GSI(midh,oppoh,ownh,mida,oppa,owna,goalsetpiece,passlong,passshort,passtotal,\
        assist,psuccess,possession,shots,par=None):
    if not par:
        par = [7000,5000,0.8,0.52,0.41,0.29,60,50,79,0.41,0.25,0.32,
               13.2,15]
    if midh>7000 and oppoh/ownh>=0.8:
        modeh=0
    elif midh<5500 and oppoh/ownh<=0.52:
        modeh=1
    else:
        modeh=0.5
    if mida>7000 and oppa/owna>=0.8:
        modea=0
    elif mida<5500 and oppa/owna<=0.52:
        modea=1
    else:
        modea=0.5
    pos = psuccess*possession*100
    if pos+0.5*assist>=60:
        pace=0
    elif pos+0.5*assist<50:
        pace=1
    else:
        pace=0.5
    tact=0
    if passshort/passtotal>=0.79 and pos>=0.41:
        tact=tact+1
    #print passlong/passtotal, pos, shots
    if passlong/passtotal>=0.25 and pos<=35 and shots>13.5:
        tact=tact+0.5
    if goalsetpiece>=15:
        tact=tact+0.25
    return modeh,modea,pace,tact

#################################################################################
#path of files
path1 = '/users/jk/11/xzhang/DAT112/torneo_data/'
#number of data
filename = ['f11_team_action','f11_team_details','team_rankings','f11_goals']
#choose seasons
sea_header = ['season','season','season','Season']
sea_tick = ['2010_2011','2010_2011','2010-11','2010-2011']
#choose league
lea_header = ['league','league','tournamentName','League']
lea_tick1 = ['EPL','LaLiga','Bundesliga','SerieA','Ligue1']
lea_tick2 = ['Premier League','La Liga','Bundesliga','Serie A','Ligue 1']
#list of all teams
tea_header = ['team_name','teamName','teamName','Team_Overall']
tea_header2 = ['team_name','teamName','teamName','Club_Home']
        
#game attribute
header0 = [tea_header[0],'middle_third','opposition_third','own_third','home_away']
header1 = [tea_header[1],'tackleWonTotal','interceptionAll','foulCommitted',\
           'foulGiven','saveTotal','goalSetPiece',\
           'turnover','keyPassLong','keyPassShort','keyPassesTotal','assist']
header3 = [tea_header[3],'GF','GA','Pts_Overall']
header3b = [tea_header2[3],'Pts_Home']
header2 = [tea_header[2],'aerialWonPerGame','passSuccess','possession','rating','shotsPerGame','yellowCard']

#data loader
df_act_raw = pd.read_csv(path1+filename[0]+'.csv',sep=',',header='infer')
df_team_raw = pd.read_csv(path1+filename[1]+'.csv',sep=',',header='infer')
df_rank_raw = pd.read_csv(path1+filename[2]+'.csv',sep=',',header='infer')
df_goals_raw = pd.read_csv(path1+filename[3]+'.csv',sep=',',header='infer')
title_cli = ['team','team_rating','off_rating','def_rating','h-a parity','mode_home','mode_away','pace',\
             'tactics','season','league']
#6 seasons, 5 leagues, 20 teams (max), 7 attributes
len_tot = 20*4+18
df_cli = pd.DataFrame(index=np.arange(6*len_tot),columns=title_cli)
count1 = 0
for sea_i in range(6):
    #season ticks
    sea_tick1 = str(2010+sea_i)+'_'+str(2010+sea_i+1)
    sea_tick2 = str(2010+sea_i)+'-'+str(10+sea_i+1)    
    for lea_i in range(len(lea_tick1)):
        #home team action stats
        df_act1 = df_act_raw.loc[(df_act_raw[sea_header[0]]==sea_tick1) & \
                                 (df_act_raw[lea_header[0]]==lea_tick1[lea_i]) & \
                                 (df_act_raw[header0[4]]=='home')]
        df_act_home = df_act1.sort_values(by=[tea_header[0]])[header0]
        len_ahome1,len_ahome2 = shape(df_act_home)
        # away team action stats
        df_act2 = df_act_raw.loc[(df_act_raw[sea_header[0]]==sea_tick1) & \
                                 (df_act_raw[lea_header[0]]==lea_tick1[lea_i]) & \
                                 (df_act_raw[header0[4]]=='away')]
        df_act_away = df_act2.sort_values(by=[tea_header[0]])[header0]
        len_aaway1,len_aaway2 = shape(df_act_away)
        # team advanced stats
        df_team1 = df_team_raw.loc[(df_team_raw[sea_header[1]]==sea_tick1) & \
                                   (df_team_raw[lea_header[1]]==lea_tick1[lea_i])]
        df_team = df_team1.sort_values(by=[tea_header[1]])[header1]
        len_team1,len_team2 = shape(df_team)
        # team season ratings
        df_rank1 = df_rank_raw.loc[(df_rank_raw[sea_header[2]]==sea_tick2) & \
                                   (df_rank_raw[lea_header[2]]==lea_tick2[lea_i])]
        df_rank = df_rank1.sort_values(by=[tea_header[2]])[header2]
        len_rank1,len_rank2 = shape(df_rank)
        # team end of season standings
        df_goals1 = df_goals_raw.loc[(df_goals_raw[sea_header[3]]==sea_tick1) & \
                                         (df_goals_raw[lea_header[3]]==lea_tick1[lea_i])]
        df_goals_ova = df_goals1.sort_values(by=[tea_header[3]])[header3]
        len_goals_ova1,len_goals_ova2 = shape(df_goals_ova)
        df_goals_home = df_goals1.sort_values(by=[tea_header2[3]])[header3b]
        len_goals_home1,len_goals_home2 = shape(df_goals_home)
        team_list = df_rank[tea_header[2]]
        team_rating = df_rank['rating']
        for i in range(len(team_list)):
            df_cli[title_cli[9]].iloc[count1] = sea_tick2
            df_cli[title_cli[10]].iloc[count1] = lea_tick1[lea_i]
            df_cli[title_cli[0]].iloc[count1] = team_list.iloc[i]
            df_cli[title_cli[1]].iloc[count1] = team_rating.iloc[i]
            ova_i = team_matcher(team_list.iloc[i],df_goals_ova[tea_header[3]])
            ghome_i = team_matcher(team_list.iloc[i],df_goals_home[tea_header2[3]].str.replace(r"\(.*\)",""))
            act1_i = team_matcher(team_list.iloc[i],df_act_home[tea_header[0]])
            act2_i = team_matcher(team_list.iloc[i],df_act_away[tea_header2[0]])
            team_i = team_matcher(team_list.iloc[i],df_team[tea_header[1]])
            df_cli[title_cli[2]].iloc[count1] = df_goals_ova.iloc[ova_i,1]
            df_cli[title_cli[3]].iloc[count1] = df_goals_ova.iloc[ova_i,2]
            df_cli[title_cli[4]].iloc[count1] = df_goals_home.iloc[ghome_i,1].astype(float)/ \
                                               (df_goals_ova.iloc[ova_i,3]-df_goals_home.iloc[ghome_i,1]).astype(float)
            df_cli[title_cli[5]].iloc[count1], df_cli[title_cli[6]].iloc[count1],\
            df_cli[title_cli[7]].iloc[count1], df_cli[title_cli[8]].iloc[count1] = \
                             GSI(df_act_home.iloc[act1_i,1],df_act_home.iloc[act1_i,2],df_act_home.iloc[act1_i,3],\
                                 df_act_away.iloc[act2_i,1],df_act_away.iloc[act2_i,2],df_act_away.iloc[act2_i,3],\
                                 df_team.iloc[team_i,6],df_team.iloc[team_i,8],df_team.iloc[team_i,9],\
                                 df_team.iloc[team_i,10],df_team.iloc[team_i,11],df_rank.iloc[i,2],\
                                 df_rank.iloc[i,3],df_rank.iloc[i,5])
            count1 = count1+1
#risk_rate = df_rank[header2[5]]/(df_rank[header2[2]]*df_rank[header2[3]])
#risk_rate2 = df_team[header1[10]]/df_team[header1[7]]
#df_odds_raw = pd.read_csv(path1+filename[4]+'.csv',sep=',',header='infer')
#df_odds1 = df_odds_raw.loc[(df_odds_raw[sea_header[4]]==sea_tick[4]) & \
#                        (df_odds_raw[lea_header[4]]==lea_tick[4])]
#team overall rating, player overall rating, player variability, offensive rating, defensive rating, 
#streak(4), home/away parity, last 6 games variability, game odds, asian handicap odds/size, 
#game style index, goal last 6 games, goal against last 6 games.  
##season average data
##TOR,OFR,DER,HAP,GSI

df_cli.to_pickle(path1+'f11_season_stats.csv')
print 'done'
    
                        
    

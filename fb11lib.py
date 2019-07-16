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
def team_matcher(string2,list3):
    if isinstance(list3, list):
        list2 = list3
    else:
        list2 = list3.tolist()
    match_mem = np.zeros(len(list2))
    ans = np.nan
    out = ['La Coruna','Hercules','Sp Gijon','Real','FC','Rennes','QPR','Verona','Ajaccio GFCO','GFC Ajaccio']
    if out[8] in list2 and (string2==out[8] or string2==out[9]):
        ans = list2.index(out[8])
    elif out[9] in list2 and (string2==out[8] or string2==out[9]):
        ans = list2.index(out[9])
    elif string2 == out[0]:
        string1='RC Deportivo de La Coru?a'
    elif string2 == out[1]:
        string1='H?rcules Club de F?tbol'
    elif string2 == out[2]:
        string1='Real Sporting de Gijn'
    elif out[3] in string2 and string2!='Real Madrid' and string2!=out[8] and string2!=out[9]:
        string1=string2.replace(out[3],'')
    elif out[4] in string2:
        string1=string2.replace(out[4],'')
    elif string2 == out[5]:
        string1='Rennais'
    elif string2 == out[6]:
        string1='Queens Park Rangers'
    elif out[6] in list2 and string2=='Queens Park Rangers':
        ans = list2.index(out[6])
    elif string2 == out[7]:
        string1 ='Hellas Verona'
    else:
        string1=string2
    if math.isnan(ans) ==True:
        for i in range(len(list2)):
            match_mem[i] = SequenceMatcher(None,string1,list2[i]).ratio()
            if match_mem[i] >0.82:
                ans = i
                break
            elif string1 in list2[i]:
                match_mem[i] = match_mem[i]+1
            else:
                if string1[:3] == list2[i][:3]:
                    match_mem[i] = match_mem[i]+0.2
                if string1[:-3] == list2[i][:-3]:
                    match_mem[i] = match_mem[i]+0.2
        if math.isnan(ans)==True:
            ans = np.argmax(match_mem)
    return ans
#team overall rating, player overall rating, player variability, offensive rating, defensive rating,
#streak(4), home/away parity, last 6 games variability, game odds, asian handicap odds/size,
#game style index, goal last 6 games, goal against last 6 games.
##season average data
def RAT_gamma(data_ts,data_mean,para=None):
    if not para:
        para = [0.25,0.4,0.02,0.1,0.15,0.3]
    len_var,len_od,len_sea = shape(data_ts)
    gamma = np.zeros((len_od,len_sea))
    for i in range(len_od):
        data_norm = np.sum(data_mean[:,i]*para)
        #print data_norm
        for j in range(len_sea):
            #print np.sum(data_ts[:,i,j]*para)
            gamma[i,j] = np.sum(data_ts[:,i,j]*para)/data_norm
    return gamma

def player_finder(match,epf1,mode):
    if mode=='home':
        player = ['home_player_1', 'home_player_2', 'home_player_3', "home_player_4", "home_player_5",
                  "home_player_6", "home_player_7", "home_player_8", "home_player_9", "home_player_10",
                  "home_player_11"]
    elif mode=='away':
        player = ["away_player_1", "away_player_2", "away_player_3", "away_player_4", "away_player_5",
                  "away_player_6", "away_player_7", "away_player_8", "away_player_9", "away_player_10",
                  "away_player_11"]
    player_id = match[player]
    player_stats = np.zeros(len(player))
    for i in range(len(player)):
        epf_pl = epf1.loc[epf1['player_api_id']==player_id.iat[0,i]]
        #print len(epf_pl.iloc[:,0])
        if len(epf_pl.iloc[:,0])==0:
            player_stats[i] = 68
        else:
            player_stats[i] = ((epf_pl)['overall_rating']).iloc[0]
    return np.sum(player_stats), np.std(player_stats)

def league_finder(league,mode=None):
    title2 = ['EPL','LaLiga','Bundesliga','SerieA','Ligue1']
    title2b = ['E0','SP1','D1','I1','F1']
    ans = np.nan
    if not mode:
        ans = title2b[title2.index(league)]
    elif mode=='ind':
        ans = title2b.index(league)
    return ans

def get_last_matches(matches, date, team, x = 10):
    ''' Get the last x matches of a given team. '''

    #Filter team matches from matches
    team_matches = matches[(matches['home_team_api_id'] == team) | (matches['away_team_api_id'] == team)]

    #Filter x last matches from team matches
    last_matches = team_matches[team_matches.date < date].sort_values(by = 'date', ascending = False).iloc[0:x,:]

    #Return last matches
    return last_matches

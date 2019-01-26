#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
touch_tunes_test.py
Created on Sat Jan 26 12:18:19 2019

@author: johnkim
"""

import requests 
from pandas.io.json import json_normalize
import pandas

# Constants, DO NOT REMOVE!!!
URL = "https://conuhacks-playback-api.touchtunes.com/"
CLIENT_SECRET = {"client-secret":"9923ac9b-8fd3-421f-b0e5-952f807c6885"}

def get_song(URL,song_id):
    '''
    get_song 
    e.g. https://conuhacks-playback-api.touchtunes.com/song/11088314 
    corresponds to get_song(URL,11088314)
    '''
    song_json = requests.get(URL+"song/"+str(song_id), headers=CLIENT_SECRET).json()
    return(json_normalize(song_json))

def get_artist(URL,artist_id): 
    ''' 
    get_artist 
    e.g. https://conuhacks-playback-api.touchtunes.com/artist/1182 
    corresponds to the function call get_artist(URL,1182) 
    '''
    artist_json = requests.get(URL+"artist/"+str(artist_id), headers=CLIENT_SECRET).json()
    return(json_normalize(artist_json))

 
def get_plays(URL,start_date,start_time,end_date,end_time,offset): 
    '''
    Gets active plays 
    e.g. query https://conuhacks-playback-api.touchtunes.com/plays?startDate=2018-02-19T21:00:00Z&endDate=2018-02-19T22:00:00Z&offset=0
    corresponds to function call get_plays(URL,"2018-02-19","21:00:00","2018-02-19","22:00:00",0)
    '''
    plays_json = requests.get(URL+"plays?startDate=%sT%sZ&endDate=%sT%sZ&offset=%s" % 
                         (start_date,start_time,end_date,end_time,str(offset)),headers=CLIENT_SECRET).json()
    return (json_normalize(plays_json,"plays"))

song = get_song(URL,11088314)
artists = get_artist(URL,1182)
plays = get_plays(URL,"2018-02-19","21:00:00","2018-02-19","22:00:00",0) 

plays["artistName"] = plays["artistId"].apply(lambda ident: get_artist(URL,ident)["artistName"])
plays["songName"] = plays["songId"].apply(lambda ident: get_song(URL,ident)["songTitle"])
    
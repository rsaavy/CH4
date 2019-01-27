# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TouchTunes.py
Created on Sat Jan 26 12:18:19 2019

@author: johnkim
"""

import requests 
from pandas.io.json import json_normalize
import pandas as pd
import os

class TouchTunes: 
    
    def __init__(self,start_date,start_time,end_date,end_time,offset): 
        self.URL = "https://conuhacks-playback-api.touchtunes.com/"
        self.CLIENT_SECRET = {"client-secret":"9923ac9b-8fd3-421f-b0e5-952f807c6885"}
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
        self.offset = offset
        self.plays = pd.DataFrame()

    def __get_song(self,song_id):
        '''
        get_song 
        e.g. https://conuhacks-playback-api.touchtunes.com/song/11088314 
        corresponds to get_song(URL,11088314)
        '''
        song_json = requests.get(self.URL+"song/"+str(song_id), headers=self.CLIENT_SECRET).json()
        return(json_normalize(song_json))

    def __get_artist(self,artist_id): 
        ''' 
        get_artist 
        e.g. https://conuhacks-playback-api.touchtunes.com/artist/1182 
        corresponds to the function call get_artist(URL,1182) 
        '''
        artist_json = requests.get(self.URL+"artist/"+str(artist_id), headers=self.CLIENT_SECRET).json()
        return(json_normalize(artist_json))

 
    def __get_plays(self):
        '''
        Gets active plays 
        e.g. query https://conuhacks-playback-api.touchtunes.com/plays?startDate=2018-02-19T21:00:00Z&endDate=2018-02-19T22:00:00Z&offset=0
        corresponds to function call get_plays(URL,"2018-02-19","21:00:00","2018-02-19","22:00:00",0)
        '''
        plays_json = requests.get(self.URL+"plays?startDate=%sT%sZ&endDate=%sT%sZ&offset=%s" % 
                             (self.start_date,self.start_time,self.end_date,self.end_time,str(self.offset)),headers=self.CLIENT_SECRET).json()
        return(json_normalize(plays_json,"plays",errors="ignore"))
    
    def consolidate(self): 
        self.plays = self.__get_plays()
        self.plays["artistName"] = self.plays["artistId"].apply(lambda ident: self.__get_artist(ident)["artistName"])
        self.plays["songName"] = self.plays["songId"].apply(lambda ident: self.__get_song(ident)["songTitle"])
        return(self.plays.drop(["artistId","songId"],axis=1))
        
        
# Example implementation
tt = TouchTunes("2018-02-19","21:00:00","2018-02-19","22:00:00",0)
touch_tunes_df = tt.consolidate()
touch_tunes_df.to_csv("../data/export.csv",index=False)


# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 12:51:08 2019

@author: Roy Angelo Saavedra
"""
# Load the Library
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
from bs4 import BeautifulSoup
import sys

# Load the Token 
TOKEN = 'BQSJArOfSf1kRZHU5zgIzHPmZXzoXwVx_n_PZApKbN7gP1CyBlMhA1YXZQxjtLXZ'

# Build a wrapper for song info, that requires new song_title and artist name
def request_song_info(song_title, artist_name):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + str(TOKEN)}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, params=data, headers=headers)

    return response

# Search for matches in the request response and query results.
def create_data(song,name):
    json = request_song_info(song,name).json()
    data = pd.DataFrame()
    # Generate a data frame that contains the results
    for hit in json['response']['hits']:
        data = data.append(hit['result'],ignore_index=True)
    
def scrap_song_url(url):
    print(url)
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    return lyrics

def generate_df(song,name):
    # Generate a data frame that contains the information from
    temp = pd.DataFrame()
    stat = pd.DataFrame()
    for index,url in enumerate(data['url']):
        lyrics = scrap_song_url(data.iat[index,15])
        lyrics = lyrics.rstrip('\n')
        lyrics = lyrics.lstrip()
        lyrics = lyrics.rstrip()
        data.iat[index,16]= lyrics
        temp = temp.append(json_normalize(data['primary_artist'][index]),ignore_index=True)
        stat = stat.append(json_normalize(data['stats'][index]),ignore_index=True)

    # Concat the pandas data frames together.     
    frames = [data,stat,temp]
    results = pd.concat(frames,axis=1)
    results.to_csv("../data"+str(song)+ "-"+str(name)+".csv")
    return results 


if __name__ == "__main__":
    song = sys.argv[0]
    name = sys.argv[1]
    data = create_data(song,name)
    data_frame = generate_df(song,name)
#def search_song():
#    import lyricsgenius as g
    
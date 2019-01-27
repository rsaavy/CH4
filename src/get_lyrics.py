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

# Load the Token 
TOKEN = 'fJ4NznrGcAKh-LRqz6mPmmfDIOlXuhV1HdU2FWUVfp6NDxzmqrv_9YRmDu7JlOzw'

# Build a wrapper for song info
def request_song_info(song_title, artist_name):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + str(TOKEN)}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, params=data, headers=headers)

    return response

# Search for matches in the request response
response = request_song_info("Shelter", "Porter Robinson")
json = response.json()

data = pd.DataFrame()
for hit in json['response']['hits']:
    data = data.append(hit['result'],ignore_index=True)
    
from bs4 import BeautifulSoup
def scrap_song_url(url):
    print(url)
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    return lyrics
# I need to remove and add lyrics into the original data frame
for ix,url in enumerate(data['url']):
    lyric = scrap_song_url(url)
    lyrics = lyric.rstrip('\n')
    print(lyrics)
    data['lyrics'] = data['lyrics'].

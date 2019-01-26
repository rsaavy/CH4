# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 14:30:07 2019

@author: Roy Angelo Saavedra
"""

import requests

base_url = "http://api.genius.com"
headers = {'Authorization': 'Bearer TOKEN'}
search_url = base_url + "/search"
song_title = "Capsized"
artist_name = "Andrew Bird"
data = {'q': song_title}
response = requests.get(search_url, data=data, headers=headers)
json = response.json()
song_info = None
for hit in json["response"]["hits"]:
  if hit["result"]["primary_artist"]["name"] == artist_name:
    song_info = hit
    break
if song_info:
  pass
  #now we have the song info and can do what we want

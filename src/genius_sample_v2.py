# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 14:30:56 2019

@author: Roy Angelo Saavedra
"""

import requests
from bs4 import BeautifulSoup

base_url = "http://api.genius.com"
headers = {'Authorization': 'Bearer TOKEN'}

song_title = "Lake Song"
artist_name = "The Decemberists"

def lyrics_from_song_api_path(song_api_path):
  song_url = base_url + song_api_path
  response = requests.get(song_url, headers=headers)
  json = response.json()
  path = json["response"]["song"]["path"]
  #gotta go regular html scraping... come on Genius
  page_url = "http://genius.com" + path
  page = requests.get(page_url)
  html = BeautifulSoup(page.text, "html.parser")
  #remove script tags that they put in the middle of the lyrics
  [h.extract() for h in html('script')]
  #at least Genius is nice and has a tag called 'lyrics'!
  lyrics = html.find(“div”, class_=”lyrics”).get_text() #updated css where the lyrics are based in HTML
  return lyrics

if __name__ == "__main__":
  search_url = base_url + "/search"
  data = {'q': song_title}  
  response = requests.get(search_url, data=data, headers=headers)
  json = response.json()
  song_info = None
  for hit in json["response"]["hits"]:
    if hit["result"]["primary_artist"]["name"] == artist_name:
      song_info = hit
      break
  if song_info:
    song_api_path = song_info["result"]["api_path"]
    print lyrics_from_song_api_path(song_api_path)

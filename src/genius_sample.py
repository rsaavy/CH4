# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 12:51:08 2019

@author: Roy Angelo Saavedra
"""

import requests

#TOKEN below should be the string that the API docs tells you
base_url = "http://api.genius.com"
#Key line below here when, this is how to authorize your request when
#using the API
headers = {'Authorization': 'Bearer ZTnknUBCXpr6gLGeb3J-SM0Ad97whU96m8rx9Vk5tApRfsN580k-I-6OXfnyi5Oh'}
search_url = base_url + "/search"
song_title = "Creep"
params = {'q': song_title}
response = requests.get(search_url, params=params, headers=headers)




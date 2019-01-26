# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 12:51:08 2019

@author: Roy Angelo Saavedra
"""

import requests
import json
from pandas.io.json import json_normalize
#TOKEN below should be the string that the API docs tells you
base_url = "http://api.genius.com"
#Key line below here when, this is how to authorize your request when
#using the API
TOKEN = 'M7se5sKqlk6P3bzifcb_CZY8NoTrslh1qb8C11GWpuWfqnX8Eh5yP1xz-7MSexE_'
headers = {'Authorization': 'Bearer'+' '+ TOKEN}
search_url = base_url + "/search"
song_title = "creep"
params = {'q': song_title}
response = requests.get(search_url, params=params, headers=headers)
json = json_normalize(response.json())





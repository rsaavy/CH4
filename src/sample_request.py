# -*- coding: utf-8 -*-
"""
Spyder Editor

@Roy Angelo Saavedra
"""


import requests 
import json

url = "https://conuhacks-playback-api.touchtunes.com/song/11088314"
headers = {"client-secret":"9923ac9b-8fd3-421f-b0e5-952f807c6885"}


call_api = requests.get(url, headers=headers)
print(call_api.text)


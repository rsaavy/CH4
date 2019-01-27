# Client ID phq.aFf5H8cwziREtuOcS8Qy6NQ3hPjlCuHBtTFW6tNe
# Clience Secret fe7qxmZBPQVxV4dmec7ksecmfx4c7CUaGWhiYlGh
# Access Token nyBfPgKu009XmCNYIPBUqHUJANUy09
import TouchTunes
import requests
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np

URL = "https://conuhacks-playback-api.touchtunes.com/"

c = TouchTunes.TouchTunes("2018-02-19","21:00:00","2018-02-19","22:00:00",0)
x = c.consolidate().drop_duplicates().reset_index()

print(x)

late = x["latitude"][0]

print(late)

results = pd.DataFrame()

for i in range(len(x)):
    lat = x["latitude"][i]
    long = x["longitude"][i]
    
    response = requests.get(
        url="https://api.predicthq.com/v1/events/",
        headers={"Authorization": "Bearer nyBfPgKu009XmCNYIPBUqHUJANUy09"},
        params={"category": "concerts", "within": "100km@%s,%s" % (lat, long)}
    )
    data = response.json()["results"]
    stuff = json_normalize(data)
    
    temp_key = np.array([i]*len(stuff))
    
    stuff["key"] = temp_key
    
    print(temp_key)
    
    results = results.append(stuff, ignore_index=True)
    
    
'''response = requests.get(
        url="https://api.predicthq.com/v1/events/",
        headers={"Authorization": "Bearer nyBfPgKu009XmCNYIPBUqHUJANUy09"},
        params={"q": "rock", "country": "US", "category": "concerts", "within": "100km@37.271873,-119.270420"}
    )'''

#data = response.json()["results"]

x = x.merge(results, left_index = True, right_on = "key")

#stuff = json_normalize(data)


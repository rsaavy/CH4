# Client ID phq.aFf5H8cwziREtuOcS8Qy6NQ3hPjlCuHBtTFW6tNe
# Clience Secret fe7qxmZBPQVxV4dmec7ksecmfx4c7CUaGWhiYlGh
# Access Token nyBfPgKu009XmCNYIPBUqHUJANUy09
import TouchTunes
import requests
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np

def mergeEvent(df):
    results = pd.DataFrame()

    for i in range(len(df)):
        lat = df["latitude"][i]
        long = df["longitude"][i]

        response = requests.get(
            url="https://api.predicthq.com/v1/events/",
            headers={"Authorization": "Bearer nyBfPgKu009XmCNYIPBUqHUJANUy09"},
            params={"category": "concerts", "within": "100km@%s,%s" % (lat, long)}
        )
        data = response.json()["results"]
        stuff = json_normalize(data)

        temp_key = np.array([i]*len(stuff))

        stuff["key"] = temp_key

        results = results.append(stuff, ignore_index=True)

    df = df.merge(results, left_index = True, right_on = "key")
    df = df.drop(["index", "state_x", "category", "country", "duration", "end", "first_seen", "labels", "rank", "relevance", "scope", "state_y", "timezone", "updated", "key"], axis = 1)
    return df

'''c = TouchTunes.TouchTunes("2018-02-19","21:00:00","2018-02-19","22:00:00",0)
x = c.consolidate().drop_duplicates().reset_index()

nuX = mergeEvent(x)'''

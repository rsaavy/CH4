# Client ID phq.aFf5H8cwziREtuOcS8Qy6NQ3hPjlCuHBtTFW6tNe
# Clience Secret fe7qxmZBPQVxV4dmec7ksecmfx4c7CUaGWhiYlGh
# Access Token nyBfPgKu009XmCNYIPBUqHUJANUy09
from JK_Files import TouchTunes
import requests

URL = "https://conuhacks-playback-api.touchtunes.com/"

plays = TouchTunes.get_plays(URL,"2018-03-19","21:00:00","2018-03-19","22:00:00",0)

print(plays["longitude"])

response = requests.get(
    url="https://api.predicthq.com/v1/events/",
    headers={"Authorization": "Bearer nyBfPgKu009XmCNYIPBUqHUJANUy09"},
    params={"q": "rock", "country": "US", "category": "concerts"}
)

data = response.json()

count = len(data["results"])

for i in range(0, count):
    print(data["results"][i])

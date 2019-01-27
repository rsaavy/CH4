import lyricsgenius as g
import pandas as pd
# Connect to lyrics genius
connect = g.Genius("vAQ-cvKgRans4CqKYz6oUJy4LZ1N8eVHRQ73_rSjF9-FoVxTUVqObcIhcbehsuL5")

# Get all Songs
def getAllSongs(artist,m):
    s= connect.search_artist(artist,max_songs=m)
    allsongs = s.songs
    l=[]
    t=[]
    a=[]
    for song in allsongs:
        l = l.append(song)
        t = t.append(song.title)
        a = a.append(artist)
    data = pd.DataFrame()
    frames = [l,t,a]
    data = pd.concat(frames,axis=1)
    data.to_csv('../data/'+str(artist)+".csv")

    return data


data = getAllSongs("Drake",5)

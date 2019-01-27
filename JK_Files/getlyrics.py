import lyricsgenius as g
from TouchTunes import TouchTunes
import os 
os.getcwd()

# Connect API to lyrics genius 
api = g.Genius("vAQ-cvKgRans4CqKYz6oUJy4LZ1N8eVHRQ73_rSjF9-FoVxTUVqObcIhcbehsuL5")
# Load Touch Tunes API
tt = TouchTunes("2018-02-19","21:00:00","2018-02-19","22:00:00",0)
tdf = tt.consolidate()

names_df = tdf.groupby(by=['artistName','songName'], as_index=False).first()
#ldf = list(names_df['artistName'])
#
#artist = api.search_artist(ldf[0])
#artist.save_lyrics()
#artist = api.search_artist(ldf[1])
#artist.save_lyrics()
#artist = api.search_artist(ldf[2])
#artist.save_lyrics()
#artist = api.search_artist(ldf[3])
#artist.save_lyrics()
#

from nltk.tokenize import word_tokenize  # to split sentences into words
from nltk.corpus import stopwords  # to get a list of stopwords
from collections import Counter  

with open('./JK_Files/Lyrics_Queen.json', 'r') as f:
    queen = json.load(f)




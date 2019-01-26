# This is source code I found from an example that uses 
#
#
#client_id = 'Your Genius Client ID'
#client_secret = 'Your Genius Client Secret'
#client_access_token = 'Your Genius Access Token'

client_secret = 'QFNFCGpypcgHmZdsR028NANEPBd5QYFqAB5jz5W2yMoESGz08wpHtNtLR3lPAv9Hhzj91R5q4jF2XLLMiF1Rkw'
client_access_token = 'FKtRnUIwZYbGiVjrV2s7xIEqGqkVI5sZp5GkJyL4g_Q8T9vFCugO57cnKtVKusFm'
client_id = 'H0CWEIbUaM1VzbMDG3XyXYR-eH1IfQ0JRHeYAAuM35th2-Z-UQP0p6jpB4OIG7DS'


#import plot_albums
import string
import requests
import nltk
from sys import argv
from bs4 import BeautifulSoup
from nltk.util import ngrams
from collections import Counter

class ArtistQuery:
    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': 'Bearer ' + str(token)}
        self.base_url = "http://api.genius.com"

    def __get_artist_id__(self, artist_name, song_name=""):
        data = {'q': artist_name + ' ' + song_name}
        response = requests.get(self.base_url + "/search", params=data, headers=self.headers).json()
        print("found artist " + response['response']['hits'][0]['result']['primary_artist']['name'])
        return response['response']['hits'][0]['result']['primary_artist']['id']

    def get_songs_by_artist(self, artist_name, song=""):
        songs = []
        page = 1
        id = self.__get_artist_id__(artist_name, song)
        last_page = False
        while not last_page:
            data = {'per_page': '50', 'page': str(page)}
            response = requests.get(self.base_url + "/artists/" + str(id) + '/songs', params=data,
                                    headers=self.headers).json()
            for song in response['response']['songs']:
                songs.append(str(song['api_path']))
            if response['response']['next_page']:
                page = response['response']['next_page']
            else:
                last_page = True
        return songs

    def build_albums(self, songs):
        albums = {}
        for song in songs:
            response = requests.get(self.base_url + song, headers=self.headers).json()
            if response['response']['song']['album']:
                albums.setdefault(response['response']['song']['album']['name'], []).append(
                    response["response"]["song"]["path"])
        return albums

    def build_album_corpus(self, album):
        album_lyrics = ""
        for song in album:
            page = requests.get("http://genius.com" + song)
            html = BeautifulSoup(page.text, "html.parser")
            [h.extract() for h in html('script')]
            lyrics = html.find("div", class_="lyrics").get_text()  # updated css where the lyrics are based in HTML
            lyrics = lyrics.replace('\n', ' ')
            lyrics = lyrics.replace('\'', '')
            for c in string.punctuation:
                lyrics = lyrics.replace(c, "")
            album_lyrics += lyrics.lower()
        return album_lyrics

    def get_album_csv(self, artist_name, filename=None):
        songs = artist.get_songs_by_artist(artist_name)
        albums = artist.build_albums(songs)

        if (filename):
            file = open(filename, "w")
            file.write("album, word count, ngrams: 2,3,4")

        albums_list = []
        for album in albums:
            if len(albums[album]) < 3:
                continue
            lyrics = artist.build_album_corpus(albums[album])
            token = nltk.word_tokenize(lyrics)
            album_name = album.replace(",",'')
            if len(album_name) > 18:
                album_name = album_name[:15] + '...'
            csv_line = album_name + ','
            csv_line += str(len(token)) + ','
            try:
                for i in range(2, 5):
                    count = 0
                    counter = Counter(ngrams(token, i))
                    for key in counter:
                        count += counter[key] - 1
                    csv_line += str(count) + ','
                print(csv_line)
                albums_list.append(csv_line.split(","))
                if (filename):
                    file.write(csv_line + '\n')
            except:
                pass
        return albums_list

if __name__ == '__main__':
    artist_name = "Drake"
    artist = ArtistQuery(client_access_token)
    albums_list = artist.get_album_csv(artist_name, artist_name + '.csv')
    import pandas as pd
    pd.to_csv('/albums_list.csv')
    #plot_albums.plot_album_ngrams(albums_list, artist_name)
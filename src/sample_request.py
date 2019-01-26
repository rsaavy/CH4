# -*- coding: utf-8 -*-
"""
Spyder Editor

@Roy Angelo Saavedra
"""

class ArtistQuery:
    def __init__(self,token):
        self.token = token
        self.headers = {'Authorization': 'Bearer ' + str(token)}
        self.base_url = "http://api.genius.com"
    
    def _get_artist_id__(self,artist):

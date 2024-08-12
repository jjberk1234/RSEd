import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import random


client_id = '6cf04184f40e42d2ade91d83547bc924'
client_secret = '9f5f7d1254384f598347391d5d374f97'

class Spotify:
    def __init__(self, client_id, client_secret):

        os.environ['SPOTIPY_CLIENT_ID'] = client_id
        os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret

        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

        # spotipy track object
        self.tracks = {}
        # spotipy album object
        self.albums = {}

    def validate_playlist_url(self, url):
        '''
        Return true if the url links to a valid Spotify playlsit
        '''
        regex = re.compile(r'https?://open\.spotify\.com/playlist/[a-zA-Z0-9]+(\?si=[a-zA-Z0-9_-]+)?')
        if regex.match(url):
            return True
        else:
            return False
    
    def get_playlist_uri(self, playlist_url):
        if self.validate_playlist_url(playlist_url):
            playlist_uri = playlist_url.split('/')[-1].split('?')[0]
            return playlist_uri
        else:
            return None
    
    def get_tracks_from_playlist(self, playlist_url):
        '''
        Makes API call to get all tracks from a url
        Adds tracks to the self.tracks dict
        '''
        playlist_uri = self.get_playlist_uri(playlist_url)
        self.tracks.update(self.sp.playlist_tracks(playlist_uri)['items']) # FIXME API call
        return self.tracks
    
    def get_albums_from_playlist(self, playlist_url):
        '''
        Gets all albums from a playlist
        Adds albums to self.albums dict
        '''
        # Can we get all the albums in one call? FIXME
        self.get_tracks_from_playlist(playlist_url)
        for track in self.tracks:
            self.get_albums_from_track(track) # FIXME API call
        
        return self.albums
    
    def get_albums_from_track(self, track):
        '''
        Gets matching album for a given track
        Adds album to self.albums dict
        '''
        self.albums.update(self.sp.album(track['album']['id'])) # FIXME API call
        return self.albums
        
    
    def get_random_albums(self, num_albums=10):
        '''
        Get random albums
        Update self.albums with new albums
        '''
        search_term = 'tag:new'
        results = self.sp.search(q=search_term, type='album', limit=num_albums*10) # FIXME API call
        albums = results['albums']['items']

        if len(albums) < num_albums:
            num_albums = albums

        random_albums = random.sample(albums, num_albums)

        for album in random_albums:
            self.albums.update(self.sp.album(album['id'])) # FIXME API call

        return self.albums

    
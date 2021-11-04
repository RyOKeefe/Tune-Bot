import requests
import json
import base64
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from secret_key import client_ID, client_secret

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_ID, client_secret))


# returns a dict list of up to size {limit} containing the search results
def get_album(album_name, limit=1):
    album_name = bytes(album_name, "utf-8").decode("unicode_escape")
    return spotify.search(album_name, type='album', limit=limit)['albums']['items']


# returns a dict list of up to size {limit} containing the search results
def get_artist(artist_name, limit=1):
    artist_name = bytes(artist_name, "utf-8").decode("unicode_escape")
    return spotify.search(artist_name, type='artist', limit=limit)['artists']['items']


# returns a dict list of up to size {limit} containing the search results
def get_song(song_name, limit=1):
    song_name = bytes(song_name, "utf-8").decode("unicode_escape")
    return spotify.search(song_name, type='track', limit=limit)['tracks']['items']


# returns a dict list of up to size {limit} containing the search results
def get_playlist(playlist_name, limit=1):
    playlist_name = bytes(playlist_name, "utf-8").decode("unicode_escape")
    return spotify.search(playlist_name, type='playlist', limit=limit)['playlists']['items']


def get_recommendations(genres=[], tracks=[], artists=[], limit=1):
    return spotify.recommendations(seed_genres=genres, seed_artists=artists, seed_tracks=tracks, limit=limit)


def main():
    data = get_playlist("This Is Abba")
    print(data[0]['name'])


if __name__ == '__main__':
    main()

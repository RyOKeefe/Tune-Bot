from flask import Flask, request
from API_Calls import *

# app reference

app = Flask(__name__)


@app.before_request
def before_request():
    print('request received')


@app.route("/")
def home_view():
    return "<h1>Welcome to Tune Bot</h1>"


@app.route('/api/recommendation')
def recommendations_default():
    return "Welcome to tunebot backend. Make a request."


@app.route('/api/recommendation', methods=['POST'])
def recommendation():
    genre_list = []
    track_list = []
    artist_list = []
    try:
        print(request.json)
        for genre in request.json["queryResult"]["parameters"]["music-genre"]:
            genre_list.append(genre)
    except TypeError:
        print("Invalid Genre Input")


    for artist in request.json["queryResult"]["parameters"]["music-artist"]:
        artist_list.append(get_artist(artist, limit=1)[0]['id'])

    for track in request.json["queryResult"]["parameters"]["song-name"]:
        track_list.append(get_song(track, limit=1)[0]['id'])
    temp = get_recommendations(genres=genre_list, artists=artist_list, tracks=track_list)['tracks'][0]
    return temp

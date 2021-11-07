from flask import Flask, request
import json
from API_Calls import *
import os
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
        if os.popen('hostname').read() == 'DESKTOP-A8S8UV7':
            for genre in request.json["queryResult"]["parameters"]["music-genre"]:
                genre_list.append(genre)

            for artist in request.json["queryResult"]["parameters"]["music-artist"]:
                artist_list.append(get_artist(artist, limit=1)[0]['id'])

            for track in request.json["queryResult"]["parameters"]["song-name"]:
                track_list.append(get_song(track, limit=1)[0]['id'])
        else:
            req_data = json.loads(request.data)
            for genre in req_data["queryResult"]["parameters"]["music-genre"]:
                genre_list.append(genre)

            for artist in req_data["queryResult"]["parameters"]["music-artist"]:
                artist_list.append(get_artist(artist, limit=1)[0]['id'])

            for track in req_data["queryResult"]["parameters"]["song-name"]:
                track_list.append(get_song(track, limit=1)[0]['id'])

    except TypeError:
        print("Invalid Genre Input")
        return get_recommendations(genres=[], artists=artist_list, tracks=track_list)
    except:
        print("Complete Failure")
        return get_recommendations(genres=[], artists=["Katy Perry"], tracks=["California Girls"])
    print("Successful Recommendation")
    return get_recommendations(genres=genre_list, artists=artist_list, tracks=track_list)

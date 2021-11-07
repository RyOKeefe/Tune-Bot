from flask import Flask, request
import json
from API_Calls import get_recommendations, get_playlist, get_song, get_artist, get_album
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
    response = None
    try:
        req_data = json.loads(request.data)
        for genre in req_data["queryResult"]["parameters"]["music-genre"]:
            genre_list.append(genre)

        for artist in req_data["queryResult"]["parameters"]["music-artist"]:
            artist_list.append(get_artist(artist, limit=1)[0]['id'])

        for track in req_data["queryResult"]["parameters"]["song-name"]:
            track_list.append(get_song(track, limit=1)[0]['id'])

    except TypeError as error:
        print("Invalid Genre Input")
        print(error)
        response = get_recommendations(genres=[], artists=artist_list, tracks=track_list)
    except Exception as error:
        print("Total failure")
        print(error)
        response = get_recommendations(genres=[], artists=[get_artist("Katy Perry",limit=1)[0]['id']], tracks=[get_song("California Girls",limit=1)[0]['id']])
    print("Successful Recommendation")
    response = get_recommendations(genres=genre_list, artists=artist_list, tracks=track_list)

    return {
  "fulfillmentMessages": [
    {
      "text": {
        "text": [
          "You should try listening to "+response['tracks'][0]['name']+" by " + response['tracks'][0]['artists'][0]['name']+". Would you like another music recommendation?"
        ]
      }
    }
  ]
}


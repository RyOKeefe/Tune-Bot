from flask import Flask, request
import json
from API_Calls import get_recommendations, get_playlist, get_song, get_artist, get_album, remove_und
import os

# app reference

app = Flask(__name__)
prev_recommendation = {'prev_artist': None,
                       'prev_song': None}


@app.before_request
def before_request():
    print('request received')


@app.route("/")
def home_view():
    return "<h1>Welcome to Tune Bot</h1>"


@app.route('/api/recommendation')
def recommendations_default():
    return "Welcome to tunebot backend. Make a request."


@app.route('/api/recommendation/iterate', methods=['POST'])
def iterate():
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
        print("Successful Recommendation")
        response = get_recommendations(genres=genre_list, artists=artist_list, tracks=track_list)
        prev_recommendation['prev_song'] = response['tracks'][0]['name']
        prev_recommendation['prev_artist'] = response['tracks'][0]['artists'][0]['name']

    except TypeError as error:
        print("Invalid Genre Input")
        print(error)
        response = get_recommendations(genres=[], artists=artist_list, tracks=track_list)
    except Exception as error:
        print("Total failure")
        print(error)
        response = get_recommendations(genres=[], artists=[get_artist("Katy Perry", limit=1)[0]['id']],
                                       tracks=[get_song("California Girls", limit=1)[0]['id']])

    if len(req_data["queryResult"]["parameters"]["song-name"]) > 0:
        print("Track Input:" + req_data["queryResult"]["parameters"]["song-name"][0])
    if len(req_data["queryResult"]["parameters"]["music-genre"]) > 0:
        print("Genre Input:" + req_data["queryResult"]["parameters"]["music-genre"][0])
    if len(req_data["queryResult"]["parameters"]["music-artist"]) > 0:
        print("Artist Input:" + req_data["queryResult"]["parameters"]["music-artist"][0])

    response = remove_und(response,
                          tracks=[prev_recommendation['prev_song']],
                          artists=[prev_recommendation['prev_artist']] + req_data["queryResult"]["parameters"]["music-artist"])
    print("Track recommendation:" + response['tracks'][0]['name'])
    print("Artist recommendation:" + response['tracks'][0]['artists'][0]['name'])



    return {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        "You should try listening to " + response['tracks'][0]['name'] + " by " +
                        response['tracks'][0]['artists'][0]['name'] + ". Would you like another music recommendation?"
                    ]
                }
            }
        ]
    }


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
        print("Successful Recommendation")
        response = get_recommendations(genres=genre_list, artists=artist_list, tracks=track_list)
    except TypeError as error:  # depreciated
        print("Invalid Genre Input, depreciated")
        print(error)
        response = get_recommendations(genres=[], artists=artist_list, tracks=track_list)
    except Exception as error:
        print("Total failure")
        print(error)
        response = get_recommendations(genres=[], artists=[get_artist("Katy Perry", limit=1)[0]['id']],
                                       tracks=[get_song("California Girls", limit=1)[0]['id']])

    if len(req_data["queryResult"]["parameters"]["song-name"]) > 0:
        print("Track Input:" + req_data["queryResult"]["parameters"]["song-name"][0])
    if len(req_data["queryResult"]["parameters"]["music-genre"]) > 0:
        print("Genre Input:" + req_data["queryResult"]["parameters"]["music-genre"][0])
    if len(req_data["queryResult"]["parameters"]["music-artist"]) > 0:
        print("Artist Input:" + req_data["queryResult"]["parameters"]["music-artist"][0])

    response = remove_und(response,
                          artists=req_data["queryResult"]["parameters"]["music-artist"],
                          tracks=track_list)
    print("Track recommendation:" + response['tracks'][0]['name'])
    print("Artist recommendation:" + response['tracks'][0]['artists'][0]['name'])
    prev_recommendation['prev_song'] = response['tracks'][0]['name']
    prev_recommendation['prev_artist'] = response['tracks'][0]['artists'][0]['name']



    return {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        "You should try listening to " + response['tracks'][0]['name'] + " by " +
                        response['tracks'][0]['artists'][0]['name'] + ". Would you like another music recommendation?"
                    ]
                }
            }
        ]
    }


@app.route('/api/recommendation/artist', methods=['POST'])
def artist_recommendation():
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
        print("Successful Recommendation")
        response = get_recommendations(genres=genre_list, artists=artist_list, tracks=track_list)

    except TypeError as error:  # depreciated
        print("Invalid Genre Input, depreciated")
        print(error)
        response = get_recommendations(genres=[], artists=artist_list, tracks=track_list)
    except Exception as error:
        print("Total failure")
        print(error)
        response = get_recommendations(genres=[], artists=[get_artist("Katy Perry", limit=1)[0]['id']],
                                       tracks=[get_song("California Girls", limit=1)[0]['id']])

    if len(req_data["queryResult"]["parameters"]["song-name"]) > 0:
        print("Track Input:" + req_data["queryResult"]["parameters"]["song-name"][0])
    if len(req_data["queryResult"]["parameters"]["music-genre"]) > 0:
        print("Genre Input:" + req_data["queryResult"]["parameters"]["music-genre"][0])
    if len(req_data["queryResult"]["parameters"]["music-artist"]) > 0:
        print("Artist Input:" + req_data["queryResult"]["parameters"]["music-artist"][0])

    response = remove_und(response, artists=artist_list + [prev_recommendation['prev_artist']])
    print("Track recommendation:" + response['tracks'][0]['name'])
    print("Artist recommendation:" + response['tracks'][0]['artists'][0]['name'])
    prev_recommendation['prev_song'] = None
    prev_recommendation['prev_artist'] = response['tracks'][0]['artists'][0]['name']
    return {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        "You should try listening to " +
                        response['tracks'][0]['artists'][0]['name'] + ". Would you like another artist recommendation?"
                    ]
                }
            }
        ]
    }

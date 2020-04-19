# Authors: Nikhil Kumar, Abhijit Raman, Nicholas Wille
import json

# Returns a list of the user's top 10 artists
def top_artists(data):
    artists = []
    items = data['items']
    for item in items:
        artist_name = item['name']
        artist_id = item['id']
        artist_tuple = (artist_name, artist_id)
        artists.append(artist_tuple)
    return artists


# Returns a list of the user's top 10 tracks
def top_tracks(data):
    tracks = {}
    for item in data['items']:
        track_name = item['name']
        track_id = item['id']
        track_tuple = (track_name, track_id)
        artist_name = item['artists'][0]['name']
        tracks[track_tuple] = artist_name
    return tracks


# Returns a list of track ids from the user's recent listening history
def recent_track_ids(data):
    tracks = []
    for item in data['items']:
        track_id = item['track']['id']
        if track_id not in tracks:
            tracks.append(track_id)
    return tracks


# Returns a list of track ids from the user's top songs
def top_track_ids(data):
    ids = []
    for item in data['items']:
        ids.append(item['id'])
    return ids


# Returns a list of urls for track artworks
def track_images(data):
    images = []
    uris = []
    try:
        for item in data['tracks']:
            image = item['album']['images'][0]['url']
            images.append(image)
            uri = item['uri']
            uris.append(uri)
        return (images, uris)
    except:
        if data['error']:
            error = data['error']
            status = error['status']
            if status == 400:
                return images


# Returns a list of urls for artist profile images
def artist_images(data):
    images = []
    uris = []
    try:
        for item in data['artists']:
            image = item['images'][0]['url']
            images.append(image)
            uri = item['uri']
            uris.append(uri)
        print(uris)
        return (images, uris)
    except:
        if data['error']:
            error = data['error']
            status = error['status']
            if status == 400:
                return images


# Returns a dictionary with recently listened to tracks grouped by artist
def recent_tracks(data):
    recents = {}
    num_listens = {}
    for item in data['items']:
        track_name = item['track']['name']
        track_id = item['track']['id']
        artist_name = item['track']['artists'][0]['name']
        artist_id = item['track']['artists'][0]['id']
        recents[(track_name, track_id)] = (artist_name, artist_id)
        if artist_id in num_listens:
            num_listens[artist_id] = num_listens[artist_id] + 1
        else:
            num_listens[artist_id] = 1
    return recents


# Returns a dictionary with the top 50 tracks grouped by artist
def top_tracks_by_artist(top_tracks, top_artists):
    top_tracks_by_artist = {}
    for artist in top_artists:
        tracks = []
        for track in top_tracks:
            track_artist = top_tracks.get(track)
            if artist[0] == track_artist:
                tracks.append(track[0])
        if len(tracks) > 0:
        	top_tracks_by_artist[artist] = tracks
    return top_tracks_by_artist


# Process the data needed for audio analysis
def get_audio_datapoints(data):
    datapoints = {}
    datapoints['danceability'] = []
    datapoints['energy'] = []
    datapoints['instrumentalness'] = []
    datapoints['tempo'] = []
    datapoints['acousticness'] = []
    datapoints['valence'] = []
    datapoints['liveness'] = []
    datapoints['loudness'] = []
    datapoints['speechiness'] = []
    for category in data['audio_features']:
        if category !=  None:
            datapoints['danceability'].append(category['danceability'])
            datapoints['energy'].append(category['energy'])
            datapoints['instrumentalness'].append(category['instrumentalness'])
            datapoints['tempo'].append(category['tempo'])
            datapoints['acousticness'].append(category['acousticness'])
            datapoints['valence'].append(category['valence'])
            datapoints['liveness'].append(category['liveness'])
            datapoints['loudness'].append(category['loudness'])
            datapoints['speechiness'].append(category['speechiness'])
    return datapoints

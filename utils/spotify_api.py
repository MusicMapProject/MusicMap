#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import requests


class SpotifyAPI:
    urls = {
        'tracks': 'https://api.spotify.com/v1/tracks',
        'audio_features': 'https://api.spotify.com/v1/audio-features',
        'search': 'https://api.spotify.com/v1/search',
        'token': 'https://accounts.spotify.com/api/token'
    }

    def __init__(self, client_id, client_secret):
        params = {"grant_type": "client_credentials"}
        headers = {"Authorization": "Basic {}".format(
            base64.b64encode("{}:{}".format(client_id, client_secret))
        )}
        answer = requests.post(self.urls['token'], params, headers=headers).json()
        self.token = answer['access_token']

    def get_audio(self, ids, market=None):
        params = {"ids": ','.join(ids)}
        if market is not None:
            params["market"] = market

        headers = {"Authorization": "Bearer {}".format(self.token)}
        return requests.get(self.urls['tracks'], params, headers=headers).json()

    def get_audio_features(self, ids):
        params = {"ids": ','.join(ids)}
        headers = {"Authorization": "Bearer {}".format(self.token)}
        return requests.get(self.urls['audio_features'], params, headers=headers).json()

    def search(self, query, type=['track', 'artist'], market=None, limit=10, offset=5):
        params = {
            "query": query,
            "type": ','.join(type),
            "limit": limit,
            "offset": offset
        }
        if market is not None:
            params["market"] = market

        headers = {"Authorization": "Bearer {}".format(self.token)}
        return requests.get(self.urls['search'], params, headers=headers).json()


if __name__ == "__main__":
    client_id, client_secret = None, None
    spotify = SpotifyAPI(client_id, client_secret)
    answer = spotify.get_audio(["7ouMYWpwJ422jRcDASZB7P", "4VqPOruhp5EdPBeR92t6lQ", "2takcwOaAZWiXQijPHIx7B"])
    print answer['tracks'][-1]['preview_url']
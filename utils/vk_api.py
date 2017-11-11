#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests


class VkAudioAPI:
    def __init__(self, token):
        self.version = "5.68"
        self.token = token

    def search(self, query, search_own=1, sort=0, count=10, offset=0):
        if count > 100:
            raise ValueError("Max limit for count is 100")

        return requests.get("https://api.vk.com/method/audio.search", params={
            'v': self.version,
            'q': query,
            'search_own': search_own,
            'offset': offset,
            'sort': sort,
            'count': count,
            'access_token': self.token
        }).json()

    def get(self, owner_id=15598144, count=10, offset=0):
        return requests.get("https://api.vk.com/method/audio.get", params={
            'v': self.version,
            'owner_id': owner_id,
            'count': count,
            'offset': offset,
            'access_token': self.token
        }).json()

    def getCount(self, owner_id=15598144):
        return requests.get("https://api.vk.com/method/audio.getCount", params={
            'v': self.version,
            'owner_id': owner_id,
            'access_token': self.token
        }).json()


def main():
    token = None
    vk_api = VkAudioAPI(token)
    # owner_id = 32993651  # Ралина
    owner_id = 15598144  # Вова
    nb_asserted = vk_api.getCount(owner_id=owner_id)['response']
    nb_count = 100

    nb_total = 0

    content_with_music = []
    content_restricted = []

    for offset in range(0, nb_asserted, nb_count):
        resp = dict()
        while resp.get('response') is None:
            resp = vk_api.get(owner_id=owner_id, count=nb_count, offset=offset)
            if resp.get('error'):
                time.sleep(2)
        content_with_music.extend(filter(
            lambda x: x.get('url') is not None and x.get('url') != '',
            resp['response']['items']))
        content_restricted.extend(filter(
            lambda x: x.get('content_restricted', 0) != 0,
            resp['response']['items']))
        nb_total += len(resp['response']['items'])

    nb_with_music = len(content_with_music)
    nb_restricted = len(content_restricted)

    print 'owner_id: {}'.format(owner_id)
    print 'nb_asserted:     {:>4d}'.format(nb_asserted)
    print 'nb_total:        {:>4d}'.format(nb_total)
    print 'nb_with_music:   {:>4d}'.format(nb_with_music)
    print 'nb_restricted:   {:>4d}'.format(nb_restricted)

    for music in content_restricted:
        print u"{} - {}".format(music['artist'], music['title'])
        if music.get('url') != '':
            print music["url"]


if __name__ == '__main__':
    main()

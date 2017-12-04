#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs

import time
import json
import codecs
import os
import urllib
import time
from multiprocessing import Pool
import threading

from utils.vk_api import VkAudioAPI

download_pool = []
database_audios = dict()
database_users = dict()


def download_audio(args):
    urllib.urlretrieve(*args)


def proccess_download_pool(path):
    t = threading.currentThread()
    
    global download_pool
    
    while getattr(t, "do_run", True):
        if len(download_pool) == 0:
            time.sleep(5)
            continue

        download_backup = download_pool[:]
        pool = Pool(processes=10)
        res = pool.map_async(
            download_audio,
            [(url, os.path.join(path, str(audio_id)+'.mp3')) for audio_id, url in download_backup]
        )
        res.get()
        pool.close()
        pool.join()

        for audio_id, url in download_backup:
            user_id = audio_id.split('_')[0]
            database_audios[user_id][audio_id]['downloaded'] = 1
        download_pool = filter(lambda d: d not in download_backup, download_pool)


conf = dict()
answer = """"<html><body><h1>Get Request Received!</h1></body>
<script type="text/javascript">window.location.replace("https://vk.com/audios{}");</script>
</html>"""


class S(BaseHTTPRequestHandler):
    global database_audios
    global database_users

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global conf

        self._set_headers()
        print "Input path:", self.path

        if self.path.startswith('/auth'):
            # TODO: Right way to authorise: https://vk.com/dev/auth_sites
            params = parse_qs(urlparse(self.path).query)
            code = params['code'][0]

            resp = VkAudioAPI.auth(code=code, **conf)
            user_id = str(resp['user_id'])
            if user_id not in database_users:
                database_users[user_id] = dict()
            database_users[user_id]['access_token'] = resp['access_token']
            database_users[user_id]['expires_in'] = resp['expires_in']

            self.wfile.write(answer.format(user_id))
        elif self.path.startswith("/playlist"):
            # TODO: Implement creating playlist using VkApi
            params = parse_qs(urlparse(self.path).query)
            user_id = params['user_id'][0]

            vk_api = VkAudioAPI(database_users[user_id]['access_token'])

            if 'album' in database_users[user_id]:
                album_id = database_users[user_id]['album']
                vk_api.deleteAlbum(album_id, user_id)
            resp = vk_api.addAlbum()
            print resp
            album_id = str(resp['response']['album_id'])
            database_users[user_id]['album'] = album_id

            audio_id = params['audio_id'][0]
            
            """
            audio_ids = {audio_id}
            
            # No check if file exists cause if point is on map then file do exist
            with open(params['predict'][0]) as f_csv:
                _ = f_csv.next()  # skip header
                for line in f_csv:
                    if len(audio_ids) == 10:
                        break
                    audio_id = line.strip().split(',')[0]
                    audio_id = audio_id.split('_')[1]
                    audio_ids.add(audio_id)
                audio_id = params['audio_id'][0]
                audio_ids.remove(audio_id)
            
            # Audios should be reversed order. It's a must
            audio_ids = list(audio_ids) + [audio_id]
            
            """
            
            user_id = params['user_id'][0]
            audio_id = params['audio_id'][0]
            predict_path = params['predict'][0]
            
            playlist_array = []
            if not os.path.isfile(predict_path + '_sorted'):
                print  "Not exit predicted sorted file"
            else:
                with open(predict_path + '_sorted') as sort_predict_file:
                    for line in sort_predict_file.readlines():
                        ids = line.strip().split(',')
                        if ids[0] == user_id + '_' + audio_id:
                            for audio in ids:
                                playlist_array = [audio.split('_')[1]] + playlist_array
                                
            playlist_array = [audio_id] + playlist_array
            
            for audio_id in playlist_array:
                print audio_id
                print vk_api.moveToAlbum(album_id, audio_id, user_id)
                time.sleep(1.0)
            
            self.wfile.write(album_id)
        else:
            if os.path.exists(self.path):
                with open(self.path) as f_csv:
                    self.wfile.write(f_csv.read())

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print post_data # <-- Print post data

        if post_data != '':
            audio_id, artist, title, url = post_data.split('\t')
            user_id = audio_id.split('_')[0]

            if user_id not in database_audios:
                database_audios[user_id] = dict()
            audio = {'id': audio_id, 'artist': artist, 'title': title, 'url': url, 'downloaded': 0}
            if audio_id not in database_audios[user_id]: # or database[user_id][audio_id]['url'] != audio['url']:
                print "{} need to be download!".format(audio_id)
                download_pool.append((audio_id, url))
                database_audios[user_id][audio_id] = audio
            else:
                print "{} has already been downloaded!".format(audio_id)
        
        self._set_headers()


def run(server_class=HTTPServer, handler_class=S, port=86):
    global conf
    with codecs.open("app.conf", mode='r', encoding='utf-8') as f_json:
        conf = json.load(f_json)

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd... at port ', port
    t1 = threading.Thread(target=proccess_download_pool, args=('/mnt/hdd/music_map_project/data_mp3', ))

    global database_audios
    global database_users

    
    if os.path.isfile("server.conf"):
        with codecs.open("server.conf", mode='r', encoding='utf-8') as f_json:
            database_audios = json.load(f_json)
   
    if os.path.isfile("users.conf"):
        with codecs.open("users.conf", mode='r', encoding='utf-8') as f_json:
            database_users = json.load(f_json)
    
    
    try:
        t1.start()
        httpd.serve_forever()
    finally:
        t1.do_run = False
        t1.join()
        
        with codecs.open("server.conf", mode='w', encoding='utf-8') as f_json:
            json.dump(database_audios, f_json)

        with codecs.open("users.conf", mode='w', encoding='utf-8') as f_json:
            json.dump(database_users, f_json)
        


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

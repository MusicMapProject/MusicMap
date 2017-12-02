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

import json
import codecs
import os
import urllib
import time
from multiprocessing import Pool
import threading

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


answer = "<html><body><h1>Get Request Received!</h1></body></html>"


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        print "Input path:", self.path

        if self.path == '/auth':
            # TODO: Right way to authorise: https://vk.com/dev/auth_sites
            # params = parse_qs(urlparse(self.path).query)
            # code = params['code'][0]
            self.wfile.write(answer)
        elif self.path == "/playlist":
            # TODO: Implement creating playlist using VkApi
            pass
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

        if post_data.find("access_token"):
            user_token = dict(map(lambda x: x.split('='), post_data.split('&')))
            database_users[user_token["user_id"]] = {
                'access_token': user_token['access_token'],
                'expires': user_token['expires']
            }
        elif post_data != '':
            audio_id, artist, title, url = post_data.split('\t')
            # url = list(urlparse(url))
            # url[-2] = ''
            # url = urlunparse(url)
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
    global database_audios
    global database_users

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd... at port ', port
    t1 = threading.Thread(target=proccess_download_pool, args=('/mnt/hdd/music_map_project/data_mp3', ))
    
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

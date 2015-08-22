# -*- coding: utf-8 -*-
import requests

def lives(query):
    url = "https://hackathon-api.livefans.jp/ver010000"
    params = {
        "client_id": "100025",
        "q": query,
        "format": "json"
    }
    r = requests.get(url + "/search/lives", params=params)
    print(r.json())

def rekognize(image_url):
    url = "https://rekognition.com/func/api/"
    data = {
        "api_key": "b6hbSTEdGClw3CnQ",
        "api_secret": "n7kK7QoOgtrkJlBL",
        "jobs": "scene_understanding_3",
        "urls": image_url
    }
    
    r = requests.post(url, data=data)
    print(r.json())

def puchi_lyrics(lyrics_text):
    url = "https://pl.t.petitlyrics.com/mh/1/lyrics/list.xml"
    auth_key = "X4c1B1mUXPnQchBP6ppcBvo8lv4HxKYW"
    
    params = {
        "lyrics_text": lyrics_text,
        "auth_key": auth_key
    }
    
    r = requests.get(url, params=params)
    print(r.text)


if __name__ == "__main__":
    # lives("Nothing's Carved in Stone")
    # rekognize("https://rekognition.com/static/img/demo/beach.jpg")
    puchi_lyrics("海,ビーチ")

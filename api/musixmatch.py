import json
import requests
from envs import get_env


class MusixMatch():
    HOST = "http://api.musixmatch.com/ws/1.1"

    def __init__(self, api_key=""):
        self.api_key = api_key or get_env("musixmatch_api_key")

    def search_track(self, q, q_lyrics="", lang="", page=0, page_size=10, f_has_lyrics=True):
        """
        https://developer.musixmatch.com/documentation/api-reference/track-search
        :param q:
        :param q_lyrics:
        :param page:
        :param page_size:
        :param f_has_lyrics:
        :return:
        """
        url = self.HOST + "/track.search"

        params = {
            "apikey": self.api_key,
            "q": q,
            "q_lyrics": q_lyrics,
            "page": page,
            "page_size": page_size,
            "format": "json"
        }

        if f_has_lyrics:
            params["f_has_lyrics"] = "true"

        if lang:
            params["f_lyrics_language"] = lang

        resp = requests.get(url, params=params)
        tracks = []

        if resp.ok:
            body = resp.json()
            body = self.__extract_body(body)
            tracks = [t["track"] for t in body["track_list"]]
        else:
            resp.raise_for_status()

        return tracks

    def get_track_lyrics(self, track_id):
        """
        https://developer.musixmatch.com/documentation/api-reference/track-lyrics-get
        :param track_id:
        :return:
        """
        url = self.HOST + "/track.lyrics.get"

        params = {
            "apikey": self.api_key,
            "track_id": track_id,
            "format": "json"
        }

        resp = requests.get(url, params=params)

        if resp.ok:
            body = resp.json()
            body = self.__extract_body(body, "lyrics")
            return body
        else:
            resp.raise_for_status()

    def match_track_and_lyrics(self, q, q_lyrics="", lang=""):
        lyrics = {}
        tracks = self.search_track(q, q_lyrics=q_lyrics, page=0, page_size=1, f_has_lyrics=True, lang=lang)

        if len(tracks) > 0:
            track_id = tracks[0]["track_id"]
            lyrics = self.get_track_lyrics(track_id)

        return lyrics

    def match_lyrics(self, q_track, q_artist):
        """
        https://developer.musixmatch.com/documentation/api-reference/matcher-lyrics-get
        :param q_track:
        :param q_artist:
        :return:
        """

        url = self.HOST + "/matcher.lyrics.get"
        params = {
            "apikey": self.api_key,
            "q_track": q_track,
            "q_artist": q_artist,
            "format": "json"
        }

        resp = requests.get(url, params=params)

        lyrics = []
        if resp.ok:
            body = resp.json()
            body = self.__extract_body(body, "lyrics")
            return body
        else:
            resp.raise_for_status()

    def __extract_body(self, body, attribute=""):
        b = {}
        if "message" in body and "body" in body["message"]:
            b = body["message"]["body"]
            if attribute and attribute in b:
                b = b[attribute]

        return b

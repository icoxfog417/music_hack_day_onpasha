import json
import requests
import xml.etree.ElementTree as ET
from envs import get_env


class Petitlyrics():

    def __init__(self):
        self.HOST = "https://pl.t.petitlyrics.com/mh/1/lyrics/list.xml"
        self.auth_key = get_env("petitlyrics_auth_key")

    def track_to_lyrics(self, title, offset=0, limit=4):
        params = {
            "title": title,
            "auth_key": self.auth_key,
            "priority": 2
        }

        r = requests.get(self.HOST, params=params)
        lyrics = []

        if r.ok:
            lyrics_xml = ET.fromstring(r.text)
            lyric_data = lyrics_xml.find("songs/song/lyricsData").text
            lines = json.loads(lyric_data)
            if "lines" in lines:
                for i, ln in enumerate(lines["lines"]):
                    ly = " ".join([s["string"] for s in ln["words"]])
                    page = i // limit
                    if page >= offset and len(lyrics) < limit:
                        lyrics.append(ly)

        return lyrics

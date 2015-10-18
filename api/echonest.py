import requests
from envs import get_env
from api.spotify import Spotify


class Track():

    def __init__(self, title, artist_name, artist_id, track_id, spotify_id, song_hotttnesss, preview_url="", images=(), track_url=""):
        self.title = title
        self.artist_name = artist_name
        self.artist_id = artist_id
        self.track_id = track_id
        self.spotify_id = spotify_id
        self.song_hotttnesss = song_hotttnesss
        self.preview_url = preview_url
        self.images = [] if len(images) == 0 else images
        self.track_url = track_url

    @classmethod
    def create(cls, trackj):
        top_track = trackj["tracks"][0]

        t = Track(
            trackj["title"],
            trackj["artist_name"],
            trackj["artist_id"],
            top_track["id"],
            top_track["foreign_id"].replace("spotify:track:", ""),
            trackj["song_hotttnesss"]
        )

        return t

    def load_spotify(self, spotify):
        if self.spotify_id:
            s = spotify.get_track(self.spotify_id)
            self.set_spotify(s)

    def set_spotify(self, track):
        self.preview_url = track["preview_url"]
        self.images = track["album"]["images"]
        self.track_url = track["external_urls"]["spotify"]

class Echonest():
    HOST = "http://developer.echonest.com/api/v4"
    MOOD = ["happy", "aggressive", "sentimental", "cheerful"]

    def __init__(self):
        self.api_key = get_env("echonest_api_key")

    def search_songs(self, mood="", genres=(), results=5):
        # use playlist api to avoid duplicates of song
        # https://developer.echonest.com/forums/thread/1347
        url = self.HOST + "/playlist/static"
        params = {
            "api_key": self.api_key,
            "format": "json",
            "song_selection": "song_hotttnesss-top",
            "type": "artist-description",
            "bucket": ["song_hotttnesss", "id:spotify", "tracks"],
            "results": results,
            "limit": True
        }
        if mood:
            params["mood"] = mood

        if genres:
            params["style"] = genres

        resp = requests.get(url, params=params)

        tracks = []
        if resp.ok:
            body = resp.json()
            if "response" in body:
                songs = body["response"]["songs"]
                for s in songs:
                    tracks.append(Track.create(s))
        else:
            resp.raise_for_status()

        return tracks

    def download_genres(self, path):
        url = self.HOST + "/genre/list"
        params = {
            "api_key": self.api_key,
            "format": "json",
            "bucket": "description"
        }

        resp = requests.get(url, params=params)

        if resp.ok:
            body = resp.json()
            if "response" in body:
                genres = body["response"]["genres"]
                lines = []
                for g in genres:
                    line = "\t".join([g["name"], g["description"]]) + "\n"
                    lines.append(line)

                with open(path, "wb") as f:
                    f.writelines([ln.encode("utf-8") for ln in lines])
        else:
            resp.raise_for_status()

    def download_moods(self, path):
        url = self.HOST + "/artist/list_terms"
        params = {
            "api_key": self.api_key,
            "format": "json",
            "type": "mood"
        }

        resp = requests.get(url, params=params)

        if resp.ok:
            body = resp.json()
            if "response" in body:
                terms = body["response"]["terms"]
                with open(path, "wb") as f:
                    for t in terms:
                        f.write((t["name"]+"\n").encode("utf-8"))
        else:
            resp.raise_for_status()

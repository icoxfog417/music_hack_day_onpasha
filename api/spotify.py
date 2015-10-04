import requests
from envs import get_env


class Spotify():
    HOST = "https://api.spotify.com/v1"

    def __init__(self):
        url = "https://accounts.spotify.com/api/token"
        client_id = get_env("spotify_client_id")
        client_secret = get_env("spotify_client_secret")

        self.token = ""
        resp = requests.post(url, data={"grant_type": "client_credentials"}, auth=(client_id, client_secret))
        if resp.ok:
            body = resp.json()
            self.token = body["access_token"]

    def get_track(self, track_id):
        url = self.HOST + "/tracks/{0}".format(track_id)
        resp = requests.get(url, headers=self.__headers())

        if resp.ok:
            body = resp.json()
            return body
        else:
            resp.raise_for_status()

    def __headers(self):
        return {
            "Authorization": "Bearer " + self.token
        }
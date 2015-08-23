import requests
from datetime import datetime
from datetime import timedelta
import random
from envs import get_env


class LiveFans():

    def __init__(self):
        self.HOST = "https://hackathon-api.livefans.jp/ver010000"
        self.client_id = get_env("livefan_client_id")

    def get_live_artists(self, count=5):
        url = self.HOST + "/search/lives"
        # search near tokyo
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=100)).strftime("%Y-%m-%d")
        params = {
            "client_id": self.client_id,
            "start_date": start_date,
            "end_date": end_date,
            "limit": count,
            "order": "CLIP_HIGHER",
            "format": "json"
        }
        r = requests.get(url, params=params)
        artists = []

        if r.ok:
            result = r.json()
            if "response" in result and "item_lives" in result["response"]:
                result = result["response"]["item_lives"]
                lives = result["item_live"]
                for live in lives:
                    if live["artist_name"]:
                        artists.append(live["artist_name"])
                    else:
                        a = random.sample(live["artists_name"].split(","), 1)[0]
                        artists.append(a)

        artists = [a.strip() for a in artists]
        return artists

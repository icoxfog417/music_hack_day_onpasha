import random
from api import pygn
from envs import get_env


class Gracenote():
    MOOD_IDS = {
        "Peaceful": "65322",
        "Easygoing": "42946",
        "Stirring": "65331",
        "Serious": "65328",
        "Aggressive": "42958",
        "Sophisticated": "42954",
        "Cool": "65326",
        "Romantic": "65323"
    }

    def __init__(self):
        self.client_id = get_env("gracenote_client_id")
        self.user_id = get_env("gracenote_user_id")

    def get_artists_mood_tracks(self, artists, mood_index):
        element_id = self.MOOD_IDS[mood_index]
        artist = random.sample(artists, 1)[0]
        metadatas = pygn.createRadio(clientID=self.client_id, userID=self.user_id, artist=artist, mood=element_id, popularity="800", similarity="800", count="5")
        return metadatas

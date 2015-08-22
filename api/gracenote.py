from api import pygn
from envs import get_env


class Gracenote():
    MOOD_IDS = {
        "Peaceful": "65322",
        "Romantic": "65323"
    }

    def __init__(self):
        self.client_id = get_env("gracenote_client_id")
        self.user_id = get_env("gracenote_user_id")

    def get_mood_tracks(self, mood_text):
        element_id = self.MOOD_IDS[mood_text]
        metadata = pygn.createRadio(clientID=self.client_id, userID=self.user_id, artist="星野源", mood=element_id, popularity="800", similarity="800", count="5")
        return metadata

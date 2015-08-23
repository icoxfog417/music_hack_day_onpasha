import requests
import numpy as np
from machines.machine_loader import MachineLoader
from envs import get_env


class Rekognition():
    FEATURES = ['building', 'clothing', 'downtown', 'maillot', 'swimwear']
    MOODS = ["Peaceful", "Easygoing", "Stirring", "Serious", "Aggressive", "Sophisticated", "Cool", "Romantic"]

    def __init__(self):
        self.columns = self.FEATURES
        self.key = get_env("rekognition_key")
        self.secret = get_env("rekognition_secret")
        self.limit = 3

    def rekognize(self, image_url):
        url = "https://rekognition.com/func/api/"
        data = {
            "api_key": self.key,
            "api_secret": self.secret,
            "jobs": "scene_understanding_3",
            "urls": image_url,
            "num_return": self.limit
        }

        score = np.zeros(len(self.columns))
        r = requests.post(url, data=data)
        if r.ok:
            content = r.json()
            if "scene_understanding" in content:
                matches = content["scene_understanding"]["matches"]
                for m in matches:
                    if m["tag"] in self.columns:
                        i = self.columns.index(m["tag"])
                        score[i] = m["score"]

        return score

    def images_to_mood(self, image_urls):
        import machines.photo_mood
        machine = MachineLoader.load(machines.photo_mood)

        mood_score = {}
        for url in image_urls:
            score = self.rekognize(url)
            mood = machine.predict(score)[0]
            mood_score[self.MOODS[int(mood)]] = 1

        return mood_score

import json
import requests
from envs import get_env


class VisionRecognizer():
    HOST = "https://gateway.watsonplatform.net/visual-recognition-beta/api"

    def __init__(self):
        self.username = get_env("vision_recognize_user")
        self.password = get_env("vision_recognize_pass")

    def recognize(self,  image_url_or_binary, label_group_or_list=""):
        url = self.HOST + "/v1/tag/recognize"
        fname = "imgFile.jpg"
        image = None
        if isinstance(image_url_or_binary, str):
            from urllib.parse import urlparse
            from os.path import basename
            fname = basename(urlparse(image_url_or_binary).path)
            image = requests.get(image_url_or_binary).content
        else:
            image = image_url_or_binary

        img_file = {
            "imgFile": (fname, image)
        }

        if label_group_or_list:
            labels = self.get_labels(label_group_or_list)
            resp = requests.post(url, data={"labels_to_check": json.dumps(labels)}, files=img_file, auth=(self.username, self.password))
        else:
            resp = requests.post(url, files=img_file, auth=(self.username, self.password))

        if resp.ok:
            return resp.json()
        else:
            raise resp.raise_for_status()

    def get_labels(self, label_group_or_list):
        url = self.HOST + "/v1/tag/labels"

        params = {
            "labels_to_check": json.dumps({
                "label_groups": label_group_or_list if isinstance(label_group_or_list, (list, tuple)) else [label_group_or_list]
            })
        }

        resp = requests.get(url, params=params, auth=(self.username, self.password))

        if resp.ok:
            return resp.json()
        else:
            raise resp.raise_for_status()

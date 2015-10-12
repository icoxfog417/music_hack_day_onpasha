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

        if isinstance(image_url_or_binary, (list, tuple)):
            fname, image = self._get_images(image_url_or_binary, fname)
        else:
            fname, image = self._get_image(image_url_or_binary, fname)

        img_file = {
            "imgFile": (fname, image)
        }

        if label_group_or_list:
            labels = self.get_labels(label_group_or_list)
            resp = requests.post(url, data={"labels_to_check": json.dumps(labels)}, files=img_file, auth=(self.username, self.password))
        else:
            resp = requests.post(url, files=img_file, auth=(self.username, self.password))

        if resp.ok:
            return Result(resp.json())
        else:
            raise resp.raise_for_status()

    def _get_images(self, image_url_or_binary, fname):
        import os
        import asyncio
        import zipfile
        from io import BytesIO

        name, ext = os.path.splitext(fname)

        @asyncio.coroutine
        def async_get_images(im_or_b, fn):
            return self._get_image(im_or_b, fn)

        tasks = [async_get_images(c, "{0}_{1}.{2}".format(name, i, ext)) for i, c in enumerate(image_url_or_binary)]
        done, _ = asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))

        buff = BytesIO()
        with zipfile.ZipFile(buff, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for f in done:
                name, binary = f.result()
                zf.writestr(name, binary)

        fname = name + ".zip"
        image = buff.getvalue()
        return fname, image

    def _get_image(self, image_url_or_binary, default_file_name):
        fname = default_file_name
        image = None

        if isinstance(image_url_or_binary, str):
            from urllib.parse import urlparse
            from os.path import basename
            fname = basename(urlparse(image_url_or_binary).path)
            image = requests.get(image_url_or_binary).content
        else:
            image = image_url_or_binary

        return fname, image

    def get_labels(self, label_group_or_list):
        url = self.HOST + "/v1/tag/labels"

        params = {}
        if label_group_or_list:
            params["labels_to_check"] = json.dumps({
                "label_groups": label_group_or_list if isinstance(label_group_or_list, (list, tuple)) else [label_group_or_list]
            })

        resp = requests.get(url, params=params, auth=(self.username, self.password))

        if resp.ok:
            return resp.json()
        else:
            raise resp.raise_for_status()


class Result():

    def __init__(self, obj):
        self.images = []
        if "images" in obj:
            for im in obj["images"]:
                r = {}
                for lb in im["labels"]:
                    r[lb["label_name"]] = float(lb["label_score"])
                self.images.append(r)

    def to_matrix(self, targets):
        import numpy as np
        mx = np.zeros((len(self.images), len(targets)))
        for i, labels in enumerate(self.images):
            for t in [n for n in labels if n in targets]:
                mx[i][targets.index(t)] = labels[t]

        return mx

    def __len__(self):
        return len(self.images)

    def __getitem__(self, i):
        return self.images[i]

    def __str__(self):
        return json.dumps(self.images)




import os
from datetime import datetime
import requests


API_KEY = "b6hbSTEdGClw3CnQ"
API_SECRET = "n7kK7QoOgtrkJlBL"

def read_file(path):
    lines = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        lines = [ln.strip(os.linesep) for ln in lines]

    return lines

def write_file(path, rows, separator="\t"):
    with open(path, "wb") as outfile:
        for row in rows:
            line = ""
            if isinstance(row, list) or isinstance(row, tuple):
                line = separator.join(row) + os.linesep
            else:
                line = row + os.linesep
            outfile.write(line.encode("utf-8"))


def rekognize(image_url):
    url = "https://rekognition.com/func/api/"
    data = {
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "jobs": "scene_understanding_3",
        "urls": image_url,
        "num_return": 3
    }

    tag_and_score = {}
    r = requests.post(url, data=data)
    if r.ok:
        content = r.json()
        if "scene_understanding" in content:
            for m in content["scene_understanding"]["matches"]:
                tag_and_score[m["tag"]] = m["score"]

    return tag_and_score

def rekognize_all(line):
    tags = []
    data = []

    for ln in line:
        url = ln[0]
        mood = ln[1]
        r = rekognize(url)
        for k in r:
            if k not in tags:
                tags.append(k)

        data.append((url, mood, r))

    tags.sort()
    header = ["url", "mood"] + tags
    lines = [header]
    for d in data:
        url = d[0]
        mood = d[1]
        tag = d[2]
        ln = [url, mood]
        for t in tags:
            if t in tag:
                ln.append(str(tag[t]))
            else:
                ln.append(str(0))

        lines.append(ln)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    path = os.path.join(os.path.dirname(__file__), "./training_data_{0}.txt".format(timestamp))
    write_file(path, lines)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        path = os.path.join(os.path.dirname(__file__), sys.argv[1])
        input_file = read_file(path)
        inputs = []
        for ln in input_file:
            inputs.append(ln.split("\t")[:2])

        rekognize_all(inputs)

    else:
        print("you have to set image_url and mood file.")

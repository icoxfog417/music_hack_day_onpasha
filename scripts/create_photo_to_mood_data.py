import os
from datetime import datetime
from api.bluemix_vision_recognition import VisionRecognizer
from api.echonest import Echonest


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
    vr = VisionRecognizer()
    result = vr.recognize(image_url)
    tag_and_score = {}
    if "images" in result:
        labels = result["images"][0]["labels"]
        for lb in labels:
            tag_and_score[lb["label_name"]] = lb["label_score"]

    return tag_and_score

def rekognize_all(line):
    tags = []
    data = []

    for i, ln in enumerate(line):
        mood = ln[0]
        url = ln[1]
        try:
            r = rekognize(url)
            for k in r:
                if k not in tags:
                    tags.append(k)

            data.append((mood, url, r))
            print("{0} success.".format(i))
        except Exception as ex:
            print("{0}: {1}".format(i, ex))

    tags.sort()
    header = ["mood", "url"] + tags
    lines = [header]
    for d in data:
        mood, url, tag_scores = d
        mood_index = -1 if mood not in Echonest.MOOD else Echonest.MOOD.index(mood)
        ln = [str(mood_index), url]
        for t in tags:
            if t in tag_scores:
                ln.append(str(tag_scores[t]))
            else:
                ln.append(str(0))

        lines.append(ln)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    path = os.path.join(os.path.dirname(__file__), "../data/photo_to_mood_{0}.txt".format(timestamp))
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
        print("you have to set mood/image_url file.")

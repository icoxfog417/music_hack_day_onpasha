import re
from collections import Counter
from api.bluemix_vision_recognition import VisionRecognizer
from api.echonest import Echonest
from api.spotify import Spotify
from machines.machine_loader import MachineLoader
import machines.photo_mood


def convert(image_urls):
    vr = VisionRecognizer()
    ec = Echonest()
    sp = Spotify()
    photo_to_mood = MachineLoader.load(machines.photo_mood)
    TARGET_LABELS = ['Boat', 'Human', 'Insect', 'Invertebrate', 'Mammal', 'Man Made Scene', 'Outdoors', 'People Activity', 'Placental Mammal', 'Vertebrate']

    # analyze moode
    moods = Counter()
    for url in image_urls:
        result = vr.recognize(url)
        vector = VisionRecognizer.to_matrix(result, TARGET_LABELS)[0]
        mood = photo_to_mood.predict(vector)[0]
        moods[mood] += 1

    target_mood = moods.most_common(1)[0][0]
    target_mood = Echonest.MOOD[int(target_mood)]

    # choose song from mood
    tracks = ec.search_songs(target_mood)

    # load spotify info
    for t in tracks:
        t.load_spotify(sp)

    result = {
        "mood": target_mood,
        "tracks": [t.__dict__ for t in tracks]
    }

    return result

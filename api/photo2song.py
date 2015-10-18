import asyncio
from collections import Counter
from api.bluemix_vision_recognition import VisionRecognizer
from api.echonest import Echonest
from api.spotify import Spotify
from machines.machine_loader import MachineLoader
import machines.photo_mood


def convert(image_urls):
    ec = Echonest()
    sp = Spotify()
    log = []

    # analyze moode
    log.append("begin vision recognition")
    target_mood = photo2mood(image_urls)

    # choose song from mood
    log.append("begin search song by mood")
    tracks = ec.search_songs(target_mood)

    # load spotify info
    @asyncio.coroutine
    def load_spotify(t):
        t.load_spotify(sp)

    log.append("begin load song information")
    tasks = [load_spotify(t) for t in tracks]
    done, _ = asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))

    result = _make_result(target_mood, tracks, log=log)
    return result

def photo2mood(image_urls):
    vr = VisionRecognizer()
    photo_to_mood = MachineLoader.load(machines.photo_mood)
    TARGET_LABELS = ['Boat', 'Human', 'Insect', 'Invertebrate', 'Mammal', 'Man Made Scene', 'Outdoors', 'People Activity', 'Placental Mammal', 'Vertebrate']
    moods = Counter()
    matrix = vr.recognize(image_urls).to_matrix(TARGET_LABELS)
    for r in matrix:
        mood = photo_to_mood.predict(r)[0]
        moods[int(mood)] += 1

    target_mood = moods.most_common(1)[0][0]  # get top and its score
    target_mood = Echonest.MOOD[target_mood]

    return target_mood

def _make_result(mood, tracks, log=()):
    result = {
        "mood": mood,
        "tracks": [t.__dict__ for t in tracks],
        "log": log if log else {}
    }

    return result

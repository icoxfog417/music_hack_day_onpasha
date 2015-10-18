from application.photo2song_handler import BaseHandler
from collections import namedtuple
from api.echonest import Track
import api.photo2song as p2s


class DummyHandler(BaseHandler):

    def post(self):
        image_urls = self.get_image_urls()
        self.respond(image_urls)

    def get(self):
        image_urls = self.get_image_urls()
        self.respond(image_urls)

    def respond(self, image_urls=()):
        ims = image_urls
        if len(ims) == 0:
            ims = ["http://www.cavortinc.com/images/Conference%20program%20-%20Presentation%20of%20the%20play.JPG"]

        api = DummyAPI()
        result = {}
        try:
            mood = p2s.photo2mood(ims)
            tracks = api.sample(mood)
            result = p2s._make_result(mood, tracks)
            self.write(result)
        except Exception as ex:
            print(ex)

class DummyAPI():

    def __init__(self):
        pass

    def sample(self, mood):
        import random

        data = self.get_data()
        tracks = [d.track for d in data if d.mood == mood]
        return random.sample(tracks, 1)

    def get_data(self):
        LabeledTrack = namedtuple("LabeledTrack", ["mood", "track"])

        h1 = LabeledTrack("happy", Track("ハッピーハッピーターン", "ico", "000", "111", "", 0, preview_url="https://net.vocaloid.com/songs/85769/preview", images=[], track_url="https://net.vocaloid.com/songs/85769"))
        h2 = LabeledTrack("happy", Track("夏のサマーキック", "ico", "000", "111", "", 0, preview_url="https://net.vocaloid.com/songs/85771/preview", images=[], track_url="https://net.vocaloid.com/songs/85771"))
        h3 = LabeledTrack("happy", Track("ドキドキバイシクル", "ico", "000", "111", "", 0, preview_url="https://net.vocaloid.com/songs/85774/preview", images=[], track_url="https://net.vocaloid.com/songs/85774"))

        a1 = LabeledTrack("aggressive", Track("WOW WOW WOW", "ico", "000", "111", "", 0, preview_url="https://net.vocaloid.com/songs/85769/preview", images=[], track_url="https://net.vocaloid.com/songs/85769"))
        a2 = LabeledTrack("aggressive", Track("狼男の襲撃", "ico", "000", "111", "", 0, preview_url="https://net.vocaloid.com/songs/85771/preview", images=[], track_url="https://net.vocaloid.com/songs/85771"))
        a3 = LabeledTrack("aggressive", Track("夜露死苦", "ico", "000", "111", "", 0, preview_url="https://net.vocaloid.com/songs/85774/preview", images=[], track_url="https://net.vocaloid.com/songs/85774"))

        s1 = LabeledTrack("sentimental", Track("さよならエール", "ico", "000", "111", "", 0, preview_url="https://net.vocaloid.com/songs/85769/preview", images=[], track_url="https://net.vocaloid.com/songs/85769"))
        s2 = LabeledTrack("sentimental", Track("秋の夜長に", "ico", "000", "111", "", 0, preview_url="https://net.vocaloid.com/songs/85771/preview", images=[], track_url="https://net.vocaloid.com/songs/85771"))
        s3 = LabeledTrack("sentimental", Track("スノーパレード", "ico", "000", "111", "", 0, preview_url="https://net.vocaloid.com/songs/85774/preview", images=[], track_url="https://net.vocaloid.com/songs/85774"))

        c1 = LabeledTrack("cheerful", Track("元気100%", "ico", "000", "111", "", 0, preview_url="https://net.vocaloid.com/songs/85769/preview", images=[], track_url="https://net.vocaloid.com/songs/85769"))
        c2 = LabeledTrack("cheerful", Track("ぐるぐるコースター", "ico", "000", "111", "", 0, preview_url="https://net.vocaloid.com/songs/85771/preview", images=[], track_url="https://net.vocaloid.com/songs/85771"))
        c3 = LabeledTrack("cheerful", Track("スマイル・メリーゴーランド", "ico", "000", "111", "", 0, preview_url="https://net.vocaloid.com/songs/85774/preview", images=[], track_url="https://net.vocaloid.com/songs/85774"))

        return [
            h1, h2, h3,
            a1, a2, a3,
            s1, s2, s3,
            c1, c2, c3
        ]

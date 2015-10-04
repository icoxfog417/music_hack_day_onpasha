import unittest
from api.echonest import Echonest
from api.spotify import Spotify


class TestEchonest(unittest.TestCase):

    def test_get_tracks(self):
        e = Echonest()
        s = Spotify()
        tracks = e.search_songs("happy")
        self.assertTrue(len(tracks) > 0)
        for t in tracks:
            t.load_spotify(s)
            print("{0}/{1} {2}".format(t.title, t.artist_name, t.preview_url))

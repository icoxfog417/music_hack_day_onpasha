import unittest
from api.gracenote import Gracenote


class TestGracenote(unittest.TestCase):

    def test_search_songs(self):
        g = Gracenote()
        m = g.get_artists_mood_tracks(["星野源"], "Romantic")
        print(m)

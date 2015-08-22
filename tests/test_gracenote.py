import unittest
from api.gracenote import Gracenote


class TestGracenote(unittest.TestCase):

    def test_search_songs(self):
        g = Gracenote()
        m = g.get_mood_tracks("Romantic")
        print(m)

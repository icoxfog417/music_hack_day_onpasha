import unittest
from api.spotify import Spotify


class TestSpotify(unittest.TestCase):

    def test_get_track(self):
        s = Spotify()
        track = s.get_track("0eGsygTp906u18L0Oimnem")
        self.assertTrue("preview_url" in track)
        print(track)

import unittest
from api.livefans import LiveFans


class TestLivefans(unittest.TestCase):

    def test_get_artists(self):
        live = LiveFans()
        artists = live.get_live_artists()
        print(artists)

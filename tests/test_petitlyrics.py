import unittest
from api.petitlyrics import Petitlyrics


class TestPetitlyrics(unittest.TestCase):

    def test_track_to_lyric(self):
        p = Petitlyrics()
        ly = p.track_to_lyrics("夜空の太陽", limit=8)
        ly_0 = p.track_to_lyrics("夜空の太陽", limit=4)
        ly_1 = p.track_to_lyrics("夜空の太陽", offset=1, limit=4)
        ly_c = ly_0 + ly_1

        for l, r in zip(ly, ly_c):
            self.assertEqual(l, r)
        print(ly)

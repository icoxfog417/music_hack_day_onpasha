import unittest
from api.yamaha import Yamaha


class TestYamaha(unittest.TestCase):

    def test_create_xml(self):
        y = Yamaha()
        xml = y._create_xml(["song song", "no music no life"])
        print(xml.decode("utf-8"))

    def test_create_song(self):
        y = Yamaha()
        mp3_url = y.create_song(["春の歌"])
        self.assertTrue(mp3_url)
        print(mp3_url)

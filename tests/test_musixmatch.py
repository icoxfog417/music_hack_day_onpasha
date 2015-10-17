
import unittest
from api.musixmatch import MusixMatch


class TestMusixMatch(unittest.TestCase):

    def test_search_track(self):
        mx = MusixMatch()
        tracks = mx.search_track("Foo Fighters")
        self.assertTrue(len(tracks) > 0)
        print(tracks)

    def test_get_lyrics(self):
        mx = MusixMatch()
        lyrics = mx.match_track_and_lyrics("ニワカ雨ニモ負ケズ", lang="ja")
        self.assertTrue(len(lyrics) > 0)
        print(lyrics["lyrics_body"])
        self.assertTrue("柔よく剛を制しまして" in lyrics["lyrics_body"])

    def test_match_lyrics(self):
        mx = MusixMatch()
        lyrics = mx.match_lyrics("君の街まで", "ASIAN KUNG FU GENERATION")
        self.assertTrue(len(lyrics) > 0)
        print(lyrics["lyrics_body"])
        self.assertTrue("shining silver moon" in lyrics["lyrics_body"])


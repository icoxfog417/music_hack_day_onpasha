import unittest
import api.photo2song as p2s


class TestPhoto2Song(unittest.TestCase):

    def test_photo_to_song(self):
        image_urls = [
            "https://oxfordportal.blob.core.windows.net/vision/Thumbnail/1.jpg",
            "https://oxfordportal.blob.core.windows.net/vision/Thumbnail/4.jpg"
        ]
        result = p2s.convert(image_urls)
        self.assertTrue("results" in result)
        print(result)

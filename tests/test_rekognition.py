import unittest
from api.rekognition import Rekognition


class TestYamaha(unittest.TestCase):

    def test_images_to_mood(self):
        image_urls = ["https://oxfordportal.blob.core.windows.net/vision/Analysis/2-1.jpg"]
        r = Rekognition()
        moods = r.images_to_mood(image_urls)
        print(moods)

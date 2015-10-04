import unittest
from api.bluemix_vision_recognition import VisionRecognizer


class TestBluemixVisionRecognition(unittest.TestCase):

    def test_vision_recognize(self):
        vr = VisionRecognizer()
        labels = vr.recognize("http://visual-recognition-demo.mybluemix.net/images/73388.jpg")
        self.assertTrue(len(labels) > 0)
        print(labels)
        vlabels = vr.recognize("http://visual-recognition-demo.mybluemix.net/images/73388.jpg", "Animal")
        print(vlabels)
        self.assertTrue(len(labels["images"][0]["labels"]) > len(vlabels["images"][0]["labels"]))

    def test_get_labels(self):
        vr = VisionRecognizer()
        labels = vr.get_labels("Vehicle")
        self.assertTrue(len(labels) > 0)
        print(labels)

    def test_to_matrix(self):
        vr = VisionRecognizer()
        labels = vr.recognize("http://visual-recognition-demo.mybluemix.net/images/73388.jpg")
        matrix = VisionRecognizer.to_matrix(labels, ["Race Car", "Auto Track Racing"])
        self.assertEqual((1, 2), matrix.shape)
        print(matrix)

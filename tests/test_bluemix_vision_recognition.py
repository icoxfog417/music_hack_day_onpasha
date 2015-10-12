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
        self.assertTrue(len(labels[0]) > len(vlabels[0]))

    def test_vision_recognize_multi(self):
        vr = VisionRecognizer()
        urls = ["http://visual-recognition-demo.mybluemix.net/images/73388.jpg",
                "http://visual-recognition-demo.mybluemix.net/images/67528.jpg"]

        result = vr.recognize(urls)
        self.assertEqual(len(urls), len(result))

        targets = ["Windmill", "Auto Racing"]
        matrix = result.to_matrix(targets)
        self.assertEqual(result[0]["Windmill"], matrix[0][0])
        self.assertEqual(result[1]["Auto Racing"], matrix[1][1])
        self.assertEqual(0, matrix[0][1])
        self.assertEqual(0, matrix[1][0])

    def test_get_images(self):
        vr = VisionRecognizer()
        urls = ["http://visual-recognition-demo.mybluemix.net/images/73388.jpg",
                "http://visual-recognition-demo.mybluemix.net/images/67528.jpg"]

        fname, image = vr._get_images(urls, "imageFile.jpg")
        self.assertTrue("imageFile.zip", fname)
        self.assertTrue(isinstance(image, bytes))

    def test_get_labels(self):
        vr = VisionRecognizer()
        labels = vr.get_labels("Vehicle")
        self.assertTrue(len(labels) > 0)
        print(labels)

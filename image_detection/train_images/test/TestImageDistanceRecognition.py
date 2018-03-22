from unittest import TestCase
from unipath import Path

from image_detection.train_images.ImageDistanceRecognition import ImageDistanceRecognition


class TestImageDistanceRecognition(TestCase):

    def setUp(self):
        self.distance_recognition = ImageDistanceRecognition()

    def test_image_distance_desk(self):
        file_path = Path(Path(__file__).parent, 'test_plate.jpg')
        distance = self.distance_recognition.get_object_distance(file_path)
        self.assertEqual(distance, 0.6096, distance)
from unittest import TestCase, skip
from unipath import Path

from image_detection.train_images.ImageContentRecognition import ImageRecognition


class TestImageRecognition(TestCase):
    @skip
    def test_mouse_image_classification(self):
        recognition = ImageRecognition(Path(Path(__file__).parent, 'test_mouse.jpg'))
        classification = recognition.classify_image()
        self.assertTrue('computer mouse' in classification['value'],
                        msg=classification)

    @skip
    def test_desk_image_classification(self):
        recognition = ImageRecognition(Path(Path(__file__).parent, 'test_desk.jpg'))
        classification = recognition.classify_image()
        self.assertTrue('desk' in classification['value'],
                        msg=classification)
    @skip
    def test_plate_image_classification(self):
        recognition = ImageRecognition(Path(Path(__file__).parent, 'test_plate.jpg'))
        classification = recognition.classify_image()
        self.assertTrue('plate' in classification['value'],
                        msg=classification)

    def test_chair_image_classification(self):
        recognition = ImageRecognition(Path(Path(__file__).parent, 'test_chair.jpg'))
        classification = recognition.classify_image()
        self.assertTrue('chair' in classification['value'],
                        msg=classification)

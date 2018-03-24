import numpy as np
import cv2

# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 24.0

# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
KNOWN_WIDTH = 11.0


class ImageDistanceRecognition(object):

    def __init__(self):
        self.initial_local_length = None

    def get_object_distance(self, file_path):
        return self.calculate_distance(file_path)

    def find_marker(self, image):
        # convert the image to grayscale, blur it, and detect edges
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 35, 125)

        # find the contours in the edged image and keep the largest one;
        # we'll assume that this is our piece of paper in the image
        im2, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        c = max(contours, key=cv2.contourArea)

        # compute the bounding box of the of the paper region and return it
        return cv2.minAreaRect(c)

    def distance_to_camera(self, knownWidth, focalLength, perWidth):
        # compute and return the distance from the maker to the camera
        return (knownWidth * focalLength) / perWidth

    def calculate_distance(self, image_path):
        image = cv2.imread(image_path)
        return self.get_distance_object(image)

    def get_distance_object(self, image):
        marker = self.find_marker(image)
        if self.initial_local_length is None:
            self.initial_local_length = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
        per_width = marker[1][0]
        inches = self.distance_to_camera(KNOWN_WIDTH,
                                         self.initial_local_length,
                                         per_width)
        return {'meters': self.inches_to_meters(inches),
                'width': per_width,
                'marker': marker}

    def inches_to_meters(self, inches):
        feet = inches / 12.00
        meter = feet / 3.28084
        return meter

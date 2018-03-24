import numpy as np
import cv2
import pandas
import scipy
from unipath import Path
import threading

from image_detection.train_images.ImageContentRecognition import ImageRecognition
from image_detection.train_images.ImageDistanceRecognition import ImageDistanceRecognition

cap = cv2.VideoCapture(0)
count = 0
LABEL = None
filename = 'frame.jpg'
FRAME = None
EACH_TIME = 3.0
keep_update_label = True

class Label(object):
    def __init__(self):
        self.name = None
        self.frame = None
        self.keep_update_label = True


label_obj = Label()


def update_label():
    if label_obj.keep_update_label is True:
        recognition = ImageRecognition(Path(Path(__file__).parent, filename))
        cv2.imwrite(filename, label_obj.frame)
        classification = recognition.classify_image()
        label_obj.name = classification['value']
        threading.Timer(EACH_TIME, update_label).start()


# update_label()

image_distance = ImageDistanceRecognition()
image_objects = []
initiated = False
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    label_obj.frame = frame
    if initiated is False:
        update_label()
        initiated = True
    distance = image_distance.get_distance_object(frame)
    print(label_obj.name)
    print(distance)
    image_objects.append({
        'label': '{}'.format(label_obj.name),
        'meters_distance': distance['meters'],
        'proportion': distance['width']
    })
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    box = np.int0(cv2.boxPoints(distance['marker']))
    cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
    # Display the resulting frame
    frame = scipy.misc.imresize(frame, 1.2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        df = pandas.DataFrame(image_objects)
        df.to_csv('image_objects_data_frames.csv', index=False)
        break

    count += 1
# When everything done, release the capture
label_obj.keep_update_label = False
cap.release()

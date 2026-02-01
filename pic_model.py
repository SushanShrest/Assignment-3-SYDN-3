import cv2
import os

class PicModel:
    def __init__(self):
        self._presentValue = None
        self._filename = ""

    def load(self, path):
        img = cv2.imread(path)

        if img is None:
            print("Error: Image could not be loaded")
            return

        self._presentValue = img
        self._filename = os.path.basename(path)
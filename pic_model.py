import cv2
import os

class PicModel:
    def __init__(self):
        self._presentValue = None
        self._previousList = []
        self._redoList = []
        self._filename = ""

    def load(self, path):
        img = cv2.imread(path)

        if img is None:
            print("Error: Image could not be loaded")
            return

        self._presentValue = img
        self._filename = os.path.basename(path)

        # Save initial state for undo
        self._previousList = [img.copy()]
        self._redoList.clear()

    def getImg(self):
        return self._presentValue

    def addState(self):
        if self._presentValue is not None:
            self._previousList.append(self._presentValue.copy())
            self._redoList.clear()

    def undo(self):
        if len(self._previousList) > 1:
            self._redoList.append(self._previousList.pop())
            self._presentValue = self._previousList[-1].copy()
            return True
        return False

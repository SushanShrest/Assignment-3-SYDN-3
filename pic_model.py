import cv2
import os

class PicModel:
    def __init__(self):
        self._realValue = None
        self._presentValue = None
        self._previousList = [] 
        self._redoList = []
        self._filename = ""

    def getImg(self):
        return self._presentValue

    def setImg(self, val):
        self._presentValue = val

    def getRealImg(self):
        return self._realValue

    def getFileName(self):
        return self._filename

    def getDimension(self):
        if self._presentValue is not None:
            h, w = self._presentValue.shape[:2]
            return f"{w} x {h}"
        return "0 x 0"

    def load(self, path):
        img = cv2.imread(path)
        if img is None:
            raise ValueError("Cannot read image")
        
        self._realValue = img.copy()
        self._presentValue = img.copy()
        self._filename = os.path.basename(path)
        
        self._previousList = [img.copy()]
        self._redoList.clear()

    def save(self, path):
        if self._presentValue is not None:
            cv2.imwrite(path, self._presentValue)

    def addState(self):
        self._previousList.append(self._presentValue.copy())
        self._redoList.clear()
        if len(self._previousList) > 20:
            self._previousList.pop(0) 

    def undo(self):
        if len(self._previousList) > 1:
            self._redoList.append(self._previousList.pop())
            self._presentValue = self._previousList[-1].copy()
            return True
        return False

    def redo(self):
        if self._redoList:
            state = self._redoList.pop()
            self._previousList.append(state)
            self._presentValue = state.copy()
            return True
        return False
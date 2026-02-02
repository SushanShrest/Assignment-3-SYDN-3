import cv2
import os

# Creating class model for handling image data and undo/redo functionality
class PicModel:
    def __init__(self):
        self._realValue = None  #original pic
        self._presentValue = None #current pic
        self._previousList = [] # for Undo
        self._redoList = [] # for Redo
        self._filename = "" #file name

# Returning the current state of the image.
    def getImg(self):
        return self._presentValue
    
# Updating the current state of the image.
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
        # Loading image from disk and reset, undo,redo list
        img = cv2.imread(path)
        if img is None:
            raise ValueError("Cannot read image")
        
        self._realValue = img.copy()
        self._presentValue = img.copy()
        self._filename = os.path.basename(path)
        
        self._previousList = [img.copy()]
        self._redoList.clear()

    def save(self, path):
        # Saving current image to disk
        if self._presentValue is not None:
            cv2.imwrite(path, self._presentValue)

    def addState(self):
        # Adding current image to undo list
        if self._presentValue is None:
            return
        self._previousList.append(self._presentValue.copy())
        self._redoList.clear()
        if len(self._previousList) > 20:
            self._previousList.pop(0)

    def undo(self):
        # Reverting to previous image state
        if len(self._previousList) > 1:
            self._redoList.append(self._previousList.pop())
            self._presentValue = self._previousList[-1].copy()
            return True
        return False

    def redo(self):
        # Reapplying undone state
        if self._redoList:
            state = self._redoList.pop()
            self._previousList.append(state)
            self._presentValue = state.copy()
            return True
        return False
import cv2
from PIL import Image, ImageTk

class PicView:
    def __init__(self, picture, status_label):
        self.picture = picture
        self.status = status_label
        self.tkImage = None

    def display(self, img):
        if img is None:
            return
        
        rgbConvert = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        h, w = rgbConvert.shape[:2]
        ratio = min(400/w, 400/h)
        new_w, new_h = int(w * ratio), int(h * ratio)
        
        resizedImg = cv2.resize(rgbConvert, (new_w, new_h))
        
        self.tkImage = ImageTk.PhotoImage(Image.fromarray(resizedImg))
        self.picture.delete("all")
        self.picture.create_image(200, 200, image=self.tkImage)

    def updateStatus(self, filename, dimensions):
        self.status.config(text=f"  File: {filename}  |  Size: {dimensions}")

import cv2
from PIL import Image, ImageTk

# Handling displaying images and updating the status bar
class PicView:
    def __init__(self, picture, statusLabel):
        self.picture = picture # canvas for picture display
        self.status = statusLabel
        self.tkImage = None # keeping reference to Tk image

    def display(self, img):
        if img is None:
            return
        
        # Converting BGR to RGB for Tkinter
        rgbConvert = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resizing image to fit canvas
        h, w = rgbConvert.shape[:2]
        ratio = min(400/w, 400/h)
        new_w, new_h = int(w * ratio), int(h * ratio)
        
        resizedImg = cv2.resize(rgbConvert, (new_w, new_h))
        
        # Displaying image on canvas
        self.tkImage = ImageTk.PhotoImage(Image.fromarray(resizedImg))
        self.picture.delete("all")
        self.picture.create_image(200, 200, image=self.tkImage)

    def updateStatus(self, filename, dimensions):
        # Showing file info in status bar
        self.status.config(text=f"  File: {filename}  |  Size: {dimensions}")
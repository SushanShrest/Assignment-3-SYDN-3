import cv2
from PIL import Image, ImageTk

class PicView:
    def __init__(self, picture):
        self.picture = picture
        self.tkImage = None

    def display(self, img):
        if img is None:
            print("No image to display")
            return

        rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pilimg = Image.fromarray(rgbimg)

        self.tkImage = ImageTk.PhotoImage(pilimg)
        self.picture.create_image(200, 200, image=self.tkImage)
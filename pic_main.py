import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

from pic_model import PicModel
from pic_view import PicView

class PicEditor:

    def __init__(self, root):
        self.root = root
        self.root.title("SYDN-3 Photo Editor Assignment-3")
        self.root.geometry("900x650")

        self.model = PicModel()

        self.setup_gui()

    def setup_gui(self):
        self.canvas = tk.Canvas(self.root, width=500, height=400, bg="gray")
        self.canvas.pack()

        self.view = PicView(self.canvas)

        self.subMenu = tk.Frame(self.root)
        self.subMenu.pack(side=tk.RIGHT, fill=tk.Y)

        self.scaleSlider = tk.Scale(
            self.root,
            from_=10,
            to=200,
            orient=tk.HORIZONTAL,
            label="Resize %"
        )
        self.scaleSlider.set(100)
        self.scaleSlider.pack()

    def apply_grayscale(self):
        img = self.model.getImg()
        if img is None:
            return
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.filteredPic = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        self.view.display(self.filteredPic)

    def apply_edges(self):
        img = self.model.getImg()
        if img is None:
            return
        edges = cv2.Canny(img, 100, 200)
        self.filteredPic = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        self.view.display(self.filteredPic)

    def applyBlur(self, val):
        img = self.model.getImg()
        if img is None:
            return
        k = int(val) * 2 + 1
        self.filteredPic = cv2.GaussianBlur(img, (k, k), 0)
        self.view.display(self.filteredPic)

    def applyBrightness(self, val):
        img = self.model.getImg()
        if img is None:
            return
        val = int(val) * 10
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[..., 2] = np.clip(hsv[..., 2] + val, 0, 255)
        self.filteredPic = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        self.view.display(self.filteredPic)

    def applyContrast(self, val):
        img = self.model.getImg()
        if img is None:
            return
        alpha = 1 + int(val) / 10
        self.filteredPic = cv2.convertScaleAbs(img, alpha=alpha, beta=0)
        self.view.display(self.filteredPic)

    def applyResize(self):
        img = self.model.getImg()
        if img is None:
            return
        scale = self.scaleSlider.get()
        h, w = img.shape[:2]
        new_w, new_h = int(w * scale / 100), int(h * scale / 100)
        self.filteredPic = cv2.resize(img, (max(1, new_w), max(1, new_h)))
        self.view.display(self.filteredPic)


    def rotatePic(self, angle):
        img = self.model.getImg()
        if img is None:
            return
        codes = {
            90: cv2.ROTATE_90_CLOCKWISE,
            180: cv2.ROTATE_180,
            270: cv2.ROTATE_90_COUNTERCLOCKWISE
        }
        self.filteredPic = cv2.rotate(img, codes[angle])
        self.view.display(self.filteredPic)

    def flipPic(self, horizontal):
        img = self.model.getImg()
        if img is None:
            return
        self.filteredPic = cv2.flip(img, 1 if horizontal else 0)
        self.view.display(self.filteredPic)
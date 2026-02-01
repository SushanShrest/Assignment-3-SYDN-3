import tkinter as tk

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

 


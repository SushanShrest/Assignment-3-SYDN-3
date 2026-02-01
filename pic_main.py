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
        pass
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
        self.filteredPic = None 

        self.setup_gui()
        self.view = PicView(self.picture, self.statusbar)

    def setup_gui(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open", command=self.uploadAction)
        fileMenu.add_command(label="Save", command=self.saveAction)
        fileMenu.add_command(label="Save As", command=self.saveAsAction)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.exitAction)
        menubar.add_cascade(label="File", menu=fileMenu)

        editMenu = tk.Menu(menubar, tearoff=0)
        editMenu.add_command(label="Undo", command=self.undoAction)
        editMenu.add_command(label="Redo", command=self.redoAction)
        menubar.add_cascade(label="Edit", menu=editMenu)

        header = tk.Frame(self.root)
        header.pack(pady=10)
        tk.Label(header, text="SYDN-03 PhotoEditior", font=("Arial", 18)).pack()

        body = tk.Frame(self.root)
        body.pack(expand=True, fill="both", padx=10)

        self.menu_frame = tk.Frame(body, bd=2, relief="ridge")
        self.menu_frame.pack(side="left", fill="y", pady=50, padx=10)

        tk.Button(self.menu_frame, text="Filters", command=self.filterMenu, width=15).pack(fill="x", pady=5, padx=10)
        tk.Button(self.menu_frame, text="Adjustments", command=self.adjustMenu, width=15).pack(fill="x", pady=5, padx=10)
        tk.Button(self.menu_frame, text="Transform", command=self.transformMenu, width=15).pack(fill="x", pady=5, padx=10)

        canvas_container = tk.Frame(body)
        canvas_container.pack(side="left", expand=True, padx=10)

        self.picture = tk.Canvas(canvas_container, width=400, height=400, bg="gray")
        self.picture.pack(expand=True, padx=10, pady=25)

        confirm_box = tk.Frame(canvas_container, bd=2, relief="groove")
        confirm_box.pack(anchor="center", padx=5, pady=5)
        tk.Label(confirm_box, text="Press apply to save changes", font=("Arial", 10)).pack(pady=(5, 5), padx=5)

        btnContainer = tk.Frame(confirm_box)
        btnContainer.pack(pady=5)
        tk.Button(btnContainer, text="Apply", command=self.applyAction, width=10).pack(side="left", padx=10, pady=5)
        tk.Button(btnContainer, text="Revert All", command=self.revertAction, width=10).pack(side="left", padx=10, pady=5)

        self.subMenu = tk.Frame(body, bd=2, relief="groove", width=150)
        self.subMenu.pack(side="right", fill="y", pady=50, padx=10)

        self.statusbar = tk.Label(self.root, text="  No file", bd=1, relief="sunken", anchor="w")
        self.statusbar.pack(side="bottom", fill="x")

    def uploadAction(self):
        filename = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp"), ("All", "*.*")])
        if filename:
            try:
                self.model.load(filename)
                self.filteredPic = self.model.getImg().copy()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Error", f"Cannot open image:\n{e}")

    def refresh(self):
        self.view.display(self.model.getImg())
        self.view.updateStatus(self.model.getFileName(), self.model.getDimension())

    def applyAction(self):
        if self.filteredPic is not None:
            self.model.setImg(self.filteredPic.copy())
            self.model.addState() 
            self.refresh()

    def revertAction(self):
        if self.model.getRealImg() is not None:
            confirm = messagebox.askyesno("Confirm", "Reset all changes?")
            if confirm:
                original = self.model.getRealImg().copy()
                self.model.setImg(original)
                self.filteredPic = original.copy()
                self.model.addState()
                self.refresh()

    def saveAction(self):
        if self.model.getImg() is not None and self.model.getFileName():
            self.model.save(self.model.getFileName())
            messagebox.showinfo("Saved", "Success!")
        else:
            self.saveAsAction()

    def saveAsAction(self):
        if self.model.getImg() is None:
            messagebox.showwarning("Warning", "Nothing to save!")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")])
        if filename:
            self.model.save(filename)

    def exitAction(self):
        if messagebox.askokcancel("Exit", "Close the app?"):
            self.root.quit()

    def undoAction(self):
        if self.model.undo():
            self.filteredPic = self.model.getImg().copy()
            self.refresh()

    def redoAction(self):
        if self.model.redo():
            self.filteredPic = self.model.getImg().copy()
            self.refresh()

    def filterMenu(self):
        for w in self.subMenu.winfo_children():
            w.destroy()
        tk.Label(self.subMenu, text="Filters", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Button(self.subMenu, text="Grayscale", command=self.apply_grayscale, width=15).pack(pady=2)
        tk.Button(self.subMenu, text="Edge Detection", command=self.apply_edges, width=15).pack(pady=2)

    def apply_grayscale(self):
        img = self.model.getImg()
        if img is None: return
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.filteredPic = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        self.view.display(self.filteredPic)

    def apply_edges(self):
        img = self.model.getImg()
        if img is None: return
        edges = cv2.Canny(img, 100, 200)
        self.filteredPic = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        self.view.display(self.filteredPic)

    def adjustMenu(self):
        for w in self.subMenu.winfo_children():
            w.destroy()
        tk.Label(self.subMenu, text="Adjustments", font=("Arial", 10, "bold")).pack(pady=5)

        tk.Label(self.subMenu, text="Blur").pack()
        self.blurScale = tk.Scale(self.subMenu, from_=1, to=10, orient="horizontal", command=self.applyBlur)
        self.blurScale.pack(fill="x")

        tk.Label(self.subMenu, text="Brightness").pack()
        self.brightScale = tk.Scale(self.subMenu, from_=-10, to=10, orient="horizontal", command=self.applyBrightness)
        self.brightScale.pack(fill="x")

        tk.Label(self.subMenu, text="Contrast").pack()
        self.contrastScale = tk.Scale(self.subMenu, from_=-10, to=10, orient="horizontal", command=self.applyContrast)
        self.contrastScale.pack(fill="x")

        tk.Label(self.subMenu, text="Scale %").pack()
        self.scaleSlider = tk.Scale(self.subMenu, from_=10, to=200, orient="horizontal")
        self.scaleSlider.set(100)
        self.scaleSlider.pack(fill="x")
        tk.Button(self.subMenu, text="Resize", command=self.applyResize, width=15).pack(pady=10)

    def applyBlur(self, val):
        img = self.model.getImg()
        if img is None: return
        k = int(val) * 2 + 1
        self.filteredPic = cv2.GaussianBlur(img, (k, k), 0)
        self.view.display(self.filteredPic)

    def applyBrightness(self, val):
        img = self.model.getImg()
        if img is None: return
        val = int(val) * 10
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[..., 2] = np.clip(hsv[..., 2] + val, 0, 255) 
        self.filteredPic = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        self.view.display(self.filteredPic)

    def applyContrast(self, val):
        img = self.model.getImg()
        if img is None: return
        alpha = 1 + int(val) / 10 
        self.filteredPic = cv2.convertScaleAbs(img, alpha=alpha, beta=0)
        self.view.display(self.filteredPic)

    def applyResize(self):
        img = self.model.getImg()
        if img is None: return
        scale = self.scaleSlider.get()
        h, w = img.shape[:2]
        new_w, new_h = int(w * scale / 100), int(h * scale / 100)
        self.filteredPic = cv2.resize(img, (max(1, new_w), max(1, new_h)))
        self.view.display(self.filteredPic)

    def transformMenu(self):
        for w in self.subMenu.winfo_children():
            w.destroy()
        tk.Label(self.subMenu, text="Transform", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Button(self.subMenu, text="Rotate 90°", command=lambda: self.rotatePic(90), width=15).pack(pady=2)
        tk.Button(self.subMenu, text="Rotate 180°", command=lambda: self.rotatePic(180), width=15).pack(pady=2)
        tk.Button(self.subMenu, text="Flip Horizontal", command=lambda: self.flipPic(True), width=15).pack(pady=2)
        tk.Button(self.subMenu, text="Flip Vertical", command=lambda: self.flipPic(False), width=15).pack(pady=2)

    def rotatePic(self, angle):
        img = self.model.getImg()
        if img is None: return
        codes = {90: cv2.ROTATE_90_CLOCKWISE, 180: cv2.ROTATE_180, 270: cv2.ROTATE_90_COUNTERCLOCKWISE}
        self.filteredPic = cv2.rotate(img, codes[angle])
        self.view.display(self.filteredPic)

    def flipPic(self, horizontal):
        img = self.model.getImg()
        if img is None: return
        self.filteredPic = cv2.flip(img, 1 if horizontal else 0)
        self.view.display(self.filteredPic)

if __name__ == "__main__":
    root = tk.Tk()
    editor = PicEditor(root)
    root.mainloop()

git

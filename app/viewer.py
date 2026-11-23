"""Panel canvas: menampilkan citra dan memetakan koordinat mouse ke piksel."""
import tkinter as tk

import cv2
from PIL import Image, ImageTk


class ImageViewer:
    """Satu canvas citra. Menyimpan skala tampil untuk konversi koordinat."""

    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.display_scale = 1.0
        self._tk_image = None  # referensi wajib agar gambar tidak hilang oleh GC

    def render(self, cv_img):
        """Gambar citra BGR ke canvas, diskalakan agar muat (tidak diperbesar)."""
        self.canvas.update_idletasks()
        cw = max(self.canvas.winfo_width(), 420)
        ch = max(self.canvas.winfo_height(), 360)

        img_h, img_w = cv_img.shape[:2]
        scale = min((cw - 16) / img_w, (ch - 16) / img_h, 1.0)
        self.display_scale = scale

        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        resized = cv2.resize(cv_img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        self._tk_image = ImageTk.PhotoImage(Image.fromarray(rgb))

        self.canvas.delete("all")
        self.canvas.create_image(cw // 2, ch // 2, image=self._tk_image, anchor=tk.CENTER)

    def canvas_to_image_coords(self, event, image_shape):
        """Petakan posisi mouse ke koordinat piksel citra; None jika di luar area."""
        img_h, img_w = image_shape[:2]
        disp_w = int(img_w * self.display_scale)
        disp_h = int(img_h * self.display_scale)
        offset_x = (self.canvas.winfo_width() - disp_w) // 2
        offset_y = (self.canvas.winfo_height() - disp_h) // 2

        ix = int((event.x - offset_x) / self.display_scale)
        iy = int((event.y - offset_y) / self.display_scale)
        if 0 <= ix < img_w and 0 <= iy < img_h:
            return (ix, iy)
        return None

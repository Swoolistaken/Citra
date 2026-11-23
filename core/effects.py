"""Bab 7 - Citra Berwarna dan Efek, modul Rinaldi Munir."""
import cv2
import numpy as np


def sepia_filter(image):
    """Transformasi Matriks Warna efek Retro / Sepia."""
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    sepia = cv2.transform(image, kernel)
    return np.clip(sepia, 0, 255).astype(np.uint8)


def edge_sketch(image):
    """Efek Sketsa Pensil menggunakan pembagian intensitas citra inversi blur."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256.0)
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

"""Bab 3 - Konvolusi dan Penapisan Spasial, modul Rinaldi Munir."""
import cv2
import numpy as np


def gaussian_blur(image, ksize=9):
    """Penapis Lolos-Rendah (Low-Pass / Smoothing) Gaussian."""
    if ksize % 2 == 0:
        ksize += 1
    return cv2.GaussianBlur(image, (ksize, ksize), 0)


def median_filter(image, ksize=5):
    """Penapis Non-Linier: Median Filter untuk meredam noise salt-and-pepper."""
    return cv2.medianBlur(image, ksize)


def sharpen(image):
    """Penapis Lolos-Tinggi (High-Pass / Sharpening) menggunakan Kernel Konvolusi."""
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]], dtype=np.float32)
    return cv2.filter2D(image, -1, kernel)

"""Bab 5 - Operasi Morfologi, modul Rinaldi Munir."""
import cv2
import numpy as np


def morph_dilation(image, ksize=5):
    """Morfologi: Dilasi (Menebalkan area terang)."""
    kernel = np.ones((ksize, ksize), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


def morph_erosion(image, ksize=5):
    """Morfologi: Erosi (Menipiskan area terang)."""
    kernel = np.ones((ksize, ksize), np.uint8)
    return cv2.erode(image, kernel, iterations=1)

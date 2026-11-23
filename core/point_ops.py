"""Bab 1 - Operasi Titik (Point Operations), modul Rinaldi Munir."""
import cv2
import numpy as np


def image_negative(image):
    """Operasi Titik: Citra Negatif (s = 255 - r)."""
    return 255 - image


def contrast_stretching(image):
    """Operasi Titik: Peregangan Kontras (Min-Max Normalization)."""
    result = np.zeros_like(image)
    for c in range(3):
        r_min = np.min(image[:, :, c])
        r_max = np.max(image[:, :, c])
        if r_max > r_min:
            result[:, :, c] = ((image[:, :, c] - r_min) / (r_max - r_min) * 255).astype(np.uint8)
        else:
            result[:, :, c] = image[:, :, c]
    return result


def binary_threshold(image, thresh_val=128):
    """Operasi Titik: Pengambangan (Thresholding) menjadi citra biner."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

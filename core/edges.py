"""Bab 4 - Pendeteksian Tepi (Edge Detection), modul Rinaldi Munir."""
import cv2
import numpy as np


def sobel_edge(image):
    """Deteksi Tepi Orde-1: Operator Gradien Sobel (Gx & Gy)."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = np.sqrt(gx**2 + gy**2)
    sobel = np.clip(magnitude, 0, 255).astype(np.uint8)
    return cv2.cvtColor(sobel, cv2.COLOR_GRAY2BGR)


def canny_edge(image):
    """Deteksi Tepi Multi-Tahap: Operator Canny."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 180)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

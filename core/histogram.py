"""Bab 2 - Histogram Citra, modul Rinaldi Munir."""
import cv2


def auto_contrast(image):
    """Perataan Histogram (Histogram Equalization) pada kanal pencahayaan Y (YCrCb)."""
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    channels = list(cv2.split(ycrcb))
    channels[0] = cv2.equalizeHist(channels[0])
    merged = cv2.merge(channels)
    return cv2.cvtColor(merged, cv2.COLOR_YCrCb2BGR)


def clahe_enhance(image, clip_limit=2.0):
    """Adaptive Histogram Equalization (CLAHE) pada ruang warna LAB."""
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    merged = cv2.merge((cl, a, b))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def compute_rgb_histograms(image):
    """Menghitung distribusi intensitas piksel (0-255) untuk kanal B, G, R."""
    hists = {}
    for idx, col in enumerate(('b', 'g', 'r')):
        hist = cv2.calcHist([image], [idx], None, [256], [0, 256]).flatten()
        hists[col] = hist
    return hists

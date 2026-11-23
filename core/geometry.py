"""Bab 6 - Operasi Geometri, modul Rinaldi Munir."""
import cv2


def flip_horizontal(image):
    """Geometri: Pencerminan Horizontal (Mirroring)."""
    return cv2.flip(image, 1)


def rotate_90_cw(image):
    """Geometri: Rotasi 90 Derajat Searah Jarum Jam."""
    return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

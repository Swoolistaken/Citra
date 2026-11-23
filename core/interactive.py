"""Fitur interaktif ala Photoshop: Magic Wand dan Object Eraser."""
import cv2
import numpy as np


def magic_wand_remove_bg(image, seed_point, tolerance=30):
    """Segmentasi warna berbasis ruang warna HSV (Magic Wand) + Morfologi Closing.

    Mengembalikan (citra hasil, mask area terseleksi).
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    x, y = seed_point
    target_color = hsv[y, x].astype(int)

    lower = np.clip(target_color - tolerance, 0, 255).astype(np.uint8)
    upper = np.clip(target_color + tolerance, 0, 255).astype(np.uint8)
    lower[0] = max(0, target_color[0] - int(tolerance * 0.6))
    upper[0] = min(179, target_color[0] + int(tolerance * 0.6))

    mask = cv2.inRange(hsv, lower, upper)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    result = image.copy()
    h, w = image.shape[:2]
    checker = np.zeros((h, w, 3), dtype=np.uint8)
    checker[:] = (220, 220, 220)
    for i in range(0, h, 16):
        for j in range(0, w, 16):
            if (i // 16 + j // 16) % 2 == 0:
                checker[i:i+16, j:j+16] = (255, 255, 255)

    result[mask > 0] = checker[mask > 0]
    return result, mask


def inpaint_erase(image, mask):
    """Object Eraser menggunakan algoritma Inpainting Fast Marching (Telea)."""
    return cv2.inpaint(image, mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA)

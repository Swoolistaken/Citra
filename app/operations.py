"""Katalog operasi sidebar.

Cara menambah fitur baru:
1. Tulis fungsi murni di modul core yang sesuai (atau buat modul core baru).
2. Tambahkan satu tupel (label, fungsi) pada bagian yang sesuai di SECTIONS.
3. Tambahkan smoke test di tests/test_core.py.
Sidebar dibangun otomatis dari katalog ini, tidak perlu mengubah window.py.
"""
from core import edges, effects, filters, geometry, histogram, morphology, point_ops

SECTIONS = [
    ("1. OPERASI TITIK (POINT OPS)", [
        ("Citra Negatif (Invert)", point_ops.image_negative),
        ("Contrast Stretching", point_ops.contrast_stretching),
        ("Binary Thresholding", point_ops.binary_threshold),
    ]),
    ("2. HISTOGRAM CITRA", [
        ("Histogram Equalization", histogram.auto_contrast),
        ("CLAHE (Adaptive Hist.)", histogram.clahe_enhance),
    ]),
    ("3. KONVOLUSI & PENAPISAN", [
        ("Gaussian Blur (Low-Pass)", filters.gaussian_blur),
        ("Median Filter (Denoising)", filters.median_filter),
        ("Sharpen (High-Pass)", filters.sharpen),
    ]),
    ("4. PENDETEKSIAN TEPI (EDGE)", [
        ("Operator Sobel (Gradien)", edges.sobel_edge),
        ("Operator Canny", edges.canny_edge),
    ]),
    ("5. OPERASI MORFOLOGI", [
        ("Dilasi (Tebalkan Terang)", morphology.morph_dilation),
        ("Erosi (Tipiskan Terang)", morphology.morph_erosion),
    ]),
    ("6. OPERASI GEOMETRI", [
        ("Flip Horizontal (Cermin)", geometry.flip_horizontal),
        ("Rotate 90 Searah Jarum Jam", geometry.rotate_90_cw),
    ]),
    ("7. EFEK & CITRA BERWARNA", [
        ("Retro Sepia Filter", effects.sepia_filter),
        ("Pencil Sketch", effects.edge_sketch),
    ]),
]

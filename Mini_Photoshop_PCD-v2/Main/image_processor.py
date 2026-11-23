import cv2
import numpy as np

class ImageProcessor:
    # =================================================================
    # 1. OPERASI TITIK (POINT OPERATIONS) - MODUL RINALDI MUNIR
    # =================================================================
    @staticmethod
    def image_negative(image):
        """Operasi Titik: Citra Negatif (s = 255 - r)."""
        return 255 - image

    @staticmethod
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

    @staticmethod
    def binary_threshold(image, thresh_val=128):
        """Operasi Titik: Pengambangan (Thresholding) menjadi citra biner."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
        return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

    # =================================================================
    # 2. HISTOGRAM CITRA - MODUL RINALDI MUNIR
    # =================================================================
    @staticmethod
    def auto_contrast(image):
        """Perataan Histogram (Histogram Equalization) pada kanal pencahayaan Y (YCrCb)."""
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        channels = list(cv2.split(ycrcb))
        channels[0] = cv2.equalizeHist(channels[0])
        merged = cv2.merge(channels)
        return cv2.cvtColor(merged, cv2.COLOR_YCrCb2BGR)

    @staticmethod
    def clahe_enhance(image, clip_limit=2.0):
        """Adaptive Histogram Equalization (CLAHE) pada ruang warna LAB."""
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        merged = cv2.merge((cl, a, b))
        return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

    # =================================================================
    # 3. KONVOLUSI & PENAPISAN SPASIAL - MODUL RINALDI MUNIR
    # =================================================================
    @staticmethod
    def gaussian_blur(image, ksize=9):
        """Penapis Lolos-Rendah (Low-Pass / Smoothing) Gaussian."""
        if ksize % 2 == 0:
            ksize += 1
        return cv2.GaussianBlur(image, (ksize, ksize), 0)

    @staticmethod
    def median_filter(image, ksize=5):
        """Penapis Non-Linier: Median Filter untuk meredam noise salt-and-pepper."""
        return cv2.medianBlur(image, ksize)

    @staticmethod
    def sharpen(image):
        """Penapis Lolos-Tinggi (High-Pass / Sharpening) menggunakan Kernel Konvolusi."""
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]], dtype=np.float32)
        return cv2.filter2D(image, -1, kernel)

    # =================================================================
    # 4. PENDETEKSIAN TEPI (EDGE DETECTION) - MODUL RINALDI MUNIR
    # =================================================================
    @staticmethod
    def sobel_edge(image):
        """Deteksi Tepi Orde-1: Operator Gradien Sobel (Gx & Gy)."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(gx**2 + gy**2)
        sobel = np.clip(magnitude, 0, 255).astype(np.uint8)
        return cv2.cvtColor(sobel, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def canny_edge(image):
        """Deteksi Tepi Multi-Tahap: Operator Canny."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 80, 180)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # =================================================================
    # 5. OPERASI MORFOLOGI - MODUL RINALDI MUNIR
    # =================================================================
    @staticmethod
    def morph_dilation(image, ksize=5):
        """Morfologi: Dilasi (Menebalkan area terang)."""
        kernel = np.ones((ksize, ksize), np.uint8)
        return cv2.dilate(image, kernel, iterations=1)

    @staticmethod
    def morph_erosion(image, ksize=5):
        """Morfologi: Erosi (Menipiskan area terang)."""
        kernel = np.ones((ksize, ksize), np.uint8)
        return cv2.erode(image, kernel, iterations=1)

    # =================================================================
    # 6. OPERASI GEOMETRI - MODUL RINALDI MUNIR
    # =================================================================
    @staticmethod
    def flip_horizontal(image):
        """Geometri: Pencerminan Horizontal (Mirroring)."""
        return cv2.flip(image, 1)

    @staticmethod
    def rotate_90_cw(image):
        """Geometri: Rotasi 90 Derajat Searah Jarum Jam."""
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    # =================================================================
    # 7. CITRA BERWARNA & FITUR INTERAKTIF ALA PHOTOSHOP
    # =================================================================
    @staticmethod
    def sepia_filter(image):
        """Transformasi Matriks Warna efek Retro / Sepia."""
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia = cv2.transform(image, kernel)
        return np.clip(sepia, 0, 255).astype(np.uint8)

    @staticmethod
    def edge_sketch(image):
        """Efek Sketsa Pensil menggunakan pembagian intensitas citra inversi blur."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blur, scale=256.0)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def magic_wand_remove_bg(image, seed_point, tolerance=30):
        """Segmentasi warna berbasis ruang warna HSV (Magic Wand) + Morfologi Closing."""
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

    @staticmethod
    def inpaint_erase(image, mask):
        """Object Eraser menggunakan algoritma Inpainting Fast Marching (Telea)."""
        return cv2.inpaint(image, mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA)

    @staticmethod
    def compute_rgb_histograms(image):
        """Menghitung distribusi intensitas piksel (0-255) untuk kanal B, G, R."""
        hists = {}
        for idx, col in enumerate(('b', 'g', 'r')):
            hist = cv2.calcHist([image], [idx], None, [256], [0, 256]).flatten()
            hists[col] = hist
        return hists
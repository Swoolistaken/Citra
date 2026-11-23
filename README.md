# Mini Photoshop - Proyek Pengolahan Citra Digital (Modul Rinaldi Munir)

Aplikasi editor citra berbasis Python (Tkinter + OpenCV + NumPy) yang mengimplementasikan 7 bab utama Pengolahan Citra Digital berdasarkan modul Rinaldi Munir:

1. **Operasi Titik**: Citra Negatif, Contrast Stretching, Binary Thresholding
2. **Histogram Citra**: Histogram Equalization & CLAHE
3. **Konvolusi & Penapisan Spasial**: Gaussian Blur (Low-Pass), Median Filter (Non-Linier), Sharpening (High-Pass)
4. **Pendeteksian Tepi**: Operator Gradien Sobel & Canny
5. **Operasi Morfologi**: Dilasi & Erosi
6. **Operasi Geometri**: Flip Horizontal & Rotasi 90 derajat
7. **Citra Berwarna & Fitur Interaktif**: Magic Wand (Segmentasi HSV) & Object Eraser (Inpainting Telea)

## Cara Menjalankan

1. Buat virtual environment dan install library:
   ```
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
2. Jalankan aplikasi dari root repositori:
   ```
   .\.venv\Scripts\python.exe main.py
   ```

Catatan: di Windows, gunakan `py` jika perintah `python` tidak tersedia.

## Struktur Proyek

- `core/`: fungsi pengolahan citra murni, satu modul per bab, tanpa GUI.
- `app/`: antarmuka Tkinter (state, viewer, panel histogram, katalog operasi).
- `tests/`: smoke test pytest.
- `docs/`: dokumentasi dan jurnal keputusan.

## Menambah Fitur Baru

1. Tulis fungsi murni di modul `core/` yang sesuai (BGR uint8 masuk dan keluar).
2. Tambahkan satu tupel `(label, fungsi)` di `app/operations.py`. Sidebar terbentuk otomatis dari katalog ini.
3. Tambahkan test di `tests/test_core.py`.

## Test

```
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest tests -q
```

Panduan kontribusi dan aturan kode: lihat `AGENTS.md`.

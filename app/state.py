"""State editor: citra asli, citra saat ini, dan riwayat undo. Tanpa GUI."""
import cv2

HISTORY_LIMIT = 15


class EditorState:
    """Menyimpan data citra dan riwayat operasi. Tidak tahu-menahu soal UI."""

    def __init__(self):
        self.original_image = None
        self.current_image = None
        self.history = []

    def load(self, path):
        """Muat citra dari berkas; menjadi citra asli sekaligus citra saat ini."""
        img = cv2.imread(path)
        if img is None:
            raise ValueError("Gagal memuat gambar.")
        self.original_image = img.copy()
        self.current_image = img.copy()
        self.history = []

    def push_history(self):
        """Simpan salinan citra saat ini ke riwayat (maksimal HISTORY_LIMIT)."""
        if self.current_image is not None:
            self.history.append(self.current_image.copy())
            if len(self.history) > HISTORY_LIMIT:
                self.history.pop(0)

    def apply(self, func):
        """Terapkan fungsi pengolahan core ke citra saat ini. True jika berhasil."""
        if self.current_image is None:
            return False
        self.push_history()
        self.current_image = func(self.current_image)
        return True

    def undo(self):
        """Kembalikan citra satu langkah. True jika ada riwayat."""
        if not self.history:
            return False
        self.current_image = self.history.pop()
        return True

    def reset(self):
        """Kembalikan citra ke kondisi asli (tetap bisa di-undo). True jika berhasil."""
        if self.original_image is None:
            return False
        self.push_history()
        self.current_image = self.original_image.copy()
        return True

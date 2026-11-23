"""Titik masuk aplikasi Mini Photoshop (Pengolahan Citra Digital)."""
import ctypes
import sys
import tkinter as tk

from app.window import MiniPhotoshopApp


def _enable_dpi_awareness():
    """Cegah Windows melakukan bitmap scaling agar UI tajam di layar HiDPI."""
    if sys.platform != "win32":
        return
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # system DPI aware
    except (AttributeError, OSError):
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except (AttributeError, OSError):
            pass


def main():
    _enable_dpi_awareness()
    root = tk.Tk()
    MiniPhotoshopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

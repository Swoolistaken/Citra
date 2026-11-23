"""Titik masuk aplikasi Mini Photoshop (Pengolahan Citra Digital)."""
import tkinter as tk

from app.window import MiniPhotoshopApp


def main():
    root = tk.Tk()
    MiniPhotoshopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

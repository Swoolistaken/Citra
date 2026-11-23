"""Jendela utama: tata letak, toolbar, sidebar, dan interaksi tool mouse."""
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
import numpy as np

from app import operations
from app.histogram_panel import HistogramPanel
from app.state import EditorState
from app.viewer import ImageViewer
from core.interactive import inpaint_erase, magic_wand_remove_bg


def _work_area(root):
    """Area kerja layar (tanpa taskbar) dalam piksel fisik."""
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes

        rect = wintypes.RECT()
        if ctypes.windll.user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(rect), 0):
            return rect.right - rect.left, rect.bottom - rect.top
    return root.winfo_screenwidth(), root.winfo_screenheight()


class MiniPhotoshopApp:
    """Merakit state + viewer + panel histogram, dan menangani event UI."""

    def __init__(self, root):
        self.root = root
        self.root.title("Mini Photoshop - Before/After & Histogram Analisis (Rinaldi Munir)")
        self.root.configure(bg="#2b2b2b")

        # Skala UI mengikuti DPI layar agar tajam dan proporsional (HiDPI).
        self.ui_scale = self.root.winfo_fpixels("1i") / 96.0
        max_w, max_h = _work_area(self.root)
        width = min(int(1280 * self.ui_scale), max_w)
        height = min(int(820 * self.ui_scale), max_h)
        self.root.geometry(f"{width}x{height}")

        self.state = EditorState()
        self.tool_mode = "none"
        self.eraser_mask = None
        self.last_x, self.last_y = None, None

        self._build_ui()

        try:
            self.load_image("sample_image.jpg")
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Tata letak
    # ------------------------------------------------------------------
    def _build_ui(self):
        # Top Toolbar
        topbar = tk.Frame(self.root, bg="#1e1e1e", height=45)
        topbar.pack(side=tk.TOP, fill=tk.X)

        btn_style = {"bg": "#3c3f41", "fg": "white", "relief": tk.FLAT,
                     "padx": 12, "pady": 6, "font": ("Segoe UI", 9, "bold")}
        tk.Button(topbar, text="Buka Gambar", command=self.open_file, **btn_style).pack(side=tk.LEFT, padx=6, pady=6)
        tk.Button(topbar, text="Simpan Hasil (After)", command=self.save_file, **btn_style).pack(side=tk.LEFT, padx=6, pady=6)
        tk.Button(topbar, text="Undo", command=self.undo, **btn_style).pack(side=tk.LEFT, padx=6, pady=6)
        tk.Button(topbar, text="Reset Asli", command=self.reset_image, **btn_style).pack(side=tk.LEFT, padx=6, pady=6)

        self.status_label = tk.Label(topbar, text="Mode: Normal", bg="#1e1e1e", fg="#a9b7c6", font=("Segoe UI", 9))
        self.status_label.pack(side=tk.RIGHT, padx=15)

        # Main Container
        main_frame = tk.Frame(self.root, bg="#2b2b2b")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._build_sidebar(main_frame)
        self._build_workspace(main_frame)

    def _build_sidebar(self, parent):
        """Sidebar kiri yang bisa di-scroll, dibangun dari katalog operasi."""
        sidebar_container = tk.Frame(parent, bg="#313335", width=int(270 * self.ui_scale))
        sidebar_container.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        sidebar_container.pack_propagate(False)

        sb_canvas = tk.Canvas(sidebar_container, bg="#313335", highlightthickness=0)
        scrollbar = tk.Scrollbar(sidebar_container, orient="vertical", command=sb_canvas.yview)
        sidebar = tk.Frame(sb_canvas, bg="#313335")

        sidebar.bind("<Configure>", lambda e: sb_canvas.configure(scrollregion=sb_canvas.bbox("all")))
        sb_canvas.create_window((0, 0), window=sidebar, anchor="nw", width=int(250 * self.ui_scale))
        sb_canvas.configure(yscrollcommand=scrollbar.set)

        sb_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def _on_mousewheel(event):
            sb_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        sb_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def add_section(title):
            lbl = tk.Label(sidebar, text=title, bg="#313335", fg="#6897bb",
                           font=("Segoe UI", 8, "bold"), anchor="w")
            lbl.pack(fill=tk.X, padx=10, pady=(10, 3))

        tool_btn = {"bg": "#4b6eaf", "fg": "white", "relief": tk.FLAT, "pady": 5, "font": ("Segoe UI", 9)}
        filter_btn = {"bg": "#3c3f41", "fg": "white", "relief": tk.FLAT, "pady": 4, "font": ("Segoe UI", 9)}

        add_section("INTERACTIVE TOOLS (KLIK DI AFTER)")
        tk.Button(sidebar, text="Magic Wand (HSV Segment)", command=self.activate_magic_wand, **tool_btn).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(sidebar, text="Object Eraser (Inpainting)", command=self.activate_eraser, **tool_btn).pack(fill=tk.X, padx=10, pady=2)

        for title, entries in operations.SECTIONS:
            add_section(title)
            for label, func in entries:
                tk.Button(sidebar, text=label, command=lambda f=func: self.apply_filter(f),
                          **filter_btn).pack(fill=tk.X, padx=10, pady=2)

        tk.Frame(sidebar, bg="#313335", height=int(13 * self.ui_scale)).pack(fill=tk.X)

    def _build_workspace(self, parent):
        """Workspace kanan: panel before/after di atas, grafik histogram di bawah."""
        workspace = tk.Frame(parent, bg="#2b2b2b")
        workspace.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        images_panel = tk.Frame(workspace, bg="#2b2b2b")
        images_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        before_box = tk.Frame(images_panel, bg="#1e1e1e", bd=1, relief=tk.SOLID)
        before_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))
        tk.Label(before_box, text="BEFORE (Citra Asli)", bg="#252526", fg="#cccccc",
                 font=("Segoe UI", 9, "bold"), pady=4).pack(fill=tk.X)
        self.viewer_before = ImageViewer(before_box, ui_scale=self.ui_scale)

        after_box = tk.Frame(images_panel, bg="#1e1e1e", bd=1, relief=tk.SOLID)
        after_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4, 0))
        tk.Label(after_box, text="AFTER (Hasil Pengolahan Citra)", bg="#252526", fg="#4ec9b0",
                 font=("Segoe UI", 9, "bold"), pady=4).pack(fill=tk.X)
        self.viewer_after = ImageViewer(after_box, ui_scale=self.ui_scale)

        # Mouse Events diarahkan ke canvas_after
        self.viewer_after.canvas.bind("<Button-1>", self.on_canvas_click)
        self.viewer_after.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.viewer_after.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        graph_panel = tk.Frame(workspace, bg="#1e1e1e", height=int(230 * self.ui_scale), bd=1, relief=tk.SOLID)
        graph_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=(6, 0))
        graph_panel.pack_propagate(False)
        self.histogram_panel = HistogramPanel(graph_panel, ui_scale=self.ui_scale)

    # ------------------------------------------------------------------
    # Aksi toolbar
    # ------------------------------------------------------------------
    def load_image(self, path):
        self.state.load(path)
        self.refresh_all()

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            self.load_image(path)
            self.tool_mode = "none"
            self.status_label.config(text="Gambar berhasil dimuat")

    def save_file(self):
        if self.state.current_image is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if path:
            cv2.imwrite(path, self.state.current_image)
            messagebox.showinfo("Tersimpan", f"Gambar hasil (After) berhasil disimpan ke:\n{path}")

    def undo(self):
        if self.state.undo():
            self.refresh_all()
            self.status_label.config(text="Undo berhasil")

    def reset_image(self):
        if self.state.reset():
            self.tool_mode = "none"
            self.refresh_all()
            self.status_label.config(text="Gambar dikembalikan ke awal")

    def apply_filter(self, func):
        if self.state.apply(func):
            self.tool_mode = "none"
            self.refresh_all()
            self.status_label.config(text=f"Metode diterapkan: {func.__name__}")

    # ------------------------------------------------------------------
    # Tool interaktif (magic wand & eraser)
    # ------------------------------------------------------------------
    def activate_magic_wand(self):
        if self.state.current_image is None:
            return
        self.tool_mode = "magic_wand"
        self.status_label.config(text="Mode Magic Wand: Klik area warna pada panel AFTER yang ingin dihapus")

    def activate_eraser(self):
        if self.state.current_image is None:
            return
        self.tool_mode = "eraser"
        h, w = self.state.current_image.shape[:2]
        self.eraser_mask = np.zeros((h, w), dtype=np.uint8)
        self.status_label.config(text="Mode Object Eraser: Coret objek pada panel AFTER, lalu lepas klik")

    def _event_coords(self, event):
        if self.state.current_image is None:
            return None
        return self.viewer_after.canvas_to_image_coords(event, self.state.current_image.shape)

    def on_canvas_click(self, event):
        coords = self._event_coords(event)
        if not coords:
            return

        if self.tool_mode == "magic_wand":
            self.state.push_history()
            res, _ = magic_wand_remove_bg(self.state.current_image, coords, tolerance=35)
            self.state.current_image = res
            self.refresh_all()
            self.status_label.config(text=f"Magic Wand diterapkan di titik {coords}")

        elif self.tool_mode == "eraser":
            self.last_x, self.last_y = coords

    def on_canvas_drag(self, event):
        if self.tool_mode == "eraser" and self.last_x is not None:
            coords = self._event_coords(event)
            if coords:
                cv2.line(self.eraser_mask, (self.last_x, self.last_y), coords, 255, thickness=18)
                preview = self.state.current_image.copy()
                preview[self.eraser_mask > 0] = (0, 0, 255)
                self.viewer_after.render(preview)
                self.last_x, self.last_y = coords

    def on_canvas_release(self, event):
        if self.tool_mode == "eraser" and self.eraser_mask is not None and np.any(self.eraser_mask > 0):
            self.state.push_history()
            self.state.current_image = inpaint_erase(self.state.current_image, self.eraser_mask)
            self.eraser_mask.fill(0)
            self.last_x, self.last_y = None, None
            self.refresh_all()
            self.status_label.config(text="Object Eraser (Inpainting) selesai!")

    # ------------------------------------------------------------------
    # Refresh tampilan
    # ------------------------------------------------------------------
    def refresh_all(self):
        if self.state.original_image is not None:
            self.viewer_before.render(self.state.original_image)
        if self.state.current_image is not None:
            self.viewer_after.render(self.state.current_image)
        self.histogram_panel.update(self.state.original_image, self.state.current_image)

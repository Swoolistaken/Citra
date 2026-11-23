import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from image_processor import ImageProcessor

class MiniPhotoshopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Photoshop - Before/After & Histogram Analisis (Rinaldi Munir)")
        self.root.geometry("1280x820")
        self.root.configure(bg="#2b2b2b")

        self.original_image = None
        self.current_image = None
        self.history = []
        self.display_scale = 1.0

        self.tool_mode = "none"
        self.eraser_mask = None
        self.last_x, self.last_y = None, None

        self._build_ui()

        try:
            self.load_image("sample_image.jpg")
        except Exception:
            pass

    def _build_ui(self):
        # Top Toolbar
        topbar = tk.Frame(self.root, bg="#1e1e1e", height=45)
        topbar.pack(side=tk.TOP, fill=tk.X)

        btn_style = {"bg": "#3c3f41", "fg": "white", "relief": tk.FLAT, "padx": 12, "pady": 6, "font": ("Segoe UI", 9, "bold")}
        tk.Button(topbar, text="📂 Buka Gambar", command=self.open_file, **btn_style).pack(side=tk.LEFT, padx=6, pady=6)
        tk.Button(topbar, text="💾 Simpan Hasil (After)", command=self.save_file, **btn_style).pack(side=tk.LEFT, padx=6, pady=6)
        tk.Button(topbar, text="↩️ Undo", command=self.undo, **btn_style).pack(side=tk.LEFT, padx=6, pady=6)
        tk.Button(topbar, text="🔄 Reset Asli", command=self.reset_image, **btn_style).pack(side=tk.LEFT, padx=6, pady=6)

        self.status_label = tk.Label(topbar, text="Mode: Normal", bg="#1e1e1e", fg="#a9b7c6", font=("Segoe UI", 9))
        self.status_label.pack(side=tk.RIGHT, padx=15)

        # Main Container
        main_frame = tk.Frame(self.root, bg="#2b2b2b")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollable Left Sidebar
        sidebar_container = tk.Frame(main_frame, bg="#313335", width=270)
        sidebar_container.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        sidebar_container.pack_propagate(False)

        sb_canvas = tk.Canvas(sidebar_container, bg="#313335", highlightthickness=0)
        scrollbar = tk.Scrollbar(sidebar_container, orient="vertical", command=sb_canvas.yview)
        sidebar = tk.Frame(sb_canvas, bg="#313335")

        sidebar.bind("<Configure>", lambda e: sb_canvas.configure(scrollregion=sb_canvas.bbox("all")))
        sb_canvas.create_window((0, 0), window=sidebar, anchor="nw", width=250)
        sb_canvas.configure(yscrollcommand=scrollbar.set)

        sb_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def _on_mousewheel(event):
            sb_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        sb_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def add_section(title):
            lbl = tk.Label(sidebar, text=title, bg="#313335", fg="#6897bb", font=("Segoe UI", 8, "bold"), anchor="w")
            lbl.pack(fill=tk.X, padx=10, pady=(10, 3))

        tool_btn = {"bg": "#4b6eaf", "fg": "white", "relief": tk.FLAT, "pady": 5, "font": ("Segoe UI", 9)}
        filter_btn = {"bg": "#3c3f41", "fg": "white", "relief": tk.FLAT, "pady": 4, "font": ("Segoe UI", 9)}

        add_section("🛠️ INTERACTIVE TOOLS (KLIK DI AFTER)")
        tk.Button(sidebar, text="🪄 Magic Wand (HSV Segment)", command=self.activate_magic_wand, **tool_btn).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(sidebar, text="🩹 Object Eraser (Inpainting)", command=self.activate_eraser, **tool_btn).pack(fill=tk.X, padx=10, pady=2)

        add_section("1️⃣ OPERASI TITIK (POINT OPS)")
        tk.Button(sidebar, text="Citra Negatif (Invert)", command=lambda: self.apply_filter(ImageProcessor.image_negative), **filter_btn).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(sidebar, text="Contrast Stretching", command=lambda: self.apply_filter(ImageProcessor.contrast_stretching), **filter_btn).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(sidebar, text="Binary Thresholding", command=lambda: self.apply_filter(ImageProcessor.binary_threshold), **filter_btn).pack(fill=tk.X, padx=10, pady=2)

        add_section("2️⃣ HISTOGRAM CITRA")
        tk.Button(sidebar, text="Histogram Equalization", command=lambda: self.apply_filter(ImageProcessor.auto_contrast), **filter_btn).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(sidebar, text="CLAHE (Adaptive Hist.)", command=lambda: self.apply_filter(ImageProcessor.clahe_enhance), **filter_btn).pack(fill=tk.X, padx=10, pady=2)

        add_section("3️⃣ KONVOLUSI & PENAPISAN")
        tk.Button(sidebar, text="Gaussian Blur (Low-Pass)", command=lambda: self.apply_filter(ImageProcessor.gaussian_blur), **filter_btn).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(sidebar, text="Median Filter (Denoising)", command=lambda: self.apply_filter(ImageProcessor.median_filter), **filter_btn).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(sidebar, text="Sharpen (High-Pass)", command=lambda: self.apply_filter(ImageProcessor.sharpen), **filter_btn).pack(fill=tk.X, padx=10, pady=2)

        add_section("4️⃣ PENDETEKSIAN TEPI (EDGE)")
        tk.Button(sidebar, text="Operator Sobel (Gradien)", command=lambda: self.apply_filter(ImageProcessor.sobel_edge), **filter_btn).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(sidebar, text="Operator Canny", command=lambda: self.apply_filter(ImageProcessor.canny_edge), **filter_btn).pack(fill=tk.X, padx=10, pady=2)

        add_section("5️⃣ OPERASI MORFOLOGI")
        tk.Button(sidebar, text="Dilasi (Tebalkan Terang)", command=lambda: self.apply_filter(ImageProcessor.morph_dilation), **filter_btn).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(sidebar, text="Erosi (Tipiskan Terang)", command=lambda: self.apply_filter(ImageProcessor.morph_erosion), **filter_btn).pack(fill=tk.X, padx=10, pady=2)

        add_section("6️⃣ OPERASI GEOMETRI")
        tk.Button(sidebar, text="Flip Horizontal (Cermin)", command=lambda: self.apply_filter(ImageProcessor.flip_horizontal), **filter_btn).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(sidebar, text="Rotate 90° Searah Jarum Jam", command=lambda: self.apply_filter(ImageProcessor.rotate_90_cw), **filter_btn).pack(fill=tk.X, padx=10, pady=2)

        add_section("7️⃣ EFEK & CITRA BERWARNA")
        tk.Button(sidebar, text="Retro Sepia Filter", command=lambda: self.apply_filter(ImageProcessor.sepia_filter), **filter_btn).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(sidebar, text="Pencil Sketch", command=lambda: self.apply_filter(ImageProcessor.edge_sketch), **filter_btn).pack(fill=tk.X, padx=10, pady=(2, 15))

        # Right Workspace (Top: Before & After Canvases, Bottom: Histogram Graphs)
        workspace = tk.Frame(main_frame, bg="#2b2b2b")
        workspace.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- TOP: BEFORE & AFTER SPLIT PANEL ---
        images_panel = tk.Frame(workspace, bg="#2b2b2b")
        images_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Left Panel: BEFORE (Citra Asli)
        before_box = tk.Frame(images_panel, bg="#1e1e1e", bd=1, relief=tk.SOLID)
        before_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))
        tk.Label(before_box, text="🖼️ BEFORE (Citra Asli)", bg="#252526", fg="#cccccc", font=("Segoe UI", 9, "bold"), pady=4).pack(fill=tk.X)
        self.canvas_before = tk.Canvas(before_box, bg="#1e1e1e", highlightthickness=0)
        self.canvas_before.pack(fill=tk.BOTH, expand=True)

        # Right Panel: AFTER (Hasil Pengolahan)
        after_box = tk.Frame(images_panel, bg="#1e1e1e", bd=1, relief=tk.SOLID)
        after_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4, 0))
        tk.Label(after_box, text="✨ AFTER (Hasil Pengolahan Citra)", bg="#252526", fg="#4ec9b0", font=("Segoe UI", 9, "bold"), pady=4).pack(fill=tk.X)
        self.canvas_after = tk.Canvas(after_box, bg="#1e1e1e", highlightthickness=0)
        self.canvas_after.pack(fill=tk.BOTH, expand=True)

        # Mouse Events diarahkan ke canvas_after
        self.canvas_after.bind("<Button-1>", self.on_canvas_click)
        self.canvas_after.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas_after.bind("<ButtonRelease-1>", self.on_canvas_release)

        # --- BOTTOM: GRAFIK HISTOGRAM RGB (BEFORE vs AFTER) ---
        graph_panel = tk.Frame(workspace, bg="#1e1e1e", height=230, bd=1, relief=tk.SOLID)
        graph_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=(6, 0))
        graph_panel.pack_propagate(False)

        self.fig = Figure(figsize=(9, 2.2), dpi=95, facecolor="#1e1e1e")
        self.ax_before = self.fig.add_subplot(121)
        self.ax_after = self.fig.add_subplot(122)
        self.fig.subplots_adjust(left=0.06, right=0.98, top=0.82, bottom=0.20, wspace=0.18)

        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=graph_panel)
        self.graph_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_image(self, path):
        img = cv2.imread(path)
        if img is None:
            raise ValueError("Gagal memuat gambar.")
        self.original_image = img.copy()
        self.current_image = img.copy()
        self.history = []
        self.refresh_all()

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            self.load_image(path)
            self.tool_mode = "none"
            self.status_label.config(text="Gambar berhasil dimuat")

    def save_file(self):
        if self.current_image is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if path:
            cv2.imwrite(path, self.current_image)
            messagebox.showinfo("Tersimpan", f"Gambar hasil (After) berhasil disimpan ke:\n{path}")

    def push_history(self):
        if self.current_image is not None:
            self.history.append(self.current_image.copy())
            if len(self.history) > 15:
                self.history.pop(0)

    def undo(self):
        if self.history:
            self.current_image = self.history.pop()
            self.refresh_all()
            self.status_label.config(text="Undo berhasil")

    def reset_image(self):
        if self.original_image is not None:
            self.push_history()
            self.current_image = self.original_image.copy()
            self.tool_mode = "none"
            self.refresh_all()
            self.status_label.config(text="Gambar dikembalikan ke awal")

    def apply_filter(self, func):
        if self.current_image is None:
            return
        self.tool_mode = "none"
        self.push_history()
        self.current_image = func(self.current_image)
        self.refresh_all()
        self.status_label.config(text=f"Metode diterapkan: {func.__name__}")

    def activate_magic_wand(self):
        if self.current_image is None:
            return
        self.tool_mode = "magic_wand"
        self.status_label.config(text="Mode Magic Wand: Klik area warna pada panel AFTER yang ingin dihapus")

    def activate_eraser(self):
        if self.current_image is None:
            return
        self.tool_mode = "eraser"
        h, w = self.current_image.shape[:2]
        self.eraser_mask = np.zeros((h, w), dtype=np.uint8)
        self.status_label.config(text="Mode Object Eraser: Coret objek pada panel AFTER, lalu lepas klik")

    def _canvas_to_image_coords(self, event):
        if self.current_image is None:
            return None
        img_h, img_w = self.current_image.shape[:2]
        disp_w = int(img_w * self.display_scale)
        disp_h = int(img_h * self.display_scale)
        offset_x = (self.canvas_after.winfo_width() - disp_w) // 2
        offset_y = (self.canvas_after.winfo_height() - disp_h) // 2

        ix = int((event.x - offset_x) / self.display_scale)
        iy = int((event.y - offset_y) / self.display_scale)
        if 0 <= ix < img_w and 0 <= iy < img_h:
            return (ix, iy)
        return None

    def on_canvas_click(self, event):
        coords = self._canvas_to_image_coords(event)
        if not coords:
            return

        if self.tool_mode == "magic_wand":
            self.push_history()
            res, _ = ImageProcessor.magic_wand_remove_bg(self.current_image, coords, tolerance=35)
            self.current_image = res
            self.refresh_all()
            self.status_label.config(text=f"Magic Wand diterapkan di titik {coords}")

        elif self.tool_mode == "eraser":
            self.last_x, self.last_y = coords

    def on_canvas_drag(self, event):
        if self.tool_mode == "eraser" and self.last_x is not None:
            coords = self._canvas_to_image_coords(event)
            if coords:
                cv2.line(self.eraser_mask, (self.last_x, self.last_y), coords, 255, thickness=18)
                preview = self.current_image.copy()
                preview[self.eraser_mask > 0] = (0, 0, 255)
                self._render_to_canvas(self.canvas_after, preview, is_after=True)
                self.last_x, self.last_y = coords

    def on_canvas_release(self, event):
        if self.tool_mode == "eraser" and self.eraser_mask is not None and np.any(self.eraser_mask > 0):
            self.push_history()
            self.current_image = ImageProcessor.inpaint_erase(self.current_image, self.eraser_mask)
            self.eraser_mask.fill(0)
            self.last_x, self.last_y = None, None
            self.refresh_all()
            self.status_label.config(text="Object Eraser (Inpainting) selesai!")

    def _render_to_canvas(self, canvas_widget, cv_img, is_after=False):
        canvas_widget.update_idletasks()
        cw = max(canvas_widget.winfo_width(), 420)
        ch = max(canvas_widget.winfo_height(), 360)

        img_h, img_w = cv_img.shape[:2]
        scale = min((cw - 16) / img_w, (ch - 16) / img_h, 1.0)
        if is_after:
            self.display_scale = scale

        new_w = int(img_w * scale)
        new_h = int(img_h * scale)

        resized = cv2.resize(cv_img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        tk_img = ImageTk.PhotoImage(pil_img)

        if is_after:
            self.tk_img_after = tk_img
        else:
            self.tk_img_before = tk_img

        canvas_widget.delete("all")
        canvas_widget.create_image(cw // 2, ch // 2, image=tk_img, anchor=tk.CENTER)

    def update_histograms(self):
        if self.original_image is None or self.current_image is None:
            return

        h_before = ImageProcessor.compute_rgb_histograms(self.original_image)
        h_after = ImageProcessor.compute_rgb_histograms(self.current_image)

        for ax, hist_data, title in [
            (self.ax_before, h_before, "Histogram Intensitas Piksel - BEFORE"),
            (self.ax_after, h_after, "Histogram Intensitas Piksel - AFTER")
        ]:
            ax.clear()
            ax.set_facecolor("#252526")
            ax.plot(hist_data['r'], color="#ff5555", linewidth=1.2, label="Red")
            ax.plot(hist_data['g'], color="#50fa7b", linewidth=1.2, label="Green")
            ax.plot(hist_data['b'], color="#61afef", linewidth=1.2, label="Blue")
            ax.fill_between(range(256), hist_data['r'], color="#ff5555", alpha=0.12)
            ax.fill_between(range(256), hist_data['g'], color="#50fa7b", alpha=0.12)
            ax.fill_between(range(256), hist_data['b'], color="#61afef", alpha=0.12)
            ax.set_title(title, color="#e0e0e0", fontsize=8.5, fontweight="bold", pad=4)
            ax.set_xlim([0, 255])
            ax.tick_params(colors="#aaaaaa", labelsize=7)
            ax.grid(True, linestyle="--", alpha=0.2, color="#888888")
            for spine in ax.spines.values():
                spine.set_color("#444444")

        self.ax_after.legend(loc="upper right", fontsize=7, facecolor="#1e1e1e", edgecolor="#444444", labelcolor="white")
        self.graph_canvas.draw()

    def refresh_all(self):
        if self.original_image is not None:
            self._render_to_canvas(self.canvas_before, self.original_image, is_after=False)
        if self.current_image is not None:
            self._render_to_canvas(self.canvas_after, self.current_image, is_after=True)
        self.update_histograms()

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniPhotoshopApp(root)
    root.mainloop()


"""Panel grafik histogram RGB (before vs after) memakai matplotlib."""
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from core.histogram import compute_rgb_histograms


class HistogramPanel:
    """Dua subplot histogram intensitas piksel, bergaya gelap."""

    def __init__(self, parent):
        self.fig = Figure(figsize=(9, 2.2), dpi=95, facecolor="#1e1e1e")
        self.ax_before = self.fig.add_subplot(121)
        self.ax_after = self.fig.add_subplot(122)
        self.fig.subplots_adjust(left=0.06, right=0.98, top=0.82, bottom=0.20, wspace=0.18)

        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.graph_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update(self, before_image, after_image):
        """Hitung ulang dan gambar histogram kedua citra."""
        if before_image is None or after_image is None:
            return

        h_before = compute_rgb_histograms(before_image)
        h_after = compute_rgb_histograms(after_image)

        for ax, hist_data, title in [
            (self.ax_before, h_before, "Histogram Intensitas Piksel - BEFORE"),
            (self.ax_after, h_after, "Histogram Intensitas Piksel - AFTER"),
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

        self.ax_after.legend(loc="upper right", fontsize=7, facecolor="#1e1e1e",
                             edgecolor="#444444", labelcolor="white")
        self.graph_canvas.draw()

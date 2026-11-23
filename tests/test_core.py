"""Smoke test fungsi murni paket core memakai citra sintetis (tanpa GUI)."""
import numpy as np
import pytest

from core import edges, effects, filters, geometry, histogram, morphology, point_ops
from core.interactive import inpaint_erase, magic_wand_remove_bg


@pytest.fixture
def image():
    """Citra sintetis 48x64 BGR uint8 dengan gradien warna."""
    img = np.zeros((48, 64, 3), dtype=np.uint8)
    img[:, :, 0] = np.linspace(0, 255, 64, dtype=np.uint8)[None, :]
    img[:, :, 1] = np.linspace(0, 255, 48, dtype=np.uint8)[:, None]
    img[:, :, 2] = 100
    return img


SMOKE_FUNCS = [
    point_ops.image_negative,
    point_ops.contrast_stretching,
    point_ops.binary_threshold,
    histogram.auto_contrast,
    histogram.clahe_enhance,
    filters.gaussian_blur,
    filters.median_filter,
    filters.sharpen,
    edges.sobel_edge,
    edges.canny_edge,
    morphology.morph_dilation,
    morphology.morph_erosion,
    geometry.flip_horizontal,
    effects.sepia_filter,
    effects.edge_sketch,
]


@pytest.mark.parametrize("func", SMOKE_FUNCS, ids=lambda f: f.__name__)
def test_shape_dtype_dan_input_tidak_berubah(image, func):
    before = image.copy()
    result = func(image)
    assert result.shape == image.shape
    assert result.dtype == np.uint8
    assert np.array_equal(image, before)


def test_negatif_ganda_kembali_ke_asli(image):
    assert np.array_equal(point_ops.image_negative(point_ops.image_negative(image)), image)


def test_contrast_stretching_rentang_penuh(image):
    result = point_ops.contrast_stretching(image)
    for c in (0, 1):  # kanal gradien diregangkan penuh
        assert result[:, :, c].min() == 0
        assert result[:, :, c].max() == 255
    assert np.all(result[:, :, 2] == 100)  # kanal konstan diteruskan apa adanya


def test_contrast_stretching_citra_konstan():
    flat = np.full((16, 16, 3), 77, dtype=np.uint8)
    assert np.array_equal(point_ops.contrast_stretching(flat), flat)


def test_threshold_hanya_biner(image):
    result = point_ops.binary_threshold(image)
    assert set(np.unique(result)).issubset({0, 255})


def test_gaussian_ksize_genap_dikoreksi(image):
    result = filters.gaussian_blur(image, ksize=4)
    assert result.shape == image.shape


def test_canny_hanya_biner(image):
    result = edges.canny_edge(image)
    assert set(np.unique(result)).issubset({0, 255})


def test_dilasi_erodi_batas_intensitas(image):
    assert np.all(morphology.morph_dilation(image) >= image)
    assert np.all(morphology.morph_erosion(image) <= image)


def test_flip_ganda_kembali_ke_asli(image):
    assert np.array_equal(geometry.flip_horizontal(geometry.flip_horizontal(image)), image)


def test_rotasi_90_tukar_dimensi_dan_4x_kembali(image):
    once = geometry.rotate_90_cw(image)
    assert once.shape == (64, 48, 3)
    four = image
    for _ in range(4):
        four = geometry.rotate_90_cw(four)
    assert np.array_equal(four, image)


def test_histogram_jumlah_sama_dengan_piksel(image):
    hists = histogram.compute_rgb_histograms(image)
    assert set(hists) == {'b', 'g', 'r'}
    total = image.shape[0] * image.shape[1]
    for channel in hists.values():
        assert len(channel) == 256
        assert channel.sum() == total


def test_histogram_citra_satu_warna():
    solid = np.zeros((8, 8, 3), dtype=np.uint8)
    solid[:] = (10, 20, 30)
    hists = histogram.compute_rgb_histograms(solid)
    assert hists['b'][10] == 64
    assert hists['g'][20] == 64
    assert hists['r'][30] == 64


def test_magic_wand_citra_satu_warna():
    solid = np.zeros((32, 32, 3), dtype=np.uint8)
    solid[:] = (200, 100, 50)
    before = solid.copy()
    result, mask = magic_wand_remove_bg(solid, (16, 16), tolerance=30)
    assert np.all(mask == 255)
    assert np.array_equal(result[0, 0], (255, 255, 255))
    assert np.array_equal(result[0, 16], (220, 220, 220))
    assert np.array_equal(solid, before)


def test_inpaint_mask_kosong_tidak_mengubah(image):
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    assert np.array_equal(inpaint_erase(image, mask), image)


def test_inpaint_area_tercoret(image):
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    mask[10:20, 10:20] = 255
    result = inpaint_erase(image, mask)
    assert result.shape == image.shape
    assert result.dtype == np.uint8

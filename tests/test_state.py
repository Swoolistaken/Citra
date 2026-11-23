"""Test EditorState: muat, apply, undo, reset, dan batas riwayat."""
import cv2
import numpy as np
import pytest

from app.state import HISTORY_LIMIT, EditorState
from core.point_ops import image_negative


@pytest.fixture
def image_path(tmp_path):
    img = np.full((16, 16, 3), 90, dtype=np.uint8)
    path = str(tmp_path / "sample.png")
    cv2.imwrite(path, img)
    return path


def test_load_mengisi_original_dan_current(image_path):
    state = EditorState()
    state.load(image_path)
    assert state.original_image is not None
    assert np.array_equal(state.current_image, state.original_image)
    assert state.history == []


def test_load_gagal_raise(image_path):
    state = EditorState()
    with pytest.raises(ValueError):
        state.load(image_path + ".tidak_ada.png")


def test_apply_dan_undo(image_path):
    state = EditorState()
    state.load(image_path)
    asli = state.current_image.copy()
    assert state.apply(image_negative)
    assert not np.array_equal(state.current_image, asli)
    assert state.undo()
    assert np.array_equal(state.current_image, asli)
    assert not state.undo()


def test_reset_bisa_di_undo(image_path):
    state = EditorState()
    state.load(image_path)
    state.apply(image_negative)
    assert state.reset()
    assert np.array_equal(state.current_image, state.original_image)
    assert state.undo()
    assert not np.array_equal(state.current_image, state.original_image)


def test_batas_riwayat(image_path):
    state = EditorState()
    state.load(image_path)
    for _ in range(HISTORY_LIMIT + 5):
        state.apply(image_negative)
    assert len(state.history) == HISTORY_LIMIT


def test_apply_tanpa_citra_false():
    state = EditorState()
    assert not state.apply(image_negative)
    assert not state.undo()
    assert not state.reset()

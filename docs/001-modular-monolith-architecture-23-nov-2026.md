# 001 - Modular Monolith Architecture

- Date: 2026-11-23
- Author: OpenCode agent with repo owner
- Type: decision
- Status: done
- Modules: main.py, core/, app/, tests/, requirements.txt, requirements-dev.txt

## Context

The app started as two files: `main.py` (334 lines, one MiniPhotoshopApp
class mixing layout, image state, mouse tools, rendering, and histogram
plotting) and `image_processor.py` (187 lines, ImageProcessor class of
static methods). No tests, unpinned dependencies, empty docs. The course
project needs room to grow chapter by chapter.

## Goal

Simple modular monolith: one process, plain Python, no frameworks. Two
layers with a single dependency direction (`app -> core`). Behavior
identical to the original app. Easy to add new operations later.

## Changes

- `core/` package: pure functions, one module per lecture chapter
  (point_ops, histogram, filters, edges, morphology, geometry, effects,
  interactive). BGR uint8 in/out, inputs never mutated, no GUI imports.
- `app/` package: operations.py (sidebar catalog SECTIONS), state.py
  (EditorState, undo history cap 15), viewer.py (canvas render and
  coordinate mapping), histogram_panel.py (matplotlib panel), window.py
  (layout and tool wiring).
- `main.py` reduced to a thin entry point. `image_processor.py` removed.
- Extension recipe: new core function + one catalog tuple + one smoke test.
- Emojis removed from all UI labels. Degree sign replaced with plain text.
- Dependencies pinned from verified installs: opencv-python 4.14.0.94
  (stays below 5 because OpenCV 5.x reorganized modules), numpy 2.5.5,
  pillow 13.0.0, matplotlib 3.11.2. pytest 9.2.0 in requirements-dev.txt.
- Language policy: UI text and docstrings Indonesian. AGENTS.md, docs,
  commits, and identifiers English.

## Verification

- `.\.venv\Scripts\python.exe -m pytest tests -q`: 35 passed.
- GUI smoke script driving the real Tk app: all 16 catalog operations
  applied, undo/reset restores the original, magic wand and eraser paths
  exercised, histograms redrawn. Result: PASS.
- Commands run from repo root on Windows, Python 3.13.14 via py launcher.

## References

- context7: /opencv/opencv-python (install and version policy),
  /websites/opencv (OpenCV 5 transition guide),
  /websites/matplotlib_stable (FigureCanvasTkAgg embedding pattern).
- Course module: Rinaldi Munir, Pengolahan Citra Digital, chapters 1-7.

# AGENTS.md

Guide for AI agents and contributors working in this repository. Read this
before making any change.

## Project Overview

Mini Photoshop: desktop image editor for the Pengolahan Citra (Digital Image
Processing) course. Implements the 7 chapters of the Rinaldi Munir module.
Stack: Python 3.13, Tkinter, OpenCV, NumPy, Pillow, matplotlib.
Architecture: modular monolith. One process, two layers, plain functions,
no frameworks, no plugins.

## Environment And Commands

Verified on Windows, 2026-11-23:

- The `python` command is a broken Microsoft Store alias on this machine.
  Use `py` instead.
- Virtual environment lives in `.venv/` (gitignored).
- Run everything from the repo root. The app autoloads `sample_image.jpg`
  by relative path.

Setup:

```
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Run app:

```
.\.venv\Scripts\python.exe main.py
```

Run tests:

```
.\.venv\Scripts\python.exe -m pytest tests -q
```

Dependencies are pinned in `requirements.txt`. OpenCV must stay on the 4.x
line (`opencv-python<5`): OpenCV 5.x reorganized modules and breaks APIs used
here. Do not upgrade without testing and a docs journal entry. Install only
one cv2 package variant (opencv-python, not contrib or headless alongside).

## Architecture

Dependency rule: `app -> core`, never the reverse. `core` must not import
tkinter, matplotlib, or anything from `app`.

```
main.py               entry point only
core/                 pure image functions, one module per topic (feature slice)
  point_ops.py        chapter 1: negative, contrast stretching, threshold
  histogram.py        chapter 2: equalization, CLAHE, RGB histogram computation
  filters.py          chapter 3: gaussian blur, median, sharpen
  edges.py            chapter 4: sobel, canny
  morphology.py       chapter 5: dilation, erosion
  geometry.py         chapter 6: flip, rotate
  effects.py          chapter 7: sepia, pencil sketch
  interactive.py      magic wand (HSV segmentation), inpaint eraser
app/                  Tkinter layer
  operations.py       sidebar catalog: SECTIONS = [(title, [(label, func), ...])]
  state.py            EditorState: original/current image, undo history (cap 15)
  viewer.py           ImageViewer: canvas render, scale, mouse-to-pixel mapping
  histogram_panel.py  matplotlib before/after histogram panel
  window.py           MiniPhotoshopApp: layout, toolbar, tool modes, event wiring
tests/                pytest smoke tests, synthetic images, no GUI needed
docs/                 documentation pipeline and decision journal
```

Image convention: BGR uint8 numpy arrays everywhere (OpenCV default).
Core functions return new arrays and never mutate their input.

## Adding A New Operation

1. Write a pure function in the matching `core/` module. New topic means a
   new `core/` module. Keep the BGR uint8 in/out convention.
2. Add one `(label, func)` tuple to the right section in `app/operations.py`.
   The sidebar builds itself from this catalog. No other UI change needed.
3. Add a smoke test in `tests/test_core.py`.
4. Run tests and the app. Log the change in `docs/journal.json`.

Interactive tools that need mouse state (magic wand, eraser) are wired in
`app/window.py`, not in the catalog.

## Code Rules

- No emojis anywhere: code, UI strings, comments, docs, commit messages.
- ASCII punctuation only. No em dashes or en dashes. Use commas, colons,
  or plain hyphens.
- Dates in ISO 8601: YYYY-MM-DD.
- Identifiers in English: snake_case for functions and modules, PascalCase
  for classes.
- UI text and docstrings in Indonesian (course context). Docs, AGENTS.md,
  and commit messages in English.
- Small functions, one responsibility. Prefer plain functions over classes
  unless state is involved.
- No new dependencies without discussion and a journal entry.
- Never commit `__pycache__/`, `.venv/`, or generated images.

## Agent Behavior Rules

- Do not assume the unknown. Read files before editing them. Verify facts
  (versions, APIs, paths) instead of guessing.
- Use the context7 MCP for library documentation (OpenCV, matplotlib, etc.)
  before relying on memory.
- After any code change: run pytest, then launch the app or a GUI smoke check.
- Ask the user when requirements are ambiguous. Do not invent features.
- Keep behavior identical during refactors unless a change is requested.
- No destructive git operations (reset --hard, force push, branch deletion)
  without explicit user confirmation.

## Contributing

- Branch names: `feat/...`, `fix/...`, `refactor/...`, `docs/...`.
- Conventional commits: feat, fix, refactor, test, docs, chore.
  Example: `refactor: split image processing into core package`.
- Small, focused commits. One logical change per commit.
- Every significant change gets a document in `docs/` and a record in
  `docs/journal.json`. See `docs/README-docs.md`.
- Before pushing: tests pass, app runs, no emojis or non-ASCII punctuation
  in new text, journal updated.

## Documentation Pipeline

- Guide: `docs/README-docs.md`
- Template: `docs/000-template-name-23-nov-2026.md` (number 000 reserved)
- Journal: `docs/journal.json` (append-only)

# 002 - Native DPI Rendering On Scaled Windows Displays

- Date: 2026-11-23
- Author: OpenCode agent
- Type: change
- Status: done
- Modules: main.py, app/window.py, app/viewer.py, app/histogram_panel.py

## Context

The app looked blurry ("low res") on the development machine. Verified cause:
Windows display scaling is 150 percent (registry AppliedDPI = 144) on a
1920x1080 panel, while the process never declared DPI awareness. Windows
therefore rendered the Tkinter window at 96 DPI and bitmap-stretched it 1.5x,
blurring text, buttons, canvases, and histogram plots. This was default
behavior, not an intended design choice. The separate INTER_AREA downscale
used to fit images into the canvas is intended and unrelated.

## Goal

Render the UI at native device pixels so it is crisp on HiDPI / scaled
displays, keep layout proportions identical to the 96 DPI design, and keep
the window inside the screen work area. No change to image processing.

## Changes

- main.py: call SetProcessDpiAwareness(1) (system DPI aware) before creating
  the Tk root, with SetProcessDPIAware() as fallback. Windows only.
- app/window.py: compute ui_scale = winfo_fpixels("1i") / 96. Scale window
  geometry, sidebar width, and graph panel height by ui_scale. Cap geometry
  to the screen work area via SystemParametersInfoW(SPI_GETWORKAREA). Pass
  ui_scale to viewers and histogram panel.
- app/viewer.py: accept ui_scale, scale the minimum canvas size and padding.
- app/histogram_panel.py: accept ui_scale, scale Figure dpi so plots render
  at native resolution.
- At 100 percent scaling ui_scale = 1.0 and behavior is unchanged.

## Verification

- pytest tests -q: 35 passed.
- GUI smoke script: 16 operations, undo/reset, magic wand, eraser, histogram
  all OK.
- Screenshot at 150 percent scaling: ui_scale ~1.5, tk scaling ~2.0, window
  1918x1032 physical pixels, text and plots crisp (no bitmap stretch).
- ASCII scan: OK.

## References

- Microsoft Windows DPI awareness APIs: SetProcessDpiAwareness,
  SetProcessDPIAware, SystemParametersInfoW (SPI_GETWORKAREA).
- Tkinter winfo_fpixels and tk scaling for font / pixel scaling.

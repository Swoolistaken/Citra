# 004 - Remove Histogram RGB Legend

- Date: 2026-11-23
- Author: OpenCode agent with repo owner
- Type: change
- Status: done
- Modules: app/histogram_panel.py

## Context

The AFTER histogram panel drew a Red/Green/Blue legend in the upper right.
On the short 2.2 inch figure the legend box sat on top of the plotted curves
and hid part of the reading.

## Goal

Remove the legend so the full plot area is visible, without changing the
channel colors or the shared symlog scale from doc 003.

## Changes

- Removed the ax_after.legend(...) call.
- Removed the now-unused label= kwargs from the three plot calls.
- Curve colors unchanged: red #ff5555, green #50fa7b, blue #61afef. The
  legend was redundant because each curve is already color-coded.

## Verification

- .\.venv\Scripts\python.exe -m pytest tests -q: 35 passed.
- GUI smoke: 16 operations, undo/reset, magic wand, eraser, histogram OK.

## References

- Follow-up to docs/003-histogram-shared-log-scale-23-nov-2026.md.

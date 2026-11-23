# 003 - Histogram Shared Dynamic Log Scale

- Date: 2026-11-23
- Author: OpenCode agent
- Type: change
- Status: done
- Modules: app/histogram_panel.py

## Context

The RGB histograms looked empty: a flat line along the bottom with a single
spike at the right edge. Verified cause on sample_image.jpg (1600x2560,
4096000 pixels): 42 percent of red pixels sit in bin 255 (1730698 counts),
and only 7 bins exceed 1 percent of that max. The panel set no explicit
ylim, so each subplot autoscaled independently. Two problems resulted:

1. BEFORE and AFTER used different Y scales, so the comparison was unfair.
2. Linear autoscale fit the dominant spike, crushing every other bin below
   1 percent of the plot height (a flat line). Detail was invisible.

The scale was already dynamic, not static. The faults were independent
per-panel scaling and a linear axis under a dominant spike.

## Goal

Make histogram detail visible despite tall spikes, and keep BEFORE and AFTER
on the SAME dynamic Y scale so the comparison stays valid. No change to the
histogram computation itself.

## Changes

- app/histogram_panel.py: compute one shared ymax = max over all six hist
  arrays (before and after, channels r/g/b), guarded to a minimum of 1.0.
- Apply set_yscale("symlog", linthresh=1) and set_ylim(0, ymax * 1.05) to
  BOTH subplots. The scale is recomputed on every update (dynamic) and is
  identical for both panels (fair comparison). The log axis keeps small bins
  visible next to a dominant spike; linthresh=1 keeps the 0..1 region linear.

## Verification

- Compared three renders: current (flat line + spike, different scales),
  shared linear (same scale but still flat), shared symlog (detail visible,
  same scale). Chose shared symlog.
- Real-panel render: both axes ylim (0, 1817232.9), yscale symlog, equal.
  Full distribution detail visible in BEFORE and AFTER.
- pytest tests -q: 35 passed.
- GUI smoke script: 16 operations, undo/reset, magic wand, eraser, histogram
  all OK.
- ASCII scan: OK.

## References

- matplotlib symlog Y scale (linthresh defines the linear region near zero).
- Diagnostic: cv2.calcHist bin counts on sample_image.jpg confirmed the
  bin-255 spike (42 percent of red pixels).

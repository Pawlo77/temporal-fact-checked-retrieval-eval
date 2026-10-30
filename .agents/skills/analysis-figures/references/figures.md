# Figures reference

## Pipeline

- One theme helper (seaborn style and context) bound per figure with
  `matplotlib.rc_context`; a test checks that global rcParams never change.
- Fixed dpi and exact physical size; fit the layout to the canvas (measure
  `fig.get_tightbbox`, shrink the layout rect) instead of `bbox_inches="tight"`.
- `figures/<set>/<stem>.png` and `tables/<set>/`; the report copy mirrors them and
  removes stale stems.
- Each stage writes `captions.csv` (stem, id, title, description, width in mm); a make
  target builds the notes table (figure link | width | description).

## Proportions for the paper

- One report variant per figure, `<stem>.png`, at the width it is placed at: exactly the
  column or the double-column width, never a second low-res copy or a `_double` suffix; the
  width is recorded with the caption so LaTeX knows if it spans one or two columns. Include
  at `width=\linewidth` unscaled, so theme font sizes (7-8 pt) are final. Only the video
  theme (other colours, 1080p) is a second image.
- Height from fixed aspect ratios (0.62 curves and scatters, 0.45 short dot or bar panels,
  1.0 heat maps); long category lists grow per row and go double width or split above a
  third of the page.
- The audit checks pixel size and aspect ratio against the declared class.

## What may appear on the image

| Allowed | Not allowed |
|---|---|
| axis and tick labels, units | notes, explanations, p-value annotations |
| short panel label | titles on single panels, wrapped titles |
| data values that are the plot | benchmark name, "pending", "indicative" |
| compact non-category legend outside the data | category legends (use the legend figure) |

## Audit test (every figure kind, report width and video)

- No cut text, no text-text overlap, no legend over an axes.
- No layout `UserWarning`, no title wider than its axes.
- One data axes per file (colour bars excepted); no lone y tick label naming a quantity.
- Only allowed text kinds.
- Prove it bites: force a legend inside, disable the fit step; keep the skip list empty.

## Look at every figure

Render from real data into a scratch folder and view a contact sheet of every PNG at the
column width.

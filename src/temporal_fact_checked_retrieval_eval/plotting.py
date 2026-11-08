"""Shared plot style for consistent, publication-ready figures.

Call :func:`apply_style` once at the top of every notebook and script. Use
:data:`LANGUAGE_COLORS` for the Polish/English contrast and
:func:`categorical_colors` for multi-category series. Save with :func:`savefig`
so figures ship at 300 dpi with a tight bounding box.
"""

from pathlib import Path

import matplotlib as mpl
from matplotlib.figure import Figure

# Okabe-Ito colourblind-safe palette.
PALETTE = {
    "black": "#000000",
    "orange": "#E69F00",
    "sky": "#56B4E9",
    "bluish_green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "reddish_purple": "#CC79A7",
}

# Monochrome + a single accent for the headline Polish/English contrast.
LANGUAGE_COLORS = {"pl": PALETTE["vermillion"], "en": PALETTE["black"]}

# Ordered colours for multi-category series (systems, extended languages).
CATEGORICAL = [
    PALETTE["black"],
    PALETTE["vermillion"],
    PALETTE["blue"],
    PALETTE["bluish_green"],
    PALETTE["orange"],
    PALETTE["reddish_purple"],
    PALETTE["sky"],
    PALETTE["yellow"],
]

_FIG_WIDTH_IN = 6.0
_HEIGHT_RATIO = 0.618  # golden-ratio height
_SAVE_DPI = 300


def apply_style() -> None:
    """Apply the shared rcParams (serif, minimal spines, 300-dpi saves)."""
    mpl.rcParams.update({
        "font.family": "serif",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linewidth": 0.5,
        "legend.frameon": False,
        "figure.dpi": 100,
        "figure.figsize": (_FIG_WIDTH_IN, _FIG_WIDTH_IN * _HEIGHT_RATIO),
        "savefig.dpi": _SAVE_DPI,
        "savefig.bbox": "tight",
    })


def categorical_colors(n: int) -> list[str]:
    """Return ``n`` colours cycling through :data:`CATEGORICAL`."""
    return [CATEGORICAL[i % len(CATEGORICAL)] for i in range(n)]


def language_color(lang: str) -> str:
    """Colour for a language: accent for ``pl``, black for ``en``, sky otherwise."""
    return LANGUAGE_COLORS.get(lang, PALETTE["sky"])


def savefig(fig: Figure, path: str | Path) -> None:
    """Save a figure at publication resolution with a tight bounding box."""
    fig.savefig(path, dpi=_SAVE_DPI, bbox_inches="tight")

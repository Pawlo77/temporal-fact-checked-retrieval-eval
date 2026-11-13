"""Tests for the shared plot style."""

import matplotlib as mpl

from temporal_fact_checked_retrieval_eval.plotting import (
    apply_style,
    categorical_colors,
    language_color,
)


def test_apply_style_sets_serif_and_dpi() -> None:
    apply_style()
    assert mpl.rcParams["font.family"] == ["serif"]
    assert mpl.rcParams["savefig.dpi"] == 300


def test_categorical_colors_cycles() -> None:
    colors = categorical_colors(10)
    assert len(colors) == 10
    assert all(color.startswith("#") for color in colors)
    assert colors[0] == colors[8]


def test_language_colors_contrast() -> None:
    assert language_color("pl") != language_color("en")

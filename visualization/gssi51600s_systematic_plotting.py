"""Plot helpers for GSSI51600S systematic benchmark figures."""

from __future__ import annotations

import math
from collections.abc import Iterable
from typing import Any


def finite_values(values: Iterable[Any]) -> list[float]:
    result: list[float] = []
    for value in values:
        if value is None:
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(number):
            result.append(number)
    return result


def set_zero_based_ylim(
    ax: Any,
    values: Iterable[Any],
    *,
    minimum_top: float = 1.0,
    headroom_fraction: float = 0.18,
) -> None:
    finite = finite_values(values)
    upper = max([float(minimum_top), *(finite or [0.0])])
    ax.set_ylim(0.0, upper * (1.0 + float(headroom_fraction)))


def set_zoomed_comparison_ylim(
    ax: Any,
    values: Iterable[Any],
    *,
    pad_fraction: float = 0.25,
    min_pad_fraction_of_value: float = 0.01,
) -> None:
    """Use for close nonzero bars where relative differences are the comparison."""
    finite = finite_values(values)
    if not finite:
        return
    low = min(finite)
    high = max(finite)
    span = high - low
    center = 0.5 * (low + high)
    pad = max(span * float(pad_fraction), abs(center) * float(min_pad_fraction_of_value), 1.0e-9)
    ax.set_ylim(low - pad, high + pad)


def annotate_bars(
    ax: Any,
    bars: Iterable[Any],
    values: Iterable[Any],
    *,
    fmt: str = "{:.4f}",
    rotation: int = 90,
    fontsize: int = 7,
    min_offset_fraction: float = 0.012,
) -> None:
    y0, y1 = ax.get_ylim()
    offset = max((y1 - y0) * float(min_offset_fraction), 1.0e-9)
    for bar, value in zip(bars, values, strict=True):
        if value is None:
            label = "n/a"
            y = 0.0 + offset
        else:
            number = float(value)
            label = fmt.format(number)
            y = number + offset if number >= 0.0 else number - offset
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            y,
            label,
            ha="center",
            va="bottom" if y >= 0.0 else "top",
            rotation=rotation,
            fontsize=fontsize,
        )


def draw_delta_bars(
    ax: Any,
    labels: list[str],
    deltas: list[float | None],
    *,
    ylabel: str,
    title: str,
) -> None:
    values = [0.0 if value is None else float(value) for value in deltas]
    max_abs = max([abs(value) for value in values] + [1.0e-6])
    colors = ["#4c78a8" if value >= 0.0 else "#e45756" for value in values]
    bars = ax.bar(labels, values, color=colors)
    for bar, raw_value, value in zip(bars, deltas, values, strict=True):
        xpos = bar.get_x() + bar.get_width() / 2.0
        if raw_value is None:
            ax.scatter([xpos], [0.0], marker="s", color="#666666", zorder=3)
            ax.text(xpos, max_abs * 0.04, "n/a", ha="center", va="bottom", fontsize=7, rotation=90)
        elif abs(value) <= 1.0e-12:
            ax.scatter([xpos], [0.0], marker="D", color="#333333", zorder=3)
            ax.text(xpos, max_abs * 0.04, "0/tie", ha="center", va="bottom", fontsize=7, rotation=90)
    y0, y1 = ax.get_ylim()
    offset = max((y1 - y0) * 0.012, 1.0e-9)
    for bar, value in zip(bars, values, strict=True):
        if abs(value) <= 1.0e-12:
            continue
        xpos = bar.get_x() + bar.get_width() / 2.0
        ypos = value + offset if value > 0.0 else value - offset
        ax.text(
            xpos,
            ypos,
            f"{value:.4f}",
            ha="center",
            va="bottom" if value > 0.0 else "top",
            fontsize=7,
            rotation=90,
        )
    ax.axhline(0.0, color="#333333", linewidth=0.8)
    ax.set_ylim(-0.12 * max_abs, 1.25 * max_abs)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.25)


def set_positive_log_ylim(
    ax: Any,
    values: Iterable[Any],
    *,
    reference: float | None = None,
    floor_fraction: float = 0.5,
) -> float:
    positives = [value for value in finite_values(values) if value > 0.0]
    if reference is not None and reference > 0.0:
        positives.append(float(reference))
    if not positives:
        floor = 1.0e-9
        top = 1.0
    else:
        floor = min(positives) * float(floor_fraction)
        top = max(positives) * 2.0
    ax.set_yscale("log")
    ax.set_ylim(floor, top)
    return floor

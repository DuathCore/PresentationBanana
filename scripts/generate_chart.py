#!/usr/bin/env python3
"""
generate_chart.py – Dark Academic Chart Generator for PresentationBanana

Reusable Matplotlib charting with a dark-professional theme that matches
the presentation style. Exports publication-quality PNGs at 200 DPI.

Usage:
    python3 generate_chart.py --type bar --title "Test" --data "A:10,B:20,C:15"
    python3 generate_chart.py --demo
"""

import argparse
import os
from pathlib import Path
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ---------------------------------------------------------------------------
# Theme constants
# ---------------------------------------------------------------------------
BG_COLOR = "#121A2E"
TEXT_COLOR = "#FFFFFF"
GRID_COLOR = "#1E3050"
ACCENT_GOLD = "#F0AB00"

PALETTE = [
    ACCENT_GOLD,   # gold  (primary accent)
    "#4A9EE0",     # blue
    "#2EA89D",     # teal
    "#3EB489",     # green
    "#9B6DD0",     # purple
    "#E8853D",     # orange
    "#E04B4B",     # red
]

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output" / "images"

# ---------------------------------------------------------------------------
# Theme helper
# ---------------------------------------------------------------------------

def apply_dark_theme():
    """Configure matplotlib rcParams for the dark academic style."""
    plt.rcParams.update({
        # figure
        "figure.figsize": (12.8, 7.2),
        "figure.dpi": 200,
        "figure.facecolor": BG_COLOR,
        "figure.edgecolor": BG_COLOR,
        # axes
        "axes.facecolor": BG_COLOR,
        "axes.edgecolor": GRID_COLOR,
        "axes.labelcolor": TEXT_COLOR,
        "axes.titlesize": 28,
        "axes.labelsize": 16,
        "axes.grid": True,
        "axes.prop_cycle": plt.cycler(color=PALETTE),
        # grid
        "grid.color": GRID_COLOR,
        "grid.linewidth": 0.6,
        "grid.alpha": 0.8,
        # ticks
        "xtick.color": TEXT_COLOR,
        "ytick.color": TEXT_COLOR,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
        # text
        "text.color": TEXT_COLOR,
        "font.family": "sans-serif",
        "font.size": 14,
        # legend
        "legend.facecolor": "#1A2440",
        "legend.edgecolor": GRID_COLOR,
        "legend.fontsize": 13,
        "legend.labelcolor": TEXT_COLOR,
        # savefig
        "savefig.facecolor": BG_COLOR,
        "savefig.edgecolor": BG_COLOR,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.3,
    })


def _output_path(name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    p = OUTPUT_DIR / f"{name}.png"
    return p


def _finalize(fig, name: str) -> str:
    """Apply tight layout, save, close, return path string."""
    fig.tight_layout()
    path = _output_path(name)
    fig.savefig(path)
    plt.close(fig)
    return str(path)


# ---------------------------------------------------------------------------
# ChartBuilder
# ---------------------------------------------------------------------------

class ChartBuilder:
    """Generates common academic chart types with the dark professional theme."""

    def __init__(self):
        apply_dark_theme()

    # -- bar chart ----------------------------------------------------------

    def bar_chart(
        self,
        categories: list[str],
        values: list[float],
        title: str,
        ylabel: str,
        colors: Optional[list[str]] = None,
        name: str = "bar_chart",
    ) -> str:
        fig, ax = plt.subplots()
        clr = colors or [PALETTE[i % len(PALETTE)] for i in range(len(categories))]
        bars = ax.bar(categories, values, color=clr, edgecolor="none", width=0.6)
        ax.set_title(title, pad=18, fontweight="bold")
        ax.set_ylabel(ylabel)
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=6))
        ax.set_axisbelow(True)
        # value labels on bars
        for bar, val in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(values) * 0.02,
                f"{val:g}",
                ha="center", va="bottom", fontsize=12, color=TEXT_COLOR,
            )
        return _finalize(fig, name)

    # -- line chart ---------------------------------------------------------

    def line_chart(
        self,
        x,
        y_series: list[list[float]],
        title: str,
        xlabel: str,
        ylabel: str,
        labels: Optional[list[str]] = None,
        name: str = "line_chart",
    ) -> str:
        fig, ax = plt.subplots()
        for i, y in enumerate(y_series):
            label = labels[i] if labels else f"Series {i+1}"
            ax.plot(x, y, linewidth=2.2, marker="o", markersize=5, label=label)
        ax.set_title(title, pad=18, fontweight="bold")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_axisbelow(True)
        if len(y_series) > 1 or labels:
            ax.legend()
        return _finalize(fig, name)

    # -- scatter plot -------------------------------------------------------

    def scatter_plot(
        self,
        x,
        y,
        title: str,
        xlabel: str,
        ylabel: str,
        name: str = "scatter_plot",
    ) -> str:
        fig, ax = plt.subplots()
        ax.scatter(x, y, color=ACCENT_GOLD, s=50, alpha=0.85, edgecolors="none")
        ax.set_title(title, pad=18, fontweight="bold")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_axisbelow(True)
        return _finalize(fig, name)

    # -- pie chart ----------------------------------------------------------

    def pie_chart(
        self,
        labels: list[str],
        values: list[float],
        title: str,
        colors: Optional[list[str]] = None,
        name: str = "pie_chart",
    ) -> str:
        fig, ax = plt.subplots()
        clr = colors or PALETTE[: len(labels)]
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            colors=clr,
            autopct="%1.1f%%",
            startangle=140,
            pctdistance=0.75,
            wedgeprops=dict(edgecolor=BG_COLOR, linewidth=2),
        )
        for t in texts:
            t.set_color(TEXT_COLOR)
            t.set_fontsize(13)
        for t in autotexts:
            t.set_color(TEXT_COLOR)
            t.set_fontsize(11)
            t.set_fontweight("bold")
        ax.set_title(title, pad=18, fontweight="bold")
        return _finalize(fig, name)

    # -- grouped bar --------------------------------------------------------

    def grouped_bar(
        self,
        categories: list[str],
        groups: list[list[float]],
        title: str,
        ylabel: str,
        group_labels: list[str],
        colors: Optional[list[str]] = None,
        name: str = "grouped_bar",
    ) -> str:
        fig, ax = plt.subplots()
        n_groups = len(groups)
        x = np.arange(len(categories))
        width = 0.7 / n_groups
        clr = colors or PALETTE[:n_groups]

        for i, (vals, lbl) in enumerate(zip(groups, group_labels)):
            offset = (i - (n_groups - 1) / 2) * width
            ax.bar(x + offset, vals, width=width * 0.9, label=lbl,
                   color=clr[i % len(clr)], edgecolor="none")

        ax.set_title(title, pad=18, fontweight="bold")
        ax.set_ylabel(ylabel)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=6))
        ax.set_axisbelow(True)
        ax.legend()
        return _finalize(fig, name)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def run_demo():
    cb = ChartBuilder()
    paths = []

    # bar
    p = cb.bar_chart(
        ["Python", "JavaScript", "Go", "Rust", "Java"],
        [42, 35, 28, 22, 18],
        "Programming Language Popularity",
        "Score",
        name="demo_bar",
    )
    paths.append(p)

    # line
    x = list(range(2020, 2027))
    p = cb.line_chart(
        x,
        [
            [10, 15, 22, 30, 38, 47, 55],
            [8, 12, 14, 18, 24, 28, 33],
        ],
        "Growth Over Time",
        "Year", "Users (M)",
        labels=["Product A", "Product B"],
        name="demo_line",
    )
    paths.append(p)

    # scatter
    rng = np.random.default_rng(42)
    p = cb.scatter_plot(
        rng.normal(50, 15, 60),
        rng.normal(50, 15, 60),
        "Correlation Analysis",
        "Variable X", "Variable Y",
        name="demo_scatter",
    )
    paths.append(p)

    # pie
    p = cb.pie_chart(
        ["Research", "Development", "Testing", "Deployment"],
        [35, 30, 20, 15],
        "Resource Allocation",
        name="demo_pie",
    )
    paths.append(p)

    # grouped bar
    p = cb.grouped_bar(
        ["Q1", "Q2", "Q3", "Q4"],
        [[12, 18, 15, 22], [10, 14, 20, 17], [8, 11, 13, 19]],
        "Quarterly Performance",
        "Revenue (M)",
        ["2024", "2025", "2026"],
        name="demo_grouped_bar",
    )
    paths.append(p)

    return paths


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_data(raw: str) -> tuple[list[str], list[float]]:
    """Parse 'A:10,B:20,C:15' into categories and values."""
    cats, vals = [], []
    for pair in raw.split(","):
        k, v = pair.strip().split(":")
        cats.append(k.strip())
        vals.append(float(v.strip()))
    return cats, vals


def main():
    parser = argparse.ArgumentParser(description="Dark Academic Chart Generator")
    parser.add_argument("--type", choices=["bar", "line", "scatter", "pie", "grouped_bar"],
                        default="bar", help="Chart type")
    parser.add_argument("--title", default="Chart", help="Chart title")
    parser.add_argument("--data", help="Data as 'A:10,B:20,C:15'")
    parser.add_argument("--ylabel", default="Value")
    parser.add_argument("--xlabel", default="X")
    parser.add_argument("--name", default=None, help="Output filename (without .png)")
    parser.add_argument("--demo", action="store_true", help="Generate demo charts")
    args = parser.parse_args()

    if args.demo:
        paths = run_demo()
        for p in paths:
            print(f"  {p}")
        return

    if not args.data:
        parser.error("--data is required (unless --demo)")

    cb = ChartBuilder()
    cats, vals = parse_data(args.data)
    out_name = args.name or args.type + "_chart"

    if args.type == "bar":
        p = cb.bar_chart(cats, vals, args.title, args.ylabel, name=out_name)
    elif args.type == "pie":
        p = cb.pie_chart(cats, vals, args.title, name=out_name)
    elif args.type == "line":
        p = cb.line_chart(cats, [vals], args.title, args.xlabel, args.ylabel, name=out_name)
    elif args.type == "scatter":
        p = cb.scatter_plot(vals, vals, args.title, args.xlabel, args.ylabel, name=out_name)
    elif args.type == "grouped_bar":
        p = cb.grouped_bar(cats, [vals], args.title, args.ylabel, ["Group 1"], name=out_name)

    print(f"  {p}")


if __name__ == "__main__":
    main()

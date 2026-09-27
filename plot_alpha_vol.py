#!/usr/bin/env python3
"""Recreate Zhu–He–Cucuringu (2026) Figure 2–style alpha vs volatility chart.

Reads Zenodo replication CSV alpha_vol_points_v3_cal6913.csv and plots
annualized FF5+MOM alpha against book volatility for the 12 clusterizers
and the K=1 / random controls (trained / neural-head component).

Data source:
  https://doi.org/10.5281/zenodo.22241254
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

LABELS = {
    "kmeans_ret": "k-means",
    "pca_load": "PCA loadings",
    "agglo_avg": "Average linkage",
    "agglo_complete": "Complete linkage",
    "spectral_unsigned": "Spectral (unsigned)",
    "gics": "GICS",
    "sponge_w60": "sponge",
    "fv2a_w60": "Sharpe (EW)",
    "fv3sm_w60": "Sharpe (graph)",
    "sharpe_fixed_w60": "Sharpe",
    "sortino_w60": "Sortino",
    "sssnetpre": "sssnet",
    "k1": "No clustering (K = 1)",
    "random": "Random partition",
}

CONTROLS = {"k1", "random"}
HIGHLIGHT = {"kmeans_ret", "gics", "spectral_unsigned"}


def load_points(csv_path: Path) -> list[dict]:
    with csv_path.open(newline="") as f:
        return list(csv.DictReader(f))


def plot(rows: list[dict], out_path: Path) -> None:
    clust = [r for r in rows if r["arm"] not in CONTROLS]
    ctrl = [r for r in rows if r["arm"] in CONTROLS]

    fig, ax = plt.subplots(figsize=(8.5, 6.2), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#fafafa")

    for r in clust:
        vol, alpha = float(r["vol"]), float(r["alpha"])
        label = LABELS.get(r["arm"], r["arm"])
        if r["arm"] in HIGHLIGHT:
            ax.scatter(
                vol, alpha, s=70, c="#1f4e79", zorder=3, edgecolors="white", linewidths=0.6
            )
            ax.annotate(
                label,
                (vol, alpha),
                textcoords="offset points",
                xytext=(6, 4),
                fontsize=8,
                color="#1f4e79",
            )
        else:
            ax.scatter(
                vol,
                alpha,
                s=55,
                c="#4a90c7",
                zorder=2,
                edgecolors="white",
                linewidths=0.5,
                alpha=0.95,
            )

    for r in ctrl:
        vol, alpha = float(r["vol"]), float(r["alpha"])
        label = LABELS[r["arm"]]
        ax.scatter(
            vol, alpha, s=90, c="#c0392b", marker="s", zorder=4, edgecolors="white", linewidths=0.7
        )
        ax.annotate(
            label,
            (vol, alpha),
            textcoords="offset points",
            xytext=(-8, 6) if r["arm"] == "k1" else (-8, -12),
            fontsize=8.5,
            color="#c0392b",
            ha="right",
        )

    ax.set_xlabel("Annualized volatility of the book (%)", fontsize=11)
    ax.set_ylabel("Annualized alpha (%/yr, FF5+MOM)", fontsize=11)
    ax.set_title(
        "Alpha vs volatility — trained component\n"
        "(recreated from Zenodo alpha_vol_points_v3_cal6913.csv)",
        fontsize=12,
        pad=10,
    )
    ax.grid(True, linestyle=":", alpha=0.55)
    ax.set_xlim(2.6, 5.4)
    ax.set_ylim(5.1, 7.3)

    legend_elems = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor="#4a90c7",
            markersize=8,
            label="12 clusterizers",
        ),
        Line2D(
            [0],
            [0],
            marker="s",
            color="w",
            markerfacecolor="#c0392b",
            markersize=8,
            label="Controls (K=1, random)",
        ),
    ]
    ax.legend(handles=legend_elems, loc="lower left", frameon=True, fontsize=9)
    ax.text(
        0.98,
        0.02,
        "Zhu, He, Cucuringu (2026) · Figure 2 style · Zenodo 10.5281/zenodo.22241254",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=7,
        color="#666666",
    )

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, bbox_inches="tight")
    print(f"Wrote {out_path}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--csv",
        type=Path,
        default=Path("data/alpha_vol_points_v3_cal6913.csv"),
        help="Path to alpha_vol_points_v3_cal6913.csv",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=Path("fig2_alpha_vol_recreated.png"),
        help="Output PNG path",
    )
    args = p.parse_args()
    if not args.csv.is_file():
        raise SystemExit(
            f"CSV not found: {args.csv}\n"
            "Download from https://doi.org/10.5281/zenodo.22241254 "
            "(results.tar.gz → analysis/results/alpha_vol_points_v3_cal6913.csv)"
        )
    plot(load_points(args.csv), args.out)


if __name__ == "__main__":
    main()

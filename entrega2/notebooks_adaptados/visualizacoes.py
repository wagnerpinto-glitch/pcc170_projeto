from __future__ import annotations

from pathlib import Path
from typing import Mapping, Sequence

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import colors
from matplotlib.cm import ScalarMappable
from IPython.display import Image as IPyImage, display


FIGURES_DIR = Path(__file__).resolve().parent / "figuras"
YATES = ["(1)", "a", "b", "ab", "c", "ac", "bc", "abc"]
CELLS = [
    (a, b, c)
    for c in (-1, 1)
    for b in (-1, 1)
    for a in (-1, 1)
]


def configure_plots() -> None:
    sns.set_theme(style="whitegrid", context="notebook", palette="colorblind")
    plt.rcParams.update({
        "figure.dpi": 120,
        "savefig.facecolor": "white",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.titleweight": "semibold",
        "axes.labelsize": 10,
        "axes.titlesize": 12,
    })


def save_figure(fig: plt.Figure, name: str) -> None:
    if not name or Path(name).name != name:
        raise ValueError("O nome da figura deve ser um nome de arquivo, sem diretórios.")
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    png_path = FIGURES_DIR / f"{name}.png"
    pdf_path = FIGURES_DIR / f"{name}.pdf"
    fig.tight_layout()
    fig.savefig(png_path, dpi=180, bbox_inches="tight")
    fig.savefig(pdf_path, dpi=600, bbox_inches="tight")
    print(f"Figura salva: {png_path.name} (PNG) e {pdf_path.name} (PDF)")
    display(IPyImage(filename=str(png_path)))
    plt.close(fig)

def plot_factorial_cube(
    cell_means: Mapping[tuple[int, int, int], float],
    cell_counts: Mapping[tuple[int, int, int], int],
) -> plt.Figure:
    missing = set(CELLS).difference(cell_means) | set(CELLS).difference(cell_counts)
    if missing:
        raise ValueError(f"Faltam células fatoriais: {sorted(missing)}")

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")
    values = np.asarray([cell_means[cell] for cell in CELLS], dtype=float)
    norm = colors.Normalize(vmin=float(values.min()), vmax=float(values.max()))
    cmap = plt.get_cmap("RdYlGn")
    positions = {
        cell: (
            (cell[0] + 1) / 2 + 0.34 * (cell[2] + 1) / 2,
            (cell[1] + 1) / 2 + 0.26 * (cell[2] + 1) / 2,
            (cell[2] + 1) / 2,
        )
        for cell in CELLS
    }

    for i, first in enumerate(CELLS):
        for second in CELLS[i + 1:]:
            if sum(left != right for left, right in zip(first, second)) == 1:
                ax.plot(
                    [positions[first][0], positions[second][0]],
                    [positions[first][1], positions[second][1]],
                    [positions[first][2], positions[second][2]],
                    color="#9aa3aa",
                    linewidth=1.2,
                    zorder=1,
                )

    for i, cell in enumerate(CELLS):
        x, y, z = positions[cell]
        ax.scatter(
            x, y, z,
            s=110,
            c=[cmap(norm(cell_means[cell]))],
            edgecolor="white",
            linewidth=1.2,
            depthshade=False,
            zorder=3,
        )
        ax.text(
            x, y, z + 0.07,
            f"{YATES[i]}\nμ={cell_means[cell]:.3f}\nn={cell_counts[cell]}",
            ha="center",
            va="bottom",
            fontsize=8,
            bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "alpha": 0.82, "edgecolor": "none"},
        )

    ax.set(
        xlabel="A — IA (−1 ativo; +1 passivo)",
        ylabel="B — ansiedade (−1 baixa; +1 alta)",
        zlabel="C — estudo (−1 baixo; +1 alto)",
        title="Cubo fatorial 2³ — média observada de ΔGPA por célula",
    )
    ax.set_xticks([0, 1], ["−1", "+1"])
    ax.set_yticks([0, 1], ["−1", "+1"])
    ax.set_zticks([0, 1], ["−1", "+1"])
    ax.view_init(elev=24, azim=-58)
    colorbar = fig.colorbar(
        ScalarMappable(norm=norm, cmap=cmap),
        ax=ax,
        shrink=0.68,
        pad=0.12,
    )
    colorbar.set_label("Média de ΔGPA")
    fig.subplots_adjust(left=0, right=0.88, bottom=0.02, top=0.9)
    return fig


def plot_cell_counts(
    counts: Sequence[int],
    labels: Sequence[str] = YATES,
    *,
    title: str = "Número de alunos por célula",
) -> plt.Figure:
    if len(counts) != len(labels) or not counts:
        raise ValueError("Informe uma contagem para cada rótulo de célula.")
    values = np.asarray(counts, dtype=int)
    fig, ax = plt.subplots(figsize=(9, 4.2))
    palette = sns.color_palette("colorblind", len(values))
    bars = ax.bar(labels, values, color=palette, edgecolor="white")
    ax.axhline(values.mean(), color="#34495e", linestyle="--", linewidth=1.2,
               label=f"Média = {values.mean():.0f}")
    ax.bar_label(bars, padding=3, fontsize=9)
    ax.set(
        xlabel="Célula (ordem de Yates)",
        ylabel="Alunos",
        title=title,
    )
    ax.legend(frameon=False)
    ax.margins(y=0.14)
    return fig


def plot_quality_dashboard(
    labels: Sequence[str],
    counts: Sequence[int],
) -> plt.Figure:
    if len(labels) != len(counts) or not labels:
        raise ValueError("Informe uma contagem para cada verificação.")
    fig, ax = plt.subplots(figsize=(9, 3.8))
    positions = np.arange(len(labels))
    colors_ = ["#2e8b57" if count == 0 else "#c0392b" for count in counts]
    ax.barh(positions, [1] * len(labels), color=colors_, alpha=0.18, height=0.62)
    for position, (label, count, color) in enumerate(zip(labels, counts, colors_)):
        status = "OK" if count == 0 else "VERIFICAR"
        marker = "✓" if count == 0 else "!"
        ax.scatter(0.06, position, s=220, color=color, marker="o", zorder=3)
        ax.text(0.06, position, marker, ha="center", va="center",
                color="white", fontsize=10, fontweight="bold", zorder=4)
        ax.text(0.14, position, f"{label} — {status} (n={count})",
                va="center", fontsize=10)
    ax.set_xlim(0, 1)
    ax.set_ylim(len(labels) - 0.5, -0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Auditoria de integridade da base")
    for spine in ax.spines.values():
        spine.set_visible(False)
    return fig


def plot_protocol_flow(
    counts: Sequence[int],
    labels: Sequence[str],
) -> plt.Figure:
    if len(counts) != len(labels) or len(counts) < 2:
        raise ValueError("O fluxo precisa de pelo menos duas etapas com contagens.")
    fig, ax = plt.subplots(figsize=(11, 3.4))
    x_positions = np.linspace(0.12, 0.88, len(counts))
    colors_ = sns.color_palette("colorblind", len(counts))
    for i, (x, count, label, color) in enumerate(zip(x_positions, counts, labels, colors_)):
        ax.text(
            x, 0.55, f"{count:,}",
            ha="center", va="center", fontsize=18, fontweight="bold",
            color=color,
            bbox={"boxstyle": "round,pad=0.55", "facecolor": "white", "edgecolor": color, "linewidth": 1.7},
        )
        ax.text(x, 0.2, label, ha="center", va="center", fontsize=9, wrap=True)
        if i < len(counts) - 1:
            ax.annotate(
                "",
                xy=(x_positions[i + 1] - 0.08, 0.55),
                xytext=(x + 0.08, 0.55),
                arrowprops={"arrowstyle": "->", "color": "#7f8c8d", "lw": 1.5},
            )
    ax.set_title("Fluxo de seleção e preparação da análise")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.9)
    ax.axis("off")
    return fig

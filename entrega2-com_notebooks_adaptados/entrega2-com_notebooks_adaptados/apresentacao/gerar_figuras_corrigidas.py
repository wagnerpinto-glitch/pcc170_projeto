from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração visual elegante e nítida
sns.set_theme(style="whitegrid", context="talk", palette="colorblind")
plt.rcParams.update({
    "figure.dpi": 160,
    "savefig.facecolor": "white",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.titleweight": "bold",
    "axes.labelsize": 13,
    "axes.titlesize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
})

BASE_DIR = Path(__file__).resolve().parent
DIRS = [
    BASE_DIR / "figuras",
    BASE_DIR.parent / "notebooks_adaptados" / "figuras",
    Path("/home/wagner/pcc170/apresentacao/figuras"),
    Path("/home/wagner/pcc170/notebooks_adaptados/figuras"),
    Path("/home/wagner/.gemini/antigravity/brain/47239ddd-c033-461b-a496-e2b52659d86a/figuras"),
]
for d in DIRS:
    d.mkdir(parents=True, exist_ok=True)

def salvar(fig, nome):
    fig.tight_layout()
    for d in DIRS:
        fig.savefig(d / f"{nome}.png", dpi=220, bbox_inches="tight")
        fig.savefig(d / f"{nome}.pdf", dpi=300, bbox_inches="tight")
    print(f"Salvo com sucesso: {nome}")
    plt.close(fig)

def plot_main_effect(level_labels, means, intervals, color, title, xlabel, output_name):
    fig, (ax, ax_summary) = plt.subplots(
        2, 1, figsize=(7.0, 5.8), gridspec_kw={"height_ratios": [4.6, 1.2]}
    )
    ax.errorbar(
        [-1, 1],
        means,
        yerr=[
            [means[0] - intervals[0][0], means[1] - intervals[1][0]],
            [intervals[0][1] - means[0], intervals[1][1] - means[1]],
        ],
        fmt="-o",
        markersize=10,
        linewidth=2.8,
        capsize=7,
        capthick=2,
        color=color,
        ecolor=color,
    )
    ax.set_xticks([-1, 1], level_labels)
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(
        min(0.12, intervals[0][0], intervals[1][0]) - 0.01,
        max(0.35, intervals[0][1], intervals[1][1]) + 0.01,
    )
    ax.set(
        title=title,
        xlabel=xlabel,
        ylabel="Média Balanceada de ΔGPA",
    )

    ax_summary.axis("off")
    summary = ax_summary.table(
        cellText=[
            [level_labels[0], f"{means[0]:.3f}", f"[{intervals[0][0]:.3f}; {intervals[0][1]:.3f}]"],
            [level_labels[1], f"{means[1]:.3f}", f"[{intervals[1][0]:.3f}; {intervals[1][1]:.3f}]"],
        ],
        colLabels=["Nível", "Média", "IC 95%"],
        cellLoc="center",
        colLoc="center",
        colWidths=[0.30, 0.20, 0.42],
        loc="center",
    )
    summary.auto_set_font_size(False)
    summary.set_fontsize(9)
    summary.scale(1, 1.25)
    salvar(fig, output_name)

# Carregar dados
csv_path = Path("/home/wagner/pcc170/csv/ai_student_impact_dataset.csv")
if not csv_path.exists():
    for candidate in (
        BASE_DIR.parent / "csv" / "ai_student_impact_dataset.csv",
        BASE_DIR.parent.parent / "csv" / "ai_student_impact_dataset.csv",
    ):
        if candidate.exists():
            csv_path = candidate
            break
df = pd.read_csv(csv_path)

# Carregar tabela canônica de efeitos e ICs, se disponível
dados_path = next(
    (p for p in (
        BASE_DIR.parent / "dados" / "efeitos_ic.csv",
        BASE_DIR.parent.parent / "dados" / "efeitos_ic.csv",
        Path("/home/wagner/pcc170/dados/efeitos_ic.csv"),
    ) if p.exists()),
    None,
)
df_efeitos = pd.read_csv(dados_path, index_col=0) if dados_path else None

df["Delta_GPA"] = df["Post_Semester_GPA"] - df["Pre_Semester_GPA"]
PASSIVE_USE_CASES = {"Copywriting/Drafting", "Direct_Answer_Generation"}
df["A"] = np.where(df["Primary_Use_Case"].isin(PASSIVE_USE_CASES), 1, -1)
stem_junior = df.loc[
    (df["Major_Category"] == "STEM") & (df["Year_of_Study"] == "Junior")
].copy()

ANXIETY_Q2 = stem_junior["Anxiety_Level_During_Exams"].median()
STUDY_Q2 = stem_junior["Traditional_Study_Hours"].median()
stem_junior["B"] = np.where(
    stem_junior["Anxiety_Level_During_Exams"] > ANXIETY_Q2, 1, -1
)
stem_junior["C"] = np.where(
    stem_junior["Traditional_Study_Hours"] > STUDY_Q2, 1, -1
)
factorial = stem_junior.copy()

CELLS = [
    (a, b, c)
    for c in (-1, 1)
    for b in (-1, 1)
    for a in (-1, 1)
]
groups = {
    key: frame["Delta_GPA"].to_numpy()
    for key, frame in factorial.groupby(["A", "B", "C"], sort=False)
}
cell_means = {cell: groups[cell].mean() for cell in CELLS}

def equal_cell_mean(fixed_levels):
    selected = [
        cell_means[cell]
        for cell in CELLS
        if all(cell[index] == level for index, level in fixed_levels.items())
    ]
    return float(np.mean(selected))

# -------------------------------------------------------------
# 1. EFEITOS PRINCIPAIS INDIVIDUAIS COM INTERVALOS DE CONFIANÇA (IC95% BOOTSTRAP)
# -------------------------------------------------------------
# Bootstrap estratificado para IC95% das médias marginais e efeitos
N_BOOT = 5000
rng = np.random.default_rng(42)
boot_marginal_means = {0: {-1: [], 1: []}, 1: {-1: [], 1: []}, 2: {-1: [], 1: []}}
boot_effects_dict = {0: [], 1: [], 2: []}

for _ in range(N_BOOT):
    b_means = {cell: groups[cell][rng.integers(0, len(groups[cell]), len(groups[cell]))].mean() for cell in CELLS}
    for idx in range(3):
        m_neg = np.mean([b_means[cell] for cell in CELLS if cell[idx] == -1])
        m_pos = np.mean([b_means[cell] for cell in CELLS if cell[idx] == 1])
        boot_marginal_means[idx][-1].append(m_neg)
        boot_marginal_means[idx][1].append(m_pos)
        boot_effects_dict[idx].append(m_pos - m_neg)

# Fator A
mA_neg = equal_cell_mean({0: -1})
mA_pos = equal_cell_mean({0: 1})
efeito_A = mA_pos - mA_neg
ci_mA_neg = np.quantile(boot_marginal_means[0][-1], [0.025, 0.975])
ci_mA_pos = np.quantile(boot_marginal_means[0][1], [0.025, 0.975])

if df_efeitos is not None and "A" in df_efeitos.index:
    ic_ef_A = [df_efeitos.loc["A", "ic95_inf"], df_efeitos.loc["A", "ic95_sup"]]
else:
    ic_ef_A = np.quantile(boot_effects_dict[0], [0.025, 0.975])

plot_main_effect(
    ["Ativo (−1)", "Passivo (+1)"],
    [mA_neg, mA_pos],
    [ci_mA_neg, ci_mA_pos],
    "#1f77b4",
    (f"Efeito Principal A (Modo de Uso de IA)\n"
     f"Δ = {efeito_A:.3f}  [IC95%: {ic_ef_A[0]:+.3f}; {ic_ef_A[1]:+.3f}]\n"
     "p(HC3) < 0.0001 (Significativo)"),
    "Nível do Fator A",
    "06_efeito_principal_A",
)

# Fator B
mB_neg = equal_cell_mean({1: -1})
mB_pos = equal_cell_mean({1: 1})
efeito_B = mB_pos - mB_neg
ci_mB_neg = np.quantile(boot_marginal_means[1][-1], [0.025, 0.975])
ci_mB_pos = np.quantile(boot_marginal_means[1][1], [0.025, 0.975])

if df_efeitos is not None and "B" in df_efeitos.index:
    ic_ef_B = [df_efeitos.loc["B", "ic95_inf"], df_efeitos.loc["B", "ic95_sup"]]
else:
    ic_ef_B = np.quantile(boot_effects_dict[1], [0.025, 0.975])

plot_main_effect(
    ["Baixa (−1)", "Alta (+1)"],
    [mB_neg, mB_pos],
    [ci_mB_neg, ci_mB_pos],
    "#e67e22",
    (f"Efeito Principal B (Ansiedade em Provas)\n"
     f"Δ = {efeito_B:.3f}  [IC95%: {ic_ef_B[0]:+.3f}; {ic_ef_B[1]:+.3f}]\n"
     "p(HC3) = 0.0268 (Significativo)"),
    "Nível do Fator B",
    "06_efeito_principal_B",
)

# Fator C
mC_neg = equal_cell_mean({2: -1})
mC_pos = equal_cell_mean({2: 1})
efeito_C = mC_pos - mC_neg
ci_mC_neg = np.quantile(boot_marginal_means[2][-1], [0.025, 0.975])
ci_mC_pos = np.quantile(boot_marginal_means[2][1], [0.025, 0.975])

if df_efeitos is not None and "C" in df_efeitos.index:
    ic_ef_C = [df_efeitos.loc["C", "ic95_inf"], df_efeitos.loc["C", "ic95_sup"]]
else:
    ic_ef_C = np.quantile(boot_effects_dict[2], [0.025, 0.975])

plot_main_effect(
    ["Baixo (−1)", "Alto (+1)"],
    [mC_neg, mC_pos],
    [ci_mC_neg, ci_mC_pos],
    "#27ae60",
    (f"Efeito Principal C (Estudo Tradicional)\n"
     f"Δ = +{efeito_C:.3f}  [IC95%: {ic_ef_C[0]:+.3f}; {ic_ef_C[1]:+.3f}]\n"
     "p(HC3) < 0.0001 (Dominante)"),
    "Nível do Fator C",
    "06_efeito_principal_C",
)

# -------------------------------------------------------------
# 2. INTERAÇÕES INDIVIDUAIS COM EIXOS E LEGENDAS TOTALMENTE LIVRES
# -------------------------------------------------------------
# Bootstrap estratificado das médias das 8 células, reutilizado nas interações
rng_int = np.random.default_rng(43)
boot_cells = np.array([
    [groups[cell][rng_int.integers(0, len(groups[cell]), len(groups[cell]))].mean() for cell in CELLS]
    for _ in range(N_BOOT)
])

def plot_interaction(x_idx, t_idx, x_labels, trace_specs, title, xlabel, output_name):
    """trace_specs: lista de (nível do traço, rótulo, cor, marcador, estilo de linha)."""
    fig, (ax, ax_summary) = plt.subplots(
        2, 1, figsize=(7.2, 6.8), gridspec_kw={"height_ratios": [4.2, 2.0]}
    )
    rows, lows, highs = [], [], []
    offsets = np.linspace(-0.035, 0.035, len(trace_specs))
    for (t_lvl, label, color, marker, ls), off in zip(trace_specs, offsets):
        means, cis = [], []
        for x_lvl in (-1, 1):
            mask = np.array([c[x_idx] == x_lvl and c[t_idx] == t_lvl for c in CELLS])
            means.append(float(cell_means_arr[mask].mean()))
            cis.append(np.quantile(boot_cells[:, mask].mean(axis=1), [0.025, 0.975]))
        ax.errorbar(
            np.array([-1, 1]) + off, means,
            yerr=[[m - c[0] for m, c in zip(means, cis)], [c[1] - m for m, c in zip(means, cis)]],
            fmt=marker, linestyle=ls, markersize=9, linewidth=2.5, capsize=6, capthick=2,
            color=color, ecolor=color, label=label,
        )
        for x_label, m, c in zip(x_labels, means, cis):
            rows.append([label, x_label, f"{m:.3f}", f"[{c[0]:.3f}; {c[1]:.3f}]"])
        lows += [c[0] for c in cis]
        highs += [c[1] for c in cis]
    span = max(highs) - min(lows)
    ax.set_ylim(min(lows) - 0.06 * span, max(highs) + 0.32 * span)
    ax.set_xticks([-1, 1], x_labels)
    ax.set_xlim(-1.45, 1.45)
    ax.set(title=title, xlabel=xlabel, ylabel="Média Balanceada de ΔGPA")
    ax.legend(loc="upper center", ncol=2, frameon=True, framealpha=0.96,
              facecolor="white", edgecolor="#aaaaaa", fontsize=10)

    ax_summary.axis("off")
    tbl = ax_summary.table(
        cellText=rows,
        colLabels=["Série", "Nível", "Média", "IC 95%"],
        cellLoc="center", colLoc="center",
        colWidths=[0.34, 0.22, 0.14, 0.26], loc="center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.2)
    salvar(fig, output_name)

cell_means_arr = np.array([cell_means[c] for c in CELLS])

plot_interaction(
    0, 1, ["Ativo (−1)", "Passivo (+1)"],
    [(-1, "Ansiedade Baixa (B = −1)", "#2ca02c", "o", "-"),
     (1, "Ansiedade Alta (B = +1)", "#d62728", "s", "--")],
    "Interação A × B (Modo IA × Ansiedade)\nEfeito = −0.0226 (p = 0.0041: Significativa)",
    "Modo de Uso de IA (Fator A)", "06_interacao_AB",
)
plot_interaction(
    0, 2, ["Ativo (−1)", "Passivo (+1)"],
    [(1, "Estudo Alto (C = +1)", "#17becf", "s", "-"),
     (-1, "Estudo Baixo (C = −1)", "#8c564b", "o", "--")],
    "Interação A × C (Modo IA × Estudo Tradicional)\nEfeito = −0.0005 (p = 0.9507: Retas Paralelas)",
    "Modo de Uso de IA (Fator A)", "06_interacao_AC",
)
plot_interaction(
    1, 2, ["Baixa (−1)", "Alta (+1)"],
    [(1, "Estudo Alto (C = +1)", "#17becf", "s", "-"),
     (-1, "Estudo Baixo (C = −1)", "#8c564b", "o", "--")],
    "Interação B × C (Ansiedade × Estudo Tradicional)\nEfeito = +0.0107 (p = 0.1766: Retas Paralelas)",
    "Ansiedade em Provas (Fator B)", "06_interacao_BC",
)

# -------------------------------------------------------------
# 3. RESUMO DOS DIAGNÓSTICOS (slide 15/16)
# -------------------------------------------------------------
diagnostic_rows = [
    ("Normalidade dos resíduos (Shapiro-Wilk)", "W = 0,999; p = 0,115", "Atendido", "ok"),
    ("Variância dos dados brutos (Levene)", "F = 4,73; p = 2,6×10⁻⁵", "Heterocedástico → HC3", "warn"),
    ("Variância nas réplicas bootstrap (Levene)", "p = 0,044", "Heterocedástico → bootstrap", "warn"),
    ("Estabilidade entre sementes", "Máx. DP = 0,0056", "Atendida", "ok"),
    ("Concordância IC bootstrap × HC3", "sem discordância", "Atendida", "ok"),
    ("Balanceamento do GPA prévio (ANOVA)", "F = 0,82; p > 0,05", "Atendido", "ok"),
]
palette = {"ok": "#2e8b57", "warn": "#d18b24", "fail": "#c0392b"}
fig, ax = plt.subplots(figsize=(11, 4.6))
for i, (label, stat, status, kind) in enumerate(diagnostic_rows):
    ax.barh(i, 1, color=palette[kind], alpha=0.16)
    ax.scatter(0.025, i, s=110, color=palette[kind], zorder=3)
    ax.text(0.055, i, label, va="center", fontsize=10, fontweight="bold")
    ax.text(0.48, i, stat, va="center", fontsize=10)
    ax.text(0.73, i, status, va="center", fontsize=10, color=palette[kind], fontweight="bold")
ax.set_xlim(0, 1)
ax.set_ylim(len(diagnostic_rows) - 0.5, -0.5)
ax.axis("off")
ax.set_title("Resumo dos diagnósticos e tratamento analítico")
salvar(fig, "07_diagnosticos_resumo")

print("Todos os gráficos foram corrigidos e exportados com sucesso!")

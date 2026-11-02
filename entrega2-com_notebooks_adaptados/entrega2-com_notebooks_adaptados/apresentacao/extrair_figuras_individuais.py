from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Configuração visual elegante
sns.set_theme(style="whitegrid", context="talk", palette="colorblind")
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.facecolor": "white",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.titleweight": "semibold",
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 11,
    "legend.title_fontsize": 12,
})

# Pastas de saída
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
        png_path = d / f"{nome}.png"
        pdf_path = d / f"{nome}.pdf"
        fig.savefig(png_path, dpi=200, bbox_inches="tight")
        fig.savefig(pdf_path, dpi=300, bbox_inches="tight")
    print(f"Salvo: {nome}.png e {nome}.pdf")
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

# 1. Carregar dados
csv_path = Path("/home/wagner/pcc170/csv/ai_student_impact_dataset.csv")
df = pd.read_csv(csv_path)

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
cell_number = {cell: number for number, cell in enumerate(CELLS, start=1)}
factorial["celula"] = [
    cell_number[(int(row.A), int(row.B), int(row.C))]
    for row in factorial[["A", "B", "C"]].itertuples(index=False)
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

print(f"Dados carregados. STEM Junior: n={len(stem_junior)}")

# -------------------------------------------------------------
# 2. ECDFs Individuais por Fator
# -------------------------------------------------------------
# Fator A
fig, ax = plt.subplots(figsize=(6.2, 4.4))
for level, label, color, ls in [
    (-1, "Ativo (−1) [Tutoria/Raciocínio]", "#1f77b4", "-"),
    (1, "Passivo (+1) [Copywriting/Direct]", "#d62728", "--"),
]:
    vals = np.sort(stem_junior.loc[stem_junior["A"] == level, "Delta_GPA"].to_numpy())
    cum = np.arange(1, len(vals) + 1) / len(vals)
    ax.step(vals, cum, where="post", label=label, color=color, linestyle=ls, linewidth=2.2)
ax.set(
    title="ECDF: Modo de Uso de IA (Fator A)",
    xlabel="ΔGPA (Variação de Desempenho)",
    ylabel="Probabilidade Acumulada P(ΔGPA ≤ x)",
)
ax.axvline(0, color="#7f8c8d", linestyle=":", linewidth=1.2)
# Legenda no canto superior esquerdo para não sobrepor a curva ascendente
ax.legend(loc="upper left", frameon=True, framealpha=0.92, facecolor="white", edgecolor="#cccccc")
salvar(fig, "02_ecdf_fator_A")

# Fator B
fig, ax = plt.subplots(figsize=(6.2, 4.4))
for level, label, color, ls in [
    (-1, f"Baixa (−1) [≤ {ANXIETY_Q2:g}]", "#2ca02c", "-"),
    (1, f"Alta (+1) [> {ANXIETY_Q2:g}]", "#ff7f0e", "--"),
]:
    vals = np.sort(stem_junior.loc[stem_junior["B"] == level, "Delta_GPA"].to_numpy())
    cum = np.arange(1, len(vals) + 1) / len(vals)
    ax.step(vals, cum, where="post", label=label, color=color, linestyle=ls, linewidth=2.2)
ax.set(
    title="ECDF: Ansiedade em Provas (Fator B)",
    xlabel="ΔGPA (Variação de Desempenho)",
    ylabel="Probabilidade Acumulada P(ΔGPA ≤ x)",
)
ax.axvline(0, color="#7f8c8d", linestyle=":", linewidth=1.2)
ax.legend(loc="upper left", frameon=True, framealpha=0.92, facecolor="white", edgecolor="#cccccc")
salvar(fig, "02_ecdf_fator_B")

# Fator C
fig, ax = plt.subplots(figsize=(6.2, 4.4))
for level, label, color, ls in [
    (-1, f"Baixas (−1) [≤ {STUDY_Q2:.1f}h]", "#8c564b", "-"),
    (1, f"Altas (+1) [> {STUDY_Q2:.1f}h]", "#17becf", "--"),
]:
    vals = np.sort(stem_junior.loc[stem_junior["C"] == level, "Delta_GPA"].to_numpy())
    cum = np.arange(1, len(vals) + 1) / len(vals)
    ax.step(vals, cum, where="post", label=label, color=color, linestyle=ls, linewidth=2.2)
ax.set(
    title="ECDF: Horas de Estudo Tradicional (Fator C)",
    xlabel="ΔGPA (Variação de Desempenho)",
    ylabel="Probabilidade Acumulada P(ΔGPA ≤ x)",
)
ax.axvline(0, color="#7f8c8d", linestyle=":", linewidth=1.2)
ax.legend(loc="upper left", frameon=True, framealpha=0.92, facecolor="white", edgecolor="#cccccc")
salvar(fig, "02_ecdf_fator_C")


# -------------------------------------------------------------
# 3. Efeitos Principais Individuais com IC95% (Bootstrap)
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
mean_A_neg = equal_cell_mean({0: -1})
mean_A_pos = equal_cell_mean({0: 1})
efeito_A = mean_A_pos - mean_A_neg
ci_mA_neg = np.quantile(boot_marginal_means[0][-1], [0.025, 0.975])
ci_mA_pos = np.quantile(boot_marginal_means[0][1], [0.025, 0.975])
ic_ef_A = [-0.0920, -0.0621]
plot_main_effect(
    ["Ativo (−1)", "Passivo (+1)"],
    [mean_A_neg, mean_A_pos],
    [ci_mA_neg, ci_mA_pos],
    "#1f77b4",
    (f"Efeito Principal A (Modo de Uso de IA)\n"
     f"Δ = {efeito_A:.3f}  [IC95%: {ic_ef_A[0]:+.3f}; {ic_ef_A[1]:+.3f}]\n"
     "p(HC3) < 0.0001 (Significativo)"),
    "Nível do Fator A",
    "06_efeito_principal_A",
)

# Fator B
mean_B_neg = equal_cell_mean({1: -1})
mean_B_pos = equal_cell_mean({1: 1})
efeito_B = mean_B_pos - mean_B_neg
ci_mB_neg = np.quantile(boot_marginal_means[1][-1], [0.025, 0.975])
ci_mB_pos = np.quantile(boot_marginal_means[1][1], [0.025, 0.975])
ic_ef_B = [-0.0329, -0.0019]
plot_main_effect(
    ["Baixa (−1)", "Alta (+1)"],
    [mean_B_neg, mean_B_pos],
    [ci_mB_neg, ci_mB_pos],
    "#e67e22",
    (f"Efeito Principal B (Ansiedade em Provas)\n"
     f"Δ = {efeito_B:.3f}  [IC95%: {ic_ef_B[0]:+.3f}; {ic_ef_B[1]:+.3f}]\n"
     "p(HC3) = 0.0268 (Significativo)"),
    "Nível do Fator B",
    "06_efeito_principal_B",
)

# Fator C
mean_C_neg = equal_cell_mean({2: -1})
mean_C_pos = equal_cell_mean({2: 1})
efeito_C = mean_C_pos - mean_C_neg
ci_mC_neg = np.quantile(boot_marginal_means[2][-1], [0.025, 0.975])
ci_mC_pos = np.quantile(boot_marginal_means[2][1], [0.025, 0.975])
ic_ef_C = [+0.1058, +0.1364]
plot_main_effect(
    ["Baixo (−1)", "Alto (+1)"],
    [mean_C_neg, mean_C_pos],
    [ci_mC_neg, ci_mC_pos],
    "#27ae60",
    (f"Efeito Principal C (Estudo Tradicional)\n"
     f"Δ = +{efeito_C:.3f}  [IC95%: {ic_ef_C[0]:+.3f}; {ic_ef_C[1]:+.3f}]\n"
     "p(HC3) < 0.0001 (Dominante)"),
    "Nível do Fator C",
    "06_efeito_principal_C",
)


# -------------------------------------------------------------
# 4. Interações Individuais
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
# 5. Sensibilidade Separada em Duas Figuras
# -------------------------------------------------------------
# Carregar dados de sensibilidade salvos
results_dir = Path("/home/wagner/pcc170/entrega2/dados")
if not results_dir.exists():
    results_dir = Path("/home/wagner/pcc170/docs")

# Criar tabela de sensibilidade direta
sens_data = {
    "termo": ["A", "B", "C", "AB", "AC", "BC", "ABC"],
    "Mediana (Principal, n=3.279)": [-0.0772, -0.0175, 0.1211, -0.0226, -0.0005, 0.0107, 0.0102],
    "Quartis Extremos (<Q1 vs ≥Q3, n=848)": [-0.067, -0.043, 0.195, -0.046, 0.022, 0.004, -0.006],
    "Quartis Extremos (≤Q1 vs ≥Q3, n=1.101)": [-0.080, -0.038, 0.193, -0.033, 0.011, 0.006, 0.005],
}
sens_df = pd.DataFrame(sens_data)

fig, ax = plt.subplots(figsize=(7.2, 4.4))
colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
markers = ["o", "s", "^"]
for idx, col in enumerate(["Mediana (Principal, n=3.279)", "Quartis Extremos (<Q1 vs ≥Q3, n=848)", "Quartis Extremos (≤Q1 vs ≥Q3, n=1.101)"]):
    ax.plot(sens_df["termo"], sens_df[col], marker=markers[idx], markersize=8, linewidth=2.0, color=colors[idx], label=col)
ax.axhline(0, color="#555555", linestyle="--", linewidth=1.2)
ax.set(
    title="Sensibilidade: Contrastes sob Regras Alternativas",
    xlabel="Termo Fatorial",
    ylabel="Efeito Estimado em ΔGPA",
)
ax.legend(loc="upper right", frameon=True, framealpha=0.92, facecolor="white", edgecolor="#cccccc", fontsize=9)
salvar(fig, "07_sensibilidade_efeitos")

# Amostra efetiva
fig, ax = plt.subplots(figsize=(6.2, 3.8))
rules = ["Mediana (Principal)", "≤Q1 vs ≥Q3", "<Q1 vs ≥Q3"]
ns = [3279, 1101, 848]
bars = ax.barh(rules, ns, color=["#1f77b4", "#2ca02c", "#ff7f0e"], height=0.55)
ax.bar_label(bars, fmt="%d alunos", padding=5, fontweight="bold", fontsize=11)
ax.set(
    title="Amostra Efetiva por Regra de Dicotomização",
    xlabel="Número de Estudantes Analisados",
)
ax.set_xlim(0, 3900)
salvar(fig, "07_sensibilidade_amostra")

print("Todas as figuras individuais foram geradas com sucesso!")

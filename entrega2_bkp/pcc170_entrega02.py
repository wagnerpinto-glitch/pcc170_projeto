# %% [markdown]
# # PCC170 – Entrega 2: Fatorial 2³ r com Bootstrap (STEM + Junior)
# Fatores: **A** uso de IA (Passivo +1 / Ativo −1), **B** ansiedade (≥Q3 = +1 / <Q1 = −1),
# **C** horas de estudo (≥Q3 = +1 / <Q1 = −1). Resposta: ΔGPA = Post − Pre.

# %%
import os, warnings
import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
import statsmodels.api as sm, statsmodels.formula.api as smf
from scipy import stats
warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")

CSV = "ai_student_impact_dataset.csv"
if not os.path.exists(CSV):
    for p in ("../csv/ai_student_impact_dataset.csv", "csv/ai_student_impact_dataset.csv"):
        if os.path.exists(p):
            CSV = p
            break
OUT_FIG, OUT_DAT = "figuras", "dados"
os.makedirs(OUT_FIG, exist_ok=True); os.makedirs(OUT_DAT, exist_ok=True)

SEED, R, M, NBOOT = 42, 30, 36, 5000
PASSIVO = ["Copywriting/Drafting", "Direct_Answer_Generation"]
CELLS = [(a, b, c) for c in (-1, 1) for b in (-1, 1) for a in (-1, 1)]  # ordem de Yates
EFFECTS = {"A": lambda k: k[0], "B": lambda k: k[1], "C": lambda k: k[2],
           "AB": lambda k: k[0]*k[1], "AC": lambda k: k[0]*k[2],
           "BC": lambda k: k[1]*k[2], "ABC": lambda k: k[0]*k[1]*k[2]}

def save(name):
    plt.tight_layout(); plt.savefig(f"{OUT_FIG}/{name}.png", dpi=200); plt.show()

# %% [markdown]
# ## 1. Dados: ΔGPA, recorte STEM + Junior, quartis e níveis ±1

# %%
df = pd.read_csv(CSV)
df["Delta_GPA"] = df["Post_Semester_GPA"] - df["Pre_Semester_GPA"]
df["A"] = np.where(df["Primary_Use_Case"].isin(PASSIVO), 1, -1)
s = df[(df.Major_Category == "STEM") & (df.Year_of_Study == "Junior")].copy()
print(f"Dataset: {len(df)} | STEM+Junior: {len(s)}")

an, hr = s["Anxiety_Level_During_Exams"], s["Traditional_Study_Hours"]
qa1, qa3 = an.quantile(.25), an.quantile(.75)
qh1, qh3 = hr.quantile(.25), hr.quantile(.75)
print(f"Ansiedade Q1={qa1} Q3={qa3} | Horas Q1={qh1:.2f} Q3={qh3:.3f}")

s["B"] = np.where(an >= qa3, 1, np.where(an < qa1, -1, 0))
s["C"] = np.where(hr >= qh3, 1, np.where(hr < qh1, -1, 0))
fat = s[(s.B != 0) & (s.C != 0)].copy()
fat["celula"] = [CELLS.index(k) + 1 for k in zip(fat.A, fat.B, fat.C)]
fat.to_csv(f"{OUT_DAT}/df_factorial.csv", index=False)
print(f"Alunos nos níveis extremos: {len(fat)} ({len(fat)/len(s):.1%} do recorte)")

tab = fat.groupby(["celula", "A", "B", "C"]).Delta_GPA.agg(["count", "mean", "std"]).round(3)
print(tab)
G = {k: v["Delta_GPA"].values for k, v in fat.groupby(["A", "B", "C"])}
assert len(G) == 8 and min(len(v) for v in G.values()) >= max(M, 10)

# %% [markdown]
# ### Balanceamento de Pre_GPA e descritivas

# %%
bal = fat.groupby("celula").Pre_Semester_GPA.agg(["mean", "std"]).round(3)
print(bal)
print("ANOVA Pre_GPA ~ célula: p =", round(stats.f_oneway(*[g.Pre_Semester_GPA for _, g in fat.groupby("celula")]).pvalue, 4))
desc = df[["Delta_GPA", "Anxiety_Level_During_Exams", "Traditional_Study_Hours"]].agg(["mean", "std", "min", "max"]).T.round(2)
desc_s = s[["Delta_GPA", "Anxiety_Level_During_Exams", "Traditional_Study_Hours"]].agg(["mean", "std", "min", "max"]).T.round(2)
desc.to_csv(f"{OUT_DAT}/descritivas_dataset.csv"); desc_s.to_csv(f"{OUT_DAT}/descritivas_stem_junior.csv")
print(desc, "\n", desc_s)

# %% [markdown]
# ## 2. Gráficos exploratórios

# %%
fig, ax = plt.subplots(1, 3, figsize=(16, 4.5))
sns.histplot(s.Delta_GPA, kde=True, ax=ax[0], color="#2980b9"); ax[0].set_title("ΔGPA (STEM Junior)")
sns.histplot(an, discrete=True, ax=ax[1], color="#e67e22")
for q, c in ((qa1, "green"), (qa3, "red")): ax[1].axvline(q, color=c, ls="--", label=f"Q={q:g}")
ax[1].set_title("Ansiedade com Q1/Q3"); ax[1].legend()
sns.histplot(hr, kde=True, ax=ax[2], color="#8e44ad")
for q, c in ((qh1, "green"), (qh3, "red")): ax[2].axvline(q, color=c, ls="--", label=f"Q={q:.2f}")
ax[2].set_title("Horas de estudo com Q1/Q3"); ax[2].legend()
save("01_distribuicoes_quartis")

# %%
n_tab = fat.groupby(["A", "B", "C"]).size().unstack("C")
plt.figure(figsize=(6, 4)); sns.heatmap(n_tab, annot=True, fmt="d", cmap="Blues")
plt.title("n por célula (linhas A,B / colunas C)"); save("02_n_por_celula")

# %%
fat["rotulo"] = fat.celula.astype(str) + " (" + fat.A.map({-1: "At", 1: "Ps"}) + "," + fat.B.map({-1: "B", 1: "A"}) + "," + fat.C.map({-1: "b", 1: "a"}) + ")"
plt.figure(figsize=(12, 5)); sns.boxplot(data=fat.sort_values("celula"), x="rotulo", y="Delta_GPA", palette="viridis")
plt.xticks(rotation=30); plt.xlabel("Célula (IA, Ansiedade, Estudo)"); save("03_boxplot_bruto_por_celula")

# %% [markdown]
# ### CDF empírica dos dados analisados

# %%
def ecdf(x):
    x = np.sort(np.asarray(x)); return x, np.arange(1, len(x) + 1) / len(x)

rot_a = {-1: "Ativo", 1: "Passivo"}
fig, ax = plt.subplots(1, 3, figsize=(17, 4.8))
for lvl, g in fat.groupby("A"):
    ax[0].step(*ecdf(g.Delta_GPA), where="post", label=f"{rot_a[lvl]} (n={len(g)})")
ax[0].set_xlabel("ΔGPA"); ax[0].set_title("CDF do ΔGPA por tipo de uso de IA (n=848)")
for lvl, g in fat.groupby("B"):
    ax[1].step(*ecdf(g.Delta_GPA), where="post", label=f"Ansiedade {'alta' if lvl == 1 else 'baixa'} (n={len(g)})")
ax[1].set_xlabel("ΔGPA"); ax[1].set_title("CDF do ΔGPA por nível de ansiedade")
for lvl, g in fat.groupby("C"):
    ax[2].step(*ecdf(g.Delta_GPA), where="post", label=f"Estudo {'alto' if lvl == 1 else 'baixo'} (n={len(g)})")
ax[2].set_xlabel("ΔGPA"); ax[2].set_title("CDF do ΔGPA por nível de horas de estudo")
for a_ in ax: a_.set_ylabel("F(x) = P(ΔGPA ≤ x)"); a_.legend(loc="lower right")
save("15_cdf_fatores")

# %%
fig, ax = plt.subplots(1, 2, figsize=(15, 5))
for i, k in enumerate(CELLS):
    lab = f"{i+1}: {rot_a[k[0]][:2]}, Ans{'+' if k[1] == 1 else '-'}, Est{'+' if k[2] == 1 else '-'} (n={len(G[k])})"
    ax[0].step(*ecdf(G[k]), where="post", label=lab)
ax[0].set_title("CDF do ΔGPA bruto por célula 2³"); ax[0].set_xlabel("ΔGPA")
ax[1].set_title("CDF – recorte STEM Junior completo vs. 848 analisados")
ax[1].step(*ecdf(s.Delta_GPA), where="post", label=f"STEM Junior (n={len(s)})")
ax[1].step(*ecdf(fat.Delta_GPA), where="post", label=f"Extremos Q1/Q3 (n={len(fat)})")
ax[1].set_xlabel("ΔGPA")
for a_ in ax: a_.set_ylabel("F(x)"); a_.legend(fontsize=8, loc="lower right")
save("16_cdf_por_celula_e_recorte")

# %%
fig, ax = plt.subplots(1, 2, figsize=(15, 5))
for var, nome, q1, q3, a_ in ((an, "Ansiedade", qa1, qa3, ax[0]), (hr, "Horas de estudo", qh1, qh3, ax[1])):
    a_.step(*ecdf(var), where="post", color="#2c3e50")
    a_.axvline(q1, color="green", ls="--", label=f"Q1={q1:.2f} (F=0,25)"); a_.axvline(q3, color="red", ls="--", label=f"Q3={q3:.2f} (F=0,75)")
    a_.axhline(.25, color="gray", lw=.6); a_.axhline(.75, color="gray", lw=.6)
    a_.set_xlabel(nome); a_.set_ylabel("F(x)"); a_.set_title(f"CDF – {nome} (STEM Junior) com cortes"); a_.legend()
save("17_cdf_ansiedade_horas_quartis")

# %% [markdown]
# ## 3. Ciclo 1 – Réplicas bootstrap (r × 8 células, m alunos com reposição) + ANOVA 2³

# %%
def make_replicas(G, r, m, seed):
    rng = np.random.default_rng(seed); rows = []
    for k in CELLS:
        for j in range(r):
            idx = rng.integers(0, len(G[k]), m)
            rows.append(dict(A=k[0], B=k[1], C=k[2], celula=CELLS.index(k) + 1, rep=j + 1,
                             seed=seed, Y=G[k][idx].mean(), sd_amostra=G[k][idx].std(ddof=1),
                             distintos=len(set(idx))))
    return pd.DataFrame(rows)

def effects_from_means(mu):
    return {n: sum(f(k) * mu[k] for k in CELLS) / 4 for n, f in EFFECTS.items()}

rep = make_replicas(G, R, M, SEED)
rep.to_csv(f"{OUT_DAT}/replicas.csv", index=False)
print(rep.shape, "| mín. de alunos distintos por réplica:", rep.distintos.min())

mod = smf.ols("Y ~ A*B*C", rep).fit()
anova = sm.stats.anova_lm(mod, typ=2)
anova["pct_var"] = anova.sum_sq / anova.sum_sq.sum() * 100
anova.to_csv(f"{OUT_DAT}/anova_bootstrap.csv"); print(anova.round(5))
ef_anova = {n.replace(":", ""): 2 * mod.params[n] for n in mod.params.index if n != "Intercept"}

# %% [markdown]
# ### Validação das premissas (Ciclo 1)

# %%
res = mod.resid
sh = stats.shapiro(res); lev = stats.levene(*[g.Y.values for _, g in rep.groupby("celula")])
# normalidade dos dados brutos x médias bootstrap, célula a célula
norm_tab = pd.DataFrame({
    "n": [len(G[k]) for k in CELLS],
    "skew_bruto": [stats.skew(G[k]) for k in CELLS],
    "shapiro_p_bruto": [stats.shapiro(G[k]).pvalue for k in CELLS],
    "skew_boot": [stats.skew(rep[rep.celula == i + 1].Y) for i in range(8)],
    "shapiro_p_boot": [stats.shapiro(rep[rep.celula == i + 1].Y).pvalue for i in range(8)]}, index=range(1, 9)).round(3)
norm_tab.to_csv(f"{OUT_DAT}/normalidade_por_celula.csv"); print(norm_tab)
print(f"Shapiro resíduos: p={sh.pvalue:.3f} ({'OK' if sh.pvalue > .05 else 'FALHOU'})")
print(f"Levene: p={lev.pvalue:.3f} ({'OK' if lev.pvalue > .05 else 'FALHOU'})")

fig, ax = plt.subplots(1, 3, figsize=(16, 4.5))
sm.qqplot(res, line="45", fit=True, ax=ax[0]); ax[0].set_title("QQ dos resíduos (Y bootstrap)")
ax[1].scatter(mod.fittedvalues, res, alpha=.5); ax[1].axhline(0, color="r"); ax[1].set_title("Resíduos × ajustados")
ax[1].set_xlabel("Ajustado"); ax[1].set_ylabel("Resíduo")
sns.histplot(res, kde=True, ax=ax[2]); ax[2].set_title("Histograma dos resíduos")
save("04_diagnostico_residuos")

# %%
cores = sns.color_palette("tab10", 8)
fig, ax = plt.subplots(1, 2, figsize=(14, 4.5))
sm.qqplot(np.concatenate([(G[k] - G[k].mean()) / G[k].std() for k in CELLS]), line="45", ax=ax[0]); ax[0].set_title("QQ – ΔGPA bruto padronizado por célula")
sm.qqplot(np.concatenate([(g.Y - g.Y.mean()) / g.Y.std() for _, g in rep.groupby("celula")]), line="45", ax=ax[1]); ax[1].set_title("QQ – médias bootstrap padronizadas")
save("05_qq_antes_depois")

fig, axs = plt.subplots(2, 4, figsize=(16, 6), sharex=True)
for i, ax_ in enumerate(axs.ravel()):
    sns.histplot(rep[rep.celula == i + 1].Y, kde=True, ax=ax_, color=cores[i]); ax_.set_title(f"Célula {i+1} {CELLS[i]}", fontsize=10)
save("06_hist_bootstrap_por_celula")

# %%
fig, ax = plt.subplots(1, 2, figsize=(15, 5))
for i, k in enumerate(CELLS):
    ax[0].step(*ecdf(rep[rep.celula == i + 1].Y), where="post", label=f"Célula {i+1}")
ax[0].set_title("CDF das médias bootstrap (Y) por célula"); ax[0].set_xlabel("Y = média de ΔGPA"); ax[0].legend(fontsize=8)
for i in range(8):
    x, f = ecdf(rep[rep.celula == i + 1].Y); mu_, sd_ = x.mean(), x.std(ddof=1)
    ax[1].plot(np.sort((x - mu_) / sd_), f, lw=1, alpha=.7)
z = np.linspace(-3, 3, 200); ax[1].plot(z, stats.norm.cdf(z), "k--", lw=2, label="Normal(0,1)")
ax[1].set_title("CDF das médias bootstrap padronizadas × Normal"); ax[1].set_xlabel("z"); ax[1].legend()
for a_ in ax: a_.set_ylabel("F(x)")
save("18_cdf_bootstrap")

# %% [markdown]
# ## Quadros do desenho: matriz de sinais e combinações de teste

# %%
nomes_a = {-1: "Ativo", 1: "Passivo"}; nomes_b = {-1: "Baixa (<Q1)", 1: "Alta (≥Q3)"}; nomes_c = {-1: "Baixas (<Q1)", 1: "Altas (≥Q3)"}
yates = ["(1)", "a", "b", "ab", "c", "ac", "bc", "abc"]
sinais = pd.DataFrame([{"Ensaio": i + 1, "Yates": yates[i], "I": 1, **{n: f(k) for n, f in EFFECTS.items()}} for i, k in enumerate(CELLS)])
sinais["Y_média_obs"] = [G[k].mean() for k in CELLS]
sinais["Y_média_boot"] = [rep[rep.celula == i + 1].Y.mean() for i in range(8)]
linha = {"Ensaio": "Divisor", "Yates": "", "I": 8, **{n: 4 for n in EFFECTS}}
sinais_out = pd.concat([sinais, pd.DataFrame([linha])], ignore_index=True)
ef_obs_q = effects_from_means({k: G[k].mean() for k in CELLS})
ef_lin = {"Ensaio": "Efeito", "Yates": "", **ef_obs_q}
sinais_out = pd.concat([sinais_out, pd.DataFrame([ef_lin])], ignore_index=True)
sinais_out.to_csv(f"{OUT_DAT}/quadro_sinais.csv", index=False); print(sinais_out.round(4).to_string(index=False))

comb = pd.DataFrame([{"Ensaio": i + 1, "Yates": yates[i],
    "A (IA)": f"{k[0]:+d} {nomes_a[k[0]]}", "B (Ansiedade)": f"{k[1]:+d} {nomes_b[k[1]]}", "C (Estudo)": f"{k[2]:+d} {nomes_c[k[2]]}",
    "n alunos": len(G[k]), "ΔGPA médio": round(G[k].mean(), 3), "DP": round(G[k].std(ddof=1), 3),
    "Réplicas (r)": R, "m por réplica": M, "Observações": R} for i, k in enumerate(CELLS)])
comb.to_csv(f"{OUT_DAT}/quadro_combinacoes.csv", index=False); print(comb.to_string(index=False))

fig, ax = plt.subplots(2, 1, figsize=(13, 8.5)); 
for a_ in ax: a_.axis("off")
t1 = ax[0].table(cellText=comb.astype(str).values, colLabels=comb.columns, loc="center", cellLoc="center"); t1.auto_set_font_size(False); t1.set_fontsize(8); t1.scale(1, 1.5)
ax[0].set_title("Quadro das combinações de teste (8 tratamentos × r = 30 réplicas)", fontweight="bold")
sg = sinais[["Ensaio", "Yates", "I", *EFFECTS, "Y_média_obs"]].copy(); sg["Y_média_obs"] = sg["Y_média_obs"].round(3)
t2 = ax[1].table(cellText=sg.astype(str).values, colLabels=sg.columns, loc="center", cellLoc="center"); t2.auto_set_font_size(False); t2.set_fontsize(9); t2.scale(1, 1.5)
for (r_, c_), cell in t2.get_celld().items():
    if r_ > 0 and 2 <= c_ <= 9:
        cell.set_facecolor("#d5f5e3" if cell.get_text().get_text() == "1" else "#fadbd8")
ax[1].set_title("Matriz de sinais dos contrastes (efeito = Σ sinal·Y / 4)", fontweight="bold")
save("19_quadros_combinacoes_e_sinais")

# %% [markdown]
# ## 4. Efeitos, cubo, interações e Pareto

# %%
mu = {k: rep[rep.celula == i + 1].Y.mean() for i, k in enumerate(CELLS)}
ef_yates = effects_from_means(mu)
print({k: round(v, 4) for k, v in ef_yates.items()})

fig = plt.figure(figsize=(7, 6)); ax = fig.add_subplot(111, projection="3d")
for k in CELLS:
    ax.scatter(*k, s=900 * abs(mu[k]) + 100, c=[mu[k]], cmap="RdYlGn", vmin=0, vmax=.45)
    ax.text(k[0], k[1], k[2] + .08, f"{mu[k]:.3f}", ha="center")
ax.set_xlabel("A (IA)"); ax.set_ylabel("B (Ansiedade)"); ax.set_zlabel("C (Estudo)")
ax.set_xticks([-1, 1]); ax.set_yticks([-1, 1]); ax.set_zticks([-1, 1]); ax.set_title("Cubo 2³ – média de ΔGPA")
save("07_cubo_2x3")

# %%
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
for i, (f, nome) in enumerate((("A", "IA (Ativo → Passivo)"), ("B", "Ansiedade"), ("C", "Estudo"))):
    m_ = rep.groupby(f).Y.agg(["mean", "std"])
    ax[i].errorbar([-1, 1], m_["mean"], yerr=1.96 * m_["std"] / np.sqrt(rep.groupby(f).size()), marker="o", capsize=4)
    ax[i].set_xticks([-1, 1]); ax[i].set_title(f"Efeito principal: {nome}"); ax[i].set_ylabel("ΔGPA médio")
save("08_efeitos_principais")

fig, ax = plt.subplots(1, 3, figsize=(14, 4))
for i, (f1, f2) in enumerate((("A", "B"), ("A", "C"), ("B", "C"))):
    for lvl, g in rep.groupby(f2):
        m_ = g.groupby(f1).Y.mean(); ax[i].plot(m_.index, m_.values, marker="o", label=f"{f2}={lvl}")
    ax[i].set_xticks([-1, 1]); ax[i].set_xlabel(f1); ax[i].set_ylabel("ΔGPA médio"); ax[i].set_title(f"Interação {f1}×{f2}"); ax[i].legend()
save("09_interacoes")

# %%
ef_s = pd.Series(ef_yates).reindex(["A", "B", "C", "AB", "AC", "BC", "ABC"])
sd_res = np.sqrt(mod.scale)
pa = (ef_s / sd_res).abs().sort_values()
plt.figure(figsize=(7, 4)); plt.barh(pa.index, pa.values, color=["#c0392b" if ef_s[i] < 0 else "#27ae60" for i in pa.index])
plt.title("Pareto dos efeitos padronizados (|efeito|/DP resíduo)\nverde: positivo | vermelho: negativo"); save("10_pareto_efeitos")

order = ef_s.sort_values().index; q = stats.norm.ppf((np.arange(1, 8) - .5) / 7)
plt.figure(figsize=(6, 4.5)); plt.scatter(ef_s[order], q)
for n_, x_, y_ in zip(order, ef_s[order], q): plt.annotate(n_, (x_, y_), xytext=(4, 3), textcoords="offset points")
plt.xlabel("Efeito"); plt.ylabel("Quantil normal"); plt.title("Normal plot dos efeitos"); save("11_normal_plot_efeitos")

# %% [markdown]
# ## 5. Ciclo 2 – Bootstrap estratificado dos efeitos (decisão de significância)

# %%
def boot_effects(G, nboot, seed):
    rng = np.random.default_rng(seed); out = []
    for _ in range(nboot):
        out.append(effects_from_means({k: v[rng.integers(0, len(v), len(v))].mean() for k, v in G.items()}))
    return pd.DataFrame(out)

obs = effects_from_means({k: G[k].mean() for k in CELLS})
BS = boot_effects(G, NBOOT, SEED)
ci = pd.DataFrame({"efeito_obs": obs, "ic_inf": BS.quantile(.025), "ic_sup": BS.quantile(.975), "dp_boot": BS.std()})
ci["ic_exclui_0"] = (ci.ic_inf > 0) | (ci.ic_sup < 0)
print(ci.round(4))

fig, ax = plt.subplots(figsize=(7, 4.5))
for i, n_ in enumerate(ci.index[::-1]):
    c = "#c0392b" if ci.loc[n_, "ic_exclui_0"] else "gray"
    ax.errorbar(ci.loc[n_, "efeito_obs"], i, xerr=[[ci.loc[n_, "efeito_obs"] - ci.loc[n_, "ic_inf"]], [ci.loc[n_, "ic_sup"] - ci.loc[n_, "efeito_obs"]]], fmt="o", color=c, capsize=4)
ax.axvline(0, color="k", ls="--"); ax.set_yticks(range(7)); ax.set_yticklabels(ci.index[::-1])
ax.set_title("Forest plot: efeitos com IC95% bootstrap (vermelho = exclui 0)"); ax.set_xlabel("Efeito em ΔGPA"); save("12_forest_plot_efeitos")

# %%
pv = anova.drop("Residual")
plt.figure(figsize=(7, 4)); sns.barplot(x=pv.index, y=pv.pct_var, color="#34495e"); plt.xticks(rotation=30)
plt.ylabel("% da variância (SS/SST)"); plt.title("Contribuição de cada termo (ANOVA bootstrap)"); save("13_pct_variancia")

# %% [markdown]
# ## 6. Validação cruzada, sensibilidade e estabilidade

# %%
raw = sm.stats.anova_lm(smf.ols("Delta_GPA ~ A*B*C", fat).fit(), typ=2)
p_raw = raw["PR(>F)"].drop("Residual"); p_raw.index = [i.replace(":", "") for i in p_raw.index]

# estabilidade entre sementes
seeds = []
for sd in (42, 1, 2, 3, 4, 5, 6, 7, 8, 9):
    m_ = smf.ols("Y ~ A*B*C", make_replicas(G, R, M, sd)).fit()
    seeds.append({n.replace(":", ""): 2 * m_.params[n] for n in m_.params.index if n != "Intercept"})
seeds = pd.DataFrame(seeds); seeds.to_csv(f"{OUT_DAT}/seeds.csv", index=False)
est = seeds.agg(["mean", "std", "min", "max"]).T.round(4); print(est)

# sensibilidade nas regras de corte
def sens(regra):
    d = s.copy()
    if regra == "mediana":
        d["B"] = np.where(an > an.median(), 1, -1); d["C"] = np.where(hr > hr.median(), 1, -1)
    elif regra == "<=Q1/>=Q3":
        d["B"] = np.where(an >= qa3, 1, np.where(an <= qa1, -1, 0)); d["C"] = np.where(hr >= qh3, 1, np.where(hr <= qh1, -1, 0))
    else:
        d["B"] = s.B; d["C"] = s.C
    d = d[(d.B != 0) & (d.C != 0)]
    g = {k: v.Delta_GPA.values for k, v in d.groupby(["A", "B", "C"])}
    e = effects_from_means({k: g[k].mean() for k in CELLS})
    bs = boot_effects(g, 1000, SEED)
    return {"n": len(d), **{f"{k}": f"{e[k]:+.3f}{'*' if (bs[k].quantile(.025) > 0 or bs[k].quantile(.975) < 0) else ''}" for k in EFFECTS}}
sensib = pd.DataFrame({r: sens(r) for r in ("<Q1/>=Q3 (principal)", "<=Q1/>=Q3", "mediana")}).T
sensib.to_csv(f"{OUT_DAT}/sensibilidade.csv"); print(sensib, "\n(* = IC95% bootstrap exclui 0)")

# sensibilidade: ANCOVA com Pre_GPA
anc = smf.ols("Delta_GPA ~ A*B*C + Pre_Semester_GPA", fat).fit()
print("ANCOVA (Pre_GPA) coef A,B,C,AB:", (2 * anc.params[["A", "B", "C", "A:B"]]).round(4).to_dict())

# %%
sub = sensib.drop(columns="n").map(lambda x: float(str(x).rstrip("*")))
sub.T.plot(kind="bar", figsize=(9, 4)); plt.axhline(0, color="k", lw=.8); plt.title("Sensibilidade: efeitos por regra de corte")
plt.ylabel("Efeito em ΔGPA"); plt.xticks(rotation=0); save("14_sensibilidade")

# %% [markdown]
# ## 7. Consolidação e veredito

# %%
mestre = pd.DataFrame({
    "efeito": ci.efeito_obs, "ic95_inf": ci.ic_inf, "ic95_sup": ci.ic_sup,
    "efeito_anova_boot": pd.Series(ef_anova), "pct_var_boot": pv.pct_var.rename(lambda i: i.replace(":", "")),
    "p_anova_boot": pv["PR(>F)"].rename(lambda i: i.replace(":", "")), "p_anova_bruta": p_raw,
    "efeito_dp_entre_seeds": seeds.std()})
def veredito(r):
    a, b = r.ic95_inf > 0 or r.ic95_sup < 0, r.p_anova_bruta < .05
    return "significativo" if a and b else ("fraco" if a or b else "não significativo")
mestre["veredito"] = mestre.apply(veredito, axis=1)
mestre = mestre.reindex(["A", "B", "C", "AB", "AC", "BC", "ABC"])
mestre.round(4).to_csv(f"{OUT_DAT}/efeitos_ic.csv"); print(mestre.round(4).to_string())

# %%
checks = pd.DataFrame([
    ("Shapiro dos resíduos (p>0,05)", sh.pvalue > .05, f"p={sh.pvalue:.3f}"),
    ("Levene entre células (p>0,05)", lev.pvalue > .05, f"p={lev.pvalue:.3f}"),
    ("Estabilidade entre seeds (DP<0,01)", bool((seeds.std() < .01).all()), f"máx DP={seeds.std().max():.4f}"),
    ("Concordância IC × ANOVA bruta (sem 'fraco')", bool((mestre.veredito != "fraco").all()), ", ".join(mestre.index[mestre.veredito == "fraco"]) or "-"),
    ("Pre_GPA balanceado (ANOVA p>0,05)", stats.f_oneway(*[g.Pre_Semester_GPA for _, g in fat.groupby("celula")]).pvalue > .05, "ver balanceamento")],
    columns=["checagem", "ok", "detalhe"])
checks.to_csv(f"{OUT_DAT}/validacao.csv", index=False); print(checks.to_string())
print("\nCONCLUSÃO:")
for n_, r in mestre.iterrows():
    print(f"  {n_:3s}: {r.efeito:+.3f} [{r.ic95_inf:+.3f}; {r.ic95_sup:+.3f}] -> {r.veredito}")

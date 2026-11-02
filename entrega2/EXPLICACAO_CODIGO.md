# Explicação detalhada do código — `pcc170_entrega02.py`

Roteiro etapa a etapa de [pcc170_entrega02.py](pcc170_entrega02.py) (também em [pcc170_entrega02.ipynb](pcc170_entrega02.ipynb), uma célula por bloco `# %%`).
Execução: `cd entrega2 && MPLBACKEND=Agg python pcc170_entrega02.py`. Saídas: `figuras/*.png` e `dados/*.csv`.

## 0. Visão geral do fluxo

```
CSV → ΔGPA → recorte STEM+Junior → níveis ±1 (mediana) → 8 células
   → AED/CDF → Ciclo 1 (réplicas balanceadas + ANOVA 2³ + diagnóstico)
   → efeitos/cubo/Pareto → Ciclo 2 (bootstrap completo, IC95%)
   → validação cruzada/sensibilidade → veredito → balanceamento e inferência (permutação, teto GPA)
```

## 1. Configuração (linhas 1–35)

| Item | O que faz | Por quê |
|---|---|---|
| imports | NumPy/pandas (dados), SciPy/statsmodels (testes e modelos), Matplotlib/seaborn (gráficos) | — |
| `CSV` | procura o arquivo em `.`, `../csv/`, `csv/` | roda no Colab ou localmente |
| `OUT_FIG`, `OUT_DAT` | pastas de saída | reprodutibilidade |
| `SEED, R, M, NBOOT = 42, 30, 36, 5000` | semente; nº de réplicas por célula; alunos por réplica; reamostras do bootstrap completo | fixa o experimento; r e m vêm do desenho (Aula 4) |
| `REGRA` | `"mediana"` (≤Q2 baixo / >Q2 alto) ou `"quartis"` (<Q1 / ≥Q3, descarta o meio) | permite reproduzir as duas versões |
| `PASSIVO` | casos de uso considerados passivos | define o fator A |
| `CELLS` | 8 combinações (A,B,C) na **ordem de Yates** — (1), a, b, ab, c, ac, bc, abc | ordem padrão do fatorial |
| `EFFECTS` | dicionário de contrastes: A=a, B=b, C=c, AB=a·b, … | cada efeito é a soma de sinal × média ÷ 4 |
| `save()` | grava a figura completa (200 dpi) em `figuras/` e, se ela tiver vários gráficos, **cada gráfico em arquivo próprio** em `figuras/separados/<nome>_<n>_<título>.png` | facilita reutilizar cada gráfico isoladamente; `_completar()` e `_ancorar()` garantem rótulos dos eixos x/y, números nos eixos e legenda explicativa em cada gráfico (dicionário `_ROT`), com a legenda posicionada abaixo do eixo x para não cobrir os dados. O quadro 19 sai em dois arquivos: `19a_quadro_combinacoes_teste` e `19b_matriz_sinais_contrastes` |

## 2. Seção 1 — Dados e níveis (linhas 36–70)

1. `Delta_GPA = Post − Pre`: variável resposta.
2. `A = +1` se o uso principal é *Copywriting* ou *Direct Answer* (passivo), `−1` caso contrário (ativo).
3. `s`: recorte **STEM + Junior** (único critério, evitando viés de composição) → n = 3.279.
4. Quartis de ansiedade e horas (`qa1/qa2/qa3`, `qh1/qh2/qh3`) calculados **no recorte**.
5. Níveis B e C: pela mediana (`>Q2 → +1`, `≤Q2 → −1`); na regra por quartis, o meio recebe 0 e é descartado.
6. `fat`: alunos analisados; `celula` = índice (1–8) na ordem de Yates.
7. `G`: dicionário `{(A,B,C): vetor de ΔGPA}`; o `assert` garante 8 células com n ≥ max(m, 10), isto é, que dá para sortear m alunos por célula.

*Observação:* a ansiedade é discreta (mediana 4, 53,4% ≤ 4), por isso os grupos não ficam exatamente 50/50.

## 3. Descritivas e balanceamento de Pre_GPA (71–85)

- Média/DP do Pre_GPA por célula e ANOVA de uma via (`f_oneway`): verifica se as células partem de níveis iguais de GPA (p = 0,89 → sem confundimento pelo ponto de partida).
- Estatísticas descritivas do dataset completo e do recorte → CSV.

## 4. Seção 2 — Gráficos exploratórios (figs 01–03, 15–17)

| Fig. | Conteúdo | Leitura |
|---|---|---|
| 01 | histogramas de ΔGPA, ansiedade, horas com o corte Q2 | onde a mediana divide cada variável |
| 02 | heatmap do n por célula | mostra o desbalanceamento (181–667) |
| 03 | boxplot do ΔGPA bruto por célula | dispersão e assimetria |
| 15 | CDF do ΔGPA por A, por B, por C | separação estocástica: curva à direita = ΔGPA maior |
| 16 | CDF por célula e do recorte completo | compara as 8 células |
| 17 | CDF de ansiedade e horas com Q1/Q2/Q3 | mostra o ponto F = 0,5 do corte |

`ecdf(x)` ordena os valores e atribui F = i/n.

## 4b. Seção 2b — NÚCLEO: ANOVA 2³ sobre os dados brutos com HC3

- `fit_raw` (OLS) e `fit_hc3` (mesmo modelo com `cov_type="HC3"`) em `Delta_GPA ~ A*B*C` nos 3.279 alunos. `anova_lm(typ=3)` (codificação ±1) testa exatamente cada contraste de efeito mesmo com n desigual; `p_raw` é o p clássico e `hc3` o robusto. `pct_raw` = SQ/SQ total (o resíduo fica com 89%).
- Heterocedasticidade: DP por célula (`dp_por_celula.csv`) e Levene bruto.
- Fig 04: diagnóstico dos resíduos do modelo bruto (QQ, resíduos × ajustados, histograma).
- Esta é a **única fonte de p-valores**. As seções marcadas APÊNDICE são ilustrativas/sensibilidade.

## 5. Seção 3 — APÊNDICE (ilustrativo): réplicas + ANOVA (linhas 165–230)

> As réplicas reamostram os mesmos alunos (pseudo-replicação): medem a variância do estimador, não o erro experimental. O p desta ANOVA é otimista (BC p = 0,001) e não é critério de decisão.

- `make_replicas(G, r, m, seed)`: para cada célula, repete r = 30 vezes: sorteia **m = 36 índices com reposição** (`rng.integers`) e guarda a **média** (Y), o DP da amostra e o nº de alunos distintos. Resultado: 8 × 30 = 240 observações **balanceadas** (mesmo n em todas as células).
- `effects_from_means(mu)`: efeito = Σ(sinal × média da célula) / 4 (contraste de Yates).
- `smf.ols("Y ~ A*B*C")` + `anova_lm(typ=2)`: ANOVA do fatorial 2³ r. `pct_var` = SS/SST (contribuição de cada termo).
- `ef_anova = 2 × coeficiente` (os coeficientes com ±1 valem metade do efeito).

**Validação das premissas:** Shapiro dos resíduos (normalidade), Levene entre células (homocedasticidade), tabela bruto × bootstrap (assimetria e Shapiro por célula). QQ-plots (figs 04b, 05), histogramas (06) e CDF das médias bootstrap vs. Normal (18) mostram que, mesmo com o ΔGPA bruto assimétrico, as **médias** ficam normais (Teorema Central do Limite).

**Quadros:** `sinais` (matriz de sinais com médias observadas e bootstrap, linha "Divisor" e linha "Efeito") e `comb` (combinações com n, média, DP, r, m) → CSVs e fig 19.

## 6. Seção 4 — Efeitos e interpretação gráfica (07–11)

- `mu`: média **bruta** por célula; `ef_obs`: efeitos por contraste (`ef_yates`, das réplicas, só ilustrativo).
- 07 cubo 2³ (média por vértice); 08 efeitos principais (média bruta ± 1,96·EP); 09 interações (retas não paralelas = interação).
- 10 Pareto: |t| com erro-padrão HC3; 11 normal plot dos efeitos (pontos fora da reta = efeitos reais).

## 7. Seção 5 — NÚCLEO: bootstrap completo, só para IC (linhas 318–345)

- `boot_effects(G, nboot, seed)`: 5.000 vezes reamostra **cada célula com seu n real** (com reposição), calcula as médias e os 7 efeitos.
- IC95% = percentis 2,5 e 97,5; efeito é "significativo no bootstrap" se o IC **exclui 0**.
- Fig 12 (forest plot) e fig 13 (% da SQ total no modelo bruto).

*Por que dois ciclos?* O Ciclo 1 mede a estrutura do desenho (ANOVA com réplicas), mas as réplicas reusam os mesmos alunos e inflam o p. O Ciclo 2 dá a incerteza honesta, reamostrando os dados reais.

## 8. Seção 6 — APÊNDICE: estabilidade e sensibilidade (350–400)

| Bloco | Ideia |
|---|---|
| Estabilidade de sementes | refaz as réplicas com 10 sementes; DP dos efeitos deve ser < 0,01 |
| `sens(regra)` | recalcula efeitos com mediana, <Q1/≥Q3 e ≤Q1/≥Q3; `*` = IC bootstrap exclui 0; informa n e menor célula |
| Regressão contínua | `ΔGPA ~ A·ansiedade + horas` sem dicotomizar; mede perda de informação (R² 0,181 vs. 0,129) |
| ANCOVA | inclui Pre_GPA como covariável |

Fig 14: efeitos por regra de corte.

## 9. Seção 7 — NÚCLEO: consolidação (405–424)

- `mestre`: tabela única (efeito, IC, % SQ bruta, p HC3 e clássico, ANOVA bootstrap só informativa, DP entre sementes).
- `veredito`: **significativo** se IC bootstrap exclui 0 *e* p (HC3) < 0,05; **fraco** se apenas um critério; **não significativo** caso contrário.
- `checks`: 6 checagens (Levene bruto, Levene réplicas, estabilidade, concordância IC × HC3, Pre_GPA balanceado etc.) → `validacao.csv`.

## 10. Seção 8 — APÊNDICE: balanceamento e inferência (linhas 425–541)

1. **`make_replicas2(..., replace)`**: igual ao Ciclo 1, mas permite sorteio **sem reposição** (subamostra de alunos distintos), com r = 300.
2. **Esquemas** (`boot m=36`, `boot m=150`, `sem reposição m=150`, `m=181`): compara efeitos médios e DP entre réplicas → `esquemas_replica.csv`.
   - Efeitos idênticos em todos → a estimativa não depende do esquema.
   - O DP sem reposição encolhe com m (correção de população finita): **não** é erro do estimador.
3. **Varredura de m** (36, 75, 120, 150, 181): fig 20.
4. **Permutação**:
   - `efeitos_perm(yy)`: efeitos por contraste sobre as médias de célula, via `bincount` (rápido).
   - Global: embaralha ΔGPA entre alunos (nula: nenhum fator importa).
   - **Resíduos do modelo reduzido (Freedman–Lane)**: ajusta o modelo sem o termo testado, permuta os resíduos e soma ao ajustado; assim testa cada efeito sem supor que os outros são nulos. `p = (#|nulo| ≥ |obs| + 1)/(N + 1)`. Fig 22 mostra a distribuição nula.
5. **Teto de GPA**: transformação `−√(c − ΔGPA)` (reflexão + raiz) com bootstrap e regressão quantílica (mediana) para reduzir o efeito da assimetria de 12,1% no 4,0 → `teto_gpa.csv`.
6. **Consolidação**: fig 21 (efeitos e ICs por método) e `inferencia_consolidada.csv` (p de permutação, HC3, ANOVA bruta e bootstrap lado a lado); checagens de Shapiro/Levene/semente do esquema sem reposição.

## 11. Como ler os resultados (resumo)

- **Efeitos**: diferença média de ΔGPA entre nível + e − de cada fator (A = −0,077; C = +0,121; AB = −0,023; B ≈ −0,018 marginal; AC, BC, ABC ≈ 0).
- **Inferência**: modelo bruto com HC3 + IC bootstrap completo (núcleo); permutação e demais no apêndice; a ANOVA das réplicas é descritiva.
- **Limitações**: dicotomização, Levene falha, teto 4,0, dados observacionais (sem causalidade).

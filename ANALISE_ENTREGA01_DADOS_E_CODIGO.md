# PCC170 – Análise profunda da Entrega 1: CSV, Notebook (Colab) e PDF

**Aluno:** Wagner Tironi Pinto · **Docente:** Prof. Dr. Carlos H. G. Ferreira
**Projeto:** Projeto fatorial 2³ r – impacto do tipo de uso de IA generativa no rendimento acadêmico (ΔGPA)

Artefatos analisados (todos os números abaixo foram **recalculados** a partir do CSV; o PSM e o ATE do notebook foram reproduzidos):

| Artefato | Caminho |
|---|---|
| Dataset | [csv/ai_student_impact_dataset.csv](csv/ai_student_impact_dataset.csv) |
| Notebook Colab | [pcc170_entrega01_ajustada.ipynb](pcc170_entrega01_ajustada.ipynb) |
| Entrega 1 (14 slides) | [Entregas/PCC170_2026_2_WagnerTironiPinto_Entrega01.pdf](Entregas/PCC170_2026_2_WagnerTironiPinto_Entrega01.pdf) |
| Análise geral da disciplina | [ANALISE_PCC170_E_BASE_PROJETO.md](ANALISE_PCC170_E_BASE_PROJETO.md) |

---

## 1. Resumo executivo

- Os dados **não são simulados**: o notebook lê o CSV real (50.000 linhas × 16 colunas, sem nulos, `Student_ID` único). O bloco com `np.random` é só *fallback* caso o arquivo não exista – e **não foi executado** (saída: "Dataset real carregado com sucesso").
- O PDF afirma "N = 10.000 simulados via np.random", o que **contradiz** o notebook (50.000 reais; 3.279 após filtro STEM + Junior).
- O recorte analisado é **STEM + Junior** (n = 3.279; 813 passivos / 2.466 ativos). O PDF não explicita esse recorte.
- Estatísticas descritivas do slide 8 (ΔGPA média 0,12, DP 0,41; ansiedade média 7,84…) **não batem** com o notebook/CSV (ΔGPA 0,20 / DP 0,19; ansiedade 4,27 / DP 2,14; horas 11,21 / DP 5,16). Apenas os valores do notebook são reproduzíveis.
- A narrativa do PDF ("ansiedade e horas de estudo confundem o efeito do uso passivo") **não é sustentada pelos dados**: as covariáveis já estão balanceadas antes do PSM (|SMD| < 0,05) e, portanto, não confundem o tratamento.
- O efeito do uso passivo existe e é pequeno, mas consistente: **ATE = −0,072 (IC95% bootstrap [−0,092; −0,053])**, ou seja, o IC exclui zero. Isso contradiz a hipótese do PDF de efeito "marginal".

---

## 2. Estrutura do CSV

50.000 registros, 16 colunas, 0 nulos, `Student_ID` de 100001 a 150000 (único).

### 2.1 Dicionário de dados

| Coluna | Tipo | Descrição / domínio | Estatística |
|---|---|---|---|
| `Student_ID` | int | Identificador | 100001–150000 |
| `Major_Category` | cat | STEM 15.059 · Business 12.538 · Humanities 9.994 · Medical 6.476 · Arts 5.933 | – |
| `Year_of_Study` | cat | Junior 11.045 · Freshman 11.031 · Senior 10.634 · Sophomore 9.860 · Graduate 7.430 | – |
| `Pre_Semester_GPA` | float | GPA antes do semestre | média 3,146; DP 0,479; 1,183–3,998 |
| `Weekly_GenAI_Hours` | float | Horas semanais com IA generativa | média 8,43; DP 8,27; 0–40 |
| `Primary_Use_Case` | cat | Debugging/Troubleshooting 12.295 · Copywriting/Drafting 12.011 · Ideation 10.721 · Summarizing_Reading 8.633 · Direct_Answer_Generation 6.340 | base do Fator A |
| `Prompt_Engineering_Skill` | cat | Beginner 18.495 · Intermediate 17.696 · Advanced 13.809 | – |
| `Tool_Diversity` | int | Nº de ferramentas (1–5) | média 2,80 |
| `Paid_Subscription` | bool | Assinatura paga | True 42,3% |
| `Traditional_Study_Hours` | float | Horas de estudo tradicional | média 11,21; DP 5,16; 1–35,86 |
| `Perceived_AI_Dependency` | int | Dependência percebida (1–10) | média 3,51 |
| `Institutional_Policy` | cat | Allowed_With_Citation 25.224 · Actively_Encouraged 14.988 · Strict_Ban 9.788 | – |
| `Anxiety_Level_During_Exams` | int | Ansiedade (1–10) | média 4,27; DP 2,14 |
| `Post_Semester_GPA` | float | GPA depois do semestre | média 3,349; DP 0,496; 1,0–4,0 |
| `Skill_Retention_Score` | float | Retenção de habilidade (0–100) | média 75,8; DP 13,3 |
| `Burnout_Risk_Level` | cat | Medium 21.144 · Low 16.369 · High 12.487 | – |

Distribuição da ansiedade (1…10): 5.655 · 5.752 · 7.806 · 8.749 · 8.222 · 6.107 · 3.850 · 2.088 · 1.151 · 620 → **assimétrica à direita, moda em 4**, e não concentrada em 7–10.

### 2.2 Características relevantes do dado

- **Teto de GPA:** 9,6% dos `Post_Semester_GPA` valem exatamente 4,0 (censura). Isso comprime ΔGPA, sobretudo para quem já tem GPA alto (correlação ΔGPA × Pre_GPA = −0,10).
- **Variável derivada ΔGPA** = `Post − Pre`: média 0,203; DP 0,187; mín −0,924; máx 1,008; mediana 0,204. Distribuição aproximadamente simétrica, com poucos outliers.
- **Correlações com ΔGPA** (n = 50.000): `Traditional_Study_Hours` **+0,376** (dominante), `Skill_Retention_Score` +0,196, `Pre_GPA` −0,104, `Tool_Diversity` +0,081, `Weekly_GenAI_Hours` −0,046, ansiedade −0,040, dependência −0,039.
- **Outras relações:** `Weekly_GenAI_Hours` × `Perceived_AI_Dependency` = 0,665; GenAI × ansiedade = 0,269; dependência × ansiedade = 0,308. O nível médio de ansiedade é maior em quem tem Burnout alto (4,89) que baixo (3,93).
- **ΔGPA por `Primary_Use_Case`** (média / DP / n):
  - Debugging/Troubleshooting: 0,249 / 0,192 / 12.295
  - Copywriting/Drafting: 0,200 / 0,169 / 12.011
  - Ideation: 0,200 / 0,170 / 10.721
  - Summarizing_Reading: 0,197 / 0,170 / 8.633
  - **Direct_Answer_Generation: 0,133 / 0,230 / 6.340** (única categoria claramente pior e com maior variância)
- O dataset parece sintético (relações e distribuições "limpas"; o nome sugere um dataset público de Kaggle). A origem exata não está documentada no projeto; convém citar a fonte.

---

## 3. Pipeline do notebook (`pcc170_entrega01_ajustada.ipynb`)

13 células (0–12). A numeração dos slides nos comentários do código (ex.: "SLIDE 7", "SLIDE 9", "SLIDES 10 e 11") **não corresponde** à numeração do PDF final (8–12).

| Célula | Função |
|---|---|
| 0–1 | Imports (numpy, pandas, matplotlib, seaborn, sklearn: `LogisticRegression`, `NearestNeighbors`, `StandardScaler`, `permutation_importance`); estilo; leitura do CSV (fallback sintético com 10.000 linhas e coluna `Anxiety_Level` – nome diferente do real). |
| 2 | Leitura do CSV (fallback com 50.000 linhas); cria `Delta_GPA`, `Treatment_Passive_AI` e `AI_Usage_Type`; **filtra STEM + Junior** (3.279). |
| 3 | PSM e Love Plot. |
| 4 | Recria features sobre o `df` completo e gera a tabela descritiva (ΔGPA, ansiedade, horas) – sobre **os 50.000**, não sobre o recorte STEM Junior. |
| 5 | Bootstrap (2.000 reamostras, seed 42) do ATE no grupo pareado. |
| 6 | Permutation importance do modelo logístico de propensão (o aviso "soma zero" apareceu; gráfico sem informação). |
| 7 | Histograma + KDE da ansiedade (df completo), com anotação fixa "Concentração em níveis elevados". |
| 8 | KDE de ΔGPA por tipo de uso e boxplot (no `matched_df`). |
| 9–10 | Markdown: teoria 2³, matriz de Yates, níveis por quartil ou mediana. |
| 11 | Quartis para os níveis: **falhou** ("Execute as células iniciais…") porque `df_filtered` não estava no escopo naquele momento. |
| 12 | Codifica A, B e C (±1), médias das 8 células e contrastes de Yates (efeitos principais e interações). |

### 3.1 Definições operacionais

- **Fator A (tratamento):** `Passivo` (+1) se `Primary_Use_Case ∈ {Copywriting/Drafting, Direct_Answer_Generation}`; `Ativo` (−1) caso contrário (Ideation, Summarizing_Reading, Debugging/Troubleshooting). A classificação é **uma escolha do autor**, não vem do dataset. Resultado: no recorte, 813 passivos × 2.466 ativos (25% × 75%).
- **Fator B (ansiedade):** +1 se > mediana do recorte (4,0); −1 caso contrário.
- **Fator C (estudo):** +1 se > mediana (10,91 h); −1 caso contrário.
- Os níveis por **mediana** (e não Q1/Q3) foram escolhidos para preservar tamanho amostral. Os cortes dividem o conjunto inteiro, e não comparam extremos.

### 3.2 PSM (reproduzido)

- Covariáveis: ansiedade, horas de estudo, GPA pré. Regressão logística padronizada; coeficientes (padronizados): −0,043, +0,016, +0,035.
- Propensity scores muito concentrados: média 0,248; DP 0,011; faixa 0,205–0,278. **As covariáveis praticamente não predizem o tratamento.**
- Pareamento 1:1 por vizinho mais próximo **com reposição** e sem *caliper*: 813 tratados → apenas **648 controles únicos**; distância máxima 0,0063.
- SMD (antes → depois): ansiedade −0,043 → −0,048; horas +0,018 → −0,039; GPA +0,036 → −0,044. O balanceamento **não melhora** (já estava abaixo de 0,1). O PDF diz que o SMD "despencou" – não é verdade.
- O bootstrap reamostra linhas do `matched_df` com controles duplicados, ignorando a dependência dos pares → IC provavelmente otimista (estreito).

### 3.3 Resultados reproduzidos

- **ATE (passivo − ativo, pareado):** −0,0721; IC95% [−0,0924; −0,0531]. Sem pareamento a diferença bruta é parecida (0,185 − 0,259 = −0,074), reforçando que o PSM pouco altera.
- **Médias de ΔGPA (STEM Junior) por célula 2³ (sem pareamento; média / DP / n):**

| A | B | C | Média ΔGPA | DP | n |
|---|---|---|---|---|---|
| −1 | −1 | −1 | 0,1963 | 0,172 | 667 |
| −1 | −1 | +1 | 0,3170 | 0,170 | 639 |
| −1 | +1 | −1 | 0,2005 | 0,185 | 576 |
| −1 | +1 | +1 | 0,3231 | 0,173 | 584 |
| +1 | −1 | −1 | 0,1520 | 0,198 | 210 |
| +1 | −1 | +1 | 0,2523 | 0,176 | 235 |
| +1 | +1 | −1 | 0,0915 | 0,236 | 187 |
| +1 | +1 | +1 | 0,2325 | 0,179 | 181 |

  Leitura: **estudo (C) é o fator dominante** (+≈0,11 a +0,14 em todas as combinações); A reduz ΔGPA em ≈0,05–0,09; B quase não importa isoladamente, mas há indício de interação AB (efeito do passivo é pior com alta ansiedade quando o estudo é baixo: 0,0915).
- **Nº de unidades por célula após PSM:** 204 / 226 / 189 / 194 / 210 / 235 / 187 / 181 (n total 1.626, com duplicatas de controles). Os controles aparecem repetidos, então **as réplicas não são independentes**.

---

## 4. Revisão do PDF slide a slide, frente aos dados

| Slide | Conteúdo | Situação |
|---|---|---|
| 1–7 | Título, hipótese, objetivo, matriz 2³ r (r ≥ 10, ≥ 80 execuções), ambiente | Coerente com a proposta; o ambiente diz "dados simulados com np.random" ✗ (são dados reais do CSV). |
| 8 | Tabela descritiva | ✗ Valores não reproduzem (ver abaixo). |
| 9 | Love Plot (SMD ±0,04) | ✓ valores corretos (≈ ±0,05), mas a narrativa "SMD despencou" é incorreta; o texto repete "despencou despencou". |
| 10 | KDE da ansiedade ("assimetria severa, 7–10") | ✗ Gráfico real tem moda em 4 e cauda à direita; o texto descreve o oposto. |
| 11 | KDE ΔGPA por tipo de IA | Curvas quase sobrepostas; o intervalo plotado (≈ −1 a 1) não coincide com mín/máx do slide 8. |
| 12 | Boxplot, outliers mantidos | ✓ Plausível; passivo com mais outliers negativos (devido à categoria Direct_Answer, DP 0,23). |
| 13 | Síntese, 4 checks "Sim" | Superestimada dada as inconsistências. |
| 14 | Próximos passos (ANOVA, contrastes, relatório) | Adequado. |

**Tabela do slide 8 × realidade:**

| Variável | PDF | Dataset (50.000) | Recorte STEM Junior (3.279) |
|---|---|---|---|
| ΔGPA | 0,12 / 0,41 / −1,85 / 2,10 | 0,203 / 0,187 / −0,924 / 1,008 | 0,240 / 0,193 / −0,853 / 0,885 |
| Ansiedade | 7,84 / 2,95 / 1 / 10 | 4,271 / 2,144 / 1 / 10 | 4,422 / 2,229 / 1 / 10 |
| Horas de estudo | 4,20 / 1,10 / 0,5 / 8 | 11,209 / 5,156 / 1 / 35,86 | 11,038 / 5,289 / 1 / 29,75 |

(Formato: média / DP / mín / máx.) A saída do próprio notebook (célula 4) coincide com a coluna do dataset completo, o que sugere que o slide foi redigido (possivelmente pelo Gemini Notebook) sem conferir os números.

---

## 5. Inconsistências e riscos (priorizados)

1. **Origem dos dados** (slides: simulados, N = 10.000; real: CSV público/sintético, N = 50.000). Corrigir.
2. **Estatísticas descritivas do slide 8 falsas** → substituir pelas do notebook, deixando claro se são do dataset completo ou do recorte.
3. **Recorte STEM + Junior** não declarado no PDF; justificar (por quê? tamanho 3.279) ou ampliar.
4. **Narrativa do "paradoxo da correlação ilusória"** não é sustentada: o tratamento não está correlacionado a ansiedade/estudo/GPA (|SMD| < 0,05). Há efeito real, pequeno, e o estudo é o fator que mais move ΔGPA. Reformular a hipótese (ex.: H0 de que A não afeta ΔGPA; H1 do efeito negativo do uso passivo; interação AB).
5. **Efeitos do notebook não reproduzem.** A célula 12 mostra A = −0,0453, AB = −0,1016 etc.; recalculando com a mesma lógica sobre `df_filtered` obtive tabela de médias (seção 3.3) que implica efeito A ≈ −0,077 e AB ≈ −0,023 (contraste/4). A saída salva provavelmente veio de um estado antigo do kernel (a célula 11 falhou antes). **Reexecutar o notebook do zero (Restart & Run all)**.
6. **Definição de "passivo"** inclui Copywriting/Drafting, cujo ΔGPA (0,200) é igual ao de Ideation (0,200). O efeito negativo vem quase todo de `Direct_Answer_Generation` (0,133). Considerar classificar apenas essa categoria como passiva ou testar sensibilidade.
7. **Desbalanceamento e dependência**: 25%/75% passivo/ativo; PSM com reposição duplica controles; bootstrap ignora o pareamento; as 8 células pós-PSM não são réplicas independentes.
8. **Aleatorização**: dados observacionais; a alegação de "quase-aleatória" via PSM só vale para covariáveis observadas.
9. **Dicotomização** por mediana perde informação e deixa os níveis próximos da fronteira (ansiedade é inteira; mediana = 4 → o corte −1/+1 é 1–4 × 5–10, desbalanceado entre B+ e B−). Documentar ou usar Q1/Q3 (contraste extremo, tendo o custo de menos dados).
10. **Teto de GPA (4,0)** em 9,6% dos casos distorce ΔGPA e pode violar normalidade/homocedasticidade dos resíduos (DP maior no grupo passivo: 0,18–0,24 vs. 0,17–0,18).
11. **Permutation importance** (célula 6) sem sentido (soma 0 por baixa capacidade preditiva); remover do relatório ou reinterpretar como evidência de ausência de confusão.
12. Nomes de coluna do fallback (`Anxiety_Level`) divergem do CSV real (`Anxiety_Level_During_Exams`); `matched_df` usa `Delta_GPA`, mas só existe após a célula 2.
13. Reprodutibilidade: seed só nos bootstraps; pareamento determinístico; sem `requirements`; numeração de slides desatualizada nos comentários.

---

## 6. Recomendações para a Entrega 2 (ANOVA fatorial 2³ r)

1. **Fixar o desenho**: 8 tratamentos × r ≥ 10 réplicas. Com n por célula > 180 existe folga para **amostrar r réplicas (ex.: r = 10, 30 ou 50)** aleatoriamente por célula (seed fixa), ou usar todas e tratar como balanceado via subamostragem estratificada. Preferir **amostrar sem reposição** dentro da célula, para garantir independência.
2. **Estimar efeitos** (A, B, C, AB, AC, BC, ABC) pelo método dos sinais/contrastes e por ANOVA (`statsmodels`: `ols('Delta_GPA ~ C(A)*C(B)*C(C)')` + `anova_lm`, ou o modelo com ±1) e comparar com o resultado do notebook.
3. **Calcular**: SS por fator, fração da variância explicada (SSx/SST), erro experimental (SSE com 8(r−1) g.l.), intervalos de confiança dos efeitos e testes F.
4. **Verificar premissas**: normalidade dos resíduos (QQ-plot, Shapiro), homocedasticidade (resíduos × ajustados; Levene), independência. Se violar, considerar transformação ou procedimentos robustos/permutação.
5. **Sensibilidade**: níveis por mediana × Q1/Q3; passivo = {Direct_Answer} × {Direct_Answer + Copywriting}; com/sem PSM; subconjuntos (outros cursos/anos).
6. **Reportar** que o estudo (C) domina; o efeito do uso passivo (A) é pequeno mas significativo; ver se AB é real.
7. **Corrigir o PDF/relatório** com as inconsistências da seção 5 (principalmente itens 1–5).
8. **Tornar o notebook reprodutível**: células em ordem, `df_filtered`/`matched_df` sempre definidos, seeds, `Restart & Run all` antes de entregar, salvando as figuras e as tabelas.

---

## 7. Como reproduzir os números

Ambiente: Python 3, pandas, numpy, scikit-learn. Em `/home/wagner/pcc170/.venv` foram instalados os pacotes usados para a análise. Os valores foram recalculados diretamente do CSV com a mesma lógica do notebook (PSM logístico + 1-NN com reposição; ATE = média passivo − média ativo = −0,0721).

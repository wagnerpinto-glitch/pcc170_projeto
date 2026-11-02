# Entrega 2 – Resultados (fatorial 2³ r, STEM + Junior)

Reproduzir: `cd entrega2 && python pcc170_entrega02.py` (ou executar [pcc170_entrega02.ipynb](pcc170_entrega02.ipynb)). Seed = 42; r = 30; m = 36; 5.000 reamostras no bootstrap estratificado. O script lê o CSV de `../csv/`.

## Dados
- 50.000 → STEM + Junior = 3.279 → níveis extremos (ansiedade < 3 / ≥ 6; horas < 7,33 / ≥ 14,475) = **848 alunos** (25,9% do recorte).
- Células (Yates): n = 133, 36, 205, 63, 118, 49, 187, 57. Balanceamento de Pre_GPA: ANOVA p = 0,61 (balanceado).

## Resultados consolidados ([dados/efeitos_ic.csv](dados/efeitos_ic.csv))
| Efeito | ΔGPA | IC95% bootstrap | % var. (ANOVA boot.) | p ANOVA bruta | Veredito |
|---|---|---|---|---|---|
| A (IA passiva) | −0,067 | [−0,097; −0,038] | 8,9% | <0,001 | significativo |
| B (ansiedade alta) | −0,043 | [−0,071; −0,013] | 3,3% | 0,127 | **fraco** (só o IC exclui 0) |
| C (estudo alto) | +0,195 | [+0,167; +0,225] | 74,7% | <0,001 | significativo |
| AB | −0,046 | [−0,076; −0,017] | 4,3% | 0,002 | significativo |
| AC | +0,022 | [−0,007; +0,052] | 1,0% | 0,152 | não significativo |
| BC | +0,004 | [−0,025; +0,034] | 0,1% | 0,565 | não significativo |
| ABC | −0,006 | [−0,034; +0,023] | 0,2% | 0,663 | não significativo |

Pior vértice: passivo + ansiedade alta + pouco estudo (ΔGPA 0,029). Melhor: ativo + ansiedade alta + muito estudo (0,345).

## Validação ([dados/validacao.csv](dados/validacao.csv))
- Shapiro dos resíduos p = 0,81 ✔; Levene p = 0,12 ✔; estabilidade entre 10 seeds (DP máx. 0,0055) ✔; Pre_GPA balanceado ✔.
- Normalização: as células passivas brutas (n = 63 e 57) têm assimetria ≈ −0,68 (Shapiro p = 0,067 e 0,052); as médias bootstrap ficam normais (p ≥ 0,10 em todas as células).
- ✘ Concordância IC × ANOVA bruta: B é "fraco". Reportar com cautela.
- Limitação: a ANOVA sobre réplicas bootstrap tem p ≈ 0 mesmo para AC e ABC (inflação por r, pois as réplicas reusam as mesmas 848 pessoas). Por isso ela só serve para decompor a variância; a decisão usa o IC bootstrap e a ANOVA bruta.

## Sensibilidade ([dados/sensibilidade.csv](dados/sensibilidade.csv))
Os sinais e a ordem de importância se mantêm com ≤Q1/≥Q3 (n = 1.101) e com mediana (n = 3.279): A ≈ −0,07 a −0,08, C dominante. A ANCOVA com Pre_GPA dá A = −0,065, B = −0,041, C = +0,196, AB = −0,048 (inalterados).

## Conclusão
O uso passivo de IA reduz o ΔGPA em ≈ 0,07 ponto. O estudo alto compensa com +0,20 e explica ~75% da variância. A ansiedade alta tem efeito pequeno (fraco) e interage com a IA: o dano do uso passivo é maior com ansiedade alta (AB). Não há evidência de AC, BC ou ABC.

## Artefatos
- Dados: [dados/](dados) (df_factorial, replicas, anova_bootstrap, efeitos_ic, sensibilidade, seeds, validacao, normalidade_por_celula, descritivas).
- Figuras ([figuras/](figuras)): 14 PNGs. Contêm distribuições com quartis, n por célula, boxplot, diagnóstico de resíduos, QQ antes/depois, histogramas bootstrap, cubo 2³, efeitos principais, interações, Pareto, normal plot, forest plot, % variância e sensibilidade.

## Quadros do desenho 2³ (figura: [figuras/19_quadros_combinacoes_e_sinais.png](figuras/19_quadros_combinacoes_e_sinais.png); CSVs: [dados/quadro_combinacoes.csv](dados/quadro_combinacoes.csv), [dados/quadro_sinais.csv](dados/quadro_sinais.csv))

### Quadro das combinações de teste
Cada ensaio é repetido r = 30 vezes (m = 36 alunos sorteados com reposição da célula) → 8 × 30 = 240 observações.

| Ensaio | Yates | A (IA) | B (Ansiedade) | C (Estudo) | n alunos | ΔGPA médio | DP |
|:-:|:-:|---|---|---|--:|--:|--:|
| 1 | (1) | −1 Ativo | −1 Baixa (< Q1) | −1 Baixas (< Q1) | 133 | 0,164 | 0,180 |
| 2 | a | +1 Passivo | −1 Baixa | −1 Baixas | 36 | 0,114 | 0,165 |
| 3 | b | −1 Ativo | +1 Alta (≥ Q3) | −1 Baixas | 205 | 0,157 | 0,180 |
| 4 | ab | +1 Passivo | +1 Alta | −1 Baixas | 63 | 0,028 | 0,250 |
| 5 | c | −1 Ativo | −1 Baixa | +1 Altas (≥ Q3) | 118 | 0,326 | 0,155 |
| 6 | ac | +1 Passivo | −1 Baixa | +1 Altas | 49 | 0,334 | 0,155 |
| 7 | bc | −1 Ativo | +1 Alta | +1 Altas | 187 | 0,340 | 0,178 |
| 8 | abc | +1 Passivo | +1 Alta | +1 Altas | 57 | 0,243 | 0,189 |

Cortes: ansiedade Q1 = 3, Q3 = 6; horas Q1 = 7,33 h, Q3 = 14,475 h.

### Matriz de sinais dos contrastes (efeito = Σ sinal·Ȳ ÷ 4)

| Ensaio | Yates | I | A | B | C | AB | AC | BC | ABC | Ȳ (obs.) |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|--:|
| 1 | (1) | + | − | − | − | + | + | + | − | 0,1638 |
| 2 | a | + | + | − | − | − | − | + | + | 0,1139 |
| 3 | b | + | − | + | − | − | + | − | + | 0,1567 |
| 4 | ab | + | + | + | − | + | − | − | − | 0,0278 |
| 5 | c | + | − | − | + | + | − | − | + | 0,3263 |
| 6 | ac | + | + | − | + | − | + | − | − | 0,3338 |
| 7 | bc | + | − | + | + | − | − | + | − | 0,3402 |
| 8 | abc | + | + | + | + | + | + | + | + | 0,2427 |
| **Divisor** | | 8 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | |
| **Efeito** | | | −0,067 | −0,043 | +0,195 | −0,046 | +0,022 | +0,004 | −0,006 | |

Os sinais de AB, AC, BC e ABC são os produtos dos sinais das colunas correspondentes (ex.: AB = A·B). Com a média bootstrap por célula (Ȳ boot) os efeitos são A −0,067, B −0,041, C +0,195, AB −0,047, AC +0,023, BC +0,007, ABC −0,010.

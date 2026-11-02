# Entrega 2 – Resultados (fatorial 2³ r, STEM + Junior) – regra de corte pela mediana

Reproduzir: `cd entrega2 && python pcc170_entrega02.py` (ou executar [pcc170_entrega02.ipynb](pcc170_entrega02.ipynb)). Seed = 42; r = 30; m = 36; 5.000 reamostras no bootstrap estratificado. O script lê o CSV de `../csv/`. A regra de corte é a constante `REGRA` (`"mediana"` = principal; `"quartis"` reproduz a versão anterior, arquivada em [dados/quartis/](dados/quartis) e [figuras/quartis/](figuras/quartis)).

## Dados
- 50.000 → STEM + Junior = **3.279 alunos (100% analisados)**.
- Níveis: ansiedade **baixa ≤ 4 (Q2) / alta > 4** (53,4% ≤ Q2, por ser variável discreta); horas **baixas ≤ 10,91 / altas > 10,91** (50,0%). Fator A: 813 passivos / 2.466 ativos.
- Células (Yates): n = 667, 210, 576, 187, 639, 235, 584, 181 (menor n = 181, antes 36). Balanceamento de Pre_GPA: ANOVA p = 0,89.

## Estrutura de análise (conforme orientação do professor)
- **Núcleo:** (1) ANOVA 2³ sobre os **3.279 dados brutos** (desbalanceada, SQ tipo III, erros robustos **HC3**) = única fonte de p; (2) bootstrap estratificado **só para os IC95%**; (3) tabela de efeitos, forest plot e diagnóstico de resíduos.
- **Apêndice (sensibilidade/ilustrativo):** réplicas bootstrap (r=30, m=36) e sua ANOVA, estabilidade entre sementes, regras de corte, ANCOVA, regressão contínua, varredura de m, permutação, quantílica, teto de GPA.
- **Por quê:** as réplicas reamostram os mesmos alunos (pseudo-replicação): medem a variância do estimador, não o erro experimental; o p da ANOVA sobre elas é otimista (BC: p = 0,001 contra 0,146 na ANOVA bruta tipo III e 0,177 no HC3).
- **Nota sobre p:** a SQ tipo II (usada antes) testa os efeitos principais ponderados pelo n e dava B p = 0,35–0,60 e BC p = 0,36–0,44; a tipo III testa exatamente o contraste estimado (equivale ao teste do coeficiente ±1) e é a usada agora. Com ela, B é marginal e todos os métodos (IC bootstrap, HC3, permutação) concordam.

## Resultados consolidados ([dados/efeitos_ic.csv](dados/efeitos_ic.csv))
| Efeito | ΔGPA | IC95% bootstrap | % SQ total (bruta) | p (HC3) | Veredito |
|---|---|---|---|---|---|
| A (IA passiva) | −0,077 | [−0,092; −0,062] | 3,01% | <0,001 | significativo |
| B (ansiedade alta) | −0,018 | [−0,033; −0,002] | 0,15% | 0,027 | significativo (marginal, magnitude desprezível) |
| C (estudo alto) | +0,121 | [+0,106; +0,136] | 7,43% | <0,001 | significativo |
| AB | −0,023 | [−0,038; −0,007] | 0,26% | 0,004 | significativo |
| AC | −0,001 | [−0,016; +0,015] | <0,01% | 0,951 | não significativo |
| BC | +0,011 | [−0,005; +0,026] | 0,06% | 0,177 | não significativo |
| ABC | +0,010 | [−0,006; +0,025] | 0,05% | 0,218 | não significativo |

Resíduo: 89,0% da SQ total (R² = 0,129): os fatores explicam pouco da variabilidade individual. Pior vértice: passivo + ansiedade alta + pouco estudo (ΔGPA 0,091). Melhor: ativo + ansiedade alta + muito estudo (0,323), praticamente empatado com ativo + ansiedade baixa + muito estudo (0,317).

## Validação ([dados/validacao.csv](dados/validacao.csv), [dados/dp_por_celula.csv](dados/dp_por_celula.csv))
- Estabilidade entre 10 seeds (DP máx. 0,0056) ✔; Pre_GPA balanceado ✔; IC bootstrap × HC3 concordam nos 7 termos ✔.
- ✘ **Heterocedasticidade:** Levene bruto p = 2,6e-5 (réplicas: 0,044). DP por célula 0,170–0,236 (máx. na célula 4: passivo, ansiedade alta, pouco estudo); DP médio passivo 0,197 vs ativo 0,175. Tratamento: HC3 + IC bootstrap (não assumem variâncias iguais). Não se usa log Y (ΔGPA ≤ 0 em parte dos alunos).
- Resíduos brutos: QQ com cauda inferior (teto de GPA 4,0), histograma aproximadamente simétrico.
- Normalização (apêndice): o Shapiro dos dados brutos rejeita normalidade em 5 de 8 células; as médias bootstrap ficam normais (p ≥ 0,077). Isso ilustra o TCL, não valida a ANOVA das réplicas.

## Sensibilidade ([dados/sensibilidade.csv](dados/sensibilidade.csv), [dados/regressao_continua.csv](dados/regressao_continua.csv))
| Regra | n | menor célula | A | B | C | AB | AC | BC | ABC |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Mediana (principal) | 3.279 | 181 | −0,077* | −0,017* | +0,121* | −0,023* | −0,000 | +0,011 | +0,010 |
| <Q1 / ≥Q3 (versão anterior) | 848 | 36 | −0,067* | −0,043* | +0,195* | −0,046* | +0,022 | +0,004 | −0,006 |
| ≤Q1 / ≥Q3 | 1.101 | 57 | −0,080* | −0,038* | +0,193* | −0,033* | +0,011 | +0,006 | +0,005 |

(* IC95% bootstrap exclui 0.) A ANCOVA com Pre_GPA dá A = −0,076, B = −0,018, C = +0,121, AB = −0,022. A regressão contínua (R² = 0,181 vs 0,129 dicotomizado) confirma: cada hora de estudo +0,014 (p < 0,001); cada ponto de ansiedade −0,005 (p = 0,002); interação IA passiva × ansiedade −0,0064 (p < 0,001).

## Mediana × quartis: o que muda
- **Mantém-se:** sinais e significância de A, C, AB; B pequeno; AC, BC, ABC nulos; ordem de importância (C > A > AB ≈ B).
- **Muda:** C cai de +0,195 para +0,121 e B/AB caem ~50%, pois o contraste deixa de ser "extremo vs extremo" e passa a "acima vs abaixo da mediana". A fica ligeiramente maior (−0,077). Os ICs ficam ~50% mais estreitos e as células deixam de ser pequenas (36 → 181).
- **Piora:** heterocedasticidade (Levene), assimetria das células passivas, e perda de informação ao dicotomizar variáveis contínuas.
- Recomendação: mediana como análise principal; quartis e regressão contínua como sensibilidade.

## Conclusão
O uso passivo de IA reduz o ΔGPA em ≈ 0,08 ponto. Estudar acima da mediana adiciona ≈ +0,12 (7,4% da SQ total; os 3 fatores juntos explicam ~11%). A ansiedade alta tem efeito pequeno e marginal e interage com a IA: o dano do uso passivo é maior com ansiedade alta (AB). Não há evidência de AC, BC ou ABC.

## Artefatos
- Dados: [dados/](dados) (df_factorial, replicas, anova_bootstrap, efeitos_ic, sensibilidade, regressao_continua, seeds, validacao, normalidade_por_celula, descritivas, quadros).
- Figuras: [figuras/](figuras) (24 PNGs + `separados/`; nomes de 01 e 17 mantêm o sufixo `quartis`).
- Versão anterior (Q1/Q3): [dados/quartis/](dados/quartis) e [figuras/quartis/](figuras/quartis).

## Quadros do desenho 2³ (figura: [figuras/19a_quadro_combinacoes_teste.png](figuras/19a_quadro_combinacoes_teste.png) e [figuras/19b_matriz_sinais_contrastes.png](figuras/19b_matriz_sinais_contrastes.png); CSVs: [dados/quadro_combinacoes.csv](dados/quadro_combinacoes.csv), [dados/quadro_sinais.csv](dados/quadro_sinais.csv))

### Quadro das combinações de teste
Cada ensaio é repetido r = 30 vezes (m = 36 alunos sorteados com reposição da célula) → 8 × 30 = 240 observações.

| Ensaio | Yates | A (IA) | B (Ansiedade) | C (Estudo) | n alunos | ΔGPA médio | DP |
|:-:|:-:|---|---|---|--:|--:|--:|
| 1 | (1) | −1 Ativo | −1 Baixa (≤ Q2) | −1 Baixas (≤ Q2) | 667 | 0,196 | 0,172 |
| 2 | a | +1 Passivo | −1 Baixa | −1 Baixas | 210 | 0,152 | 0,198 |
| 3 | b | −1 Ativo | +1 Alta (> Q2) | −1 Baixas | 576 | 0,201 | 0,184 |
| 4 | ab | +1 Passivo | +1 Alta | −1 Baixas | 187 | 0,091 | 0,236 |
| 5 | c | −1 Ativo | −1 Baixa | +1 Altas (> Q2) | 639 | 0,317 | 0,170 |
| 6 | ac | +1 Passivo | −1 Baixa | +1 Altas | 235 | 0,252 | 0,176 |
| 7 | bc | −1 Ativo | +1 Alta | +1 Altas | 584 | 0,323 | 0,173 |
| 8 | abc | +1 Passivo | +1 Alta | +1 Altas | 181 | 0,233 | 0,179 |

Cortes: ansiedade Q2 = 4; horas Q2 = 10,91 h.

### Matriz de sinais dos contrastes (efeito = Σ sinal·Ȳ ÷ 4)
A matriz de sinais é a mesma da versão anterior (depende só do desenho); os valores de Ȳ e dos efeitos estão em [dados/quadro_sinais.csv](dados/quadro_sinais.csv): Ȳ = 0,196; 0,152; 0,201; 0,091; 0,317; 0,252; 0,323; 0,233 e efeitos A −0,077, B −0,018, C +0,121, AB −0,023, AC −0,001, BC +0,011, ABC +0,010.

| Ensaio | Yates | I | A | B | C | AB | AC | BC | ABC |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | (1) | + | − | − | − | + | + | + | − |
| 2 | a | + | + | − | − | − | − | + | + |
| 3 | b | + | − | + | − | − | + | − | + |
| 4 | ab | + | + | + | − | + | − | − | − |
| 5 | c | + | − | − | + | + | − | − | + |
| 6 | ac | + | + | − | + | − | + | − | − |
| 7 | bc | + | − | + | + | − | − | + | − |
| 8 | abc | + | + | + | + | + | + | + | + |

## Balanceamento e inferência (melhoria v3)

Seção 8 de [pcc170_entrega02.py](pcc170_entrega02.py); saídas em `dados/esquemas_replica.csv`, `varredura_m.csv`, `inferencia_consolidada.csv`, `teto_gpa.csv` e figuras 20–22.

**O n desigual (181–667) compromete?** Não os efeitos, mas a ortogonalidade e a precisão por célula. O bootstrap/subamostragem com m igual por célula devolve um desenho balanceado; ele **não normaliza** o ΔGPA bruto (só aproxima a distribuição das médias).

| Esquema | Efeitos (A, C, AB) | DP entre réplicas |
|---|---|---|
| boot m=36 (atual) | −0,075; +0,121; −0,023 | ≈ 0,021 |
| boot m=150 | −0,077; +0,121; −0,023 | ≈ 0,011 |
| sem reposição m=150 | −0,078; +0,121; −0,023 | ≈ 0,007 |
| sem reposição m=181 | −0,077; +0,121; −0,023 | ≈ 0,006 |

- Efeitos estimados são **idênticos** em todos os esquemas (±0,003): a estimativa não depende de m nem de reposição.
- **Atenção:** o DP entre réplicas sem reposição encolhe com m (correção de população finita; em m = n seria 0). Ele descreve a variabilidade da subamostra, **não** o erro do estimador. Por isso Shapiro e Levene das réplicas sem reposição falham (p ≈ 0) por construção, e o IC de inferência continua sendo o do **bootstrap completo** (reamostra cada célula com seu n real).
- Seeds: DP entre sementes ≤ 0,0006 (sem reposição m=150).

**Permutação** (5.000; resíduos do modelo reduzido): A p=0,0002; C p=0,0002; AB p=0,0016; B p=0,019; AC 0,95; BC 0,145; ABC 0,18. Concorda com IC bootstrap e HC3 em A, C, AB (significativos) e AC, BC, ABC (nulos). B: permutação 0,019, HC3 0,027, ANOVA bruta 0,017 e IC bootstrap excluindo 0 por pouco: todos concordam em efeito marginal e pequeno.

**Teto de GPA (12,1% no 4,0):** com transformação (reflexão + raiz) e regressão quantílica (mediana) os sinais se mantêm; A −0,051 e C +0,114 na mediana quantílica; B e interações AC/BC/ABC permanecem não significativos.

**Conclusão:** a estimativa de efeitos é robusta ao esquema. A inferência principal é o modelo bruto com HC3 + IC bootstrap completo; permutação e demais esquemas são apêndice; a ANOVA das réplicas é apenas descritiva (p inflado: BC 0,001 vs HC3 0,177).

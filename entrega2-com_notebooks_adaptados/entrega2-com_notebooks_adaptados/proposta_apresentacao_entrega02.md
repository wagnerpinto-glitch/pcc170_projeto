# Proposta Detalhada de Apresentação — Entrega 2: Resultados Preliminares (Versão Expandida com Gráficos Individuais)
**Disciplina:** PCC170 — Projeto e Análise de Experimentos Computacionais  
**Docente:** Prof. Carlos Henrique Gomes Ferreira  
**Discente:** Wagner  
**Tema:** *Impacto do Tipo de Uso de Inteligência Artificial, Nível de Ansiedade e Horas de Estudo Tradicional no Rendimento Acadêmico ($\Delta GPA$)*  
**Formato:** LaTeX Beamer (`Madrid`, Tons em Azul) — 21 Slides Dedicados com Análise Individual de Casos  
**Tempo Estimado de Apresentação:** 15 a 20 minutos (Pontuação: 30%)

---

## 1. Mapeamento de Conformidade com o Escopo da Aula 4

A especificação do documento **`Aula 4 - Descrição do Projeto.pdf`** estabelece seis requisitos avaliativos obrigatórios para a Entrega 2. A estrutura expandida dedica slides exclusivos para cada visualização e análise individual de caso:

| Requisito Avaliativo da Aula 4 | Slides Correspondentes | Códigos Python de Referência | Principais Figuras / Quadros |
| :--- | :---: | :--- | :--- |
| **1. Evidências de viabilidade do projeto experimental** | Slides 2, 4 e 5 | `01_planejamento_pcc170_entrega02.ipynb`<br>`03_falhas_experimentais_pcc170_entrega02.ipynb`<br>`05_projeto_pcc170_entrega02.ipynb` | • Quadro de Auditoria Nativo em LaTeX<br>• Fluxo Amostral em TikZ ($N=50.000 \to n=3.279$) |
| **2. Primeiros resultados obtidos com o projeto fatorial $2^k r$** | Slides 6, 7, 8 e 9 | `01_planejamento_pcc170_entrega02.ipynb`<br>`02_analise_exploratoria_pcc170_entrega02.ipynb` | • `01_cubo_fatorial_resposta.png`<br>• Tabela Yates Nativa em LaTeX<br>• `02_ecdf_fator_A.png`<br>• `02_ecdf_fator_B.png`<br>• `02_ecdf_fator_C.png` |
| **3. Interpretação preliminar dos efeitos principais e interações** | Slides 10, 11, 12, 13, 14 e 15 | `06_fatorial_2k_pcc170_entrega02.ipynb` | • `06_efeito_principal_C.png`<br>• `06_efeito_principal_A.png`<br>• `06_efeito_principal_B.png`<br>• `06_interacao_AB.png`<br>• `06_interacao_AC.png`<br>• `06_interacao_BC.png` |
| **4. Intervalos de confiança e testes de significância aplicáveis** | Slides 16 e 17 | `04_estudos_de_caso_pcc170_entrega02.ipynb`<br>`06_fatorial_2k_pcc170_entrega02.ipynb` | • Quadro de Diagnósticos Nativo em LaTeX<br>• Tabela de Inferência Consolidada<br>• `06_pareto_hc3.png` |
| **5. Avaliação preliminar da hipótese geral do estudo** | Slides 3, 18, 19 e 20 | `01_planejamento_pcc170_entrega02.ipynb`<br>`07_projeto_relatorio_pcc170_entrega02.ipynb` | • `07_sensibilidade_efeitos.png`<br>• `07_sensibilidade_amostra.png`<br>• Quadro Síntese de Validação da Hipótese |
| **6. Indicação de ajustes ou aprimoramentos planejados** | Slide 21 | `07_projeto_relatorio_pcc170_entrega02.ipynb` | • Blocos estruturados com ANCOVA, subpopulações e relatório final LaTeX |

---

## 2. Detalhamento Slide a Slide da Apresentação Expandida

---

### Slide 1: Abertura e Identificação Institucional
* **Tempo sugerido:** 1 min | **Objetivo:** Apresentação formal.
* **Conteúdo:** Título do trabalho, identificação do discente, docente orientador, PPGCC/UFOP e ciclo DoE.

---

### Slide 2: Contextualização e Motivação
* **Tempo sugerido:** 1 min | **Requisito 1 (Viabilidade e Contexto)**.
* **Conteúdo:** O paradoxo da IA generativa no ensino superior (tutoria ativa vs. atalho superficial), interações com hábitos comportamentais (horas de estudo tradicional e ansiedade) e a aplicação do DoE como metodologia científica de avaliação.

---

### Slide 3: Pergunta de Pesquisa, Hipótese Geral e Demarcação Epistemológica
* **Tempo sugerido:** 1.5 min | **Requisito 5 (Hipótese Geral)**.
* **Conteúdo:** Pergunta orientadora, formulação explícita da hipótese geral *a priori* e a ressalva ética de que os dados são observacionais (associações ajustadas robustas, não intervenção clínica).

---

### Slide 4: Estrutura Experimental $2^3 r$ e Variável de Resposta
* **Tempo sugerido:** 1 min | **Requisito 2 (Estrutura Experimental)**.
* **Conteúdo:** Unidade experimental (aluno individual), resposta ($\Delta \text{GPA} = \text{GPA}_{\text{pós}} - \text{GPA}_{\text{pré}}$) e codificação $\pm 1$ dos fatores $A$ (Modo de IA), $B$ (Ansiedade) e $C$ (Horas de Estudo Tradicional).

---

### Slide 5: Auditoria de Integridade e Viabilidade Amostral
* **Tempo sugerido:** 1.5 min | **Requisito 1 (Evidências de Viabilidade)**.
* **Conteúdo:** 
  * **Quadro Nativo em LaTeX:** Checagem de integridade (0 duplicatas, 0 ausentes, GPAs em $[0, 4]$, todas as checagens com status **OK**).
  * **Fluxograma Vetorial em TikZ:** Transição da base completa ($N=50.000$) para a coorte STEM Junior ($n=3.279$).
  * **Garantia de Réplicas:** Menor célula com $n=181$ alunos, superando em mais de 18 vezes a exigência de $r \ge 10$.

---

### Slide 6: Espaço Fatorial $2^3$: Cubo Tridimensional e Células de Yates
* **Tempo sugerido:** 1.5 min | **Requisito 2 (Primeiros Resultados $2^3 r$)**.
* **Imagem:** `figuras/01_cubo_fatorial_resposta.png` (Cubo tridimensional colorido com médias de $\Delta \text{GPA}$ por vértice e tamanhos $n$).
* **Quadro Nativo em LaTeX:** Tabela completa com os 8 ensaios na ordem de Yates, perfis, $n$ e médias $\pm$ desvios-padrão.
* **Explicação do caso:** Pior vértice é `ab` ($\mu = -0.134$) e melhor vértice é `c` ($\mu = +0.104$).

---

### Slide 7: Distribuição Acumulada (ECDF) — Fator A: Modo de Uso de IA
* **Tempo sugerido:** 1 min | **Requisito 2 (AED e Distribuições)**.
* **Imagem:** `figuras/02_ecdf_fator_A.png`
* **Garantia visual:** Eixos claramente identificados com labels completos e legenda em fundo branco no canto superior esquerdo sem sobrepor as curvas.
* **Explicação objetiva do caso:** A curva de uso passivo ($+1$) situa-se consistentemente à esquerda da curva de uso ativo ($-1$), demonstrando probabilidade estocasticamente maior de decréscimo de GPA em quem usa IA como atalho passivo.

---

### Slide 8: Distribuição Acumulada (ECDF) — Fator B: Ansiedade em Provas
* **Tempo sugerido:** 1 min | **Requisito 2 (AED e Distribuições)**.
* **Imagem:** `figuras/02_ecdf_fator_B.png`
* **Garantia visual:** Eixo vertical e horizontal com formatação elegante, legenda limpa.
* **Explicação objetiva do caso:** A curva de alta ansiedade ($+1$) localiza-se discretamente à esquerda da de baixa ansiedade ($-1$), refletindo um efeito moderado e contínuo, sem distorções anômalas nas caudas.

---

### Slide 9: Distribuição Acumulada (ECDF) — Fator C: Horas de Estudo Tradicional
* **Tempo sugerido:** 1 min | **Requisito 2 (AED e Distribuições)**.
* **Imagem:** `figuras/02_ecdf_fator_C.png`
* **Garantia visual:** Rótulos independentes, alta nitidez.
* **Explicação objetiva do caso:** Dominância estocástica expressiva em todos os percentis: a curva de estudo alto ($+1$) desloca-se fortemente para a direita, comprovando que maior estudo tradicional eleva sistematicamente as chances de ganho acadêmico positivo.

---

### Slide 10: Efeito Principal do Fator C: Horas de Estudo Tradicional
* **Tempo sugerido:** 1 min | **Requisito 3 (Efeitos Principais)**.
* **Imagem:** `figuras/06_efeito_principal_C.png`
* **Garantia visual:** Eixo vertical com "Média Balanceada de $\Delta \text{GPA}$", anotações $\mu = -0.057$ e $\mu = +0.064$ sem colisão.
* **Explicação objetiva do caso:** É o fator dominante do experimento: $\mathbf{\Delta = +0.1211}$ (IC 95%: $[+0.106; +0.136]$, $|t|_{\text{HC3}} = 16.98$, $p < 0.0001$). Estudar acima da mediana acrescenta mais de 0,12 pontos líquidos ao GPA.

---

### Slide 11: Efeito Principal do Fator A: Modo de Uso de IA
* **Tempo sugerido:** 1 min | **Requisito 3 (Efeitos Principais)**.
* **Imagem:** `figuras/06_efeito_principal_A.png`
* **Garantia visual:** Eixo vertical completo, anotações $\mu = +0.042$ (ativo) e $\mu = -0.035$ (passivo).
* **Explicação objetiva do caso:** Segundo maior impacto: $\mathbf{\Delta = -0.0772}$ (IC 95%: $[-0.092; -0.062]$, $|t|_{\text{HC3}} = 10.49$, $p < 0.0001$). O uso passivo impõe uma penalidade expressiva frente ao uso como tutoria ativa.

---

### Slide 12: Efeito Principal do Fator B: Ansiedade em Provas
* **Tempo sugerido:** 1 min | **Requisito 3 (Efeitos Principais)**.
* **Imagem:** `figuras/06_efeito_principal_B.png`
* **Garantia visual:** Eixos perfeitamente formatados, anotações de $\mu$ claras.
* **Explicação objetiva do caso:** $\mathbf{\Delta = -0.0175}$ (IC 95%: $[-0.033; -0.002]$, $|t|_{\text{HC3}} = 2.22$, $p = 0.0268$). A ansiedade elevada deprime moderadamente o GPA, com significância estatística assegurada.

---

### Slide 13: Interação Fatorial $A \times B$: Modo de Uso de IA $\times$ Ansiedade
* **Tempo sugerido:** 1.5 min | **Requisito 3 (Interações Fatoriais)**.
* **Imagem:** `figuras/06_interacao_AB.png`
* **Garantia visual:** Legenda das duas retas no canto superior direito sem cruzar com as anotações numéricas dos pontos.
* **Explicação objetiva do caso:** Quebra explícita de paralelismo: efeito $\mathbf{-0.0226}$ ($p = 0.0041$). A queda no $\Delta \text{GPA}$ provocada pelo uso passivo de IA é de $-0.066$ em baixa ansiedade e agrava-se para $\mathbf{-0.088}$ sob alta ansiedade, comprovando uma sinergia negativa aditiva.

---

### Slide 14: Interação Fatorial $A \times C$: Modo de Uso de IA $\times$ Estudo Tradicional
* **Tempo sugerido:** 1 min | **Requisito 3 (Interações Fatoriais)**.
* **Imagem:** `figuras/06_interacao_AC.png`
* **Garantia visual:** Eixos e legendas independentes.
* **Explicação objetiva do caso:** Retas estritamente paralelas: efeito $\mathbf{-0.0005}$ ($p = 0.9507$, IC 95%: $[-0.016; +0.015]$). O benefício das horas de estudo tradicional é preservado integralmente, sem depender do tipo de uso da IA.

---

### Slide 15: Interação Fatorial $B \times C$: Ansiedade $\times$ Estudo Tradicional
* **Tempo sugerido:** 1 min | **Requisito 3 (Interações Fatoriais)**.
* **Imagem:** `figuras/06_interacao_BC.png`
* **Garantia visual:** Rótulos sem sobreposição.
* **Explicação objetiva do caso:** Retas paralelas: efeito $\mathbf{+0.0107}$ ($p = 0.1766$). A dedicação ao estudo tradicional atua como um escudo aditivo protetor, independente do grau de ansiedade do discente.

---

### Slide 16: Diagnósticos Estatísticos dos Pressupostos
* **Tempo sugerido:** 1 min | **Requisito 4 (Intervalos de Confiança e Significância)**.
* **Quadro Nativo em LaTeX:** Teste de Shapiro-Wilk ($W=0.999$, $p=0.115$ $\to$ Normalidade OK); Teste de Levene ($F=4.73$, $p=2.6 \times 10^{-5}$ $\to$ Heterocedasticidade detectada e corrigida com matriz sanduíche HC3); Estabilidade de seeds (máx $\text{DP}=0.0056$); e Balanço do GPA prévio ($p > 0.05$).

---

### Slide 17: Inferência Consolidada e Diagrama de Pareto
* **Tempo sugerido:** 1.5 min | **Requisito 4 (Testes de Significância)**.
* **Imagem:** `figuras/06_pareto_hc3.png` (Gráfico de Pareto das estatísticas $|t|$ com linha de referência $|t|=1.96$).
* **Quadro Nativo em LaTeX:** Tabela com todos os 7 contrastes, estimativas pontuais, ICs 95% Bootstrap, $|t|$ robusto e veredito final (termos significativos: $C, A, AB, B$).

---

### Slide 18: Sensibilidade dos Efeitos a Regras de Corte Alternativas
* **Tempo sugerido:** 1 min | **Requisito 4 e 5 (Robustez e Avaliação)**.
* **Imagem:** `figuras/07_sensibilidade_efeitos.png`
* **Garantia visual:** Gráfico dedicado mostrando as linhas de efeitos sob a regra da Mediana ($n=3.279$) versus Quartis Extremos ($n=848$ e $n=1.101$).
* **Explicação objetiva do caso:** Os sinais e a ordenação de relevância dos fatores mantêm-se idênticos em todas as regras. O efeito de estudo tradicional intensifica-se para $+0.195$ nos quartis extremos, confirmando a robustez dos achados.

---

### Slide 19: Sensibilidade: Amostra Efetiva por Regra de Dicotomização
* **Tempo sugerido:** 1 min | **Requisito 4 e 5 (Robustez e Avaliação)**.
* **Imagem:** `figuras/07_sensibilidade_amostra.png`
* **Garantia visual:** Gráfico de barras horizontais nítido com contagens exatas de alunos.
* **Explicação objetiva do caso:** Justifica a escolha da regra pela mediana, que preserva 100% da coorte ($3.279$ alunos), contra a perda de mais de 66% da amostra nos cortes por quartis, maximizando o poder estatístico dos testes.

---

### Slide 20: Avaliação Preliminar da Hipótese Geral do Estudo
* **Tempo sugerido:** 1.5 min | **Requisito 5 (Avaliação da Hipótese Geral)**.
* **Quadro Nativo em LaTeX:** Confronto direto item por item entre o que foi postulado na hipótese geral e a evidência experimental obtida:
  * Maior estudo tradicional eleva o $\Delta \text{GPA}$ $\implies$ **Corroborado** ($C = +0.1211$);
  * Uso ativo supera o uso passivo de IA $\implies$ **Corroborado** ($A = -0.0772$);
  * Alta ansiedade reduz o $\Delta \text{GPA}$ $\implies$ **Corroborado** ($B = -0.0175$);
  * Interação adversa entre uso passivo e ansiedade $\implies$ **Corroborado** ($AB = -0.0226$);
  * Independência benéfica do estudo tradicional $\implies$ **Evidência original adicionada**.

---

### Slide 21: Aprimoramentos para a Versão Final e Encerramento
* **Tempo sugerido:** 1.5 min | **Requisito 6 (Aprimoramentos Planejados)**.
* **Conteúdo:** Ajustes analíticos para a Entrega Final (modelo ANCOVA com covariáveis contínuas sem discretização e controle pelo GPA prévio exato), análise setorial por cursos STEM, diretrizes pedagógicas institucionais e elaboração do artigo científico no template oficial LaTeX da disciplina. Agradecimentos à banca.

---

## 3. Repositório e Arquivos do Projeto

* Código LaTeX da Apresentação: [`apresentacao/apresentacao_entrega02.tex`](file:///home/wagner/pcc170/apresentacao/apresentacao_entrega02.tex)
* Script de Extração de Imagens Individuais: [`apresentacao/extrair_figuras_individuais.py`](file:///home/wagner/pcc170/apresentacao/extrair_figuras_individuais.py)
* Pasta com Todas as Figuras Individuais em Alta Resolução (PNG e PDF): [`apresentacao/figuras/`](file:///home/wagner/pcc170/apresentacao/figuras/)

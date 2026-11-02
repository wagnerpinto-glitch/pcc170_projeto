# Apresentação da Entrega 2 — PCC170 (Beamer Madrid em Tons de Azul — Versão Corrigida)

Este diretório contém a versão em **LaTeX Beamer** da apresentação para a **Entrega 2: Resultados Preliminares** da disciplina PCC170, estruturada em **22 slides dedicados** com correção completa de escala, legendas livres de sobreposição e tabela de inferência em largura total perfeitamente alinhada.

## Estrutura do Diretório

```
apresentacao/
├── apresentacao_entrega02.tex       # Código-fonte LaTeX da apresentação (22 slides corrigidos)
├── gerar_figuras_corrigidas.py     # Script Python com escalas e offsets corrigidos
├── README.md                        # Instruções e documentação
└── figuras/                         # Todas as figuras individuais (PNG e PDF vetorial)
    ├── 01_cubo_fatorial_resposta.png
    ├── 02_ecdf_fator_A.png          # ECDF individual: Modo de IA
    ├── 02_ecdf_fator_B.png          # ECDF individual: Ansiedade em Provas
    ├── 02_ecdf_fator_C.png          # ECDF individual: Horas de Estudo Tradicional
    ├── 06_efeito_principal_A.png    # Efeito principal A (médias e IC95% em quadro separado)
    ├── 06_efeito_principal_B.png    # Efeito principal B (médias e IC95% em quadro separado)
    ├── 06_efeito_principal_C.png    # Efeito principal C (médias e IC95% em quadro separado)
    ├── 06_interacao_AB.png          # Interação A x B (sem sobreposição de dados/legendas)
    ├── 06_interacao_AC.png          # Interação A x C (retas paralelas, sem colisão)
    ├── 06_interacao_BC.png          # Interação B x C (retas paralelas, sem colisão)
    ├── 06_pareto_hc3.png            # Diagrama de Pareto de |t| robusto HC3
    ├── 07_sensibilidade_efeitos.png # Sensibilidade: Efeitos sob regras de corte
    └── 07_sensibilidade_amostra.png # Sensibilidade: Tamanho amostral n por regra
```

## Correções Implementadas nesta Versão

1. **Correção dos Gráficos de Efeitos Principais (A, B e C):**
   - As médias e os IC95% bootstrap são apresentados em uma tabela abaixo da área do gráfico, sem cobrir a linha nem as barras de erro.
   - A escala do eixo $Y$ se ajusta aos limites dos IC95%, mantendo linhas e intervalos totalmente visíveis.

2. **Eliminação de Sobreposição nas Interações ($A \times B$, $A \times C$, $B \times C$):**
   - O teto do eixo $Y$ foi expandido para $0.35$ (em $AB$), $0.40$ (em $AC$) e $0.38$ (em $BC$), criando uma área livre superior dedicada à legenda com fundo branco semi-transparente.
   - As anotações de valores numéricos dos vértices receberam offsets alternados (acima para a reta superior e abaixo para a inferior), eliminando qualquer colisão com os pontos e linhas.

3. **Alinhamento da Tabela de Inferência Consolidada:**
   - Foi criado um slide exclusivo (Slide 16) com largura total (`\textwidth`), formatado em `\small` com `booktabs`, colunas uniformemente espaçadas, destaque em tom suave (`rowcolor{SoftBlue!40}`) para os termos significativos e vereditos claros sem truncamento.
   - O Diagrama de Pareto de $|t|$ robusto HC3 foi alocado no Slide 17, permitindo leitura limpa e espaçada de ambos os elementos.

## Como Compilar

### Opção 1: Overleaf
1. Compacte a pasta `apresentacao/` (`apresentacao.zip`) com o `.tex` e a pasta `figuras/`.
2. No Overleaf, clique em *New Project* $\rightarrow$ *Upload Project*.
3. O compilador padrão (*pdfLaTeX*) compilará os 22 slides diretamente.

### Opção 2: Linha de Comando (Linux / macOS / Windows)
Com o TeX Live ou MiKTeX:
```bash
pdflatex apresentacao_entrega02.tex
pdflatex apresentacao_entrega02.tex
```

# Apresentação da Entrega 2 — PCC170 (Beamer Madrid em Tons de Azul)

Este diretório contém a versão em **LaTeX Beamer** da apresentação para a **Entrega 2: Resultados Preliminares** da disciplina PCC170.

## Estrutura do Diretório

```
apresentacao/
├── apresentacao_entrega02.tex   # Código-fonte LaTeX da apresentação
├── README.md                    # Instruções de compilação e estrutura
└── figuras/                     # Gráficos utilizados como figuras (PNG)
    ├── 01_cubo_fatorial_resposta.png
    ├── 02_ecdf_delta_gpa_por_fator.png
    ├── 06_efeitos_principais.png
    ├── 06_interacoes_fatoriais.png
    ├── 06_pareto_hc3.png
    └── 07_sensibilidade_cortes.png
```

## Diretrizes Atendidas

1. **Tema e Cores:**
   - Tema: `\usetheme{Madrid}`
   - Cores: Esquema `whale` com personalização refinada em tons de azul (`DarkBlue`, `MedBlue`, `SoftBlue`).
   - Proporção: Widescreen 16:9 (`aspectratio=169`).

2. **Uso de Imagens e Quadros Nativos:**
   - **Gráficos Reais:** Inseridos via `\includegraphics` a partir de `figuras/` (cubo $2^3$, ECDF acumulada, efeitos principais, interações, Pareto HC3 e sensibilidade aos cortes).
   - **Quadros e Tabelas:** Todos os quadros de auditoria, fluxo de amostra (desenhado em TikZ), diagnóstico de premissas, tabela de Yates e tabela de inferência foram criados **diretamente em código LaTeX**, garantindo nitidez tipográfica absoluta.

3. **Tempo Estimado:**
   - 12 slides balanceados para o tempo regulamentar de **15 a 20 minutos**.

## Como Compilar

### Opção 1: Overleaf
1. Compacte esta pasta (`apresentacao.zip`) contendo `apresentacao_entrega02.tex` e a pasta `figuras/`.
2. No Overleaf, clique em *New Project* $\rightarrow$ *Upload Project*.
3. O compilador padrão (*pdfLaTeX*) compilará a apresentação sem necessidade de configurações adicionais.

### Opção 2: Linha de Comando (Linux / macOS / Windows)
Com o TeX Live ou MiKTeX instalado:
```bash
pdflatex apresentacao_entrega02.tex
pdflatex apresentacao_entrega02.tex
```
*(Executar duas vezes para resolver as referências cruzadas e numeração de slides do tema Madrid)*.


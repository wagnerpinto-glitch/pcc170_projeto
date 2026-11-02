# Notebooks adaptados — PCC170 Entrega 2

Esta pasta contém novas versões dos sete notebooks dos exemplos da disciplina,
adaptadas à análise de ΔGPA em `entrega2/pcc170_entrega02.py`. Os notebooks
originais do professor foram preservados.

## Sequência

1. `01_planejamento_pcc170_entrega02.ipynb` — pergunta, fatores, níveis e tabela 2³.
2. `02_analise_exploratoria_pcc170_entrega02.ipynb` — descritivas, cortes e células.
3. `03_falhas_experimentais_pcc170_entrega02.ipynb` — auditoria de dados e desbalanceamento.
4. `04_estudos_de_caso_pcc170_entrega02.ipynb` — comparação de células e diagnósticos.
5. `05_projeto_pcc170_entrega02.ipynb` — protocolo e plano de análise.
6. `06_fatorial_2k_pcc170_entrega02.ipynb` — efeitos, HC3 e IC bootstrap.
7. `07_projeto_relatorio_pcc170_entrega02.ipynb` — síntese e texto-base de resultados.

Os notebooks 01–06 leem o CSV original e procuram a pasta `csv/` no diretório
atual e em seus ancestrais. O notebook 07 lê os resultados gerados pelo script;
para atualizá-los, execute `python pcc170_entrega02.py` dentro de `entrega2/`.
As dependências de análise são as mesmas do script principal (NumPy, pandas,
Matplotlib, Seaborn, SciPy e statsmodels).

## Gráficos

O módulo compartilhado `visualizacoes.py` padroniza o estilo, exporta figuras
em PNG (180 dpi) e PDF vetorial e é importado pelos notebooks. Os arquivos são
salvos em `notebooks_adaptados/figuras/` e também aparecem inline ao executar
as células.

- **01:** cubo 2³ com médias de ΔGPA por vértice e contagem de alunos por célula.
- **02:** distribuições, boxplots por célula e ECDFs por fator.
- **03:** painel de integridade e gráfico do desbalanceamento.
- **04:** distribuição bruta, médias e IC bootstrap por célula, diagnóstico dos resíduos.
- **05:** fluxo amostral e composição das células.
- **06:** forest plot, efeitos principais, interações e Pareto dos testes HC3.
- **07:** forest plot para relatório, sensibilidade aos cortes e diagnósticos.

## Decisões metodológicas mantidas

- Recorte STEM + Junior e corte principal pela mediana (Q2).
- ΔGPA = GPA pós-semestre − GPA pré-semestre.
- Aluno é a unidade observacional; o desenho não é randomizado.
- O modelo principal usa os dados brutos e erros robustos HC3.
- O bootstrap estratificado estima IC95%; reamostras não são novas unidades.
- Quartis e regressão contínua permanecem como análises de sensibilidade.
- Resultados são associações; não sustentam afirmações causais.

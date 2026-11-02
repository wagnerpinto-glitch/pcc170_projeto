# PCC170 — análise da documentação e base para o projeto

**Disciplina:** Projeto e Análise de Experimentos Computacionais (PCC170)  
**Período indicado nos materiais:** 2026/2  
**Data desta análise:** 31/10/2026  
**Finalidade:** consolidar as regras da disciplina, analisar a proposta da Aula 4 e transformar o material já existente em uma base concreta para iniciar o projeto.

> **Síntese executiva.** O trabalho não é apenas uma análise de dados nem uma comparação observacional entre grupos. O requisito metodológico central é planejar e executar um experimento fatorial completo \(2^k\), com pelo menos dez replicações independentes por combinação, e analisar efeitos principais e interações. O notebook atual oferece uma boa entrada exploratória para o tema de IA e estudantes, mas sua hipótese sobre uso de IA, ansiedade e horas de estudo usa características observadas dos estudantes como se fossem fatores experimentais. Isso não satisfaz, por si só, a exigência de experimento computacional controlado. A recomendação deste documento é preservar o domínio e os dados disponíveis, mas formular o experimento em torno de escolhas controláveis do pipeline de classificação.

## 1. Escopo e fontes consultadas

Foram examinados os materiais do diretório `Material Alunos DoE 2026-2`, o plano de ensino, os sete notebooks exemplares, o CSV do projeto e o notebook ajustado da Entrega 1. A documentação foi lida para identificar requisitos explícitos, sequência didática, práticas de análise e a relação entre a proposta atual e o experimento exigido.

| Material | Como contribui para esta análise |
|---|---|
| [Aula 1 - Apresentação da Disciplina.pdf](<./Material Alunos DoE 2026-2/Aula 1 - Apresentação da Disciplina.pdf>) e [PCC 170 - Projeto e Análise de Experimentos Computacionais.pdf](<./Material Alunos DoE 2026-2/PCC 170 - Projeto e Análise de Experimentos Computacionais.pdf>) | Objetivos, ementa, avaliação, cronograma, ferramentas e contexto da disciplina. |
| [Aula 2 - Introdução ao Curso.pdf](<./Material Alunos DoE 2026-2/Aula 2 - Introdução ao Curso.pdf>) | Ciclo do experimento: problema, objetivo, hipótese, fatores, planejamento, execução, análise, apresentação e reprodutibilidade. |
| [Aula 3 - Material Suplementar sobre Python.pdf](<./Material Alunos DoE 2026-2/Aula 3 - Material Suplementar sobre Python.pdf>) | Referência prática para Python, Jupyter/Colab, NumPy, Pandas, gráficos e manipulação de dados. |
| [Aula 4 - Descrição do Projeto.pdf](<./Material Alunos DoE 2026-2/Aula 4 - Descrição do Projeto.pdf>) | Regras obrigatórias, conteúdo das entregas e critérios do projeto. É a referência operacional principal. |
| [Aula 4.1 Proposta do Projeto DoE.pdf](<./Material Alunos DoE 2026-2/Aula 4.1 Proposta do Projeto DoE.pdf>) | Motivação e exemplos de projetos fatoriais e de comparação entre sistemas/métodos. |
| [Aula 5 - Revisão Probabilidade e Estatística.pdf](<./Material Alunos DoE 2026-2/Aula 5 - Revisão Probabilidade e Estatística.pdf>) | Estatística descritiva, distribuições, associação e visualizações para a AED. |
| [Aula 6 - Comparação entre experimentos.pdf](<./Material Alunos DoE 2026-2/Aula 6 - Comparação entre experimentos.pdf>) | População e amostra, intervalos de confiança, testes, comparação pareada/não pareada e bootstrap. |
| [Aula 7 - Projetos Fatoriais.pdf](<./Material Alunos DoE 2026-2/Aula 7 - Projetos Fatoriais.pdf>) | Fatores, níveis, interações, projetos completos/fracionados, replicação, ANOVA, efeitos e premissas. |
| [Notebooks com exemplos/notebooks/](<./Material Alunos DoE 2026-2/Notebooks com exemplos/notebooks/>) | Exemplos executáveis de planejamento, análise, falhas experimentais, estudos de caso e relatório. |
| [ai_student_impact_dataset.csv](<./csv/ai_student_impact_dataset.csv>) e [pcc170_entrega01_ajustada.ipynb](./pcc170_entrega01_ajustada.ipynb) | Base e análise exploratória/proposta de tema já desenvolvidas. |
| [PCC170_2026_2_WagnerTironiPinto_Entrega01.pdf](<./Entregas/PCC170_2026_2_WagnerTironiPinto_Entrega01.pdf>) | PDF de entrega existente. A extração textual retornou zero linhas; portanto, esta análise usa o notebook como evidência do conteúdo, sem afirmar que o PDF foi conferido visualmente. |
| [Link para submissão da etapa 2.docx](<./Material Alunos DoE 2026-2/Link para submissão da etapa 2.docx>) | Contém o endereço do formulário de submissão da etapa 2: <https://forms.gle/aoS5EDPHFy3RPakR8>. |

O nome de origem, autores, versão, licença e documentação do CSV não foram encontrados entre os arquivos listados. Isso é uma lacuna a resolver antes de apresentar a base como dado real ou publicar resultados. A existência de 50 mil linhas, por si só, não comprova que sejam observações reais ou representativas.

## 2. O que a disciplina espera que o projeto demonstre

O plano de ensino organiza a disciplina em torno de planejamento experimental, comparação estatística e projeto fatorial. O projeto é o fio condutor que aplica esses conteúdos a um problema de computação, otimização, aprendizado de máquina ou área relacionada à pesquisa do aluno.

### 2.1 Ciclo experimental

O fluxo ensinado nos materiais é:

1. delimitar um problema relevante e um cenário de uso;
2. definir o objetivo e formular a hipótese geral **antes** de observar os resultados experimentais;
3. especificar a unidade experimental, fatores, níveis e variável(is) de resposta;
4. identificar condições que devem permanecer constantes e fontes de variação;
5. planejar combinações, replicações e ordem aleatória;
6. executar e registrar o experimento;
7. explorar e validar os dados;
8. estimar efeitos e incerteza, testar hipóteses e interpretar interações;
9. relatar limitações, aplicação final e próximos passos;
10. preservar código, dados, configurações e ambiente para permitir reprodução.

### 2.2 Requisitos metodológicos obrigatórios

O [guia da Aula 4](<./Material Alunos DoE 2026-2/Aula 4 - Descrição do Projeto.pdf>) exige:

- contextualização, motivação e definição do problema;
- objetivo delimitado;
- hipótese geral prévia sobre a relação esperada entre fatores e resposta;
- análise exploratória dos dados (AED), separada da avaliação da hipótese;
- projeto fatorial completo \(2^k\), com todas as combinações de \(k\) fatores binários;
- pelo menos \(r=10\) replicações independentes **por combinação**;
- identificação da unidade experimental, fatores, níveis, resposta, controles e aleatorização;
- fonte dos dados e ambiente computacional, incluindo ferramentas, bibliotecas e versões;
- análise de efeitos principais, interações, intervalos de confiança e testes aplicáveis;
- avaliação final da hipótese, limitações, aplicação do experimento e trabalhos futuros.

Assim, um fatorial \(2^3\) tem \(2^3=8\) combinações. Com dez replicações por combinação, são pelo menos \(8 \times 10=80\) execuções completas. A quantidade de linhas do conjunto de dados não substitui esse número de execuções.

Uma replicação deve ser uma nova execução completa da combinação experimental, com nova amostra, divisão dos dados ou semente, conforme o problema. O guia alerta que as partições de uma única validação cruzada não são automaticamente replicações independentes. O projeto deve explicar exatamente o que muda entre replicações, o que permanece igual e qual população de variabilidade as replicações representam.

### 2.3 AED não é análise dos efeitos fatoriais

A AED é descritiva: apresenta a estrutura, distribuição, qualidade e limitações dos dados, podendo orientar o planejamento. Não é o lugar para antecipar a conclusão sobre a hipótese experimental. Por exemplo:

- **AED:** descrever distribuição das classes, valores faltantes, escalas, assimetrias, outliers, relações entre variáveis e viabilidade da tarefa;
- **análise experimental:** comparar as respostas das combinações do fatorial, estimar efeitos, intervalos de confiança, significância e interações;
- **discussão:** interpretar os resultados experimentais frente à hipótese e às limitações.

Essas três funções devem aparecer separadamente na apresentação e no relatório.

## 3. Progressão dos materiais da disciplina

| Material | Conteúdo e uso no projeto |
|---|---|
| Aula 1 — apresentação | Introduz experimentação, reprodutibilidade, objetivos e avaliação. Enquadra o projeto como aplicação dos conteúdos, não como simples relatório descritivo. |
| Aula 2 — introdução | Sistematiza a pergunta, os objetivos, hipótese, fatores, desenho, execução, análise e comunicação. Apresenta o ciclo que deve orientar o trabalho. |
| Aula 3 — Python | Oferece apoio técnico em Jupyter/Colab, bibliotecas, estruturas de dados, funções, NumPy, Pandas e visualização. É suporte de implementação, não um requisito estatístico alternativo. |
| Aula 5 — probabilidade e estatística | Revisa média, mediana, moda, variância, desvio-padrão, quartis, IQR, assimetria, curtose, covariância, correlação, histogramas, boxplots, PMF/PDF/CDF e gráficos de associação. Serve principalmente à AED e à leitura de respostas. |
| Aula 6 — comparação | Discute população/amostra, estatísticas/parâmetros, intervalos de confiança, distribuições \(t\) e \(z\), testes de médias, comparações pareadas e não pareadas, métodos paramétricos/não paramétricos e bootstrap. A escolha do teste depende do desenho e das premissas; não deve ser feita apenas pela conveniência. |
| Aula 7 — fatoriais | Introduz fatores e níveis, efeitos principais e interações, fatoriais completos e fracionados, tabela de sinais, alocação da variação, \(2^k r\), erro experimental, intervalos e premissas. O tema central do experimento obrigatório. |
| Notebooks 01–07 | Materializam planejamento, organização da ordem de execução, modelo e coeficientes, ANOVA, intervalos, diagnóstico de resíduos, erros de coleta/transcrição, escalas, estudos de caso e relatório. O notebook 07 também organiza preparação, pergunta, CSV de execução e interpretação. |

Os exemplos da Aula 4.1 mostram o padrão esperado: pergunta aplicada, hipótese sobre fatores manipuláveis ou parâmetros de métodos, resposta mensurável, combinações fatoriais, replicações e interpretação do resultado. Entre os exemplos estão virtualizadores sob recursos/cargas diferentes, seleção de pseudorrótulos, parâmetros do UMAP e detecção de congelamento da marcha. A mensagem é escolher um problema suficientemente específico e tecnicamente viável; um projeto complexo não é automaticamente melhor.

## 4. Entregas, avaliação e datas

O guia da Aula 4 define três marcos, que somam a nota do projeto:

| Marco | Conteúdo/formato | Peso e tempo |
|---|---|---|
| Entrega e apresentação 1 — proposta e AED | Apresentação em PDF; problema, objetivo, hipótese, estrutura experimental, todas as combinações e \(r \geq 10\), fonte, ambiente e AED. | 20%; 15–20 min. |
| Entrega e apresentação 2 — resultados preliminares | Viabilidade, primeiros resultados do fatorial, efeitos e interações preliminares, intervalos/testes aplicáveis, avaliação inicial da hipótese e ajustes planejados. | 30%; 15–20 min. |
| Trabalho final — apresentação e relatório | Apresentação e relatório final em PDF. O guia pede relatório em LaTeX no modelo disponibilizado, incorporando correções das apresentações. | 50%; 15–20 min. |

O guia registra as datas 21/09 para a primeira entrega, 26/10 para a segunda e 30/11 para o final. O plano de ensino indica apresentações distribuídas em 21/09–30/09, 26/10–23/11 e 30/11–07/12, com entrega de relatórios em 09/12. Há, portanto, diferença entre o prazo final do guia e a distribuição do cronograma. **Como a data desta análise é 31/10/2026, os prazos indicados para as etapas 1 e 2 já passaram.** É necessário confirmar diretamente com o docente qual calendário vale para a turma e como regularizar ou adaptar o andamento; não se deve inferir uma autorização a partir desta síntese.

O guia também informa que a apresentação é obrigatória e que a ausência na data/ordem agendada implica nota zero para o trabalho; trocas de ordem requerem autorização prévia. O plano de ensino declara que ferramentas de IA, celulares e outros dispositivos não devem ser usados durante as aulas, salvo autorização pedagógica do docente. Essa regra se refere ao contexto indicado no plano; convém confirmar com o professor quais são as regras para apoio externo ao horário de aula e para a elaboração do trabalho.

## 5. Análise do material de projeto já existente

### 5.1 Base disponível

O arquivo [ai_student_impact_dataset.csv](<./csv/ai_student_impact_dataset.csv>) contém **50.000 linhas, 16 colunas e nenhum valor ausente** na leitura estrutural feita para esta análise. Entre as colunas estão:

- perfil: `Major_Category`, `Year_of_Study`;
- uso de IA: `Weekly_GenAI_Hours`, `Primary_Use_Case`, `Prompt_Engineering_Skill`, `Tool_Diversity`, `Paid_Subscription`, `Institutional_Policy`, `Perceived_AI_Dependency`;
- atributos acadêmicos e relacionados: `Pre_Semester_GPA`, `Traditional_Study_Hours`, `Anxiety_Level_During_Exams`, `Post_Semester_GPA`, `Skill_Retention_Score`;
- identificador e alvo possível: `Student_ID`, `Burnout_Risk_Level`.

As classes de `Burnout_Risk_Level` têm 16.369 casos `Low` (32,7%), 21.144 `Medium` (42,3%) e 12.487 `High` (25,0%). A distribuição não é perfeitamente equilibrada, mas nenhuma classe é residual. `Student_ID` é único por linha e não deve ser usado como preditor.

O notebook filtra `Major_Category == STEM` e `Year_of_Study == Junior`, chegando a **3.279 registros**. Nesse recorte, a ansiedade tem Q1=3, mediana=4 e Q3=6; horas de estudo tradicional têm Q1=7,33, mediana=10,91 e Q3=14,475. Esses valores descrevem o recorte observado; não definem, por si, tratamentos experimentais.

### 5.2 O que o notebook ajustado já faz

O [notebook da Entrega 1](./pcc170_entrega01_ajustada.ipynb) calcula `Delta_GPA = Post_Semester_GPA - Pre_Semester_GPA`, define uma classificação binária de uso de IA (“ativo” versus “passivo”), restringe a análise a estudantes STEM do terceiro ano e contém:

- estatísticas descritivas e visualizações da base;
- propensity score matching com ansiedade, horas de estudo e GPA pré-semestre;
- diagnóstico de balanceamento por standardized mean difference (Love plot);
- bootstrap para estimar diferença média de \(\Delta GPA\) entre os grupos;
- importância por permutação e gráficos de distribuições/boxplots;
- uma proposta preliminar de fatorial \(2^3\): uso de IA, ansiedade e horas de estudo, com \(\Delta GPA\) como resposta;
- uma sugestão de usar quartis para escolher níveis baixo/alto de ansiedade e estudo.

O material fornece um tema e uma AED inicial útil, mas os itens abaixo precisam ser resolvidos antes de transformar essa proposta em experimento fatorial:

1. **Os fatores propostos são atributos observados dos estudantes, não fatores controlados pelo experimento.** O tipo de uso, a ansiedade e as horas de estudo não foram atribuídos aleatoriamente. Formar oito grupos ou recodificar valores em baixo/alto não cria as oito condições experimentais nem permite interpretar os efeitos como efeitos causais de tratamentos.
2. **O agrupamento “uso ativo/passivo” exige justificativa.** O notebook classifica `Copywriting/Drafting` e `Direct_Answer_Generation` como “passivo”, e os outros casos como “ativo”. Essa regra mistura casos de uso distintos e não é validada pela coluna original; precisa de definição conceitual e fonte, ou deve ser tratada apenas como uma recodificação exploratória.
3. **A dicotomização por quartis descarta a faixa central.** Usar \(\leq Q1\) e \(\geq Q3\) pode ser uma escolha para comparar extremos, mas reduz a amostra e muda o escopo da inferência. Os limiares devem ser definidos antes do experimento, justificados e aplicados sem selecionar retrospectivamente os resultados mais favoráveis.
4. **Matching e bootstrap não substituem o fatorial computacional.** São técnicas de análise observacional. O matching depende de covariáveis, sobreposição e ausência de confundidores não medidos; bootstrap quantifica incerteza sob as unidades reamostradas, mas não converte estudantes em replicações de execuções computacionais.
5. **A origem da base é desconhecida no diretório.** Sem fonte, versão, licença, método de coleta e descrição das variáveis, não é seguro afirmar que a base representa estudantes reais. Investigar se os dados são sintéticos ou observacionais e descrever essa limitação.
6. **Há risco de execução com dados simulados sem perceber.** O notebook tenta abrir `ai_student_impact_dataset.csv` no diretório atual e contém fallback que gera dados simulados. A base disponível está em `csv/ai_student_impact_dataset.csv`. Se o caminho não for corrigido, uma execução pode não usar o CSV pretendido e produzir resultados sintéticos. Remover o fallback silencioso ou interromper a execução com erro explícito quando o arquivo esperado não for encontrado.
7. **O PDF da entrega precisa de conferência visual.** Como sua extração textual não retornou conteúdo, confirmar que os slides estão consistentes com o notebook, especialmente a formulação da hipótese, os números do recorte e a distinção entre associação e causalidade.

## 6. Direção recomendada para um experimento compatível

Uma forma de preservar o tema de IA e estudantes sem confundir associação com experimento é usar o CSV como conjunto de dados fixo e conduzir um **experimento computacional sobre o pipeline de classificação**. Nesse desenho, os fatores são decisões do pipeline que o analista controla; os registros dos estudantes são dados de entrada, não unidades às quais se atribuem tratamentos.

### 6.1 Título de trabalho

**Efeito da representação de variáveis de uso de IA e da configuração do classificador na predição do risco de burnout estudantil**

Este é um recorte inicial para validação com o docente e após verificação da proveniência da base. Não equivale a afirmar que uso de IA causa burnout.

### 6.2 Pergunta, objetivo e hipótese

- **Problema:** não se sabe se acrescentar indicadores de uso de IA a atributos acadêmicos gerais melhora a classificação computacional de níveis de risco de burnout, nem se o resultado depende do classificador e do tratamento do desbalanceamento.
- **Objetivo:** quantificar os efeitos de (i) incluir indicadores de uso de IA, (ii) escolher entre dois classificadores e (iii) ponderar classes na macro-F1 para `Burnout_Risk_Level`.
- **Hipótese geral proposta:** incluir indicadores de uso de IA melhora a macro-F1 em relação ao conjunto de atributos acadêmicos gerais, e a magnitude desse efeito depende do classificador e da ponderação de classes.
- **Limite da interpretação:** a hipótese trata de desempenho preditivo nesta base e neste protocolo. Não é uma hipótese causal sobre comportamento, saúde ou desempenho de estudantes.

### 6.3 Fatores, níveis e desenho proposto

| Fator | Nível baixo (-1) | Nível alto (+1) | Regra operacional proposta |
|---|---|---|---|
| A — conjunto de atributos | Base geral | Base geral + atributos de uso de IA | Definir previamente as listas de colunas; excluir ID, alvo e atributos posteriores ao desfecho. |
| B — classificador | Regressão logística | Random Forest | Fixar implementação, hiperparâmetros e pré-processamento de cada algoritmo antes da coleta experimental. |
| C — ponderação de classes | Desativada (`class_weight=None`) | Ativada (`class_weight="balanced"`) | Usar a configuração equivalente disponível nos dois classificadores e registrar versões. |

**Estrutura:** fatorial completo \(2^3\), oito combinações, dez replicações por combinação, totalizando **80 ajustes e avaliações**. A matriz a seguir enumera os tratamentos; a ordem real de execução deve ser aleatorizada:

| Ensaio | A — atributos IA | B — classificador | C — pesos de classe |
|---:|:---:|:---:|:---:|
| 1 | -1 | -1 | -1 |
| 2 | +1 | -1 | -1 |
| 3 | -1 | +1 | -1 |
| 4 | +1 | +1 | -1 |
| 5 | -1 | -1 | +1 |
| 6 | +1 | -1 | +1 |
| 7 | -1 | +1 | +1 |
| 8 | +1 | +1 | +1 |

### 6.4 Unidade experimental, resposta e protocolo

- **Unidade experimental:** uma execução completa de preparação, treinamento e avaliação do classificador para uma combinação de fatores, em uma partição de dados especificada.
- **Resposta primária:** macro-F1 calculada no conjunto de teste. Ela dá peso igual às três classes, reduzindo a dominância da classe `Medium`.
- **Respostas secundárias:** balanced accuracy e tempo de treinamento; definir previamente como serão medidos e interpretados. Não escolher a resposta principal depois de ver qual resultado “funcionou”.
- **Replicações:** gerar dez partições estratificadas treino/teste com sementes independentes. Em cada partição, executar as oito combinações; a partição é um bloco comum, permitindo comparar tratamentos sob as mesmas linhas de treino e teste. Isso produz dez execuções por combinação. Registrar as sementes e a associação partição–ensaio. A aceitação desse esquema de replicação/blocagem deve ser confirmada com o professor; não tratar folds de uma única validação cruzada como dez replicações independentes.
- **Aleatorização:** aleatorizar a ordem das oito execuções dentro de cada bloco/semente. Se o algoritmo for estocástico, registrar e controlar as sementes do modelo, distinguindo-as das sementes de divisão.
- **Controles:** mesmo alvo, mesma proporção treino/teste, estratificação, pré-processamento, critérios de parada, orçamento computacional e versões. Ajustar transformações somente no treino para evitar vazamento.
- **Possível conjunto de atributos:** o nível “base geral” poderia conter `Major_Category`, `Year_of_Study`, `Pre_Semester_GPA` e `Traditional_Study_Hours`; o nível “base geral + IA” acrescentaria `Weekly_GenAI_Hours`, `Primary_Use_Case`, `Prompt_Engineering_Skill`, `Tool_Diversity`, `Paid_Subscription`, `Institutional_Policy` e `Perceived_AI_Dependency`. A lista final deve ser justificada e congelada antes das execuções.
- **Exclusões preventivas:** retirar `Student_ID`; retirar `Burnout_Risk_Level` dos preditores; não usar `Post_Semester_GPA` ou `Skill_Retention_Score` até esclarecer quando e como foram medidos e se participam da definição do risco; avaliar `Anxiety_Level_During_Exams` como possível proxy/vazamento e não incluí-la sem justificativa.

O delineamento deve investigar também se o alvo foi criado a partir de alguma das variáveis candidatas. Se isso ocorreu, o modelo pode apenas reconstruir uma regra de geração/rotulagem, em vez de revelar uma capacidade preditiva válida. Esse risco reforça a necessidade de obter a documentação de origem da base antes de interpretar os resultados.

### 6.5 Análise estatística planejada

1. Manter uma tabela de execução em formato longo, com uma linha por execução e, no mínimo: ID do bloco/replicação, ordem realizada, níveis A/B/C, semente, versão/configuração, métricas e status/erro.
2. Conferir os dados, contagens por combinação, duplicatas, falhas, valores ausentes e consistência dos níveis antes de modelar.
3. Estimar efeitos principais de A, B e C e interações AB, AC, BC e ABC sobre a macro-F1. Não limitar a leitura à comparação das médias brutas se uma interação indicar que o efeito depende de outro fator.
4. Usar o modelo fatorial/ANOVA conforme o material da Aula 7, incorporando o bloco de partição se o protocolo for aceito como blocado. Relatar estimativas, erro-padrão, graus de liberdade, intervalos de confiança, estatística e valor-p aplicáveis.
5. Verificar pressupostos pelos resíduos e gráficos. Se variância, distribuição ou independência forem inadequadas, discutir transformação ou abordagem alternativa compatível com as aulas; não escolher testes por automatismo.
6. Apresentar tamanho/direção dos efeitos e incerteza, não apenas significância. Com múltiplas métricas, declarar a primária e tratar as demais como secundárias/exploratórias.
7. Avaliar a hipótese após a análise. “Não significativo” não demonstra ausência de efeito; relatar limites de potência e variabilidade.
8. Aplicar a configuração escolhida à finalidade final (por exemplo, classificar casos no conjunto de teste), mostrar matriz de confusão e métricas por classe e descrever limites de generalização. Não avaliar no mesmo conjunto usado para escolher a configuração.

## 7. Plano de AED para a primeira apresentação

A AED pode ser reaproveitada, revisada e separada da análise experimental. Um roteiro adequado para esta base:

1. **Proveniência:** fonte, autores, data/versão, licença, população, método de coleta ou geração, unidade de observação e dicionário de dados.
2. **Integridade:** dimensões, tipos, duplicatas, campos ausentes, faixas válidas, cardinalidade e identificador.
3. **Alvo:** contagens e proporções de `Burnout_Risk_Level`; verificar rótulos e documentação de sua construção.
4. **Variáveis:** estatísticas numéricas (média, mediana, dispersão, quartis, mínimo/máximo); frequências de categorias; histogramas, boxplots e gráficos de associação adequados às escalas.
5. **Relações e qualidade:** correlações com cautela para escalas ordinais, possíveis outliers, redundância e potenciais proxies do alvo. Distinguir associação de efeito causal.
6. **Recorte analítico:** justificar se os 50 mil registros serão usados ou se haverá filtro. O recorte STEM + Junior contém 3.279 linhas e reduz o escopo de generalização; para o classificador proposto, começar com a base completa é mais simples, desde que proveniência e qualidade sejam confirmadas.
7. **Viabilidade:** mostrar que há dados suficientes por classe, que o pipeline pode ser executado 80 vezes e que as métricas e recursos são compatíveis com o prazo.

Os resultados observados na AED não devem ser apresentados como confirmação da hipótese do fatorial. Se a origem da base não puder ser verificada, indicar explicitamente que a análise descreve o arquivo disponível e que não sustenta conclusões sobre estudantes reais.

## 8. Estrutura sugerida para as apresentações e o relatório

### Apresentação inicial (15–20 minutos)

1. título, domínio e motivação;
2. problema e cenário de uso;
3. objetivo e hipótese geral prévia;
4. base, proveniência e unidade observacional;
5. AED: qualidade, alvo, classes, variáveis e limitações;
6. unidade experimental computacional e fatores/níveis;
7. tabela das oito combinações e plano das dez replicações;
8. variáveis de resposta, controles, aleatorização e ambiente;
9. viabilidade, ameaças à validade e próximos passos.

### Relatório final

Seguir as seções requeridas no guia: cabeçalho/resumo; introdução; AED; materiais e métodos; resultados experimentais; caracterização/aplicação final; discussão; conclusões e trabalhos futuros. Em materiais e métodos, especificar todos os dados e procedimentos necessários para outra pessoa repetir as execuções. Em resultados, separar os efeitos do fatorial da aplicação final do modelo.

## 9. Riscos, decisões pendentes e próximos passos

| Prioridade | Pendência/risco | Ação recomendada |
|---|---|---|
| Imediata | Prazos 21/09 e 26/10 já passaram na data desta análise; fontes divergem sobre o calendário final. | Confirmar com o docente situação, prazos válidos e entregas ainda aceitas. |
| Imediata | Proveniência, versão e licença do CSV desconhecidas. | Localizar fonte/dicionário ou obter autorização e registrar claramente se a base é sintética. |
| Imediata | Notebook pode carregar caminho errado e gerar dados simulados. | Corrigir a leitura para `csv/ai_student_impact_dataset.csv`, validar arquivo e interromper com erro claro; remover fallback que pareça sucesso. |
| Alta | Hipótese inicial trata atributos de estudantes como fatores manipulados. | Não usar esse fatorial observacional como evidência causal; validar com o professor a reformulação como experimento de pipeline. |
| Alta | Possível vazamento/definição circular do alvo de burnout. | Investigar como o rótulo foi produzido e revisar atributos permitidos antes de treinar. |
| Alta | Replicações em dados fixos podem ter dependência por sobreposição de partições. | Descrever as partições como blocos/replicações de execução, usar sementes pré-definidas e obter confirmação docente sobre o protocolo inferencial. |
| Média | Classificadores têm hiperparâmetros próprios e podem diferir em escala/tempo. | Fixar e documentar configurações; não ajustar hiperparâmetros com o conjunto de teste. |
| Média | Muitas análises exploratórias podem dispersar o escopo. | Definir uma resposta primária e um protocolo antes das 80 execuções. |

### Sequência prática sugerida

1. Confirmar calendário e regras de entrega com o professor.
2. Verificar origem, licença, documentação e natureza real/sintética do CSV.
3. Escolher e congelar alvo, colunas permitidas, fatores, níveis, métrica primária, divisão e sementes.
4. Ajustar o notebook para carregar a base certa e registrar falhas sem gerar substitutos silenciosamente.
5. Concluir AED e avaliar riscos de vazamento e viabilidade.
6. Implementar um piloto curto para validar o pipeline, sem usar o piloto como parte das replicações finais.
7. Executar as oito combinações em dez blocos/partições pré-definidos, aleatorizando a ordem e salvando cada execução.
8. Analisar efeitos e interações, verificar premissas, preparar a entrega preliminar e incorporar o feedback.
9. Congelar código/configurações, executar a versão final, gerar relatório LaTeX/PDF e apresentação.

## 10. Checklist de aprovação antes da coleta experimental

- [ ] O problema e o contexto de uso estão delimitados?
- [ ] A hipótese geral foi escrita antes dos resultados experimentais?
- [ ] A origem e a natureza da base estão documentadas?
- [ ] O alvo e a unidade observacional foram definidos sem vazamento?
- [ ] A unidade experimental é uma execução completa do pipeline?
- [ ] Os fatores são decisões computacionais controláveis e cada um tem exatamente dois níveis?
- [ ] As \(2^k\) combinações estão enumeradas?
- [ ] Há pelo menos dez execuções completas por combinação?
- [ ] O protocolo explica como as replicações são independentes ou blocadas e por que isso é apropriado?
- [ ] A ordem é aleatória e todas as condições controladas estão registradas?
- [ ] A métrica primária, as métricas secundárias e os critérios de análise foram definidos previamente?
- [ ] A AED está separada da análise do fatorial?
- [ ] O carregamento do CSV falha explicitamente quando a base não está no caminho esperado?
- [ ] Código, ambiente, versões, sementes, dados e resultados serão preservados?
- [ ] O cronograma e o formato foram confirmados com o docente?

## 11. Referências locais

- [Aula 4 - Descrição do Projeto.pdf](<./Material Alunos DoE 2026-2/Aula 4 - Descrição do Projeto.pdf>) — fonte primária dos requisitos e entregas.
- [Aula 4.1 Proposta do Projeto DoE.pdf](<./Material Alunos DoE 2026-2/Aula 4.1 Proposta do Projeto DoE.pdf>) — exemplos de projetos e motivação para o uso do fatorial.
- [PCC 170 - Projeto e Análise de Experimentos Computacionais.pdf](<./Material Alunos DoE 2026-2/PCC 170 - Projeto e Análise de Experimentos Computacionais.pdf>) — ementa, objetivos, avaliação e calendário.
- [Notebooks exemplares](<./Material Alunos DoE 2026-2/Notebooks com exemplos/notebooks/>) — execução do planejamento e análise fatorial.
- [Notebook ajustado da Entrega 1](./pcc170_entrega01_ajustada.ipynb) e [CSV](<./csv/ai_student_impact_dataset.csv>) — estado atual do trabalho, a revisar conforme as distinções metodológicas deste documento.


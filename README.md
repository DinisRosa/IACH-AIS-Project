# IACH-AIS-Project

Projeto de Inteligência Artificial Centrada no Humano para análise de
trajetórias AIS e deteção de atividade de pesca.

## Objetivo

O projeto investiga a segmentação semântica de trajetórias AIS em duas
classes:

- **Navegação**: classes originais `01`, `03` e `05`;
- **Pesca**: classes originais `02` e `04`.

A proposta científica estuda a utilização de janelas sobrepostas e
pós-processamento temporal, mantendo a decisão final sob responsabilidade de
um inspetor humano. A proposta completa está em
[`latex/proposta_pt.tex`](latex/proposta_pt.tex).

## Estado atual

### Implementado

- Conversão do dataset de CSV para JSON em
  [`CODE/partition_dataset.py`](CODE/partition_dataset.py);
- Agrupamento dos pontos por trajetória/ID;
- Centralização de caminhos, features, classes e parâmetros em
  [`CODE/constants.py`](CODE/constants.py);
- Análise exploratória e geração de figuras em
  [`CODE/visualizations.py`](CODE/visualizations.py);
- Análises de distribuição de classes, fragmentação, features por classe,
  outliers, gaps temporais, normalização e janelas sobrepostas;
- Figuras resultantes disponíveis em [`figures/`](figures/);
- Proposta de projeto em português e respetivos PDFs em [`latex/`](latex/);
- Bibliografia científica reunida em [`bibliografia/`](bibliografia/).

### Ainda planeado

O classificador de janelas, os baselines HMM/Wu et al., o pós-processamento
temporal, a avaliação quantitativa e o dashboard de apoio à decisão humana
descritos na proposta ainda não fazem parte do pipeline implementado.

## Dados

O dataset utilizado é o
[Detailed Labelled Fishing Trajectories from AIS](https://www.kaggle.com/datasets/thedevastator/detailed-labelled-fishing-trajectories-from-ais),
obtido através do Kaggle.

O repositório contém:

- uma amostra parcial em `CODE/database/partial/`;
- os ficheiros processados do dataset completo em `CODE/database/full/`,
  quando disponíveis localmente.

O CSV completo não é obtido automaticamente pelo projeto e pode não estar
versionado devido ao seu tamanho. Nesse caso, deve ser descarregado a partir
do Kaggle e colocado em:

```text
CODE/database/full/128_fishing_trajs.csv
```

Os caminhos atualmente utilizados pelo pipeline estão definidos em
[`CODE/constants.py`](CODE/constants.py). Para trabalhar com a amostra
parcial, alterar `ALL_TRAJS` para `False`.

## Como executar

A partir da raiz do projeto:

```bash
python3 CODE/partition_dataset.py
python3 CODE/visualizations.py
```

O primeiro comando converte o CSV configurado para JSON e cria a versão
agrupada por ID. O segundo carrega o JSON agrupado e gera as figuras na pasta
`figures/`.

As dependências Python principais são `numpy`, `pandas`, `matplotlib` e
`seaborn`. O ambiente virtual local existente em `CODE/AIS_venv/` não faz
parte do código da aplicação.

## Estrutura principal

```text
CODE/
├── constants.py              # Configuração partilhada
├── partition_dataset.py      # Conversão e agrupamento dos dados
├── visualizations.py         # Análise exploratória e figuras
└── database/
    ├── full/                 # Dataset completo e derivados locais
    └── partial/              # Amostra parcial e derivados

figures/                      # Figuras geradas pelo pipeline
latex/                        # Proposta e documentos LaTeX
bibliografia/                 # Artigos e fontes bibliográficas
docs/                         # Revisões e notas sobre a proposta
```

## Verificação

Os módulos Python podem ser verificados sem executar o pipeline completo:

```bash
python3 -m compileall -q CODE/*.py
```

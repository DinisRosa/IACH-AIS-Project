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
um inspetor humano.

## Estado atual

### Implementado

- Conversão do dataset de CSV para JSON em
  [`partition_dataset.py`](partition_dataset.py);
- Agrupamento dos pontos por trajetória/ID;
- Centralização de caminhos, features, classes e parâmetros em
  [`constants.py`](constants.py);
- Análise exploratória e geração de figuras em
  [`visualizations.py`](visualizations.py);
- Análises de distribuição de classes, fragmentação, features por classe,
  outliers, gaps temporais, normalização e janelas sobrepostas;

### Ainda planeado

O classificador de janelas, os baselines HMM/Wu et al., o pós-processamento
temporal, a avaliação quantitativa e o dashboard de apoio à decisão humana
descritos na proposta ainda não fazem parte do pipeline implementado.

## Dados

O dataset utilizado é o
[Detailed Labelled Fishing Trajectories from AIS](https://www.kaggle.com/datasets/thedevastator/detailed-labelled-fishing-trajectories-from-ais),
obtido através do Kaggle.

O repositório contém:

- código para processar os datasets locais em `database/`, que não são
  versionados.

O CSV completo não é obtido automaticamente pelo projeto e pode não estar
versionado devido ao seu tamanho. Nesse caso, deve ser descarregado a partir
do Kaggle e colocado em:

```text
database/full/128_fishing_trajs.csv
```

Os caminhos atualmente utilizados pelo pipeline estão definidos em
[`constants.py`](constants.py). Para trabalhar com a amostra
parcial, alterar `ALL_TRAJS` para `False`.

## Como executar

A partir da raiz do projeto:

```bash
python3 partition_dataset.py
python3 visualizations.py
```

O primeiro comando converte o CSV configurado para JSON e cria a versão
agrupada por ID. O segundo carrega o JSON agrupado e gera as figuras na pasta
`figures/`. O bloco `if __name__ == "__main__":` de
`visualizations.py` usa diretamente o ID
`211477000-2`, uma janela de 50 pontos e uma sobreposição de 25 pontos; altere
esses valores diretamente nas chamadas das funções se necessário.
Também gera uma imagem com cinco subgráficos através de
`plot_multiple_trajectories(dataset, 5)`, comparando as trajetórias
`longitude/latitude` e `x/y` normalizadas para `0–1`.

Ao executar `partition_dataset.py`, além do JSON agrupado original, é
criado um segundo dataset com apenas as variáveis necessárias para o modelo:
`x`, `y` e as restantes features, mas sem `longitude` e `latitude`. O ficheiro
é guardado com o sufixo `_xy_ordered_by_id.json`.

As dependências Python principais são `numpy`, `pandas`, `matplotlib` e
`seaborn`. O ambiente virtual local existente em `AIS_venv/` não faz
parte do código da aplicação.

## Estrutura principal

```text
.
├── constants.py              # Configuração partilhada
├── partition_dataset.py      # Conversão e agrupamento dos dados
├── visualizations.py         # Análise exploratória e figuras
└── README.md                 # Instruções do código

database/                     # Dados locais, não versionados
figures/                      # Figuras geradas, não versionadas
```

## Verificação

Os módulos Python podem ser verificados sem executar o pipeline completo:

```bash
python3 -m compileall -q *.py
```

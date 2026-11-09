# IACH-AIS-Project

Código para análise de trajetórias AIS e deteção de atividade de pesca no
âmbito do projeto de Inteligência Artificial Centrada no Humano.

## Objetivo

O pipeline trabalha com trajetórias AIS e agrupa os pontos por ID. As classes
originais são agregadas em:

- **Navegação**: `01`, `03` e `05`;
- **Pesca**: `02` e `04`.

O código inclui análises exploratórias, comparação de coordenadas e
visualização de janelas sobrepostas.

## Estrutura do repositório

Esta pasta (`CODE/`) é a raiz do repositório GitHub e contém apenas o código e
as instruções de utilização:

```text
.
├── constants.py
├── 0_features_eng/
│   ├── divide_dataset.py
│   ├── tests_datasets.py
│   └── visualizations_pre_training.py
└── README.md
```

Os splits gerados ficam em `1_training/`, `2_testing/` e `3_validation/`, que
são locais e não versionados.
```

Os diretórios `database/`, `figures/` e `docs/` são locais e estão incluídos no
`.gitignore`. Não fazem parte do conteúdo versionado no GitHub.

## Dados

O dataset utilizado é o
[Detailed Labelled Fishing Trajectories from AIS](https://www.kaggle.com/datasets/thedevastator/detailed-labelled-fishing-trajectories-from-ais),
obtido através do Kaggle.

Os caminhos de entrada e saída estão definidos em
[`constants.py`](constants.py). Por predefinição, `ALL_TRAJS = True` e o
pipeline espera o dataset completo em:

```text
database/full/128_fishing_trajs.csv
```

Para usar a amostra parcial, altere `ALL_TRAJS` para `False`. Nesse caso, o
ficheiro esperado é:

```text
database/partial/small_fishing_trajs.csv
```

Os datasets e os ficheiros gerados são locais e não são enviados para o
GitHub.

## Instalação

As principais dependências Python são:

- `numpy`;
- `pandas`;
- `matplotlib`;
- `seaborn`.

Pode usar o ambiente virtual local `AIS_venv/`, que não é versionado.

## Processamento dos dados

A partir da raiz do repositório:

```bash
python3 CODE/0_features_eng/tests_datasets.py
```

O script executa três etapas:

1. converte o CSV configurado para JSON;
2. agrupa os pontos por trajetória/ID;
3. cria uma segunda versão do JSON sem as colunas redundantes
   (`longitude`, `latitude`, `t`, `bearing`, `distance_gap`).

O primeiro JSON mantém todas as colunas. O segundo contém as variáveis
necessárias para trabalhar apenas com `x` e `y`, mantendo também as restantes
features e labels. Os ficheiros gerados usam estes nomes:

```text
database/full/128_fishing_trajs_ordered_by_id.json
database/full/128_fishing_trajs_wo_redundant_features.json
```

Ou, quando `ALL_TRAJS = False`:

```text
database/partial/small_fishing_trajs_ordered_by_id.json
database/partial/small_fishing_trajs_wo_redundant_features.json
```

## Divisão em treino, teste e validação

```bash
python3 CODE/0_features_eng/divide_dataset.py
```

`divide_dataset(dataset_path, train_percentage, test_percentage,
validation_percentage, seed=RANDOM_SEED)` divide o dataset **por ID**: cada
trajetória vai inteira para um único split, nunca é partida por pontos. As
percentagens têm de ser inteiros, pelo menos 1 e somar 100; a contagem de IDs
segue o método do maior resto, para a soma ser sempre o total de IDs. A
repartição é reprodutível para a mesma `seed`.

Os ficheiros gerados são locais e não são versionados:

```text
1_training/train.json
2_testing/test.json
3_validation/validation.json
```

A função devolve os três caminhos por ordem (treino, teste, validação).

## Visualizações

Execute, a partir de qualquer diretório:

```bash
python3 CODE/0_features_eng/visualizations_pre_training.py
```

O script acrescenta `CODE/` e `CODE/0_features_eng/` ao `sys.path`, pelo que não
é necessário definir `PYTHONPATH` nem correr a partir de uma pasta específica.

As figuras são guardadas localmente em subpastas de `figures/`, na raiz do
projecto (pasta acima de `CODE/`), organizadas por fase e finalidade:

```text
figures/
└── 0_features_eng/
    ├── comparacao_features/
    ├── estatisticas/
    ├── sobreposicao/
    ├── velocidade/
    └── normalizacao/
```

Os parâmetros das
visualizações são definidos diretamente no bloco
`if __name__ == "__main__":`, sem parser de linha de comandos.

Atualmente, o script:

- usa a trajetória `"211477000-2"` no gráfico `speed versus turn`;
- desenha janelas de 50 pontos com 25 pontos de sobreposição;
- compara `longitude/latitude` com `x/y` normalizados em cinco subgráficos;
- gera análises de distribuição, segmentos, features, outliers, gaps
  temporais e normalização.

Para alterar a trajetória ou os parâmetros das janelas, edite diretamente as
chamadas no final de
[`visualizations_pre_training.py`](0_features_eng/visualizations_pre_training.py),
por exemplo:

```python
plot_speed_vs_turn_id(dataset, "211477000-2")
plot_overlapping_windows(dataset, "211477000-2", 50, 25)
plot_multiple_trajectories(dataset, 5)
```

## Verificação

Para verificar a sintaxe sem executar o pipeline completo:

```bash
python3 -m compileall -q constants.py 0_features_eng/*.py
```

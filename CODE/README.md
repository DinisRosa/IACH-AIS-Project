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
│   ├── csv_to_dataset.py
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

O processamento segue esta ordem:

```text
CSV validado -> JSON final agrupado por ID -> train/test/validation
```

### 1. Converter e validar o CSV

`0_features_eng/csv_to_dataset.py` lê o CSV configurado, valida todas as
linhas e só cria o JSON depois de o dataset completo passar as validações.
O JSON final é indexado pelo ID e mantém, para cada trajetória, apenas:

- `id`;
- `x`;
- `y`;
- `signed_turn`;
- `time_gap`;
- `euc_speed`;
- `distanceToShore`;
- `label`;

O `label` de origem é convertido para o label binário usado pelo pipeline:
`02-fishing` e `04-fishing` tornam-se `1`; `01-sailing`, `03-sailing` e
`05-sailing` tornam-se `0`. As colunas `longitude`, `latitude`, `t`, `bearing`
e `distance_gap` não são copiadas. A conversão pode ser executada a partir da
raiz de `CODE` com:

```bash
AIS_venv/bin/python -c \
  "from constants import INPUT_CSV_FILE_PATH, OUTPUT_JSON_FILE_PATH; \
from importlib.util import spec_from_file_location, module_from_spec; \
spec = spec_from_file_location('csv_to_dataset', '0_features_eng/csv_to_dataset.py'); \
module = module_from_spec(spec); spec.loader.exec_module(module); \
print(module.convert_csv_to_json(INPUT_CSV_FILE_PATH, OUTPUT_JSON_FILE_PATH))"
```

O caminho de entrada e o caminho do JSON final dependem de `ALL_TRAJS` em
`constants.py`:

```text
ALL_TRAJS = True:
  database/full/128_fishing_trajs.csv
  database/full/128_fishing_trajs_ordered_by_id.json

ALL_TRAJS = False:
  database/partial/small_fishing_trajs.csv
  database/partial/small_fishing_trajs_ordered_by_id.json
```

Se uma coluna obrigatória estiver ausente, se houver um ID vazio, um label de
origem fora das cinco classes conhecidas, ou um valor não numérico, a
conversão falha e não escreve um JSON parcial. Valores `NaN` e `inf` também
são erros explícitos: a mensagem inclui o ficheiro, a linha física do CSV
(com o cabeçalho como linha 1), o ID, a coluna e o valor inválido.

### 2. Dividir o JSON final em treino, teste e validação

```bash
AIS_venv/bin/python 0_features_eng/divide_dataset.py
```

Executar o comando a partir da raiz de `CODE` usa o JSON final configurado e
gera os três splits. A função `divide_dataset(dataset_path, train_percentage,
test_percentage,
validation_percentage, seed=RANDOM_SEED)` divide o dataset **por ID completo**:
cada trajetória vai inteira para um único split, nunca é partida por pontos.
Neste projeto, cada ID completo é uma unidade independente; IDs com o mesmo
prefixo não são agrupados. A execução direta do script gera 70/15/15. As
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

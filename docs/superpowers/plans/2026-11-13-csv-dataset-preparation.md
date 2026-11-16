# CSV Dataset Preparation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` skill to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar um fluxo robusto que converta diretamente o CSV original num JSON final agrupado por trajetória e depois gere os três splits por ID.

**Architecture:** Um novo módulo lê e valida o CSV com pandas, seleciona explicitamente as colunas necessárias e só escreve o JSON depois de todo o dataset passar as validações. `divide_dataset.py` continua responsável apenas por dividir esse JSON final em treino, teste e validação.

**Tech Stack:** Python 3.14, pandas, NumPy, JSON, pytest.

**Spec:** [2026-11-13-csv-dataset-preparation-design.md](../specs/2026-11-13-csv-dataset-preparation-design.md)

## Global Constraints

- Manter `id`, `label` e as features `x`, `y`, `signed_turn`, `time_gap`, `euc_speed` e `distanceToShore`.
- Excluir do JSON final as colunas `t`, `longitude`, `latitude`, `bearing` e `distance_gap`.
- Mapear `02-fishing`/`04-fishing` para 1 e `01-sailing`/`03-sailing`/`05-sailing` para 0.
- Rejeitar colunas ausentes, IDs vazios, labels inválidos, valores não numéricos, `NaN` e `inf`.
- Reportar a linha física do CSV, considerando o cabeçalho como linha 1.
- Não remover linhas inválidas silenciosamente.
- Não escrever JSON parcial quando o CSV falhar na validação.
- Manter temporariamente os scripts antigos para comparação e compatibilidade.
- Preservar a divisão por ID completo e a seed determinística de `divide_dataset.py`.

## Review Focus

- CSV sem uma coluna obrigatória: falhar antes de criar qualquer saída.
- Texto ou valor não convertível numa das seis features (`x`, `y`,
  `signed_turn`, `time_gap`, `euc_speed`, `distanceToShore`): indicar coluna e
  linha física; labels textuais fora das cinco classes conhecidas também
  falham.
- `NaN` ou `inf`: indicar ficheiro, linha, ID, coluna e valor.
- ID vazio ou label que não pertença às cinco classes de origem: indicar a
  linha física.
- CSV válido mas com zero linhas ou IDs repetidos: rejeitar com erro explícito.

---

### Task 1: Criar o conversor CSV para JSON final

**Files:**
- Create: `CODE/0_features_eng/csv_to_dataset.py`
- Modify: `CODE/constants.py` apenas se for necessário expor o caminho oficial do CSV final
- Test: `CODE/0_features_eng/test_csv_to_dataset.py`

**Interfaces:**
- Produces `convert_csv_to_json(csv_path: str | os.PathLike, output_path: str | os.PathLike) -> Path`.
- Produces `REQUIRED_COLUMNS`, `FEATURE_COLUMNS` e `OUTPUT_COLUMNS` como constantes reutilizáveis.
- O JSON produzido é um objeto indexado por ID; cada ID contém listas com
  `label` binário mapeado e as seis features `x`, `y`, `signed_turn`,
  `time_gap`, `euc_speed` e `distanceToShore`.

- [ ] **Step 1: Escrever testes falhando para o cabeçalho e a estrutura final**

Criar um CSV temporário com o cabeçalho real:
`id,t,longitude,latitude,x,y,signed_turn,bearing,time_gap,distance_gap,euc_speed,distanceToShore,label`.
Verificar que a conversão mantém exatamente `id`, `label` binário mapeado e as
seis features `x`, `y`, `signed_turn`, `time_gap`, `euc_speed` e
`distanceToShore`, agrupa várias linhas do mesmo ID e não inclui `longitude`,
`latitude`, `t`, `bearing` ou `distance_gap`.

- [ ] **Step 2: Executar os testes para confirmar a falha inicial**

Run:

```bash
cd CODE && AIS_venv/bin/python -m pytest 0_features_eng/test_csv_to_dataset.py -q
```

Expected: FAIL porque `csv_to_dataset.py` e `convert_csv_to_json` ainda não existem.

- [ ] **Step 3: Implementar `convert_csv_to_json`**

Usar `pandas.read_csv` para ler o CSV. Validar o cabeçalho, converter as seis
features numéricas, mapear os labels textuais para o label binário, agrupar por
`id` preservando a ordem das linhas e escrever o JSON apenas depois da
validação completa. Usar `json.dump(..., allow_nan=False)` para impedir
valores JSON não padrão.

- [ ] **Step 4: Testar as falhas de validação com linha física**

Adicionar testes para:

```python
def test_missing_required_column_fails_without_output(tmp_path): ...
def test_non_numeric_feature_reports_csv_line(tmp_path): ...
def test_non_finite_value_reports_line_id_column_and_value(tmp_path): ...
def test_invalid_label_reports_csv_line(tmp_path): ...
def test_empty_id_reports_csv_line(tmp_path): ...
def test_empty_dataset_fails_without_output(tmp_path): ...
```

As mensagens devem incluir a linha física do CSV, usando `DataFrame` indexado com `index + 2`, além do ID, coluna e valor quando disponíveis.

- [ ] **Step 5: Implementar erros explícitos e sem saída parcial**

Definir uma exceção de validação específica ou `ValueError` com mensagens
estáveis. Validar `id` não vazio, labels de origem pertencentes às cinco
classes conhecidas, features finitas e ausência de linhas inválidas antes de
criar o ficheiro de saída; escrever no JSON apenas o label binário mapeado.

- [ ] **Step 6: Executar os testes da tarefa**

Run:

```bash
cd CODE && AIS_venv/bin/python -m pytest 0_features_eng/test_csv_to_dataset.py -q
```

Expected: PASS.

- [ ] **Step 7: Testar contra o cabeçalho do CSV real sem carregar o dataset inteiro na saída**

Executar uma verificação que leia apenas o cabeçalho do CSV real e confirme as colunas esperadas:

```bash
cd CODE && AIS_venv/bin/python -c "import pandas as pd; from constants import INPUT_CSV_FILE_PATH; print(pd.read_csv(INPUT_CSV_FILE_PATH, nrows=0).columns.tolist())"
```

Expected: as colunas obrigatórias estão presentes.

- [ ] **Step 8: Commitar o conversor e os testes**

```bash
git add 0_features_eng/csv_to_dataset.py 0_features_eng/test_csv_to_dataset.py constants.py
git commit -m "feat: add validated CSV to JSON conversion"
```

### Task 2: Integrar o JSON final com a divisão dos splits

**Files:**
- Modify: `CODE/0_features_eng/divide_dataset.py`
- Modify: `CODE/0_features_eng/csv_to_dataset.py` apenas se for necessário expor um entry point de pipeline
- Test: `CODE/0_features_eng/test_divide_dataset.py`

**Interfaces:**
- Consumes o JSON agrupado produzido por `convert_csv_to_json`.
- Preserves `divide_dataset(dataset_path, train_percentage, test_percentage, validation_percentage, seed=RANDOM_SEED)`.
- Produces os caminhos de `train.json`, `test.json` e `validation.json` sem repartir pontos de uma trajetória.

- [ ] **Step 1: Escrever testes de integração**

Criar um JSON sintético no formato final e verificar que `divide_dataset` produz três ficheiros, que os IDs são disjuntos e que todos os pontos de cada ID permanecem juntos.

- [ ] **Step 2: Executar os testes existentes e novos**

Run:

```bash
cd CODE && AIS_venv/bin/python -m pytest 0_features_eng/test_divide_dataset.py -q
```

Expected: os testes existentes passam; qualquer incompatibilidade do formato final fica identificada.

- [ ] **Step 3: Ajustar apenas o necessário para consumir o JSON final**

Não duplicar validação do CSV em `divide_dataset.py`; manter a sua responsabilidade limitada à validação das percentagens, leitura do JSON final e divisão determinística por ID.

- [ ] **Step 4: Executar a integração completa com CSV sintético**

Testar o fluxo:

```text
CSV temporário -> convert_csv_to_json -> divide_dataset
```

Confirmar os ficheiros e a disjunção dos IDs.

- [ ] **Step 5: Commitar a integração**

```bash
git add 0_features_eng/divide_dataset.py 0_features_eng/test_divide_dataset.py
git commit -m "test: integrate final dataset with split generation"
```

### Task 3: Atualizar documentação e comando de execução

**Files:**
- Modify: `CODE/README.md`
- Modify: `docs/superpowers/plans/2026-11-13-pipeline-experimental-baseline.md`

**Interfaces:**
- Documenta o novo fluxo CSV → JSON final → splits.
- Regista que a validação de `NaN`/`inf` ocorre na preparação do dataset e inclui a linha física do CSV no erro.

- [ ] **Step 1: Atualizar o README**

Documentar o módulo novo, o comando de conversão, os caminhos de entrada/saída e a política de falha para dados inválidos.

- [ ] **Step 2: Corrigir a Task 1 do plano experimental**

Remover a obrigação de repetir no carregador do pipeline a validação profunda do CSV. Manter no carregador apenas as validações mínimas necessárias para transformar o JSON final em `Trajectory`.

- [ ] **Step 3: Executar a suíte focada**

```bash
cd CODE && AIS_venv/bin/python -m pytest 0_features_eng/test_csv_to_dataset.py 0_features_eng/test_divide_dataset.py -q
```

Expected: PASS.

- [ ] **Step 4: Commitar documentação**

```bash
git add README.md ../docs/superpowers/plans/2026-11-13-pipeline-experimental-baseline.md
git commit -m "docs: describe validated dataset preparation flow"
```

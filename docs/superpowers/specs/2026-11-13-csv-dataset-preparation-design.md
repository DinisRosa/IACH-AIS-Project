# Design: preparação robusta do dataset a partir do CSV

## Intenção

Criar um fluxo oficial que leia diretamente o CSV original do Kaggle, valide a
estrutura e os valores, e produza um JSON final agrupado por trajetória. O
objetivo é eliminar a dependência dos JSONs intermédios sem remover
silenciosamente dados inválidos.

## Objetivos

- Ler o CSV com pandas.
- Validar as colunas obrigatórias antes do processamento.
- Manter todas as colunas que não pertencem ao conjunto excluído:
  `id`, `x`, `y`, `signed_turn`, `time_gap`, `euc_speed`, `distanceToShore` e o
  `label` binário mapeado.
- Excluir do JSON final `longitude`, `latitude`, `t`, `bearing` e
  `distance_gap`.
- Mapear as classes textuais `02-fishing` e `04-fishing` para 1, e
  `01-sailing`, `03-sailing` e `05-sailing` para 0.
- Rejeitar `NaN` e `inf` com uma mensagem que indique o ficheiro, a linha física
  do CSV, o ID, a coluna e o valor inválido.
- Validar IDs e labels antes de escrever qualquer JSON.
- Manter `divide_dataset.py` como responsável apenas por dividir o JSON final por
  ID completo.

## Não objetivos

- Não alterar nesta fase a lógica de divisão 70/15/15.
- Não remover silenciosamente linhas inválidas.
- Não apagar imediatamente os scripts antigos de preparação; ficam disponíveis
  para comparação e compatibilidade temporária.
- Não incluir as colunas de localização, timestamp, bearing ou distance gap no
  JSON usado pelo pipeline; `time_gap` é mantido.

## Abordagens consideradas

### A — Validação linha a linha com `csv`

Daria mensagens de erro muito diretas e consumiria pouca memória, mas duplicaria
parte da conversão numérica que pandas já fornece.

### B — Leitura e validação com pandas (escolhida)

O CSV é carregado com pandas, as colunas são convertidas para tipos numéricos e
os índices dos valores inválidos são convertidos para números de linha física
(`índice do DataFrame + 2`, devido ao cabeçalho). Esta abordagem integra melhor
com o processamento tabular existente e mantém mensagens precisas.

### C — Divisão direta durante a leitura

Misturaria preparação, validação e divisão dos dados, dificultando testes,
reutilização e diagnóstico.

## Decisões de implementação

- Criar um novo módulo em `CODE/0_features_eng/` para CSV → JSON final.
- Derivar a seleção a partir de
  `columns_to_remove = {'longitude', 'latitude', 't', 'bearing',
  'distance_gap'}`, mantendo `id`, as seis features usadas pelo pipeline e o
  label binário mapeado.
- Converter as seis features com pandas antes de validar finitude e mapear o
  label textual para a classe binária.
- Falhar antes da escrita se houver coluna ausente, ID vazio, label inválido,
  valor não numérico ou valor não finito.
- A linha reportada será a linha física do ficheiro CSV, com o cabeçalho como
  linha 1.
- Escrever trajetórias agrupadas por ID apenas após o CSV completo passar todas
  as validações.
- Fazer `divide_dataset.py` consumir esse JSON final.

## Resultado esperado

```text
CSV Kaggle
  -> validação pandas
  -> JSON final agrupado por ID
  -> divide_dataset.py
  -> train.json, test.json, validation.json
```

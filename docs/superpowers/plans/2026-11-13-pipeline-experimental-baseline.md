# Pipeline Experimental e Baseline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` skill to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar um pipeline reprodutível que transforma os splits por ID completo em janelas, avalia previsões temporais e fornece um baseline simples para comparação com modelos posteriores.

**Architecture:** Manter os JSON atuais como fonte, com cada ID completo tratado como trajetória independente. Adicionar módulos pequenos para carregar/validar dados, ajustar a normalização apenas com treino, gerar janelas e reconstruir probabilidades por ponto; um baseline clássico treina nos mesmos dados e produz resultados persistidos e métricas. O pipeline fica preparado para sobreposição e pós-processamento posteriores, sem implementar ainda uma rede profunda, HMM, dashboard ou ablações completas.

**Tech Stack:** Python 3.14 no ambiente `AIS_venv`, NumPy, pandas, scikit-learn, pytest e JSON/CSV para resultados.

**Spec:** A proposta em `latex/proposta_pt.tex`, em especial as secções de Abordagem, Dados e Avaliação; decisão do projeto: split por ID completo a 70/15/15.

## Global Constraints

- Cada ID completo representa uma trajetória independente e deve permanecer inteiro num único split.
- Usar `1_training/train.json`, `2_testing/test.json` e `3_validation/validation.json`; não voltar a repartir pontos.
- Ajustar parâmetros de normalização apenas com dados de treino e aplicá-los sem reajuste a validação e teste.
- Uma janela nunca pode atravessar trajetórias; preservar o alinhamento entre pontos e labels.
- Fixar e registar sementes aleatórias para operações estocásticas.
- O teste final só pode ser usado para avaliação, não para seleção de modelo ou limiar.

## Review Focus

- Trajetórias curtas, vazias ou cujo comprimento não seja múltiplo do passo: não perder pontos nem criar janelas incompletas silenciosamente.
- Features constantes, valores não finitos ou campos ausentes: normalização e validação devem falhar com erro legível ou tratamento explícito.
- Classes desequilibradas e trajetórias contendo ambas as classes: métricas devem incluir suporte por classe e não esconder a classe minoritária.
- Fronteiras de janela: cada ponto deve receber uma única previsão reconstruída segundo regra documentada, sem mistura de IDs.
- Desequilíbrio entre trajetória e número de pontos: explicitar se o baseline otimiza por ponto ou por janela e reportar os dois níveis de suporte.

## Ficheiros e responsabilidades

- Criar `CODE/1_training/pipeline/data.py`: ler splits, validar campos, converter features/labels e normalizar com estado ajustado em treino.
- Criar `CODE/1_training/pipeline/windows.py`: gerar janelas por trajetória e reconstruir previsões de janela para pontos.
- Criar `CODE/1_training/pipeline/metrics.py`: métricas binárias por ponto e por segmento, com suporte e fronteiras.
- Criar `CODE/1_training/pipeline/baseline.py`: baseline scikit-learn, treino, validação, seleção e avaliação final.
- Criar `CODE/1_training/pipeline/run_experiment.py`: orquestrar execução e gravar configurações, métricas e previsões.
- Criar `CODE/1_training/tests/`: testes unitários com datasets sintéticos pequenos.
- Modificar `CODE/README.md`: instalação, execução, outputs e limites da experiência.

---

### Task 1: Definir esquema de entrada e carregamento dos splits

**Interfaces:**
- Produz `load_splits(train_path, validation_path, test_path) -> dict[str, dict[str, Trajectory]]`.
- Cada `Trajectory` contém `features: np.ndarray` com forma `(N, F)`, `labels: np.ndarray` binário com forma `(N,)` e `feature_names: tuple[str, ...]`.
- Mapear `02-fishing` e `04-fishing` para 1; `01-sailing`, `03-sailing` e `05-sailing` para 0.

- [ ] Escrever testes para labels conhecidos, alinhamento de comprimentos, IDs não duplicados entre splits e chaves/colunas ausentes.
- [ ] Executar `cd CODE && AIS_venv/bin/python -m pytest 1_training/tests/test_data.py -q`; confirmar falha inicial.
- [ ] Implementar `Trajectory` e `load_splits` em `data.py`, consumindo o JSON final produzido pela preparação validada do CSV. O carregador não repete a validação profunda do CSV; verifica apenas o esquema mínimo do JSON final, IDs não duplicados entre splits, alinhamento dos comprimentos, labels binários e features numéricas finitas antes de construir cada `Trajectory`.
- [ ] Reexecutar o teste e confirmar sucesso.

### Task 2: Ajustar e aplicar normalização sem fuga de informação

**Interfaces:**
- `fit_normalizer(train: Mapping[str, Trajectory]) -> NormalizerState` calcula média e desvio por feature sobre pontos de treino.
- `transform_trajectories(data, state) -> dict[str, Trajectory]` aplica a mesma transformação sem alterar labels nem ordem.

- [ ] Testar que os parâmetros coincidem apenas com treino, dados de validação/teste não os alteram, e feature de variância zero produz saída finita.
- [ ] Implementar estado serializável com nomes, médias e desvios; substituir desvio zero por 1 apenas para a divisão.
- [ ] Confirmar que `transform` preserva formas, labels e ordem temporal.

### Task 3: Gerar janelas e reconstruir previsões por ponto

**Interfaces:**
- `make_windows(trajectories, window_length, overlap) -> WindowBatch`; overlap é proporção em `[0, 1)` e janelas só são completas.
- `aggregate_window_predictions(window_predictions, window_batch) -> dict[str, np.ndarray]` projeta probabilidades para os pontos cobertos, calculando a média nos pontos em sobreposição.

- [ ] Testar limites da trajetória, ausência de cruzamento entre IDs, overlap zero e positivo, trajetórias curtas e cobertura dos pontos elegíveis.
- [ ] Tornar explícita a política de cauda: incluir uma última janela completa alinhada ao fim quando o passo não cobrir os últimos pontos; erro se a trajetória for menor que a janela.
- [ ] Implementar as duas funções e verificar que probabilidades reconstruídas ficam em `[0,1]` e têm alinhamento determinístico.

### Task 4: Implementar métricas por ponto e por segmento

**Interfaces:**
- `evaluate_point_predictions(y_true, y_prob, threshold=0.5) -> dict[str, float | int]` devolve precisão, sensibilidade, F1, IoU, matriz de confusão e suporte por classe.
- `evaluate_segments(y_true, y_pred) -> dict[str, float | int]` devolve contagem de segmentos previsto/referência e erro absoluto médio das fronteiras sob correspondência ordenada por classe.

- [ ] Testar sequência perfeita, sem positivos previstos, classe ausente, transições coincidentes e deslocadas.
- [ ] Implementar métricas com convenção definida para divisões por zero e resultado serializável em JSON.
- [ ] Confirmar que a avaliação agrega primeiro por trajetória e depois reporta média e desvio entre trajetórias, além das métricas micro por ponto.

### Task 5: Treinar e selecionar baseline clássico

**Decisão inicial:** classificador `RandomForestClassifier` da scikit-learn; features de cada janela são média, desvio padrão, mínimo e máximo por feature, concatenados. Treino usa janelas de trajetórias de treino; escolha do limiar usa apenas validação.

- [ ] Testar extração determinística de atributos de janela e mapeamento da label de janela por maioria; empate é resolvido como navegação (0).
- [ ] Implementar treino com `random_state=RANDOM_SEED`, pesos `balanced` e probabilidades para classe pesca.
- [ ] Comparar limiares candidatos `0.1, 0.2, ..., 0.9` na validação, selecionando maior F1 macro; empate escolhe o limiar mais próximo de 0.5.
- [ ] Testar que dados de teste não entram no treino nem na escolha do limiar.

### Task 6: Executar experiência e guardar artefactos

- [ ] Orquestrar carregamento, normalização, janelamento, treino, seleção de limiar e avaliação final no teste.
- [ ] Gravar em `CODE/4_results/<run_id>/`: `config.json`, `normalizer.json`, `metrics.json`, `predictions.json` e versão/dependências usadas.
- [ ] Incluir seed, features, tamanho/overlap da janela, política de agregação, limiar escolhido e hashes/caminhos dos splits na configuração.
- [ ] Testar execução end-to-end com dados sintéticos; confirmar repetibilidade dos resultados para a mesma seed.

### Task 7: Documentar execução e limitações

- [ ] Atualizar README com dependências, comando de execução, semântica das métricas e localização dos resultados.
- [ ] Documentar que o baseline é referência inicial, a seleção ocorre em validação e o teste é usado uma única vez para estimativa final.
- [ ] Executar a bateria completa: `cd CODE && AIS_venv/bin/python -m pytest 1_training/tests -q` e o experimento sobre os splits locais; registar os resultados observados.

## Critério de conclusão

O caminho 1 está implementado quando o comando documentado executa de ponta a ponta, gera métricas e previsões reproduzíveis, mantém IDs separados e não usa estatísticas de validação/teste no ajuste do preprocessamento nem o teste na seleção do modelo.

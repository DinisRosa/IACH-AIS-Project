# Revisão da proposta e das referências

**Ficheiros analisados:** `proposta_pt.tex` e `references.bib`
**Tema:** Segmentação semântica de trajetórias AIS para deteção de atividade de pesca

No geral, a proposta está bem estruturada e o raciocínio é claro: problema, lacuna, objetivos, abordagem e avaliação encaixam uns nos outros. Os problemas estão na fundamentação de algumas afirmações, em pormenores metodológicos e em algumas referências.

---

## 1. Proposta

### O que está bem

- A cadeia problema → lacuna → objetivos → avaliação é coerente, e os critérios de sucesso são concretos.
- A variante sem pós-processamento serve para isolar o contributo de cada componente.
- Validar por trajetória em vez de por ponto é a decisão certa.
- A secção de ética tem conteúdo real (decisão humana obrigatória, enviesamento, confiança calibrada).

### Afirmações sem suporte (o ponto mais importante)

- Na secção 1 dizes que os modelos atuais "produzem segmentações ruidosas", e na secção 2 que as janelas sobrepostas com pós-processamento são uma via "ainda pouco explorada" e que "a maioria dos trabalhos avalia apenas o desempenho preditivo". Nenhuma tem citação, e a lacuna é a base da contribuição. **✔ tratado nesta ronda** (suavizado/qualificado, sem citações novas).
- Confirma que o Wu et al. (2022), a referência central, não faz já algo equivalente. Se fizer, a novidade enfraquece, e convém dizer explicitamente o que acrescentas. **⚠️ parcialmente tratado nesta ronda** (novidade clarificada explicitamente; verificação do conteúdo de Wu et al. ainda em aberto).
- O "até cerca de 20%" da pesca IUU está citado a Chuaysi & Kiattisin, que é uma fonte secundária. O valor vem normalmente de Agnew et al. (2009), que deve ser citado diretamente. **✔ tratado nesta ronda** (Agnew et al. 2009 citado diretamente como fonte primária; `chuaysi2020` mantido como apoio).

### Questões metodológicas

- **Fuga de dados.** Se o mesmo navio aparecer em várias trajetórias, dividir por trajetória não chega. Usar uma divisão agrupada por navio. Além disso, "fuga temporal" não descreve bem o problema: o risco aqui é fuga entre janelas sobrepostas da mesma trajetória.
- **Limitação do dataset.** Todas as 128 trajetórias já contêm pesca, por isso não se medem falsos positivos em navios que nunca pescam, que é o cenário real de fiscalização. Deve ser assumido como limitação.
- **Estabilidade.** O sucesso inclui "segmentações temporalmente estáveis", mas as métricas (P, R, F1, IoU) não a medem. Acrescentar, por exemplo, número de segmentos por trajetória (fragmentação) e erro de fronteira com tolerância.
- **Ablação.** Para isolar o efeito da sobreposição, é preciso também uma variante com janelas sem sobreposição, não só sem pós-processamento.
- **Calibração.** Prometes "confiança calibrada", mas não há nenhuma métrica de calibração na avaliação (ECE, Brier, diagrama de fiabilidade).
- **Explicabilidade.** "Importâncias de características" é vago para um modelo LSTM/CNN. Indicar o método (SHAP, integrated gradients, atenção).
- **Componente HCAI.** É um dos pilares do projeto, mas a avaliação é "preliminar" e as referências não incluem nada de HCAI, explicabilidade ou calibração. É a maior fragilidade face ao posicionamento defendido.
- **Inconsistência.** Na abordagem diz-se que a distância à costa é calculada, mas o dataset já traz `distanceToShore` (e também velocidade, rumo e intervalos).
- **Baselines.** Reimplementar o Wu et al. pode dar muito trabalho. Se não houver código público, referir esse risco.

### Escrita e estilo

- "dentro do ambiente virtual já criado no repositório" e "o CSV é carregado" são informais para um artigo. Cortar. **✔ tratado nesta ronda**
- "PyTorch (ou TensorFlow)" soa a indecisão. Escolher um. **✔ tratado nesta ronda** (PyTorch)
- Usar português europeu de forma consistente: "confiável" → "fiável", e "revocação" é muito brasileiro (usar "sensibilidade" ou manter *recall*). **✔ tratado nesta ronda** ("fiável"; "sensibilidade (recall)")
- Pôr *baselines* em itálico em todo o texto, como já é feito com *pipeline*. **✔ tratado nesta ronda**
- O resumo não menciona dados, baselines nem avaliação. Uma frase com isso ajuda. **✔ tratado nesta ronda**
- Sem `babel` em português, os títulos automáticos (Abstract, References) e a hifenização ficam em inglês. Pode manter-se por exigência do template, mas deve ser uma decisão consciente. **✔ tratado nesta ronda** (decisão registada: mantém-se sem babel)
- Algumas frases são muito longas, sobretudo na secção 2, e o parágrafo final de referências ("Outras contribuições relevantes incluem…") é uma lista de citações sem síntese. **✔ tratado nesta ronda**

---

## 2. Referências (`references.bib`)

### Estrutura e formatação: está boa

As chaves são consistentes (autor+ano), os acrónimos estão protegidos com chavetas, os acentos estão escapados corretamente, os tipos de entrada são adequados e todas as chaves citadas existem e são usadas. Quase todas têm DOI.

### Problemas a corrigir

- **Citação desajustada.** No texto, `guillot2018` e `ghazizadeh2019` aparecem como "comparações sistemáticas de métodos sobre VMS". Mas o título da tese de Ghazizadeh é sobre classificação de imagens a partir de dados **AIS**. Ajustar a frase ou trocar a referência.
- **Literatura cinzenta fraca.**
  - `guillot2018` ("Working paper") não tem instituição, URL nem identificador, e não foi possível confirmar a partir do ficheiro que seja encontrável.
  - `ghazizadeh2019` é uma tese de mestrado sem URL.
  - Verificar se existem e são acessíveis, acrescentar `url`/`institution`, ou substituir por artigos revistos por pares.
- **Campos em falta.**
  - `wang2026`, `luo2023` e `xing2023` não têm DOI. Os DOI da MDPI seguem um padrão previsível (por exemplo 10.3390/jmse11091646 para o Luo), mas confirmar cada um.
  - `soares2018` e `arasteh2020` não têm páginas.
  - `cheng2025` não tem o número de artigo.
- **Referências em falta.**
  - O dataset do Kaggle não está citado (convém indicar a origem, a região e a licença).
  - Falta a fonte primária da estatística IUU.
  - Faltam referências para HCAI, explicabilidade e calibração (por exemplo Shneiderman sobre HCAI, SHAP, Guo et al. sobre calibração).
- **Verificação.** Foi avaliada a estrutura e a consistência das entradas, mas não foi confirmado online se cada referência existe com os dados indicados. Antes de submeter, vale a pena fazer essa verificação, sobretudo nas de 2026 e nas não indexadas.

---

## 3. Lista de ações (resumo)

| Prioridade | Ação |
|---|---|
| Alta | Confirmar que o Wu et al. (2022) não faz já janelas sobrepostas + pós-processamento; clarificar a novidade |
| Alta | Fundamentar com citações as afirmações sobre "segmentações ruidosas", "pouco explorada" e "só desempenho preditivo" |
| Alta | Reforçar a componente HCAI: referências e método de avaliação concreto |
| Alta | Divisão treino/teste agrupada por navio; assumir a limitação de só haver trajetórias com pesca |
| Média | Adicionar métricas de estabilidade e de calibração; variante sem sobreposição na ablação |
| Média | Especificar o método de explicabilidade; resolver a inconsistência de `distanceToShore` |
| Média | Corrigir a citação de `guillot2018` / `ghazizadeh2019`; citar o dataset e a fonte IUU primária |
| Baixa | Completar DOI, páginas e número de artigo; limpar o estilo e o português europeu |

---

## Já tratado (ronda 1) — 2026-10-07

Foram tratadas as secções **"Afirmações sem suporte"** e **"Escrita e estilo"**:

- **Afirmações sem suporte** — as três afirmações sem citação foram suavizadas/qualificadas (sem novas citações, por decisão do autor); a novidade face a Wu et al. (2022) foi clarificada explicitamente; a estatística IUU passou a citar Agnew et al. (2009) como fonte primária (`agnew2009` adicionado a `references.bib`, mantendo `chuaysi2020` como apoio).
- **Escrita e estilo** — removidas expressões informais; escolhido PyTorch; português europeu ("fiável", "sensibilidade (recall)"); *baselines* em itálico; resumo com dados, baselines e avaliação; registada a decisão de manter sem `babel`; frases longas divididas e parágrafo final de referências sintetizado.

**Em aberto (não tratado nesta ronda):** verificação factual do conteúdo de Wu et al. (2022) (se fazem ou não janelas sobrepostas + pós-processamento); secções "Questões metodológicas" e "Referências" do documento.

O documento LaTeX compila sem erros e com todas as referências resolvidas.

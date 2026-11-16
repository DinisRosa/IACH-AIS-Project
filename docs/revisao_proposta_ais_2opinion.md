# Revisão crítica da proposta — Segmentação semântica de trajetórias AIS

## 1. Síntese da avaliação

**Avaliação global: a proposta está bem encaminhada e tem uma estrutura bastante sólida, mas ainda não está totalmente “fechada” como proposta científica.**

A ideia central é clara:

> usar janelas sobrepostas sobre trajetórias AIS, classificar atividade de pesca/navegação e aplicar pós-processamento temporal para obter segmentos mais estáveis e interpretáveis, mantendo o humano no circuito de decisão.

A proposta tem uma boa sequência lógica:

**problema → contexto → lacuna → objetivos → abordagem → dados → avaliação**

Isto é provavelmente o seu maior ponto forte.

O principal problema não é a organização geral, mas sim o facto de algumas afirmações e objetivos serem **mais ambiciosos do que aquilo que a metodologia realmente operacionaliza**. Em particular:

1. “segmentação semântica” aparece como o problema, mas a abordagem é descrita sobretudo como **classificação de janelas seguida de agregação/pós-processamento**;
2. a componente **HCAI/human-in-the-loop** é bem justificada conceptualmente, mas ainda é pouco avaliada experimentalmente;
3. a novidade científica de “janelas sobrepostas + pós-processamento temporal” precisa de ser formulada de forma mais precisa e demonstrada através de **ablation studies**;
4. os baselines não estão ainda suficientemente especificados para garantir uma comparação justa;
5. faltam referências explícitas para alguns elementos importantes, sobretudo **HCAI**, o próprio **dataset** e, idealmente, técnicas específicas de explicabilidade/calibração;
6. alguns detalhes metodológicos fundamentais ainda estão em aberto (“por exemplo”, “tipicamente”, “como amostragem ou ponderação”), o que faz a proposta parecer parcialmente exploratória.

Em resumo: **a proposta está estruturalmente bem construída, mas precisa de transformar uma boa ideia de projeto numa pergunta científica mais falsificável e numa metodologia mais determinada.**

---

# 2. O que está muito bem feito

## 2.1. A narrativa global é coerente

A proposta apresenta uma progressão natural:

1. apresenta o problema da pesca IUU;
2. explica porque é que AIS é relevante;
3. introduz o problema técnico de identificar atividade de pesca;
4. apresenta trabalhos anteriores;
5. identifica duas lacunas;
6. propõe uma solução;
7. define objetivos;
8. apresenta o pipeline;
9. especifica dados e ferramentas;
10. define uma avaliação.

Esta organização é boa porque o leitor consegue perceber **por que razão o projeto existe** antes de saber como vai ser implementado.

A passagem de:

> problema de fiscalização → dificuldade de trabalhar com trajetórias AIS → ruído/fronteiras instáveis → necessidade de contexto temporal → janelas sobrepostas + pós-processamento

é particularmente convincente.

---

## 2.2. O problema está suficientemente concreto

A formulação:

> “classificar automaticamente, ao longo de uma trajetória AIS, os intervalos temporais correspondentes a atividade de pesca versus navegação”

é uma boa forma de tornar o problema operacional.

Não se fica apenas por “detetar pesca com IA”; existe uma unidade de análise temporal e uma distinção explícita entre pesca e navegação.

Isto é importante para uma proposta académica.

---

## 2.3. A escolha de segmentação semântica é interessante

A ligação à segmentação semântica de trajetórias é uma boa escolha conceptual.

A proposta não trata simplesmente cada ponto AIS como uma observação independente. A intenção é produzir **segmentos temporalmente coerentes**, o que é mais adequado ao domínio.

A referência a Wu et al. como trabalho central também ajuda a posicionar o projeto.

---

## 2.4. A lacuna científica está relativamente bem identificada

A proposta identifica duas dimensões:

### Lacuna 1 — Robustez temporal

As previsões podem ser ruidosas e as fronteiras entre segmentos podem ser instáveis.

A proposta responde com:

- janelas sobrepostas;
- agregação das previsões;
- pós-processamento temporal;
- avaliação da estabilidade.

### Lacuna 2 — Dimensão humana

O sistema não deve simplesmente produzir uma classificação automática, mas apoiar a decisão de um inspetor.

Esta combinação é interessante porque dá ao projeto uma componente algorítmica e uma componente de interação/fiabilidade.

---

## 2.5. Os objetivos estão relativamente bem alinhados com a abordagem

Os cinco objetivos específicos acompanham bem o pipeline:

| Objetivo | Correspondência |
|---|---|
| Pré-processamento | Etapa 1 |
| Modelo de classificação | Etapa 3 |
| Pós-processamento | Etapa 4 |
| Avaliação | Secção de avaliação |
| Explicabilidade | Etapa 5 |

Isto é uma boa característica da proposta.

Não existem, por exemplo, objetivos completamente desligados da metodologia.

---

## 2.6. Existe uma tentativa muito boa de isolar as contribuições

Um dos melhores aspetos é a inclusão de:

> “uma variante sem pós-processamento, de modo a isolar a contribuição das janelas sobrepostas e do pós-processamento.”

Isto aponta na direção certa.

Uma proposta experimentalmente forte não deve apenas mostrar:

> “o meu método obtém F1 = X”.

Deve tentar responder:

> “qual é exatamente o valor acrescentado de cada componente?”

A proposta já começa a fazer isso.

---

## 2.7. A validação por trajetória é uma boa decisão

A afirmação:

> “A validação será feita por trajetória (e não por ponto), para evitar fuga temporal entre treino e teste.”

é importante e demonstra consciência de um problema metodológico real.

Se pontos da mesma trajetória fossem distribuídos aleatoriamente entre treino e teste, o modelo poderia beneficiar de informação extremamente semelhante nos dois conjuntos, produzindo resultados artificialmente otimistas.

A intenção de fazer a separação por trajetória é, portanto, um ponto forte.

---

## 2.8. A componente ética está melhor do que o habitual numa proposta deste género

A proposta não trata a IA como autoridade final.

É particularmente positivo afirmar que:

> “a deteção automática não deve, por si só, fundamentar sanções”

e que a decisão final deve permanecer humana.

Também é interessante mencionar:

- confiança calibrada;
- risco de falsa segurança;
- enviesamentos;
- auditabilidade.

Isto combina bem com a ideia de apoio à decisão.

---

# 3. O que está menos bem / principais problemas

## 3.1. O maior problema: segmentação semântica vs. classificação de janelas

Este é, na minha opinião, o ponto que mais vale a pena corrigir.

O título e a motivação apresentam o trabalho como:

> **segmentação semântica de trajetórias AIS**

Mas a metodologia diz essencialmente:

> dividir a trajetória em janelas → classificar cada janela como pesca/navegação → combinar previsões → suavizar → obter segmentos.

Isto pode perfeitamente ser uma forma de implementar segmentação semântica, mas a proposta **não explica formalmente essa ligação**.

### Porque é que isto é importante?

Um avaliador pode perguntar:

> “Estão a fazer semantic segmentation ou simplesmente window classification?”

E a proposta, neste momento, não responde de forma suficientemente explícita.

### Como melhorar

Definir formalmente:

- entrada: trajetória `T = {p1, ..., pN}`;
- cada ponto `pi` possui características;
- as janelas `W1, ..., WK` são extraídas com determinado comprimento e overlap;
- o modelo produz uma probabilidade `P(fishing | Wk)` ou, idealmente, previsões por ponto;
- as previsões das janelas sobrepostas são projetadas novamente para os pontos originais;
- uma função de agregação transforma as várias previsões de cada ponto numa previsão final;
- o pós-processamento transforma a sequência de labels numa sequência de segmentos.

Ou seja:

**trajectory → overlapping windows → window predictions → point-level reconstruction → temporal regularization → semantic segments**

Se isto for explicitado, o conceito de segmentação fica muito mais sólido.

---

# 4. A novidade científica precisa de ser mais bem definida

A frase:

> “janelas sobrepostas com pós-processamento temporal”

é interessante, mas ainda não constitui, por si só, uma contribuição científica suficientemente específica.

Um avaliador pode perguntar:

> “Porque é que isto é novo?”

ou:

> “Qual é exatamente o algoritmo proposto?”

Neste momento aparecem várias alternativas:

- “por exemplo”;
- “tipicamente”;
- LSTM ou CNN 1D;
- votação ponderada;
- HMM ou votação por vizinhança;
- importância de características ou confiança calibrada.

Isso faz a metodologia parecer ainda aberta.

### Como melhorar

Definir uma hipótese principal.

Por exemplo:

> **H1:** a utilização de janelas sobrepostas reduz a instabilidade das fronteiras de segmentação relativamente a janelas não sobrepostas.

> **H2:** o pós-processamento temporal reduz fragmentação e melhora IoU/F1 ao nível dos segmentos.

> **H3:** a combinação de sobreposição e pós-processamento produz segmentos mais estáveis sem degradar significativamente a deteção de atividade de pesca.

A partir daqui, o projeto deixa de ser apenas “vamos experimentar X” e passa a ser:

> “vamos testar estas hipóteses.”

Isso melhora bastante a qualidade científica.

---

# 5. O papel das janelas sobrepostas precisa de ser isolado

Atualmente existe uma pequena ambiguidade.

A proposta diz que as janelas sobrepostas:

> “dão contexto local a cada ponto e mitigam os efeitos de fronteira.”

Depois o pós-processamento:

> “garante consistência e estabilidade.”

São duas ideias diferentes e deveriam ser separadas experimentalmente.

## Sugestão de ablation study

Ter pelo menos:

| Variante | Overlap | Pós-processamento |
|---|---:|---:|
| A | Não | Não |
| B | Sim | Não |
| C | Não | Sim |
| D — proposta | Sim | Sim |

Isto permitiria responder claramente:

- o overlap ajuda?
- o pós-processamento ajuda?
- os dois juntos têm efeito adicional?
- existe interação entre ambos?

Este desenho experimental seria uma das melhorias mais importantes que eu faria.

---

# 6. O modelo está demasiado indefinido

Na secção de abordagem aparece:

> “tipicamente uma arquitetura recorrente (LSTM) ou convolucional 1D com atenção”

Isto é demasiado aberto para uma proposta que pretende ser avaliada.

Não é necessário definir cada hiperparâmetro, mas convém escolher uma arquitetura principal.

Por exemplo:

> “O modelo principal será uma LSTM bidirecional com mecanismo de atenção.”

E depois:

> “Como análise de robustez, será considerada uma CNN 1D.”

Ou o inverso.

Neste momento, “LSTM ou CNN” pode transmitir a ideia de que o método ainda não está decidido.

---

# 7. Os baselines precisam de maior cuidado

Os baselines propostos são:

- HMM;
- Wu et al.

Isto é bom como ponto de partida, mas a comparação pode não ser completamente justa.

## HMM

A referência de Peel & Good trabalha com VMS, enquanto a proposta utiliza AIS.

Isto não invalida o baseline, mas exige que se explique como o HMM será adaptado aos dados AIS.

## Wu et al.

É uma referência muito mais próxima e provavelmente deve ser o baseline principal.

Seria importante especificar:

- que parte do método de Wu et al. será reproduzida;
- se será usado o mesmo protocolo;
- se os dados são compatíveis;
- que diferenças existem entre o dataset original e o dataset usado no projeto.

Sem isso, “comparar com Wu et al.” pode parecer mais simples do que realmente é.

---

# 8. O dataset devia ter uma referência explícita

A proposta afirma:

> “Detailed Labelled Fishing Trajectories from AIS (Kaggle)”

e fornece números bastante específicos:

- 128 trajetórias;
- cerca de 1,03 milhões de pontos;
- 13 atributos;
- cinco classes.

Mas a bibliografia não contém uma entrada para o dataset.

Isto é uma falha relativamente pequena, mas fácil de corrigir.

### Sugestão

Adicionar uma referência bibliográfica ao dataset, se existir uma página oficial/dataset paper.

Além disso, seria útil indicar:

- URL ou identificador do dataset;
- versão/data de acesso;
- licença, se relevante;
- como as 128 trajetórias são divididas.

---

# 9. A parte HCAI é interessante, mas ainda está subdesenvolvida

A proposta afirma que o projeto integra:

> “Inteligência Artificial Centrada no Humano (HCAI)”

e fala de:

- cooperação humano-IA;
- confiança;
- responsabilidade;
- explicabilidade;
- decisão humana.

O problema é que isto ainda aparece sobretudo como **motivação**, e não como metodologia experimental.

Por exemplo:

> “avaliar-se-á a explicabilidade das deteções”

mas não está definido:

- como?
- com que métricas?
- por quem?
- segundo que critérios?
- haverá utilizadores humanos?
- será avaliada compreensão?
- será avaliada calibração da confiança?
- haverá comparação entre explicações?

## Duas opções

### Opção A — manter o projeto simples

Reduzir a força da reivindicação HCAI.

Em vez de sugerir uma avaliação completa de cooperação humano-IA, dizer que o sistema é:

> “desenhado segundo princípios HCAI, incorporando explicabilidade, confiança calibrada e decisão humana final.”

É uma afirmação mais defensável.

### Opção B — assumir HCAI como contribuição

Então seria necessário incluir um pequeno estudo com utilizadores, por exemplo:

- inspetores ou utilizadores representativos;
- casos de sucesso e falha;
- tarefa de aceitar/rejeitar uma deteção;
- medir confiança;
- medir tempo de decisão;
- medir concordância com a explicação.

Esta opção torna o projeto muito mais forte, mas também aumenta bastante o âmbito.

Para uma proposta de projeto académico, eu tenderia para **Opção A**, a menos que exista tempo e acesso a participantes humanos.

---

# 10. Faltam referências fundamentais de HCAI/XAI

A bibliografia é razoavelmente boa para AIS e deteção de pesca, mas a proposta afirma explicitamente que se enquadra em HCAI.

No entanto, não há referências dedicadas a:

- Human-Centered AI;
- explainable AI;
- confiança em sistemas IA;
- human-AI collaboration;
- calibration/uncertainty;
- human-in-the-loop decision support.

Isto cria uma assimetria:

**a proposta diz que HCAI é uma dimensão central, mas a bibliografia praticamente só fundamenta a dimensão AIS/ML.**

Eu adicionaria pelo menos algumas referências fundamentais nesta área.

---

# 11. “Explicabilidade” ainda está demasiado vaga

A proposta diz:

> “importâncias de características ou confiança calibrada”

Mas estes conceitos não são equivalentes.

### Feature importance

Responde:

> “Que características contribuíram para esta previsão?”

### Confidence calibration

Responde:

> “Quando o modelo diz 80%, essa probabilidade corresponde aproximadamente a 80% de acerto?”

São propriedades diferentes.

Idealmente deveriam ser separadas:

1. **explicabilidade** → feature attribution;
2. **incerteza/calibração** → reliability/calibration;
3. **human-in-the-loop** → apresentação dessas informações ao utilizador.

---

# 12. A avaliação precisa de métricas mais específicas

Precisão, recall, F1 e IoU são adequados como ponto de partida.

Mas como o problema é **segmentação temporal**, seria interessante definir explicitamente métricas que capturem a qualidade das fronteiras.

Por exemplo:

- IoU por segmento;
- boundary error;
- diferença entre início/fim previsto e verdadeiro;
- número de segmentos espúrios;
- duração média dos segmentos;
- fragmentação;
- estabilidade relativamente a pequenas alterações de janela.

A proposta já fala em “estabilidade temporal”, mas ainda não define claramente **como a estabilidade será medida**.

Este é um ponto que eu reforçaria bastante.

---

# 13. “Estabilidade” precisa de uma definição operacional

A palavra aparece várias vezes:

> “segmentações temporalmente estáveis”

> “avaliar explicitamente o efeito ... na estabilidade dos segmentos”

Mas o leitor ainda não sabe exatamente o que significa estabilidade.

Uma possibilidade seria definir estabilidade relativamente à alteração de:

- tamanho da janela;
- percentagem de overlap;
- pequena perturbação dos pontos;
- seeds do modelo;
- ruído temporal.

Por exemplo:

> duas segmentações obtidas com pequenas alterações nos parâmetros devem apresentar elevada concordância temporal.

Poderia então ser medida por IoU entre segmentações, boundary displacement ou outra métrica adequada.

---

# 14. A redução das cinco classes para duas merece justificação

O dataset contém:

- `02-fishing`
- `04-fishing`
- `01-sailing`
- `03-sailing`
- `05-sailing`

e a proposta agrega tudo em:

- pesca;
- navegação.

Isto é razoável se o objetivo for simplesmente pesca vs. não pesca.

Mas existe uma questão científica:

**se o dataset tem diferentes tipos/estados de atividade, o que se perde ao agregá-los?**

Convém justificar:

> “O objetivo deste projeto é exclusivamente distinguir atividade piscatória de navegação; por isso, as subclasses são agregadas.”

Também seria útil indicar se a agregação será feita antes da divisão treino/teste.

---

# 15. O desequilíbrio de classes está apenas mencionado

A proposta diz:

> “tratando o desequilíbrio por amostragem ou ponderação.”

Mais uma vez, existem alternativas mas nenhuma escolha definida.

Seria melhor dizer:

> “O desequilíbrio será tratado através de pesos de classe na função de perda.”

ou:

> “Será utilizada amostragem estratificada...”

Se ainda não estiver decidido, pode ficar como análise experimental, mas o método principal deveria estar definido.

---

# 16. A divisão treino/validação/teste devia ser explícita

A proposta diz corretamente que a divisão será feita por trajetória.

Mas falta indicar algo como:

- 70/15/15;
- 5-fold cross-validation por trajetória;
- treino/validação/teste fixos.

Também seria importante garantir que a escolha de hiperparâmetros usa apenas treino/validação.

Uma estrutura forte seria:

**train trajectories → validation trajectories → held-out test trajectories**

e nunca selecionar hiperparâmetros olhando para o test set.

---

# 17. Seria muito útil incluir uma pergunta de investigação principal

Atualmente existe um objetivo geral, mas não uma verdadeira pergunta de investigação.

Eu acrescentaria algo deste género:

> **RQ1:** Em que medida a utilização de janelas sobrepostas melhora a qualidade e estabilidade da segmentação de atividade de pesca em trajetórias AIS?

> **RQ2:** Em que medida o pós-processamento temporal reduz a fragmentação e melhora a concordância entre os segmentos previstos e os anotados?

> **RQ3:** Que informação de explicabilidade é mais útil para permitir que um utilizador humano valide uma deteção?

Mesmo que RQ3 fique mais simples, as duas primeiras já tornariam a proposta bastante mais científica.

---

# 18. Estrutura atual vs. estrutura recomendada

## Estrutura atual

```text
Abstract
│
├── Problema e Motivação
├── Contexto
├── Objetivos
├── Abordagem
├── Materiais e Dados
├── Avaliação
└── Referências
```

Esta estrutura é boa.

## Estrutura que eu recomendaria

```text
Abstract
│
├── 1. Problema e Motivação
│
├── 2. Contexto e Trabalho Relacionado
│     ├── AIS e deteção de pesca
│     ├── Semantic segmentation
│     ├── Métodos de aprendizagem
│     └── HCAI / XAI
│
├── 3. Questão de Investigação e Contribuições
│     ├── RQ1
│     ├── RQ2
│     ├── Hipóteses
│     └── Contribuições
│
├── 4. Abordagem
│     ├── Pré-processamento
│     ├── Janelamento
│     ├── Modelo
│     ├── Reconstrução ponto-a-ponto
│     ├── Pós-processamento
│     └── Explicabilidade
│
├── 5. Dados e Materiais
│
├── 6. Protocolo Experimental
│     ├── Splits
│     ├── Baselines
│     ├── Ablations
│     ├── Métricas
│     └── Análise estatística/robustez
│
├── 7. Considerações HCAI e Éticas
│
└── Referências
```

Não é obrigatório aumentar o número de secções. O essencial é **tornar explícitas as perguntas e o protocolo experimental**.

---

# 19. O abstract está bom, mas pode ficar mais preciso

O abstract tem os elementos essenciais:

- problema;
- dados;
- método;
- baselines;
- métricas;
- dimensão HCAI.

Isso é bom.

O principal problema é que diz:

> “Propomos um sistema...”

quando algumas decisões metodológicas ainda não estão fechadas.

Se a proposta for apresentada antes da implementação, isso é aceitável, mas seria melhor tornar a contribuição mais específica:

> “Propomos estudar se a combinação de janelas sobrepostas e pós-processamento temporal melhora a estabilidade e qualidade da segmentação...”

Isso coloca a **questão experimental** no centro.

---

# 20. A secção “Contexto” pode ser melhorada

A revisão bibliográfica cobre bastante coisa:

- VMS;
- AIS;
- HMM;
- semantic segmentation;
- deep learning;
- comportamento de navios;
- IUU.

Isto mostra boa cobertura.

Contudo, há alguma sensação de “lista de trabalhos”.

Seria mais forte organizar a literatura por **linhas de abordagem**:

### A. Métodos probabilísticos

HMM / VMS.

### B. Semantic segmentation

Soares Júnior → Wu et al.

### C. Deep learning

Cheng → Wang → Hu → outros.

### D. Fishing activity detection / trajectory classification

Ferreira → Arasteh → Luo → Xing.

### E. Human-centered AI

Adicionar literatura específica.

Depois terminar com:

> “Nenhuma destas linhas aborda explicitamente X nas condições Y.”

Isto produz uma revisão mais argumentativa e menos descritiva.

---

# 21. Um problema de posicionamento: “deep learning” pode estar a distrair da contribuição principal

A proposta menciona vários trabalhos recentes de deep learning, mas a contribuição anunciada não parece ser uma nova arquitetura.

Isso pode criar uma expectativa errada.

O trabalho parece ser mais sobre:

**temporal segmentation + overlapping windows + post-processing + decision support**

do que sobre:

**nova arquitetura deep learning**.

Eu evitaria vender demasiado a parte da arquitetura.

O modelo pode ser relativamente standard. A contribuição experimental está na forma como as previsões são construídas e estabilizadas.

---

# 22. O pipeline devia ser acompanhado por uma figura

A proposta descreve o pipeline em texto:

```text
Ingestão
   ↓
Pré-processamento
   ↓
Janelamento
   ↓
Classificação
   ↓
Agregação das janelas
   ↓
Pós-processamento temporal
   ↓
Segmentos
   ↓
Explicabilidade / decisão humana
```

Uma figura simples deste pipeline teria bastante valor.

Especialmente porque ajudaria a resolver a ambiguidade entre:

**window classification**

e

**semantic segmentation**.

---

# 23. A proposta precisa de um protocolo experimental mais concreto

Eu tentaria fazer com que a secção de avaliação respondesse explicitamente a estas perguntas:

### Experiência 1 — Baseline

Como funciona o método sem overlap e sem pós-processamento?

### Experiência 2 — Overlap

O que acontece quando introduzimos overlap?

### Experiência 3 — Pós-processamento

O que acontece quando introduzimos apenas pós-processamento?

### Experiência 4 — Método completo

Overlap + pós-processamento.

### Experiência 5 — Robustez

Como variam os resultados para:

- 0%;
- 25%;
- 50%;
- 75%;

de overlap?

### Experiência 6 — Robustez do pós-processamento

Comparar diferentes níveis de suavização/regularização.

### Experiência 7 — Explicabilidade

Mostrar casos de:

- verdadeiro positivo;
- falso positivo;
- verdadeiro negativo;
- falso negativo;
- fronteira correta;
- fronteira incorreta.

Isto produziria uma história experimental muito mais convincente.

---

# 24. Uma questão importante: “superar os baselines” é uma condição demasiado forte

A proposta diz:

> “Considera-se o trabalho bem-sucedido se o sistema (i) superar os baselines...”

Eu mudaria isto.

Um projeto científico não deve necessariamente ser considerado mal sucedido se não superar um baseline.

Pode descobrir que:

- overlap melhora estabilidade mas não F1;
- pós-processamento melhora IoU mas reduz recall;
- determinado baseline é melhor;
- a técnica funciona apenas para determinadas trajetórias.

Isso também é resultado científico.

Melhor formulação:

> “O sucesso do trabalho será avaliado pela capacidade de caracterizar quantitativamente o efeito das janelas sobrepostas e do pós-processamento, procurando melhorar a qualidade e estabilidade da segmentação relativamente aos baselines.”

É uma formulação mais científica e menos “competitiva”.

---

# 25. A bibliografia está consistente internamente

Foi verificada a correspondência entre citações e entradas bibliográficas.

### Resultado

- **17 referências** na bibliografia;
- **17 chaves citadas**;
- **0 referências não utilizadas**;
- **0 citações sem entrada correspondente**.

Isto está muito bem.

Não há, portanto, neste ficheiro, o problema clássico de referências quebradas ou bibliografia desatualizada em relação às citações utilizadas.

---

# 26. Mas a bibliografia está desequilibrada

A bibliografia está muito forte em:

- AIS;
- pesca;
- trajectory classification;
- semantic segmentation.

Está fraca em:

- HCAI;
- XAI;
- human-AI collaboration;
- uncertainty/calibration;
- decision support.

Como HCAI é apresentado como parte importante da proposta, esta é provavelmente a maior lacuna bibliográfica.

Também falta uma referência explícita ao dataset.

---

# 27. Questões formais/LaTeX

## 27.1. Autores

O documento contém:

> Dinis Soveral Botelho Rosa  
> University of Coimbra / Department of Informatics Engineering  
> dinisrosa22@gmail.com

Se a submissão for **anónima**, isto tem de ser alterado.

O próprio comentário no `.tex` já reconhece isso:

> “For an anonymous submission, replace this block...”

Portanto, é preciso confirmar as regras concretas da inscrição.

---

## 27.2. Line numbers

A proposta usa:

```latex
\linenumbers
```

Isto pode estar correto para submissão, dependendo das regras do template.

Deve ser removido para a versão final/camera-ready se as instruções do template assim determinarem.

---

## 27.3. Template

A proposta está explicitamente preparada para o template IJCAI–ECAI 26.

Isto é positivo porque demonstra preocupação com conformidade formal.

No entanto, convém verificar as instruções específicas da **modalidade/track onde o projeto será inscrito**, porque uma proposta de projeto pode ter requisitos adicionais diferentes de um paper científico normal.

---

# 28. O que eu mudaria primeiro — prioridade alta

Se tivesse pouco tempo, faria estas alterações nesta ordem:

## Prioridade 1 — Definir claramente a contribuição

Uma frase muito concreta:

> “Este projeto investiga se a combinação de janelas temporais sobrepostas e regularização temporal melhora a qualidade e estabilidade da segmentação de atividade de pesca em trajetórias AIS.”

---

## Prioridade 2 — Introduzir RQs/hipóteses

Pelo menos:

- RQ1 — efeito do overlap;
- RQ2 — efeito do pós-processamento;
- RQ3 — interação entre ambos.

---

## Prioridade 3 — Resolver semantic segmentation vs window classification

Adicionar explicitamente a etapa:

```text
window predictions
        ↓
point-level reconstruction
        ↓
temporal segmentation
```

---

## Prioridade 4 — Criar ablation study

Comparar:

```text
No overlap + no post-processing
No overlap + post-processing
Overlap + no post-processing
Overlap + post-processing
```

Esta é provavelmente a experiência mais importante do projeto.

---

## Prioridade 5 — Tornar o modelo principal concreto

Escolher uma arquitetura principal.

Não deixar:

> “LSTM ou CNN”

como decisão central.

---

## Prioridade 6 — Definir estabilidade

Explicar matematicamente ou pelo menos operacionalmente o que significa uma segmentação “estável”.

---

## Prioridade 7 — Fortalecer HCAI ou reduzir a reivindicação

Se não houver estudo com utilizadores:

> apresentar HCAI como princípio de design e não como uma avaliação completa de interação humano-IA.

---

## Prioridade 8 — Adicionar referências HCAI/XAI

É necessário sustentar academicamente a parte humana da proposta.

---

## Prioridade 9 — Referenciar o dataset

Adicionar a referência bibliográfica correspondente.

---

## Prioridade 10 — Especificar o split experimental

Por exemplo:

```text
train trajectories
validation trajectories
test trajectories
```

com proporções ou estratégia de cross-validation claramente definidas.

---

# 29. O que eu NÃO mudaria

Há partes que eu manteria praticamente como estão.

### Problema e motivação

Está forte e bem contextualizado.

### Ligação entre pesca IUU e AIS

É clara e relevante.

### Escolha de Wu et al.

É uma boa âncora para posicionar o trabalho.

### Objetivos

Estão bem alinhados com o pipeline.

### Uso de validação por trajetória

Manter.

### Preocupação com decisão humana

Manter.

### Considerações éticas

Manter, mas eventualmente separar da metodologia HCAI.

### Métricas básicas

F1, recall, precisão e IoU fazem sentido e devem continuar.

---

# 30. Como eu caracterizaria a proposta neste momento

Eu classificaria os diferentes componentes aproximadamente assim:

| Dimensão | Avaliação | Comentário |
|---|---|---|
| Problema | **Muito bom** | Concreto e relevante |
| Motivação | **Muito bom** | Boa ligação entre domínio e problema técnico |
| Estado da arte | **Bom** | Boa cobertura, mas falta HCAI/XAI |
| Gap científico | **Bom** | Existe, mas precisa de maior precisão |
| Objetivos | **Muito bom** | Bem alinhados com a abordagem |
| Metodologia | **Bom** | Coerente, mas ainda demasiado aberta |
| Novidade | **Razoável/Bom** | Precisa de ser melhor defendida |
| Avaliação | **Bom** | Boa direção, mas faltam definições experimentais |
| HCAI | **Razoável** | Boa motivação, avaliação ainda fraca |
| Ética | **Bom** | Boa consciência das implicações |
| Bibliografia | **Bom** | Consistente, mas desequilibrada |
| Estrutura | **Muito bom** | Sequência lógica e fácil de seguir |
| Clareza | **Muito bom** | Linguagem direta e compreensível |
| Reprodutibilidade | **Razoável** | Faltam várias decisões experimentais |
| Formalidade LaTeX | **Bom** | Bem encaminhada, sujeito às regras da submissão |

---

# 31. Veredicto final

**Sim — eu diria que a proposta está bem inscrita do ponto de vista estrutural.**

Não me parece uma proposta desorganizada nem uma coleção de ideias soltas. Pelo contrário: existe uma história clara e uma boa correspondência entre problema, objetivos e abordagem.

O que falta é sobretudo **transformar uma boa proposta de engenharia num projeto científico mais rigorosamente testável**.

A principal evolução que faria seria esta:

### De:

> “Vamos construir um sistema de segmentação com janelas sobrepostas, pós-processamento e explicabilidade.”

### Para:

> “Vamos investigar se a combinação de janelas sobrepostas e pós-processamento temporal melhora a qualidade e estabilidade da segmentação de atividade de pesca em trajetórias AIS, isolando experimentalmente o contributo de cada componente e avaliando a utilidade das previsões como apoio à decisão humana.”

A segunda formulação é muito mais forte porque:

- define a pergunta;
- define a contribuição;
- implica uma experiência;
- permite um resultado positivo ou negativo;
- evita prometer uma arquitetura revolucionária;
- dá uma justificação clara para o ablation study.

---

# 32. Estrutura que eu recomendaria para a versão final

Se fosse eu a fechar esta proposta, tentaria chegar a:

```text
ABSTRACT
    ↓
1. PROBLEMA E MOTIVAÇÃO
    ↓
2. CONTEXTO / TRABALHO RELACIONADO
    ↓
3. QUESTÕES DE INVESTIGAÇÃO E CONTRIBUIÇÕES
    ↓
4. ABORDAGEM
      ├── Pré-processamento
      ├── Janelas sobrepostas
      ├── Classificador
      ├── Reconstrução ponto-a-ponto
      ├── Pós-processamento
      └── Explicabilidade
    ↓
5. DADOS E MATERIAIS
    ↓
6. PROTOCOLO EXPERIMENTAL
      ├── Dataset split
      ├── Baselines
      ├── Ablation study
      ├── Métricas
      └── Robustez
    ↓
7. HCAI / ÉTICA
    ↓
REFERÊNCIAS
```

Se o limite de páginas for apertado, não é necessário criar todas estas secções. Algumas podem ser combinadas. **O mais importante é que a lógica acima apareça no texto.**

---

# 33. Conclusão curta

A proposta tem uma **base forte**.

Os maiores méritos são:

- problema relevante;
- narrativa coerente;
- bom posicionamento em semantic segmentation;
- objetivos alinhados;
- boa ideia de ablation;
- preocupação com leakage;
- preocupação com explicabilidade e decisão humana;
- bibliografia AIS consistente.

Os maiores riscos são:

- novelty ainda pouco precisa;
- segmentação vs. classificação de janelas não suficientemente formalizada;
- HCAI pouco operacionalizado;
- estabilidade não definida;
- modelo e técnicas de pós-processamento ainda vagos;
- baselines a necessitar de protocolo de comparação mais rigoroso;
- dataset sem referência explícita;
- falta de RQs/hipóteses.

**A minha recomendação seria não mudar radicalmente a proposta.** A estrutura de base está boa. Em vez disso, faria uma revisão cirúrgica para tornar a pergunta científica, a contribuição e o protocolo experimental muito mais explícitos.


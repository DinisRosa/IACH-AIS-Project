---
name: delegate-terminal
description: Delega tarefas pesadas (refactors multi-ficheiro, revisões de código alargadas, geração de blocos extensos, documentação ou testes em grande volume, análises profundas) para o terminal via abacusai e opencode, para poupar a quota do modelo principal. Usa esta skill sempre que o utilizador pedir trabalho grande de geração ou análise de código, mesmo que não mencione "delegar", "Abacus" ou "poupar quota". Não uses para perguntas curtas, pequenas edições num único ficheiro ou simples leitura do projeto.
---

# Delegar para o terminal

O teu papel aqui é de orquestrador: decides se a tarefa vale a pena delegar e, se valer, chamas o script `scripts/delegate.sh` (na pasta desta skill). O trabalho pesado corre em modelos remotos via `abacusai` e `opencode`, fora da quota do modelo principal.

**Regra firme:** não uses Ollama nem qualquer modelo local, em lado nenhum.

## 1. Responder diretamente ou delegar?

**Responde tu (não delegues) quando:**
- a pergunta é curta ou conceptual (explicar um erro, um comando, um conceito);
- a alteração é pequena (até ~30 linhas, num único ficheiro);
- só é preciso ler ou localizar algo no projeto;
- delegar custaria mais, em tempo e tokens, do que responder.

**Delega quando:**
- a tarefa envolve vários ficheiros (refactor, migração, revisão alargada);
- é preciso gerar blocos extensos (mais de ~100 linhas), documentação longa ou muitos testes;
- é preciso análise profunda de código ou raciocínio demorado.

Na dúvida, responde diretamente. Delegar é uma otimização, não uma obrigação.

## 2. Como delegar

Usa sempre o script, em vez de montares pipes e aspas à mão:

```bash
scripts/delegate.sh [opções] "<tarefa>"
```

| Opção | Função |
|---|---|
| `-f FICHEIRO` | Inclui um ficheiro como contexto (repetível). A Abacus não vê o projeto, por isso passa sempre os ficheiros relevantes. |
| `-P FICHEIRO` | Lê a tarefa de um ficheiro (para prompts longos ou com muitos caracteres especiais). |
| `-m MODELO` | Modelo da Abacus (por omissão `ROUTE_LLM`). |
| `-r "instrução"` | Depois da Abacus, refina o resultado com o `opencode`. |
| `-M provider/modelo` | Modelo remoto do `opencode`. Obrigatório para `-r` e para o fallback, a menos que `OPENCODE_MODEL` esteja definida. |
| `-o FICHEIRO` | Guarda o resultado num ficheiro e mostra só um resumo no stdout. |
| `-t SEGUNDOS` | Timeout por chamada (por omissão 300). |

### Exemplos

Revisão de um ficheiro:
```bash
scripts/delegate.sh -f src/api.py "Revê este código: bugs, problemas de segurança e melhorias. Responde com uma lista priorizada."
```

Vários ficheiros, resultado guardado (poupa mais, porque não tens de ler o output todo):
```bash
scripts/delegate.sh -f src/a.ts -f src/b.ts -o /tmp/refactor.md "Propõe um plano de refactor para extrair a lógica comum destes dois módulos."
```

Gerar com a Abacus e refinar com o OpenCode:
```bash
scripts/delegate.sh -M "<provider/modelo>" -r "Simplifica e corta o que for redundante." "Escreve a documentação do módulo de autenticação."
```

Prompt longo, escrito primeiro num ficheiro:
```bash
scripts/delegate.sh -P /tmp/prompt.txt -f src/main.py
```

## 3. Antes de correres

- **Modelo do OpenCode:** se vais usar `-r` ou queres fallback e `OPENCODE_MODEL` não estiver definida, pergunta ao utilizador uma vez qual é o modelo remoto (`provider/modelo`) e reutiliza-o durante a sessão.
- **Prompts curtos:** o objetivo é poupar tokens. Escreve a tarefa de forma direta e deixa o ficheiro de contexto fazer o trabalho de volume.
- **Executa tu o comando** se tiveres acesso ao terminal e lê o output. Se não tiveres, mostra o comando pronto a copiar e pede ao utilizador que cole o resultado.

## 4. Falhas

O script já tenta o `opencode` se a `abacusai` falhar ou devolver vazio. Se ambos falharem, termina com código 2:

- diz ao utilizador o que aconteceu, numa frase;
- responde tu diretamente, na medida do razoável;
- não repitas tentativas em ciclo.

Se o código for 1, foi um erro de uso (opção em falta, ficheiro inexistente): corrige o comando e corre uma vez.

## 5. Depois de teres o resultado

Resume-o em poucas linhas, aponta os próximos passos e, se o resultado foi guardado com `-o`, diz onde está. Não colas o output inteiro na resposta, a menos que o utilizador peça. Responde em português europeu.
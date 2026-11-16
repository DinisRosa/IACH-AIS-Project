# Correção do split por ID completo — desenho

## Intenção

Manter cada trajetória identificada pelo seu ID completo num único conjunto
de treino, validação ou teste. Neste projeto, um ID completo é a unidade de
análise independente; não será feita agregação pelo prefixo do ID.

## Objetivos

- Usar percentagens 70/15/15 nos splits gerados por omissão.
- Tornar explícito no código e no README que o split é por ID completo.
- Atualizar a proposta e o PDF, marcando a vermelho cada alteração textual.

## Fora de âmbito

- Agrupar trajetórias por MMSI/prefixo do ID.
- Alterar modelos, métricas ou o restante pipeline.

## Abordagem escolhida

O algoritmo existente já embaralha e atribui chaves integrais do dataset, pelo
que preserva cada trajetória completa. A alteração limita-se a clarificar esta
semântica e a corrigir as percentagens predefinidas. No LaTeX, as frases novas
ou substituídas são envolvidas em `\textcolor{red}{...}` e o PDF é recompilado.

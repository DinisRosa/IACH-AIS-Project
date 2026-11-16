# Split por ID Completo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` skill (recommended) or `executing-plans` skill to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Gerar splits 70/15/15 por ID completo e refletir essa decisão no PDF com alterações a vermelho.

**Architecture:** O dataset permanece indexado por ID completo; o algoritmo de divisão existente continua a usar essas chaves sem as decompor. Apenas se atualizam a configuração, os textos explicativos e o artefacto PDF compilado.

**Tech Stack:** Python, JSON, LaTeX/pdfLaTeX.

**Spec:** `docs/superpowers/specs/2026-11-13-split-id-completo-design.md`

## Global Constraints

- Cada ID completo é uma unidade independente, sem agrupamento pelo prefixo.
- A divisão é 70/15/15 e cada trajetória é integralmente atribuída a um único split.
- Toda a redação alterada na proposta deve aparecer a vermelho no PDF.

## Review Focus

- IDs com prefixos iguais podem pertencer a splits distintos; o ID completo nunca pode ser duplicado.
- As contagens dos splits devem somar o número de IDs e respeitar o método do maior resto.
- A recompilação do PDF deve refletir texto vermelho, sem referências ou erros LaTeX novos.

### Task 1: Configurar e regenerar splits por ID completo

**Files:**
- Modify: `CODE/0_features_eng/divide_dataset.py`
- Modify: `CODE/README.md`
- Modify: `CODE/1_training/train.json`
- Modify: `CODE/2_testing/test.json`
- Modify: `CODE/3_validation/validation.json`

- [ ] Clarificar no docstring que o ID é usado integralmente e trocar o exemplo executável para 70/15/15.
- [ ] Regenerar os três JSON com o dataset existente e confirmar 86/19/18 IDs, sem IDs completos repetidos.

### Task 2: Atualizar e compilar a proposta

**Files:**
- Modify: `latex/proposta_pt.tex`
- Modify: `latex/proposta_pt.pdf`

- [ ] Atualizar a descrição da divisão e da contagem de IDs, com cada texto alterado em vermelho.
- [ ] Compilar o LaTeX e confirmar que o PDF resultante contém as alterações.

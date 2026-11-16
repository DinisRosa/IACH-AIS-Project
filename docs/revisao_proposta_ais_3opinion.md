# Avaliação da Proposta de Projeto: Segmentação Semântica de Trajetórias AIS

Parabéns pelo excelente trabalho! A tua proposta demonstra maturidade científica, com uma narrativa lógica que flui perfeitamente desde o problema global (pesca IUU) até às decisões de implementação técnica (janelas sobrepostas e HCAI). A estrutura que escolheste é clássica e muito eficaz para artigos científicos.

## O que está muito bem feito (Pontos Fortes)

*   **Estrutura Lógica:** A divisão em seções (Problema e Motivação, Contexto, Objetivos, Abordagem, Materiais/Dados, Avaliação) segue as melhores práticas da escrita científica. O leitor sabe exatamente o que esperar e onde encontrar a informação.
*   **Posicionamento (Gap Analysis):** Na secção de Contexto, fazes um excelente trabalho a mapear o estado da arte e, de seguida, apontas exatamente onde o teu projeto inova: combinar a segmentação de Wu et al. (2022) com robustez temporal e a vertente Humano-IA.
*   **Objetivos Claros e Mensuráveis:** A lista de 5 objetivos específicos na Secção 3 é muito pragmática e mapeia diretamente para a tua secção de Abordagem.
*   **Uso de Referências:** As tuas referências não estão apenas "atiradas" para o texto; elas sustentam ativamente as tuas decisões arquiteturais (ex: usar um HMM baseado em Peel e Good, 2011).

## Áreas de Crescimento e Oportunidades de Melhoria

Embora o texto esteja excelente, aqui estão duas áreas fundamentais onde podes refinar a tua proposta para garantir que não restam dúvidas ao avaliador:

*   **Clarificação da Componente Humana (Human-in-the-loop):**
    *   *Onde no texto:* Na secção 4 (Abordagem), referes que "o sistema devolve a trajetória segmentada com um nível de confiança por segmento e justificações... apresentadas de forma a apoiar --- e não substituir --- a decisão do inspetor." Na secção 6 (Avaliação), dizes que avaliarás "a utilidade do sistema como apoio à decisão, ainda que de forma preliminar."
    *   *Porquê:* A proposta foca-se bastante em HCAI, mas a metodologia para *avaliar* essa componente humana é vaga. Se não vais testar com inspetores reais, o leitor pode achar que a promessa do "human-in-the-loop" fica por cumprir.
    *   *Próximo passo:* Como poderias clarificar de que forma será feita essa avaliação preliminar? Será através da simulação de um cenário de inspeção por ti mesmo, ou através da criação de uma prova de conceito visual (ex: um *dashboard*)? Sugiro adicionares meia frase na secção de Avaliação a explicar *como* vais medir essa utilidade.

*   **Gestão de Risco e Limitações:**
    *   *Onde no texto:* No final da secção 3 (Objetivos), dizes: "Considera-se o trabalho bem-sucedido se o sistema (i) superar os *baselines* nas métricas definidas..."
    *   *Porquê:* Em propostas científicas fortes, é importante demonstrar que o investigador pensou no que acontece se a hipótese principal falhar. E se o pós-processamento não superar os *baselines*? O projeto deixa de ter valor? (A resposta é não: provar que janelas sobrepostas não ajudam em AIS também seria um contributo científico válido).
    *   *Próximo passo:* Que frase poderias acrescentar na secção de Avaliação ou Objetivos para salvaguardar o valor do teu estudo caso os resultados quantitativos não sejam os esperados?

## Notas Menores de Estilo

*   Na secção 5 (Materiais e Dados), detalhas bastante os atributos do dataset Kaggle. Tem apenas cuidado com os nomes das variáveis em inglês no meio do texto em português (ex: `signed_turn`, `time_gap`). Está correto usar itálico, mas garante que é estritamente necessário enumerar todos estes atributos, ou se bastaria resumir os mais importantes para a classificação.
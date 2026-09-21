---
title: "Backlog — transformar melhoria geral em entregas"
tipo: planejamento
estado_documental: proposto
atualizado: 2026-09-09
tags:
  - atlas
  - planejamento
---

# Backlog — transformar melhoria geral em entregas

> [!important] Planejamento consolidado
> Para trabalho novo, usar [[wiki/planejamento/plano-do-projeto|Plano do projeto]], com entregas `PL-*`. Os códigos `AT-*` abaixo são legados desta lista e **não correspondem** aos achados técnicos homônimos. As descrições ficam preservadas como referência; os IDs canônicos de defeitos estão em [[wiki/planejamento/prioridades]].

As frentes vêm do objetivo confirmado. Prioridades, sequência e critérios abaixo são propostas técnicas, sem responsáveis ou datas inventados. Nenhuma caixa está marcada como concluída por simples existência de código.

## P0 — consolidar a base física e o controle

- [ ] **AT-01 — Inventário e versões instaladas.** Fotografar hardware, identificar alimentação/GPS/áudio, registrar SHAs do Pi e host de nuvem. Conclui com ficha reproduzível e sem credenciais. Fonte: [[wiki/hardware/especificacoes]].
- [ ] **AT-02 — Um broker no Pi.** Escolher apt ou Docker, registrar configuração efetiva, provar que ponte e serviços usam o mesmo processo. Depende de AT-01. Conclui após reboot e recepção consistente dos comandos.
- [ ] **AT-03 — Operar sem ESP32.** Usar BLE NUS no Pi, retirar dependência operacional de serial_ingestor e atualizar instalação/diagrama. Depende de AT-02. Conclui com ensaio filmado sem ESP32.
- [ ] **AT-04 — Motores reais e parada.** Conferir backend, sentidos, rampa e comportamento ao perder controle. Depende de AT-01/02/03. Conclui com resultados do protocolo T-CONTROLE e limitações registradas.

## P1 — IA, GPS e informações

- [ ] **AT-05 — Medir e melhorar a IA.** Montar perguntas de referência sobre a SETREM, comparar respostas e tempos, testar modo offline e recuperação. Registrar modelos/voz/configuração. Conclui com comparação antes/depois e avaliação da equipe.
- [ ] **AT-06 — Áudio e escuta.** Validar Vosk, silêncio/fim de frase, chamadas e sinais, ruído ambiente e reconexão USB. Pode avançar com AT-05. Conclui com amostras e ocorrências documentadas.
- [ ] **AT-07 — Instalar e validar GPS.** Identificar módulo e porta, obter fix real, conferir MQTT/banco/mapa e perda de sinal. Depende de AT-01/02. Conclui com registros reais correlacionados de ponta a ponta.
- [ ] **AT-08 — Confiabilidade da telemetria.** Ensaiar queda de rede e banco; quantificar atraso, duplicatas e perdas. Definir tratamento para eventos sem timestamp e distinguir origem real/simulada. Depende de AT-02 e coleta identificada.
- [ ] **AT-09 — Informações claras no controle.** Distinguir enviado, recebido, estado comandado e medido; indicar dado antigo e desconexão; testar telas em Android/iOS disponíveis. Depende dos contratos e de AT-04/07/08 para dados reais.
- [ ] **AT-10 — Implantação e continuidade do banco.** Confirmar PC/VM atual, responsável, backup/restauração, retenção e acesso. Decidir migração LARCC. Conclui com recuperação documentada e host identificado.

## P2 — integração e consolidação acadêmica

- [ ] **AT-11 — Conectar IA e corpo.** Definir se a conversa apenas consulta estado ou também atende `robo/voz/falar`; implementar contratos e testar indisponibilidade. Proposta que detalha “IA melhor”, ainda a validar como prioridade.
- [ ] **AT-12 — Dados para estatística.** Selecionar período real, variáveis e qualidade da amostra; produzir análise verificável sem misturar simulação. Entrega prevista no [[wiki/historico/relatorio-atual|LaTeX]], a confirmar com a equipe.
- [ ] **AT-13 — Atualizar relatórios e evidências.** Registrar arquitetura sem ESP32, classes, banco, resultados, limitações e extensão. Depende das entregas técnicas efetivamente concluídas.
- [ ] **AT-14 — Reconciliar documentação dos repos.** Corrigir ESP32 obrigatório, localização de implantação, afirmações de GPS e observabilidade MQTT. Base: [[wiki/estado/divergencias]].

## Estacionamento — não obrigatório no objetivo confirmado

- Serviço que execute automaticamente a rota planejada.
- Sensor de bateria: avaliar necessidade para informação/estatística de energia; produtor ainda inexistente.
- Rodas/amortecimento para piso de tijolos, após avaliação mecânica.
- Refatorações gerais que não impedem integração, como encerramento repetido dos serviços.

## Regra de conclusão

Para marcar uma tarefa: link de commit/PR quando houver código, SHA instalado quando aplicável, experimento com resultado, data, responsável e notas afetadas atualizadas. “Código escrito” não equivale a “implantado e validado”. Use [[modelos/Melhoria]] e [[modelos/Experimento]].

## Fontes e conferência

- [[wiki/planejamento/onde-queremos-ir]]
- [[wiki/estado/divergencias]]
- [[wiki/historico/relatorio-atual]]

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

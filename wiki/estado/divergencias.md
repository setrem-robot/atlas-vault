---
title: "Divergências — o que ainda precisa de confirmação"
tipo: estado
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - estado
---

# Divergências — o que ainda precisa de confirmação

As divergências ficam visíveis para evitar transformar fontes antigas em fatos atuais. Nenhuma foi resolvida por suposição.

| ID | Questão | Evidências em conflito | Tratamento / ação |
|---|---|---|---|
| D01 | GPS está montado? | PDF Orquestrador p. 38 declara integração; README atual diz módulo não montado; usuário pede implementar | Serviço existente; instalação atual pendente de inspeção e teste |
| D02 | Robô já se move com o código atual? | Narrativas gerais dizem sistema funcional; Estrutura p. 26 e README motores registram validação pendente | Não declarar movimento validado sem ensaio físico com SHA |
| D03 | API está no LARCC? | LaTeX/relatório citam LARCC; README informa PC provisório | Confirmar host, serviço, persistência e responsável |
| D04 | Pi precisa do ESP32? | Contrato e comentários antigos dizem não haver Bluetooth no Pi; código RobotEye implementa BLE direto | Arquitetura atual usa Pi; atualizar fontes antigas em tarefa futura |
| D05 | IA já usa MQTT? | README simplifica o contato à ponte; `web/comandos.py` também usa MQTT | Documentar ponte e painel; integração de fala/telemetria continua pendente |
| D06 | Rampa suportada? | Estrutura p. 20 fala 20°; p. 22 fala 5–7°; testes motorizados não realizados | Manter como requisitos divergentes, sem capacidade certificada |
| D07 | Ano/PIE da origem? | Capa Estrutura 2025; conteúdo 2026/PIE V; relatório atual PIE IV | Usuário define a entrega anterior; datas e numeração precisam de confirmação acadêmica |
| D08 | Modelo/áudio/SO históricos? | Interface usa “Gemma 3B”, P2, Bookworm/Trixie; README atual descreve outros modelos e áudio USB | Preservar relato; conferir artefatos/modelos e hardware atuais |
| D09 | Memória da face? | README reconhece 130–145 MB vs 70 MiB em medições distintas | Repetir medição com versão/configuração, não escolher número por conveniência |
| D10 | Retenção e perda de dados? | README estima horas de fila; código limita mensagens/bytes e ingestor pode descartar | Ensaiar queda de conexão e banco, contabilizar perdas/duplicatas |
| D11 | Rota segura é autonomia? | App envia pontos; não há consumidor em `robo/rota/comando` | Planejamento de rota implementado; execução autônoma futura |
| D12 | Commit local é melhoria inédita? | SHAs locais fora do remoto, mas árvores idênticas a squashes publicados | Usar a análise Git antes de planejar push/merge |

## Correções no vault anterior

O backup anterior foi preservado em [[fontes/vault-anterior-2026-09-09.zip]]. A documentação ativa foi revisada para corrigir comandos F/B/L/R/S, tópicos reais, endpoints reais, tabela única de telemetria, parada imediata no software, status comandado e limitações de segurança. Foram removidas afirmações sem sustentação de cobertura “100%” e origem em “monografia”.

Para fechar uma divergência, adicionar fonte nova, data, versão, resultado e responsável; depois atualizar as notas relacionadas. Não apagar silenciosamente a evidência antiga. [[wiki/meta/como-usar]].

## Fontes e conferência

- [[wiki/historico/relatorios-semestre]]
- [[wiki/historico/relatorio-atual]]
- [[wiki/estado/git-local-e-remoto]]
- [orquestrador/README.md](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/README.md)
- [RobotEye/README.md](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/README.md)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

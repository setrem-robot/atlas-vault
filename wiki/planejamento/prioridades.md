---
title: "Prioridades — a fila de trabalho"
tipo: planejamento
estado_documental: revisado
atualizado: 2026-09-10
tags:
  - atlas
  - planejamento
---

# Prioridades

**Entregas e dependências:** [[wiki/planejamento/plano-do-projeto|Plano do projeto]]. Nesta nota, `AT-*` identifica exclusivamente os achados da revisão técnica; não usar a numeração homônima do backlog legado.

Atualizado: **2026-09-09** · [[INICIO|Início]] · [[wiki/revisoes/2026-09-09-revisao-tecnica|Evidências e critérios de aceite]]

> [!warning] Controle e conectividade primeiro
> Resolver AT-01 e tratar AT-04 antes de validar movimento real. Corrigir AT-02/03 antes de medir concorrência da API. Esta lista não autoriza implantações automaticamente.

IDs correspondem aos itens numerados da revisão. Estados não revalidados permanecem pendentes; a atualização de 11/09 identificou correção versionada de AT-02, ainda sem verificar todo seu aceite.

| ID | Prioridade | Trabalho | Status | Responsável / evidência |
|---|---|---|---|---|
| AT-01 | P0 | Corrida de movimento depois de STOP | pendente | — |
| AT-02 | P1 | Conninfo inválido na API | em validacao | Correção `836593f` presente no HEAD local `69f2fce`; teste de parser versionado. Falta verificar timeout efetivo e casos de escaping; suíte não reexecutada nesta leitura |
| AT-03 | P1 | Consultas bloqueantes | pendente | — |
| AT-04 | P1 | Comandos antigos na fila MQTT | pendente | — |
| AT-05 | P1 | Perdas e duplicações de telemetria | em andamento | 11/09: store-and-forward no ar (Pi → `.150`): serviço `telemetria`, bridge `cleansession false` + fila 100 000, ingestor grava por `ts` (não duplica nem desordena o que sobe atrasado). Caminho-feliz na LAN validado (chega ao banco e à API). **Falta:** exercer a queda/reenvio offline; e o caminho por internet, que exige expor o MQTT do `.150` (8883/TLS). Ver [[wiki/historico/registro-de-trabalho]] |
| AT-06 | P1 | Identidade e isolamento por robô | pendente | — |
| AT-07 | P1 | Credenciais Wi-Fi nos logs | pendente | — |
| AT-08 | P1 | Autorização do controle BLE | pendente | — |
| AT-09 | P1 | Transporte e permissões cloud | pendente | — |
| AT-10 | P1 | Rollback de dependências | pendente | — |
| AT-11 | P2 | Custo de consultas e retenção | pendente | — |
| AT-12 | P2 | Contrato de tempo, payload e cursor | pendente | — |
| AT-13 | P2 | Limites do servidor de configuração | pendente | — |
| AT-14 | P2 | Instalação integrada de broker | pendente | — |
| AT-15 | P2 | CI e testes das fronteiras | pendente | — |
| AT-16 | P2 | Operação, backups e recursos | pendente | — |

## Sequência proposta

1. Controle: AT-01/04; ensaio físico após validação em software.
2. API: AT-02/03.
3. Segurança e dados: AT-07/08/09/05.
4. Entrega e integração: AT-10/14/15.
5. Frota e histórico: AT-06/11/12.
6. Robustez operacional e carga: AT-13/16.

## Status

`pendente` → `em andamento` → `em validacao` → `concluido`.

`bloqueado`: explicar dependência concreta. Ao iniciar, registrar responsável/agente, branch e escopo. Ao concluir, ligar commit/PR, testes e resultado de aceite. Separar validação em software e física. Compilar não basta para fechar um achado.

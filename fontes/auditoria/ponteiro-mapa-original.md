---
title: "Ponteiro — o mapa mudou de lugar"
tipo: fonte
estado_documental: snapshot
atualizado: 2026-09-10
tags:
  - atlas
  - fonte
---

# Mapa de comunicação da Atlas — mudou de lugar

Este arquivo virou um ponteiro. O mapa de verdade agora é **versionado**, em:

> **[`orquestrador/MAPA-COMUNICACAO.md`](./orquestrador/MAPA-COMUNICACAO.md)**

## Por que mudou

Ele morava aqui, nesta pasta, que **não é um repositório git**. O documento que
explica como os três repositórios conversam — os UUIDs do BLE, os nomes dos
tópicos MQTT, os contratos que quebram em silêncio quando um lado muda — existia
em uma única cópia, num disco, sem histórico e sem backup.

Foi para o `orquestrador` porque é lá que mora o `robo_common/topics.py`, a
fonte de verdade dos tópicos: o mapa e o contrato que ele descreve passam a
andar juntos, e uma mudança de fronteira pode atualizar os dois no mesmo commit.

## Não edite este arquivo

Qualquer coisa escrita aqui se perde do mesmo jeito que antes. Edite a cópia
versionada.

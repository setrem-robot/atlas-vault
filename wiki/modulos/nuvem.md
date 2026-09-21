---
title: "Nuvem — da mensagem à informação"
tipo: modulo
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - modulo
---

# Nuvem — da mensagem à informação

## Componentes encontrados

| Componente | Local em `orquestrador` | Função |
|---|---|---|
| Mosquitto remoto | `cloud/mosquitto` | Receber telemetria com autenticação |
| Ingestor | `cloud/ingestor/main.py` | Assinar MQTT e inserir registros |
| TimescaleDB | `cloud/timescaledb/init` | Armazenar payloads e tempo |
| FastAPI | `cloud/api/app` | Consultas de leitura, acesso e respostas |
| Cloudflared | `cloud/docker-compose.yml` | Caminho HTTP via túnel configurável |
| Ambiente local | `cloud/compose.local.yml`, `cloud/scripts` | Execução de desenvolvimento e simulação |
| Site | `site/index.html`, `ao-vivo.js`, `config.js`, `estilo.css` | Apresentação estática e dados públicos |

O Compose de nuvem tem cinco serviços. O modo local combina a definição principal com um override. O README relata hospedagem provisória no PC de um integrante e migração pendente para o LARCC; a implantação atual não foi acessada nesta tarefa.

## Confiabilidade encontrada

A bridge é somente de saída para `robo/telemetria/#`, com QoS 1 e sessão persistente. A configuração local de exemplo prevê 100.000 mensagens e 32 MiB de fila. A duração suportada depende do volume e tamanho das mensagens; não há garantia geral de “14 horas sem perda”.

O ingestor reconecta ao banco e tenta gravar um registro até duas vezes. Se ambas as tentativas falham, registra descarte. O esquema não tem identificador único de evento, e QoS 1 pode reenviar mensagens. A fila do broker não equivale a persistência garantida no banco.

## Dados de demonstração

`robo-falso.py` publica pelo broker; `semear-demonstracao.py` gera dados para visualização; `telemetria_falsa.py` também está disponível. Esses recursos permitem testar telas e integração, mas não demonstram GPS montado, bateria sensoriada ou motor em movimento.

## Próximas melhorias

Medir atraso, perdas/duplicatas, reconexão, origem real/simulada e crescimento do banco. Definir retenção e backup/restauração, confirmar host operacional e tornar as telas explícitas quando os dados estiverem atrasados. [[wiki/api/contratos]] e [[wiki/planejamento/backlog]].

## Fontes e conferência

- [orquestrador/cloud/docker-compose.yml](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/docker-compose.yml)
- [orquestrador/cloud/ingestor/main.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/ingestor/main.py)
- [orquestrador/pi/mosquitto/apt/robo.conf.example](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/mosquitto/apt/robo.conf.example)
- [orquestrador/cloud/timescaledb/init/01_schema.sql](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/timescaledb/init/01_schema.sql)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

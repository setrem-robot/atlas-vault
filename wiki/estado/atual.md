---
title: "Estado atual — o que funciona hoje"
tipo: estado
estado_documental: revisado
atualizado: 2026-09-21
tags:
  - atlas
  - estado
---

# Estado atual

Atualizado: **2026-09-21** · [[INICIO|Início]] · [[wiki/planejamento/prioridades|Próximas tarefas]]

> [!summary] Onde estamos
> Revisão de arquitetura, caminhos críticos e testes concluída (09/09–11/09). Em **20–21/09**, corrigidos no robô a **voz** (que não saía) e a **ponte BLE** (em crash-loop) — os dois eram regressões da conversão camelCase em nomes de bibliotecas; implantados e verificados no Pi. Adicionado o **switch IA local/nuvem** no app (RobotEye + app + contrato). App teve **release nova `1.2.4+11`** porque o patch OTA estava quebrado desde 16/09. Detalhes em [[wiki/historico/registro-de-trabalho#2026-09-21 — Conserto da voz e da ponte BLE, switch IA local/nuvem no app|Registro de 21/09]].

> [!check] Corrigido e no ar em 20–21/09 (verificado por SSH)
> - **Voz volta a falar.** `miniaudio.decode`/`PiperVoice.load` e atributos do chunk do Piper tinham nomes camelCase; edge (francisca) e Piper falhavam juntos → robô mudo. `falando: Oi oi, acordei!` sem erro após o conserto.
> - **Ponte BLE conecta.** `mqtt.Client(client_id=…)` restaurado (era `clientId`); `roboteye-ble.service` deixou o crash-loop e publica em `robo/comando/entrada`.
> - **Vosk sempre esteve certo** — a confusão era ouvido (Vosk) × voz (Piper).
> - **Switch IA local/nuvem** funcionando ponta a ponta (app → BLE → broker → face troca o LLM). Ver [[wiki/modulos/roboteye]] e [[wiki/modulos/aplicativo]].

## Base da revisão

| Componente | Commit revisado | Observação |
|---|---|---|
| IA | `e1b26d78f1f9b5ccb1f33c122203d791fa20ad44` | Cópia publicada separada; não atualizou RobotEye local |
| Orquestrador | `98ee681498e05426ff47041ae7f8e7ec97d0ffaf` | Local conferido com GitHub na revisão |
| App | `44d500160ecf13d7d1db2a4fe0c54052d352c0aa` | Local conferido com GitHub na revisão |

RobotEye local estava em `43a6fe0`, branch `producao` na coleta existente. Conferir novamente antes de corrigir. [[wiki/estado/git-local-e-remoto|Como atualizar o retrato Git]].

## Conclusão

Base modular favorável; confiabilidade e isolamento de múltiplos robôs precisam evoluir. Principais bloqueios: corrida movimento/STOP, conninfo inválido, I/O bloqueante, validade de comandos e garantia de entrega de telemetria.

## Evidências

- Orquestrador/API: 135 testes e 14 subtestes passaram.
- App: 32 testes passaram.
- IA: 781 testes na suíte; um teste de FPS falhou e passou isoladamente.
- Reproduções confirmaram corrida de STOP, erro de conninfo, bloqueio do event loop, fila offline MQTT, senha fictícia em logs e comparação incompatível de datas.

[[wiki/revisoes/2026-09-09-revisao-tecnica|Detalhes e limites]]. Esses testes não comprovam segurança física ou capacidade máxima.

## Implantado e conferido no robô em 09/09

Conferido por SSH, depois da revisão acima:

| | |
|---|---|
| RobotEye no Pi | `producao` `43a6fe0`, serviço `active` |
| Escuta | Vosk, microfone abrindo, vigia de captura sem disparar |
| CPU do serviço | 37,6 % · temperatura 54,3 °C · `throttled=0x0` |
| Serviços do `orquestrador` | 09/09: nenhum. **11/09: `telemetria` instalado e `active`** — publica a saúde do Pi; gps/motores/orquestrador seguem sem instalar (robô ainda sem andar) |
| Telemetria na nuvem (11/09) | Bridge Mosquitto Pi → `.150` no ar; `tipo=sistema` chega ao banco e à API pública. Ver [[wiki/historico/registro-de-trabalho]] |

Detalhes e limites em [[wiki/revisoes/2026-09-09-escuta-vosk-hardware]]. Precisão da escuta com voz humana continua **não validada**.

## Ainda não confirmado nesta revisão

Versões implantadas na VM; serviços do `orquestrador` instalados; configuração efetiva de broker, TLS e firewall; motores/GPS físicos; teste de carga; backup/restauração.

## Documentação local

Na inspeção, o vault tinha `.git`, mas nenhum commit nem remoto. Arquivos locais não equivalem a backup remoto. Esta organização não publicou nem criou commits. Os três repositórios receberam apenas instruções de navegação documental.

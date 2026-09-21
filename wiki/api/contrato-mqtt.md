---
title: "Contrato MQTT e BLE — o que o código usa"
tipo: contrato
estado_documental: revisado
atualizado: 2026-09-21
tags:
  - atlas
  - contrato
---

# Contrato MQTT e BLE — o que o código usa

> [!info] Referência reconciliada com o código
> O contrato original do orquestrador ainda descreve ESP32 obrigatório em alguns parágrafos. Aqui o caminho principal é BLE no Pi, e os nomes/payloads foram conferidos nos produtores, roteador e consumidores.

## BLE e entrada

| Item | Valor |
|---|---|
| Serviço NUS | `6e400001-b5a3-f393-e0a9-e50e24dcca9e` |
| RX — celular escreve | `6e400002-b5a3-f393-e0a9-e50e24dcca9e` |
| TX — notificação ao celular | `6e400003-b5a3-f393-e0a9-e50e24dcca9e` |
| Formato | Objeto JSON em UTF-8, terminado por quebra de linha |
| Limite da linha na ponte | 512 bytes |
| Entrada MQTT | `robo/comando/entrada` |

| Letra | Ação |
|---|---|
| F | Frente |
| B | Trás/ré |
| L | Esquerda |
| R | Direita |
| S | Parar |

As letras corretas são F/B/L/R/S. `R` não significa ré e `D` não é direção aceita no formato compacto.

## Comandos expandidos — exemplos válidos de formato

```json
{"tipo":"motor","acao":"frente","velocidade":80}
```
```json
{"tipo":"motor","acao":"mover","linear":0.8,"angular":-0.3}
```
```json
{"tipo":"voz","texto":"Olá, sou a Atlas."}
```
```json
{"tipo":"parada_emergencia"}
```
```json
{"tipo":"ia","modo":"nuvem"}
```

`ia.modo` ∈ `{local, nuvem}` — adicionado em 21/09. É o **único comando consumido pela cara (RobotEye), não pelo roteador**: troca qual modelo de linguagem responde. `local` = modelo do próprio Pi (`gemma3:1b`, offline e mais rápido); `nuvem` = modelo maior na rede (`qwen3:8b`), com queda automática para o local. O RobotEye assina `robo/comando/entrada` direto (`core/controle.py`); o roteador do orquestrador descarta este `tipo` como qualquer outro que não seja dele. Ver [[wiki/modulos/roboteye]].

Velocidade é limitada a 0–100, padrão 60. Eixos são limitados a -1–1; positivo linear avança e positivo angular gira à direita. Ausência de um eixo zera só aquele eixo. A parada normalizada é `{"acao":"parar","velocidade":0}`.

## Roteamento de comandos

| Entrada `tipo` | Destino | Payload repassado/normalizado | Consumidor |
|---|---|---|---|
| motor / comando compacto | `robo/motores/comando` | `acao`, `velocidade` ou eixos | motores |
| parada_emergencia | `robo/motores/comando` | `acao=parar`, `velocidade=0` | motores |
| voz | `robo/voz/falar` | `texto` | Pendente |
| ia | — (não roteado) | — | **RobotEye (cara)** — assina `robo/comando/entrada` direto; troca o LLM |
| wifi | `robo/wifi/comando` | `acao`, SSID e credencial quando necessários | wifi |
| rota | `robo/rota/comando` | `inicio`, `ponto` ou `fim` | Navegação pendente |

## Rota fatiada

```json
{"tipo":"rota","acao":"inicio","total":1,"nome":"exemplo"}
```
```json
{"tipo":"rota","acao":"ponto","i":0,"lat":-28.2,"lon":-54.0}
```
```json
{"tipo":"rota","acao":"fim"}
```

As coordenadas acima são ilustrativas. O roteador valida cada mensagem; não remonta a rota. Publicar `fim` não implica navegação iniciada.

## Estado e espelhamento

| Tópico de domínio | Produtor | Retido no domínio | Destino de telemetria |
|---|---|---|---|
| `robo/gps/posicao` | gps | Sim | `robo/telemetria/gps` |
| `robo/motores/status` | motores | Sim | `robo/telemetria/motores` |
| `robo/sistema/wifi` | wifi | Sim | `robo/telemetria/wifi` |
| `robo/sistema/bateria` | A definir | Previsto pelo contrato | `robo/telemetria/bateria` |
| `robo/telemetria/sistema` | telemetria | Não (QoS 1, sem retain) | publica **direto** aqui (não espelha) |

GPS inclui `lat`, `lon`, `fix`, `satelites`, `altitude_m`, `velocidade_kmh`, `rumo` e `ts`. Motores incluem `acao`, `velocidade`, `esquerda`, `direita` e eventualmente `motivo`. Wi-Fi publica `conectado`, `ssid`, `ip`, `ts`. O formato previsto de bateria usa `percentual` e `tensao_v`.

**Saúde do Pi** (`robo/telemetria/sistema`, serviço `telemetria`, a cada 30 s): publica **direto** no destino de telemetria — a saúde do Pi só serve ao histórico, não tem consumidor local a espelhar. Payload: `ts`, `temperatura_c`, `throttled` (cada bit de `vcgencmd get_throttled` aberto em booleano + `ok` + `hex`), `cpu` (`uso_pct`, `por_nucleo` [%], `freq_mhz`, `governor`, `voltagem_v`), `carga` (1/5/15 min), `processos` (`rodando`/`total`), `memoria` (`total_mb`, `disponivel_mb`, `uso_pct`, `swap_total_mb`, `swap_usado_mb`), `disco` (`total_gb`, `livre_gb`, `uso_pct`), `uptime_s`, `rede` (`rx_mb`/`tx_mb` por interface), `wifi` (`link`, `sinal_dbm` — `null` no cabo). Campos que a máquina não expõe viram `null`, nunca um zero falso.

Os serviços publicam heartbeat em `robo/sistema/heartbeat/<servico>`; a bridge usa `robo/sistema/bridge_status`. Esses tópicos não entram automaticamente no espelhamento de quatro domínios. `robo/voz/intencao` existe como constante, sem que isso comprove um fluxo de intenção integrado.

A publicação da ponte BLE usa QoS 1, sem retain. A bridge replica `robo/telemetria/# out 1`. Conferir QoS e retain no produtor específico antes de introduzir novo tópico. Não há, no código examinado, os tópicos `robo/motores/velocidade`, `robo/motores/parada` ou `robo/diagnostico/uptime` apresentados na versão anterior do vault.

[[wiki/api/contratos]] · [[wiki/arquitetura/mapa-comunicacao]] · [[wiki/seguranca/index]].

## Fontes e conferência

- [orquestrador/pi/services/_common/src/robo_common/topics.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/_common/src/robo_common/topics.py)
- [orquestrador/pi/services/orquestrador/src/orquestrador/roteador.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/orquestrador/src/orquestrador/roteador.py)
- [RobotEye/src/roboteye/ble/nus.py](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/src/roboteye/ble/nus.py)
- [RobotEye/src/roboteye/ble/mqtt.py](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/src/roboteye/ble/mqtt.py)
- [orquestrador/docs/contrato-mqtt.md](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/docs/contrato-mqtt.md)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

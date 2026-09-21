---
title: "ESP32 e serial — legado a retirar da operação"
tipo: modulo
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - modulo
---

# ESP32 e serial — legado a retirar da operação

O firmware `esp32/esp32_ble_bridge/esp32_ble_bridge.ino` implementa BLE NUS, recebe JSON e encaminha pela serial. O serviço `serial_ingestor` no Pi publica as linhas no MQTT. O relatório do semestre anterior descreve uma versão com Bluetooth Classic/SPP; o firmware atual já é BLE.

## O que mudou

A ponte `RobotEye/src/roboteye/ble` assume o mesmo serviço NUS e publica diretamente em `robo/comando/entrada`. Isso elimina a placa intermediária e o trecho serial no caminho principal. O destino dos comandos permanece o mesmo.

## Decisão do semestre

**Objetivo confirmado pelo usuário:** retirar o ESP32 e manter somente o Raspberry Pi no robô. O código antigo é evidência de origem e pode continuar arquivado para consulta. Preservar documentação histórica não significa manter dependência de hardware na operação.

Para declarar a retirada concluída: ligar o robô sem ESP32, iniciar BLE no Pi, usar um único broker, dirigir/parar e comprovar os comandos no serviço de motores. Atualizar instalação, fotos e relatório acadêmico com esse ensaio.

[[wiki/decisoes/registro]] · [[wiki/planejamento/backlog]] · [[wiki/arquitetura/mapa-comunicacao]].

## Fontes e conferência

- [orquestrador/esp32/esp32_ble_bridge/esp32_ble_bridge.ino](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/esp32/esp32_ble_bridge/esp32_ble_bridge.ino)
- [orquestrador/pi/services/serial_ingestor/src/serial_ingestor/main.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/serial_ingestor/src/serial_ingestor/main.py)
- [RobotEye/src/roboteye/ble/nus.py](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/src/roboteye/ble/nus.py)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

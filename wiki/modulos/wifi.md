---
title: "Wi-Fi — provisionamento e estado"
tipo: modulo
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - modulo
---

# Wi-Fi — provisionamento e estado

O serviço `pi/services/wifi` assina `robo/wifi/comando` e usa NetworkManager por `nmcli`. O roteador admite `conectar`, `listar` e `status`; a validação/aplicação está no módulo `rede.py`.

O comando de configuração entra pelo mesmo caminho das direções. Credenciais reais ficam fora do vault. O estado é publicado em `robo/sistema/wifi`, contendo conectado, SSID, IP e timestamp, e pode ser espelhado para a nuvem.

## Pontos de operação

- `robo-wifi.service` depende do ambiente e das permissões para alterar rede.
- A perda da rede não deve tirar o controle BLE do caminho local.
- O RobotEye inclui diagnóstico de rádio e scripts para separar o uso de Wi-Fi/Bluetooth; a existência do script não comprova qual adaptador está em uso hoje.
- Estado publicado no MQTT não garante confirmação de aplicação na interface do app. É uma melhoria a planejar.

O teste deve cobrir rede válida/inválida, retorno de status, reconexão da bridge e continuidade do BLE. [[wiki/configuracao/diagnostico]] e [[wiki/planejamento/backlog]].

## Fontes e conferência

- [orquestrador/pi/services/wifi/src/wifi/rede.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/wifi/src/wifi/rede.py)
- [orquestrador/pi/services/wifi/src/wifi/main.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/wifi/src/wifi/main.py)
- [RobotEye/src/roboteye/radio.py](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/src/roboteye/radio.py)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

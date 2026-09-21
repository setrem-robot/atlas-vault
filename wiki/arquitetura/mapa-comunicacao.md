---
title: "Mapa de comunicação — atual e legado"
tipo: arquitetura
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - arquitetura
---

# Mapa de comunicação — atual e legado

## Controle atual implementado

```mermaid
flowchart LR
  A[App Flutter] -->|BLE NUS - JSON por linha| P[Ponte BLE no Pi - RobotEye]
  W[Painel web local] -->|MQTT| B[Broker local único]
  P -->|robo/comando/entrada| B
  B --> O[Orquestrador]
  O -->|robo/motores/comando| M[Motores]
  O -->|robo/wifi/comando| F[Wi-Fi]
  O -.->|robo/voz/falar| V[Consumidor de fala pendente]
  O -.->|robo/rota/comando| N[Navegação pendente]
  M --> D[Drivers STEP e DIR]
```

Setas tracejadas terminam em consumidores que ainda faltam. A seta para drivers representa implementação encontrada, não teste físico realizado agora.

## Telemetria e banco

```mermaid
flowchart LR
  G[GPS - serviço existente] --> O[Orquestrador]
  M[Estado comandado dos motores] --> O
  W[Estado Wi-Fi] --> O
  B[Bateria - produtor pendente] -.-> O
  O -->|robo/telemetria/#| L[Mosquitto local]
  L -->|bridge out QoS 1| R[Broker remoto]
  R --> I[Ingestor]
  I --> T[(TimescaleDB)]
  T --> F[FastAPI de leitura]
  F -->|Bearer| A[App - Agora, Trajeto, Histórico, Eventos]
  F -->|Rotas públicas| S[Site estático]
```

## Caminho legado preservado

```mermaid
flowchart LR
  A[App] --> E[ESP32]
  E -->|Serial| S[serial_ingestor no Pi]
  S -->|robo/comando/entrada| B[Broker local]
```

O relatório anterior usava SPP nesse caminho. O firmware presente hoje usa BLE. Não misturar as duas versões. O destino MQTT é compartilhado, permitindo manter o restante dos serviços.

## Conversa e expressão

```mermaid
flowchart LR
  M[Microfone] --> H[Vosk ou Whisper]
  H --> G[Gatilho e transcrição]
  W[Painel ou terminal] --> A[Assistant]
  G --> A
  A --> L[Ollama - rede ou local]
  L --> S[Frases e Speaker]
  S --> T[Edge, Piper ou Kokoro]
  T --> O[Áudio]
  S --> E[Eventos]
  E --> F[Face]
```

Os endereços e portas estão em [[wiki/configuracao/setup-completo]]. Os payloads ficam em [[wiki/api/contrato-mqtt]].

## Fontes e conferência

- [orquestrador/pi/services/orquestrador/src/orquestrador/main.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/orquestrador/src/orquestrador/main.py)
- [RobotEye/src/roboteye/ble/nus.py](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/src/roboteye/ble/nus.py)
- [RobotEye/COMO-FUNCIONA.md](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/COMO-FUNCIONA.md)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

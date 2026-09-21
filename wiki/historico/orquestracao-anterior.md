---
title: "Orquestração — conectividade herdada"
tipo: historico
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - historico
---

# Orquestração — conectividade herdada

## Arquitetura relatada

O app Flutter enviava JSON em uma linha via Bluetooth Classic/SPP. Um ESP32-WROOM-DA validava e encaminhava o conteúdo pela serial. O Raspberry Pi distribuía as mensagens em MQTT, os serviços produziam estado e uma bridge encaminhava telemetria para o TimescaleDB.

```mermaid
flowchart LR
  A[App Android] -->|SPP| E[ESP32]
  E -->|Serial| S[serial_ingestor no Pi]
  S --> B[MQTT local]
  B --> O[Orquestrador e serviços]
  O --> T[Telemetria]
  T --> C[Broker remoto e ingestor]
  C --> D[TimescaleDB]
  D --> Q[Painel Quarkus e Leaflet]
```

## O que o relatório descreve

- App testado em Motorola Moto G30 com Android 12; direções `F`, `B`, `L`, `R`, `S` e parada ao soltar o botão (p. 28–30).
- Ajustes nas permissões Android e problema de dependência corrigida apenas no cache local (p. 29–30).
- Entrada MQTT `robo/comando/entrada`, roteamento para motores/voz/Wi-Fi e espelhamento seletivo (p. 31–34).
- Wi-Fi aplicado via NetworkManager/`nmcli`; status sem retorno serial→Bluetooth (p. 33).
- Serviço GPS com NMEA, posição, fix, satélites e velocidade (p. 33–34).
- Banco com tabela única `telemetria(ts, tipo, topico, payload)` (p. 34–35).
- Painel histórico Quarkus com REST/SSE, Leaflet e OpenStreetMap (p. 35–37).

## Lacunas registradas

O estado mostrado pelo controle representava a intenção enviada, sem confirmação de execução. A reconexão exigia ação manual. O suporte a iOS exigiria abandonar SPP. A conclusão ainda aponta integração da IA, motores, testes em campo, autonomia energética e distância percorrida como continuidade (p. 39).

## Conflitos que não podem ser apagados

A p. 38 declara a integração GPS concluída. Os READMEs atuais dizem que o módulo não está instalado. O relatório também usa descrições diferentes para o pareamento no Pi/ESP32. Essas afirmações ficam como evidência histórica, com validação atual pendente.

O backend encontrado hoje é FastAPI; o painel Quarkus é histórico e seu código não foi encontrado nos repositórios inventariados. Não foi presumida uma migração formal com data ou equivalência integral entre os dois.

Veja [[wiki/historico/evolucao]], [[wiki/estado/divergencias]] e [[wiki/modulos/nuvem]].

## Fontes e conferência

- [[fontes/relatorios/OrquestradorPDF.pdf#page=31|Arquitetura — p. 31]]
- [[fontes/relatorios/OrquestradorPDF.pdf#page=38|Conclusão — p. 38]]

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

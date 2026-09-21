---
title: "GPS — implementação e integração pendente"
tipo: modulo
estado_documental: revisado
atualizado: 2026-09-21
tags:
  - atlas
  - modulo
---

# GPS — implementação e integração pendente

O serviço `pi/services/gps` lê uma serial com `pyserial`, interpreta NMEA com `pynmea2` e acumula campos na classe `Posicao`. GGA fornece posição, fix e satélites; RMC acrescenta velocidade/rumo. A velocidade é convertida de nós para km/h.

Publicação de domínio: `robo/gps/posicao`. Espelhamento: `robo/telemetria/gps`. A posição válida exige fix e coordenadas disponíveis; o período é configurável por `GPS_INTERVALO_S`.

```json
{"lat":-28.2,"lon":-54.0,"fix":true,"satelites":7,"altitude_m":300.0,"velocidade_kmh":1.2,"rumo":90.0,"ts":1788969600}
```

Este payload é **exemplo ilustrativo** de formato, não leitura coletada do robô. Configure `GPS_PORT` e `GPS_BAUD` de acordo com o módulo identificado. Não foi encontrado inventário confiável do modelo físico ou da pinagem GPS atual.

## Atualização 2026-09-20/21 — módulo identificado, fiação diagnosticada

- **Módulo:** GY-GPS6MV2 (u-blox **NEO-6M**), NMEA a 9600 baud, TX em lógica 3,3 V (seguro para o Pi).
- **Ligação:** no **Pi 5, os pinos 8/10 (GPIO14/15) são do Bluetooth (UART0)** e não servem para o GPS sem desligar o BT que a ponte usa. Passou para a **UART3** (`dtoverlay=uart3-pi5`): GPS **TX → pino 21** (GPIO9/RXD3), GPS RX → pino 24 (GPIO8/TXD3). Config do Pi conferida por `pinctrl` (mux `a2`).
- **Diagnóstico:** mesmo com a UART correta, **zero byte** chega. Teste elétrico (pull-down interno no GPIO9) mostrou a linha sem nada empurrando — o módulo **não emite NMEA**, e um NEO-6M energizado emitiria na hora, mesmo sem satélite. Conclusão: **falta de energia** (VCC/GND sem contato firme; LED da placa apagado), a confirmar pelo usuário. Não é espera de satélite. Setup em `orquestrador/docs/setup-gps.md` (pinos a corrigir para UART3 quando o módulo ler).

## Pendência confirmada para este semestre

O usuário pediu implementar o GPS. O README atual informa que ele não está montado, apesar da conclusão histórica declarar integração. A tarefa é verificar módulo/ligação, observar sentenças reais, obter fix, conferir posição no MQTT, no banco e nas telas e testar perda de fix/reconexão.

O código não deve confundir última coordenada conhecida com posição atual válida. Esse comportamento, incluindo envelhecimento do fix e carimbo de tempo, precisa fazer parte do teste. A existência do serviço não demonstra precisão nem disponibilidade de sinal no campus.

[[wiki/estado/divergencias]] · [[wiki/planejamento/validacao]] · [[wiki/api/contratos]].

## Fontes e conferência

- [orquestrador/pi/services/gps/src/gps/main.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/gps/src/gps/main.py)
- [orquestrador/README.md](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/README.md)
- [[fontes/relatorios/OrquestradorPDF.pdf#page=38]]

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

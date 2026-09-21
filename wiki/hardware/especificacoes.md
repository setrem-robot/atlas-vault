---
title: "Hardware — herança e inventário a confirmar"
tipo: hardware
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - hardware
---

# Hardware — herança e inventário a confirmar

| Peça                       | Evidência disponível                                        | Situação documental                                               |
| -------------------------- | ----------------------------------------------------------- | ----------------------------------------------------------------- |
| Chassi aço e carenagem PLA | Relatório Estrutura                                         | Construção e ensaios manuais relatados                            |
| Raspberry Pi 5 de 8 GB     | README RobotEye                                             | Configuração de robô relatada                                     |
| Display 800×480            | README RobotEye                                             | Usado nas medições relatadas                                      |
| Microfone e áudio USB      | Relatório Interface e código/README RobotEye                | Hardware/modelo exato atual a conferir                            |
| Motores Nema 23            | Relatório Estrutura                                         | 2 unidades previstas/descritas; acionamento atual a validar       |
| Drivers TMC2209            | Código de acionamento e docs                                | Implementação destinada a esses drivers; confirmar peças e ajuste |
| ESP32                      | Relatório e firmware no orquestrador                        | Legado; retirada é objetivo confirmado                            |
| GPS                        | Serviço NMEA, PDF e READMEs divergentes                     | Modelo, montagem, porta e leitura física a confirmar              |
| Bateria e alimentação      | Relatórios e contrato de telemetria                         | Capacidade, proteção, autonomia e sensoriamento a confirmar       |
| Refrigeração               | README RobotEye relata calor sob IA e ausência de ventoinha | Conferir montagem atual e medir sob carga                         |

## Lacunas do acervo

Não foram localizados arquivos CAD/STL, esquema elétrico consolidado, lista de compras comprovada, capacidade de bateria confirmada ou fotografias recentes avulsas da montagem. Os PDFs incluem imagens históricas. Esta ausência é do acervo inspecionado, não afirma que a equipe não possui os arquivos em outro lugar.

## O que registrar na próxima bancada

Fotografia geral e interna; identificação do Pi e SO; modelos das placas; pinagem efetiva; fonte/bateria e tensões nominais; motores/drivers e ajustes; portas USB/serial; display; cooler; alterações desde os PDFs. Vincular esses dados a uma nota de experimento.

A pinagem declarada pelo código dos motores está em [[wiki/modulos/motores]]. Não foi inventado esquema elétrico para preencher as lacunas.

As medidas históricas estão em [[wiki/historico/estrutura-anterior]]. Orçamento e decisões novas devem ficar separados do custo estimado antigo.

## Fontes e conferência

- [[fontes/relatorios/EstruturaPDF.pdf#page=20]]
- [RobotEye/README.md](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/README.md)
- [orquestrador/pi/services/motores/src/motores/acionamento.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/motores/src/motores/acionamento.py)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

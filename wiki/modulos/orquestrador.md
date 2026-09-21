---
title: "Orquestrador — regras e barramento"
tipo: modulo
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - modulo
---

# Orquestrador — regras e barramento

O pacote `pi/services/orquestrador` recebe comandos, publica ordens de domínio e espelha quatro fontes de estado para telemetria. A biblioteca `_common` centraliza tópicos e o cliente MQTT.

## Peças principais

- `roteador.py`: lógica pura `rotear(dict) → lista de (tópico, payload)`.
- `ComandoRoteavel`: classe abstrata das regras; subclasses Motor, Voz, ParadaEmergencia, Rota e Wifi.
- `_ROTAS`: tabela de despacho por `tipo`; o formato compacto `cmd` é normalizado antes.
- `main.py`: integra essa lógica ao MQTT e espelha os tópicos selecionados.
- `_common/topics.py`: nomes canônicos. `mqtt_client.py`: publicação/assinatura, reconexão e heartbeat.

## Contrato efetivo

Direções: F frente, B trás, L esquerda, R direita, S parar. A intensidade padrão é 60. A forma contínua usa `acao=mover`, `linear` e `angular` entre -1 e 1. Cada eixo ausente vira zero individualmente; um eixo válido ainda pode mover o robô. Não assumir que qualquer mensagem incompleta implica parada total.

O roteador de rota valida mensagens individuais, mas não armazena nem executa o percurso. Voz e rota têm tópicos de saída sem consumidor funcional encontrado para falar/navegar. O Wi-Fi é encaminhado para validação e aplicação no serviço próprio.

Os testes presentes cobrem regras de despacho e normalização. A docstring promete tolerância a mensagens inválidas, mas isso não substitui validação de todas as entradas possíveis. Esta tarefa não foi uma auditoria exaustiva de robustez do software.

[[wiki/api/contrato-mqtt]] · [[wiki/decisoes/registro]] · [[wiki/modulos/motores]].

## Fontes e conferência

- [orquestrador/pi/services/orquestrador/src/orquestrador/roteador.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/orquestrador/src/orquestrador/roteador.py)
- [orquestrador/pi/services/orquestrador/src/orquestrador/main.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/orquestrador/src/orquestrador/main.py)
- [orquestrador/pi/services/_common/src/robo_common/mqtt_client.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/_common/src/robo_common/mqtt_client.py)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

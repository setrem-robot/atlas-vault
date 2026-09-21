---
title: "Motores — comando, cálculo e acionamento"
tipo: modulo
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - modulo
---

# Motores — comando, cálculo e acionamento

## Três responsabilidades

| Camada | Arquivo | Papel |
|---|---|---|
| Cálculo | `cinematica.py` | Velocidades de cada lado, saturação, conversão de ações e rampa |
| Acionamento | `acionamento.py` | Interface abstrata, implementação simulada e STEP/DIR/EN |
| Serviço | `main.py` e `vigia.py` | MQTT, timeout, estado, coordenação por lock e encerramento |

## Parâmetros do código

- `MOTORES_BACKEND=auto`: tenta hardware e pode cair para simulação. O log precisa ser consultado para saber o backend real.
- `COMANDO_TIMEOUT_S=1.0`: silêncio de movimento aciona parada; 0 desliga o vigia.
- `ACELERACAO=3.0`: rampa em unidades normalizadas por segundo; não é aceleração medida em m/s².
- `TICK_S=0.05`: laço de atualização a cada 50 ms.
- `MOTOR_ESQ_INVERTIDO`/`MOTOR_DIR_INVERTIDO`: ajustes de sentido conforme montagem.

Parada explícita e emergência zeram a rampa imediatamente no software. O backend real remove pulsos e desabilita os drivers. Tempo/distância física até parar dependem da montagem e não foram medidos aqui.

## Pinagem declarada, a confirmar na montagem

| Sinal | Esquerdo | Direito |
|---|---|---|
| STEP | BCM 20 | BCM 19 |
| DIR | BCM 21 | BCM 26 |
| EN | BCM 16 | BCM 13 |

São números BCM usados pelo código, não posições físicas do conector. O backend trabalha com duty de 50% para os pulsos; EN em LOW habilita e HIGH desabilita. A conferência elétrica e do driver/motor instalado é parte do ensaio de hardware.

## O que significa a telemetria

`robo/motores/status` contém `acao`, `velocidade`, `esquerda` e `direita`, e pode trazer `motivo`. Representa o alvo calculado. Estados iguais não são republicados a cada tick. Não há posição por encoder ou velocidade medida nesse serviço.

## Estado de validação

Há testes para cinemática, serviço, vigia e concorrência. O README registra que o motor real ainda não foi acionado com esse código. A próxima evidência deve registrar versão, backend efetivo, sentido de cada roda, parada por silêncio e observação física. [[wiki/planejamento/validacao]] e [[wiki/seguranca/index]].

## Fontes e conferência

- [orquestrador/pi/services/motores/src/motores/acionamento.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/motores/src/motores/acionamento.py)
- [orquestrador/pi/services/motores/src/motores/main.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/motores/src/motores/main.py)
- [orquestrador/pi/services/motores/src/motores/cinematica.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/motores/src/motores/cinematica.py)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

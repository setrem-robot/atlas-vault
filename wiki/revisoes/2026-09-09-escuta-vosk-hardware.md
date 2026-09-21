---
title: "Escuta em streaming — medição no Raspberry Pi"
tipo: experimento
estado_documental: validado_no_hardware
atualizado: 2026-09-09
tags:
  - atlas
  - escuta
  - desempenho
  - hardware
---

# Escuta em streaming — medição no Raspberry Pi

Data: **2026-09-09** · Executor: Claude Opus 5 por SSH · Protocolo: comparação dos dois reconhecedores sobre o mesmo PCM, no próprio robô.

Cobre [[wiki/decisoes/registro|DEC-08]]. Distingue o que foi **validado no hardware** do que continua **pendente de ensaio com voz humana** — a separação exigida por [[CONTEXTO-IA]].

## Ambiente e versão

| | |
|---|---|
| Hardware | Raspberry Pi 5, 8 GB, sem cooler ativo |
| Temperatura durante o ensaio | 54,3 °C · `throttled=0x0` |
| RobotEye | branch `producao`, `43a6fe0` (merge de `e1b26d7`) |
| Reconhecedores | `faster-whisper base` (int8, 3 threads) e `vosk-model-small-pt-0.3` (52 MB) |
| Origem do áudio | **sintetizado no próprio Pi** com a voz `dii` (Piper) — não é voz humana |

## Hipótese e critério de aceitação

O Whisper só começa a reconhecer depois da frase inteira; o Vosk decodifica durante a fala. A hipótese é que a espera **após o último som** caia de aproximadamente dois segundos para perto de zero, e o critério é que a diferença apareça no mesmo áudio, entregue aos dois motores.

## Procedimento

Cada frase foi sintetizada uma vez e o mesmo PCM a 16 kHz entregue aos dois. No Vosk o cronômetro soma apenas o custo dos blocos **posteriores ao fim da fala** — é o que a pessoa espera de fato. No Whisper, a transcrição inteira, que só pode começar ali.

## Resultado observado

**Passou** quanto ao tempo.

| Frase dita | Whisper `base` | Vosk pequeno | Ganho |
|---|---:|---:|---:|
| "Atlas, quantos alunos tem o curso de engenharia de computação?" (3,73 s) | 2293 ms | 76 ms | **2217 ms** |
| "Atlas, quanto é dois mais dois?" (2,18 s) | 1924 ms | 295 ms | **1629 ms** |
| "Atlas" (0,79 s) | 1727 ms | 742 ms | 985 ms |

Confirma a estimativa de ~1,9 s que motivou a troca: medido, o Whisper custa **1,7 a 2,3 s de silêncio** depois de a pessoa parar de falar.

Verificado também no serviço em execução, após a troca de `ROBOTEYE_HEARING_BACKEND`:

- o microfone **abriu** — `escutando pelo microfone (vosk, decodificando enquanto voce fala)`;
- o vigia de captura **não disparou** em 45 s de observação, ou seja, há áudio chegando de forma contínua;
- CPU do serviço em **37,6 %**, contra os ~105 % do defeito de reenumeração USB descrito em [[wiki/estado/divergencias]];
- `systemctl is-active` = `active`.

## Limites e conclusão

**O que este ensaio prova:** que a diferença de tempo é real no hardware de produção, que ela vem da arquitetura do reconhecedor e não de ajuste, e que o caminho do Vosk abre o microfone desta placa — o que não acontecia antes da correção de negociação de taxa.

**O que este ensaio não prova, e é o ponto mais importante:** nada sobre precisão com voz humana. O áudio veio da voz sintética do próprio robô, e **os dois motores transcreveram mal**:

| Dito | Whisper | Vosk |
|---|---|---|
| "Atlas, quantos alunos tem o curso…" | `Atos, quando os amunos têm um curso…` | `a todos quando os alunos têm um curso…` |
| "Atlas" | `Atos.` | `atuais` |

Nenhum dos dois reconheceu a palavra de despertar nesse áudio. Isso indica que **a voz `dii` é entrada ruim para reconhecimento**, não que os motores sejam ruins: num ensaio anterior em outra máquina, com voz sintética diferente, o Vosk devolveu `quantos alunos têm o curso de engenharia de computação` corretamente.

**Ação seguinte:** ensaio com voz humana diante do microfone do robô, observando `journalctl -u roboteye -f`. É o único jeito de saber se a Atlas é acordada de forma confiável. Registrar em [[wiki/planejamento/validacao]].

**Risco a vigiar:** se a palavra "atlas" não for reconhecida com frequência, o sintoma no log é `ouvi '<pergunta sem o nome>', mas nao era comigo` — que aponta para o gatilho e não para o reconhecimento. Nesse caso as saídas são voltar ao Whisper (uma variável) ou tolerar quase-acertos do nome em `hearing/gatilho.py`.

## Fontes

- [RobotEye/src/roboteye/hearing/vosk_ears.py](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe0/src/roboteye/hearing/vosk_ears.py)
- [RobotEye/tests/test_vosk.py](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe0/tests/test_vosk.py)
- PRs [#19](https://github.com/setrem-robot/atlas_ai_v2/pull/19) e [#20](https://github.com/setrem-robot/atlas_ai_v2/pull/20)
- [[wiki/diario/2026-09-09]]

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

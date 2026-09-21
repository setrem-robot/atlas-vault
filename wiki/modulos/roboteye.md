---
title: "RobotEye — IA, escuta, voz, face e painel"
tipo: modulo
estado_documental: revisado
atualizado: 2026-09-21
tags:
  - atlas
  - modulo
---

# RobotEye — IA, escuta, voz, face e painel

**Pasta:** `RobotEye` · **Repo:** `atlas_ai_v2` · **Branch local:** `producao`.

## Mapa interno

| Área em `src/roboteye` | Papel |
|---|---|
| `core/assistant.py`, `core/events.py` | Coordenação da conversa e eventos de estado |
| `llm` | Ollama, modelo echo de teste, memória de conversa, persona e reserva |
| `hearing` | Microfone, gatilho de chamada, Vosk e Whisper |
| `speech` | Síntese, player, acabamento de áudio, fila de fala e reserva |
| `face` | Estado visual, animação, expressões, formas e renderização |
| `web` | Página de configuração/conversa, estado do Pi e comandos |
| `ble` | NUS no Raspberry Pi e entrega ao broker |
| `config.py`, `setup_wizard.py` | Configuração centralizada e assistente inicial |
| `diagnostics.py`, `memoria.py`, `radio.py` | Diagnóstico de dependências, RAM e conectividade |
| `voice_catalog.py`, `voices.py` | Catálogo e escolha de vozes |

## IA e voz atuais

O código conversa com Ollama e permite trocar de backend. O README descreve uso de `qwen3:8b` em máquina da rede e `gemma3:1b` como reserva local. O padrão da dataclass em `config.py` é `llama3.2:1b`; esses valores não são a configuração ativa do robô. O `.env` real não foi copiado nem usado como prova de implantação.

Os motores de voz incluem Edge, Piper, Kokoro e null. O modo descrito no README privilegia voz online e reserva Piper. A síntese e a resposta trabalham por frases/blocos para reduzir espera. A face reage aos eventos e à amplitude de áudio.

## Mudança mais recente da escuta

Em 09/09, `a88c2dd` tornou Vosk o padrão e `e1b26d7` acrescentou silêncio antes da primeira palavra. Whisper continua disponível. Essas mudanças estão em `main` e no conteúdo de `producao` observado.

O código também inclui sinais sonoros de escuta, finalização por silêncio, controle de concorrência entre escuta e inferência, correções de contexto e `keep_alive`. Há recuperação da captura/saída quando o dispositivo de áudio USB reaparece.

## Atualização 2026-09-21 — voz corrigida e switch de IA

Implantado e verificado no Pi (`producao` `a5c73c5`). Ver [[wiki/historico/registro-de-trabalho#2026-09-21 — Conserto da voz e da ponte BLE, switch IA local/nuvem no app|registro de 21/09]].

- **Voz voltou a sair.** A conversão camelCase havia renomeado nomes de bibliotecas externas: `miniaudio.decode(sampleRate=…)` (edge/francisca) e `PiperVoice.load(configPath=…)` + `chunk.sampleRate`/`sampleWidth` (Piper). Com os dois motores quebrados o robô ficava mudo. Restaurados os nomes snake das libs; o `AudioFormat` do projeto segue camelCase.
- **Ponte BLE corrigida.** `mqtt.Client(clientId=…)` → `client_id=` em `ble/mqtt.py` e `web/comandos.py`; o serviço saiu do crash-loop.
- **Switch de IA local/nuvem** (override manual sobre a troca automática por queda): `llm/fallback.py::FallbackLLMClient.definirModo`, novo `core/controle.py::ControleRemoto` (assina `robo/comando/entrada` e aplica `{"tipo":"ia","modo":…}`), `Assistant.definirModoIa`. "nuvem" = Ollama da máquina do usuário (`qwen3:8b`); "local" = Ollama do Pi (`gemma3:1b`). Voz independente do switch. Suíte **811** verde.

## Integrações existentes e ausentes

A ponte BLE publica comandos e o painel usa MQTT para observar/enviar comandos. Portanto, dizer que “o RobotEye não usa MQTT” seria incorreto. **Desde 21/09 a face também consome do barramento:** `core/controle.py` assina `robo/comando/entrada` e trata `{"tipo":"ia",…}` — é o primeiro comando do app que o RobotEye consome diretamente, sem depender do roteador do orquestrador. O que ainda falta é conectar a conversa à telemetria e consumir `robo/voz/falar` para o app pedir fala.

O painel escuta `robo/comando/entrada`; a indicação de comando recebido não é medição do motor. Seus controles e a configuração de PIN pertencem à rede local do robô; não equivalem à API pública da nuvem.

## Números relatados, não medidos nesta sessão

O README relata Pi 5 de 8 GB, OS Lite, display 800×480, face em 30 FPS e medições de arranque/CPU/temperatura. O próprio texto reconhece conflito nas medições de RAM da face. Preservamos essa ressalva em [[wiki/estado/divergencias]], sem transformar medições antigas em promessa de desempenho atual.

## Como melhorar

Definir perguntas de referência, registrar transcrição e tempo até primeiro áudio, avaliar respostas corretas sobre a SETREM, testar ausência de rede e manter a face responsiva sob carga. [[wiki/planejamento/validacao]] detalha um ensaio proposto.

## Fontes e conferência

- [RobotEye/README.md](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/README.md)
- [RobotEye/src/roboteye/config.py](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/src/roboteye/config.py)
- [RobotEye/src/roboteye/hearing/vosk_ears.py](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/src/roboteye/hearing/vosk_ears.py)
- [RobotEye/src/roboteye/web/comandos.py](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/src/roboteye/web/comandos.py)
- [RobotEye/src/roboteye/core/assistant.py](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/src/roboteye/core/assistant.py)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

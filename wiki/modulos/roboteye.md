---
title: "RobotEye — IA, escuta, voz, face e painel"
tipo: modulo
estado_documental: revisado
atualizado: 2026-11-22
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

## Realidades práticas no Pi (banca, 2026-10-16)

O que de fato roda bem no Raspberry Pi 5, apurado preparando a demonstração. Ver
[[wiki/historico/registro-de-trabalho#2026-10-16 — Preparação do robô para a banca (Interdisciplinar IV)|registro de 16/10]].

- **Chat de texto pela página web.** `web/conversa.py` (rota `/api/conversar`) é
  uma entrada de texto para o `Assistant`: digita-se na página `:8080` e a Atlas
  **responde falando**, com a face reagindo — sem depender do microfone. É a
  interface usada na banca; a página foi redesenhada com o chat no centro.
- **Voz confiável = local.** A voz online `francisca` (edge-tts) sofre **403 da
  Microsoft** (endpoint bloqueado). A voz local **`dii`** (Piper `pt_BR-dii-high`)
  é o padrão que sempre funciona: offline, instantânea, robótica. A `dii` é a
  melhor Piper PT do catálogo; `faber` (medium) é a outra local.
- **Modelo local:** **`gemma3:1b`** é o único prático no Pi. O **`gemma3:4b`**
  estoura o timeout de 60 s na CPU — bom em qualidade, inviável em velocidade aqui.
- **Persona × modelo pequeno.** A `atlas.md` grande (~2039 tokens) confunde o 1 B
  e torna o cold-start lento (~58 s). Uma persona **enxuta e directiva**
  (`persona/atlasdemo.md`) faz o 1 B acertar nome, autoria, uso de IA e localização.
- **Aquecimento:** a saudação não aquece o LLM; a 1ª pergunta fria custa ~40 s,
  quente ~6–8 s. `keep_alive=30m` mantém carregado. O `Assistant` responde **só a
  última** de uma rajada (barge-in).
- **IA "nuvem" do robô = um Ollama numa máquina da rede** (`KerlonPC`), não um
  serviço de nuvem; hoje desligada. O LARCC hospeda a telemetria, **não** um LLM.

## Atualização 2026-11-22 — LLM treinado e face com humor

Substitui o item "Modelo local" acima. Fonte: `RobotEye/TREINO-E-OTIMIZACAO.md`
(`producao` `73c37a0`). Detalhes em
[[wiki/historico/registro-de-trabalho#2026-11-22 — LLM treinado (atlas-qwen), rodadas automáticas e face com humor|registro de 22/11]].

- **LLM:** `atlas-qwen-r2` — Qwen2.5-1.5B-Instruct com LoRA (Unsloth, treinado no
  WSL do PC), q4_K_M no Ollama do Pi 5. Prova de 72 perguntas: **64/72**, contra
  42/72 do `qwen2.5:1.5b` base e 34/72 do `gemma3:1b`. Conversa: mediana 2,5 s até
  começar a falar; 1º texto mediana 0,4 s. O `atlas-qwen-r3` empatou (64/72) e
  não entrou.
- **Treino contínuo:** `scripts/orquestrar-treinos.sh` (professor `qwen3:8b` →
  juiz → dataset → LoRA → prova no Pi → troca só se ganhar e mantiver mediana
  ≤ 2,5 s). Scripts em `scripts/treino/` (`professor.py`, `dataset.py`,
  `treinar.py`, `avaliar.py`, `instalar-no-pi.sh`).
- **Face com humor:** `core/humor.py` (palavras-chave, sem modelo) → HAPPY, DIZZY,
  LAUGH, TIRED pela fala; ANGRY ao xingamento e RAGE no terceiro seguido
  (`face/app.py`).
- **Escuta:** `vosk-pt-atlas` (grafo refeito no PC; 79% de frases inteiras certas
  no Pi, 537 MiB de pico).

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

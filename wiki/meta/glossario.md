---
title: "Glossário — os termos que aparecem em tudo"
tipo: referencia
estado_documental: revisado
atualizado: 2026-11-22
tags:
  - atlas
  - referencia
  - glossario
---

# Glossário

> [!info] Para que serve
> Quase todo documento deste projeto usa dez ou quinze termos sem explicar.
> Esta nota explica cada um **no contexto da Atlas** — não no geral. Quando um
> termo tiver uma pegadinha específica daqui, ela está marcada.

---

## As três partes do robô

| Termo | O que é |
|---|---|
| **RobotEye** | O repositório `atlas_ai_v2`, apelidado de "a cara". Face animada, voz, IA e escuta. É o único que está instalado no Pi hoje. |
| **orquestrador** | O repositório do "corpo": motores, GPS, Wi-Fi e a nuvem. **Cuidado:** a classe `Assistant` do RobotEye também "orquestra" (liga IA + memória + voz), mas não tem relação com este repositório. |
| **app** | O repositório `aplicativo`, o "controle". Flutter, roda no celular. |
| **Atlas** | O robô inteiro, e também o nome que o desperta quando alguém fala com ele. |

---

## Como as peças conversam

| Termo | O que é | Onde aparece |
|---|---|---|
| **MQTT** | Um correio de mensagens. Quem tem algo a dizer *publica* num assunto; quem se interessa *assina* esse assunto. Ninguém precisa conhecer o outro. | Todo o tráfego dentro do Pi |
| **tópico** | O endereço de um assunto no MQTT, escrito com barras: `robo/motores/comando`. | [[wiki/api/contrato-mqtt]] |
| **broker** | O programa que entrega as mensagens. Aqui é o **Mosquitto**, em `127.0.0.1:1883` — só escuta de dentro do Pi. | [[wiki/modulos/orquestrador]] |
| **retido** *(retained)* | Mensagem que o broker guarda: quem assinar depois recebe a última na hora, sem esperar a próxima. Usado em posição de GPS e estado de Wi-Fi. | |
| **bridge** | Ponte entre dois brokers. Copia só `robo/telemetria/#` do Pi para a nuvem — é o filtro do que sai da rede local. | [[wiki/modulos/nuvem]] |
| **BLE** | Bluetooth Low Energy. Substituiu o Bluetooth clássico porque o iOS nunca permitiu SPP a aplicativos de terceiros. | [[wiki/decisoes/registro\|DEC-01]] |
| **NUS** | *Nordic UART Service*. Um padrão de BLE que finge ser um cabo serial. Os UUIDs dele são contrato: mudar de um lado sem o outro quebra em silêncio. | [[wiki/api/contrato-mqtt]] |
| **SPP** | *Serial Port Profile*, o Bluetooth clássico que o projeto **abandonou**. Aparece nos relatórios antigos. | [[wiki/historico/orquestracao-anterior]] |
| **NDJSON** | Um JSON por linha. Formato dos comandos: a quebra de linha marca onde uma mensagem acaba. | |

---

## Conversa: ouvir, pensar, falar

| Termo | O que é | Pegadinha daqui |
|---|---|---|
| **STT** | *Speech-to-Text* — transformar voz em texto. | |
| **Vosk** | Motor de STT que reconhece **enquanto a pessoa fala**. É o padrão atual. | Rápido (85 ms) e impreciso: ouve "classe" no lugar de "Atlas" |
| **Whisper** | Motor de STT que só começa **depois** da frase inteira. | Entende bem, mas custa ~2 s de silêncio depois de cada pergunta |
| **TTS** | *Text-to-Speech* — transformar texto em voz. | |
| **Piper** | Motor de voz **local**. A voz `dii` é dele. | Rápido (~500 ms), sem internet |
| **Edge TTS** | Motor de voz **online**, da Microsoft. A voz `francisca` é dele. | Mais bonita, mas ~1,4 s e depende de internet |
| **LLM** | *Large Language Model* — o modelo que escreve a resposta. | |
| **Ollama** | O programa que roda o LLM dentro do Pi. | |
| **atlas-qwen-r2** | O modelo em uso desde 22/11: Qwen2.5 de 1,5 bilhão de parâmetros, treinado (LoRA) para ser a Atlas. | 64/72 na prova; ainda erra fatos numéricos |
| **gemma3:1b** | O modelo da banca de 16/10. "1b" = um bilhão de parâmetros. Removido do Pi em 22/11. | Pequeno o bastante para **inventar fatos** — ver [[wiki/estado/divergencias]] |
| **LoRA** | Treino que ajusta só uma parte pequena do modelo, barato o bastante para uma GPU de PC. | |
| **bateria** | `scripts/treino/bateria.py`: conversas de teste corrigidas pelo texto, sem som. | |
| **persona** | O arquivo `persona/atlas.md` que define quem ela é e o que sabe da Setrem. | Ocupa ~1945 dos 4096 tokens de contexto |
| **token** | Pedaço de palavra. É a unidade que o modelo lê e escreve, e o que se mede para saber se algo "cabe". | |
| **num_ctx** | Quanto o modelo consegue ler de uma vez, em tokens. Hoje 4096. | Persona + histórico + resposta precisam caber juntos |
| **keep_alive** | Quanto tempo o modelo fica na memória sem uso. Hoje `-1s` = para sempre. | Se ele descarregar, reler a persona custa ~56 s |
| **palavra de despertar** | O nome que faz o robô entender que é com ele. Vazio faz ele responder a tudo. | |

---

## Movimento

| Termo | O que é |
|---|---|
| **NEMA 23** | O padrão de tamanho dos motores de passo usados. Os do projeto entregam 30 kgf·cm nominais. |
| **TMC2209** | O driver que traduz pulsos em corrente para o motor. **Ponto a conferir:** entrega ~1,4 A, e um NEMA 23 desse torque costuma pedir 2,8–3,0 A. |
| **STEP/DIR** | Como o Pi fala com o driver: um pulso em STEP = um passo; o nível em DIR = o sentido. |
| **microstep** | Dividir cada passo em frações (aqui 1/8) para o movimento ficar suave e silencioso. |
| **rampa** | Subir e descer a velocidade aos poucos. Sem ela o motor perde passo e o driver esquenta. |
| **parada de emergência** | Corta o movimento ignorando a rampa. Protegida para que nenhum comando atrasado a ultrapasse. |

---

## Infraestrutura

| Termo | O que é |
|---|---|
| **Raspberry Pi 5** | O computador do robô. 4 núcleos, 8 GB. **Sem relógio de bateria** (a hora salta ao ligar) e **sem cooler**. |
| **systemd** | Quem liga os serviços junto com o sistema e os reinicia se caírem. |
| **unidade** *(unit)* | Um serviço no systemd: `roboteye.service`, `mosquitto.service`. |
| **ALSA** | A camada de som do Linux. `dmix` deixa vários programas usarem a mesma caixinha; `dsnoop` faz o mesmo com o microfone. |
| **TimescaleDB** | O banco da nuvem, feito para séries no tempo — trajeto, bateria, posição. |
| **hypertable** | Tabela do TimescaleDB partida por data automaticamente. Aqui: `telemetria`. |
| **FastAPI** | O que serve a API de leitura da nuvem. **Os relatórios antigos falam em Quarkus** — foi substituído. |
| **Shorebird** | Publica correções no app sem passar pela loja. |
| **branch `producao`** | O ramo que o robô roda. Receber um merge nele **não prova** que o Pi já puxou. |

---

## Vocabulário do vault

| Termo | O que quer dizer aqui |
|---|---|
| **validado no hardware** | Rodou no robô e foi medido |
| **reproduzido em software** | Passou em teste, sem tocar no hardware |
| **análise estática** | Lido no código, não executado |
| **planejado** | Ainda não existe |
| **AT-01 … AT-16** | Os achados da [[wiki/revisoes/2026-09-09-revisao-tecnica\|revisão técnica]], com IDs estáveis |
| **DEC-01 … DEC-11** | As decisões de arquitetura, em [[wiki/decisoes/registro]] |
| **T-CONTROLE, T-IA** | Protocolos de ensaio em [[wiki/planejamento/validacao]] |
| **coleta** | Um retrato datado de algo (Git, árvore de arquivos). Não é telemetria atual. |

---
[[INICIO|Início]] · [[wiki/index|Mapa da documentação]] · [[wiki/meta/fontes|Fontes e limites]]

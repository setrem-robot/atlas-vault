---
title: "Registro de trabalho"
tipo: historico
estado_documental: em_uso
atualizado: 2026-11-22
tags:
  - atlas
  - historico
---

# Registro de trabalho

Exigido por `AGENTS.md`: cada tarefa que altera software, implanta ou valida deixa uma linha aqui, com escopo, branch e evidência. Entradas mais recentes no topo.

Esta nota não existia até 09/09; entradas anteriores a essa data estão em [[wiki/historico/linha-do-tempo]] e [[wiki/diario/2026-09-09]].

---

## 2026-11-22 — LLM treinado (atlas-qwen), rodadas automáticas e face com humor

**Escopo:** trocar o LLM genérico do Pi por um modelo treinado para ser a Atlas,
automatizar as rodadas de treino e ligar as expressões da face ao que se fala.
**Repositório:** `atlas_ai_v2` (`producao`, PRs #26–#36, último `73c37a0`).
**Fonte primária:** `RobotEye/TREINO-E-OTIMIZACAO.md`, `scripts/orquestrar-treinos.sh`,
`scripts/treino/`, `src/roboteye/core/humor.py` e o log do orquestrador.

**Regra:** o Pi não treina nada. O PC (RTX 4060, WSL) treina e constrói; o Pi só
recebe o modelo pronto e é onde a prova roda.

**LLM do robô (validado no hardware):** base **Qwen2.5-1.5B-Instruct**, ajustado
por **LoRA** (Unsloth, rank 32, no WSL do PC), quantizado **q4_K_M** e servido pelo
Ollama do Raspberry Pi 5. Prova de 72 perguntas inéditas, corrigida sozinha, no Pi:

| modelo | certas | observação |
|---|---|---|
| `gemma3:1b` (base) | 34/72 | antigo modelo da banca; misturava fatos |
| `qwen2.5:1.5b` (base) | 42/72 | robô usou na madrugada de 22/11 |
| **`atlas-qwen-r2`** (14.964 exemplos) | **64/72 (89%)** | **em uso desde 22/11 de manhã**; conversa mediana 2,5 s até falar; 1º texto mediana 0,4 s; release `atlas-qwen-r2` |
| `atlas-qwen-r3` (21.588 exemplos, ~1h45 de LoRA) | 64/72 | empate: identidade 6/7, fato 11/11, data 3/3, não-sei 7/7, aula 20/22, papo 12/12, conta 2/3, lixo 0/4, memória 3/3 — **não substituiu** o r2 |

**Rodadas automáticas** (`scripts/orquestrar-treinos.sh`, no WSL, até alguém parar):
professor (`qwen3:8b` no Ollama do Windows gera *aula*, *comuns*, *papo*, *seguida*,
*paráfrase* e *web*) → juiz (só nota 4–5 entra) → dataset (só treina se crescer
≥ 5%) → LoRA do zero → instala no Pi → prova → troca só se **ganhar** do modelo em
uso **e** mantiver a conversa com mediana ≤ 2,5 s. Cada rodada gera uma **volta**
nova de perguntas (`VOLTAS = rodada − 1`) para o professor não saturar. A tarefa
*comuns* gera perguntas do dia a dia com **quatro respostas variadas** cada, para
o modelo aprender a gerar a resposta em vez de decorar. Em 22/11 à tarde a
**rodada 4** já gerava dados.

**Bug corrigido (PR #34):** o `transformers` 5 grava `rope_theta` só em
`rope_parameters`; o conversor do Ollama procura no topo do `config.json` e, sem
ele, assume 10000 — o Qwen2.5 importado assim gerava lixo (primeira tentativa do
r2: 10/72). `treinar.py` agora copia `rope_theta` para o topo.

**Face com humor (PR #36, reproduzido em software):** `core/humor.py` escolhe a
expressão por palavras-chave sobre o texto que já existe — custo zero no Pi e sem
atrasar a fala. Resposta alegre → HAPPY; "não entendi" → DIZZY; piada → LAUGH;
"infelizmente" → TIRED. Xingamento do usuário → ANGRY; três seguidos → RAGE. Os
dados de treino também ensinam a Atlas a responder **brava e firme** a
xingamentos, **sem xingar de volta**.

**Também em 21–22/11 (PR #26, medido no Pi):** escuta `vosk-pt-atlas` (frase
inteira certa 25% → 79%, carga 27,6 s → 0,5 s) e conversa reaquecida a cada turno
(RAM do `roboteye` 3249 → 821 MiB). Números e como refazer em
`RobotEye/TREINO-E-OTIMIZACAO.md`.

---

## 2026-10-16 — Preparação do robô para a banca (Interdisciplinar IV)

**Escopo:** deixar a Atlas pronta para a apresentação de banca: mostrar a **voz
saindo**, o **conhecimento sobre a SETREM** e a ideia de **IA local/nuvem**.
Como o microfone não ouve bem ("Atlas, qual seu nome" não era reconhecido), a
decisão foi **contornar a escuta** e demonstrar por um **chat de texto** — a
pessoa digita e a Atlas responde falando. Tudo ajustado ao vivo no Pi por SSH.

**Agente:** Claude Opus 4.8. **Repositório:** `atlas_ai_v2` (`producao`). **Pi:**
`atlas.local` / `192.168.1.111` / Tailscale `100.110.189.21`.

**Interface da demo — página web "Conversar".** O RobotEye já serve, junto com a
face, uma página em `http://atlas.local:8080` (PIN) com uma caixa de conversa
(`web/conversa.py`, rota `/api/conversar`): o texto vai ao `Assistant`, a resposta
sai pela **voz** e a face reage. **É a tela que vai ser apresentada.** Ela foi
**redesenhada** (commit `10cdf6b`) com o chat como protagonista — balões você/Atlas
com os olhos, indicador "pensando…", responsiva e leve — e **toda a configuração
recolhida** num `<details>` "Ajustes avançados" (também evita salvar sem querer,
que havia zerado o `.env` por engano: a página reescreve `OLLAMA_HOST`, `VOICE`,
`LLM_MODEL` e `PERSONA` ao salvar).

**Descobertas e decisões (o que de fato roda bem no Pi):**
- **Voz:** a voz online bonita `francisca` (edge-tts) está com **403 da Microsoft**
  — o endpoint foi bloqueado; nem a versão nova (7.2.8) resolve. Trocado o padrão
  para **`dii`** (Piper `pt_BR-dii-high`, já baixada): **local, instantânea, sem
  internet, sem 403**. É robótica, mas confiável — o que importa num demo.
- **Modelo de IA local:** **`gemma3:1b`** é o único viável no Pi. O **`gemma3:4b`**
  foi baixado e testado, mas **estoura o timeout de 60 s** na CPU do Pi 5 — pesado
  demais. Ficou no disco para um hardware futuro.
- **Persona:** a `atlas.md` original (~2039 tokens) **confunde o modelo de 1 B** e
  deixa o cold-start em ~58 s. Criada uma persona **enxuta e directiva**
  `persona/atlasdemo.md`: com os fatos ditos de forma explícita ("Seu nome é
  Atlas", "feita por alunos do curso de Engenharia de Computação da SETREM", "você
  funciona com inteligência artificial"), o 1 B passou a **acertar** nome, quem a
  construiu, uso de IA e localização. A `atlas.md` ficou **intacta**.
- **IA nuvem:** aponta para `KerlonPC.local` (um PC da rede, **desligado** agora).
  O LARCC **não** tem Ollama (só a telemetria). Então, para a banca, ficou **só a
  IA local**; a nuvem é explicada pelos slides. "Nuvem" aqui = um Ollama numa
  máquina da rede, não um serviço de nuvem.
- **Cold-start:** a saudação (fixa, sem LLM) não aquece o modelo; o `warmUp` roda
  em segundo plano. A 1ª pergunta com o cache frio leva ~40 s; **quente, ~6–8 s**.
  Por isso: **aquecer com uma pergunta ~1 min antes** de apresentar. `keep_alive`
  posto em 30 m para não esfriar. O `Assistant` responde **só a última** quando
  recebe várias de uma vez (barge-in) — perguntar uma de cada vez.

**Config final do demo (`.env`, tudo local, `atlas.md` e `.env.bak-demo` de
backup no Pi):** `OLLAMA_HOST=127.0.0.1` · `LLM_MODEL=gemma3:1b` ·
`LLM_FALLBACK_HOST=` (vazio) · `PERSONA=atlasdemo` · `VOICE=dii` ·
`HEARING_ENABLED=false` · `SAUDACAO` de auto-apresentação ·
`LLM_MAX_TOKENS=110` · `LLM_KEEP_ALIVE=30m`. Áudio: **USB PnP Sound Device**
(card 0, controle `Speaker`) em 90 %.

**Evidência (testado ao vivo):** "Qual é o seu nome?" → *"Eu sou Atlas."*; "Quem
te construiu?" → *"Eu fui feita por alunos do curso de Engenharia de Computação
da SETREM…"*; "Você usa inteligência artificial?" → *"Sim, eu uso inteligência
artificial."* — todas faladas pela voz `dii`, ~6–8 s com o modelo quente.

**Relacionado:** foi montada também a **apresentação de banca** em PDF
(`Apresentacao-Atlas.pdf`, refeita com o template visual da equipe e todos os
subsistemas). Ver [[wiki/modulos/roboteye]].

---

## 2026-10-02 — Nuvem migrada do `.150` para a VM do LARCC

**Escopo:** a pedido do usuário, mover **toda a pilha Atlas** (mosquitto, TimescaleDB, ingestor, API, Caddy com landing/painel/completo e o túnel Cloudflare `atlas-api`) do servidor de casa `.150` para a VM do LARCC, preservando o que já rodava lá e todo o banco.

**Agente:** Claude Opus 5.5. **Hosts:** LARCC `root@atlas` (Ubuntu 24.04, 2 vCPU/8 GB, acesso por Tailscale `100.118.95.115`); `.150`; Pi `atlas@atlas.local` (agora `192.168.1.111`).

**O que havia no LARCC:** uma versão antiga da mesma pilha (`/root/setrem-robot/cloud`, só mosquitto/banco/ingestor) com **983 registros** antigos (jun–set) e uma tabela `gps_location` vazia. Mesmas portas (1883/5432) e nomes de container — não coexistem com a nova.

**Feito:**
- Backup do banco antigo do LARCC em `/root/backups/` (`pg_dump -Fc`, roles, pasta `cloud`, export COPY). Pilha antiga parada com `docker compose down` **sem `-v`** (volumes `cloud_*` preservados).
- Pilha do `.150` copiada como estava (com `.env`, credenciais do túnel e `passwd` do mosquitto) para **`/root/docker-stacks/atlas`** no LARCC; imagens `api`/`ingestor` reconstruídas lá.
- Banco migrado por `COPY` (independe da versão do Timescale: `.150` 2.30, LARCC novo): 25 329 do `.150` + 983 antigos do LARCC + `gps_location`. Depois, delta de 40 registros que o Pi mandou ao `.150` entre o boot e a troca, inserido sem duplicar (chave ts/tipo/tópico). Total no corte: **26 355**.
- Túnel: `cloudflared-cloud` subiu no LARCC (4 conexões registradas) e só então foi parado no `.150` — sem queda do domínio. Os outros túneis do `.150` (odysseus/tokens, crono) não servem nada do Atlas e não foram tocados.
- Pi: **Tailscale instalado** (`atlas-pi`, `100.110.189.21`); bridge `/etc/mosquitto/conf.d/bridge.conf` repontada para `100.118.95.115:1883` (backup em `/etc/mosquitto/bridge.conf.bak-150-20261002`). Agora a telemetria sobe **de qualquer rede**, não só da LAN de casa — resolve o limite citado em 11/09 sem expor porta.
- `.150`: pilha atlas **desativada** — containers e rede removidos (`docker compose --profile tunel down`, sem `-v`); a pasta `~/docker-stacks/atlas` e os volumes `atlas_*` ficaram só como backup frio. Não há unit systemd do Atlas lá. crafty, crono-sw e factorio intactos.
- `orquestrador` `3b9f45e`: README e `docs/setup-cloud.md` ("Como o Pi alcança a VM") atualizados para LARCC + Tailscale. O código implantado no LARCC é o do `.150` (anterior à conversão camelCase de 17/09); difere do repositório só em nomes, não em comportamento.

**Evidência:** pela internet, `atlas.kerlonr.com.br` `/`, `/painel/`, `/completo/`, `/api/saude`, rotas públicas e `/v1/estado` com token → 200; `/api/v1/publico/resumo` com as contagens que só existem no LARCC; `/api/v1/publico/saude` com `idade_s` ≈ 4 s (telemetria ao vivo do Pi via LARCC). Log do broker no LARCC: `Received PUBLISH from atlas.bridge-telemetria`. `docker`/`tailscaled` habilitados no boot; containers `unless-stopped`.

**Rollback:** no Pi, restaurar o `.bak` e reiniciar o mosquitto; no `.150`, `docker compose --profile tunel up -d` (recria os containers sobre os volumes guardados); no LARCC, parar o `cloudflared-cloud`.

## 2026-10-02 — App: telemetria ao vivo

**Escopo:** o app só mostrava dados novos ao fechar e reabrir. Causa: o widget `Carregando` (usado pelas quatro abas) buscava uma vez no `initState`; depois, só com "puxar para atualizar".

**Correção** ([aplicativo #19](https://github.com/setrem-robot/aplicativo/pull/19)): `Carregando.atualizarACada` repete a busca enquanto a aba está à vista — Agora 5 s, Eventos 10 s, Trajeto 15 s, Histórico 30 s. Silenciosa (sem giro; leitura antiga fica até a nova chegar), falha passageira não apaga dados, buscas não se empilham, pausa em segundo plano/outra tela por cima e busca ao voltar. Só Dart → patch OTA na `1.2.4+11`.

**Evidência:** 7 testes de widget novos; `flutter test` 68 verdes, `flutter analyze` limpo. Validação no celular pendente do patch.

---


---

## 2026-09-21 — Conserto da voz e da ponte BLE, switch IA local/nuvem no app

**Escopo:** o robô subia **sem falar** e a ponte com o app estava em reinício-laço; o usuário também pediu um **switch no app** para trocar entre IA local e IA de nuvem. Diagnosticar, corrigir, implementar o switch nos três repositórios e implantar.

**Agente:** Claude Opus 4.8. **Repositórios:** `atlas_ai_v2` (`producao`), `aplicativo` (`main`), `orquestrador` (`main`). **Pi:** `atlas@atlas.local`, por SSH.

**Diagnóstico de partida:** três defeitos, todos da **mesma causa** — a conversão camelCase feita nos repositórios (padronização de nomes, feita antes) renomeou **nomes de bibliotecas externas**, que só quebram no Pi porque essas libs não estão no ambiente de dev e nenhum teste as exercita:

- **Voz muda:** `miniaudio.decode(sampleRate=…)` (deveria ser `sample_rate=`) derrubava a voz de nuvem (francisca/edge), que caía para o Piper — e o Piper também quebrava por `PiperVoice.load(configPath=…)` (→ `config_path=`) e por ler `chunk.sampleRate`/`chunk.sampleWidth` (→ `sample_rate`/`sample_width`). Com os dois motores quebrados, **nenhuma voz saía**. Era esse o "a voz não iniciou / citou o Piper".
- **Ponte BLE em crash-loop:** `mqtt.Client(clientId=…)` (→ `client_id=`, paho), também em `web/comandos.py`. Deixava `roboteye-ble.service` reiniciando sem parar → o app não falava com o robô.
- **Vosk nunca esteve quebrado.** O log mostrava `frase fechada pelo vosk em ~60 ms`; a impressão de "não usa Vosk" era confusão entre Vosk (ouvido/STT) e Piper (voz/TTS).

**Feito — RobotEye** (`atlas_ai_v2` `producao`, commits `189a69e`, `a5c73c5`):

- Corrigidos os quatro nomes externos acima. Os nomes do `AudioFormat` do projeto (`sampleRate`/`sampleWidth`) seguem camelCase — só o que cruza a fronteira da lib voltou ao snake dela.
- **Switch de IA (override manual):** `llm/fallback.py::FallbackLLMClient.definirModo("local"/"nuvem")` por cima da troca automática por queda; novo `core/controle.py::ControleRemoto` assina `robo/comando/entrada` no processo da face e aplica `{"tipo":"ia","modo":…}`; `Assistant.definirModoIa` liga o comando ao LLM; `app.py` monta/encerra o receptor. "nuvem" = Ollama da máquina do usuário (`KerlonPC`, `qwen3:8b`); "local" = Ollama do Pi (`gemma3:1b`). A **voz é independente** do switch. 6 testes novos; suíte **811** verde, ruff+mypy limpos.

**Feito — App** (`aplicativo` `main`): `models/iaModo.dart` (enum, `code` é contrato), `RobotConnection.setIaModo` (manda `{"tipo":"ia",…}` pela ponte BLE, guarda em `SharedPreferences`, reenvia ao conectar), switch na tela de controle. Sem ícone de propósito (ver distribuição abaixo). Testes verdes, `flutter analyze` limpo.

**Feito — Contrato** (`orquestrador` `main`, `a014d7a`): `{"tipo":"ia","modo":"local|nuvem"}` documentado — é o **único comando consumido pela cara (RobotEye)**, não pelo roteador. Ver [[wiki/api/contrato-mqtt]].

**Evidência (implantado e verificado no Pi):** rodei `scripts/atualizar.sh --agora`; face em `a5c73c5`, `roboteye` e `roboteye-ble` `active`. BLE conecta ao broker (`publicando comandos em robo/comando/entrada`), sem o `TypeError`. Voz: `falando: Oi oi, acordei!` sem nenhum erro de kwarg. Switch ponta a ponta: publiquei `{"tipo":"ia","modo":"local"}` e `…"nuvem"` no broker → log da face `switch do app: IA local` / `IA de nuvem`.

**Distribuição do app — release nova exigida** (`aplicativo` `main`, release **`1.2.4+11`**, APK publicado): o patch OTA do Shorebird **estava quebrado desde 16/09** — a feature de telemetria daquele dia adicionou ícones novos e patch não pode mudar a fonte `MaterialIcons` (tree-shaking), mas nenhuma release foi cortada. Desde então nada chegava por OTA. Bumpei a versão `1.2.3+10 → 1.2.4+11`; o `deploy.yml` cortou **release** (APK assinado + GitHub Release), re-sincronizando a base dos patches. O APK entrega de uma vez tudo que estava preso (telemetria) + o switch. **O usuário precisa instalar esse APK uma vez**; depois os patches OTA voltam a fluir. APK: https://github.com/setrem-robot/aplicativo/releases/tag/v1.2.4%2B11

**Limites:** a voz de nuvem (francisca) e a "IA nuvem" (qwen3:8b) só valem com a máquina `KerlonPC` ligada; no momento ela está desligada, então o robô responde pela IA local e a voz usa o motor disponível. GPS segue pendente ([[wiki/modulos/gps]]): módulo GY-GPS6MV2 na UART3 (pinos 21/24), Pi configurado e correto, mas o módulo não emite NMEA — diagnóstico elétrico apontou **falta de energia** (VCC/GND / LED apagado), a confirmar pelo usuário.

---

## 2026-09-11 — Telemetria do Pi no ar (serviço + bridge) e site publicado

**Escopo:** fazer o Raspberry Pi publicar a própria saúde e essa telemetria chegar ao banco na nuvem, com guarda local para quando o LARCC estiver fora de alcance. Fechar também o refactor do site.

**Agente:** Claude Opus 4.8. **Repositório:** `orquestrador`. **Pi:** `atlas@atlas.local` (eth0, `192.168.1.110`). **Servidor:** `192.168.1.150`.

**Diagnóstico de partida:** o Pi **não** mandava telemetria. Só o RobotEye rodava lá; nenhum serviço do `orquestrador` estava instalado e não havia bridge para a nuvem. A infra de store-and-forward já estava **desenhada** no repo (`pi/mosquitto/apt/robo.conf.example` e `.../config/conf.d/bridge.conf.example`), faltava o publicador e a config real.

**Feito:**

- **Novo serviço `pi/services/telemetria`** ([orquestrador #17](https://github.com/setrem-robot/orquestrador/pull/17), mesclado). Publica a cada 30 s em `robo/telemetria/sistema` (QoS 1, sem retain): temperatura, `throttled` (cada bit aberto em booleano), CPU (delta de `/proc/stat`), memória (`MemAvailable`), disco, uptime e Wi-Fi. `coletor.py` são funções puras sobre texto — 21 testes, sem precisar de um Pi. `ts` no payload para o ingestor gravar na hora medida, não na de chegada.
- **Instalação focada no Pi** (só telemetria; **não** subi gps/motores/orquestrador num robô ligado). Venv em `~/orquestrador/pi/.venv`, `robo-common` + `telemetria` editáveis, unit `robo-telemetria.service` com `User=atlas` (o modelo do repo usa `setrem`). Serviço `active`.
- **Store-and-forward configurado no Mosquitto do Pi** (apt, não container): `robo-fila.conf` (`max_queued_messages 100000`, `max_queued_bytes 32 MiB`) e `bridge.conf` (600, fora do git) — bridge `robo/telemetria/# out 1` para `192.168.1.150:1883`, `cleansession false` + `try_private true`. É o `cleansession false` + a fila que guardam o que não subiu e reenviam ao reconectar.

**Evidência (cadeia ponta a ponta validada):**

- Bridge autenticada no `.150`: log do broker remoto — `New bridge connected from 192.168.1.110 as atlas.bridge-telemetria (u'piev')`.
- Ingestor: `Gravado: tipo=sistema topico=robo/telemetria/sistema`. No banco, `SELECT` da `telemetria` traz o payload completo (temp 65 °C, cpu 8.7 %, mem 54 %, `throttled ok`).
- API pública: `/api/v1/publico/resumo` lista `tipo=sistema` com dados **reais** do Pi (última há ~13 s), ao lado dos de demonstração.

**Site** ([orquestrador #18](https://github.com/setrem-robot/orquestrador/pull/18), mesclado): o Caddy serve os estáticos de `site/` e a raiz virou apresentação; o painel ao vivo foi para `/painel/`. `config.js` aponta para `/api` no mesmo domínio (sem CORS, sem token no JS). O refactor **já estava publicado** no `.150` (montado à mão, não é checkout git) e o commit apenas o levou ao repositório. Ao vivo: `https://atlas.kerlonr.com.br/` (200), `/painel/` (200), `/api/...` (200). `testar-site.mjs` OK (10 estados do painel).

**Telemetria enriquecida no mesmo dia** ([orquestrador #19](https://github.com/setrem-robot/orquestrador/pull/19), mesclado): a pedido de "quero saber todas as info do rpi". Sem quebrar o payload, o bloco `cpu` passou a trazer **uso por núcleo** (o "consumo por thread" — os 4 núcleos do Pi 5), `freq_mhz`, `governor` e `voltagem_v`; a memória ganhou swap; e entraram `processos` (rodando/total) e `rede` (rx/tx por interface). 33 testes (eram 21). Validado no banco: `por_nucleo` chega, ex.: `[16.2, 4.3, 8.6, 6.0]` a 2400 MHz / 0,887 V. Campos documentados em [[wiki/api/contrato-mqtt]].

**Painel público de saúde** ([orquestrador #20](https://github.com/setrem-robot/orquestrador/pull/20), mesclado): resposta ao "onde eu vejo essas informações?" — escolha do usuário foi o **painel público**. Nova rota **sem token** `GET /v1/publico/saude` (a saúde do Pi não é sensível, ao contrário do trajeto) devolve a última leitura de `sistema`. O `/painel/` ganhou o cartão **"Saúde do robô"**: temperatura, processador, memória, tempo ligado, **barras de uso por núcleo**, freq/governor/voltagem, swap, disco, rede, e um estado (recente / alerta de subtensão / sem leitura). Deploy no `.150`: rebuild da imagem da API (`build: ./api`, código não é montado) + cópia do site (montado). Ao vivo: `atlas.kerlonr.com.br/api/v1/publico/saude` (200, sem token) e `/painel/` mostrando `por_nucleo`. `testar-site.mjs`: 12 estados. Ver [[wiki/site-e-painel]].

**Tela de análise completa** ([orquestrador #22](https://github.com/setrem-robot/orquestrador/pull/22), mesclado): a pedido de "quero uma tela completa pra análise de absolutamente TUDO". Escolha do usuário: **completa e privada, com token**. Nova página `/completo/` que pede o token uma vez (guardado só no navegador) e usa a API **com token** para mostrar tudo: visão geral por tipo, saúde do Pi com gráficos históricos (temperatura, CPU, por núcleo, memória, frequência), energia, movimento, mapa em **precisão total**, Wi-Fi, e **log cru** filtrável/paginado. Gráficos são SVG desenhados à mão a partir de `/v1/eventos` (até 500/chamada) — alcança campos aninhados como `cpu.por_nucleo` sem agregação no servidor. `401/403` corta a sessão. Sem token embutido. O Caddy já serve `/completo/` (é `file_server`), então o deploy foi só cópia do site (montado, sem rebuild). Testes: `testar-completo.mjs` (portão, entrada, sessão, gráficos, log, 401) + `testar-site.mjs`. Ao vivo: `atlas.kerlonr.com.br/completo/` (200). Ver [[wiki/site-e-painel]].

**Redesenho da `/completo/` como console** ([orquestrador #23](https://github.com/setrem-robot/orquestrador/pull/23), mesclado): a pedido de "mais bonito, UI/UX, simples de usar". Trocou a rolagem longa por: **faixa de sinais vitais** no topo (estado geral com veredito colorido, temperatura, CPU, memória, bateria, tempo ligado — cada um com sparkline e cor de estado verde/âmbar/vermelho) e **abas** (Saúde do Pi · Sensores · Localização · Eventos). Barra fixa com status/última-atualização/auto/atualizar/sair. Mapa desenha só ao abrir a aba (Leaflet não mede container escondido). Paleta da Atlas mantida + tokens `--bom/--atencao/--critico`. Testes `testar-completo.mjs` e `testar-site.mjs` OK. **Limite:** revisão visual da tela logada não foi possível por automação — a regra de segurança impede digitar o token em campos do navegador; validado por 200 nas rotas e estrutura servida (`vitais`, `tablist`).

**Limite:** o `wifi` vem `null` porque o robô está no **cabo** (eth0); preenche sozinho no campo, via wlan0. O store-and-forward vale **na LAN** — se o robô sair da rede do `.150`, o bridge não alcança o IP interno; telemetria por internet exigiria expor o MQTT do `.150` (porta 8883/TLS), decisão ainda em aberto.

**Pendências:** ver [[wiki/planejamento/prioridades]]. PR #13 do dependabot segue sem mexer.

---

## 2026-09-10 — Nuvem centralizada no servidor .150

**Escopo:** subir toda a pilha de nuvem (banco, ingestor, API, broker) em Docker no `192.168.1.150`, alimentar com dados, e expor a API para o app pela internet.

**Agente:** Claude Opus 4.8. **Servidor:** `server@192.168.1.150`, Ubuntu 24.04. **Repositório:** `orquestrador`.

**Feito:**

- Pilha em `~/docker-stacks/atlas/` (transferida por SFTP, não clonada — o servidor não tem credencial do GitHub). Isolada dos outros projetos que já rodam ali (`crafty`, `odysseus`, etc.).
- `.env` de produção com senhas fortes geradas na hora; `passwd` do Mosquitto gerado com `mosquitto_passwd`.
- **Conflito de porta resolvido:** a 8000 é do `crafty`. Um `compose.150.yml` com `ports: !reset []` tira a API do host — o túnel a alcança pela rede interna (`api:8000`).
- Quatro serviços no ar e saudáveis; ingestor conectado ao banco e ao broker.
- **7200 registros** de demonstração (6 h de trajeto) semeados via container efêmero com as credenciais de escrita.
- Túnel Cloudflare *quick tunnel* (sem conta, URL provisória) — a API responde pela internet. O de domínio fixo aguarda o `TUNNEL_TOKEN` do usuário.

**Bug corrigido no caminho** ([orquestrador #14](https://github.com/setrem-robot/orquestrador/pull/14), mesclado): a conninfo da API tinha `options=-c statement_timeout=8000` sem aspas. O libpq quebra a string em espaços, lia `statement_timeout` como campo solto e recusava **toda** conexão — API respondia 503 em tudo. O teste antigo conferia que a string continha o trecho quebrado; o novo usa `conninfo_to_dict` (o parser real). Validado no `.150`: 503 → `{"ok":true,"banco":true}`.

**Evidência:** `curl` da minha máquina (fora do servidor) em `/saude` e `/v1/publico/resumo` pelo túnel retornou os dados. 4 testes de `test_banco` verdes no container com psycopg real.

**Limite:** os dados são de **demonstração**, não do robô (o Pi ainda não publica telemetria real). A URL do túnel é **provisória** — muda a cada reinício até o domínio fixo entrar.

**Túnel de domínio fixo (fechado no mesmo dia):** `atlas.kerlonr.com.br/api` no ar. O `atlas.kerlonr.com.br` já existia no DNS mas dava erro 1033 (ligado a nada). O login headless do cloudflared falhou (servidor atrás de NAT não recebe o callback); resolvido rodando `cloudflared tunnel login` **neste PC** (callback local funciona) e enviando o `cert.pem` ao `.150`. Daí: túnel nomeado `atlas-api`, `route dns --overwrite-dns`, ingress → Caddy (`localhost:8088`), serviço `cloudflared-atlas.service`. Um Caddy corta o `/api`. Testado pela internet: `/api/saude`, `/api/v1/estado` (token), `/api/v1/publico/resumo`, `/api/v1/trajeto?horas=6`.

**App:** o código de busca já estava correto (GET com base+caminho, token, timeout, trata 401/429/503). Nenhuma mudança de código — só configurar URL (`https://atlas.kerlonr.com.br/api`) + token nos ajustes.

**Pendência que depende do usuário:** colar URL + `API_TOKEN` nos ajustes do app. Detalhe em [[wiki/configuracao/servidor-150]].

**Não mexido:** PR #13 do dependabot (bump do psycopg) no orquestrador — anterior a este trabalho, e um bump de dependência na pilha recém-subida não é decisão minha de mesclar sem ordem.

---

## 2026-09-10 — Nuvem consolidada num compose só

**Escopo:** deixar tudo (Caddy + túnel) num único `docker-compose.yml`, para rodar no LARCC com um comando.

**Agente:** Claude Opus 4.8. **Repositório:** `orquestrador` ([#16](https://github.com/setrem-robot/orquestrador/pull/16), mesclado). **Servidor:** `.150`.

**Antes:** três peças soltas — compose base + override de VM (`compose.150.yml`) + túnel como serviço systemd do host. **Agora:** `docker compose --profile tunel up -d` sobe os 6 serviços.

- **Caddy** virou serviço de primeira classe (porta de entrada, corta o `/api`).
- **API** deixou de publicar porta (`expose`); o Caddy fica na frente. Isso elimina o conflito com a 8000 do `crafty` **sem override** — o `compose.150.yml` foi removido.
- **Caddy** publica em porta configurável (`CADDY_BIND`/`CADDY_PORT`, padrão `127.0.0.1:8088`), no lugar do antigo `API_BIND`.
- **`cloudflared`** passou de token de painel para **config versionada** (`cloudflared/config.yml` → `http://caddy:80`); credenciais fora do git.

**Migração na `.150`:** túnel movido do systemd do host para o compose (4 conexões), `cloudflared-atlas.service` e `atlas-config.yml` do host removidos, `compose.150.yml` apagado. Ajuste de permissão: as credenciais precisam de `chmod 644` para o usuário não-root do container do cloudflared ler.

**Docs:** `.env.example`, `.env.local.example`, `compose.local.yml` e a §4 do `docs/setup-cloud.md` reescritos para o fluxo por config + Caddy.

**Verificação:** os 6 serviços de pé com `restart=unless-stopped`; `https://atlas.kerlonr.com.br/api/saude` → `{"ok":true,"banco":true}` pela internet, após a consolidação.

---

## 2026-09-10 — Correção de erros e limpeza no .150

**Escopo:** corrigir os erros pendentes e apagar o que não é usado, deixando a pilha rodando no `.150`.

**Agente:** Claude Opus 4.8. **Repositório:** `orquestrador`. **Servidor:** `.150`.

**Corrigido** ([orquestrador #15](https://github.com/setrem-robot/orquestrador/pull/15), mesclado): a suíte da API falhava na coleta de `test_cabecalhos` com `requires the httpx2 package`. O Starlette 1.6 (puxado por `fastapi>=0.141`) faz `import httpx2 as httpx` no `testclient.py`; o pin de dev `httpx>=0.28.1` era o cliente errado. Trocado para `httpx2>=2.12.0`. Só afeta os testes — o runtime não usa cliente HTTP e a imagem da VM não leva nenhum dos dois. Suíte no container do `.150`: **37 testes, OK** (era 1 erro de coleta). Sem rebuild da imagem de produção.

**Apagado (não usado):**
- Túnel Cloudflare **`Atlas`** (vazio, sem conexões, cujo hostname eu já havia repontado). Os outros túneis da conta (Bifrost, Crafty, Home Assistant, Home Server, RPI4) — intactos.
- Lixo em `/tmp` do `.150` (`cloudflared.deb`, `cf-login.log`, scripts de teste).
- Imagens Docker penduradas (dangling, sem tag): **576 MB** recuperados.

**Estado final conferido:** 5 containers `running` com `restart=unless-stopped` (api e banco `healthy`); `cloudflared-atlas.service` `enabled` (sobe no boot); `https://atlas.kerlonr.com.br/api/saude` → `{"ok":true,"banco":true}` e `/api/v1/estado` com token → HTTP 200, **após** a limpeza.

**Runtime sem erros:** 0 linhas de erro nos logs dos 5 containers nos últimos 20 min.

---

## 2026-09-10 — Reorganização do vault

**Escopo:** deixar o vault mais legível e adicionar o que faltava para alguém entender o projeto sem já conhecê-lo.

**Agente:** Claude Opus 5. **Repositório:** `AtlasVault`.

**Criado:**

- [[wiki/meta/glossario|Glossário]] — ~60 termos explicados **no contexto da Atlas**, com as pegadinhas daqui marcadas (o `orquestrador` repositório contra o `Assistant` que também orquestra; Vosk rápido/impreciso contra Whisper lento/preciso; branch `producao` que não prova instalação).
- [[wiki/meta/verificacao|Verificação pendente]] — era um link pendurado em duas notas. Reúne o que foi afirmado sem conferência, na escala de evidência que o vault já usava.
- **`Mapa do projeto.canvas`** — estava vazio (2 bytes). Agora tem 33 cartões e 8 setas: o caminho de um comando e de uma pergunta, com o elo que falta marcado em vermelho.

**Corrigido:**

- **A tabela do `INICIO.md` renderizava quebrada.** Wikilinks com alias — a forma `colchete-colchete nota, barra, texto` — dentro de célula de tabela partem a coluna na própria barra. Escapado com `\|` em todas.
- Dois links apontavam para notas inexistentes que **existem com outro nome**: `wiki/fontes/index` → `wiki/meta/fontes`, `wiki/governanca/manutencao` → `wiki/meta/como-usar`.
- `wiki/meta/inventario` apontava para `fontes/imagens/`, mas as imagens estão em `fontes/identidade/`. A pasta vazia foi removida.
- Frontmatter em 6 notas que não tinham — ficavam fora do painel de propriedades e da busca por tipo.

**Reescrito:** [[INICIO]] (painel, com trilha de leitura de 15 minutos e diagrama) e [[wiki/index]] (mapa da documentação, agora organizado por pergunta e não por pasta).

**Evidência:** 86 links, **nenhum quebrado**. Os **8 diagramas mermaid** do vault renderizados com `@mermaid-js/mermaid-cli` 11.17.0 — todos válidos. Cartões do canvas conferidos: 20 apontam para arquivos existentes, nenhuma seta órfã.

**Limite:** organização documental. Nenhuma afirmação técnica nova foi produzida aqui; o conteúdo veio das notas existentes e das medições já registradas.

---

## 2026-09-09 — Escuta em streaming com Vosk

**Escopo:** trocar o reconhecedor padrão de Whisper para Vosk, para eliminar a espera entre o fim da fala e o início da resposta.

**Agente:** Claude Opus 5. **Repositório:** `atlas_ai_v2`. **Branch:** `main`, depois `producao`.

**Motivo:** medições anteriores de tempo de resposta usaram **pergunta digitada**, que não passa pelo microfone — a espera do reconhecimento nunca esteve nelas. Confirmado no Pi: 1,7 a 2,3 s de silêncio depois de a pessoa parar de falar.

**Alterado:**

- `hearing/vosk_ears.py` reescrito. O caminho existia mas **não abria o microfone deste robô**: pedia 16 kHz direto, e a placa C-Media com `dsnoop` não anuncia essa taxa. Negociação de taxa, conversão e passa-alta passaram a ser funções de módulo em `hearing/microfone.py`, usadas pelos dois motores.
- Supervisão de reabertura no caminho do Vosk. Sem ela voltaria o defeito de reenumeração USB — robô surdo com um núcleo a 100 % e nada no log.
- `ao_fechar_frase` no Vosk. Os dois bipes vinham do `Microfone`, que o Vosk não usa; sem isso a troca os teria emudecido.
- Silêncio de partida (0,5 s) ao retomar a escuta. Ver abaixo.
- Padrão em `config.py`, `.env.example`, `COMO-FUNCIONA.md` e `scripts/baixar-modelo-escuta.sh`. O script baixava Whisper sem argumento — quem instalasse do zero subiria com o motor certo e o modelo do outro.
- `ROBOTEYE_HEARING_BACKEND` exposto na página de configuração, para trocar sem SSH.

**Defeito encontrado durante a validação:** o Vosk come a primeira palavra quando o áudio começa nela. Numa sala isso não aparece — silêncio é o que mais chega ao microfone —, mas aparece **ao retomar depois de a Atlas falar**, porque enquanto pausada nada é entregue ao reconhecedor. A palavra comida seria o nome dela. Simulando o turno completo, três de quatro perguntas seriam descartadas como "não era comigo". Corrigido enfileirando silêncio no `retomar`.

**Evidência:**

- Suíte do RobotEye: **781 testes, todos passaram** (763 antes; 18 novos em `tests/test_vosk.py`, que não tinha nenhum). Ruff, ruff-format e mypy limpos. CI verde nos 5 jobs em ambos os PRs.
- PRs [#19](https://github.com/setrem-robot/atlas_ai_v2/pull/19) e [#20](https://github.com/setrem-robot/atlas_ai_v2/pull/20), ambos revisados, mesclados e com branch removida. Nenhum PR aberto ao final.
- Implantado em `producao` `43a6fe0` e **validado no hardware** — ver [[wiki/revisoes/2026-09-09-escuta-vosk-hardware]].

**Limite:** precisão com voz humana **não validada**. O ensaio usou a voz sintética do robô, entrada ruim para reconhecimento, e nela nenhum dos dois motores acertou a palavra de despertar. Pendência registrada em [[wiki/planejamento/validacao]].

**Reversível:** `ROBOTEYE_HEARING_BACKEND=whisper` no `.env` e reiniciar. Cópia do arquivo anterior em `~/atlas_ai_v2/.env.bak-pre-vosk` no Pi. Os dois modelos estão no disco.

---

## 2026-09-09 — Leitura dos relatórios do semestre anterior

**Escopo:** ler os três PDFs em `Relatorios/` e confrontá-los com o código atual.

**Resultado:** [[wiki/historico/relatorios-semestre]]. Os três trabalhos terminam apontando um para o outro, e o elo comum — acionamento dos motores — hoje existe em código (`pi/services/motores/`) mas **não está instalado no Pi**, o que mantém os ensaios T2–T6 da estrutura impossíveis.

**Divergências encontradas nos relatórios**, relevantes para quem for citá-los: inclinação de rampa 20° contra 5–7° dentro do mesmo texto; cálculo de torque com 8 kg quando o peso de projeto é 15 kg; painel descrito em Quarkus que hoje é FastAPI; "Gemma 3B" e Debian Bookworm que hoje são `gemma3:1b` e Trixie.

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

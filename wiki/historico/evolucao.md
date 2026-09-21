---
title: "Antes, agora e próxima melhoria"
tipo: historico
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - historico
---

# Antes, agora e próxima melhoria

| Aspecto | Entrega anterior | Código/documentação atual | Direção definida |
|---|---|---|---|
| Entrada do controle | SPP no ESP32 e serial para o Pi | BLE NUS diretamente no Pi; ESP32 e serial ainda no repositório como legado | Consolidar operação somente no Pi |
| App | Controle direcional Android | BLE para Android/iOS, telemetria em quatro abas, rota planejada, distribuição Android | Melhorar controle, retorno e confiabilidade |
| Motores | Integração ainda pendente nos relatórios | Cinemática, rampa, vigia, lock e backends real/simulado | Validar acionamento e parada no robô |
| IA | Vosk + modelo chamado Gemma 3B + eSpeak/MBROLA, local | Ollama local/rede, voz Edge/Piper/Kokoro, reserva, streaming e persona | Qualidade, latência, áudio e integração melhores |
| Escuta | Vosk no relato da interface | Vosk voltou a ser padrão em 09/09; Whisper disponível | Medir entendimento em situações reais |
| GPS | Integração declarada na conclusão de orquestração | Serviço existe; README atual informa módulo não montado | Implementar e validar GPS físico |
| Banco | MQTT → ingestor → TimescaleDB | Mesmo fluxo mais API FastAPI, controles de acesso e telas | Melhorar confiabilidade, qualidade e uso dos dados |
| Painel | Quarkus + SSE + Leaflet no PDF | API FastAPI, app Flutter e site estático | Informações coerentes, recentes e rastreáveis |
| Infraestrutura | VM do LARCC citada | Compose pronto; README relata execução em PC provisório | Confirmar implantação e continuidade da coleta |
| Estrutura | PLA/aço com ensaios manuais | Não foram encontrados CAD/STL atuais na pasta | Preservar herança e documentar alterações físicas |
| Gestão do conhecimento | Relatórios e documentação por repo | Este vault conecta fontes, estado, decisões e planos | Atualizar a cada teste, decisão e entrega |

“Atual” nesta tabela significa o retrato de 09/09/2026 das fontes inspecionadas. Operação física só deve passar para validada após ensaio registrado.

Fontes detalhadas: [[wiki/historico/relatorios-semestre]], [[wiki/modulos/index]], [[wiki/estado/git-local-e-remoto]] e [[wiki/estado/divergencias]]. Objetivos confirmados pelo usuário em 09/09/2026: [[wiki/planejamento/onde-queremos-ir]].

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

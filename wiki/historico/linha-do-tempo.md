---
title: "Linha do tempo — da herança ao retrato atual"
tipo: historico
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - historico
---

# Linha do tempo — da herança ao retrato atual

As datas dos commits representam registros Git, não a data em que algo foi instalado no robô. A entrega anterior é identificada pelo usuário e pelos PDFs, sem converter a numeração PIE em sequência cronológica.

| Momento | Marco documentado | Evidência |
|---|---|---|
| Etapa anterior, documentos de 2026 com divergência de capa | Estrutura híbrida, interface local e conectividade ESP32/MQTT | [[wiki/historico/relatorios-semestre]] |
| 27/08/2026 | API de leitura, túnel, site e melhorias de motores/ambiente publicadas como conjunto | orquestrador `19815b8` |
| 27/08/2026 | Otimizações de reserva de RAM e rádio incorporadas | RobotEye `60abf91` |
| 30/08/2026 | App planeja e envia rota; orquestrador valida/republica | app `cf52b55`; orquestrador `367d9f4` |
| 02/09/2026 | Último push registrado do repositório acadêmico na consulta | [[fontes/auditoria/repositorios-github.json]] |
| 03/09/2026 | Correções de parada/tela, concorrência de motores e teto de tempo do banco | app `04b7ad2`; orquestrador `cdb5553` |
| 03/09/2026 | Recuperação de áudio USB, sinais de escuta e coordenação com inferência | RobotEye `dcbcdef`, `16acb2f`, `4d57814`, `5318bb0` |
| 04/09/2026 | Ajustes de prompt/contexto e `keep_alive` para Ollama | RobotEye `6503b67`, `9e468b8`, `61b00c9` |
| 09/09/2026 | Vosk padrão e silêncio inicial; integração em produção | RobotEye `a88c2dd`, `e1b26d7`, `43a6fe0` |
| 09/09/2026 | Objetivo de melhoria geral confirmado e vault revisado | [[wiki/diario/2026-09-09]] |

O histórico completo permite rastrear também as etapas anteriores a esses marcos. Ver [[wiki/meta/historicos-git]]. A existência de commits antigos não prova que pertencem ao semestre anterior ou que representam exatamente a versão dos PDFs.

## Fontes e conferência

- [[wiki/meta/historicos-git]]
- [[fontes/auditoria/repositorios-github.json]]

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

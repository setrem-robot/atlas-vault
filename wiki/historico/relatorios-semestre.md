---
title: "De onde viemos — a entrega anterior"
tipo: historico
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - historico
---

# De onde viemos — a entrega anterior

O usuário identificou os três PDFs da pasta `Relatorios` como a entrega do semestre anterior. Eles são a base histórica desta documentação. Os textos descrevem frentes diferentes do mesmo robô e não comprovam, isoladamente, o funcionamento integrado de todas elas.

| Frente | Autores no PDF | O que foi relatado | O que ficou aberto |
|---|---|---|---|
| [[wiki/historico/estrutura-anterior|Estrutura mecânica]] | Andriel Felipe Schultz; Crístofer Mateus Rutzen; Gabriel Kaspary | CAD, chassi tubular de aço, carenagem modular em PLA e ensaios manuais | Acionamento motorizado, rampas e validação dinâmica |
| [[wiki/historico/interface-anterior|Interface humano-robô]] | Bernardo Baú; Guilherme Machry da Silva; Rychard Daniel dos Santos | Conversa local, Vosk, Ollama, voz e animações no Pi 5 | Usabilidade ampliada, áudio e base institucional |
| [[wiki/historico/orquestracao-anterior|Conectividade e orquestração]] | Kauã Rambo; Eduardo Augusto Goetz; Thales Gabriel Fernandes Diniz Martins | App Flutter, SPP/ESP32/serial, MQTT, GPS descrito e TimescaleDB; painel Quarkus | Retorno ao app, integração da IA, motores e energia |

## A herança principal

Recebemos uma plataforma física e diferentes implementações de software. A estrutura separa a responsabilidade mecânica; a interface demonstra o ciclo ouvir–pensar–falar; a orquestração organiza comandos e telemetria. A evolução atual concentra-se em integrar, tornar observável e melhorar esse conjunto.

Não se deve converter “objetivo alcançado” em um PDF em uma afirmação de que o robô atual está montado e testado da mesma forma. Exemplo concreto: o relatório de orquestração declara o GPS integrado, enquanto os READMEs atuais dizem que o módulo não está montado. Ver [[wiki/estado/divergencias]].

## Datas e nomes acadêmicos

Os documentos referem-se a 2026, mas a capa de Estrutura traz 2025 e a folha seguinte traz 2026. O texto de Estrutura cita PIE V; o repositório acadêmico atual se chama `doc-interdisciplinar-4-semestre` e identifica PIE IV. Preservei essas diferenças. A sequência “entrega anterior → trabalho atual” vem do usuário; a numeração não foi usada para deduzir a cronologia.

As referências de página neste vault usam a **página física do PDF, contando a capa como 1**. A numeração impressa pode ser diferente.

Continue em [[wiki/historico/evolucao]] e [[wiki/historico/relatorio-atual]].

## Fontes e conferência

- [[fontes/relatorios/EstruturaPDF.pdf]]
- [[fontes/relatorios/InterfacePDF.pdf]]
- [[fontes/relatorios/OrquestradorPDF.pdf]]

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

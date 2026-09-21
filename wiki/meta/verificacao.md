---
title: "Verificação pendente — o que foi afirmado sem ser conferido"
tipo: meta
estado_documental: em_uso
atualizado: 2026-09-10
tags:
  - atlas
  - meta
  - verificacao
---

# Verificação pendente

> [!important] Por que esta nota existe
> A confusão mais cara deste projeto não é técnica: é tomar **"está no código"**
> por **"está funcionando no robô"**. As duas coisas divergiram várias vezes, e
> sempre custou tempo. Esta nota lista o que ainda está do lado não conferido.
>
> Era um link pendurado em [[wiki/diario/2026-09-09]] e
> [[wiki/planejamento/validacao]] antes de virar nota.

---

## A escala que o vault usa

Cada afirmação técnica cabe em um destes degraus. Quanto mais alto, mais caro de
produzir e mais confiável:

| Degrau | Significa | O que prova |
|---|---|---|
| **validado no hardware** | Rodou no robô e foi medido | Que funciona ali, naquele dia |
| **reproduzido em software** | Passou em teste automatizado | Que a lógica está certa |
| **análise estática** | Lido no código, não executado | Que a intenção está escrita |
| **documentado por outra fonte** | Alguém escreveu | Nada, sozinho |
| **planejado** | Ainda não existe | Nada |

Três armadilhas específicas deste projeto:

- **Uma branch `producao` não prova a versão instalada.** Ela prova que alguém
  fez um merge. O Pi só tem aquilo depois de um `git pull` lá dentro.
- **Uma coleta Git é um retrato datado.** Vale para o instante em que foi tirada.
- **Afirmação em `CLAUDE.md` não é telemetria.** Ela envelhece sem avisar.

---

## Aberto hoje

### Escuta — o ensaio que decide [[wiki/decisoes/registro|DEC-08]]

| | |
|---|---|
| **Validado** | Tempo. No Pi, o Vosk fecha a frase em 76–742 ms contra 1727–2293 ms do Whisper. Ver [[wiki/revisoes/2026-09-09-escuta-vosk-hardware]]. |
| **Não validado** | **Precisão com voz humana.** O ensaio usou a voz sintética do próprio robô, e nela nenhum dos motores acertou a palavra de despertar. |
| **Evidência real contrária** | Falando de verdade com o robô, o Vosk pequeno transcreveu "Atlas" como **"classe"** duas vezes seguidas. |
| **Como fechar** | Protocolo [[wiki/planejamento/validacao\|T-IA-1]], com pessoas diferentes. |

### Movimento — nunca houve ensaio

| | |
|---|---|
| **Reproduzido em software** | Cinemática, rampa e parada de emergência têm teste. |
| **Não validado** | Nada girou uma roda a partir de um comando. Os serviços do `orquestrador` **não estão instalados no Pi**. |
| **Herdado sem prova** | Os ensaios T2 a T6 do relatório de estrutura não foram executados — pelo mesmo motivo, no semestre anterior. |
| **A conferir antes** | Corrente do TMC2209 contra o NEMA 23, e o teto de velocidade (~0,20 m/s hoje, contra 0,3 m/s que o próprio ensaio T5 exige). |

### Fatos que o robô afirma

| | |
|---|---|
| **Observado** | Disse que a Setrem fica na cidade de **"Balsy"**. A persona diz "Três de Maio" três vezes e nunca menciona Balsy. Em outra rodada inventou "Em 1922, a Setrem tinha 1.500 estudantes". |
| **Causa provável** | `gemma3:1b` confabulando — um bilhão de parâmetros é pouco para ancorar fatos. |
| **Não investigado** | Se um modelo maior ou uma persona mais curta e direta corrige. |

### Nuvem e telemetria

Nada da infraestrutura de nuvem foi conferido nesta etapa: versão implantada na
VM, configuração de broker remoto, TLS, firewall, retenção do banco,
backup e restauração.

### Ambiente do robô

| Item | Situação |
|---|---|
| Refrigeração | Sem cooler ativo. Medido a 54,3 °C em repouso, `throttled=0x0` — mas nunca sob carga longa. |
| Relógio | Sem bateria: a hora salta no arranque até a rede sincronizar. |
| Acesso SSH | Por senha. Trocar por chave **testando a chave antes** de desligar a senha. |
| Autonomia | Consumo em operação nunca foi medido; o banco de baterias não foi dimensionado. |

---

## Como fechar um item

1. Escolher o protocolo em [[wiki/planejamento/validacao]] ou escrever um novo com [[modelos/Experimento]].
2. Registrar ambiente, versão e **origem dos dados** — real ou simulada.
3. Anotar o que o ensaio **não** prova. É a parte que costuma faltar.
4. Registrar em [[wiki/historico/registro-de-trabalho]] e atualizar a prioridade.
5. Só então mover a afirmação de degrau, aqui e em [[wiki/estado/atual]].

> [!danger] O que não fazer
> Marcar um achado como resolvido sem alteração identificável e sem evidência de
> aceite. `pendente` não quer dizer que alguém assumiu; `em validação` não quer
> dizer `concluído`.

---
[[INICIO|Início]] · [[wiki/estado/divergencias|Divergências]] · [[wiki/meta/fontes|Fontes e limites]]

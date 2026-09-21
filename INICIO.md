---
cssclasses: [atlas-home]
title: "Atlas — conhecimento do projeto"
projeto: Atlas
tipo: painel
atualizado: 2026-09-10
status: referencia
tags:
  - atlas
  - painel
---

![[fontes/identidade/atlas-olhos-1024.png|180]]

# Atlas
### Conhecimento do projeto · Engenharia de Computação · SETREM

**Próxima entrega:** demonstração completa de um robô funcionando. [[wiki/planejamento/plano-do-projeto|Plano central]] · [[wiki/planejamento/site-e-acesso|Evolução do site e login]].

> [!abstract] O que é a Atlas, em três frases
> Um robô móvel que circula pelo campus e conversa com quem chega perto. Uma
> plataforma de aço com carenagem impressa em 3D, um Raspberry Pi 5 que ouve,
> pensa e fala, e um aplicativo que dirige e mostra por onde ele andou.
> São **três repositórios que rodam sozinhos** e precisam falar a mesma língua
> nas fronteiras — este vault é o mapa dessas fronteiras.

---

## Se você tem 15 minutos

Uma ordem de leitura que sai do zero e chega ao ponto de conseguir opinar:

| | Leia | Por quê |
|---|---|---|
| 1 | [[wiki/meta/glossario\|Glossário]] | Vinte termos que aparecem em tudo. Sem eles o resto trava. |
| 2 | [[wiki/arquitetura/visao-geral\|Arquitetura]] | Quem faz o quê, e onde cada programa roda. |
| 3 | [[wiki/estado/atual\|Estado atual]] | O que funciona hoje, conferido no robô. |
| 4 | [[wiki/historico/relatorios-semestre\|De onde viemos]] | O que o semestre anterior entregou e o que deixou aberto. |
| 5 | [[wiki/planejamento/prioridades\|Prioridades]] | O que está na fila, com IDs estáveis. |

Ou abra o **[[Mapa do projeto.canvas\|mapa visual]]** e navegue clicando.

---

## O sistema em uma imagem

```mermaid
flowchart LR
    subgraph CEL["CELULAR"]
        APP["app<br/>Flutter"]
    end
    subgraph PI["RASPBERRY PI 5"]
        RE["RobotEye<br/>face · voz · IA · escuta"]
        BUS{{"MQTT local<br/>127.0.0.1:1883"}}
        ORQ["orquestrador<br/>motores · GPS · Wi-Fi"]
    end
    subgraph NUV["NUVEM"]
        API["API + TimescaleDB"]
    end
    PESSOA(["pessoa"])

    APP -- "BLE / NUS" --> RE
    RE -- "robo/comando/entrada" --> BUS
    BUS --> ORQ
    ORQ -- "robo/telemetria/#" --> API
    API --> APP
    PESSOA -- "voz" --> RE
    RE -- "resposta falada" --> PESSOA
```

> [!warning] O elo que ainda falta
> Os serviços do `orquestrador` **não estão instalados no Pi**. O comando sai do
> celular, atravessa o BLE, chega ao barramento — e morre ali, porque não há
> quem consuma. **O robô conversa, mas não anda.**
> Detalhe em [[wiki/estado/atual#O que está no ar hoje\|Estado atual]].

---

## Onde estamos hoje

> [!success] Funcionando e conferido no robô (10/09)
> Face, voz e conversa de pé · escuta reconhecendo **durante** a fala · voz
> `francisca` com o brilho ajustado à caixinha · 801 testes verdes.

> [!danger] Aberto, em ordem de impacto
> 1. **Serviços do orquestrador não instalados** — é o que impede o robô de andar.
> 2. **O modelo inventa fatos** — disse que a Setrem fica em "Balsy". Ver [[wiki/estado/divergencias]].
> 3. **Palavra de despertar mal reconhecida** — o Vosk pequeno ouve "classe" no lugar de "Atlas".
> 4. **16 achados da revisão técnica** (AT-01 a AT-16), nenhum corrigido.

---

## Os três repositórios

| Pasta | Apelido | Responsabilidade | Código |
|---|---|---|---|
| `RobotEye` | a **cara** | Face, voz, IA, escuta e ponte BLE | [atlas_ai_v2](https://github.com/setrem-robot/atlas_ai_v2) |
| `orquestrador` | o **corpo** | Roteamento, motores, GPS, Wi-Fi e nuvem | [orquestrador](https://github.com/setrem-robot/orquestrador) |
| `app` | o **controle** | Direção, rota e telemetria | [aplicativo](https://github.com/setrem-robot/aplicativo) |

Detalhe de cada um em [[wiki/modulos/index|Catálogo dos componentes]].

---

## Por assunto

| Quero… | Abrir |
|---|---|
| Entender uma sigla ou termo | [[wiki/meta/glossario\|Glossário]] |
| Trabalhar como agente de IA | [[CONTEXTO-IA\|Contexto e protocolo]] |
| Saber o que funciona hoje | [[wiki/estado/atual\|Estado atual]] · [[wiki/estado/divergencias\|Divergências]] |
| Escolher a próxima tarefa | [[wiki/planejamento/prioridades\|Prioridades]] |
| Ver como as peças conversam | [[wiki/arquitetura/mapa-comunicacao\|Mapa de comunicação]] · [[wiki/api/contrato-mqtt\|Contrato MQTT]] |
| Consultar a revisão técnica | [[wiki/revisoes/2026-09-09-revisao-tecnica\|16 achados]] |
| Ligar, operar ou diagnosticar | [[wiki/configuracao/setup-completo\|Operação]] · [[wiki/configuracao/diagnostico\|Diagnóstico]] |
| Saber o que já foi feito | [[wiki/historico/registro-de-trabalho\|Registro de trabalho]] |
| Planejar um ensaio | [[wiki/planejamento/validacao\|Protocolos de validação]] |
| Achar um documento | [[wiki/index\|Mapa da documentação]] |

---

## Como este vault funciona

> [!tip] Contexto → estado → prioridades → evidência → ação → registro
> Informação sem **data** ou sem **fonte** deve ser confirmada antes de orientar
> uma mudança. Toda nota diz quando foi escrita e de onde veio.

Uma distinção que atravessa o vault inteiro e evita a maior parte dos enganos:

| Rótulo | Significa |
|---|---|
| **validado no hardware** | Rodou no robô e foi medido |
| **reproduzido em software** | Passou em teste, sem tocar no hardware |
| **análise estática** | Lido no código, não executado |
| **documentado por outra fonte** | Alguém escreveu; não foi conferido aqui |
| **planejado** | Ainda não existe |

Manutenção e convenções em [[wiki/meta/como-usar|Como usar e manter]] · fontes e
limites em [[wiki/meta/fontes|Fontes]] · o que ainda não foi conferido em
[[wiki/meta/verificacao|Verificação pendente]].

Algo novo e sem lugar ainda? Deixe em [[inbox/LEIA-ME|inbox]].

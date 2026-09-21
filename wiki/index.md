---
title: "Mapa da documentação"
tipo: indice
estado_documental: revisado
atualizado: 2026-09-10
tags:
  - atlas
  - indice
---

# Mapa da documentação

[[INICIO|← Painel]] · [[Mapa do projeto.canvas|Mapa visual]] · [[wiki/meta/glossario|Glossário]]

> [!tip] Qual usar
> O **painel** responde "o que está acontecendo". O **mapa visual** responde
> "como as peças se ligam". Esta página responde "onde está tal documento".

---

## Entender o projeto

| Nota | O que responde |
|---|---|
| [[wiki/meta/glossario\|Glossário]] | O que cada sigla e termo quer dizer aqui |
| [[wiki/arquitetura/visao-geral\|Arquitetura]] | Quem faz o quê, e onde cada programa roda |
| [[wiki/arquitetura/como-funciona\|Como funciona]] | O caminho de um toque e de uma pergunta |
| [[wiki/arquitetura/mapa-comunicacao\|Mapa de comunicação]] | Quem fala com quem, por qual transporte |
| [[wiki/modulos/index\|Catálogo dos componentes]] | Cada peça em detalhe |
| [[wiki/hardware/especificacoes\|Hardware]] | O que existe fisicamente |
| [[wiki/site-e-painel\|Site e painel]] | Endereços públicos, dados exibidos e manutenção das páginas |

## Saber o estado

| Nota | O que responde |
|---|---|
| [[wiki/estado/atual\|Estado atual]] | O que funciona hoje, conferido no robô |
| [[wiki/estado/divergencias\|Divergências]] | O que ainda não bate e precisa de confirmação |
| [[wiki/estado/onde-estamos\|Onde estamos]] | Leitura narrativa do momento do projeto |
| [[wiki/estado/git-local-e-remoto\|Git]] | Publicado, local e instalado — e por que diferem |
| [[wiki/meta/verificacao\|Verificação pendente]] | O que foi afirmado sem ter sido conferido |

## Decidir o que fazer

| Nota | O que responde |
|---|---|
| [[wiki/planejamento/plano-do-projeto\|Plano do projeto]] | Ordem das entregas, dependências, estudo e aceite da demonstração |
| [[wiki/planejamento/site-e-acesso\|Site, painel e acesso]] | Visual, conteúdo, dados públicos e área com login |
| [[wiki/planejamento/prioridades\|Prioridades]] | A fila, com IDs estáveis (AT-01…AT-16) |
| [[wiki/planejamento/backlog\|Backlog]] | Melhorias ainda sem prioridade |
| [[wiki/planejamento/onde-queremos-ir\|Onde queremos ir]] | O destino, sem confundir com o presente |
| [[wiki/planejamento/validacao\|Validação]] | Como provar um avanço, protocolo a protocolo |
| [[wiki/planejamento/equipe-e-entregas\|Equipe e entregas]] | Quem faz o quê, e os prazos acadêmicos |
| [[wiki/decisoes/registro\|Decisões]] | Por que o projeto é assim (DEC-01…DEC-11) |

## Contratos e código

| Nota | O que responde |
|---|---|
| [[wiki/api/contrato-mqtt\|Contrato MQTT e BLE]] | Tópicos, formatos e UUIDs que os três repos compartilham |
| [[wiki/api/contratos\|API HTTP]] | Rotas da nuvem e modelo de dados |
| [[wiki/seguranca/index\|Segurança]] | Proteções existentes e limites reais |

## Operar o robô

| Nota | O que responde |
|---|---|
| [[wiki/configuracao/setup-completo\|Operação]] | Por onde começar |
| [[wiki/configuracao/servidor-150\|Servidor .150]] | A nuvem centralizada em Docker: banco, API e túnel |
| [[wiki/configuracao/diagnostico\|Diagnóstico]] | Descobrir em que etapa falhou |
| [[wiki/configuracao/ambiente-local\|Ambiente local]] | Testar sem o robô |

## O que já aconteceu

| Nota | O que responde |
|---|---|
| [[wiki/historico/registro-de-trabalho\|Registro de trabalho]] | Cada tarefa, com evidência e limite |
| [[wiki/historico/relatorios-semestre\|De onde viemos]] | O que o semestre anterior entregou |
| [[wiki/historico/linha-do-tempo\|Linha do tempo]] | A sequência, da herança até hoje |
| [[wiki/historico/evolucao\|Antes, agora e depois]] | Comparação por área |
| [[wiki/historico/relatorio-atual\|Relatório acadêmico]] | O trabalho deste semestre |
| [[wiki/diario/2026-09-09\|Diário]] | Notas do dia |

**Os três relatórios anteriores, um a um:**
[[wiki/historico/estrutura-anterior|Estrutura]] ·
[[wiki/historico/interface-anterior|Interface]] ·
[[wiki/historico/orquestracao-anterior|Orquestração]]

## Medições e revisões

| Nota | O que responde |
|---|---|
| [[wiki/revisoes/2026-09-09-revisao-tecnica\|Revisão técnica]] | 16 achados, com evidência e critério de aceite |
| [[wiki/revisoes/2026-09-09-escuta-vosk-hardware\|Escuta no Pi]] | Medição dos dois reconhecedores no hardware |

## Sobre o próprio vault

| Nota | O que responde |
|---|---|
| [[CONTEXTO-IA\|Contexto para IA]] | Protocolo de trabalho para agentes |
| [[wiki/meta/como-usar\|Como usar e manter]] | Convenções, modelos e manutenção |
| [[wiki/meta/fontes\|Fontes]] | Origem, preservação e limites do que está aqui |
| [[wiki/meta/inventario\|Inventário]] | Tudo que foi encontrado nos repositórios |
| [[wiki/meta/historicos-git\|Históricos Git]] | Commits coletados, por repositório |
| [[inbox/LEIA-ME\|Inbox]] | Onde deixar algo novo sem lugar ainda |

---

> [!warning] O que estas notas não são
> Visões gerais são **sínteses**. Para implementação, consulte os arquivos dos
> repositórios. Coletas preservam a data em que foram feitas e **não substituem
> uma verificação atual** — uma branch `producao` não prova o que está instalado.

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

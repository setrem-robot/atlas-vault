---
projeto: Atlas
atualizado: 2026-09-09
status: referencia
---

# Contexto para agentes de IA

> [!important] Entrada comum do projeto
> Leia esta nota antes de propor ou executar trabalho. Ela registra o objetivo e onde encontrar evidências; não substitui o código nem instruções específicas do repositório.

## Objetivo atual

Melhorar confiabilidade, organização e escalabilidade da Atlas, mantendo documentação clara para continuidade entre ferramentas e agentes. A revisão técnica foi produzida; suas correções permanecem pendentes de implementação e validação. A organização documental não implementou os achados.

## Ordem de leitura

1. [[wiki/estado/atual|Estado atual]] — versão revisada, conhecimento e limites.
2. [[wiki/planejamento/prioridades|Prioridades]] — IDs estáveis e próximos trabalhos.
3. [[wiki/revisoes/2026-09-09-revisao-tecnica|Revisão técnica]] — evidências e aceite.
4. [[wiki/arquitetura/visao-geral|Arquitetura]] e [[wiki/arquitetura/mapa-comunicacao|fronteiras]].
5. `AGENTS.md`, `CLAUDE.md` e documentação do repositório afetado. No RobotEye, ler também `.claude/agents/roboteye-keeper.md` para alterações de código.

## Workspace

`D:\SetremRobot` contém somente `app/`, `orquestrador/`, `RobotEye/` e `AtlasVault/`. Código no repositório correspondente; documentação transversal e referências no vault. Não criar relatórios soltos na raiz.

## Regras de evidência

- Conferir branch, HEAD e alterações locais antes de trabalhar. Preservar trabalho de outros agentes.
- Distinguir **reproduzido em software**, **análise estática**, **documentado por outra fonte**, **planejado** e **validado no hardware**.
- Uma branch `producao` não comprova a versão instalada. Coleta Git é um retrato datado.
- Código e contratos do commit relevante são fontes primárias. Notas sintetizam; snapshots antigos dão contexto histórico.
- Afirmações sobre instalação em CLAUDE.md exigem conferir data e ambiente; não são telemetria atual.
- Registrar resultado das suítes, não só o código de saída do shell.
- Não marcar achado como resolvido sem alteração identificável e evidência de aceite.
- Proteger parada, validade de comandos e controle local. Mudança app/BLE/MQTT exige conferir ambos os lados.
- Não copiar credenciais, tokens ou `.env` para o vault.

## Continuidade entre tarefas

Ao iniciar, registrar escopo, achados relacionados, responsável/agente e branch. Ao concluir, atualizar a prioridade e registrar evidência em [[wiki/historico/registro-de-trabalho]]. Mudança de arquitetura exige entrada em [[wiki/decisoes/registro]]. Evitar duplicar o relatório.

`pendente` não significa atribuição a alguém. `em validacao` não significa `concluido`. Correção em software e ensaio físico devem ter registros separados.

## Ferramentas diferentes

Arquivos `AGENTS.md` e referências em `CLAUDE.md` nos três repositórios apontam para este contexto. A leitura automática depende da ferramenta. Se ela não carregar as instruções, iniciar com: **“Leia AtlasVault/CONTEXTO-IA.md e as instruções do repositório antes de trabalhar.”**

## Escopo desta etapa

Revisar, documentar e organizar arquivos. Não afirmar que bugs foram corrigidos, que uma implantação ocorreu ou que documentos foram publicados. A próxima tarefa deve seguir o pedido concreto do usuário.

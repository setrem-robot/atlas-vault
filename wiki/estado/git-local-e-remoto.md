---
title: "Git — publicado, local e instalado"
tipo: estado
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - estado
---

# Git — publicado, local e instalado

## Retrato da coleta

As referências de `origin` foram atualizadas com `git fetch`, sem checkout, merge, reset, commit ou push. Foram examinadas **todas as branches locais**, além da árvore de trabalho e dos históricos remotos disponíveis.

| Pasta | Branch ativa | HEAD | À frente / atrás do upstream | Arquivos modificados |
|---|---|---|---|---|
| app | main | `44d5001` | 0 / 0 | Nenhum |
| orquestrador | main | `98ee681` | 0 / 0 | Nenhum |
| RobotEye | producao | `43a6fe0` | 0 / 0 | Nenhum |

## O detalhe dos commits locais

Há **14 SHAs no app, 25 no orquestrador e 14 no RobotEye** presentes em branches locais e não alcançáveis por qualquer referência remota conhecida na coleta. São 53 identificadores somados entre repositórios, não 53 melhorias inéditas. Integrações por squash produzem novos SHAs e preservam o conteúdo por outro caminho.

Exemplos de equivalência comprovada por **árvore completa idêntica**, incluindo arquivos e modos, em um commit remoto:

| Branch local | Commit remoto com a mesma árvore | Interpretação |
|---|---|---|
| app `dados-do-robo` | `9934857` | Conteúdo incorporado à versão publicada de telemetria |
| app `dependabot` | `7e5a873` | Configuração já publicada |
| app `ui-mais-limpa` | `3b3edaf` | Conteúdo de UI já publicado |
| orquestrador `api-e-landing` | `19815b8` | Conjunto da API, nuvem e melhorias já publicado |
| orquestrador `seguranca-api` | `a63a92c` | Conteúdo já publicado |
| RobotEye `dependabot` | `cc63403` | Configuração já publicada |
| RobotEye `otimizacao-ram-e-radio` | `60abf91` | Conjunto de otimizações já publicado |

As branches `ios-e-parada-automatica`, `motores-escalaveis`, `parada-automatica` e `ble-no-raspberry` não tiveram correspondência exata de árvore no teste. Suas funcionalidades principais aparecem no código atual e/ou em conjuntos posteriores, mas isso não comprova equivalência de cada hunk. Registrar como **histórico local a revisar**, sem afirmar que precisam de push ou apagar branches.

Uma referência marcada como `gone` significa que o upstream configurado não está disponível; não significa trabalho perdido ou não integrado. Contagens por branch podem repetir ancestrais e não devem ser somadas para obter o total único.

## main e producao no RobotEye

`origin/main` está em `e1b26d7`; `origin/producao` está em `43a6fe0`. A branch de produção tem 13 commits exclusivos pelo grafo em relação à main, mas o diff de árvores mostra apenas **o modo de `scripts/bench-radio.sh`, de 100755 em main para 100644 em producao**, sem mudança de conteúdo textual. Isso pode importar para executar o script diretamente no Linux, porém não são 13 funcionalidades faltantes na main.

## Publicado não significa instalado

O updater do RobotEye possui seleção de branch e serviço próprio. A coleta desta máquina não leu o Git no Pi nem na VM. Para fechar uma entrega, registrar SHA em cada ambiente, data de instalação e teste. O app também tem versão instalada e patch de distribuição próprios.

## Onde consultar e como atualizar

- [[wiki/estado/coletas/git-2026-09-09_17-16-47|Coleta completa com todas as branches e SHAs locais]]
- [[fontes/auditoria/equivalencia-branches.json|Resultado de equivalência de árvores e patches]]
- [[wiki/meta/historicos-git|Histórico completo coletado por repositório]]

No PowerShell:

```powershell
python D:\SetremRobot\AtlasVault\ferramentas\atualizar_git.py --fetch
```

Cada execução cria novos arquivos com data/hora, preservando os anteriores. O script não publica, mescla nem altera código. Sem `--fetch`, o retrato usa referências possivelmente antigas. Revise esta nota e o estado atual após uma nova coleta; a narrativa não é reescrita automaticamente.

## Fontes e conferência

- [[fontes/auditoria/git-2026-09-09_17-16-47.json]]
- [[fontes/auditoria/equivalencia-branches.json]]
- [RobotEye/scripts/roboteye-update.service](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/scripts/roboteye-update.service)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

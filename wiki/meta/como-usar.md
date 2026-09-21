---
title: "Como usar e manter o cérebro do projeto"
tipo: meta
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - meta
---

# Como usar e manter o cérebro do projeto

## Abrir no Obsidian

Escolha **Abrir pasta como vault** e selecione `D:\SetremRobot\AtlasVault`. Abra [[INICIO]]. A estrutura usa recursos nativos: links, propriedades, backlinks, busca, marcadores, diário, templates, Mermaid e Canvas. Não depende de plugin comunitário.

[[Mapa do projeto.canvas|O Canvas]] dá uma visão geral clicável. O grafo conecta histórias, módulos, contratos e tarefas. As propriedades `tipo`, `estado_documental` e `atualizado` descrevem a nota; `estado_documental: revisado` não significa que o robô foi validado.

## Onde cada informação mora

| Pasta | Conteúdo |
|---|---|
| `wiki/historico` | Origem, relatórios, linha do tempo e evolução |
| `wiki/estado` | Retrato atual, Git e divergências |
| `wiki/arquitetura`, `modulos`, `api`, `hardware` | Como o sistema está organizado |
| `wiki/configuracao`, `seguranca` | Operação e limites das proteções |
| `wiki/planejamento`, `decisoes` | Objetivos, tarefas, critérios e escolhas |
| `wiki/diario` | O que aconteceu, quando e com qual resultado |
| `wiki/meta` | Fontes, inventários e manutenção do vault |
| `modelos` | Formulários para notas novas |
| `inbox` | Material novo ainda não conferido |
| `fontes` | Originais, snapshots, imagens e auditoria |
| `ferramentas` | Coleta Git, verificação e registro de construção |

## Rotina leve

1. Antes de trabalhar, abrir a tarefa do backlog e consultar a nota do módulo.
2. Registrar descoberta/teste no diário com fonte, SHA e resultado.
3. Ao terminar, atualizar a nota afetada e ligar commit/PR e experimento.
4. Após publicar, atualizar a coleta Git. Após instalar, registrar o SHA do dispositivo separadamente.
5. Na reunião, revisar divergências, próximos passos e autoria/prazos.

## Modelos

[[modelos/Diario]] · [[modelos/Melhoria]] · [[modelos/Experimento]] · [[modelos/Decisao]] · [[modelos/Fonte]]

O recurso nativo Templates insere esses modelos; não há processamento de plugins externos. Alguns campos de contexto são preenchidos pela pessoa e ficam claramente a confirmar.

## Verificar navegação

```powershell
python D:\SetremRobot\AtlasVault\ferramentas\verificar_vault.py
```

O verificador confere links internos, arquivos referenciados pelo Canvas, JSON de configuração, cópias de PDFs e hashes dos snapshots de código. Ele não executa o robô nem resolve links externos pela internet.

## Preservação e versionamento

O vault já possuía `.git`, mas não tinha commits. Esta tarefa mantém as alterações para revisão local e não cria push/commit automaticamente. Não apagar o backup anterior. Os scripts `montar_vault.py`, `complementar_vault.py` e `coletar_fontes.py` registram a construção inicial: **não reexecutá-los depois de editar as notas**, pois podem sobrescrever a documentação e os snapshots de 09/09. Para o uso rotineiro, executar apenas `atualizar_git.py` e `verificar_vault.py`.

Antes de versionar ou compartilhar, revisar material privado e os registros adicionados pela equipe. Preferências de tela/workspace são locais e ficam ignoradas pelo Git.

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

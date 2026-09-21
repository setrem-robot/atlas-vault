---
title: "Fontes — origem, preservação e limites"
tipo: meta
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - meta
---

# Fontes — origem, preservação e limites

## Fontes primárias desta organização

| Fonte | Como foi consultada | Preservação |
|---|---|---|
| Três relatórios em `D:\SetremRobot\Relatorios` | Extração textual com páginas; leitura de conteúdo relevante | PDFs copiados, texto pesquisável e SHA-256 |
| `app`, `orquestrador`, `RobotEye` | Arquivos rastreados, docs, código, testes e scripts; estado Git | ZIP por repo, manifesto e históricos |
| Organização GitHub | Página pública e API via `gh` autenticado | Metadados e árvores JSON |
| Relatório LaTeX privado | Fontes principais e PDF em commit fixado | Arquivos locais em `fontes/github` |
| `.github` da organização | Perfil e referência de commit | Cópia do README e metadados |
| Usuário | Objetivos confirmados nesta conversa em 09/09/2026 | [[wiki/diario/2026-09-09]] |
| Vault anterior | Conteúdo inicial antes da revisão | ZIP preservado |

## Abrir originais e snapshots

- [[fontes/relatorios/EstruturaPDF.pdf]] · [[fontes/relatorios/EstruturaPDF.txt|Texto pesquisável]]
- [[fontes/relatorios/InterfacePDF.pdf]] · [[fontes/relatorios/InterfacePDF.txt|Texto pesquisável]]
- [[fontes/relatorios/OrquestradorPDF.pdf]] · [[fontes/relatorios/OrquestradorPDF.txt|Texto pesquisável]]
- [[fontes/github/doc-interdisciplinar-4-semestre/main.pdf|Relatório acadêmico atual]] · [[fontes/github/doc-interdisciplinar-4-semestre/main.txt|Texto pesquisável]]
- [[fontes/codigo-app-2026-09-09.zip]] · [[fontes/codigo-orquestrador-2026-09-09.zip]] · [[fontes/codigo-RobotEye-2026-09-09.zip]]
- [[fontes/auditoria/manifesto-fontes.json|Manifesto com hashes e procedência]] · [[fontes/auditoria/repositorios-github.json|Inventário GitHub]]
- [[fontes/vault-anterior-2026-09-09.zip|Backup da documentação anterior]]

O arquivo raiz `MAPA-COMUNICACAO.md` também foi preservado em `fontes/documentos-locais`; a versão viva dentro do repositório orquestrador tem referência Git. Os dois PNGs da marca foram copiados para `fontes/imagens`.

## Hierarquia de evidência

Para comportamento do software, priorizar o código da versão indicada e seus testes, considerando as condições de execução. Para o semestre anterior, usar PDFs com página e preservar a linguagem de relato. Para funcionamento físico, exigir registro de ensaio com versão e ambiente. README e relatório podem conflitar; consultar [[wiki/estado/divergencias]].

**Código local não é prova de implantação.** Branch `producao` não é inspeção do Pi. Teste existente não é teste executado. Dado de demonstração não é coleta física. Plano não é entrega.

## Limites do acervo

Não houve acesso operacional ao Raspberry Pi/VM, execução das suítes do robô/app, leitura de banco real ou reprodução de ensaios. O código foi inspecionado para documentar responsabilidades e contratos; não há promessa de auditoria linha a linha ou cobertura total.

PDFs podem conter erros de extração em comandos, tabelas e caracteres. Para reproduzir um detalhe, conferir o PDF e o código atual. Links GitHub de código estão fixados em SHA, para não mudar de significado quando a branch avançar. O inventário de arquivos é do checkout consultado.

O material privado copiado permanece no computador; nenhuma permissão de compartilhamento foi alterada. As fontes não precisam ser publicadas para que o vault funcione localmente.

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

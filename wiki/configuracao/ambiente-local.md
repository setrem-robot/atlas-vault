---
title: "Ambiente local — testar o caminho dos dados"
tipo: operacao
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - operacao
---

# Ambiente local — testar o caminho dos dados

O repositório `orquestrador` traz scripts Bash para Linux/WSL e Docker. No Windows, esses comandos pertencem ao terminal WSL, não ao PowerShell comum.

Na pasta `orquestrador`, o fluxo documentado é:

```bash
./cloud/scripts/ambiente-local.sh
./cloud/scripts/ambiente-local.sh --robo
```

A primeira etapa sobe/verifica o ambiente. A segunda fornece um robô falso publicando pelo caminho MQTT → ingestor → banco → API. A origem simulada deve ser registrada nos resultados.

```bash
./cloud/scripts/ambiente-local.sh --logs
./cloud/scripts/ambiente-local.sh --endereco
./cloud/scripts/ambiente-local.sh --parar
```

`--endereco` pode mostrar configuração sensível; não colar a saída integral no vault. `--rede` altera exposição/firewall para permitir celular, conforme o script e a rede. Essa alteração deve ser feita conscientemente quando necessária ao teste.

## Conferência ponta a ponta proposta

1. Registrar versão e configuração do ambiente de teste.
2. Confirmar `/saude` e banco acessível.
3. Gerar eventos identificados como simulação.
4. Conferir contagem, timestamps e payloads no banco/API.
5. Configurar o app e verificar as quatro abas.
6. Registrar perda/reconexão de rede e separar esse teste do futuro ensaio de sensor real.

O banco de teste pode conter dados anteriores. Não apagar volumes como etapa padrão de diagnóstico. Não foi executada a opção de zerar o banco durante esta tarefa.

[[wiki/modulos/nuvem]] · [[wiki/planejamento/validacao]].

## Fontes e conferência

- [orquestrador/docs/ambiente-local.md](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/docs/ambiente-local.md)
- [orquestrador/cloud/scripts/ambiente-local.sh](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/scripts/ambiente-local.sh)
- [orquestrador/cloud/scripts/robo-falso.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/scripts/robo-falso.py)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

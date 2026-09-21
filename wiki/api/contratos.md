---
title: "API HTTP e modelo de dados"
tipo: contrato
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - contrato
---

# API HTTP e modelo de dados

## Banco efetivo

Uma tabela `telemetria`, transformada em hypertable TimescaleDB, guarda:

| Coluna | Tipo | Significado |
|---|---|---|
| `ts` | TIMESTAMPTZ | Instante do evento, derivado do payload ou da chegada |
| `tipo` | TEXT | Último segmento do tópico, como gps ou motores |
| `topico` | TEXT | Tópico MQTT recebido |
| `payload` | JSONB | Objeto completo da mensagem |

Índice: `(tipo, ts DESC)`. A política de retenção de 90 dias aparece comentada no SQL; não está ativada por esse arquivo. Não há tabelas separadas chamadas `telemetria_motores`/`telemetria_gps` neste esquema.

## Endpoints GET implementados

| Rota | Acesso | Entrada principal | Saída / uso |
|---|---|---|---|
| `/saude` | Sem token | — | `ok`, `banco`, `token_configurado`, `publico`; 503 se banco indisponível |
| `/v1/estado` | Bearer | — | `gerado_em`, `itens` com `ts`, `idade_s`, `dados` |
| `/v1/trajeto` | Bearer | `desde`, `ate`, `limite` | `pontos`, `total` |
| `/v1/serie/{tipo}` | Bearer | `campo`, `intervalo`, `desde`, `ate` | Média por período e contagem de amostras |
| `/v1/eventos` | Bearer | `tipo`, `limite`, `antes_de` | Eventos crus e cursor `proximo_antes_de` |
| `/v1/publico/resumo` | Público se habilitado | — | Contagem/último evento por tipo, cache curto |
| `/v1/publico/trajeto` | Público se habilitado | `limite` 1–500 | Percurso recente, coordenadas arredondadas |

Não existe `/v1/publico/posicao` no `main.py` atual. A API é de consulta, sem endpoints de escrita/controle do robô.

O token é estático, configurado por `API_TOKEN`, conferido por comparação constante. Não há fluxo de login, JWT com prazo automático ou blacklist no código examinado. Sem token configurado, as rotas privadas recusam acesso.

O limite configurado é 120 requisições por IP por minuto para as portas protegidas/públicas que usam as dependências. `/saude` não usa esse limitador. A confiança em cabeçalhos de proxy depende de `CONFIAR_EM_PROXY` e do caminho real de acesso.

## Exemplo de inspeção local

```powershell
Invoke-RestMethod http://127.0.0.1:8000/saude
```

É um comando de verificação sugerido; não indica que a API está de pé neste computador. As consultas completas exigem a configuração da instalação.

## Qualidade dos dados a melhorar

O banco guarda o objeto recebido, não confirma que ele veio de sensor real. QoS 1 admite reentrega, e o esquema não deduplica por ID de evento. Um payload sem `ts` recebe tempo de chegada. Esses pontos afetam gráficos, atraso e estatística: devem constar no desenho da coleta.

Adicionar identificação de origem real/simulada, timestamp de captura e ingestão, critérios de duplicação e exportação para análise é **proposta de evolução**, não parte já concluída. [[wiki/planejamento/backlog]].

## Fontes e conferência

- [orquestrador/cloud/api/app/main.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/api/app/main.py)
- [orquestrador/cloud/api/app/consultas.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/api/app/consultas.py)
- [orquestrador/cloud/api/app/seguranca.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/api/app/seguranca.py)
- [orquestrador/cloud/timescaledb/init/01_schema.sql](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/timescaledb/init/01_schema.sql)
- [orquestrador/cloud/ingestor/main.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/ingestor/main.py)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

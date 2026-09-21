---
title: "Site e painel da Atlas"
tipo: configuracao
estado_documental: verificado
atualizado: 2026-09-11
tags:
  - atlas
  - site
---

# Site e painel da Atlas

[[wiki/index|Mapa da documentação]] · [[wiki/configuracao/servidor-150|Servidor]]

O site público tem duas áreas com objetivos diferentes:

| Endereço publicado | Finalidade | Código |
|---|---|---|
| `https://atlas.kerlonr.com.br/` | Apresentação do projeto, propósito e componentes | `orquestrador/site/index.html` |
| `https://atlas.kerlonr.com.br/painel/` | Consulta de telemetria pública e trajeto | `orquestrador/site/painel/index.html` |
| `https://atlas.kerlonr.com.br/completo/` | **Análise completa (com token)** de toda a telemetria | `orquestrador/site/completo/` |
| `/api/*` | API existente, encaminhada pelo Caddy | `orquestrador/cloud/caddy/Caddyfile` |

As duas páginas compartilham a identidade visual. O painel é uma superfície de consulta, sem controle de motores. Consome `GET /api/v1/publico/resumo`, `GET /api/v1/publico/trajeto` e `GET /api/v1/publico/saude`, sem token no navegador.

O painel tem um cartão **"Saúde do robô"** (desde 11/09) que mostra a última leitura do Pi: temperatura, processador (com **barras de uso por núcleo**), memória, tempo ligado, frequência/governor/voltagem, swap, disco e rede, além de um estado (leitura recente, alerta de subtensão/limite, ou sem leitura). Vem de `/v1/publico/saude` — rota **sem token** porque a saúde do Pi não revela onde ele está nem carrega segredo, ao contrário do trajeto. Campos em [[wiki/api/contrato-mqtt]].

## Análise completa (com token) — `/completo/`

Para "ver absolutamente tudo", há a página `/completo/` (desde 11/09). Ela **pede o token uma vez** e o guarda **só neste navegador** (`localStorage`/`sessionStorage`); o token vai apenas para a API da Atlas e nunca é embutido no código. Diferente do painel público, ela usa as rotas **com token** (`/v1/estado`, `/v1/eventos`, `/v1/trajeto`), que servem tudo.

O layout é de **console** (desde 11/09): uma **faixa de sinais vitais** no topo mostra o essencial num relance — estado geral (veredito colorido), temperatura, CPU, memória, bateria e tempo ligado, cada um com sparkline e cor de estado (verde/âmbar/vermelho) — e o detalhe fica em **abas** (Saúde do Pi · Sensores · Localização · Eventos), sem rolagem longa. Nas abas: **saúde do Pi com gráficos históricos** (temperatura, CPU, por núcleo, memória, frequência) + núcleos/flags/rede; energia (carga/tensão) e movimento (velocidade) com gráficos; **mapa em precisão total** (desenhado ao abrir a aba); Wi-Fi (conexão + sinal medido pelo Pi); e um **log cru** de eventos, filtrável por tipo e paginado. Os gráficos são SVG desenhados no próprio navegador a partir dos eventos crus (`/v1/eventos`, até 500 por chamada), o que permite traçar campos aninhados como `cpu.por_nucleo`. Um `401/403` apaga o token e volta ao portão. O Caddy serve a página como estático (`file_server`), sem infra nova.

As contagens indicam registros no histórico. Não representam percentual de bateria, velocidade atual ou garantia de que o robô está ligado. A idade vem do horário do último registro; dados antigos ficam identificados. Falha no mapa não deve impedir a leitura do resumo.

## Hospedagem

Cloudflare Tunnel → Caddy → arquivos estáticos ou API. A pasta `site/` é montada como `/srv/atlas`, somente para leitura. A API mantém `/api/` no endereço público; o Caddy remove esse prefixo ao encaminhar. Não é necessário criar outro subdomínio ou projeto Cloudflare Pages para essa estrutura.

A instalação está em `/home/server/docker-stacks/atlas` no host `192.168.1.150`. Nessa instalação, que contém apenas a estrutura cloud, os arquivos ficam em `site/` e o volume usa `./site:/srv/atlas:ro`. No checkout completo do repositório, o compose usa `../site:/srv/atlas:ro`.

Publicação verificada em **11/09/2026**: apresentação, painel, CSS, JavaScript, imagem, saúde da API e as duas consultas públicas responderam HTTP 200 pelo domínio. A configuração do Caddy passou na validação; os testes automatizados do painel passaram. Isso comprova a entrega web e as consultas, não operação física do robô. O banco contém dados de demonstração, e a API pública ainda não os distingue de telemetria física.

Para manutenção, usar `scripts/publicar-site.sh` conforme o README. O script exige sudo, valida a configuração e guarda a versão anterior em `backups/site-<data-hora>/`, dentro da instalação. A publicação inicial preservou `backups/site-20260911-032832/`. Editar o repositório local não atualiza o servidor automaticamente.

## Prévia e manutenção

Executar `python scripts/preview-site.py` no repositório orquestrador. A prévia usa a API pública por um proxy local limitado às rotas de consulta pública. Abrir apenas `index.html` pelo disco pode bloquear dados por CORS.

Conteúdo institucional: `site/index.html`. Painel: `site/painel/index.html` e `site/ao-vivo.js`. Identidade: `site/estilo.css` e `site/assets/atlas.png`. Endereço da API: `site/config.js`. Instruções de publicação: [README do site](../../orquestrador/site/README.md).

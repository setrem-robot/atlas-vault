---
title: "Site, painel e acesso — especificação de evolução"
tipo: planejamento
estado_documental: proposto
atualizado: 2026-09-11
tags: [atlas, site, seguranca]
---

# Site, painel e acesso

[[wiki/planejamento/plano-do-projeto|Plano do projeto]] · [[wiki/site-e-painel|Publicação atual]]

Escopo confirmado: melhorar visual e informações do projeto; consulta geral aberta e dados completos protegidos. Rotas novas e políticas abaixo são propostas, ainda não implantadas. Prioridade geral: demonstração de um robô funcionando.

## Estrutura desejada

| Área | Público | Conteúdo |
|---|---|---|
| `/` — apresentação | Todos | Propósito, robô, capacidades, arquitetura, equipe, evidências e próximos passos |
| `/painel/` — resumo | Todos | Visão geral, origem e idade dos dados; demonstração claramente identificada |
| `/equipe/` — área completa proposta | Convidados autorizados | Estado detalhado, histórico, filtros, gráficos, eventos sanitizados e diagnósticos |

Menu comum: Projeto · Como funciona · Resultados · Equipe · Painel · Entrar. A apresentação carrega mesmo sem API. O botão Entrar deve existir quando houver fluxo funcional de autenticação.

## Uma landing page mais bonita e informativa

Direção visual: manter os olhos e a identidade verde da Atlas; fundo escuro, texto claro, espaços maiores e hierarquia tipográfica consistente. Usar fotografias reais do robô como destaque, diagramas simples e poucas animações discretas. Contraste, foco de teclado e redução de movimento fazem parte do desenho.

| Seção, na ordem da página | Conteúdo necessário | Fonte a preparar |
|---|---|---|
| Abertura | O que é Atlas, para quem existe e contexto SETREM; botões Conhecer o projeto e Ver o painel | Objetivo confirmado; foto atual do robô |
| Problema e proposta | Por que construir a plataforma e o que será demonstrado; separar intenção de resultado | Texto curto revisado pela equipe |
| O que a Atlas faz | Voz/IA, controle, GPS e telemetria; rótulos “validado”, “em validação” e “planejado” | Evidência com versão, data e limite |
| Como funciona | Pessoa → aplicativo/voz → Raspberry Pi → serviços → nuvem; papel de cada repositório | Arquitetura efetivamente adotada; confirmar remoção do ESP32 |
| O robô por dentro | Fotos com identificação de Pi, áudio, motores, alimentação e GPS | Inventário real, sem componentes presumidos |
| Demonstração e resultados | Vídeo curto, descrição acessível e medidas úteis; disponibilidade quando houver evidência | Ensaio PL-05; não usar contagens de registros como prova de operação |
| Equipe e contexto acadêmico | Nomes, papéis confirmados, disciplinas e apoios autorizados | Autoria existente; validar papéis e uso de marcas/fotos |
| Próximas entregas e perguntas | Marcos próximos, limitações e links de código; como participar/acompanhar | Plano central e contato definido pela equipe |

Critérios: leitura confortável a 360 px e desktop; sem rolagem horizontal; teclado e ampliação utilizáveis; imagens otimizadas com dimensões e texto alternativo; vídeo sem reprodução automática; links verificados; título, descrição, imagem de compartilhamento e ícone. Antes da publicação, revisar visualmente a versão candidata e testar a navegação real.

## Dados públicos e dados completos

| Informação | Público proposto | Área autorizada |
|---|---|---|
| Projeto e capacidades | Sim | Sim |
| Origem real/demo e idade | Sempre que houver dado | Sempre |
| Resumo | Indicadores agregados e permitidos | Indicadores detalhados por tipo |
| Localização | Preferir área geral ou percurso demonstrativo identificado | Trajeto real e filtros conforme permissão |
| Bateria, motores e GPS | Somente campos explicitamente aprovados | Medidas disponíveis, unidades, qualidade e instante |
| CPU, memória e temperatura | Opcional, resumido | Histórico depois de validar produtor e contrato |
| Eventos técnicos | Não | Campos permitidos, filtros e limite de resposta |
| Áudio e transcrições | Não | Fora da primeira versão; exigem finalidade, acesso e retenção definidos |
| Credenciais | Nunca | Nunca |

O endpoint público atual arredonda coordenadas para quatro casas, mas arredondamento não garante anonimato de um trajeto. A publicação de localização real precisa de uma escolha explícita. A política proposta não altera agora o endpoint existente.

`/v1/estado`, `/v1/trajeto`, `/v1/serie/{tipo}` e `/v1/eventos` já existem com Bearer compartilhado. É possível reutilizar as consultas; isso não fornece contas individuais. Exportação CSV, seleção de período e filtros são extensões propostas, com os mesmos limites e permissões das consultas.

## Login recomendado para a primeira equipe

Hipótese de planejamento: entrada por convite, sem cadastro público. Para esta fase, avaliar **Cloudflare Access**, aproveitando o túnel existente. Ele permite proteger caminhos específicos, mantendo apresentação e resumo públicos. É uma recomendação de arquitetura; configurações, conta, limites e custos precisam ser conferidos antes de adotar. [Documentação de caminhos do Access](https://developers.cloudflare.com/cloudflare-one/access-controls/policies/app-paths/).

Desenho proposto: proteger `/equipe` e seus subcaminhos e criar uma entrada autenticada `/api/equipe/*`. A API valida identidade e aplica permissões antes de reutilizar as consultas existentes. Verificar explicitamente correspondência da rota base e de seus subcaminhos na configuração do Access.

Não proteger todo `/api/*` indiscriminadamente: isso afetaria o painel público e o app Flutter. Manter as rotas atuais do app durante uma migração planejada; o token compartilhado continua sendo uma limitação até substituí-lo por acesso individual. Não colocar esse token no JavaScript nem usar cabeçalho de e-mail sem validação como identidade.

O backend deve verificar assinatura, emissor, audiência e validade do JWT do Access, além de acesso ao recurso; o caminho direto até a origem não pode contornar isso. [Validação oficial de JWT](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/validating-json/).

Se a meta passar a ser contas comuns entre aplicativo e web, cadastro amplo ou múltiplas organizações, avaliar um provedor OIDC para ambos. Essa escolha exige modelar usuários, associações a robôs e revogação, além de integrar o login no app. Evitar criar armazenamento próprio de senhas como primeira entrega.

## Permissões e sessão

Perfis propostos: **visitante** lê dados públicos; **integrante** consulta dados autorizados; **administrador** gerencia acesso. Login no painel não concede controle de motores. Começar com política simples para um robô e negar acesso por padrão; acrescentar vínculo usuário/robô antes de expandir.

Para sessões próprias de uma eventual implementação OIDC, usar cookies Secure/HttpOnly, SameSite compatível com o fluxo, expiração e encerramento efetivo; proteger operações de alteração contra CSRF. No caminho Access, documentar a expiração e revogação reais oferecidas pela configuração escolhida. O botão sair deve limpar também a tela e o estado privado mantido no cliente. [Orientação OWASP sobre sessões](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).

Permissão precisa ser validada em cada consulta e exportação. Respostas privadas usam política que impeça cache compartilhado; separar claramente caches públicos e privados. Registrar ações de acesso/administração sem tokens, senhas ou payload sensível. [Orientação OWASP sobre autorização](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).

## Experiência do painel completo

Cabeçalho com robô, origem dos dados e última atualização. Visão geral com valores reais disponíveis; navegação para Histórico, Trajeto e Diagnóstico. Filtros de período e tipo; unidade nos gráficos; estado vazio, atraso, erro parcial e sessão expirada. Dados simulados devem ser selecionáveis e identificados, sem se misturar silenciosamente à medição real.

A interface deve distinguir “comando enviado”, “comando aceito” e “movimento medido” conforme o contrato permitir. Um estado de motor comandado não comprova que a roda se moveu. Ao expirar sessão, interromper consultas e orientar reentrada.

## Sequência e aceite

1. Recuperar e versionar a base publicada; registrar política de dados públicos.
2. Preparar textos, imagens e layout da landing; implementar PL-06 com identidade comum.
3. Definir campos e corrigir origem/idade/qualidade, concorrência e limites de consultas (PL-04).
4. Configurar login em ambiente de teste; integrar validação de identidade no backend e perfis.
5. Entregar visão geral privada; depois histórico, gráficos e trajeto. Exportação entra após limites e permissões.
6. Testar visitante, integrante, administrador, usuário removido e sessão expirada. Tentar acesso direto sem identidade, JWT inválido, caminho alternativo e recurso sem permissão; não receber dados privados.
7. Conferir que o público continua aberto e o app continua consultando sua API. Validar ausência de segredos em HTML/JS, cache e logs; revisar visualmente desktop/celular; preparar rollback antes do deploy.

Fontes locais: `orquestrador/cloud/api/app/main.py`, `seguranca.py` e `consultas.py`; [[wiki/site-e-painel]] e [[wiki/planejamento/plano-do-projeto]]. As referências externas foram consultadas em 11/09/2026.

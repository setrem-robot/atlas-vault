---
projeto: Atlas
atualizado: 2026-09-09
status: revisao-historica
---

[[INICIO|Início]] · [[wiki/planejamento/prioridades|Andamento das correções]]

> [!info] Retrato datado
> Relatório preservado da revisão. O andamento das correções fica no quadro de prioridades.

# Revisão técnica — Atlas / Setrem Robot

Data: 9 de setembro de 2026.

## Parecer

**A arquitetura oferece uma boa base modular, mas a versão revisada ainda não está pronta para expansão confiável para vários robôs.** Antes de aumentar infraestrutura, há falhas de controle, conexão com banco e entrega de dados que precisam ser corrigidas. Para um único robô, a prioridade é confiabilidade operacional; para uma frota, também será necessário introduzir identidade e isolamento por robô em toda a cadeia.

Escalabilidade de capacidade não foi demonstrada: testes unitários não medem quantos clientes, mensagens ou inferências simultâneas a instalação suporta. Não há neste relatório uma capacidade máxima inventada.

## Escopo e versões

Consultei a [organização Setrem Robot](https://github.com/setrem-robot) e revisei os três componentes: IA/face/voz/BLE, orquestrador/serviços/cloud e aplicativo Flutter. Examinei os caminhos principais, contratos, configuração de implantação e automação; executei testes disponíveis e reproduções isoladas dos problemas prioritários.

| Componente | Commit examinado | Origem |
|---|---|---|
| atlas_ai_v2 | `e1b26d78f1f9b5ccb1f33c122203d791fa20ad44` | Cópia separada da versão publicada no GitHub |
| orquestrador | `98ee681498e05426ff47041ae7f8e7ec97d0ffaf` | Cópia local limpa, HEAD conferido com GitHub |
| aplicativo | `44d500160ecf13d7d1db2a4fe0c54052d352c0aa` | Cópia local limpa, HEAD conferido com GitHub |

A IA local estava no commit `43a6fe0`; a revisão usou o commit publicado acima. Nenhum código de produção foi alterado. Não foram acionados motores, serviços de produção, atualizações OTA ou APIs operacionais. Não inspecionei arquivos de segredos.

Limites: sem ensaio no Raspberry Pi, BLE físico, motores, GPS, servidor de IA, broker e banco reais. Docker não estava disponível no PATH. Não verifiquei as configurações efetivamente aplicadas à VM, firewall, backups externos ou proteção de branches. Assim, configuração versionada e comportamento observado em produção são coisas distintas.

## O que vale preservar

- Separação entre lógica e infraestrutura em roteamento, cinemática e acesso a dados: facilita testes e evolução por equipe.
- Controle de movimento local e vigia de silêncio: a conexão com a nuvem não precisa participar do caminho de parada.
- Interface de acionamento simulado, rampa e proteção de concorrência no serviço de motores.
- MQTT como fronteira entre serviços; biblioteca comum de tópicos no orquestrador.
- Banco temporal com índice por tipo e tempo; consultas parametrizadas e limites em vários endpoints.
- Usuário de leitura separado e processo da API sem root no container.
- Alternância entre IA de rede e local, streaming da resposta e organização do áudio por interfaces.
- Testes numerosos e documentação explícita sobre trabalho ainda não concluído.

Essas escolhas ajudam a evoluir o sistema. Elas não eliminam os defeitos abaixo, nem provam a capacidade da instalação.

## Achados prioritários

Prioridades: **P0** corrigir antes de operar movimento real; **P1** corrigir antes de uso compartilhado/expansão; **P2** evolução necessária para manutenção e crescimento. “Reproduzido” significa uma execução isolada com o código indicado ou driver real; não significa reprodução em hardware.

### 1. P0 — App pode enviar movimento novamente depois de STOP

**Reproduzido em Dart, com o método `send` extraído sem alterações e transporte substituído por futures controladas.**

Em [robot_connection.dart, linha 167](https://github.com/setrem-robot/aplicativo/blob/44d500160ecf13d7d1db2a4fe0c54052d352c0aa/lib/services/robot_connection.dart#L167), `send` cancela o timer antes de aguardar `_write`. Se “frente” ainda está aguardando quando chega “parar”, ambas as chamadas cancelam o timer antigo; depois a primeira instala um timer novo. A conclusão da parada não cancela esse novo timer.

Resultado obtido: `writes=[forward, stop, forward]; lastCommand=stop`. O app pode mostrar parada enquanto continua repetindo movimento. Como chegam comandos novos, o vigia de silêncio dos motores não resolve esse caso.

**Correção:** invalidar chamadas anteriores com geração/sequência de comando, conferir essa geração depois de cada `await` e permitir repetição apenas do comando vigente. Parada/desconexão deve invalidar qualquer operação pendente. Acrescentar tratamento explícito de perda de foco do app.

**Aceite:** testar pressão/soltura rápida, trocas de direção, parada durante escrita e desconexão durante escrita; nenhuma operação anterior pode rearmar movimento.

### 2. P1 — String de conexão da API é inválida

**Reproduzido com o parser real do psycopg 3.3.5, sem abrir conexão.**

[banco.py, linha 48](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/api/app/banco.py#L48) monta `options=-c statement_timeout=8000`. Sem delimitar o valor que contém espaço, `statement_timeout` é interpretado como outra opção de conexão. Resultado: `ProgrammingError: invalid connection option "statement_timeout"`.

A substituição isolada por `options='-c statement_timeout=8000'` passou no parser. O formato da string atual impede conexões bem-sucedidas do pool; não foi consultada a API implantada para verificar se usa esse mesmo código.

**Correção:** preferir parâmetros estruturados/gerador de conninfo, incluindo escaping de usuário, senha e demais valores. A [documentação libpq](https://www.postgresql.org/docs/current/libpq-connect.html) descreve a delimitação de valores com espaços.

**Aceite:** parser real, conexão real, `SHOW statement_timeout` igual a 8000 ms e consulta longa efetivamente cancelada. Os testes atuais de substring passam mesmo com a configuração inválida.

### 3. P1 — Consultas bloqueiam o atendimento concorrente da API

**Reproduzido chamando a rota real com consulta substituída por espera controlada.**

[main.py, linha 182](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/api/app/main.py#L182) usa `async def`, mas chama `Banco.consultar`, que executa psycopg síncrono. O mesmo padrão aparece em outras rotas e na saúde. O Dockerfile inicia um único worker.

Uma consulta simulada de 200 ms atrasou um timer de 10 ms para aproximadamente **212 ms**. Isso demonstra bloqueio do event loop, não é benchmark do banco. Quatro conexões no pool não tornam essas chamadas concorrentes dentro do único event loop.

**Correção:** usar acesso assíncrono ao banco ou deslocar a operação bloqueante para execução em threads. Rotas síncronas são uma opção, revisando a segurança de concorrência dos caches e do limitador compartilhado. A distinção é explicada na [documentação do FastAPI](https://fastapi.tiangolo.com/async/).

**Aceite:** requisição lenta não deve bloquear saúde e requisições rápidas; medir p95/p99 sob carga concorrente.

### 4. P1 — Comandos antigos podem ficar na fila MQTT

**Fila offline reproduzida com o cliente Paho real; efeito nos motores é inferência do caminho de código.**

[ble/mqtt.py, linha 71](https://github.com/setrem-robot/atlas_ai_v2/blob/e1b26d78f1f9b5ccb1f33c122203d791fa20ad44/src/roboteye/ble/mqtt.py#L71) publica comandos com QoS 1, sem prazo de validade, sequência ou verificação de resultado. O serviço de motores carimba a chegada como movimento novo em [main.py, linha 239](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/motores/src/motores/main.py#L239).

No cliente desconectado, publicar “frente” e “parar” devolveu erro de ausência de conexão, mas manteve ambas as mensagens na fila de saída. Sem descarte por idade, uma reconexão pode reintroduzir comandos que já perderam o sentido.

**Correção:** política própria para movimento: sessão do controlador, sequência, validade curta e descarte de comandos vencidos; impedir fila histórica de movimento e priorizar parada. QoS deve ser escolhido junto com essa política. A [API do Paho](https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html) documenta resultados de publicação e controle de filas.

**Aceite:** derrubar/reconectar o broker com movimento pendente; nenhum comando vencido pode acionar o motor. Não basta verificar que o tópico usa `retain=False`.

### 5. P1 — A cadeia não garante histórico sem perdas nem duplicações

Em [ingestor/main.py, linha 101](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/ingestor/main.py#L101), o cliente não configura sessão persistente. A inscrição é refeita após conectar; mensagens durante ausência do ingestor não têm garantia de retenção como histórico dessa assinatura. Mensagens retidas recuperam somente o último estado por tópico.

A gravação acontece dentro do callback MQTT, com um `INSERT` por mensagem e autocommit. Reconectar ao banco entra em laço bloqueante; após falhas de gravação o código pode descartar o registro. O schema não tem identificador único de evento para deduplicação. Reiniciar, reassinar tópicos retidos ou receber retransmissões pode gerar duplicatas.

**Correção:** definir garantia ponta a ponta, sessão persistente, identidade de evento, escrita idempotente e confirmação após persistência durável. Separar recepção e gravação com fila limitada e estratégia de recuperação; considerar lote de escrita conforme medições. Não adicionar várias réplicas iguais: o `client_id="ingestor"` colide e assinaturas comuns não distribuem carga automaticamente.

**Aceite:** matar o ingestor, indisponibilizar banco, repetir eventos e reconectar bridge; comparar eventos produzidos e persistidos. A fila de 100 mil mensagens no Pi protege apenas parte do percurso.

### 6. P1 — Vários robôs misturam telemetria

Os [tópicos comuns](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/_common/src/robo_common/topics.py#L9) usam raiz fixa `robo`. O [schema](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/timescaledb/init/01_schema.sql#L16) armazena `ts`, `tipo`, `topico`, `payload`, sem identidade obrigatória de robô. API e aplicativo também não selecionam robô nas consultas.

Dois robôs publicando no mesmo backend podem produzir um estado composto de fontes diferentes e um trajeto misturado. Brokers locais separados evitam colisão local, mas não fornecem identidade no histórico central.

**Correção:** introduzir `robot_id` obrigatório no contrato e banco, namespace por robô na nuvem, filtros/autorização na API e seleção no app. Acrescentar versão de schema, identificador de evento e horário de geração. Os tópicos locais podem permanecer simples se a bridge fizer mapeamento explícito e verificável.

**Aceite:** dois simuladores simultâneos, identificadores distintos, trajetos separados e credenciais sem acesso cruzado.

### 7. P1 — Credenciais Wi-Fi são registradas nos logs

**Reproduzido com senha fictícia e logger interceptado.**

[ComandoWifi](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/orquestrador/src/orquestrador/roteador.py#L218) repassa `senha` e `password`. O [handler de roteamento](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/orquestrador/src/orquestrador/main.py#L78) registra o payload completo. A ponte serial também registra o payload de entrada.

**Correção:** registrar campos permitidos, como tipo, ação, destino e identificador de correlação; ocultar credenciais em todos os caminhos de erro. Verificar o alcance dos logs existentes antes de decidir rotação de credenciais.

**Aceite:** teste com sentinela fictícia garante ausência de senha em logs de sucesso e falha.

### 8. P1 — Controle BLE não exige autorização no código revisado

Em [nus.py, linha 193](https://github.com/setrem-robot/atlas_ai_v2/blob/e1b26d78f1f9b5ccb1f33c122203d791fa20ad44/src/roboteye/ble/nus.py#L193), a característica permite escrita sem flags de autenticação/criptografia; o callback entrega o objeto recebido sem credencial de aplicação. O PIN protege a interface HTTP, não esse caminho BLE.

**Correção:** autenticação/pareamento apropriado ao hardware, autorização de controlador, sessão exclusiva e procedimento de provisionamento. Confirmar as configurações efetivas do BlueZ antes de concluir a exposição física da instalação.

**Aceite:** dispositivo não autorizado não pode enviar comandos de motor nem alterar Wi-Fi; reconectar não transfere controle implicitamente.

### 9. P1 — Proteção de transporte e permissões cloud é incompleta no modelo versionado

O [compose cloud](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/docker-compose.yml#L24) publica MQTT em `1883:1883`; o broker usa senha, sem TLS ou ACL por tópico no arquivo revisado. A bridge apresenta TLS apenas como configuração opcional. HTTPS do túnel da API não protege automaticamente esse tráfego MQTT. Firewall/VPN reais não foram verificados.

O ingestor recebe o mesmo usuário configurado como `POSTGRES_USER`, ampliando seu privilégio; o app guarda um token global em SharedPreferences e aceita URL HTTP, útil no desenvolvimento, mas inadequado como padrão de produção compartilhada.

**Correção:** transporte protegido entre redes, credenciais individuais, ACL por robô, usuário de ingestão com privilégio mínimo e credenciais de leitura revogáveis por usuário/dispositivo. Separar configuração de desenvolvimento; guardar token no armazenamento seguro do sistema e exigir HTTPS em produção.

### 10. P1 — Rollback da IA pode manter dependências da versão que falhou

Em [atualizar.sh, linha 154](https://github.com/setrem-robot/atlas_ai_v2/blob/e1b26d78f1f9b5ccb1f33c122203d791fa20ad44/scripts/atualizar.sh#L154), `aplicar(alvo)` compara dependências entre `ATUAL` e o alvo. Ao voltar para `ATUAL`, a comparação vira o commit antigo contra ele mesmo. Se a atualização instalou dependências novas e falhou, o retorno do código pula a restauração dessas dependências.

**Correção:** releases com ambiente de dependências próprio e versões fixadas, com troca atômica de versão e rollback do conjunto código+ambiente. Há um mecanismo de rollback implementado; o problema é ele não restaurar integralmente a execução.

**Aceite:** atualização que muda dependência e falha no healthcheck deve voltar ao código e às versões anteriores. Este achado é análise estática; o script não foi executado.

### 11. P2 — Consultas e crescimento do banco precisam de orçamento explícito

[consultas.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/api/app/consultas.py#L136) permite série de até 90 dias com bucket de um minuto: aproximadamente **129.600 intervalos**, sem teto de pontos nessa rota. `resumo()` conta o histórico inteiro; o cache diminui frequência, mas não custo de cada atualização. A retenção está comentada no schema.

**Correção:** teto de pontos com escolha automática de intervalo, agregações mantidas previamente quando justificadas, retenção e arquivamento definidos. Medir `EXPLAIN (ANALYZE, BUFFERS)` com massa representativa. `time_bucket` não implica que os agregados estejam pré-computados.

**Aceite:** consultas de 1/30/90 dias têm limite de resposta e latência acordados; projeção de disco inclui índices, WAL, backups e folga.

### 12. P2 — Contrato permite inconsistências de tempo, formato e paginação

O ingestor aceita qualquer objeto JSON, mas consultas convertem campos diretamente para booleano/número. Um valor incompatível pode quebrar consultas do período. Eventos são paginados apenas por `ts < cursor`: quando vários têm o mesmo timestamp e a página termina nesse grupo, o restante pode ser omitido.

Também reproduzi `TypeError` em `janela(datetime sem fuso, None)`: datas recebidas sem offset podem ser comparadas com UTC consciente de fuso. O status de motores é publicado sem `ts`, então o ingestor usa horário de chegada; replay pode fazer estado antigo parecer novo.

**Correção:** validação por tipo e versão na entrada, campos numéricos finitos, horário de geração obrigatório e separado da recepção, normalização/exigência de UTC e cursor composto estável. Para eventos históricos, identidade idempotente deve fazer parte do contrato.

**Aceite:** testar timestamp repetido, data sem fuso, payload malformado, replay e relógio incorreto do produtor.

### 13. P2 — Servidor de configuração lê corpo sem limite antes do PIN

[server.py, linhas 186–239](https://github.com/setrem-robot/atlas_ai_v2/blob/e1b26d78f1f9b5ccb1f33c122203d791fa20ad44/src/roboteye/web/server.py#L186) usa ThreadingHTTPServer, lê `Content-Length` sem teto nem timeout explícito e só depois verifica o PIN. O bind padrão é `0.0.0.0`, por HTTP. O bloqueio por tentativas também é global, podendo afetar o operador legítimo.

**Correção:** autenticar antes de ler ações protegidas, limitar tamanho/tempo/conexões, restringir acesso à rede de administração e proteger transporte. Serializar a operação completa de salvar/validar/reverter configuração: há lock de ambiente, mas não de toda a transação de arquivo.

**Aceite:** requisição lenta/grande não consome recursos sem limite e duas alterações simultâneas não perdem atualização.

### 14. P2 — Instalação ainda depende de escolha manual de broker

O setup da IA instala/inicia Mosquitto pelo apt; o orquestrador também oferece compose na mesma porta. **Já existe** aviso no instalador e exemplo de configuração apt; portanto não é ausência total de tratamento. Ainda falta uma instalação integrada e verificável que escolha um único dono e aplique a bridge correta.

**Correção:** manifesto de instalação comum e preflight: broker escolhido, porta, caminhos, bridge, serviços consumidores e healthcheck ponta a ponta. Documentação deve refletir a opção implantada.

**Aceite:** instalar duas vezes em cartão limpo produz um broker, sem conflito de porta e com telemetria chegando à nuvem.

### 15. P2 — Testes e entrega não cobrem as fronteiras críticas

Há CI de testes/lint/tipos na IA. No orquestrador, a pasta `.github` examinada contém dependabot, sem workflow de testes. No app, o workflow publica patch/release, sem etapa `flutter test` ou análise estática antes da entrega. Proteções externas de branch não foram verificadas.

Os testes atuais não detectaram os achados 1–3. Também não foi encontrada suíte do ingestor na árvore examinada. Na IA, o teste de FPS falhou na suíte e passou isoladamente, indicando sensibilidade a tempo/carga/ordem; não demonstra defeito de FPS no Pi.

**Correção:** testes obrigatórios antes de merge/deploy, integração com Mosquitto e TimescaleDB descartáveis, testes de contrato entre repositórios e ensaios de interrupção de rede/processos. Substituir expectativas de tempo real por relógio controlado onde o requisito é lógica.

### 16. P2 — Operação e recursos precisam ser mensuráveis

O compose central reúne serviços em uma instalação com volumes locais. Nas configurações examinadas não encontrei automação de backup/restauração, migração incremental do schema nem painel/alertas de capacidade. Isso não prova que não existam fora do repositório.

A IA oferece fallback e gerenciamento de memória, mas face, escuta e inferência local competem por recursos do Pi. O assistente tem fila sem teto; embora descarte mensagens antigas ao iniciar o próximo turno, ela pode crescer enquanto a inferência atual está ocupada. A interrupção de voz não cancela por si só toda a geração em andamento.

**Correção:** backup com restauração ensaiada, migrações versionadas, versões de dependências/imagens reproduzíveis e métricas de latência, CPU, RAM, temperatura, filas, disco e atraso da telemetria. Definir política de cancelamento e admissão de mensagens. Isolar o controle de movimento da pressão computacional da IA e ensaiar uma parada independente do processo principal.

**Aceite:** teste prolongado de operação simultânea e queda/retorno de rede, sem crescimento contínuo de memória, sem replay de movimento e com objetivos de recuperação documentados.

## Escalabilidade por dimensão

| Dimensão | Avaliação | Próximo passo |
|---|---|---|
| Equipes e novos módulos | Base modular favorável; contratos duplicados entre linguagens | Contrato versionado e testes de compatibilidade |
| Um robô em demonstração | Corrigir controle e validar integração real | Achados 1–5; ensaio supervisionado |
| Um robô em uso prolongado | Capacidade térmica e recuperação não medidas nesta revisão | Teste combinado de IA/voz/face/motores/rede |
| Mais leitores da API | Bloqueio síncrono e consultas históricas limitam evolução | Corrigir I/O e medir carga |
| Vários robôs | Identidade/isolamento ausentes no caminho central | `robot_id`, namespace, ACL e UI |
| Histórico de meses | Armazenamento cresce sem política ativa de retenção | Retenção, agregação, dimensionamento |
| Alta disponibilidade | Compose atual não demonstra redundância/recuperação | Primeiro restauração testada; redundância conforme necessidade |

### Projeção de volume — cenário, não benchmark

Assumindo **2 mensagens por segundo por robô, continuamente**:

| Robôs | Mensagens/s | Mensagens/dia | Mensagens/90 dias |
|---:|---:|---:|---:|
| 1 | 2 | 172.800 | 15.552.000 |
| 10 | 20 | 1.728.000 | 155.520.000 |
| 100 | 200 | 17.280.000 | 1.555.200.000 |

A premissa deve ser substituída pela taxa observada. Mensagens JSON de 200 bytes não equivalem ao custo de uma linha persistida com índice, WAL e backups. A fila de 100 mil mensagens corresponderia a cerca de 13,9 horas a 2/s, antes de considerar teto de bytes, mensagens em trânsito, frequência de persistência e outros limites.

### Validação de capacidade proposta

1. Corrigir os defeitos de conexão/concorrência e montar ambiente de teste separado.
2. Carga de ingestão em degraus de 2, 20 e 200 msg/s, com replay de backlog; medir atraso, duplicação, perdas e disco.
3. Leitores simultâneos em degraus de 1, 10 e 50; variar estado, trajeto e séries, com massa histórica representativa.
4. Interromper broker, ingestor e banco separadamente; verificar recuperação pela identidade de eventos.
5. Rodar no Pi a carga combinada por várias horas, com rede presente/ausente; registrar temperatura, frequência, memória, latência da voz e de parada.

Esses números são degraus de ensaio, não promessa de suporte. Critérios iniciais para pactuar: p95 de leitura interativa abaixo de 500 ms no cenário-alvo, nenhum movimento por comando vencido, recuperação sem perda dos eventos aceitos dentro da janela definida. O tempo seguro de parada deve ser determinado e medido com o conjunto físico.

## Plano de execução recomendado

| Ordem | Entrega | Evidência para concluir |
|---|---|---|
| 1 | Corrigir corrida de STOP e descarte de comandos antigos | Testes de concorrência e reconexão, depois ensaio físico controlado |
| 2 | Corrigir conninfo e I/O da API | Conexão real, timeout real e requisições concorrentes |
| 3 | Fechar vazamento de logs e autorização de comandos | Credencial fictícia ausente dos logs; cliente não autorizado recusado |
| 4 | Tornar ingestão recuperável e idempotente | Teste de falha com reconciliação dos eventos |
| 5 | Automatizar integração e implantação reproduzível | CI nos três repositórios, instalação limpa e rollback completo |
| 6 | Introduzir identidade de robô, retenção e recuperação | Dois robôs isolados e backup restaurado |
| 7 | Medir capacidade e dimensionar recursos | Relatório de carga e operação prolongada |

Manter MQTT, Python, Flutter e TimescaleDB é compatível com esse plano. A revisão não encontrou evidência que justifique trocar toda a stack. Aumentar máquinas ou adotar um orquestrador de containers não corrige identidade, replay, bloqueio de I/O ou perda de dados.

## Verificação executada

Ambiente: Windows, Python 3.12.10, dependências em ambiente virtual isolado. Bibliotecas usadas incluem psycopg 3.3.5, psycopg-pool 3.3.1, Paho 2.1.0 e FastAPI 0.141.1. Não se trata de reconstrução exata do ambiente de produção, pois as dependências Python usam limites inferiores sem lock na configuração examinada.

| Verificação | Resultado |
|---|---|
| IA, suíte completa com SDL dummy | 781 testes coletados/executados; 1 falha de FPS, demais sem falha indicada |
| Reexecução isolada do teste de FPS | 1 passou; investigar fragilidade temporal/ordem |
| Orquestrador/API/motores/Wi-Fi | 135 passaram, além de 14 subtestes; 2 avisos de depreciação |
| Aplicativo, `flutter test --no-pub` | 32 passaram |
| Conninfo com parser real | Falha reproduzida; aspas no valor de options corrigem o parse |
| Concorrência da rota de estado | Timer de 10 ms atrasado para 212 ms com I/O simulado de 200 ms |
| Método Dart de envio, futures controladas | Sequência frente → parada → frente reproduzida |
| MQTT offline, sem broker | Dois comandos QoS 1 permaneceram na fila apesar do retorno de desconexão |
| Log de provisionamento Wi-Fi | Senha fictícia aparece nos argumentos do logger |
| Datas sem fuso | Comparação naive/aware levanta TypeError |

Também apareceram erros de logging para stream fechado durante a suíte da IA; isso deve ser investigado no isolamento dos testes. Não executei testes de carga reais, auditoria completa de dependências, lint/tipagem completos ou validação elétrica/mecânica. O parecer cobre arquitetura, caminhos críticos de código e verificações descritas, sem certificar toda execução possível do sistema.

**Decisão recomendada:** preservar a arquitetura modular e abrir primeiro as correções de controle e conectividade; concluir confiabilidade e medição antes de assumir operação contínua ou expandir para frota.

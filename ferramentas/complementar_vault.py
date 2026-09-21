"""Registro da construção inicial. Não executar depois de editar as notas."""
from montar_vault import V, R, DATE, SHA, REMOTE, note, source
from pathlib import Path
import json
import subprocess
import shutil
from urllib.parse import quote

audits = sorted((V/'fontes/auditoria').glob('git-*.json'))
audit = json.loads(audits[-1].read_text(encoding='utf-8'))
collection = 'wiki/estado/coletas/' + audits[-1].stem

note('wiki/estado/git-local-e-remoto.md','Git — publicado, local e instalado',f'''
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

- [[{collection}|Coleta completa com todas as branches e SHAs locais]]
- [[fontes/auditoria/equivalencia-branches.json|Resultado de equivalência de árvores e patches]]
- [[wiki/meta/historicos-git|Histórico completo coletado por repositório]]

No PowerShell:

```powershell
python D:\\SetremRobot\\AtlasVault\\ferramentas\\atualizar_git.py --fetch
```

Cada execução cria novos arquivos com data/hora, preservando os anteriores. O script não publica, mescla nem altera código. Sem `--fetch`, o retrato usa referências possivelmente antigas. Revise esta nota e o estado atual após uma nova coleta; a narrativa não é reescrita automaticamente.
''','estado',sources=[f'[[{audits[-1].relative_to(V).as_posix()}]]','[[fontes/auditoria/equivalencia-branches.json]]',source('RobotEye','scripts/roboteye-update.service')])

note('wiki/estado/divergencias.md','Divergências — o que ainda precisa de confirmação','''
As divergências ficam visíveis para evitar transformar fontes antigas em fatos atuais. Nenhuma foi resolvida por suposição.

| ID | Questão | Evidências em conflito | Tratamento / ação |
|---|---|---|---|
| D01 | GPS está montado? | PDF Orquestrador p. 38 declara integração; README atual diz módulo não montado; usuário pede implementar | Serviço existente; instalação atual pendente de inspeção e teste |
| D02 | Robô já se move com o código atual? | Narrativas gerais dizem sistema funcional; Estrutura p. 26 e README motores registram validação pendente | Não declarar movimento validado sem ensaio físico com SHA |
| D03 | API está no LARCC? | LaTeX/relatório citam LARCC; README informa PC provisório | Confirmar host, serviço, persistência e responsável |
| D04 | Pi precisa do ESP32? | Contrato e comentários antigos dizem não haver Bluetooth no Pi; código RobotEye implementa BLE direto | Arquitetura atual usa Pi; atualizar fontes antigas em tarefa futura |
| D05 | IA já usa MQTT? | README simplifica o contato à ponte; `web/comandos.py` também usa MQTT | Documentar ponte e painel; integração de fala/telemetria continua pendente |
| D06 | Rampa suportada? | Estrutura p. 20 fala 20°; p. 22 fala 5–7°; testes motorizados não realizados | Manter como requisitos divergentes, sem capacidade certificada |
| D07 | Ano/PIE da origem? | Capa Estrutura 2025; conteúdo 2026/PIE V; relatório atual PIE IV | Usuário define a entrega anterior; datas e numeração precisam de confirmação acadêmica |
| D08 | Modelo/áudio/SO históricos? | Interface usa “Gemma 3B”, P2, Bookworm/Trixie; README atual descreve outros modelos e áudio USB | Preservar relato; conferir artefatos/modelos e hardware atuais |
| D09 | Memória da face? | README reconhece 130–145 MB vs 70 MiB em medições distintas | Repetir medição com versão/configuração, não escolher número por conveniência |
| D10 | Retenção e perda de dados? | README estima horas de fila; código limita mensagens/bytes e ingestor pode descartar | Ensaiar queda de conexão e banco, contabilizar perdas/duplicatas |
| D11 | Rota segura é autonomia? | App envia pontos; não há consumidor em `robo/rota/comando` | Planejamento de rota implementado; execução autônoma futura |
| D12 | Commit local é melhoria inédita? | SHAs locais fora do remoto, mas árvores idênticas a squashes publicados | Usar a análise Git antes de planejar push/merge |

## Correções no vault anterior

O backup anterior foi preservado em [[fontes/vault-anterior-2026-09-09.zip]]. A documentação ativa foi revisada para corrigir comandos F/B/L/R/S, tópicos reais, endpoints reais, tabela única de telemetria, parada imediata no software, status comandado e limitações de segurança. Foram removidas afirmações sem sustentação de cobertura “100%” e origem em “monografia”.

Para fechar uma divergência, adicionar fonte nova, data, versão, resultado e responsável; depois atualizar as notas relacionadas. Não apagar silenciosamente a evidência antiga. [[wiki/meta/como-usar]].
''','estado',sources=['[[wiki/historico/relatorios-semestre]]','[[wiki/historico/relatorio-atual]]','[[wiki/estado/git-local-e-remoto]]',source('orquestrador','README.md'),source('RobotEye','README.md')])

note('wiki/planejamento/onde-queremos-ir.md','Onde queremos ir — melhoria geral da Atlas','''
## Direção confirmada pelo usuário em 09/09/2026

Melhorar o projeto como um todo: retirar o ESP32 e manter somente o Raspberry Pi no robô, melhorar a IA e o controle, implementar o GPS e melhorar a comunicação com o banco e a apresentação das informações.

“Somente o Raspberry Pi” foi interpretado como simplificação da eletrônica embarcada e retirada da ponte ESP32. Não foi inferido que a equipe quer proibir a IA opcional em outra máquina ou remover o banco remoto. Essas escolhas adicionais ainda podem ser discutidas.

## Tradução em entregas verificáveis — proposta

| Frente | Resultado desejado | O que já existe | Evidência proposta de conclusão |
|---|---|---|---|
| Um Pi no robô | Operar sem ESP32/serial intermediária | Ponte BLE no Pi | Inicializar sem ESP32, controlar e parar; foto e logs |
| IA melhor | Respostas mais úteis e interação consistente | Ollama, motores de voz, Vosk, reserva e painel | Comparação antes/depois com perguntas fixas e tempos registrados |
| Controle melhor | Movimento previsível e retorno claro | Direcional, repetição, vigia e telas | Ensaios de botão, desconexão, troca de tela e backend real |
| GPS implementado | Posição real disponível e válida | Leitor NMEA e contrato | Amostras físicas até MQTT, banco e mapa, incluindo perda de fix |
| Dados melhores | Informação recente, íntegra e compreensível | Bridge, TimescaleDB, API, app e site | Origem/tempo explícitos, reconexão testada e dados exportáveis |
| Projeto bem documentado | Outra equipe consegue entender e reproduzir | Código, relatórios e este vault | Decisões, instalação, testes e evidências ligados às versões |

## Sequência sugerida

1. **Consolidar base:** inventário físico, versões instaladas, broker único e operação sem ESP32.
2. **Controle e IA:** validar motores/parada e medir conversa, áudio, escuta e estabilidade.
3. **GPS e dados:** ligar sensor, comprovar posição, persistência e visualização reais.
4. **Entrega integrada:** repetir demonstração completa, fechar lacunas e atualizar relatório/estatística.

Controle e IA podem evoluir em frentes paralelas da equipe; integrar frequentemente evita descobrir conflitos de CPU, rede ou configuração no fim. Responsáveis e datas não foram atribuídos sem confirmação.

Autonomia para seguir rotas aparece como possibilidade futura porque o protocolo já existe. O usuário não a definiu como requisito obrigatório deste semestre; não foi incluída como condição para concluir a melhoria geral.

[[wiki/planejamento/backlog]] · [[wiki/planejamento/validacao]] · [[wiki/planejamento/equipe-e-entregas]].
''','planejamento',status='objetivos-confirmados-criterios-propostos',sources=['[[wiki/diario/2026-09-09|Instrução do usuário e registro da sessão]]','[[wiki/estado/onde-estamos]]'])

note('wiki/planejamento/backlog.md','Backlog — transformar melhoria geral em entregas','''
As frentes vêm do objetivo confirmado. Prioridades, sequência e critérios abaixo são propostas técnicas, sem responsáveis ou datas inventados. Nenhuma caixa está marcada como concluída por simples existência de código.

## P0 — consolidar a base física e o controle

- [ ] **AT-01 — Inventário e versões instaladas.** Fotografar hardware, identificar alimentação/GPS/áudio, registrar SHAs do Pi e host de nuvem. Conclui com ficha reproduzível e sem credenciais. Fonte: [[wiki/hardware/especificacoes]].
- [ ] **AT-02 — Um broker no Pi.** Escolher apt ou Docker, registrar configuração efetiva, provar que ponte e serviços usam o mesmo processo. Depende de AT-01. Conclui após reboot e recepção consistente dos comandos.
- [ ] **AT-03 — Operar sem ESP32.** Usar BLE NUS no Pi, retirar dependência operacional de serial_ingestor e atualizar instalação/diagrama. Depende de AT-02. Conclui com ensaio filmado sem ESP32.
- [ ] **AT-04 — Motores reais e parada.** Conferir backend, sentidos, rampa e comportamento ao perder controle. Depende de AT-01/02/03. Conclui com resultados do protocolo T-CONTROLE e limitações registradas.

## P1 — IA, GPS e informações

- [ ] **AT-05 — Medir e melhorar a IA.** Montar perguntas de referência sobre a SETREM, comparar respostas e tempos, testar modo offline e recuperação. Registrar modelos/voz/configuração. Conclui com comparação antes/depois e avaliação da equipe.
- [ ] **AT-06 — Áudio e escuta.** Validar Vosk, silêncio/fim de frase, chamadas e sinais, ruído ambiente e reconexão USB. Pode avançar com AT-05. Conclui com amostras e ocorrências documentadas.
- [ ] **AT-07 — Instalar e validar GPS.** Identificar módulo e porta, obter fix real, conferir MQTT/banco/mapa e perda de sinal. Depende de AT-01/02. Conclui com registros reais correlacionados de ponta a ponta.
- [ ] **AT-08 — Confiabilidade da telemetria.** Ensaiar queda de rede e banco; quantificar atraso, duplicatas e perdas. Definir tratamento para eventos sem timestamp e distinguir origem real/simulada. Depende de AT-02 e coleta identificada.
- [ ] **AT-09 — Informações claras no controle.** Distinguir enviado, recebido, estado comandado e medido; indicar dado antigo e desconexão; testar telas em Android/iOS disponíveis. Depende dos contratos e de AT-04/07/08 para dados reais.
- [ ] **AT-10 — Implantação e continuidade do banco.** Confirmar PC/VM atual, responsável, backup/restauração, retenção e acesso. Decidir migração LARCC. Conclui com recuperação documentada e host identificado.

## P2 — integração e consolidação acadêmica

- [ ] **AT-11 — Conectar IA e corpo.** Definir se a conversa apenas consulta estado ou também atende `robo/voz/falar`; implementar contratos e testar indisponibilidade. Proposta que detalha “IA melhor”, ainda a validar como prioridade.
- [ ] **AT-12 — Dados para estatística.** Selecionar período real, variáveis e qualidade da amostra; produzir análise verificável sem misturar simulação. Entrega prevista no [[wiki/historico/relatorio-atual|LaTeX]], a confirmar com a equipe.
- [ ] **AT-13 — Atualizar relatórios e evidências.** Registrar arquitetura sem ESP32, classes, banco, resultados, limitações e extensão. Depende das entregas técnicas efetivamente concluídas.
- [ ] **AT-14 — Reconciliar documentação dos repos.** Corrigir ESP32 obrigatório, localização de implantação, afirmações de GPS e observabilidade MQTT. Base: [[wiki/estado/divergencias]].

## Estacionamento — não obrigatório no objetivo confirmado

- Serviço que execute automaticamente a rota planejada.
- Sensor de bateria: avaliar necessidade para informação/estatística de energia; produtor ainda inexistente.
- Rodas/amortecimento para piso de tijolos, após avaliação mecânica.
- Refatorações gerais que não impedem integração, como encerramento repetido dos serviços.

## Regra de conclusão

Para marcar uma tarefa: link de commit/PR quando houver código, SHA instalado quando aplicável, experimento com resultado, data, responsável e notas afetadas atualizadas. “Código escrito” não equivale a “implantado e validado”. Use [[modelos/Melhoria]] e [[modelos/Experimento]].
''','planejamento',status='proposto',sources=['[[wiki/planejamento/onde-queremos-ir]]','[[wiki/estado/divergencias]]','[[wiki/historico/relatorio-atual]]'])

note('wiki/planejamento/validacao.md','Validação — como demonstrar o avanço','''
Estes são protocolos propostos, não resultados de testes realizados. A equipe deve definir limites de aceitação antes da comparação final. Não foram inventados ganhos percentuais, tolerâncias de GPS ou tempos já medidos.

## Registro comum a todo ensaio

Data, executor, ambiente, hardware, SHAs dos repositórios, versão do app, configuração relevante sem segredos, origem dos dados, procedimento, esperado, observado, logs/amostras e limitações. Use [[modelos/Experimento]].

## T-CONTROLE — operação sem ESP32

1. Confirmar montagem apropriada ao teste e meios de interromper o movimento; começar com rodas sem contato com o piso.
2. Inicializar com o ESP32 ausente; registrar único broker e serviço BLE do Pi.
3. Pressionar/soltar cada direção, cancelar o toque, mudar tela e desconectar.
4. Observar entrada MQTT, status de motores e resposta física separadamente.
5. Interromper envio enquanto houver comando de movimento e conferir o vigia.
6. Repetir após reinício, anotando sentido e tempo de parada observado.

Critério proposto: nenhuma perda de controle mantém movimento contínuo; versões e comportamento são reproduzíveis. O timeout configurado de 1 s não é prova de parada física em exatamente 1 s.

## T-IA — antes e depois da melhoria

Criar um conjunto fixo de perguntas institucionais, perguntas fora do conhecimento disponível, chamadas curtas e enunciados em ambiente com ruído. Usar as mesmas frases para comparar versões.

Registrar texto esperado/transcrito, resposta, correção factual, tempo até fim da transcrição e primeiro áudio, modo de rede/local, modelo, voz, CPU/RAM/temperatura e falhas. Proposta de rodada inicial: 20 enunciados, repetidos quando necessário, sem apresentar esse número como exigência do curso.

Testar perda/retorno de rede e de áudio USB. Critério proposto: respostas mais úteis no conjunto definido, menos falhas e tempos comparáveis sem travar face/controle. A equipe deve definir os limites desejados após medir a base.

## T-GPS — sensor até a tela

Identificar módulo e serial; salvar NMEA e eventos processados; obter fix; conferir coordenadas e timestamp em MQTT, banco, API e mapa. Testar perda de fix e retomada, observando se o sistema informa dado antigo. Registrar condições de ambiente e método usado para avaliar posição.

Critério proposto: os registros exibidos correspondem aos dados físicos e a perda de validade não é apresentada como leitura atual. Precisão aceitável deve ser definida conforme o uso, não presumida pelo número de casas decimais.

## T-DADOS — reconexão e qualidade

Gerar uma sequência conhecida em ambiente de teste, identificada como simulação; contar publicados/recebidos/persistidos; interromper rede e banco em situações separadas; restabelecer e comparar timestamps, duplicatas e perdas. Depois repetir o caminho normal com GPS real.

Critério proposto: perdas e duplicações são conhecidas e tratadas, origem e idade aparecem de forma coerente, backup restaura uma amostra verificável. Não declarar “zero perda” com base apenas na configuração da fila MQTT.

## T-ENTREGA — demonstração integrada

Reinício → conexão BLE no Pi → controle/parada → interação de voz → GPS válido → telemetria no banco → consulta nas telas → evidências no vault e relatório. Registrar falhas e limitações mesmo se a demonstração for parcial.

## Verificações já feitas na montagem do vault

Leitura documental, comparação Git remota/local, equivalência de árvores, cópias e hashes das fontes. A verificação de links/arquivos está em [[wiki/meta/verificacao]]. As suítes de software e os ensaios acima não foram executados nesta tarefa.
''','planejamento',status='proposto')

note('wiki/planejamento/equipe-e-entregas.md','Equipe e entregas acadêmicas','''
## Pessoas documentadas

O `main.tex` do relatório atual registra **Enzo Allebrand, Fernando Bastian, Kerlon Ribeiro e Victor Genz**. Essa é a autoria na fonte, sem confirmação dos papéis individuais nesta conversa.

| Frente | Responsável | Próxima definição |
|---|---|---|
| Integração no Pi, broker e controle | A definir pela equipe | AT-01 a AT-04 |
| IA, voz e escuta | A definir pela equipe | AT-05 e AT-06 |
| GPS, banco e informações | A definir pela equipe | AT-07 a AT-10 |
| Relatório, estatística e evidências | A definir pela equipe | AT-12 e AT-13 |

Não há prazo final confirmado pelo usuário. O LaTeX planeja setembro–dezembro de 2026 e apresentação em dezembro. Comentários internos citam datas acadêmicas, mas o calendário precisa ser confirmado antes de assumir compromissos.

## Entregas previstas no documento acadêmico

POO: organização em classes/padrões e diagrama; Banco de Dados: modelagem, esquema e consultas; Estatística: análise de dados reais; Gerenciamento de Projetos: escopo, cronograma, responsabilidades e entregas; Extensão: evidências de contato/divulgação previstas no roteiro citado.

O vault serve de base para reunir evidências. Fotos, formulários, posts ou resultados que ainda não existem não foram preenchidos artificialmente.

## Perguntas para a próxima reunião

- Quem assume cada frente e quem integra as entregas?
- Qual é a data oficial e quais marcos intermediários serão usados?
- Onde o robô e a nuvem estão instalados e quem pode acompanhar os testes?
- Qual é o módulo GPS disponível, a alimentação atual e o material CAD?
- A análise de bateria exige adicionar um sensor neste semestre?

Registrar respostas no [[wiki/diario/2026-09-09|diário]] ou em uma nova nota diária e atualizar o backlog.
''','planejamento',status='parcial',sources=['[[fontes/github/doc-interdisciplinar-4-semestre/main.tex]]','[[fontes/github/doc-interdisciplinar-4-semestre/tex/cap1.tex]]','[[fontes/github/doc-interdisciplinar-4-semestre/tex/cap3.tex]]'])

note('wiki/decisoes/registro.md','Decisões — por que o projeto é assim','''
| ID | Decisão | Estado | Motivo / consequência |
|---|---|---|---|
| DEC-01 | Raspberry Pi como único computador/controlador principal, retirando a ponte ESP32 | Direção confirmada pelo usuário; BLE já implementado | Menos uma placa e uma serial no caminho de comando |
| DEC-02 | Preservar NUS/JSON e tópico de entrada ao trocar transporte | Implementada no código | App e serviços mantêm contrato apesar de mudar a ponte |
| DEC-03 | Mensagens MQTT entre componentes | Implementada | Serviços separados por responsabilidade |
| DEC-04 | API de leitura separada da ingestão | Implementada | Aplicativo consulta dados sem acesso direto ao banco |
| DEC-05 | Movimento precisa ser renovado; silêncio dispara parada | Implementada, pendente de validação física atual | Tratar perda de comunicação sem depender do último `S` |
| DEC-06 | Cinemática separada do hardware, com simulação | Implementada | Permitir desenvolvimento e testes sem robô |
| DEC-07 | IA/voz de rede com alternativa local configurável | Código implementado e uso relatado | Continuar interagindo sem rede, com diferenças de qualidade |
| DEC-08 | Vosk como padrão de escuta | Publicada em 09/09 | Reconhecimento durante a fala e ajuste da primeira palavra |
| DEC-09 | Um único broker local | Necessidade documentada; configuração efetiva pendente | Evitar conflito apt/Docker na porta 1883 |
| DEC-10 | Rota planejada sem assumir navegação pronta | Estado atual documentado | Não confundir envio de pontos com execução autônoma |
| DEC-11 | Separar evidência histórica, código, implantação e proposta | Adotada neste vault | Manter narrativa verificável e atualizável |

O motivo de uma decisão implementada foi extraído das fontes quando descrito. Não foi atribuída autoria individual a decisões coletivas sem evidência. Para novas decisões, usar [[modelos/Decisao]] com alternativas, impactos, fonte e status.

DEC-01 não estabelece que o banco ou toda IA precisam rodar exclusivamente no Pi: o objetivo explicitado foi retirar o ESP32 da eletrônica embarcada. Ver [[wiki/planejamento/onde-queremos-ir]].
''','decisao',sources=[source('RobotEye','src/roboteye/ble/nus.py'),source('orquestrador','README.md'),source('orquestrador','pi/services/motores/src/motores/main.py'),'[[wiki/diario/2026-09-09]]'])

note('wiki/historico/linha-do-tempo.md','Linha do tempo — da herança ao retrato atual','''
As datas dos commits representam registros Git, não a data em que algo foi instalado no robô. A entrega anterior é identificada pelo usuário e pelos PDFs, sem converter a numeração PIE em sequência cronológica.

| Momento | Marco documentado | Evidência |
|---|---|---|
| Etapa anterior, documentos de 2026 com divergência de capa | Estrutura híbrida, interface local e conectividade ESP32/MQTT | [[wiki/historico/relatorios-semestre]] |
| 27/08/2026 | API de leitura, túnel, site e melhorias de motores/ambiente publicadas como conjunto | orquestrador `19815b8` |
| 27/08/2026 | Otimizações de reserva de RAM e rádio incorporadas | RobotEye `60abf91` |
| 30/08/2026 | App planeja e envia rota; orquestrador valida/republica | app `cf52b55`; orquestrador `367d9f4` |
| 02/09/2026 | Último push registrado do repositório acadêmico na consulta | [[fontes/auditoria/repositorios-github.json]] |
| 03/09/2026 | Correções de parada/tela, concorrência de motores e teto de tempo do banco | app `04b7ad2`; orquestrador `cdb5553` |
| 03/09/2026 | Recuperação de áudio USB, sinais de escuta e coordenação com inferência | RobotEye `dcbcdef`, `16acb2f`, `4d57814`, `5318bb0` |
| 04/09/2026 | Ajustes de prompt/contexto e `keep_alive` para Ollama | RobotEye `6503b67`, `9e468b8`, `61b00c9` |
| 09/09/2026 | Vosk padrão e silêncio inicial; integração em produção | RobotEye `a88c2dd`, `e1b26d7`, `43a6fe0` |
| 09/09/2026 | Objetivo de melhoria geral confirmado e vault revisado | [[wiki/diario/2026-09-09]] |

O histórico completo permite rastrear também as etapas anteriores a esses marcos. Ver [[wiki/meta/historicos-git]]. A existência de commits antigos não prova que pertencem ao semestre anterior ou que representam exatamente a versão dos PDFs.
''','historico',sources=['[[wiki/meta/historicos-git]]','[[fontes/auditoria/repositorios-github.json]]'])

note('wiki/meta/fontes.md','Fontes — origem, preservação e limites','''
## Fontes primárias desta organização

| Fonte | Como foi consultada | Preservação |
|---|---|---|
| Três relatórios em `D:\\SetremRobot\\Relatorios` | Extração textual com páginas; leitura de conteúdo relevante | PDFs copiados, texto pesquisável e SHA-256 |
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
''','meta')

note('wiki/meta/como-usar.md','Como usar e manter o cérebro do projeto','''
## Abrir no Obsidian

Escolha **Abrir pasta como vault** e selecione `D:\\SetremRobot\\AtlasVault`. Abra [[INICIO]]. A estrutura usa recursos nativos: links, propriedades, backlinks, busca, marcadores, diário, templates, Mermaid e Canvas. Não depende de plugin comunitário.

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
python D:\\SetremRobot\\AtlasVault\\ferramentas\\verificar_vault.py
```

O verificador confere links internos, arquivos referenciados pelo Canvas, JSON de configuração, cópias de PDFs e hashes dos snapshots de código. Ele não executa o robô nem resolve links externos pela internet.

## Preservação e versionamento

O vault já possuía `.git`, mas não tinha commits. Esta tarefa mantém as alterações para revisão local e não cria push/commit automaticamente. Não apagar o backup anterior. Os scripts `montar_vault.py`, `complementar_vault.py` e `coletar_fontes.py` registram a construção inicial: **não reexecutá-los depois de editar as notas**, pois podem sobrescrever a documentação e os snapshots de 09/09. Para o uso rotineiro, executar apenas `atualizar_git.py` e `verificar_vault.py`.

Antes de versionar ou compartilhar, revisar material privado e os registros adicionados pela equipe. Preferências de tela/workspace são locais e ficam ignoradas pelo Git.
''','meta')

note('wiki/diario/2026-09-09.md','09/09/2026 — organização do conhecimento','''
## Pedido e objetivo confirmado

Organizar o AtlasVault na pasta `D:\\SetremRobot`, tornando explícitos o ponto de partida dos relatórios, o estado atual local/GitHub e a direção do projeto.

O usuário confirmou a intenção de melhoria geral: retirar ESP32, manter Raspberry Pi como base embarcada, melhorar IA e controle, implementar GPS e melhorar comunicação com banco e informações. O prazo e as responsabilidades individuais não foram confirmados.

## Trabalho realizado

Preservação do vault anterior; cópia e extração dos três relatórios; inventário de arquivos; consulta a quatro repositórios públicos e um privado acessível; leitura das fontes principais do relatório LaTeX; atualização de refs Git; comparação de branches, árvores e alterações; revisão dos contratos e estado; criação de notas, plano, modelos e navegação.

## Descobertas relevantes

- BLE no Pi já existe, com legado ESP32 ainda no repositório.
- As branches ativas estão sincronizadas e limpas, mas há histórico em branches locais antigas; vários conjuntos coincidem com squashes publicados.
- GPS, motores e implantação na VM têm diferenças entre narrativas históricas e docs atuais.
- O status dos motores é comandado, não medido; rota enviada não é navegação autônoma.
- O relatório acadêmico atual já identifica autores e proposta de estatística, mas contém resultados a desenvolver.

## Próximos passos da equipe

Confirmar responsáveis/prazo; inventariar o robô e registrar SHAs instalados; escolher broker único; testar controle sem ESP32; medir IA; instalar GPS e validar dados reais. A sequência detalhada está no [[wiki/planejamento/backlog]].

## Limite desta sessão

Nenhum código dos três repositórios de software foi alterado. Não houve deploy, publicação no GitHub, acesso ao banco operacional nem testes físicos. A validação do acervo e navegação fica em [[wiki/meta/verificacao]].
''','diario')

for name, title, body in [
('Diario','Registro diário','''Data: {{date}} · Participantes: a preencher

## Objetivo do dia

A preencher. Relacionar tarefa do [[wiki/planejamento/backlog]].

## O que aconteceu

Descrever ação, descoberta ou decisão; separar observação de hipótese.

## Evidência

Fonte/arquivo, SHA local, SHA publicado, versão instalada quando aplicável; resultado observado.

## Próximo passo

Responsável, prazo combinado e notas que precisam mudar.
'''),
('Melhoria','Ficha de melhoria','''ID: AT-XX · Frente: a preencher · Responsável: a definir · Prazo: a definir

## Problema e origem

Qual comportamento precisa melhorar? Qual relato, incidente ou teste demonstra isso?

## Resultado esperado

Comportamento concreto, limites e critério de conclusão.

## Dependências e implementação

Repositório, branch, arquivos, dependências, commit/PR.

## Estado de entrega

- [ ] Implementado localmente
- [ ] Testado no ambiente indicado
- [ ] Publicado no repositório
- [ ] Instalado no ambiente alvo, se aplicável
- [ ] Resultado validado e documentação atualizada

## Evidências

Link do experimento e comparação antes/depois. Não marcar por suposição.
'''),
('Experimento','Registro de experimento','''Data: {{date}} · Executor: a preencher · Protocolo: a preencher

## Ambiente e versão

Hardware, SO, versão do app, SHAs dos repos e backend/modelo. Sem credenciais.

## Hipótese e critério de aceitação

Definir antes do ensaio. Origem dos dados: real ou simulada.

## Procedimento

Passos reproduzíveis e meios de interromper o ensaio quando aplicável.

## Resultado observado

Passou / falhou / inconclusivo. Medidas, logs e anexos reais.

## Limites e conclusão

O que o teste prova, o que não prova, ação seguinte e notas a atualizar.
'''),
('Decisao','Registro de decisão','''ID: DEC-XX · Data: {{date}} · Estado: proposta / aceita / substituída

## Contexto

Problema, restrições e fontes.

## Alternativas

Opções consideradas e consequências.

## Decisão e autoria

Escolha, justificativa e quem a confirmou.

## Consequências e verificação

Impactos nos repositórios/hardware, dependências, teste e relação com decisão anterior.
'''),
('Fonte','Ficha de fonte','''Recebida em: {{date}} · Tipo: PDF / código / medição / reunião / outro

## Origem

Autor, data, caminho/URL, versão/SHA e acesso público/privado.

## O que afirma

Resumo com página ou trecho localizável.

## O que foi conferido

Relato histórico, implementação ou ensaio? Há conflitos com outras fontes?

## Destino no vault

Notas atualizadas e pendências; preservar o original.
''')]:
    note('modelos/'+name+'.md',title,body,'modelo',status='modelo')

note('inbox/LEIA-ME.md','Entrada de informações novas','''
Coloque aqui documentos, atas e anotações que ainda precisam de conferência. Dê nome com data e assunto. Use [[modelos/Fonte]] para registrar origem e versão.

Depois de conferir, preserve o original em `fontes`, incorpore o conhecimento à nota do assunto e ligue a evidência. Não transformar qualquer arquivo novo automaticamente em estado atual do projeto.

Pendências de acervo: CAD/STL, fotos atuais, esquema elétrico, inventário do GPS/alimentação, SHAs instalados, calendário confirmado e resultados de campo.
''','meta')

# Inventário completo de arquivos rastreados, com navegação por categoria.
inventory_links=[]
history_links=[]
for result in audit['repositorios']:
    repo=result['pasta']
    files=subprocess.check_output(['git','-C',str(R/repo),'ls-files','-z'],encoding='utf-8').split('\0')
    files=[f for f in files if f]
    groups={}
    for f in files:
        head=f.split('/')[0] if '/' in f else 'Raiz'
        groups.setdefault(head,[]).append(f)
    body=[f"**{len(files)} arquivos rastreados** no checkout `{SHA[repo][:7]}`. Lista obtida por Git, sem arquivos ignorados/ambientes de build. Os links de código estão fixados nessa versão.",f"\nSnapshot offline: [[fontes/codigo-{repo}-2026-09-09.zip]]. O ZIP preserva a árvore de arquivos; extrair para consulta fora das pastas de software existentes."]
    for group,paths in sorted(groups.items()):
        body += [f'\n## {group}\n', '| Arquivo | Tamanho em bytes |','|---|---|']
        for f in paths:
            size=(R/repo/f).stat().st_size if (R/repo/f).exists() else 'ausente'
            body.append(f'| {source(repo,f,f)} | {size} |')
    note(f'wiki/meta/inventario-{repo}.md',f'Inventário de arquivos — {repo}','\n'.join(body),'inventario')
    inventory_links.append(f'- [[wiki/meta/inventario-{repo}|{repo}: {len(files)} arquivos]]')
    body=['Histórico coletado com `git log --all`. Inclui branches remotas e locais; presença nesta lista não significa commit implantado nem publicado. Para classificar diferenças, ver [[wiki/estado/git-local-e-remoto]].','\n| SHA | Data de commit | Assunto |','|---|---|---|']
    local={c['sha'] for c in result['commits_locais_nao_alcancaveis_por_remotos']}
    for c in result['historico_todas_branches']:
        label=f"`{c['sha'][:7]}` (grafo local)" if c['sha'] in local else f"[{c['sha'][:7]}]({result['github']}/commit/{c['sha']})"
        subject=c['assunto'].replace('|','\\|').replace('\n',' ')
        body.append(f"| {label} | {c['data_commit']} | {subject} |")
    note(f'wiki/meta/historico-{repo}.md',f'Histórico Git coletado — {repo}','\n'.join(body),'inventario')
    history_links.append(f'- [[wiki/meta/historico-{repo}|{repo}: {len(result["historico_todas_branches"])} commits coletados]]')

note('wiki/meta/inventario.md','Inventário — tudo que foi encontrado','''
## Pastas da área de trabalho

`app`, `orquestrador` e `RobotEye` contêm os três checkouts de software. `Relatorios` contém os três PDFs históricos. `AtlasVault` contém o conhecimento organizado. Há ainda `MAPA-COMUNICACAO.md`, dois PNGs da marca e configurações auxiliares `.claude`, que não são componentes de execução do robô.

## Código e arquivos por repositório

'''+ '\n'.join(inventory_links)+'''

Os inventários incluem código, testes, scripts, documentação, assets e arquivos de plataforma. Eles não listam dependências baixadas, `.git` interno, caches, build ou arquivos ignorados. Isso mantém a lista focada no projeto versionado.

## Acervo além dos checkouts

- [[wiki/historico/relatorios-semestre|Três PDFs históricos: 34 + 34 + 41 páginas]]
- [[wiki/historico/relatorio-atual|Repositório acadêmico LaTeX, privado e sem checkout original local]]
- [[fontes/github/.github/profile/README.md|Perfil da organização]]
- [[fontes/imagens/atlas-icone-1024.png|Ícone da Atlas]] · [[fontes/imagens/atlas-olhos-1024.png|Olhos da Atlas]]
- [[wiki/meta/historicos-git|Histórico Git]] · [[wiki/estado/git-local-e-remoto|Diferenças locais/remotas]]

Para compreender responsabilidades, usar [[wiki/modulos/index]]; para consultar os originais, [[wiki/meta/fontes]].
''','inventario')
note('wiki/meta/historicos-git.md','Históricos completos dos repositórios','\n'.join(history_links)+f'\n\nA coleta completa em JSON está em [[{audits[-1].relative_to(V).as_posix()}]]. Datas de autoria e commit são preservadas no JSON; as tabelas exibem a data do commit. A interpretação de squash, branch antiga e produção fica em [[wiki/estado/git-local-e-remoto]].','inventario')

# Arquivos locais auxiliares preservados e imagens originais.
(V/'fontes/imagens').mkdir(parents=True,exist_ok=True)
for name in ['atlas-olhos-1024.png','atlas-icone-1024.png']:
    shutil.copy2(R/name,V/'fontes/imagens'/name)
(V/'fontes/documentos-locais').mkdir(parents=True,exist_ok=True)
shutil.copy2(R/'MAPA-COMUNICACAO.md',V/'fontes/documentos-locais/MAPA-COMUNICACAO.md')

# Canvas nativo com três eixos e notas reais.
nodes=[];edges=[]
columns=[('origem','De onde viemos','1',0,[('Relatórios e herança','wiki/historico/relatorios-semestre.md'),('Evolução','wiki/historico/evolucao.md')]),('presente','Onde estamos','4',510,[('Estado atual','wiki/estado/onde-estamos.md'),('Arquitetura','wiki/arquitetura/visao-geral.md'),('Local e GitHub','wiki/estado/git-local-e-remoto.md')]),('futuro','Onde queremos ir','5',1020,[('Objetivos confirmados','wiki/planejamento/onde-queremos-ir.md'),('Backlog','wiki/planejamento/backlog.md'),('Validação','wiki/planejamento/validacao.md')])]
for key,title,color,x,items in columns:
    nodes.append({'id':key,'type':'group','x':x,'y':0,'width':470,'height':850,'label':title,'color':color})
    for i,(label,path) in enumerate(items):
        nodes.append({'id':key+str(i),'type':'file','file':path,'x':x+25,'y':55+i*260,'width':420,'height':235,'color':color})
edges=[{'id':'historia-hoje','fromNode':'origem1','fromSide':'right','toNode':'presente0','toSide':'left','label':'evoluiu para'}, {'id':'hoje-futuro','fromNode':'presente0','fromSide':'right','toNode':'futuro0','toSide':'left','label':'melhorar e validar'}]
(V/'Mapa do projeto.canvas').write_text(json.dumps({'nodes':nodes,'edges':edges},ensure_ascii=False,indent=2),encoding='utf-8')

obs=V/'.obsidian'
def config(name,changes):
    p=obs/name
    old=json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else {}
    old.update(changes)
    p.write_text(json.dumps(old,ensure_ascii=False,indent=2),encoding='utf-8')
config('app.json',{'alwaysUpdateLinks':True,'newLinkFormat':'absolute','useMarkdownLinks':False,'attachmentFolderPath':'fontes/anexos','newFileLocation':'folder','newFileFolderPath':'inbox','showUnsupportedFiles':True})
config('templates.json',{'folder':'modelos','dateFormat':'YYYY-MM-DD','timeFormat':'HH:mm'})
config('daily-notes.json',{'folder':'wiki/diario','format':'YYYY-MM-DD','template':'modelos/Diario'})
config('appearance.json',{'accentColor':'#09d085','enabledCssSnippets':['atlas']})
(obs/'snippets').mkdir(exist_ok=True)
(obs/'snippets/atlas.css').write_text('''/* Atlas: tipografia simples, tabelas legíveis e marca discreta. */
body { --file-line-width: 1000px; --table-header-background: var(--background-secondary); }
.markdown-preview-view h1 { border-bottom: 2px solid var(--interactive-accent); padding-bottom: .4em; }
.markdown-preview-view h2 { margin-top: 1.8em; }
.markdown-preview-view table { font-size: .94em; }
.markdown-preview-view th { white-space: normal; }
.markdown-preview-view .internal-link { text-decoration-thickness: 1px; }
''',encoding='utf-8')
bookmarks=[{'type':'file','ctime':1788969600000,'path':p,'title':t} for t,p in [('Início','INICIO.md'),('Mapa visual','Mapa do projeto.canvas'),('Onde estamos','wiki/estado/onde-estamos.md'),('Backlog','wiki/planejamento/backlog.md'),('Git local e remoto','wiki/estado/git-local-e-remoto.md')]]
config('bookmarks.json',{'items':bookmarks})
# Preserva estrutura de painéis e substitui apenas a nota aberta inicial.
workspace=json.loads((obs/'workspace.json').read_text(encoding='utf-8'))
def walk(obj):
    if isinstance(obj,dict):
        if obj.get('file')=='wiki/arquitetura/como-funciona.md': obj['file']='INICIO.md'
        if obj.get('title')=='como-funciona': obj['title']='Atlas — cérebro do projeto'
        for value in obj.values(): walk(value)
    elif isinstance(obj,list):
        for value in obj: walk(value)
walk(workspace)
workspace['lastOpenFiles']=['INICIO.md','Mapa do projeto.canvas','wiki/estado/onde-estamos.md','wiki/planejamento/backlog.md']
(obs/'workspace.json').write_text(json.dumps(workspace,ensure_ascii=False,indent=2),encoding='utf-8')
(V/'.gitignore').write_text('''# Preferências por máquina, caches e segredos não pertencem ao acervo versionado.
.obsidian/workspace*.json
.obsidian/cache/
.trash/
__pycache__/
*.pyc
.env
.env.*
!.env.example
*.jks
*.pem
*.key
''',encoding='utf-8')
print('Planejamento, Git, inventários, modelos e configuração gravados.')

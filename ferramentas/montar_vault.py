"""Construção inicial das notas em 09/09/2026. Não executar após editar o vault:
este arquivo registra a elaboração inicial e sobrescreve as notas que criou.
Para manutenção diária use atualizar_git.py e edite as notas no Obsidian.
"""
from pathlib import Path
import json
import re
import shutil
import subprocess
import textwrap
from urllib.parse import quote

V = Path(__file__).resolve().parents[1]
R = V.parent
DATE = "2026-09-09"
SHA = {r: subprocess.check_output(["git", "-C", str(R/r), "rev-parse", "HEAD"], encoding="utf-8").strip() for r in ["app", "orquestrador", "RobotEye"]}
REMOTE = {"app": "aplicativo", "orquestrador": "orquestrador", "RobotEye": "atlas_ai_v2"}

def source(repo, path, label=None):
    return f"[{label or repo+'/'+path}](https://github.com/setrem-robot/{REMOTE[repo]}/blob/{SHA[repo]}/{quote(path)})"

def note(path, title, body, kind="referencia", status="revisado", sources=()):
    p = V / path
    p.parent.mkdir(parents=True, exist_ok=True)
    meta = f'---\ntitle: {json.dumps(title, ensure_ascii=False)}\ntipo: {kind}\nestado_documental: {status}\natualizado: {DATE}\ntags:\n  - atlas\n  - {kind}\n---\n\n'
    content = meta + '# ' + title + '\n\n' + textwrap.dedent(body).strip() + '\n'
    if sources:
        content += '\n## Fontes e conferência\n\n' + '\n'.join('- '+s for s in sources) + '\n'
    if path != "INICIO.md":
        content += '\n---\n[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]\n'
    p.write_text(content, encoding='utf-8')

note('INICIO.md', 'Atlas — cérebro do projeto', '''
![[fontes/imagens/atlas-olhos-1024.png|160]]

Este é o ponto de entrada do projeto Atlas, da Engenharia de Computação da SETREM. Aqui estão a herança recebida, o software encontrado em `D:\\SetremRobot`, a comparação com o GitHub e a direção de melhoria definida para este semestre.

> [!info] Retrato de 9 de setembro de 2026
> Código conferido e referências remotas atualizadas. A inspeção foi documental: não houve conexão ao robô nem ensaio físico. “Existe no código”, “relatado como testado” e “validado agora” são estados diferentes.

## As três perguntas centrais

| De onde viemos | Onde estamos | Onde queremos ir |
|---|---|---|
| [[wiki/historico/relatorios-semestre|Herança dos três relatórios]] | [[wiki/estado/onde-estamos|Estado atual por subsistema]] | [[wiki/planejamento/onde-queremos-ir|Objetivos confirmados e entregas]] |
| [[wiki/historico/linha-do-tempo|Linha do tempo]] | [[wiki/estado/git-local-e-remoto|Local × GitHub × produção]] | [[wiki/planejamento/backlog|Backlog priorizado]] |
| [[wiki/historico/evolucao|O que mudou desde a entrega anterior]] | [[wiki/estado/divergencias|Divergências e perguntas abertas]] | [[wiki/planejamento/validacao|Como comprovar as melhorias]] |

## Entender o projeto

- [[wiki/arquitetura/visao-geral|Arquitetura e fronteiras entre repositórios]]
- [[wiki/arquitetura/mapa-comunicacao|Diagramas de comunicação]] · [[Mapa do projeto.canvas|Mapa visual navegável]]
- [[wiki/modulos/index|Catálogo de componentes]] · [[wiki/hardware/especificacoes|Estrutura e hardware]]
- [[wiki/api/contrato-mqtt|Contrato MQTT e BLE]] · [[wiki/api/contratos|API e banco de dados]]
- [[wiki/configuracao/setup-completo|Instalação e operação]] · [[wiki/configuracao/diagnostico|Diagnóstico por sintoma]]
- [[wiki/seguranca/index|Proteções implementadas e seus limites]]

## Trabalhar e registrar

- [[wiki/planejamento/equipe-e-entregas|Equipe, responsabilidades e entregas acadêmicas]]
- [[wiki/decisoes/registro|Decisões e critérios]]
- [[wiki/diario/2026-09-09|Registro desta organização]]
- [[wiki/meta/como-usar|Como usar e manter este vault]] · [[wiki/meta/inventario|Inventário dos arquivos]]
- [[wiki/meta/fontes|Fontes, PDFs originais e snapshots]] · [[inbox/LEIA-ME|Entrada de novas informações]]

## Leitura em 15 minutos

1. Leia a [[wiki/historico/evolucao|comparação entre antes e agora]].
2. Veja o [[wiki/estado/onde-estamos|estado atual]] e as limitações físicas.
3. Siga o [[wiki/arquitetura/como-funciona|caminho de um comando e de uma leitura]].
4. Escolha uma entrega no [[wiki/planejamento/backlog|backlog]] e registre o resultado no diário.

O objetivo é uma melhoria geral: um único Raspberry Pi no robô, IA e controle melhores, GPS real e informações confiáveis do robô até o banco e as telas. Os critérios propostos estão explicitados para que a equipe possa transformar essa direção em entregas verificáveis.
''', 'mapa')

note('wiki/index.md','Índice do AtlasVault','''
O painel principal é [[INICIO]]. Esta página mantém o endereço do índice anterior.

[[wiki/historico/relatorios-semestre|História]] · [[wiki/estado/onde-estamos|Presente]] · [[wiki/planejamento/onde-queremos-ir|Futuro]]

[[wiki/modulos/index|Módulos]] · [[wiki/meta/inventario|Arquivos]] · [[wiki/meta/fontes|Fontes]] · [[wiki/meta/como-usar|Como manter]]
''','mapa')

note('wiki/historico/relatorios-semestre.md','De onde viemos — a entrega anterior','''
O usuário identificou os três PDFs da pasta `Relatorios` como a entrega do semestre anterior. Eles são a base histórica desta documentação. Os textos descrevem frentes diferentes do mesmo robô e não comprovam, isoladamente, o funcionamento integrado de todas elas.

| Frente | Autores no PDF | O que foi relatado | O que ficou aberto |
|---|---|---|---|
| [[wiki/historico/estrutura-anterior|Estrutura mecânica]] | Andriel Felipe Schultz; Crístofer Mateus Rutzen; Gabriel Kaspary | CAD, chassi tubular de aço, carenagem modular em PLA e ensaios manuais | Acionamento motorizado, rampas e validação dinâmica |
| [[wiki/historico/interface-anterior|Interface humano-robô]] | Bernardo Baú; Guilherme Machry da Silva; Rychard Daniel dos Santos | Conversa local, Vosk, Ollama, voz e animações no Pi 5 | Usabilidade ampliada, áudio e base institucional |
| [[wiki/historico/orquestracao-anterior|Conectividade e orquestração]] | Kauã Rambo; Eduardo Augusto Goetz; Thales Gabriel Fernandes Diniz Martins | App Flutter, SPP/ESP32/serial, MQTT, GPS descrito e TimescaleDB; painel Quarkus | Retorno ao app, integração da IA, motores e energia |

## A herança principal

Recebemos uma plataforma física e diferentes implementações de software. A estrutura separa a responsabilidade mecânica; a interface demonstra o ciclo ouvir–pensar–falar; a orquestração organiza comandos e telemetria. A evolução atual concentra-se em integrar, tornar observável e melhorar esse conjunto.

Não se deve converter “objetivo alcançado” em um PDF em uma afirmação de que o robô atual está montado e testado da mesma forma. Exemplo concreto: o relatório de orquestração declara o GPS integrado, enquanto os READMEs atuais dizem que o módulo não está montado. Ver [[wiki/estado/divergencias]].

## Datas e nomes acadêmicos

Os documentos referem-se a 2026, mas a capa de Estrutura traz 2025 e a folha seguinte traz 2026. O texto de Estrutura cita PIE V; o repositório acadêmico atual se chama `doc-interdisciplinar-4-semestre` e identifica PIE IV. Preservei essas diferenças. A sequência “entrega anterior → trabalho atual” vem do usuário; a numeração não foi usada para deduzir a cronologia.

As referências de página neste vault usam a **página física do PDF, contando a capa como 1**. A numeração impressa pode ser diferente.

Continue em [[wiki/historico/evolucao]] e [[wiki/historico/relatorio-atual]].
''','historico',sources=['[[fontes/relatorios/EstruturaPDF.pdf]]','[[fontes/relatorios/InterfacePDF.pdf]]','[[fontes/relatorios/OrquestradorPDF.pdf]]'])

note('wiki/historico/estrutura-anterior.md','Estrutura — o que a equipe anterior entregou','''
## Problema e solução

Construir uma plataforma móvel para interação no ambiente acadêmico da SETREM. O relatório apresenta modelagem em SolidWorks, chassi de aço e carenagem modular impressa em PLA, com acesso para manutenção e componentes pesados concentrados na base.

## Dimensões e materiais documentados

| Item | Registro histórico | Local no PDF |
|---|---|---|
| Altura | 875 mm | p. 22 |
| Base | 420 × 480 mm; carenagem inferior de 180 mm | p. 22 |
| Cintura/pescoço | 220 mm | p. 22 |
| Massa | Cerca de 15 kg, **estimada** | p. 20 e 22 |
| Chassi | Tubos de aço 25 × 25 × 1,5 mm | p. 14 e 29 |
| Tração prevista | 2 motores Nema 23, torque citado de 30 kgf.cm | p. 14 e 18 |
| Rodas orçadas | 4 rodas de borracha de 100 mm | p. 14 |
| Fixações | Insertos M3 e parafusos | p. 20 |
| Orçamento histórico | R$ 1.218,00, estimativa com cotações de maio de 2026 | p. 13–14 |

O orçamento é da frente mecânica, não o custo total atual do robô. Os valores não são cotações atuais nem comprovantes de aquisição.

## Ensaios efetivamente relatados

| Ensaio | Procedimento descrito | Resultado dos autores |
|---|---|---|
| TP1 | Deslocamento manual de 3 m em piso liso | Sem trepidação perceptível |
| TP2 | Deslocamento manual de 3 m em tijolos | Trepidação; sem folgas detectadas |
| TP3 | Avaliação auditiva em piso liso | Ruído moderado |
| TP4 | Avaliação auditiva em tijolos | Ruído elevado; reprovado no critério adotado |
| TP5 | Carga de 20 kg sobre a carenagem por 10 minutos | Sem deformação permanente relatada |
| TP6 | Carga de 30 kg no chassi por 10 minutos | Sem deformação permanente relatada |

Fonte: p. 26–29. Os testes de movimento foram manuais. Não equivalem a ensaios com motores acionados nem a uma certificação de carga de operação.

## Limitações herdadas

A seção 3.3 informa que problemas no acionamento Nema 23 impediram os testes motorizados T2 a T6. Há uma divergência entre rampa de 20° no quadro da p. 20 e 5–7° na seção 3.1.3 da p. 22. Nenhuma das inclinações deve ser tratada como capacidade comprovada.

A melhoria sugerida pelos autores envolve rodas/amortecimento para reduzir ruído e vibração. Antes de repetir ensaios, confirmar montagem, distribuição de massa, alimentação e critério de inclinação com a equipe. Ver [[wiki/hardware/especificacoes]] e [[wiki/planejamento/validacao]].
''','historico',sources=['[[fontes/relatorios/EstruturaPDF.pdf#page=22|Dimensões — p. 22]]','[[fontes/relatorios/EstruturaPDF.pdf#page=26|Limitações e ensaios — p. 26 em diante]]'])

note('wiki/historico/interface-anterior.md','Interface — da bancada à conversa local','''
## Ponto de partida

A equipe buscou uma interface que entendesse perguntas e respondesse em português sem depender de internet. O relatório descreve três etapas: percepção, cognição e expressão.

1. **Bancada no Pi 4 de 8 GB:** TinyLlama e Qwen2-0.5B via Ollama, entrada inicialmente por terminal, eSpeak-ng/MBROLA para a fala (p. 19–22).
2. **Migração para o Pi 5:** microfone USB, Vosk para reconhecimento e um modelo chamado “Gemma 3B” no documento (p. 22–24).
3. **Integração física:** display, caixas de som, organização dos cabos e início automático via systemd (p. 25).

## Ciclo documentado

```mermaid
flowchart LR
  M[Microfone USB] --> V[Vosk]
  V --> O[Ollama e modelo local]
  O --> T[eSpeak-ng e MBROLA]
  T --> A[Áudio]
  O --> D[Animações no display]
```

Os autores relatam o ciclo completo funcionando na SETREM e uma avaliação informal positiva das expressões (p. 28). Não há amostra ou métricas suficientes nessa seção para quantificar taxa de acerto ou satisfação.

## Problemas e aprendizado

- Concorrência entre IA e áudio provocava travamentos; foram aplicados limites de resposta e ajustes de prioridade.
- Volume baixo apareceu na banca e motivou ajuste no mixer ALSA.
- A escolha de microfone USB veio da necessidade de uma entrada de áudio adequada.
- A base institucional era contextualizada no Modelfile.

Preservamos “Gemma 3B” como **nome usado pelo relatório**, não como identificação verificada de um artefato do Ollama. As referências a jack P2 e aos sistemas Bookworm/Trixie também pertencem ao relato histórico; o inventário de áudio e SO do robô atual precisa ser conferido fisicamente.

## Continuidade

Os trabalhos futuros das p. 30–31 são ampliar conhecimento da SETREM, testar com mais usuários, consolidar o áudio e evoluir as expressões. Hoje o código oferece motores de IA/voz intercambiáveis, reserva local, face por eventos, painel web e recuperação de áudio USB. Ver [[wiki/modulos/roboteye]] e [[wiki/planejamento/onde-queremos-ir]].
''','historico',sources=['[[fontes/relatorios/InterfacePDF.pdf#page=19|Desenvolvimento — p. 19]]','[[fontes/relatorios/InterfacePDF.pdf#page=28|Resultados — p. 28]]','[[fontes/relatorios/InterfacePDF.pdf#page=30|Conclusão e continuidade — p. 30]]'])

note('wiki/historico/orquestracao-anterior.md','Orquestração — conectividade herdada','''
## Arquitetura relatada

O app Flutter enviava JSON em uma linha via Bluetooth Classic/SPP. Um ESP32-WROOM-DA validava e encaminhava o conteúdo pela serial. O Raspberry Pi distribuía as mensagens em MQTT, os serviços produziam estado e uma bridge encaminhava telemetria para o TimescaleDB.

```mermaid
flowchart LR
  A[App Android] -->|SPP| E[ESP32]
  E -->|Serial| S[serial_ingestor no Pi]
  S --> B[MQTT local]
  B --> O[Orquestrador e serviços]
  O --> T[Telemetria]
  T --> C[Broker remoto e ingestor]
  C --> D[TimescaleDB]
  D --> Q[Painel Quarkus e Leaflet]
```

## O que o relatório descreve

- App testado em Motorola Moto G30 com Android 12; direções `F`, `B`, `L`, `R`, `S` e parada ao soltar o botão (p. 28–30).
- Ajustes nas permissões Android e problema de dependência corrigida apenas no cache local (p. 29–30).
- Entrada MQTT `robo/comando/entrada`, roteamento para motores/voz/Wi-Fi e espelhamento seletivo (p. 31–34).
- Wi-Fi aplicado via NetworkManager/`nmcli`; status sem retorno serial→Bluetooth (p. 33).
- Serviço GPS com NMEA, posição, fix, satélites e velocidade (p. 33–34).
- Banco com tabela única `telemetria(ts, tipo, topico, payload)` (p. 34–35).
- Painel histórico Quarkus com REST/SSE, Leaflet e OpenStreetMap (p. 35–37).

## Lacunas registradas

O estado mostrado pelo controle representava a intenção enviada, sem confirmação de execução. A reconexão exigia ação manual. O suporte a iOS exigiria abandonar SPP. A conclusão ainda aponta integração da IA, motores, testes em campo, autonomia energética e distância percorrida como continuidade (p. 39).

## Conflitos que não podem ser apagados

A p. 38 declara a integração GPS concluída. Os READMEs atuais dizem que o módulo não está instalado. O relatório também usa descrições diferentes para o pareamento no Pi/ESP32. Essas afirmações ficam como evidência histórica, com validação atual pendente.

O backend encontrado hoje é FastAPI; o painel Quarkus é histórico e seu código não foi encontrado nos repositórios inventariados. Não foi presumida uma migração formal com data ou equivalência integral entre os dois.

Veja [[wiki/historico/evolucao]], [[wiki/estado/divergencias]] e [[wiki/modulos/nuvem]].
''','historico',sources=['[[fontes/relatorios/OrquestradorPDF.pdf#page=31|Arquitetura — p. 31]]','[[fontes/relatorios/OrquestradorPDF.pdf#page=38|Conclusão — p. 38]]'])

note('wiki/historico/relatorio-atual.md','Relatório acadêmico atual — PIE IV','''
Foi encontrado um quinto repositório pela conta GitHub autenticada: [doc-interdisciplinar-4-semestre](https://github.com/setrem-robot/doc-interdisciplinar-4-semestre). É privado na coleta e não aparecia na listagem pública da organização. As cópias no vault mantêm essa informação local; nenhuma publicação foi feita.

**Título registrado:** Robô Atlas: plataforma robótica orientada a objetos para coleta e análise de dados de telemetria.

**Autores em `main.tex`:** Enzo Allebrand, Fernando Bastian, Kerlon Ribeiro e Victor Genz. Os papéis individuais não estão atribuídos neste vault; ver [[wiki/planejamento/equipe-e-entregas]].

## Organização e relação com o trabalho

| Arquivo | Conteúdo | Situação na fonte |
|---|---|---|
| `main.tex` | Capa, resumo, autores e inclusão dos capítulos | Documento em desenvolvimento |
| `tex/intro.tex` | Contexto, telemetria e proposta interdisciplinar | Texto narrativo |
| `tex/cap1.tex` | Tema, objetivos, metodologia, cronograma e orçamento | Orçamento ainda a confirmar |
| `tex/cap2.tex` | Fundamentação: POO, banco, estatística e arquitetura | Referência acadêmica |
| `tex/cap3.tex` | Hardware, classes, banco, coleta, estatística, integração e extensão | Seções com marcação explícita “em desenvolvimento” |
| `tex/conclusao.tex` | Síntese e trabalhos futuros | Trechos “a completar” |

A análise estatística é uma entrega prevista pelo texto, sem resultados apresentados. O cronograma indica atividades até dezembro de 2026; um comentário menciona o intervalo 15/08 a 19/12 e o início do capítulo 3 a partir de 24/10. Esses registros não substituem confirmação de prazo pela equipe/roteiro oficial.

## Revisões que as evidências pedem

- Atualizar a descrição do ESP32 para refletir a decisão atual de retirada.
- Sustentar com coleta real as afirmações de GPS, bateria, motores e banco em operação.
- Conferir a localização de implantação: o relatório cita LARCC, enquanto o README do orquestrador informa hospedagem provisória em um PC.
- Preencher resultados com método, versão, data, dados e limites; separar demonstração de coleta real.

O vault oferece a trilha de fontes e um [[wiki/planejamento/validacao|plano de validação]] para apoiar essa escrita. Não altera o relatório remoto automaticamente.
''','historico',sources=['[[fontes/github/doc-interdisciplinar-4-semestre/main.pdf|PDF acadêmico coletado]]','[[fontes/github/doc-interdisciplinar-4-semestre/main.tex]]','[[fontes/github/doc-interdisciplinar-4-semestre/tex/cap3.tex]]','[[fontes/github/doc-interdisciplinar-4-semestre/referencia.json|Commit fixado da coleta]]'])

note('wiki/historico/evolucao.md','Antes, agora e próxima melhoria','''
| Aspecto | Entrega anterior | Código/documentação atual | Direção definida |
|---|---|---|---|
| Entrada do controle | SPP no ESP32 e serial para o Pi | BLE NUS diretamente no Pi; ESP32 e serial ainda no repositório como legado | Consolidar operação somente no Pi |
| App | Controle direcional Android | BLE para Android/iOS, telemetria em quatro abas, rota planejada, distribuição Android | Melhorar controle, retorno e confiabilidade |
| Motores | Integração ainda pendente nos relatórios | Cinemática, rampa, vigia, lock e backends real/simulado | Validar acionamento e parada no robô |
| IA | Vosk + modelo chamado Gemma 3B + eSpeak/MBROLA, local | Ollama local/rede, voz Edge/Piper/Kokoro, reserva, streaming e persona | Qualidade, latência, áudio e integração melhores |
| Escuta | Vosk no relato da interface | Vosk voltou a ser padrão em 09/09; Whisper disponível | Medir entendimento em situações reais |
| GPS | Integração declarada na conclusão de orquestração | Serviço existe; README atual informa módulo não montado | Implementar e validar GPS físico |
| Banco | MQTT → ingestor → TimescaleDB | Mesmo fluxo mais API FastAPI, controles de acesso e telas | Melhorar confiabilidade, qualidade e uso dos dados |
| Painel | Quarkus + SSE + Leaflet no PDF | API FastAPI, app Flutter e site estático | Informações coerentes, recentes e rastreáveis |
| Infraestrutura | VM do LARCC citada | Compose pronto; README relata execução em PC provisório | Confirmar implantação e continuidade da coleta |
| Estrutura | PLA/aço com ensaios manuais | Não foram encontrados CAD/STL atuais na pasta | Preservar herança e documentar alterações físicas |
| Gestão do conhecimento | Relatórios e documentação por repo | Este vault conecta fontes, estado, decisões e planos | Atualizar a cada teste, decisão e entrega |

“Atual” nesta tabela significa o retrato de 09/09/2026 das fontes inspecionadas. Operação física só deve passar para validada após ensaio registrado.

Fontes detalhadas: [[wiki/historico/relatorios-semestre]], [[wiki/modulos/index]], [[wiki/estado/git-local-e-remoto]] e [[wiki/estado/divergencias]]. Objetivos confirmados pelo usuário em 09/09/2026: [[wiki/planejamento/onde-queremos-ir]].
''','historico')

note('wiki/estado/onde-estamos.md','Onde estamos — estado atual do projeto','''
## Leitura correta do estado

**Implementado** significa encontrado no código. **Relatado** significa descrito por uma fonte, sem repetição do teste nesta sessão. **Pendente** significa lacuna documentada ou confirmação necessária. Um recurso pode estar implementado e ainda pendente de validação física.

| Subsistema | Evidência atual | Limite / próximo passo |
|---|---|---|
| Mecânica | Estrutura híbrida e ensaios manuais nos PDFs | Confirmar estado físico, medidas, rodas e alimentação atuais |
| BLE direto no Pi | `RobotEye/ble/nus.py`, serviço e publicação MQTT | Código e relatos de conexão; consolidar instalação sem ESP32 |
| Controle Flutter | Direcional, repetição de 300 ms e parada | Testar desconexão, troca de tela e comportamento real |
| Motores | Backend STEP/DIR, simulação, rampa, vigia de 1 s, RLock | README informa ausência de teste do motor real com esse código |
| Rota segura | Planejamento, persistência local, envio fatiado e roteamento | Não há consumidor de navegação; não segue a rota sozinho |
| GPS | Serviço NMEA e contrato prontos | Montagem e coleta atual não comprovadas; fontes divergem |
| Bateria | Contrato, banco e telas preparados | Não foi encontrado produtor físico de bateria |
| Wi-Fi | Serviço `nmcli`, status e roteamento | Testar aplicação e retorno; confirmar broker único |
| Face e conversa | Pipeline de IA/voz, painel, persona, reservas e recuperação de áudio | Métricas atuais e qualidade com usuários ainda precisam de coleta |
| Escuta | Vosk padrão; alternativa Whisper | Mudanças publicadas em 09/09; validar no ambiente de uso |
| MQTT e nuvem | Broker, bridge, ingestor, TimescaleDB e FastAPI | Disputa apt/Docker documentada; confirmar implantação e perdas |
| Visualização | App, site público e painel local do RobotEye | Distinguir dado simulado, comando recebido e estado medido |
| IA ligada à telemetria | Há integração MQTT para controle/painel | Não há consumo de `robo/voz/falar` pela fala nem contexto de bateria integrado |
| Relatório acadêmico | LaTeX com proposta e capítulos | Capítulo de resultados e estatística em desenvolvimento |

## Versões observadas

- App: `main`, HEAD `44d5001`, versão declarada `1.2.2+9`.
- Orquestrador: `main`, HEAD `98ee681`.
- RobotEye: `producao`, HEAD `43a6fe0`; `main` em `e1b26d7`.
- As três árvores de trabalho estavam limpas e as branches ativas em 0 à frente / 0 atrás do upstream após fetch.

Há histórico local adicional, detalhado em [[wiki/estado/git-local-e-remoto]]. O nome `producao` não prova que esse SHA está instalado no Raspberry Pi.

## Prioridade prática

Consolidar o caminho app → BLE no Pi → broker único → motores, em paralelo à melhoria da IA. Instalar o GPS e comprovar sua chegada ao banco e às telas. Registrar o que é real, simulado, atrasado ou ainda não medido. Ver [[wiki/planejamento/backlog]].
''','estado',sources=[source('app','pubspec.yaml'),source('orquestrador','README.md'),source('RobotEye','README.md'),source('RobotEye','src/roboteye/config.py')])

note('wiki/arquitetura/visao-geral.md','Arquitetura — responsabilidades e fronteiras','''
A Atlas combina uma plataforma física, três repositórios de software e um repositório acadêmico. Os programas executam em ambientes diferentes: celular, Raspberry Pi e servidor/PC da nuvem. Uma máquina de IA na rede é opcional no desenho atual.

| Pasta local | Repositório | Responsabilidade | Executa onde |
|---|---|---|---|
| `app` | `setrem-robot/aplicativo` | Direção BLE, rota planejada e consulta de dados | Celular; alvos adicionais no projeto Flutter |
| `orquestrador` | `setrem-robot/orquestrador` | Roteamento, motores, GPS, Wi-Fi, legado ESP32 e nuvem | Pi e host Docker |
| `RobotEye` | `setrem-robot/atlas_ai_v2` | Face, voz, IA, escuta, BLE e painel local | Pi ou ambiente de desenvolvimento |
| Sem checkout de trabalho | `doc-interdisciplinar-4-semestre` | Relatório LaTeX | Compilação documental |
| Sem checkout de trabalho | `.github` | Apresentação da organização | GitHub |

## Fronteiras importantes

**Comandos:** entram no Pi pelo BLE do RobotEye e chegam ao tópico `robo/comando/entrada`. O orquestrador roteia; o serviço de destino executa. A API de nuvem é de leitura e não comanda motores.

**Informações:** serviços publicam status; o orquestrador seleciona o que espelhar; a bridge envia apenas `robo/telemetria/#`; o ingestor grava; a API lê; app e site apresentam.

**Conversa:** microfone/painel/terminal → Assistant → Ollama → Speaker → áudio e eventos visuais. O painel também possui MQTT para observar/enviar comandos, mas isso não constitui integração da IA com bateria/GPS ou consumo de `robo/voz/falar`.

**Retirada do ESP32:** o transporte direto no Pi já existe, preservando os UUIDs NUS e o formato JSON. O firmware e o `serial_ingestor` seguem presentes como alternativa histórica. Retirar o componente da montagem precisa ser comprovado por um ensaio sem ele.

**Autonomia:** o código de rota aceita e encaminha pontos; não foi encontrado serviço que execute navegação. Hoje a descrição tecnicamente sustentada é plataforma teleoperada com assistente conversacional e infraestrutura de telemetria.

Veja [[wiki/arquitetura/mapa-comunicacao]], [[wiki/modulos/index]] e [[wiki/decisoes/registro]].
''','arquitetura',sources=[source('orquestrador','README.md'),source('app','COMO-FUNCIONA.md'),source('RobotEye','src/roboteye/ble/mqtt.py'),source('RobotEye','src/roboteye/web/comandos.py')])

note('wiki/arquitetura/mapa-comunicacao.md','Mapa de comunicação — atual e legado','''
## Controle atual implementado

```mermaid
flowchart LR
  A[App Flutter] -->|BLE NUS - JSON por linha| P[Ponte BLE no Pi - RobotEye]
  W[Painel web local] -->|MQTT| B[Broker local único]
  P -->|robo/comando/entrada| B
  B --> O[Orquestrador]
  O -->|robo/motores/comando| M[Motores]
  O -->|robo/wifi/comando| F[Wi-Fi]
  O -.->|robo/voz/falar| V[Consumidor de fala pendente]
  O -.->|robo/rota/comando| N[Navegação pendente]
  M --> D[Drivers STEP e DIR]
```

Setas tracejadas terminam em consumidores que ainda faltam. A seta para drivers representa implementação encontrada, não teste físico realizado agora.

## Telemetria e banco

```mermaid
flowchart LR
  G[GPS - serviço existente] --> O[Orquestrador]
  M[Estado comandado dos motores] --> O
  W[Estado Wi-Fi] --> O
  B[Bateria - produtor pendente] -.-> O
  O -->|robo/telemetria/#| L[Mosquitto local]
  L -->|bridge out QoS 1| R[Broker remoto]
  R --> I[Ingestor]
  I --> T[(TimescaleDB)]
  T --> F[FastAPI de leitura]
  F -->|Bearer| A[App - Agora, Trajeto, Histórico, Eventos]
  F -->|Rotas públicas| S[Site estático]
```

## Caminho legado preservado

```mermaid
flowchart LR
  A[App] --> E[ESP32]
  E -->|Serial| S[serial_ingestor no Pi]
  S -->|robo/comando/entrada| B[Broker local]
```

O relatório anterior usava SPP nesse caminho. O firmware presente hoje usa BLE. Não misturar as duas versões. O destino MQTT é compartilhado, permitindo manter o restante dos serviços.

## Conversa e expressão

```mermaid
flowchart LR
  M[Microfone] --> H[Vosk ou Whisper]
  H --> G[Gatilho e transcrição]
  W[Painel ou terminal] --> A[Assistant]
  G --> A
  A --> L[Ollama - rede ou local]
  L --> S[Frases e Speaker]
  S --> T[Edge, Piper ou Kokoro]
  T --> O[Áudio]
  S --> E[Eventos]
  E --> F[Face]
```

Os endereços e portas estão em [[wiki/configuracao/setup-completo]]. Os payloads ficam em [[wiki/api/contrato-mqtt]].
''','arquitetura',sources=[source('orquestrador','pi/services/orquestrador/src/orquestrador/main.py'),source('RobotEye','src/roboteye/ble/nus.py'),source('RobotEye','COMO-FUNCIONA.md')])

note('wiki/arquitetura/como-funciona.md','Como funciona — do toque à informação','''
## Um comando de frente

1. O operador pressiona frente no app. `RobotConnection` envia `{"cmd":"F"}` em UTF-8 com quebra de linha e repete o movimento a cada 300 ms.
2. A ponte BLE no Raspberry Pi recebe e valida a linha. O limite é 512 bytes. `EntregaMqtt` publica em `robo/comando/entrada` com QoS 1.
3. O roteador transforma `F` em `{"acao":"frente","velocidade":60}` e publica no tópico `robo/motores/comando`.
4. `ServicoMotores` converte a ação em velocidades esquerda/direita, renova o vigia e pede o alvo à rampa.
5. O laço de 50 ms avança a rampa e chama o backend. No modo simulado, registra os comandos; no real, ajusta STEP/DIR/EN.
6. Ao soltar/cancelar, o app envia `S`. O serviço zera a rampa imediatamente. Se as mensagens param de chegar, o vigia de 1 s também manda parar.

Não foram medidas latências entre essas etapas nesta sessão. O tick de 50 ms é frequência do laço, não taxa fixa de telemetria.

## Uma leitura até o banco

1. O GPS interpreta NMEA e produz `robo/gps/posicao`.
2. O orquestrador espelha para `robo/telemetria/gps`.
3. A bridge leva esse prefixo ao broker remoto; comandos não descem pela bridge configurada.
4. O ingestor extrai o tipo do tópico e usa `ts` numérico do payload, ou o instante de chegada se esse campo for ausente/inválido.
5. O registro entra na tabela `telemetria`, mantendo o payload JSONB.
6. A API consulta o histórico. O app distingue estado atual, trajeto, série e eventos; `idade_s` ajuda a identificar dados antigos.

## Três informações diferentes

| Informação | O que comprova | O que não comprova |
|---|---|---|
| Último botão pressionado | Intenção do operador | Recepção ou movimento |
| Comando observado no MQTT/painel | Entrada chegou ao barramento | Roda girou ou posição mudou |
| Status do serviço de motores | Alvo de ação e velocidades calculadas | Velocidade física medida por encoder |

O código atual não mede posição/encoder dos motores. A navegação, o GPS real e o retorno de execução pertencem às etapas de integração em [[wiki/planejamento/backlog]].
''','arquitetura',sources=[source('app','lib/services/robot_connection.dart'),source('orquestrador','pi/services/motores/src/motores/main.py'),source('orquestrador','cloud/ingestor/main.py')])

note('wiki/modulos/index.md','Catálogo dos componentes','''
| Componente | Função | Nota detalhada |
|---|---|---|
| App Flutter | Conexão BLE, direção, telemetria, mapa e rota planejada | [[wiki/modulos/aplicativo]] |
| Orquestrador | Validar, rotear e espelhar mensagens | [[wiki/modulos/orquestrador]] |
| Motores | Cinemática, rampa, vigia, simulação e GPIO | [[wiki/modulos/motores]] |
| GPS | Ler NMEA e publicar posição | [[wiki/modulos/gps]] |
| Wi-Fi | Configurar NetworkManager e publicar estado | [[wiki/modulos/wifi]] |
| ESP32 e serial_ingestor | Entrada alternativa/legada | [[wiki/modulos/legado-esp32]] |
| RobotEye | IA, voz, face, escuta, BLE e painel | [[wiki/modulos/roboteye]] |
| Nuvem | Brokers, ingestão, banco, API, túnel e site | [[wiki/modulos/nuvem]] |

O [[wiki/meta/inventario|inventário]] enumera arquivos rastreados, testes, scripts e documentação. As páginas explicam o papel das peças; os snapshots preservam o código consultado.
''','mapa')

note('wiki/modulos/aplicativo.md','Aplicativo — controle e informações','''
**Pasta:** `app` · **Repo:** `aplicativo` · **Versão declarada:** `1.2.2+9`.

## Organização

| Pasta/arquivo em `lib` | Responsabilidade |
|---|---|
| `main.dart`, `app/theme.dart`, `app/versao.dart` | Entrada, aparência e versão visível |
| `screens/connect_screen.dart` | Descoberta e conexão BLE; acesso à telemetria |
| `screens/control_screen.dart` | Direcional e desconexão |
| `screens/telemetria_screen.dart` | Abas Agora, Trajeto, Histórico e Eventos |
| `screens/rota_segura_screen.dart` | Planejamento de caminho e envio |
| `screens/ajustes_api_screen.dart` | Endereço e token da API |
| `services/robot_connection.dart` | Transporte BLE, repetição e envio de rota |
| `services/telemetry_api.dart` | Acesso HTTP e configuração persistida |
| `services/rota_store.dart` | Persistência da rota no aparelho |
| `models/robot_command.dart` | Comandos compactos |
| `models/telemetria.dart`, `models/rota_segura.dart` | Dados de telemetria e rota |
| `widgets` | Direcional, mapas, frescor do dado, gráficos e painéis |

## Funcionalidades e limites

O controle BLE é independente da internet. A visualização remota usa API e pode consultar histórico com o robô desligado. A parada depende de soltar/cancelar o botão e do vigia no serviço de motores. A rota é desenhada, salva e enviada em mensagens `inicio`, `ponto`, `fim`; isso não faz o robô percorrê-la autonomamente.

O projeto contém pastas Android, iOS, Linux, Windows, macOS e web, mas a presença de uma pasta de plataforma não comprova validação do BLE em todas elas. O alvo declarado é Android/iOS; a esteira de distribuição atual cobre Android.

## Distribuição

O workflow `deploy.yml` integra Shorebird. Alteração em Dart pode ser entregue por patch conforme o fluxo configurado; recursos e código nativo exigem nova release. Conferir a execução real do workflow antes de declarar uma distribuição concluída. Não houve build nem publicação nesta sessão.

Configuração salva pelo usuário prevalece sobre valores padrão da build. O app pode continuar apontando a uma API antiga após atualizar; revisar Ajustes antes de atribuir a falha ao código.

## Testes e continuidade

Existem testes de comando, direcional, telemetria e rota segura. Os comandos de verificação são `flutter analyze` e `flutter test`. Não foram executados nesta organização documental.

Próxima melhoria: retorno claro de conexão/recepção/execução, ensaios de desconexão e dados reais no mapa. [[wiki/planejamento/backlog]] · [[wiki/api/contrato-mqtt]].
''','modulo',sources=[source('app','ARQUITETURA.md'),source('app','README.md'),source('app','.github/workflows/deploy.yml'),source('app','lib/services/robot_connection.dart')])

note('wiki/modulos/orquestrador.md','Orquestrador — regras e barramento','''
O pacote `pi/services/orquestrador` recebe comandos, publica ordens de domínio e espelha quatro fontes de estado para telemetria. A biblioteca `_common` centraliza tópicos e o cliente MQTT.

## Peças principais

- `roteador.py`: lógica pura `rotear(dict) → lista de (tópico, payload)`.
- `ComandoRoteavel`: classe abstrata das regras; subclasses Motor, Voz, ParadaEmergencia, Rota e Wifi.
- `_ROTAS`: tabela de despacho por `tipo`; o formato compacto `cmd` é normalizado antes.
- `main.py`: integra essa lógica ao MQTT e espelha os tópicos selecionados.
- `_common/topics.py`: nomes canônicos. `mqtt_client.py`: publicação/assinatura, reconexão e heartbeat.

## Contrato efetivo

Direções: F frente, B trás, L esquerda, R direita, S parar. A intensidade padrão é 60. A forma contínua usa `acao=mover`, `linear` e `angular` entre -1 e 1. Cada eixo ausente vira zero individualmente; um eixo válido ainda pode mover o robô. Não assumir que qualquer mensagem incompleta implica parada total.

O roteador de rota valida mensagens individuais, mas não armazena nem executa o percurso. Voz e rota têm tópicos de saída sem consumidor funcional encontrado para falar/navegar. O Wi-Fi é encaminhado para validação e aplicação no serviço próprio.

Os testes presentes cobrem regras de despacho e normalização. A docstring promete tolerância a mensagens inválidas, mas isso não substitui validação de todas as entradas possíveis. Esta tarefa não foi uma auditoria exaustiva de robustez do software.

[[wiki/api/contrato-mqtt]] · [[wiki/decisoes/registro]] · [[wiki/modulos/motores]].
''','modulo',sources=[source('orquestrador','pi/services/orquestrador/src/orquestrador/roteador.py'),source('orquestrador','pi/services/orquestrador/src/orquestrador/main.py'),source('orquestrador','pi/services/_common/src/robo_common/mqtt_client.py')])

note('wiki/modulos/motores.md','Motores — comando, cálculo e acionamento','''
## Três responsabilidades

| Camada | Arquivo | Papel |
|---|---|---|
| Cálculo | `cinematica.py` | Velocidades de cada lado, saturação, conversão de ações e rampa |
| Acionamento | `acionamento.py` | Interface abstrata, implementação simulada e STEP/DIR/EN |
| Serviço | `main.py` e `vigia.py` | MQTT, timeout, estado, coordenação por lock e encerramento |

## Parâmetros do código

- `MOTORES_BACKEND=auto`: tenta hardware e pode cair para simulação. O log precisa ser consultado para saber o backend real.
- `COMANDO_TIMEOUT_S=1.0`: silêncio de movimento aciona parada; 0 desliga o vigia.
- `ACELERACAO=3.0`: rampa em unidades normalizadas por segundo; não é aceleração medida em m/s².
- `TICK_S=0.05`: laço de atualização a cada 50 ms.
- `MOTOR_ESQ_INVERTIDO`/`MOTOR_DIR_INVERTIDO`: ajustes de sentido conforme montagem.

Parada explícita e emergência zeram a rampa imediatamente no software. O backend real remove pulsos e desabilita os drivers. Tempo/distância física até parar dependem da montagem e não foram medidos aqui.

## Pinagem declarada, a confirmar na montagem

| Sinal | Esquerdo | Direito |
|---|---|---|
| STEP | BCM 20 | BCM 19 |
| DIR | BCM 21 | BCM 26 |
| EN | BCM 16 | BCM 13 |

São números BCM usados pelo código, não posições físicas do conector. O backend trabalha com duty de 50% para os pulsos; EN em LOW habilita e HIGH desabilita. A conferência elétrica e do driver/motor instalado é parte do ensaio de hardware.

## O que significa a telemetria

`robo/motores/status` contém `acao`, `velocidade`, `esquerda` e `direita`, e pode trazer `motivo`. Representa o alvo calculado. Estados iguais não são republicados a cada tick. Não há posição por encoder ou velocidade medida nesse serviço.

## Estado de validação

Há testes para cinemática, serviço, vigia e concorrência. O README registra que o motor real ainda não foi acionado com esse código. A próxima evidência deve registrar versão, backend efetivo, sentido de cada roda, parada por silêncio e observação física. [[wiki/planejamento/validacao]] e [[wiki/seguranca/index]].
''','modulo',sources=[source('orquestrador','pi/services/motores/src/motores/acionamento.py'),source('orquestrador','pi/services/motores/src/motores/main.py'),source('orquestrador','pi/services/motores/src/motores/cinematica.py')])

note('wiki/modulos/gps.md','GPS — implementação e integração pendente','''
O serviço `pi/services/gps` lê uma serial com `pyserial`, interpreta NMEA com `pynmea2` e acumula campos na classe `Posicao`. GGA fornece posição, fix e satélites; RMC acrescenta velocidade/rumo. A velocidade é convertida de nós para km/h.

Publicação de domínio: `robo/gps/posicao`. Espelhamento: `robo/telemetria/gps`. A posição válida exige fix e coordenadas disponíveis; o período é configurável por `GPS_INTERVALO_S`.

```json
{"lat":-28.2,"lon":-54.0,"fix":true,"satelites":7,"altitude_m":300.0,"velocidade_kmh":1.2,"rumo":90.0,"ts":1788969600}
```

Este payload é **exemplo ilustrativo** de formato, não leitura coletada do robô. Configure `GPS_PORT` e `GPS_BAUD` de acordo com o módulo identificado. Não foi encontrado inventário confiável do modelo físico ou da pinagem GPS atual.

## Pendência confirmada para este semestre

O usuário pediu implementar o GPS. O README atual informa que ele não está montado, apesar da conclusão histórica declarar integração. A tarefa é verificar módulo/ligação, observar sentenças reais, obter fix, conferir posição no MQTT, no banco e nas telas e testar perda de fix/reconexão.

O código não deve confundir última coordenada conhecida com posição atual válida. Esse comportamento, incluindo envelhecimento do fix e carimbo de tempo, precisa fazer parte do teste. A existência do serviço não demonstra precisão nem disponibilidade de sinal no campus.

[[wiki/estado/divergencias]] · [[wiki/planejamento/validacao]] · [[wiki/api/contratos]].
''','modulo',sources=[source('orquestrador','pi/services/gps/src/gps/main.py'),source('orquestrador','README.md'),'[[fontes/relatorios/OrquestradorPDF.pdf#page=38]]'])

note('wiki/modulos/wifi.md','Wi-Fi — provisionamento e estado','''
O serviço `pi/services/wifi` assina `robo/wifi/comando` e usa NetworkManager por `nmcli`. O roteador admite `conectar`, `listar` e `status`; a validação/aplicação está no módulo `rede.py`.

O comando de configuração entra pelo mesmo caminho das direções. Credenciais reais ficam fora do vault. O estado é publicado em `robo/sistema/wifi`, contendo conectado, SSID, IP e timestamp, e pode ser espelhado para a nuvem.

## Pontos de operação

- `robo-wifi.service` depende do ambiente e das permissões para alterar rede.
- A perda da rede não deve tirar o controle BLE do caminho local.
- O RobotEye inclui diagnóstico de rádio e scripts para separar o uso de Wi-Fi/Bluetooth; a existência do script não comprova qual adaptador está em uso hoje.
- Estado publicado no MQTT não garante confirmação de aplicação na interface do app. É uma melhoria a planejar.

O teste deve cobrir rede válida/inválida, retorno de status, reconexão da bridge e continuidade do BLE. [[wiki/configuracao/diagnostico]] e [[wiki/planejamento/backlog]].
''','modulo',sources=[source('orquestrador','pi/services/wifi/src/wifi/rede.py'),source('orquestrador','pi/services/wifi/src/wifi/main.py'),source('RobotEye','src/roboteye/radio.py')])

note('wiki/modulos/legado-esp32.md','ESP32 e serial — legado a retirar da operação','''
O firmware `esp32/esp32_ble_bridge/esp32_ble_bridge.ino` implementa BLE NUS, recebe JSON e encaminha pela serial. O serviço `serial_ingestor` no Pi publica as linhas no MQTT. O relatório do semestre anterior descreve uma versão com Bluetooth Classic/SPP; o firmware atual já é BLE.

## O que mudou

A ponte `RobotEye/src/roboteye/ble` assume o mesmo serviço NUS e publica diretamente em `robo/comando/entrada`. Isso elimina a placa intermediária e o trecho serial no caminho principal. O destino dos comandos permanece o mesmo.

## Decisão do semestre

**Objetivo confirmado pelo usuário:** retirar o ESP32 e manter somente o Raspberry Pi no robô. O código antigo é evidência de origem e pode continuar arquivado para consulta. Preservar documentação histórica não significa manter dependência de hardware na operação.

Para declarar a retirada concluída: ligar o robô sem ESP32, iniciar BLE no Pi, usar um único broker, dirigir/parar e comprovar os comandos no serviço de motores. Atualizar instalação, fotos e relatório acadêmico com esse ensaio.

[[wiki/decisoes/registro]] · [[wiki/planejamento/backlog]] · [[wiki/arquitetura/mapa-comunicacao]].
''','modulo',sources=[source('orquestrador','esp32/esp32_ble_bridge/esp32_ble_bridge.ino'),source('orquestrador','pi/services/serial_ingestor/src/serial_ingestor/main.py'),source('RobotEye','src/roboteye/ble/nus.py')])

note('wiki/modulos/roboteye.md','RobotEye — IA, escuta, voz, face e painel','''
**Pasta:** `RobotEye` · **Repo:** `atlas_ai_v2` · **Branch local:** `producao`.

## Mapa interno

| Área em `src/roboteye` | Papel |
|---|---|
| `core/assistant.py`, `core/events.py` | Coordenação da conversa e eventos de estado |
| `llm` | Ollama, modelo echo de teste, memória de conversa, persona e reserva |
| `hearing` | Microfone, gatilho de chamada, Vosk e Whisper |
| `speech` | Síntese, player, acabamento de áudio, fila de fala e reserva |
| `face` | Estado visual, animação, expressões, formas e renderização |
| `web` | Página de configuração/conversa, estado do Pi e comandos |
| `ble` | NUS no Raspberry Pi e entrega ao broker |
| `config.py`, `setup_wizard.py` | Configuração centralizada e assistente inicial |
| `diagnostics.py`, `memoria.py`, `radio.py` | Diagnóstico de dependências, RAM e conectividade |
| `voice_catalog.py`, `voices.py` | Catálogo e escolha de vozes |

## IA e voz atuais

O código conversa com Ollama e permite trocar de backend. O README descreve uso de `qwen3:8b` em máquina da rede e `gemma3:1b` como reserva local. O padrão da dataclass em `config.py` é `llama3.2:1b`; esses valores não são a configuração ativa do robô. O `.env` real não foi copiado nem usado como prova de implantação.

Os motores de voz incluem Edge, Piper, Kokoro e null. O modo descrito no README privilegia voz online e reserva Piper. A síntese e a resposta trabalham por frases/blocos para reduzir espera. A face reage aos eventos e à amplitude de áudio.

## Mudança mais recente da escuta

Em 09/09, `a88c2dd` tornou Vosk o padrão e `e1b26d7` acrescentou silêncio antes da primeira palavra. Whisper continua disponível. Essas mudanças estão em `main` e no conteúdo de `producao` observado.

O código também inclui sinais sonoros de escuta, finalização por silêncio, controle de concorrência entre escuta e inferência, correções de contexto e `keep_alive`. Há recuperação da captura/saída quando o dispositivo de áudio USB reaparece.

## Integrações existentes e ausentes

A ponte BLE publica comandos e o painel usa MQTT para observar/enviar comandos. Portanto, dizer que “o RobotEye não usa MQTT” seria incorreto. O que ainda falta é conectar a conversa à telemetria e consumir `robo/voz/falar` para o app pedir fala.

O painel escuta `robo/comando/entrada`; a indicação de comando recebido não é medição do motor. Seus controles e a configuração de PIN pertencem à rede local do robô; não equivalem à API pública da nuvem.

## Números relatados, não medidos nesta sessão

O README relata Pi 5 de 8 GB, OS Lite, display 800×480, face em 30 FPS e medições de arranque/CPU/temperatura. O próprio texto reconhece conflito nas medições de RAM da face. Preservamos essa ressalva em [[wiki/estado/divergencias]], sem transformar medições antigas em promessa de desempenho atual.

## Como melhorar

Definir perguntas de referência, registrar transcrição e tempo até primeiro áudio, avaliar respostas corretas sobre a SETREM, testar ausência de rede e manter a face responsiva sob carga. [[wiki/planejamento/validacao]] detalha um ensaio proposto.
''','modulo',sources=[source('RobotEye','README.md'),source('RobotEye','src/roboteye/config.py'),source('RobotEye','src/roboteye/hearing/vosk_ears.py'),source('RobotEye','src/roboteye/web/comandos.py'),source('RobotEye','src/roboteye/core/assistant.py')])

note('wiki/modulos/nuvem.md','Nuvem — da mensagem à informação','''
## Componentes encontrados

| Componente | Local em `orquestrador` | Função |
|---|---|---|
| Mosquitto remoto | `cloud/mosquitto` | Receber telemetria com autenticação |
| Ingestor | `cloud/ingestor/main.py` | Assinar MQTT e inserir registros |
| TimescaleDB | `cloud/timescaledb/init` | Armazenar payloads e tempo |
| FastAPI | `cloud/api/app` | Consultas de leitura, acesso e respostas |
| Cloudflared | `cloud/docker-compose.yml` | Caminho HTTP via túnel configurável |
| Ambiente local | `cloud/compose.local.yml`, `cloud/scripts` | Execução de desenvolvimento e simulação |
| Site | `site/index.html`, `ao-vivo.js`, `config.js`, `estilo.css` | Apresentação estática e dados públicos |

O Compose de nuvem tem cinco serviços. O modo local combina a definição principal com um override. O README relata hospedagem provisória no PC de um integrante e migração pendente para o LARCC; a implantação atual não foi acessada nesta tarefa.

## Confiabilidade encontrada

A bridge é somente de saída para `robo/telemetria/#`, com QoS 1 e sessão persistente. A configuração local de exemplo prevê 100.000 mensagens e 32 MiB de fila. A duração suportada depende do volume e tamanho das mensagens; não há garantia geral de “14 horas sem perda”.

O ingestor reconecta ao banco e tenta gravar um registro até duas vezes. Se ambas as tentativas falham, registra descarte. O esquema não tem identificador único de evento, e QoS 1 pode reenviar mensagens. A fila do broker não equivale a persistência garantida no banco.

## Dados de demonstração

`robo-falso.py` publica pelo broker; `semear-demonstracao.py` gera dados para visualização; `telemetria_falsa.py` também está disponível. Esses recursos permitem testar telas e integração, mas não demonstram GPS montado, bateria sensoriada ou motor em movimento.

## Próximas melhorias

Medir atraso, perdas/duplicatas, reconexão, origem real/simulada e crescimento do banco. Definir retenção e backup/restauração, confirmar host operacional e tornar as telas explícitas quando os dados estiverem atrasados. [[wiki/api/contratos]] e [[wiki/planejamento/backlog]].
''','modulo',sources=[source('orquestrador','cloud/docker-compose.yml'),source('orquestrador','cloud/ingestor/main.py'),source('orquestrador','pi/mosquitto/apt/robo.conf.example'),source('orquestrador','cloud/timescaledb/init/01_schema.sql')])

note('wiki/api/contrato-mqtt.md','Contrato MQTT e BLE — o que o código usa','''
> [!info] Referência reconciliada com o código
> O contrato original do orquestrador ainda descreve ESP32 obrigatório em alguns parágrafos. Aqui o caminho principal é BLE no Pi, e os nomes/payloads foram conferidos nos produtores, roteador e consumidores.

## BLE e entrada

| Item | Valor |
|---|---|
| Serviço NUS | `6e400001-b5a3-f393-e0a9-e50e24dcca9e` |
| RX — celular escreve | `6e400002-b5a3-f393-e0a9-e50e24dcca9e` |
| TX — notificação ao celular | `6e400003-b5a3-f393-e0a9-e50e24dcca9e` |
| Formato | Objeto JSON em UTF-8, terminado por quebra de linha |
| Limite da linha na ponte | 512 bytes |
| Entrada MQTT | `robo/comando/entrada` |

| Letra | Ação |
|---|---|
| F | Frente |
| B | Trás/ré |
| L | Esquerda |
| R | Direita |
| S | Parar |

As letras corretas são F/B/L/R/S. `R` não significa ré e `D` não é direção aceita no formato compacto.

## Comandos expandidos — exemplos válidos de formato

```json
{"tipo":"motor","acao":"frente","velocidade":80}
```
```json
{"tipo":"motor","acao":"mover","linear":0.8,"angular":-0.3}
```
```json
{"tipo":"voz","texto":"Olá, sou a Atlas."}
```
```json
{"tipo":"parada_emergencia"}
```

Velocidade é limitada a 0–100, padrão 60. Eixos são limitados a -1–1; positivo linear avança e positivo angular gira à direita. Ausência de um eixo zera só aquele eixo. A parada normalizada é `{"acao":"parar","velocidade":0}`.

## Roteamento de comandos

| Entrada `tipo` | Destino | Payload repassado/normalizado | Consumidor |
|---|---|---|---|
| motor / comando compacto | `robo/motores/comando` | `acao`, `velocidade` ou eixos | motores |
| parada_emergencia | `robo/motores/comando` | `acao=parar`, `velocidade=0` | motores |
| voz | `robo/voz/falar` | `texto` | Pendente |
| wifi | `robo/wifi/comando` | `acao`, SSID e credencial quando necessários | wifi |
| rota | `robo/rota/comando` | `inicio`, `ponto` ou `fim` | Navegação pendente |

## Rota fatiada

```json
{"tipo":"rota","acao":"inicio","total":1,"nome":"exemplo"}
```
```json
{"tipo":"rota","acao":"ponto","i":0,"lat":-28.2,"lon":-54.0}
```
```json
{"tipo":"rota","acao":"fim"}
```

As coordenadas acima são ilustrativas. O roteador valida cada mensagem; não remonta a rota. Publicar `fim` não implica navegação iniciada.

## Estado e espelhamento

| Tópico de domínio | Produtor | Retido no domínio | Destino de telemetria |
|---|---|---|---|
| `robo/gps/posicao` | gps | Sim | `robo/telemetria/gps` |
| `robo/motores/status` | motores | Sim | `robo/telemetria/motores` |
| `robo/sistema/wifi` | wifi | Sim | `robo/telemetria/wifi` |
| `robo/sistema/bateria` | A definir | Previsto pelo contrato | `robo/telemetria/bateria` |

GPS inclui `lat`, `lon`, `fix`, `satelites`, `altitude_m`, `velocidade_kmh`, `rumo` e `ts`. Motores incluem `acao`, `velocidade`, `esquerda`, `direita` e eventualmente `motivo`. Wi-Fi publica `conectado`, `ssid`, `ip`, `ts`. O formato previsto de bateria usa `percentual` e `tensao_v`.

Os serviços publicam heartbeat em `robo/sistema/heartbeat/<servico>`; a bridge usa `robo/sistema/bridge_status`. Esses tópicos não entram automaticamente no espelhamento de quatro domínios. `robo/voz/intencao` existe como constante, sem que isso comprove um fluxo de intenção integrado.

A publicação da ponte BLE usa QoS 1, sem retain. A bridge replica `robo/telemetria/# out 1`. Conferir QoS e retain no produtor específico antes de introduzir novo tópico. Não há, no código examinado, os tópicos `robo/motores/velocidade`, `robo/motores/parada` ou `robo/diagnostico/uptime` apresentados na versão anterior do vault.

[[wiki/api/contratos]] · [[wiki/arquitetura/mapa-comunicacao]] · [[wiki/seguranca/index]].
''','contrato',sources=[source('orquestrador','pi/services/_common/src/robo_common/topics.py'),source('orquestrador','pi/services/orquestrador/src/orquestrador/roteador.py'),source('RobotEye','src/roboteye/ble/nus.py'),source('RobotEye','src/roboteye/ble/mqtt.py'),source('orquestrador','docs/contrato-mqtt.md')])

note('wiki/api/contratos.md','API HTTP e modelo de dados','''
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
''','contrato',sources=[source('orquestrador','cloud/api/app/main.py'),source('orquestrador','cloud/api/app/consultas.py'),source('orquestrador','cloud/api/app/seguranca.py'),source('orquestrador','cloud/timescaledb/init/01_schema.sql'),source('orquestrador','cloud/ingestor/main.py')])

note('wiki/hardware/especificacoes.md','Hardware — herança e inventário a confirmar','''
| Peça | Evidência disponível | Situação documental |
|---|---|---|
| Chassi aço e carenagem PLA | Relatório Estrutura | Construção e ensaios manuais relatados |
| Raspberry Pi 5 de 8 GB | README RobotEye | Configuração de robô relatada |
| Display 800×480 | README RobotEye | Usado nas medições relatadas |
| Microfone e áudio USB | Relatório Interface e código/README RobotEye | Hardware/modelo exato atual a conferir |
| Motores Nema 23 | Relatório Estrutura | 2 unidades previstas/descritas; acionamento atual a validar |
| Drivers TMC2209 | Código de acionamento e docs | Implementação destinada a esses drivers; confirmar peças e ajuste |
| ESP32 | Relatório e firmware no orquestrador | Legado; retirada é objetivo confirmado |
| GPS | Serviço NMEA, PDF e READMEs divergentes | Modelo, montagem, porta e leitura física a confirmar |
| Bateria e alimentação | Relatórios e contrato de telemetria | Capacidade, proteção, autonomia e sensoriamento a confirmar |
| Refrigeração | README RobotEye relata calor sob IA e ausência de ventoinha | Conferir montagem atual e medir sob carga |

## Lacunas do acervo

Não foram localizados arquivos CAD/STL, esquema elétrico consolidado, lista de compras comprovada, capacidade de bateria confirmada ou fotografias recentes avulsas da montagem. Os PDFs incluem imagens históricas. Esta ausência é do acervo inspecionado, não afirma que a equipe não possui os arquivos em outro lugar.

## O que registrar na próxima bancada

Fotografia geral e interna; identificação do Pi e SO; modelos das placas; pinagem efetiva; fonte/bateria e tensões nominais; motores/drivers e ajustes; portas USB/serial; display; cooler; alterações desde os PDFs. Vincular esses dados a uma nota de experimento.

A pinagem declarada pelo código dos motores está em [[wiki/modulos/motores]]. Não foi inventado esquema elétrico para preencher as lacunas.

As medidas históricas estão em [[wiki/historico/estrutura-anterior]]. Orçamento e decisões novas devem ficar separados do custo estimado antigo.
''','hardware',sources=['[[fontes/relatorios/EstruturaPDF.pdf#page=20]]',source('RobotEye','README.md'),source('orquestrador','pi/services/motores/src/motores/acionamento.py')])

note('wiki/seguranca/index.md','Proteções existentes e limites reais','''
## Movimento

O app repete movimentos a cada 300 ms e envia parada ao soltar/cancelar. A ponte BLE no Pi possui parada ao desconectar. O serviço de motores para após 1 s de silêncio por padrão. `RLock` serializa mudanças de estado entre callback MQTT e tick, inclusive emergência sem rampa.

Esses mecanismos aparecem no código; não são quatro garantias independentes contra qualquer falha. O lock evita corrida entre threads, mas não atua se o Pi travar ou perder energia. A parada física precisa de ensaio e de avaliação do conjunto mecânico/elétrico.

## Rede e dados

| Mecanismo encontrado | Limite |
|---|---|
| Broker local em `127.0.0.1:1883` na configuração de exemplo | Confirmar qual configuração está instalada |
| Broker remoto com usuário/senha | Exemplo padrão usa 1883; TLS aparece comentado/opcional |
| Bridge só de telemetria para fora | Não representa canal de comando remoto pela API |
| Usuário `robo_leitura` para a API | Conferir criação/permissões na instância implantada |
| Token Bearer estático | Não há login com expiração automática implementado |
| Consultas parametrizadas e filtros | Inspeção documental não é auditoria completa de segurança |
| Rate limit e cabeçalhos HTTP | Dependem do acesso via proxy e configuração real |
| Coordenadas públicas arredondadas | Reduz precisão numérica; não assegura anonimato ou impossibilidade de inferir localização |

A versão anterior do vault afirmava TLS mútuo, ACLs por serviço e um usuário de ingestão restrito que não foram comprovados pelos arquivos atuais. O ingestor usa configuração de banco própria; somente a separação explícita da API de leitura foi confirmada.

## Operação do conhecimento

O vault não contém valores de `.env`, chaves de assinatura ou senhas de instalação. O código arquivado vem dos arquivos rastreados; fontes acadêmicas privadas continuam locais. Antes de compartilhar o vault, verificar o material privado e os futuros registros de bancada que forem adicionados.

[[wiki/configuracao/setup-completo]] · [[wiki/planejamento/validacao]] · [[wiki/estado/divergencias]].
''','referencia',sources=[source('app','lib/services/robot_connection.dart'),source('RobotEye','src/roboteye/ble/nus.py'),source('orquestrador','pi/services/motores/src/motores/main.py'),source('orquestrador','cloud/timescaledb/init/02_usuario_leitura.sh'),source('orquestrador','pi/mosquitto/config/conf.d/bridge.conf.example')])

note('wiki/configuracao/setup-completo.md','Operação — por onde começar','''
Esta página organiza os caminhos já presentes nos repositórios. Não foi feita instalação, atualização no robô ou publicação na nuvem durante a montagem do vault.

## Ambientes e portas declaradas

| Ambiente | Ferramentas/componentes | Porta/configuração |
|---|---|---|
| Celular | App Flutter e BLE | NUS; API configurada no app |
| Raspberry Pi | Python, systemd, BlueZ, Mosquitto, áudio/vídeo e serviços | MQTT local 1883; painel RobotEye 8080 |
| IA local ou de rede | Ollama | 11434 por padrão |
| Nuvem/local Docker | Mosquitto, ingestor, TimescaleDB, API e túnel | MQTT 1883; PostgreSQL 5432 interno; API local 8000 |
| Site de desenvolvimento | Servidor estático | 8080 no exemplo do README |

O site de desenvolvimento e o painel RobotEye usam a mesma porta nos exemplos, mas normalmente em hosts diferentes. Na mesma máquina, escolher outra porta para o site.

## Pi e retirada do ESP32

1. Conferir inventário físico, SO, áudio e display.
2. Conferir os instaladores do RobotEye e do orquestrador, suas paths e unidades systemd.
3. Escolher **um broker MQTT local**. A configuração apt já está documentada em `pi/mosquitto/apt/robo.conf.example`; evitar o conflito com o Compose do Pi.
4. Conferir `roboteye-ble`, `robo-orquestrador`, `robo-motores`, `robo-gps` e `robo-wifi`, conforme os componentes efetivamente instalados.
5. Executar o teste sem ESP32 e sem depender de `serial_ingestor`.

O repositório da interface fornece `setup-raspberry-pi.sh`; `--service`, `--bluetooth-app` e seleção de branch fazem parte do fluxo documentado. Antes de instalar, ler os arquivos da versão que será usada. Uma atualização do RobotEye não atualiza automaticamente todos os demais repositórios.

## Desenvolvimento sem hardware

[[wiki/configuracao/ambiente-local]] descreve a nuvem local e simulação. Para o app, executar `flutter pub get`, `flutter analyze` e `flutter test` em `app`. Para RobotEye, usar o setup da plataforma e seu ambiente virtual, sem confundir o ambiente ARM do robô com o Windows.

## Configuração sensível

Os exemplos versionados indicam os nomes necessários: `.env.example` do RobotEye, `cloud/.env.example`, `cloud/.env.local.example`, `bridge.conf.example` e `android/key.properties.example`. O vault documenta finalidade e localização, sem guardar valores reais.

Registrar SHA instalado e configuração relevante **sem credenciais** em cada experimento. [[wiki/estado/git-local-e-remoto]] explica a diferença entre publicado e implantado.
''','operacao',sources=[source('orquestrador','docs/setup-pi.md'),source('orquestrador','docs/setup-cloud.md'),source('RobotEye','scripts/setup-raspberry-pi.sh'),source('RobotEye','scripts/roboteye-update.service'),source('orquestrador','pi/mosquitto/apt/robo.conf.example')])

note('wiki/configuracao/ambiente-local.md','Ambiente local — testar o caminho dos dados','''
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
''','operacao',sources=[source('orquestrador','docs/ambiente-local.md'),source('orquestrador','cloud/scripts/ambiente-local.sh'),source('orquestrador','cloud/scripts/robo-falso.py')])

note('wiki/configuracao/diagnostico.md','Diagnóstico — descobrir em que etapa falhou','''
| Sintoma | Verificar primeiro | Evidência a registrar |
|---|---|---|
| App não encontra Atlas | Serviço BLE, adaptador, UUID NUS e anúncio | Log de `roboteye-ble`, aparelho e versão |
| Conecta mas não move | Comando entrou no MQTT? Broker único? Backend simulado? | Tópico de entrada, serviço motores e backend |
| Para no meio do toque | Repetição do app e timeout dos motores | Intervalos entre comandos e log do vigia |
| GPS sem mapa | Serial/NMEA, fix e mensagem no tópico antes da API | Modelo, porta, amostra real e idade |
| Dados antigos nas telas | `ts`, `idade_s`, bridge e ingestor | Horários de captura/recepção e origem |
| API 401 | Endereço salvo e presença do token correto | HTTP status, sem copiar credencial |
| API 503 em `/saude` | Conexão com o banco | Logs de API/banco |
| Erro de túnel | API de pé e configuração/host do cloudflared | Estado dos serviços e destino do túnel |
| Voz muda após falha USB | Dispositivo, captura/reprodução e recuperação | Log de áudio e identificação USB |
| IA demora ou muda qualidade | Backend/modelo efetivo, rede, contexto e temperatura | Modo rede/local, tempos e carga |
| Painel indica frente, roda parada | Indicação é comando recebido, não sensor | Comparar MQTT, serviço, driver e roda |

## Leituras úteis no Pi

```bash
systemctl status roboteye roboteye-ble mosquitto robo-orquestrador robo-motores
journalctl -u robo-motores -n 80 --no-pager
journalctl -u roboteye -n 80 --no-pager
ss -ltnp
```

Unidades ausentes indicam que a instalação precisa ser identificada, não autorizam presumir que o robô usa outro serviço. Não executar comandos de movimento como primeiro teste de conectividade.

Para escutar dados já presentes no broker local:

```bash
mosquitto_sub -h 127.0.0.1 -t 'robo/motores/status' -v
mosquitto_sub -h 127.0.0.1 -t 'robo/telemetria/gps' -v
```

Ao registrar logs, remover senhas, tokens e conteúdo de conversas que não precisa constar no projeto. Relacionar cada ocorrência à nota do módulo e ao commit instalado.
''','operacao',sources=[source('orquestrador','README.md'),source('RobotEye','README.md'),source('orquestrador','pi/scripts/verificar-telemetria.sh')])

print('Primeiro conjunto de notas gravado.')

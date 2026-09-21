---
title: "Validação — como demonstrar o avanço"
tipo: planejamento
estado_documental: proposto
atualizado: 2026-09-09
tags:
  - atlas
  - planejamento
---

# Validação — como demonstrar o avanço

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

### T-IA-1 — a Atlas é acordada de forma confiável?

> [!warning] Pendência aberta desde a troca para Vosk
> O tempo de escuta foi medido no Pi e melhorou; a **precisão com voz humana não foi validada** — o ensaio disponível usou a voz sintética do robô, e nela nenhum dos dois reconhecedores acertou a palavra de despertar. Ver [[wiki/revisoes/2026-09-09-escuta-vosk-hardware]]. Este é o ensaio que decide se [[wiki/decisoes/registro|DEC-08]] fica.

Com `journalctl -u roboteye -f` aberto, e pessoas diferentes falando (incluindo voz aguda, que é o público real):

1. Só o nome — "Atlas!" — e esperar. Esperado: bipe, face em espera, e "Oi?" se a pergunta não vier.
2. Nome e pergunta na mesma frase — "Atlas, quanto é dois mais dois?".
3. Nome, pausa, pergunta — o modo como as pessoas realmente falam.
4. Uma frase **sem** o nome, para conferir que ele não responde à sala.
5. Repetir os itens 1 a 3 **logo depois de ela terminar de falar**, sem esperar. É o caso que o silêncio de partida corrige.

Anotar, para cada tentativa, a linha `frase fechada pelo vosk em N ms` e o texto transcrito.

Critério proposto: o nome é reconhecido na maioria das tentativas de cada pessoa, e o item 4 não desperta.

Se aparecer `ouvi '<pergunta sem o nome>', mas nao era comigo`, o reconhecimento perdeu o nome — não é defeito do gatilho. Saídas: `ROBOTEYE_HEARING_BACKEND=whisper` (volta ao anterior, custa ~2 s por pergunta) ou tolerar quase-acertos do nome em `hearing/gatilho.py`.

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

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

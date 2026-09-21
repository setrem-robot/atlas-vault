---
title: "Onde queremos ir — melhoria geral da Atlas"
tipo: planejamento
estado_documental: objetivos-confirmados-criterios-propostos
atualizado: 2026-09-09
tags:
  - atlas
  - planejamento
---

# Onde queremos ir — melhoria geral da Atlas

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

## Fontes e conferência

- [[wiki/diario/2026-09-09|Instrução do usuário e registro da sessão]]
- [[wiki/estado/onde-estamos]]

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

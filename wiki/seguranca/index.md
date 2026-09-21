---
title: "Proteções existentes e limites reais"
tipo: referencia
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - referencia
---

# Proteções existentes e limites reais

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

## Fontes e conferência

- [app/lib/services/robot_connection.dart](https://github.com/setrem-robot/aplicativo/blob/44d500160ecf13d7d1db2a4fe0c54052d352c0aa/lib/services/robot_connection.dart)
- [RobotEye/src/roboteye/ble/nus.py](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/src/roboteye/ble/nus.py)
- [orquestrador/pi/services/motores/src/motores/main.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/motores/src/motores/main.py)
- [orquestrador/cloud/timescaledb/init/02_usuario_leitura.sh](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/timescaledb/init/02_usuario_leitura.sh)
- [orquestrador/pi/mosquitto/config/conf.d/bridge.conf.example](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/mosquitto/config/conf.d/bridge.conf.example)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

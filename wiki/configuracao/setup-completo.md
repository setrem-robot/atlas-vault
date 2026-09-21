---
title: "Operação — por onde começar"
tipo: operacao
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - operacao
---

# Operação — por onde começar

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

## Fontes e conferência

- [orquestrador/docs/setup-pi.md](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/docs/setup-pi.md)
- [orquestrador/docs/setup-cloud.md](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/docs/setup-cloud.md)
- [RobotEye/scripts/setup-raspberry-pi.sh](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/scripts/setup-raspberry-pi.sh)
- [RobotEye/scripts/roboteye-update.service](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/scripts/roboteye-update.service)
- [orquestrador/pi/mosquitto/apt/robo.conf.example](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/mosquitto/apt/robo.conf.example)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

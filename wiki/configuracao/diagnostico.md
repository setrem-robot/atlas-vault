---
title: "Diagnóstico — descobrir em que etapa falhou"
tipo: operacao
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - operacao
---

# Diagnóstico — descobrir em que etapa falhou

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

## Fontes e conferência

- [orquestrador/README.md](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/README.md)
- [RobotEye/README.md](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/README.md)
- [orquestrador/pi/scripts/verificar-telemetria.sh](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/scripts/verificar-telemetria.sh)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

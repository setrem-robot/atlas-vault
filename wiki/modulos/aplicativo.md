---
title: "Aplicativo — controle e informações"
tipo: modulo
estado_documental: revisado
atualizado: 2026-09-21
tags:
  - atlas
  - modulo
---

# Aplicativo — controle e informações

**Pasta:** `app` · **Repo:** `aplicativo` · **Versão declarada:** `1.2.4+11` (release de 21/09; APK abaixo).

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

## Atualização 2026-09-21 — switch de IA e release 1.2.4+11

- **Switch IA Local / IA Nuvem** na tela de controle: `models/iaModo.dart` (enum; o `code` é contrato com o robô), `RobotConnection.setIaModo` manda `{"tipo":"ia","modo":…}` pela ponte BLE, guarda em `SharedPreferences` e reenvia ao conectar. O widget é um `Switch` **de texto, sem ícone** de propósito (ver distribuição). Ver [[wiki/api/contrato-mqtt]] e [[wiki/modulos/roboteye]].
- **Release `1.2.4+11`** (APK): https://github.com/setrem-robot/aplicativo/releases/tag/v1.2.4%2B11 — precisa ser instalado uma vez.

## Distribuição

O workflow `deploy.yml` integra Shorebird. Alteração em Dart pode ser entregue por patch; **ícone/asset novo, pacote nativo ou versão nova exigem release** (APK). **Achado em 21/09:** o patch OTA vinha **falhando desde 16/09** — a feature de telemetria daquele dia adicionou ícones e mudou a fonte `MaterialIcons` (tree-shaking), o que patch não pode fazer, mas nenhuma release foi cortada; o workflow "Deploy" ficou vermelho em silêncio e nada chegou aos celulares por OTA nesse intervalo. Corrigido cortando a release `1.2.4+11`, que re-sincroniza a base dos patches. **Lição:** conferir a execução do workflow "Deploy" após todo push do app; adicionar ícone novo obriga release. Não confiar em "patch OTA" sem ver o run verde.

Configuração salva pelo usuário prevalece sobre valores padrão da build. O app pode continuar apontando a uma API antiga após atualizar; revisar Ajustes antes de atribuir a falha ao código.

## Testes e continuidade

Existem testes de comando, direcional, telemetria e rota segura. Os comandos de verificação são `flutter analyze` e `flutter test`. Não foram executados nesta organização documental.

Próxima melhoria: retorno claro de conexão/recepção/execução, ensaios de desconexão e dados reais no mapa. [[wiki/planejamento/backlog]] · [[wiki/api/contrato-mqtt]].

## Fontes e conferência

- [app/ARQUITETURA.md](https://github.com/setrem-robot/aplicativo/blob/44d500160ecf13d7d1db2a4fe0c54052d352c0aa/ARQUITETURA.md)
- [app/README.md](https://github.com/setrem-robot/aplicativo/blob/44d500160ecf13d7d1db2a4fe0c54052d352c0aa/README.md)
- [app/.github/workflows/deploy.yml](https://github.com/setrem-robot/aplicativo/blob/44d500160ecf13d7d1db2a4fe0c54052d352c0aa/.github/workflows/deploy.yml)
- [app/lib/services/robot_connection.dart](https://github.com/setrem-robot/aplicativo/blob/44d500160ecf13d7d1db2a4fe0c54052d352c0aa/lib/services/robot_connection.dart)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

---
title: "Estrutura — o que a equipe anterior entregou"
tipo: historico
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - historico
---

# Estrutura — o que a equipe anterior entregou

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

## Fontes e conferência

- [[fontes/relatorios/EstruturaPDF.pdf#page=22|Dimensões — p. 22]]
- [[fontes/relatorios/EstruturaPDF.pdf#page=26|Limitações e ensaios — p. 26 em diante]]

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]

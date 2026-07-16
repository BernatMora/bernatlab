# Resum - Capitol 9: Privadesa de la IA

## La idea clau

Quan fas servir ChatGPT, Claude, o qualsevol LLM al nuvol, **estes enviant les teves dades a una empresa**. Aixo inclou:
- Les teves preguntes (que poden contenir informacio personal).
- El context que passes (documents, correus, etc.).
- Les respostes generades.
- Metadades (hora, ubicacio, IP, etc.).

Aixi funciona la **IA tradicional**. Te un preu: la teva privadesa.

La **IA local** (Ollama) es diferent: tot corre al **teu ordinador**. Ningun mes te acces a les teves dades. Es la diferencia entre **tenir un assistent al núvol** i **tenir-lo a casa**.

## Per que importa

Casos reals on la privadesa es crucial:
- **Dades personals**: historial medica, correus, calendaris.
- **Dades de negoci**: informacio financera, plans estrategics.
- **Dades d'altres**: el que escrius sobre familia, amics, clients.
- **Dades sensibles de l'hort**: ubicacio exacta, sistema de seguretat, alarmes.

Si envies tot això a un LLM al nuvol, **l'empresa que el te** pot:
- Guardar-ho als seus servidors (per entrenar futurs models).
- Analitzar-ho per als seus interessos.
- Cedir-ho a tercers (governs, altres empreses).
- Ser vulnerada (data breach).

## Avantatges de la IA local

1. **Privadesa total** - Les dades no surten del teu PC.
2. **Cost zero** - No pagues per consulta.
3. **Sense limits** - Pots fer tantes consultes com vulgudes.
4. **Sense censura** - Cap empresa decideix quines preguntes pots fer.
5. **Personalitzable** - Pots afinar el model amb les teves dades.
6. **Funciona offline** - Sense internet, funciona igual.

## Limitacions de la IA local

Per ser honest, la IA local tambe te inconvenients:
- **Menys potent** - Els millors models (GPT-4, Claude Opus) son al nuvol.
- **Mes lent** - La teva RPi no te les GPUs del núvol.
- **Cal hardware** - Cal un PC decent per a models grans.
- **Setup mes complex** - Has d'instal·lar i configurar.

Pero per a molts casos, **la IA local es mes que suficient**.

## El paper del model al núvol

Aquest llibre sha fet amb un model al nuvol (minimax-m3:cloud). No es perfecte per a privadesa, pero:
- Es mes barat que GPT-4.
- No envia dades a Meta, Google, o OpenAI.
- Pot funcionar en servidors europeus (millor per a GDPR).

**Si vols maxima privadesa**, pots:
- Usar un model local (Ollama) per a les teves dades sensibles.
- Usar el nuvol nomes per a tasques generals (resumir, generar text).
- Combinar els dos: cerca al local primer, nuvol com a backup.

## Bones practiques

- **No comparteixis informacio sensible** amb cap sistema (local o nuvol).
- **Xifra els embeddings** si els emmagatzemes.
- **Fes neteja periodica** dels historials de converses.
- **Llegeix els termes del servei** si uses un LLM al nuvol.

## Connexions

- **M5 del llibre** - Seguretat i privadesa al servidor.
- **M4 cap 8** - Implementacio RAG que es queda local.
- **M4 cap 10** - Aplicacio practica: Hort Osona privat.

## El dilema

Cal ser honest: hi ha un **trade-off** entre:
- **Privadesa** (local, mes lent, menys potent).
- **Potencia** (nuvol, menys privat, mes rapid).

Per a cada cas, la millor opcio depen de les teves necessitats. No hi ha una resposta universal.

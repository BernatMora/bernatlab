# Capítol 33 — Què és la IA local i per què a Hort Osona

> *"L'any 2026, tenir un assistent intel·ligent a casa ja no és qüestió d'enviar les teves dades a una empresa de Califòrnia. Pots tenir el cervell al teu Mac i la saviesa al teu hort."*

## 33.1 Què és la IA local

**IA local** (també anomenada **IA on-premise** o **self-hosted AI**) és executar models d'intel·ligència artificial al teu propi ordinador, sense enviar res al núvol. Quan fas una pregunta a ChatGPT, el text viatja a un servidor d'OpenAI, es processa allà, i torna la resposta. Amb IA local, tot el procés passa dins la teva màquina.

Això és possible gràcies a dues coses:

1. **Models petits però capaços**. Fa tres anys, per tenir un model útil calia un servidor amb 100 GB de RAM. Avui, n'hi ha prou amb un MacBook amb 16 GB per fer córrer un model que escriu en català, raona sobre text, i segueix instruccions complexes.

2. **Eines com Ollama**. Ollama és una aplicació que descarrega models, els posa en marxa amb una sola comanda, i exposa una API local compatible amb la d'OpenAI. Tu li dius `ollama run gemma3:12b` i tens un assistent a la terminal.

## 33.2 Diferència entre IA al núvol i IA local

| Aspecte | IA al núvol (ChatGPT, Claude) | IA local (Ollama) |
|---|---|---|
| On es processa | Servidors de l'empresa | El teu Mac/RPi |
| Privadesa | Les dades surten del teu ordinador | Tot es queda a casa |
| Cost | Subscripció mensual (~20 €/mes) | Gratuït, després de comprar el hardware |
| Velocitat | Ràpida (cloud potent) | Depèn del model i el hardware |
| Català | Molt bo | Variable, depèn del model |
| Disponibilitat | Si tens Internet | Funciona offline |
| Personalització | Limitada | Pots entrenar amb les teves dades |

Per a Hort Osona, **la IA local és ideal** perquè:

- Les teves 76 fitxes de cultius, 30+ guies, i el coneixement de l'hort no surten de casa.
- Pots preguntar coses específiques del teu terreny, varietats locals, el clima d'Osona.
- No pagues subscripció.
- Funciona encara que TallCable o el router estiguin caiguts.

## 33.3 Què pots fer amb IA local a Hort Osona

Aquestes són les aplicacions reals que veurem al llarg del mòdul:

1. **Assistent hort Osona**. Li preguntes en català: "Quan he de sembrar les carbasses a la zona d'Osona?" Et contesta basant-se en les 76 fitxes i el calendari lunar d'Osona.

2. **Resum de documents**. Tens un PDF de 50 pàgines sobre compostatge. Li dius "Fes-me'n un resum d'una pàgina" i te'l fa.

3. **Cercar informació**. Tens 30+ guies. En lloc de cercar per paraules clau, li preguntes "Què he de fer si el tomàquet té míldiu?" i troba els paràgrafs rellevants.

4. **Generar textos**. Necessites un correu al veí per demanar permís d'ampliar l'hort? Li dius "Escriu un correu amable" i te l'escriu.

5. **Veu**. Li parles en lloc d'escriure, mentre treballes a l'hort. Et contesta amb veu.

6. **Integració amb el BernatLab**. La Raspberry consulta Ollama al Mac via Tailscale. Les dades dels sensors LoRa alimenten un assistent que t'avisa: "El sòl del sector 3 està massa sec; rega'l demà al matí."

## 33.4 Què NO és (i què sí)

**NO és**:

- Una còpia exacta de ChatGPT. Els models locals són menys capaços que GPT-4 o Claude Opus. Són útils però no miracles.
- Màgia. Necessites bons models, bons prompts, i bons documents.
- Privat per defecte. Si copies les dades a un model al núvol, sí que surten. Cal configurar bé.

**SÍ és**:

- Prou bona per a 90% de les tasques quotidianes.
- Molt personalitzable. Pots afinar-la amb els teus documents.
- Transparent. Saps exactament què fa perquè és al teu ordinador.
- Econòmica. Després del hardware, tot és gratis.

## 33.5 Com aprendràs a usar-la

El mòdul segueix un camí pràctic:

1. **Cap 34**: instal·lar Ollama al Mac i fer les primeres preguntes.
2. **Cap 35**: com triar el model adequat (català, mida, velocitat).
3. **Cap 36**: com funciona la cerca semàntica (embeddings, vectorstores).
4. **Cap 37**: muntar un RAG amb les 76 fitxes d'hort.
5. **Cap 38**: client web per parlar amb l'assistent des del navegador.
6. **Cap 39**: integrar Ollama amb l'API del BernatLab.
7. **Cap 40**: afegir-hi veu.
8. **Cap 41**: privadesa i seguretat.
9. **Cap 42**: casos d'ús reals, amb 10 consultes que pots fer ja.

## 33.6 El que necessites

**Hardware mínim**:

- Mac amb Apple Silicon (M1, M2, M3, M4) i 16 GB de RAM. Recomanable 32 GB per a models grans.
- Alternativa: PC amb targeta gràfica NVIDIA (RTX 3060 o superior) amb 8+ GB VRAM.
- Raspberry Pi 4 amb 8 GB: només per a models molt petits (1B-3B paràmetres).

**Software**:

- macOS, Linux o Windows 10/11.
- 10-30 GB d'espai lliure per als models.
- Ollama (gratis, descarregable de ollama.com).

**Coneixements previs**:

- Ús bàsic de la terminal (Cap 3 del Mòdul 1).
- Python intermedi (saber instal·lar llibreries, escriure scripts petits).

## 33.7 Privadesa des del primer dia

Una regla d'or:

> **Si una dada és prou sensible per no explicar-la a un desconegut al carrer, no l'enviïs a cap servei d'IA al núvol.**

Això inclou:

- Dades mèdiques.
- Informació financera personal.
- Correspondència privada.
- Dades d'altres persones sense el seu consentiment.
- Secrets comercials o professionals.

Amb IA local, aquest problema desapareix: la dada no surt del teu ordinador. Però encara cal configurar-ho bé, cosa que veurem al Cap 41.

## 33.8 El futur a Hort Osona

A mesura que escrigui més capítols del llibre i tinguis més dades, l'assistent es fa més savi:

- **Fitxes de cultius** (76) → sap tot sobre cada varietat.
- **Guies** (30+) → sap sobre compost, plagues, associacions, calendari lunar.
- **Dades de sensors** (M3) → sap l'estat real del teu hort en temps real.
- **Bitàcoles** → aprèn què funciona i què no al teu terreny.
- **Correspondència** (si vols) → recorda el que has après amb cada veí.

D'aquí un any, el teu Hort Osona serà un dels millor documentats de Catalunya, i el teu assistent podrà respondre qualsevol pregunta que li facis sobre el que has après.

## 33.9 Resum

La IA local et permet tenir un assistent potent al teu Mac o Raspberry, sense enviar dades al núvol, sense subscripció, i personalitzable amb els teus propis documents. Per a Hort Osona és una eina natural: 76 fitxes de cultius, 30+ guies, dades de sensors, i tot el coneixement que has anat acumulant. En els propers capítols aprendrem a instal·lar Ollama, triar un bon model, i muntar un sistema RAG complet.

## 33.10 Exercicis pràctics

1. Comprova quin Mac tens: Apple Icon → About This Mac. Anota el xip (M1/M2/M3/M4) i la RAM.
2. Comprova l'espai lliure al disc: `df -h` (a la terminal). Hauries de tenir almenys 30 GB.
3. Comprova la versió de macOS: Apple Icon → About This Mac. Hauries de tenir macOS 13+ per a la millor compatibilitat.
4. Fes una llista de les 5 preguntes que t'agradaria poder fer al teu assistent hort Osona.
5. Comprova que tens Python 3.10+: `python3 --version`.
6. Documenta al README del projecte el teu hardware i les preguntes que tens en ment.

Paraules clau: **IA local, self-hosted AI, on-premise, Ollama, RAG, embeddings, vectorstore, LLM, model, prompt, privadesa, Apple Silicon, M1, M2, M3, M4, Mac, RAM, 16 GB, 32 GB, català, model de llengua, self-hosted, núvol, subscripció, ChatGPT, Claude, GPT-4, Opus, alternativa, open source, codi obert, transparent**.

# Qüestionari - Capitol 9: Privadesa de la IA

> 15 preguntes · ~20 min · 7 test + 8 obertes

## Pregunta 1
Quan usem un LLM al nuvol, quina informacio s'envia?

- [ ] Nomes la pregunta
- [x] Preguntes, contexte adjunt, respostes, metadades (hora, IP, etc.)
- [ ] Res, tot es xifrat
- [ ] Nomes les metadades

## Pregunta 2
Que vol dir "IA local"?

- [ ] Una IA que nomes funciona en horari local
- [x] Una IA que s'executa al teu propi ordinador sense enviar dades a tercers
- [ ] Una IA de pagament
- [ ] Una IA gratuita

## Pregunta 3
Quin dels seguents NO es un risc d'enviar dades a un LLM al nuvol?

- [ ] Emmagatzematge per part del proveidor
- [ ] Data breach
- [x] El model es massa petit
- [ ] Cessio a tercers (governs, altres empreses)

## Pregunta 4
Quin avantatge de la IA local es mes important al BernatLab?

- [x] Privadesa total
- [ ] Mes velocitat
- [ ] Millor qualitat de les respostes
- [ ] Mes models disponibles

## Pregunta 5
Quin es el risc mes gran de la IA al nuvol?

- [ ] Es de pagament
- [x] Les teves dades poden ser usades per entrenar futurs models
- [ ] Es mes lenta
- [ ] Nomes funciona en angles

## Pregunta 6
Quina llei europea es important considerar en termes de IA i privadesa?

- [ ] LPI (Llei de Propietat Intel·lectual)
- [x] GDPR (General Data Protection Regulation)
- [ ] LEC (Llei d'Edificacio Catalana)
- [ ] LOREG

## Pregunta 7
Quin dels seguents NO es una limitacio de la IA local?

- [ ] Menys potent que els millors models al nuvol
- [ ] Cal hardware decent
- [x] Es mes cara
- [ ] Setup mes complex

## Pregunta 8 (oberta)
Explica amb les teves paraules: per que la privadesa es un tema tant important en la IA? Pensa en quines dades sensibles podries enviar a un LLM sense adonar-te.

Pistes per respondre:
- Dades personals: historial, correus, calendaris.
- Dades de negoci: informacio financera, plans estrategics.
- Dades d'altres: informacio sobre familia, amics, clients.
- Exemples concrets: una consulta medica, un correu sobre un projecte secret, una foto d'un document.

## Pregunta 9 (oberta)
Imagina que tens un correu sobre una situacio legal delicada (un conflicte amb un vei, per exemple). Quins riscos hi ha si envies aquest correu a ChatGPT per obtenir consell? Argumenta amb detall.

Pistes per respondre:
- Risc 1: el correu pot quedar emmagatzemat als servidors d'OpenAI.
- Risc 2: pot ser usat per entrenar futurs models.
- Risc 3: si hi ha data breach, queda exposat.
- Risc 4: l'empresa pot cedir les dades a tercers.
- Alternativa: model local (Ollama).

## Pregunta 10 (oberta)
Quina relacio hi ha entre privadesa i control de les dades? Per que tenir la IA al teu servidor et dona mes poder que tenir-la al nuvol?

Pistes per respondre:
- Amb IA local: tens el control absolut. Les dades no surten.
- Amb IA al nuvol: el proveidor te les dades. Tu nomes tens un servei.
- Analogia: llogar una casa vs tenir-la en propietat.
- Que passa si el proveidor canvia les condicions?

## Pregunta 11 (oberta)
Argumenta: prefereixes pagar una subscripcio a ChatGPT Plus (20$/mes) o tenir un servidor local amb Ollama? Posa arguments economics i de privadesa.

Pistes per respondre:
- ChatGPT Plus: 20$/mes, 240$/any. Sense hardware.
- Local: 0$/mes (electricitat ~50$/any), cal hardware (500-2000€).
- Payback: 1-2 anys.
- Mes enlla: privadesa, disponibilitat, personalitzacio.

## Pregunta 12 (oberta)
Que pasa si una empresa (Meta, Google, OpenAI) canvia les seves politiques de privadesa i comença a usar les converses per a altres fins? Com t'afectaria?

Pistes per respondre:
- Si ja has enviat dades, no pots recuperar-les.
- Son "bones" fins que deixen de ser-ho.
- Exemple historic: canvis de termes a Instagram, WhatsApp, etc.
- L'avantatge de la IA local: tu controles el teu desti.

## Pregunta 13 (oberta)
Quines bones practiques implementaries al BernatLab per garantir la privadesa quan usis IA, tant si es local com al nuvol?

Pistes per respondre:
- Bones practiques generals: minimitzar dades enviades, anonimitzar, xifrar, auditar.
- Pel local: tenir el servidor en una xarxa privada, actualitzar el sistema, fer backups xifrats.
- Pel nuvol: llegir els termes, usar comptes dedicats, no enviar informacio personal.

## Pregunta 14 (oberta)
Com evaluaries la privadesa dun model LLM abans de fer-lo servir? Quines preguntes clau et faries?

Pistes per respondre:
- Pregunta 1: on s'executa? Local o nuvol?
- Pregunta 2: quines dades recull per defecte?
- Pregunta 3: pot usar les meves dades per entrenar?
- Pregunta 4: te una opcio "no entrenar amb les meves dades"?
- Pregunta 5: en cas de breach, que pasa?
- Pregunta 6: esta allotjat en servers europeus (GDPR)?

## Pregunta 15 (oberta)
Defenssa: encara que la IA local es mes limitada (model mes petit, menys potent), per que creus que al BernatLab es la millor opcio? Posa 3 arguments solids.

Pistes per respondre:
- Argument 1: privadesa - les dades es queden al servidor.
- Argument 2: cost - sense subscriptcions mensuals.
- Argument 3: control - tu决定 quines dades s'usen.
- Argument 4 (bonus): independencia - no depens de tercers.
- Argument 5 (bonus): personalitzacio - pots afinar el model per al teu cas.

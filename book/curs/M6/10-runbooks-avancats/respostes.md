# Respostes - Capitol 10: Runbooks avançats

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es un runbook

**Resposta correcta**: Un document que descriu pas a pas com fer una tasca concreta del sistema.

**Explicacio**: Un runbook es la versio "instruccions d'operacio" de la documentacio tecnica. No ensenya, instruccions. Es un document que poses davant quan estas sota pressio i necessites recordar l'ordre exacte de les coses. Es practic, no teorica.

---

## Pregunta 2: Diferencia amb tutorial

**Resposta correcta**: El tutorial ensenya, el runbook instruccions pas a pas per actuar.

**Explicacio**: Un tutorial te explica conceptes i t'ensenya a fer coses. Un runbook et dona els pasos exactes per resoldre un problema concret. Un tutorial es per quan tens temps per aprendre; un runbook es per quan el sistema esta caigut i necessites actuar rapid.

---

## Pregunta 3: Parts essencials

**Resposta correcta**: Totes (Requisits, Passos numerats, Verificacio, Rollback).

**Explicacio**: Totes les parts son importants. Sense requisits no saps que necessites. Sense passos numerats no tens ordre. Sense verificacio no saps si ha funcionat. Sense rollback, si algo va malament estas atrapat. Es un paquet complet.

---

## Pregunta 4: Millor moment

**Resposta correcta**: Quan el sistema funciona be i tens temps.

**Explicacio**: Escriure els runbooks "en calent" (sistema funcionant) permet recollir informacio que no recordes quan falla: l'ordre correcte, les comandes exactes, els errors tipics. Si esperes a l'incident, tindras 30 missatges oberts, un sistema caigut, i el cap en mil llocs. No escriuras res de profit.

---

## Pregunta 5: Postmortem

**Resposta correcta**: Un document que s'escriu despres d'un incident per aprendre.

**Explicacio**: Un postmortem es l'analisi "a posteriori" d'un incident. El nom ve de la medicina: analitzar les causes de la mort per evitar futurs casos. L'objectiu NO es trobar un culpable, sino entendre que ha fallat i com evitar que torni a passar.

---

## Pregunta 6: Estructura postmortem

**Resposta correcta**: Resum, timeline, causa arrel, impacte, accions.

**Explicacio**: L'estructura classica d'un postmortem te aquestes parts: resum (1 paragraf), timeline (que va passar i quan), causa arrel (per que va passar), impacte (que conseqüencies va tenir), accions preventives (que farem perque no torni a passar). Es la diferencia entre "una historia" i "una historia amb conclusions".

---

## Pregunta 7: Per que son importants

**Resposta correcta**: Perque permeten actuar ordenadament, sense oblidar passos, en situacions d'estres.

**Explicacio**: Quan el sistema falla a les 3 de la matinada, tens el cap espes, molta pressio, i el risc d'oblidar un pas es molt alt. Un runbook et guia pas a pas. Es com un checklist de pilot: en una emergencia, la memoria falla, pero el checklist no.

---

## Pregunta 8: Tamany ideal

**Resposta correcta**: 1-2 pagines.

**Explicacio**: Si es mes curt, probablement no te prou detall. Si es mes llarg, ningú el llegira sencer en una urgencia. 1-2 pagines es el sweet spot: prou detall per ser util, prou curt per ser utilitzable. Si cal mes, parteix-lo en dos runbooks.

---

## Pregunta 9 (oberta): Estructura runbook

**Resposta model**:

L'estructura ideal d'un runbook d'incidencia te les següents seccions:

**1. Titol**

Clar i descriptiu. No "Runbook 1" sino "Contenidor de Home Assistant caigut". Que amb nomes llegir el titol ja saps si es el que busques.

**2. Resum**

Un paragraf breu explicant que cobreix aquest runbook. Tipus: "Aquest runbook cobreix el cas en que un contenidor Docker del BernatLab ha caigut i no es reinicia automaticament." Serveix per confirmar rapidament que has trobat el document correcte.

**3. Símptomes**

Com saps que estàs en aquesta situacio. Exemples concrets: "Rebs una alerta de Telegram 'ContenidorCaigut'", "el servei no respon al navegador", "els logs contenen 'OOMKilled'". Es la llista de senyals que et porten a aquest runbook.

**Per que es important**: si tens un problema pero els teus simptomes no coincideixen amb cap runbook, tens un problema NO documentat. Cal crear un runbook nou (despres) o adaptar-ne un.

**4. Severitat**

P1, P2, P3 o similar. P1 = critic (tot caigut). P2 = important (degradacio). P3 = molest. Serveix per prioritzar: si tens 2 incidents alhora, saps quin atendre primer.

**5. Diagnostic pas a pas**

Les comandes exactes per confirmar que realment estas en aquesta situacio. Exemple:
- `docker ps -a | grep Exited`
- `docker logs NOM --tail 50`
- `curl -v http://localhost:8123`

**Per que es important**: sense diagnostic, podries estar tractant un problema que NO es el que penses. Imagina que reinicies HA quan el problema es que no te xarxa. Has perdut el temps.

**6. Solucio**

Els passos exactes per resoldre, en ordre. Amb les comandes COPIABLES. Exemple:
```bash
cd ~/bernatlab
docker compose restart homeassistant
sleep 30
docker logs homeassistant --tail 20
```

**Per que es important**: en una urgencia, no vols haver de pensar "quines comandes feia servir?". Vull copiar-enganxar i llest.

**7. Verificacio**

Una llista de checkboxes per confirmar que el problema s'ha resolt. Exemple:
- [ ] El contenidor esta UP
- [ ] El servei respon
- [ ] L'alerta s'ha resolt a Alertmanager
- [ ] Les metricas son normals a Grafana

**Per que es important**: un cop "tornat a aixecar" no vol dir "funcionant". La verificacio et dona la seguretat que el problema esta realment resolt i no es nomes una mica millor.

**8. Rollback**

Que fer si els passos anteriors no funcionen O empitjoren les coses. Com tornar a l'estat anterior. Exemple:
- Revertir canvis a docker-compose.yml
- Restaurar el volum desde backup
- `docker compose down` i tornar a posar la versio anterior

**Per que es important**: en un incident es pot fer PEOR. Si un pas no funciona, cal saber com tornar enrrere. Es la xarxa de seguretat.

**9. Contactes i referencies**

Links utils: dashboard de Grafana, documentacio del projecte, forum on buscar ajuda. Telefons de contacte si es un cas amb collaboracio externa.

**Per que es important**: en una urgencia, no vols perdre temps buscant on esta el dashboard o quina era la URL del forum.

Aquesta estructura es IMPORTANT perque et dona un marc mental clar: primer entendre (resum, simptomes), confirmar (diagnostic), actuar (solucio), verificar, i tenir plan B (rollback). Es el cicle complet de gestio d'incidents.

---

## Pregunta 10 (oberta): Postmortem inventat

**Resposta model**:

Aqui tens un postmortem d'un incident inventat (pero realista):

```markdown
# Postmortem: Home Assistant ha estat reiniciant-se cada 5 minuts

## Resum
Durant 4 hores, Home Assistant s'ha reiniciat en bucle cada 5-7 minuts
despres d'una actualitzacio. Les automatitzacions de la casa no funcionaven.

## Timeline
- 2026-04-15 09:00: Watchtower actualitza HA de 2024.4 a 2024.5
- 2026-04-15 09:12: Rebo alerta: "ContenidorCaigut homeassistant"
- 2026-04-15 09:15: Comprovo: HA torna a aixecar-se pero cau als 5 min
- 2026-04-15 09:20: Miro logs: "MemoryError: out of memory"
- 2026-04-15 09:30: Investigant a la web: bug conegut a HA 2024.5 amb
  integracio de Xiaomi
- 2026-04-15 09:45: Decideixo fer downgrade a 2024.4
- 2026-04-15 09:50: Cambio tag al docker-compose, docker compose up -d
- 2026-04-15 10:00: HA estable de nou, sense reinicis
- 2026-04-15 10:15: Marco alerta com a "Resolved"
- 2026-04-15 10:20: Escric aquest postmortem
- 2026-04-15 10:30: Afegeixo regles per evitar Watchtower automatic a HA

## Causa arrel
Un bug a HA 2024.5 provoca memory leak quan tens la integracio de Xiaomi
activada. La memoria puja fins que el contenidor es queda sense RAM i es
reinicia. Watchtower ha actualitzat automaticament sense que jo sabés.

## Impacte
- 4 hores amb HA inestable
- Automatitzacions no funcionaven (llums, alarma, etc.)
- Familia afectada: calefaccio automatica no va funcionar al mati
- Risc: si passava de nit, podia haver durat 12 hores

## Que ha anat be
- L'alerta de Telegram s'ha disparat als 12 min, no als 12 hores
- He pogut accedir per SSH des del movil
- Tenia el docker-compose amb tags especifics (facil fer downgrade)
- He trobat la solucio rapid a Google (bug report a GitHub)
- Watchtower nomes ha tocat HA, no la base de dades

## Que ha anat malament
- Watchtower ha actualitzat HA sense que jo ho sapigués
- No havia llegit el CHANGELOG de HA 2024.5
- No tenia regla per deshabilitar Watchtower a HA
- El contenidor no tenia limit de memoria (va poder menjar tota la RAM)
- L'alerta es dispara quan JA ha caigut, no quan la memoria puja

## Accions preventives
- [ ] Treure la label de Watchtower a Home Assistant
- [ ] Actualitzar HA nomes manualment (1 cop al mes, havent llegit CHANGELOG)
- [ ] Posar limit de memoria a HA: mem_limit: 2g
- [ ] Crear alerta: "HA memoria > 1.5GB durant 30 min"
- [ ] Afegir al runbook de HA: "primer pas, llegir CHANGELOG"
- [ ] Documentar aquest incident al runbook
- [ ] Revisar altres serveis que Watchtower actualitza automaticament
```

La gràcia d'aquest postmortem es que es molt ESPECIFIC: te hores, te noms de versions, te logs concrets. D'aqui 6 mesos, quan llegeixi aquest document, entendré exactament que va passar i que fer per evitar-ho. 

A mes, les "accions preventives" son totes CONCRETES i ACCIONABLES. No posa "mirar mes de prop les actualitzacions" sino "treure la label de Watchtower a Home Assistant i fer-ho manualment". Es a dir, son coses que es poden fer avui i que tenen un impacte mesurable.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici desde zero observant cada pas.
- **0-2 encerts**: Repassem junts el capitol abans de continuar.

## Que fer si has encertat totes

- Felicitats! Has acabat el **Modul 6 (Operativa 24/7)**.
- Comparteix els teus runbooks amb la comunitat.
- Escriu un postmortem cada vegada que tinguis un incident real.
- Considera muntar un sistema de "on-call" per a tu i la teva familia.

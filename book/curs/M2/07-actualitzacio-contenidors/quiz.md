# Qüestionari - Capitol 7: Actualitzacio de contenidors

> 10 preguntes · ~15 min

## Pregunta 1
Que fa principalment Watchtower?

- [ ] Fa backups dels contenidors
- [x] Mira si hi ha noves versions de les imatges i actualitza els contenidors automaticament
- [ ] Esborra imatges antigues
- [ ] Sincronitza volums entre hosts

## Pregunta 2
Quina es la diferencia entre "update" i "upgrade"?

- [ ] Son sinonims
- [x] Update es el proces; upgrade es el resultat concret d'una nova versio
- [ ] Update nomes es per a aplicacions; upgrade per a sistema operatiu
- [ ] Update nomes funciona a Windows

## Pregunta 3
Que es una estrategia "blue-green"?

- [ ] Canviar la paleta de colors de la web
- [x] Mantenir dues versions corrent i canviar el tràfic nomes quan la nova funciona
- [ ] Fer actualitzacions de nit
- [ ] Usar una base de dades blava i una verda

## Pregunta 4
Que es un "rolling update"?

- [ ] Fer actualitzacions nomes en divendres
- [x] Actualitzar un servei de mica en mica, substituint instances gradualment
- [ ] Una actualitzacio que triga molt
- [ ] Reiniciar el servidor

## Pregunta 5
Per que es important afegir labels als serveis que vols que Watchtower actualitzi?

- [ ] Per estetica
- [x] Perque Watchtower nomes actualitzi els contenidors que tu vols, no tots
- [ ] Per a que Watchtower s'inici mes rapidament
- [ ] Per a que els contenidors siguin mes segurs

## Pregunta 6
Quin es l'interval recomanable per a Watchtower?

- [ ] Cada 5 min
- [x] Un cop al dia (WATCHTOWER_POLL_INTERVAL=86400)
- [ ] Un cop al mes
- [ ] Mai

## Pregunta 7
Que es un "healthcheck" en un context de contenidors?

- [ ] Una revisio medica
- [x] Una comanda que Docker executa per saber si el servei esta funcionant be
- [ ] Un analisi de vulnerabilitats
- [ ] Un diagnostic del hardware

## Pregunta 8
Que vol dir "zero-downtime deployment"?

- [ ] Actualitzar el hardware
- [x] Actualitzar sense que els usuaris notin cap tall del servei
- [ ] Una actualitzacio que no costa diners
- [ ] Fer actualitzacions sense connexio a Internet

## Pregunta 9 (oberta)
Explica amb les teves paraules: quins son els avantatges i els inconvenients de les actualitzacions automatiques (amb Watchtower) vs les manuals? En quins casos usaries cada un?

Pistes per respondre:
- Automatic: estalvia feina, pero no tens control.
- Manual: tens control total, pero cal dedicacio.
- Pensa en serveis critics (bases de dades) vs serveis menors (eines d'analisi).

## Pregunta 10 (oberta)
Al BernatLab tens un Nextcloud amb una base de dades MariaDB i vols actualitzar el Nextcloud a una nova versio. Com ho faries pas a pas? Tingues en compte que Watchtower esta activat pero vols tenir el control.

Pistes per respondre:
- Primer pas obligatori: backup de la base de dades i del volum.
- Comprovar compatibilitat amb plugins abans.
- Desactivar Watchtower temporalment per al servei.
- Fer l'actualitzacio manual amb docker compose.
- Verificar i tornar a activar Watchtower.
- Si falla, restaurar el backup.

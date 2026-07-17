# Qüestionari - Capitol 7: Actualitzacio de contenidors

> 15 preguntes · ~20 min

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
- [x] Mantenir dues versions corrent i canviar el trafic nomes quan la nova funciona
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

## Pregunta 11 (oberta)
Per que creus que les actualitzacions automatitzades tenen mala fama entre els administradors de sistemes? Es mereixcuda aquesta fama o es un mite? Argumenta amb exemples del BernatLab.

Pistes per respondre:
- Cas classic: actualitzacio automatica que trenca un servei a les 3 de la matinada.
- Watchtower te la opcio de notificar abans de reiniciar.
- Es pot automatitzar nomes les actualitzacions de seguretat.
- Trade-off: comoditat vs estabilitat.

## Pregunta 12 (oberta)
Quina relacio hi ha entre la frequencia d'actualitzacio i la finestra de risc? Com afecta al BernatLab (100.115.134.76) tenir els serveis desactualitzats durant setmanes vs dies? Calcula mentalment el risc.

Pistes per respondre:
- Finestra de risc: temps entre que es publica una vulnerabilitat i l'aplicacio del pegat.
- Cada dia desactualitzat es un dia mes exposat.
- Un atac automatitzat pot comprometre el sistema en hores un cop publicada la vulnerabilitat.
- Trade-off: estabilitat vs seguretat.

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "Watchtower es perillós, jo actualitzo manualment quan me'n recordo". Argumenta per que aixo te un cost operatiu amagat i proposa una estrategia mixta que combini el millor dels dos mons.

Pistes per respondre:
- Memoria humana vs automatitzacio: oblidar actualitzacions es facil.
- Les actualitzacions de seguretat son urgents i no esperen.
- Es poden usar notificacions (Watchtower en mode "monitor", no update).
- Es pot combinar: automatitzar les actualitzacions menors i fer manual les majors.

## Pregunta 14 (oberta)
Aplica el concepte d'actualitzacio al cas concret del BernatLab amb l'stack d'Hort Osona (Ollama, ChromaDB, Open WebUI). Per a cada servei, proposa una politica d'actualitzacio: automatica amb Watchtower, manual, o mixta. Justifica cada decisio considerant el risc i l'impacte.

Pistes per respondre:
- Ollama: actualitza sovint per nous models. Conv Watchtower?
- ChromaDB: la base de coneixement es local; actualitzar nomes si hi ha canvis.
- Open WebUI: aplicacio web, vulnerabilitats son importants. Conv Watchtower.
- Que passa si Ollama s'actualitza i trenca la compatibilitat amb els embeddings existents?

## Pregunta 15 (oberta)
Quines consequencies te per a la disponibilitat del servei fer actualitzacions sense previ avís? Com pot el BernatLab planificar les finestres de manteniment per minimitzar l'impacte als usuaris (inclús si nomes ets tu)? Pensa en horaris, testing previ i rollback.

Pistes per respondre:
- Els usuaris (tu mateix) volen estabilitat.
- Es pot definir una finestra de manteniment (per exemple, diumenges a les 4h).
- Testing previ en entorn separat (perfil dev de Compose).
- Tenir un pla de rollback clar: backup + docker-compose.down + restaurar imatge anterior.
- Trade-off: disponibilitat vs seguretat.

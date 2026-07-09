# Capítol 51 — Filosofia operativa: del DIY al servei 24/7

> *"Un servidor personal no és un experiment: és un servei. I com a tal, cal tractar-lo."*

## 51.1 El salt mental: de provar a operar

Quan comences amb un homelab, estàs en mode **experiment**: proves coses, toques, trenques, repares. Però en algun moment, el servidor comença a allotjar coses que **importen**:

- Dades de sensors.
- Una web pública.
- Un assistent d'IA.
- Còpies de seguretat.
- Un bot de Telegram.

Llavors cal canviar la mentalitat: ja no estàs experimentant, estàs **operant un servei**. I això implica:

- **Fiabilitat**: el servei ha d'estar disponible.
- **Recuperabilitat**: si falla, ha de poder tornar-se a aixecar.
- **Observabilitat**: has de saber què passa.
- **Mantenibilitat**: el sistema ha de ser fàcil d'actualitzar.

## 51.2 SLA personal

Un **SLA** (Service Level Agreement) és un contracte sobre la qualitat d'un servei. En un homelab, ets l'**empresa i el client alhora**. Defineix el teu SLA personal:

- **Disponibilitat objectiu**: 99% (3.6 dies de caiguda a l'any) o 99.9% (8.8 hores a l'any)?
- **Temps de resposta**: 24 h per a incidents crítics.
- **Temps de resolució**: 4-8 h per a incidents crítics.
- **Manteniment programat**: dilluns de 3 a 5 de la matinada?

Això és flexible, però cal posar-ho per escrit.

## 51.3 El principi de "boring tech"

**Boring tech** (tecnologia avorrida) és tecnologia que:

- Funciona sense sorpreses.
- Té anys de maduresa.
- Té bona documentació.
- Té comunitat gran.
- No és la més nova ni la més brillant.

Per al BernatLab, "boring tech" seria:

- **Debian** (no Arch, no NixOS).
- **Docker** (no Kubernetes, no Podman).
- **Docker Compose** (no Helm, no K8s manifests).
- **restic** (no fer la teva pròpia eina de còpies).
- **Prometheus + Grafana** (no construir el teu propi sistema de mètriques).
- **Tailscale** (no muntar la teva pròpia VPN).

Això redueix el temps de manteniment i la probabilitat de problemes.

## 51.4 El cicle operatiu

Un cop tens el sistema en producció, hi ha un cicle operatiu:

1. **Monitorar**: veure què passa.
2. **Alertar**: avisar quan alguna cosa va malament.
3. **Diagnosticar**: trobar la causa.
4. **Resoldre**: arreglar el problema.
5. **Documentar**: registrar què ha passat.
6. **Aprendre**: millorar per evitar que es repeteixi.

Això és un bucle continu. Com més madur és el sistema, més ràpid és el cicle.

## 51.5 Què cal monitorar

Al BernatLab, monitorem:

- **Disponibilitat**: serveis funcionant o caiguts.
- **Rendiment**: CPU, RAM, disc, xarxa.
- **Salut del sistema**: temperatura, errors de disc, etc.
- **Tràfic de xarxa**: ample de banda utilitzat.
- **Certificats**: quan caduquen.
- **Còpies**: quan es fan i quan fallen.
- **Logs de seguretat**: intents d'intrusió.
- **Dades específiques**: lectures de sensors, etc.

## 51.6 Cicles d'actualització

Defineix una cadència:

- **Diàriament**: comprovar alertes.
- **Setmanalment**: revisar logs, actualitzar sistema.
- **Mensualment**: auditar seguretat, fer neteja.
- **Trimestralment**: revisar configuració, planificar canvis.
- **Anualment**: revisar el DRP, planificar hardware.

Si no tens cadència, les coses es degraden. Els discos s'omplen, els registres es caducen, les actualitzacions s'acumulen.

## 51.7 El concepte d'"on-call"

En empreses, hi ha un equip d'**on-call** (guàrdia) que respon a incidents 24/7. En un homelab, **tu ets l'on-call**. Però pots ser-ho de manera sostenible:

1. **Defineix horaris**: no vols rebre alertes a les 3 de la matinada tots els dies.
2. **Diferencia per severitat**: alertes crítiques (24/7) i no crítiques (horari laboral).
3. **Automatitza el que puguis**: les alertes que no necessiten acció humana s'han de resoldre soles.
4. **Tingues un pla B**: si no pots respondre, qui més pot?

## 51.8 Mantenibilitat

Un sistema mantenible és:

- **Documentat**: cada component té una descripció.
- **Reproduïble**: pots muntar-lo de zero amb les instruccions.
- **Modular**: cada component es pot canviar sense trencar la resta.
- **Testejat**: tens proves que validen que funciona.

Per al BernatLab, això es tradueix en:

- Un **README complet** amb totes les passes d'instal·lació.
- Un **docker-compose.yml** que defineix tots els serveis.
- **Scripts d'instal·lació** idempotents (es poden executar múltiples cops).
- **Tests** que validen els components crítics.

## 51.9 El temps com a factor

Un dels factors que la gent no considera és el **temps**. Cada decisió tècnica té un cost de temps:

- Triar Kubernetes: 100+ hores d'aprenentatge.
- Triar Docker Compose: 5-10 hores d'aprenentatge.
- Triar una eina de mètriques nova: 20-50 h.
- Aprendre una nova tecnologia: variable.

Quan planegis, pregunta't: **val la pena el temps invertit?** Si tens 10 hores, és millor:

- 5 hores a configurar alerting → beneficis immediats.
- 5 hores a provar una tecnologia nova → beneficis dubtosos.

## 51.10 El factor "embarrassment-driven development"

A vegades, la millor motivació per fer les coses bé és **la vergonya**:

- Tens una gràfica de pèrdua de dades? No voldràs ensenyar-la.
- Tens una web que es cau cada 2 dies? No la voldràs compartir.
- Tens un sistema que triga 3 dies a recuperar? No voldràs explicar-ho.

Fes servir la vergonya constructiva. Documenta les coses que **no** vols que es repeteixin.

## 51.11 Filosofia del "menys és més"

Al BernatLab, **menys serveis** vol dir:

- Menys coses que poden fallar.
- Menys temps de manteniment.
- Menys dependències.
- Menys complexitat.

Cada nou servei ha de **justificar el seu cost de temps**. Si no t'aporta valor clar, no l'afegeixis.

## 51.12 Cultura de la documentació

Un bon sistema operatiu té bona documentació. La documentació:

- **Permet que qualsevol** (inclòs tu del futur) entengui el sistema.
- **Redueix errors** en canvis.
- **Facilita la recuperació** quan falla.
- **Comunica coneixement** a altres persones (família, amics).

Al BernatLab, documenta:

- L'arquitectura (README).
- Els procediments operatius (DRP, runbooks).
- Els canvis (CHANGELOG).
- Les decisions (ADR - Architecture Decision Records, registres de decisions arquitectòniques).

## 51.13 Indicadors que vas bé

Senyals que el sistema és madur:

- **Pocs incidents** al mes.
- **Recuperació ràpida** quan passa alguna cosa.
- **Actualitzacions regulars** sense trencar res.
- **Mètriques bones** (latència baixa, disponibilitat alta).
- **Documentació actualitzada**.

Si tot això es compleix, el sistema està sa.

## 51.14 Quan replantejar-se

De vegades, cal fer canvis radicals:

- El sistema creix massa per la Raspberry.
- Una tecnologia queda obsoleta.
- Les necessitats canvien (per exemple, l'hort creix i cal més capacitat).
- Apareix una millor alternativa.

Replantejar-se cada 2-3 anys és sa. No tinguis por de migrar si la nova opció és clarament millor.

## 51.15 Resum

L'operativa 24/7 és una mentalitat, no un producte. Boring tech, cicles regulars, observabilitat, mantenibilitat, documentació. Al proper capítol veurem el monitoratge avançat amb Grafana i Prometheus.

## 51.16 Exercicis pràctics

1. Defineix el teu SLA personal.
2. Inventaria tots els serveis i classifica'ls per criticitat.
3. Defineix els cicles d'actualització (diari, setmanal, mensual).
4. Crea una checklist de manteniment setmanal.
5. Documenta l'arquitectura actual al README.
6. Escriu el primer ADR (per què has triat Docker, per exemple).
7. Comença un CHANGELOG.md.

# Capítol 1 — Què és BernatLab

> *"Si vols entendre un sistema, construeix-lo tu mateix. Si el vols mantenir, documenta'l."*

## 1.1 Què és un homelab

Un **homelab** és un servidor — o un petit conjunt de servidors — que un particular munta a casa seva per aprendre, experimentar i allotjar els seus propis serveis. No és una empresa de hosting. No és un núvol professional. És el teu laboratori personal, la teva escola i, sovint, la teva joguina preferida.

La paraula **home** ja diu molt: el servidor viu a casa teva, normalment connectat al teu router domèstic, darrere d'una IP dinàmica i d'un tallafoc que no controles. La paraula **lab** diu la resta: és un entament d'experimentació, no de producció. Aquí es pot trencar coses. Aquí es poden provar tecnologies noves. Aquí s'equivoca un mateix i s'aprèn d'això.

Un homelab no és cap novetat. Fa dècades que enginyers i administradors de sistemes en tenen: torres amb discs durs, màquines velles reciclades, plaques base en calaixos. El que ha canviat en els últims anys és que avui pots muntar un homelab seriós, capaç de fer feines reals, amb una Raspberry Pi de 50 € i una targeta microSD de 16 €. I el que també ha canviat és el programari: contenidors Docker, serveis autoallotjats, xarxes privades com Tailscale, eines de monitorització com Uptime Kuma, panells com Homepage. Tot plegat, un ecosistema ric que abans era patrimoni de les empreses.

## 1.2 Per què construir un servidor propi

Hi ha moltes raons per tenir un homelab, i la majoria d'elles tenen poc a veure amb estalviar diners — probablement pagaries menys per un VPS de 3 € al mes. La raó de fons és **aprenentatge i control**.

Quan algú decideix muntar un homelab, el que busca és:

- **Aprendre de veritat**. Llegir sobre Docker no és entendre Docker. Posar-lo en marxa, trencar-lo, refer-lo, llegir els logs a les dues de la matinada, descobrir per què un contenidor no es connecta a una xarxa — això és aprendre.
- **Tenir control sobre les dades**. Quan puges una foto a un núvol, algú altre decideix què se'n fa, durant quant de temps es guarda i qui hi té accés. Quan les dades viuen a la teva Raspberry, la decisió és teva.
- **Experimentar amb projectes reals**. Sensors, automatitzacions, webs personals, bases de dades, petits models d'intel·ligència artificial. Tot plegat, en una sola caixa que cabria en un calaix.
- **Reduir la dependència tecnològica**. Si un dia vols deixar d'utilitzar un servei comercial, tenir la infraestructura a casa et permet fer-ho gradualment.
- **Divertir-se**. Muntar un homelab i mantenir-lo sa és una afició com pot ser-ho la moto, la cuina o la programació. Té un component pràctic, però sobretot un component de plaer personal.

I, francament, hi ha una darrera raó menys noble però igualment vàlida: la **curiositat**. Saber què passa quan un contenidor no arrenca, entendre per què una VPN et permet entrar al teu servidor des de qualsevol lloc del món, descobrir que un missatge de Telegram pot fer arrencar un motor a 245 metres de casa teva. Això, avui, és a l'abast de qualsevol amb una Raspberry Pi i ganes de furgar.

## 1.3 Què volem aconseguir amb el BernatLab

El BernatLab no és un projecte abstracte. Té objectius molt concrets:

1. **Centralitzar serveis**. En lloc de tenir una Raspberry per als sensors, un servidor vell per a la web, un portàtil per fer proves, tenir una sola màquina que ho aculli tot — o que, com a mínim, en sigui el centre de control.
2. **Donar suport al projecte Hort Osona**. Una aplicació web pública allotjada a GitHub Pages, una API futura allotjada al BernatLab, sensors al terreny que enviaran dades per MQTT, una base de dades InfluxDB, gràfiques amb Grafana.
3. **Servir com a entorn d'aprenentatge continu**. Vull aprendre Docker a fons, entendre xarxes, provar Node-RED, experimentar amb Telegram bots, muntar un assistent IA local amb Ollama. Tot plegat, en un entorn segur i controlat.
4. **Servir com a centre de projectes personals**. Música, fotografia, desenvolupament web, scripts d'automatització, còpies de seguretat. Tot ha de tenir cabuda.
5. **Ser resilient dins les seves limitacions**. Una Raspberry Pi 4 amb 4 GB de RAM no és un servidor de producció. No ha de ser-ho. Ha de ser estable, documentat, fàcil de recuperar i honest amb els seus límits.

El que **no** volem:

- Un servidor que depengui de trucs opacs que ningú entén.
- Un sistema ple de comandes copiades de StackOverflow que ningú sap per què funcionen.
- Un punt únic de fallada que, quan es trenqui, ens deixi sense res.
- Una despesa energètica o econòmica desproporcionada.

## 1.4 Arquitectura general del BernatLab

A grans trets, el BernatLab té tres capes:

```
┌───────────────────────────────────────────────────────────────┐
│                          EXTERIOR                             │
│                                                               │
│  Internet ── Tailscale ── 100.115.134.76 ── hortosona        │
│                                                               │
└───────────────────────────────────────────────────────────────┘
                               │
┌───────────────────────────────────────────────────────────────┐
│                       SISTEMA OPERATIU                        │
│                                                               │
│   Debian 13 Lite · arm64 · kernel Linux · systemd             │
│   Usuari bernat · SSH · tallafoc UFW opcional                │
│                                                               │
└───────────────────────────────────────────────────────────────┘
                               │
┌───────────────────────────────────────────────────────────────┐
│                  PLATAFORMA DE CONTENIDORS                    │
│                                                               │
│   Docker Engine                                              │
│   └── Docker Compose (fitxers a /home/bernat/homelab)         │
│       ├── Portainer     (gestió web)                          │
│       ├── Uptime Kuma   (monitorització)                      │
│       ├── Homepage      (panell d'entrada)                    │
│       ├── [pròxims: File Browser, Node-RED, Mosquitto, ...]   │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

Aquesta divisió en tres capes és pedagògica i pràctica alhora. Entenent-les per separat, podem raonar sobre què falla quan alguna cosa falla.

### La capa exterior

És el que es veu des de fora. La Raspberry Pi té una IP a la teva xarxa local (normalment `192.168.x.y`), una IP pública dinàmica que el teu operador assigna al router, i una IP Tailscale (`100.115.134.76` en el nostre cas) que és fixa mentre duri la teva subscripció i que ens permet accedir-hi des de qualsevol lloc del món sense tocar el router.

La idea clau és aquesta: **mai no exposem directament la Raspberry a Internet**. Tots els accessos remots passen per Tailscale, que crea una xarxa privada virtual entre els teus dispositius. El router de casa no sap que existeix la Raspberry com a servidor — sap que és un dispositiu més de la xarxa local.

### La capa de sistema operatiu

Debian 13 Lite és la base. La versió Lite no porta entorn gràfic, ni servidor d'impressió, ni mil programes innecessaris. Porta just el que un servidor necessita: el kernel, les utilitats bàsiques, el gestor de paquets `apt`, el dimoni `systemd` que arrenca els serveis, i poc més. Això és bo perquè redueix la superfície d'atac i el consum de RAM.

Aquí és on vivim nosaltres com a administradors: editem fitxers, instal·lem programes, configurem serveis de sistema, gestionem usuaris, mirem logs.

### La capa de contenidors

Per sobre del sistema operatiu, Docker. Docker ens permet instal·lar serveis complexos — com Portainer, Uptime Kuma, Homepage, Grafana — sense contaminar el sistema base. Cada servei viu en un **contenidor**: un entorn aïllat que conté el seu propi sistema de fitxers, la seva pròpia xarxa i el seu propi cicle de vida. Si un contenidor es trenca, l'esborres, el tornes a crear, i tot segueix igual. Si vols actualitzar un servei, fas una ordre i Docker es descarrega la nova versió, atura l'antic i engega el nou.

La capa de contenidors es gestiona amb **Docker Compose**, que és un fitxer `yaml` on descrius tots els teus serveis, les seves configuracions, els volums, les xarxes i els ports. En lloc de recordar vint ordres llargues, tens un sol fitxer que documenta tot el sistema. A `/home/bernat/homelab/docker-compose.yml` hi haurà la definició de tot el BernatLab.

## 1.5 Serveis que ja tenim en marxa

A dia d'avui, el BernatLab té tres serveis principals desplegats amb Docker Compose:

### Portainer (`https://100.115.134.76:9443`)

Portainer és una interfície web que ens permet veure i gestionar tots els contenidors Docker de la Raspberry sense haver de tocar la línia d'ordres. És com un panell de control per al Docker. Porta un any, dos, sent l'eina estàndard per a homelabs i petites empreses.

Hi accedim per HTTPS, tot i que el certificat és autosignat (ens saltarà l'avís del navegador la primera vegada, cosa perfectament normal en un entorn personal). Un cop dins, podem veure contenidors actius, aturar-los, reiniciar-los, veure els logs en directe, explorar volums, veure imatges, gestionar xarxes. També permet crear piles (stacks) de Docker Compose directament des del navegador, cosa que pot ser útil però que, per a aquest manual, farem sempre des de la línia d'ordres per entendre què passa.

### Uptime Kuma (`http://100.115.134.76:3001`)

Uptime Kuma és una eina de monitorització. La seva feina és senzilla: comprovar periòdicament que els nostres serveis estan vius i avisar-nos quan no ho estan. Pot fer pings a màquines, peticions HTTP a webs, comprovacions de ports TCP, comprovacions de certificats SSL, i un llarg etcètera.

En el BernatLab, Uptime Kuma vigila, com a mínim:

- La pròpia Raspberry Pi (ping).
- Portainer (HTTP).
- El mateix Uptime Kuma (meta-monitorització).
- La web pública Hort Osona (HTTP a `bernatmora.github.io`).

Quan algun d'aquests serveis falla, Uptime Kuma pot enviar una alerta per correu, Telegram, Discord, Slack, webhook, o qualsevol combinació imaginable. En aquest manual veurem com configurar-lo per avisar-nos per Telegram.

### Homepage (`http://100.115.134.76:3000`)

Homepage és el **panell d'entrada** al BernatLab. Una pàgina web molt neta, feta per un projecte de codi obert, que ens mostra una graella de targetes: cadascuna és un enllaç directe als nostres serveis. L'objectiu és que quan obrim el navegador i posem `100.115.134.76:3000`, veiem d'un cop d'ull tot el que tenim, si està funcionant, i hi puguem entrar amb un sol clic.

Homepage és personalitzable: podem posar un fons, podem agrupar serveis per categories (Monitorització, Gestió, Dades, Experimentals, etc.), podem afegir widgets que mostren estadístiques en directe (ús de CPU, RAM, temperatura, etc.). És la porta d'entrada i la targeta de presentació del BernatLab.

## 1.6 Filosofia del projecte

El BernatLab es regeix per cinc principis. No són normes escrites en marbre, però ajuden a prendre decisions quan hi ha dubtes.

### Primer principi: entendre abans de copiar

Quan trobem una ordre a Internet, abans d'executar-la a cegues, l'hem d'entendre. Què fa? Per què funciona? Què canviaria si la meva màquina fos diferent? Si no podem respondre aquestes preguntes, millor preguntar, provar en un entorn segur o esperar. Un homelab és, sobretot, una escola.

### Segon principi: documentar sempre

Si hem après alguna cosa, l'escrivim. Si hem trobat un error, l'escrivim. Si hem canviat una configuració, l'escrivim. El futur jo del Bernat agrairà el present jo del Bernat cada vegada que obri un fitxer i hi trobi el context que necessita.

### Tercer principi: senzillesa per defecte

Si hi ha dues maneres de fer una cosa, escollim la més senzilla. Un sol contenidor és millor que dos. Un fitxer de configuració és millor que tres. Una eina bona és millor que tres eines mitjanes. La complexitat és la principal font d'errors en un homelab.

### Quart principi: còpies de seguretat com a rutina

Un homelab sense còpies de seguretat és una bomba de rellotgeria. Les targetes microSD fallen. Els discs durs fallen. Les actualitzacions fallen. Si no podem restaurar el sistema en una hora, no estem preparats. Per això, en el Capítol 9, dedicarem temps a còpies de seguretat de la carpeta `/home/bernat/homelab` i de les bases de dades.

### Cinquè principi: mesurar abans d'optimitzar

No afegim RAM perquè sí. No comprem un disc SSD perquè ens sembla. No movem serveis a una màquina més potent per intuïció. Primer mesurem — Uptime Kuma, `htop`, `docker stats`, logs — i després decidim.

## 1.7 Com s'administra un homelab: el dia a dia

Un homelab no és un projecte que es fa un cop i s'oblida. És un sistema viu que canvia, creix i, de tant en tant, es trenca. La vida d'un administrador de homelab es compon de tasques quotidianes que, amb el temps, esdevenen rutines:

- **Matí**: comprovar Uptime Kuma, mirar si hi ha alertes.
- **Setmanal**: actualitzar contenidors, llegir notes de versió, fer còpia de seguretat.
- **Quan toca**: afegir un servei nou, configurar un sensor nou, muntar una base de dades.
- **Quan es trenca**: mirar logs, buscar l'error, arreglar-lo, documentar-lo.

Aquest manual està pensat per donar-te les eines per fer tot això amb confiança. No per tenir un servidor bonic, sinó per tenir un servidor **entès**.

## 1.8 Resum

En aquest primer capítol hem après què és un homelab, per què val la pena tenir-ne un, quins objectius concrets té el BernatLab, com s'estructura en tres capes (xarxa, sistema operatiu, contenidors) i quins serveis hi ha desplegats. També hem establert cinc principis que ens guiaran: entendre, documentar, simplificar, copiar i mesurar. En el proper capítol baixarem al metall: la Raspberry Pi 4, peça a peça.

## 1.9 Exercicis pràctics

1. **Obre el panell d'Homepage** (`http://100.115.134.76:3000`) i mira què hi ha. Anota tres serveis que vulguis afegir.
2. **Obre Portainer** (`https://100.115.134.76:9443`) i compta quants contenidors estan `running`. Apunta'ls tots en un paper.
3. **Obre Uptime Kuma** (`http://100.115.134.76:3001`) i mira l'estat dels monitors. N'hi ha cap de caigut? Si sí, investiga per què.
4. **Connecta't per SSH** a la Raspberry i executa `hostname`, `uptime` i `whoami`. Apunta el resultat. Això ja és administració de veritat.

Comandes útils d'aquest capítol:
```bash
ssh bernat@100.115.134.76
hostname
uptime
whoami
```

Paraules clau per recordar: **homelab, autosuficiència, contenidors, documentació, mesurar, simplificar**.

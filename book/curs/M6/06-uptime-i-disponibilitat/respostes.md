# Respostes - Capitol 6: Uptime i disponibilitat

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es un SLA

**Resposta correcta**: Un acord sobre la disponibilitat d'un servei.

**Explicacio**: SLA (Service Level Agreement) es un contracte (formal o informal) entre qui ofereix un servei i qui el consumeix. Defineix coses com el uptime garantit, el temps maxim de resposta en cas d'incidencia, i les compensacions si no es compleix. Per un servidor casola, el SLA te l'auto-imposat: "vull que estigui disponible el 99% del temps" o el que sigui.

---

## Pregunta 2: SLA 99.9%

**Resposta correcta**: 8.76 hores d'inactivitat per any.

**Explicacio**: 99.9% son 3 "nines" i equival a 8.76 hores d'inactivitat per any (o 43.83 minuts al mes, o 1.44 minuts al dia). Es un objectiu raonable per un servidor casola. 99.99% ("four nines") son 52 minuts l'any, que es molt agosarat per una RPi.

---

## Pregunta 3: Per que cal monitor extern

**Resposta correcta**: Perque el monitor intern cau amb el sistema i no detecta fallades de xarxa.

**Explicacio**: Si tens Prometheus a la mateixa RPi, quan la RPi es penja, Prometheus tambe. Tu no reps cap alerta perque el sistema que havia d'avisar tambe esta caigut. I si nomes monitors des de dins, no saps si la RPi es accessible des de fora. Es com tenir un detector de fum que nomes funciona si hi ha llum.

---

## Pregunta 4: Eina de monitoratge

**Resposta correcta**: Uptime Kuma.

**Explicacio**: Uptime Kuma es una eina open source creada per Louis (louislam) que ha esdevingut molt popular. Es una alternativa auto-allotjada a UptimeRobot i Pingdom. Te una UI molt bonica, soporta molts tipus de probes, i es molt facil d'instal·lar.

---

## Pregunta 5: Port per defecte

**Resposta correcta**: 3001.

**Explicacio**: Uptime Kuma escolta al port 3001 per defecte perque Grafana ja te el 3000. Es una bona practica escollir ports que no col·lisionin. Si necessites accedir des de fora, recorda obrir el port al router o fer servir un proxy.

---

## Pregunta 6: Status page publica

**Resposta correcta**: Una pagina web que mostra l'estat dels teus serveis en temps real.

**Explicacio**: Una status page es com les que veus a empreses grans (status.github.com, status.cloudflare.com, etc.): una pagina que mostra si tots els serveis funcionen, l'historic d'incidencies, i el temps de resposta. Uptime Kuma et permet tenir la teva propia.

---

## Pregunta 7: Probe per port 22

**Resposta correcta**: TCP.

**Explicacio**: El port 22 (SSH) no parla HTTP sino el protocol SSH. La unica manera de comprovar que esta obert es fent una connexio TCP al port. Uptime Kuma te la probe "Port" o "TCP" que simplement obre una connexio i la tanca. Si el port esta obert, esta UP; si esta tancat, esta DOWN.

---

## Pregunta 8: Servei cloud gratuit

**Resposta correcta**: UptimeRobot.

**Explicacio**: UptimeRobot te un free tier amb 50 monitors i comprovacio cada 5 min. Es molt usat per servidors petits. Altres opcions: Cronitor (tambe te free tier), Healthchecks.io (especialitzat en cron jobs), Hetrixtools (free tier limitat).

---

## Pregunta 9 (oberta): Limitacio del monitor intern

**Resposta model**:

Un monitor nomes INTERN te limitacions greus que el fan insufficient per a operativa 24/7:

**Limitacio 1 - El monitor cau amb el sistema**: si tens Uptime Kuma o Prometheus a la mateixa RPi, quan la RPi es penja, el monitor tambe. Aleshores no reps cap alerta perque el sistema que havia d'avisar tambe esta caigut. Es com tenir un detector de fum que nomes funciona quan no hi ha foc.

**Limitacio 2 - No detecta fallades de xarxa**: des de dins de la xarxa, la RPi pot estar "be" pero no accesible des de fora. Si el router es reinicia, si la IP publica canvia, si el DNS no apunta correctament, la RPi funciona pero ningu pot accedir-hi. Un monitor intern nomes veu que la xarxa local va be.

**Limitacio 3 - No veu la perspectiva de l'usuari**: el que importa es si l'USUARI pot accedir al servei, no si el servei esta corrent. Si la RPi esta be pero el port 8123 (Home Assistant) esta tancat al firewall, l'usuari no pot entrar. Un monitor extern simula el que veu un usuari real.

**Exemple concret del BernatLab**: tens la RPi a casa amb Home Assistant, Grafana i els teus altres serveis. Tot funciona perfectament. Un dia, el router de la companyia es reinicia per una actualitzacio. La RPi torna a arrencar correctament, Prometheus es reinicia, Grafana es reinicia... tot funciona. Pero el router, quan torna, agafa una IP publica nova. La teva DDNS no s'actualitza rapid, i durant 30 minuts el teu domini bernatlab.example.com apunta a la IP antiga. Durant aquests 30 minuts:
- Des de dins, tot funciona perfectament. Prometheus, Grafana, Uptime Kuma intern: tot "UP".
- Des de fora, ningu pot accedir a res. El teu mobil, la teva parella, tot dona error de connexio.
- Si nomes tens monitor intern, NO T'ASSABENTES de res. Per tu tot va be fins que algú et truca dient "no puc entrar a res".

Un monitor extern, en canvi, cada 5 minuts intenta accedir a `https://bernatlab.example.com:8123`. Veu que falla, t'avisa per Telegram amb "Home Assistant no accesible des de fora" i tu pots actuar: accedir al router, actualitzar la DDNS manualment, o reiniciar el servei de DDNS.

Aixo es el valor afegit del monitor extern: la **perspectiva de l'usuari final**. I per definicio, nomes pot veure aixo un sistema que esta FORA de la teva xarxa.

---

## Pregunta 10 (oberta): Monitors del BernatLab

**Resposta model**:

Aqui tens els 8-10 monitors que configuraria al BernatLab:

**1. Router (Ping)**
- Tipus: Ping
- Hostname: `192.168.1.1`
- Heartbeat: 30s
- Severitat: critica
- Per que: si el router cau, tota la xarxa cau. Es la porta d'entrada.

**2. DNS extern (DNS)**
- Tipus: DNS
- Hostname: `google.com`
- Heartbeat: 60s
- Severitat: warning
- Per que: si el DNS no funciona, ningu pot navegar. Detecta problemes de DNS.

**3. Internet (HTTP)**
- Tipus: HTTP(s)
- URL: `https://www.google.com`
- Heartbeat: 60s
- Severitat: warning
- Per que: confirma que la conexio a internet funciona.

**4. DDNS (HTTP amb keyword)**
- Tipus: HTTP(s)
- URL: `http://bernatlab.example.com:8123`
- Heartbeat: 60s
- Severitat: critica
- Per que: valida que la DDNS apunta correctament i el servei es accessible des de fora.

**5. Home Assistant (HTTP amb keyword)**
- Tipus: HTTP(s)
- URL: `http://192.168.1.50:8123`
- Accepts keyword: "Home Assistant"
- Heartbeat: 60s
- Severitat: critica
- Per que: HA es el cervell de la llar automatitzada. Si cau, tot falla.

**6. Grafana (HTTP)**
- Tipus: HTTP(s)
- URL: `http://192.168.1.50:3000`
- Heartbeat: 60s
- Severitat: warning
- Per que: si Grafana esta caigut, no tens visibilitat. No es critic pero si molest.

**7. Prometheus (HTTP)**
- Tipus: HTTP(s)
- URL: `http://192.168.1.50:9090`
- Heartbeat: 60s
- Severitat: warning
- Per que: si Prometheus cau, Grafana no te dades. Caldra investigar.

**8. SSH (TCP)**
- Tipus: Port
- Port: 22
- Hostname: `192.168.1.50`
- Heartbeat: 60s
- Severitat: warning
- Per que: si SSH no va, no pots accedir per gestionar res. Pero la RPi pot estar be igualment.

**9. API externa (HTTP amb JSON)**
- Tipus: HTTP(s) amb JSON
- URL: `https://api.openweathermap.org/data/2.5/weather?q=Barcelona&appid=XXX`
- Heartbeat: 300s (cada 5 min)
- Severitat: info
- Per que: serveix per monitorar serveis de tercers que fas servir. Si la API de meteo cau, el teu HA deixa de tenir dades.

**10. Backup push (Push)**
- Tipus: Push
- URL: la que et doni Uptime Kuma
- Heartbeat: 86400 (24h)
- Severitat: critica
- Per que: si el backup automatic no ha enviat senyal en 24h, vol dir que ha fallat. Et permet validar que els backups es fan realment.

Tots aquests monitors amb **alertes a Telegram** quan canvien d'estat (de UP a DOWN o de DOWN a UP). Les "warning" amb menys urgencia, les "critica" amb missatge inmediat.

Bonus: a mes, configuraria **UptimeRobot gratuit** (cloud, realment extern) amb 1-2 monitors basics com a segon ull. Si la RPi cau del tot, Uptime Kuma tambe, pero UptimeRobot es independent i t'avisara.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici desde zero observant cada pas.
- **0-2 encerts**: Repassem junts el capitol abans de continuar.

## Que fer si has encertat totes

- Passa al **Capitol 7** (Actualitzacio segura).
- Configura UptimeRobot (cloud) com a monitor REALMENT extern.
- Investiga la integracio amb Tailscale per tenir una VPN.

# Respostes - Capitol 1: Amenaces comunes al servidor

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es la superficie datac?

**Resposta correcta**: El conjunt de punts per on un atacant podria entrar.

**Explicacio**: Es una metrica que quantifica l'exposicio. Mes superficie = mes risc. L'objectiu es minimitzar-la: tancar ports innecessaris, limitar serveis exposats, etc.

---

## Pregunta 2: Perill numero 1

**Resposta correcta**: Els atacs de bruteforce a SSH.

**Explicacio**: Es l'atac mes frequent i mes automatic. Els bots escanegen constantment el port 22 i proven milers de contrasenyes. Si tens contrasenya feble, tard o d'hora entraren.

---

## Pregunta 3: Que es bruteforce?

**Resposta correcta**: Provar milers de combinacions d'usuari i contrasenya.

**Explicacio**: Un atac automatitzat on es proven totes les combinacions possibles fins encertar. Amb eines modernes, milers de intents per segon. Una contrasenya de 8 caracters triga segons a trencar-se.

---

## Pregunta 4: Usuaris mes atacats

**Resposta correcta**: root, pi, admin.

**Explicacio**: Són els noms per defecte que els bots coneixen. Si tens un usuari personal (ex. "bernat"), sera menys atacat. Si tens "pi" o "root", sera el primer que provaran.

---

## Pregunta 5: Que fa un port scan?

**Resposta correcta**: Mira quins serveis escolten a quins ports.

**Explicacio**: nmap es l'eina estandard. Fa peticions a cada port i mira quins responen. Mostra servei, versio, i a vegades el sistema operatiu.

---

## Pregunta 6: Servei mes critic

**Resposta correcta**: SSH.

**Explicacio**: Perque dona acces a la consola amb permisos de superusuari. Un atacant que entra per SSH pot fer tot el que tu pots fer.

---

## Pregunta 7: Que es credential stuffing?

**Resposta correcta**: Usar combinacions que han fugit d'altres incidents.

**Explicacio**: Si un atacant te una llista d'emails+contrasenyes d'un breach (LinkedIn, Adobe, etc.), els prova tots als serveis que troba. Molta gent reutilitza contrasenyes, per la qual cosa funciona sovint.

---

## Pregunta 8 (oberta): Superficie datac i minimitzacio

**Resposta model**:

La superficie d'atac es el **conjunt de punts vulnerables** d'un sistema. Es com un castell: cada porta, cada finestra, cada esquerda es un possible punt d'entrada. Minimitzar-la es **reduir el nombre d'entrades possibles**.

Al BernatLab la superficie d'atac inclou:
- **Port 22 obert**: SSH es la porta principal.
- **Port 80/443**: HTTP/HTTPS si hi ha un servidor web.
- **Serveis Docker exposats**: Portainer, Gitea, Home Assistant, etc.
- **Tailscale ACLs**: si son massa permissives, qualsevol dispositiu autenticat pot accedir a tot.
- **Subdominis DNS**: si tens un domini, els bots el troben rapid.

Per minimitzar:
- **SSH nomes a Tailscale**: el port 22 nomes escolta a la IP de Tailscale, no a Internet.
- **Serveis en localhost**: Grafana, InfluxDB, etc. nomes a 127.0.0.1.
- **Tancar el que no es fa servir**: si no uses Portainer, no l'instal·lis o desactiva'l.
- **UFW deny-by-default**: nomes obrim els ports estrictament necessaris.
- **Reverse proxy amb TLS**: si cal exposar algun servei, passa per Nginx/Caddy amb TLS.

**Principi basic**: cada servei exposat es un risc. Si no es absolutament necessari exposar-lo, no ho facis. La pregunta correcta no es "puc exposar-ho?" sino "necessito exposar-ho?".

**Exemple concret**: una Raspberry Pi amb un servidor web personal i Home Assistant. Si nomes ho usas tu des de casa, tot a Tailscale. Si vols mostrar l'hort a un amic, nomes exposar el frontend public, mai la base de dades ni el sistema intern.

---

## Pregunta 9 (oberta): Bots que escanegen Internet

**Resposta model**:

Hi ha bots que escanegen totes les IPs d'Internet per varies raons:

**1. Recerca academic / Shodan / Censys**. Organitzacions que mesuren la salut d'Internet. Escanegen per fer estadistiques: quantes maquines corren tal versio de tal servei, quantes tenen ports oberts, etc. Publicar aquestes dades ajuda a conscienciar sobre la seguretat.

**2. Bots criminals**. Busquen maquines vulnerables per:
- Instal·lar miners de criptomonedes (usen la teva CPU per generar diners).
- Crear botnets (usen la teva maquina per atacar altres).
- Robar dades (si hi ha una base de dades accessible).
- Extorsio (ransomware que xifra els teus fitxers).

**3. Competencia deslleial**. Empreses que contracten "research" per trobar vulnerabilitats en sistemes semblants als seus competidors.

**4. Estudiants i "script kiddies"**. Persones amb pocs coneixements que fan servir eines automatiques (nmap, Hydra, Metasploit) per "experimentar". Son els mes nombrosos pero tambe els menys sofisticats.

**Que fan quan troben una maquina vulnerable**:
- Si es SSH: bruteforce amb llistes de contrasenyes comunes.
- Si es HTTP: exploren directoris, busquen panells d'administracio, proven SQL injection.
- Si es una versio vulnerable: exploten l'exploit especific (EternalBlue, Shellshock, etc.).
- Si troben una base de dades accessible: descarreguen tot el que poden.

**Quant de triguen**: un bot pot escanejar totes les IPs d'Internet en qüestio de dies o setmanes. Això vol dir que **si poses una maquina a Internet sense proteccio, sera trobada en menys d'una setmana**. No es paranoia: es la realitat.

---

## Pregunta 10 (oberta): Flux dun atac reeixit

**Resposta model**:

Segueixo el flux d'un atac amb exit a una RPi amb port 22 obert i contrasenya "raspberry" per a l'usuari pi:

**Pas 1 - Descobriment**. Un bot fa un escaneig massiu d'IPs. Troba que la IP X.X.X.X te el port 22 obert. Temps: 1-2 segons per IP.

**Pas 2 - Identificacio del servei**. El bot fa `nmap -sV X.X.X.X` i veu: "OpenSSH 9.2p1 Debian". Sap que es un Linux amb SSH recent. Temps: 5 segons.

**Pas 3 - Bruteforce**. El bot conecta amb SSH i prova combinacions de la llista "rockyou.txt" (14 milions de contrasenyes). Per a cada combinacio, triga ~0.5 segons. Temps total: varies hores, pero nomes es una maquina entre milions.

**Pas 4 - Exit**. Troba la contrasenya "raspberry" per a l'usuari "pi". Aixo passa perque "pi" + "raspberry" es la combinacio per defecte de Raspberry Pi OS. Temps: 1-2 hores.

**Pas 5 - Acces inicial**. El bot entra al sistema. Comprova els privilegis: `sudo -l` mostra que l'usuari "pi" pot fer tot sense contrasenya (configuracio per defecte). 

**Pas 6 - Escalada de privilegis**. El bot ja te root. Pot:
- Llegir `/etc/shadow` (hashes de contrasenyes).
- Instal·lar un miner de criptomonedes (xmrig, etc.).
- Modificar el sistema per persistir (afegir a `~/.bashrc`, crear un cron, etc.).
- Obrir un reverse shell per accedir des de fora.

**Pas 7 - Persistencia i expansio**. El bot:
- Crea un usuari nou amb acces root.
- Desactiva fail2ban o el firewall.
- Escaneja la xarxa local per trobar altres maquines.
- Si troba la xarxa Tailscale, intenta atacar altres maquines.

**Pas 8 - Atac a tercers**. La RPi es ara part d'un botnet. Pot:
- Fer atacs DDoS a altres servidors.
- Enviar correu brossa.
- Minar criptomonedes.
- Exfiltrar dades personals.

**Tot aquest proces pot passar en menys de 24 hores** des de que la maquina esta a Internet. Si la contrasenya es robusta, l'atac falla. Pero si es feble o no hi ha fail2ban, l'atac te exit.

**Lliço**: la combinacio "port obert + contrasenya feble + sense fail2ban" es la recepta per desastre. Tots tres elements son necesaris pero cap es suficient per si sol. Cal **defense in depth**: multiples capes.

---

## Pregunta 11 (oberta): Tailscale i seguretat

**Resposta model**:

Tailscale es una **capa de seguretat** pero NO una panacea. No ens fa inmunes a tots els atacs.

**Que ens dona Tailscale**:
- **Xarxa privada**: el servidor no es visible a Internet public. Els bots no el poden trobar.
- **Xifratge**: tot el trafic entre dispositius Tailscale va xifrat amb WireGuard.
- **Autenticacio**: nomes dispositius autenticats al nostre tailnet poden accedir.
- **MagicDNS**: noms en lloc d'IPs, mes facil de gestionar.

**Que NO ens dona**:
- Si les ACLs son massa permissives, qualsevol dispositiu pot accedir a qualsevol port.
- Si una maquina Tailscale es compromete (roba el portatil, per exemple), l'atacant te acces a tot el tailnet.
- Tailscale no substitueix les bones practiques dins del sistema (contrasenyes, actualitzacions, etc.).
- Si hi ha una errada a Tailscale (rar pero possible), els beneficis desapareixen.

**Exemple de fallada**: tens una maquina de desenvolupament al tailnet amb contrasenya feble. Un membre de la familia entra accidentalment i instal·la un programa malicios. Ara aquest programa te acces a tots els serveis del tailnet perque les ACLs permeten comunicacio interna.

**Defense in depth**: Tailscale es la primera capa, pero calen mes capes:
- ACLs restrictives (cap dispositiu te acces a tot).
- Contrasenyes robustes a totes les maquines.
- 2FA al compte de Tailscale.
- SSH amb claus, no contrasenyes.
- Firewall ufw nomes permet el que cal.

**Conclusio**: Tailscale es una eina poderosa pero no es una bala magica. Es part d'una estrategia de seguretat, no tota la estrategia.

---

## Pregunta 12 (oberta): Tres tipus datac i defenses

**Resposta model**:

**Atac 1 - SSH bruteforce**:
- Com es manifesta: milers d'intents de login a `/var/log/auth.log` amb usuaris com "pi", "root", "admin".
- Perill: si la contrasenya es feble, l'atacant entra en hores o dies.
- **Millor defensa**: SSH nomes amb claus publiques (no contrasenyes). Amb claus de 256 bits (ed25519), l'atac es computacionalment inviable. A mes, fail2ban bloqueja les IPs que insisteixen.

**Atac 2 - Port scan / servei vulnerable**:
- Com es manifesta: peticions a molts ports des d'una mateixa IP, o consultes a serveis amb versions antigues.
- Perill: si tens una versio vulnerable (Heartbleed, Shellshock, EternalBlue), l'atacant pot entrar sense autenticacio.
- **Millor defensa**: tancar tots els ports que no son estrictament necessaris. Si nomes serves HTTP, obre el 80 i 443, no el 22 a Internet. Mantenir el sistema actualitzat.

**Atac 3 - Aplicacio web vulnerable (SQL injection, XSS)**:
- Com es manifesta: peticions HTTP malformades, intents d'injeccio a formularis.
- Perill: robo de dades, defacement, acces al sistema de fitxers.
- **Millor defensa**: mantenir el framework actualitzat, validar totes les entrades, usar ORM que escapen automaitcament, WAF (Web Application Firewall) si es vol anar mes enlla.

**Aplica al BernatLab**:
- Atac 1: ja cobert amb Tailscale + claus SSH.
- Atac 2: ufw nomes permet els ports estrictament necessaris.
- Atac 3: aplica a la web publica de l'hort si n'hi ha. Cal validar totes les entrades, no usar contrasenyes per defecte, mantenir el framework actualitzat.

---

## Pregunta 13 (oberta): Deteccio datacs

**Resposta model**:

Hi ha quatre senyals principals que indiquen que el servidor esta sent atacat:

**Seny al 1 - Intents de login fallits a SSH**:
```bash
sudo journalctl -u ssh | grep "Failed password"
```
Si veus mes de 100 intents per dia desde una sola IP, es un atac.

**Senyal 2 - CPU alta sense causa evident**:
- Un miner de criptomonedes pot consumir 100% de CPU.
- Comprovar amb `htop` o `top`.
- Si veus processos sospitosos (`xmrig`, `minerd`, etc.), es un senyal d'alerta.

**Senyal 3 - Trafic de xarxa anormal**:
- `iftop` o `nethogs` mostren qui esta fent trafic.
- Si una IP externa esta fent molt trafic al teu servidor, pot ser un atac o una exfiltracio de dades.

**Senyal 4 - Fitxers nous o modificats sense permis**:
- Eines com `aide` o `tripwire` monitoritzen canvis.
- Si trobes fitxers a `/tmp` o al home d'un usuari que no reconeixes, posible senyal de compromes.

**Eines de deteccio**:
- **fail2ban**: ja cobert, bloqueja IPs amb molts intents fallits.
- **portsentry**: detecta escanejos de ports i bloqueja la IP.
- **auditd**: registra acces a fitxers sensibles.
- **OSSEC / Wazuh**: sistemes complets de HIDS (Host-based Intrusion Detection System).
- **Logwatch / GoAccess**: resumeixen els logs diariament.

**Al BernatLab**: fail2ban + portsentry + auditd es la combinacio minima recomanable. S'instal·len amb `apt`, son gratuits, i configuren alertes.

**Limitacio important**: cap eina detecta tots els atacs. Un atac sofisticat pot evitar la deteccio durant setmanes o mesos. Per tant, **cal combinar eines amb revisio humana peri dica**.

---

## Pregunta 14 (oberta): Impacte dun atac reexit

**Resposta model**:

Un atac reeixit pot tenir consequencies molt mes enlla del servidor. Al BernatLab especificament:

**Impacte 1 - Perdua de dades personals**:
- Si el servidor te correus, documents, fotos, son accessibles.
- Aixo inclou informacio personal, possiblement de familia tambe.
- Pot ser usat per robo d'identitat o sextorsion (si hi ha fotos intimes).

**Impacte 2 - Control de l'hort**:
- Si tens un sistema de reg automatic, l'atacant pot:
  - Inundar el hort (reg continu).
  - Deixar les plantes sense aigua.
  - Modificar el pH o la fertilitzacio.
  - Espiar les lectures dels sensors.
- Pot afectar collites senceres.

**Impacte 3 - El servidor com a arma**:
- La teva RPi pot ser part d'un botnet.
- Pot atacar altres servidors (DDoS).
- Pot enviar correu brossa.
- Pot minar criptomonedes (increment de la factura electrica).

**Impacte 4 - Conseq uencies economiques**:
- Si tens serveis de pagament associats (Stripe, etc.), l'atacant pot fer compres.
- Si el servidor es a una empresa, la perdua de productivitat es gran.
- Cost de neteja i forensics.

**Impacte 5 - Reputacio**:
- Si el servidor s'usa per atacar tercers, la teva IP es llistada a llistes negres.
- Altres servidors et poden bloquejar.
- Si tens un domini propi, pot ser associat a spam.

**Impacte 6 - Implicacions legals**:
- A la UE, el GDPR obliga a notificar breaches de dades personals en 72 hores.
- Si el servidor gestiona dades d'altres persones, pots tenir responsabilitat legal.
- Si la teva maquina es fa servir per atacar tercers, et poden demandar.

**Cas real**: un homelab compromet pot passar dies o setmanes sense que ho saps. L'atacant pot estar extraient dades lentament, o usant la teva maquina per a altres fins. La deteccio pot trigar mesos. Per tant, la **prevencio** (Tailscale, claus, firewall) es molt mes barata que la **remediacio** (forensics, neteja, restablir serveis).

**Aplica al BernatLab**: encara que sembli un sistema petit, els impactes poden ser severs. Un hort automatic es un sistema critic (afecta plantes, animals si hi ha, etc.). Cal prendre's la seguretat seriosament des del primer dia.

---

## Pregunta 15 (oberta): Tres primeres mesures

**Resposta model**:

Les tres mesures de seguretat que aplicaria **primer** al BernatLab, en ordre:

**Mesura 1 - Tailscale** (la mes critica). Abans de res, cal amagar el servidor a Internet. Tailscale:
- Amaga tots els ports (22, 80, etc.) a Internet public.
- Crea una xarxa privada nomes per a nosaltres.
- No cal obrir cap port al router.
- Temps d'implementacio: 15-30 minuts.
- **Justificacio de l'ordre**: sense aixo, totes les altres mesures son inutils perque els bots ja estan entrant.

**Mesura 2 - SSH amb claus publiques** (no contrasenyes). Un cop Tailscale esta actiu, cal asegurar que SSH nomes accepta claus:
- Generar parell de claus (ed25519).
- Copiar la clau publica al servidor.
- Desactivar `PasswordAuthentication yes` a `/etc/ssh/sshd_config`.
- Afegir `PermitRootLogin no`.
- **Justificacio**: encara que Tailscale amaga el servidor, si la teva maquina Tailscale es compromete, les contrasenyes son molt mes febles que les claus. Es la "defensa en profunditat".

**Mesura 3 - Firewall (ufw)** amb politica deny-by-default. Un cop SSH es segur, cal tancar la resta:
- `sudo ufw default deny incoming`
- Obrir nomes els ports estrictament necessaris (80, 443 si cal).
- `sudo ufw enable`.
- **Justificacio**: encara que els serveis estiguin a localhost, un misconfiguration podria fer que escoltin a tot. El firewall es la xarxa de seguretat.

**L'ordre es important**:
- Si nomes fas Mesura 1, el servidor esta amagat pero si la teva maquina Tailscale es compromete, l'atacant te acces per SSH amb contrasenyes febles.
- Si nomes fas Mesura 1 i 2, el servidor esta amagat i nomes amb claus, pero si accidentalment actives un servei al port 8080, sera accessible desde Tailscale a tothom.
- Si nomes fas Mesura 1 i 3, el servidor esta amagat i nomes ports oberts, pero SSH encara te contrasenyes febles per si Tailscale falla.

**Aplicacio gradual**:
1. Dia 1: instal·la Tailscale, comprova que funciona.
2. Dia 2: genera claus SSH, desactiva contrasenyes, verifica que pots entrar.
3. Dia 3: configura ufw, obre nomes el que cal, verifica que els serveis funcionen.

**Despres**: fail2ban, portsentry, auditd, monitoritzacio. Pero les tres primeres son **imprescindibles**.

---

## Que fer si has fallat moltes preguntes

- **10-12 encerts**: repassa el resum i fes l'exercici practic.
- **7-9 encerts**: posa atencio al Pas 3 (logs SSH) per entendre la magnitud del problema.
- **0-6 encerts**: comença pel Pas 1-2 (inventari de serveis), es la base per entendre la superficie d'atac.

## Que fer si has encertat totes

- Passa al **Capitol 2** (Tailscale i ACLs).
- O investiga "attack surface mapping" amb eines com nmap scripting.
- O llegeix el "OWASP Top 10" per entendre les vulnerabilitats web mes comuns.

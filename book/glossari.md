# Glossari del BernatLab

> Tots els termes tecnics que fas servir al projecte, explicats en catala de manera clara.

Aquest glossari recull, organitza i defineix la terminologia tecnica que apareix al llarg dels set moduls del BernatLab (M1 a M7). Cada entrada porta una definicio curta i, quan es posible, un exemple aplicat al projecte i un enllac al capitol del llibre on sha tractat amb mes profunditat.

Com utilitzar-lo:

- **Lectura lineal** si acabes d'arribar al projecte: et posara al dia amb el vocabulari basic.
- **Consulta puntual** quan trobis un terme que no reconeixes mentre llegeixes un capitol o fas una tasca de manteniment.
- **Referencia rapida** abans de fer un runbook, una auditoria o un DRP.

Si hi trobes a faltar un terme o vols afegir-ne un de nou, obre una PR a `bernatlab/book/glossari.md`.

---

## Xarxa i connectivitat

### IP (adreca IP)
Identificador numeric unic que rep cada dispositiu dins d'una xarxa. En IPv4 son quatre grups de fins a tres xifres (p. ex. `192.168.1.42`); en IPv6 son vuit grups de quatre hexadecimals. 
**Al BernatLab:** la Raspberry te una IP local del tipus `192.168.1.42` a la LAN de casa, i una IP publica assignada per l'operador que canvia sovint. 
Veure: capitol 4 (Xarxa, SSH i Tailscale).

### DNS (Domain Name System)
Sistema que tradueix noms de domini (`bernatlab.cat`) a adreces IP. Es el "agenda de telefon" d'Internet. 
**Al BernatLab:** MagicDNS de Tailscale ens permet accedir a `pi.bernatlab.ts.net` sense recordar la IP. 
Veure: capitols 4 i 44.

### DHCP (Dynamic Host Configuration Protocol)
Protocol pel qual un router assigna automaticament una IP, mascara de subxarxa, porta d'enllac i DNS als dispositius de la xarxa. 
**Al BernatLab:** el router de casa fa de servidor DHCP; la Raspberry rep la IP `192.168.1.42` en engegar. 
Veure: capitol 4.

### Port
Numero de 16 bits (0-65535) que identifica una aplicacio o servei dins d'una IP. Combinant IP + port s'identifica un punt de comunicacio unic. 
**Al BernatLab:** port 22 per a SSH, 80/443 per a HTTP/HTTPS, 1883 per a MQTT, 8086 per a InfluxDB, 3000 per a Grafana, 9000 per a Portainer, 9090 per a Prometheus, 11434 per a Ollama. 
Veure: capitols 4, 12, 15, 19.

### NAT (Network Address Translation)
Mecanisme pel qual el router tradueix adreces privades internes a una adreca publica quan un dispositiu surt a Internet. Permet compartir una sola IP publica entre molts dispositius. 
**Al BernatLab:** la Raspberry surt a Internet a traves del router de casa fent NAT; per aixi la IP publica no es veu des de fora sense fer port forwarding. 
Veure: capitol 4.

### Firewall (tallafoc)
Sistema que filtra el trafic de xarxa segons regles: permet o denega connexions per IP, port, protocol o direccio. 
**Al BernatLab:** tenim el tallafoc del router (WAN) i un tallafoc de host amb UFW. 
Veure: capitol 47 (fail2ban i tallafocs).

### VPN (Virtual Private Network)
Connexio xifrada que crea un "tunel" segur entre dos punts a traves d'una xarxa no confiable com Internet. Permet accedir a la xarxa de casa des de fora com si hi fossis fisicament. 
**Al BernatLab:** Tailscale actua com a VPN basada en WireGuard, creant una xarxa privada entre la Raspberry, el Mac, el mobil i el portatil de viatge. 
Veure: capitols 4 i 44.

### Tailscale
Servei de VPN mesh basat en WireGuard que crea una xarxa privada entre dispositius sense necessitat d'obrir ports al router. Inclou MagicDNS i ACLs. 
**Al BernatLab:** es la columna vertebral de la nostra xarxa: tots els serveis s'accedeixen nomes a traves de Tailscale, mai directament per Internet. 
Veure: capitols 4, 44, 59.

### MagicDNS
Funcionalitat de Tailscale que resol automticament els noms dels nodes de la xarxa Tailscale sense configurar un servidor DNS manual. 
**Al BernatLab:** podem fer `ssh bernat@pi` en lloc de buscar la IP `100.x.y.z`. 
Veure: capitols 4 i 44.

### ACL (Access Control List)
Llista de regles que defineix que pot fer cada usuari o dispositiu dins d'una xarxa o servei. A Tailscale, les ACLs determinen quin node pot accedir a quin altre node i per quin port. 
**Al BernatLab:** el node `pi` pot accedir a `mac` per SSH (port 22), pero `mac` no pot accedir a `pi` per Portainer (port 9000) si no ho permetem explicitament. 
Veure: capitol 44.

### Node
Dispositiu dins d'una xarxa. A Tailscale, cada maquina que hi esta connectada es considera un node. 
**Al BernatLab:** els nodes son la Raspberry Pi (`pi`), el Mac (`mac`), el portatil (`laptop`), el servidor VPS (`vps`) i el mobil (`phone`). 
Veure: capitols 4 i 44.

### SSH (Secure Shell)
Protocol de xarxa que permet accedir a la linia de comandes d'un servidor remot de forma xifrada. Substitueix telnet i FTP sense xifrat. 
**Al BernatLab:** es la porta d'entrada al servidor. `ssh bernat@pi` ens connecta a la Raspberry des de qualsevol node de Tailscale. 
Veure: capitol 4.

### Clau publica / clau privada
Parell de fitxers criptografics: la clau privada es queda al teu dispositiu i es secreta; la clau publica es copia al servidor. Serviran per autenticacio sense contrasenya. 
**Al BernatLab:** tenim una clau Ed25519 generada al Mac, la clau publica copiada a `~/.ssh/authorized_keys` de la Raspberry, i la privada protegida a `~/.ssh/id_ed25519`. 
Veure: capitol 4.

### Agent SSH
Programa que desa les claus privades desxifrades en memoria per evitar haver-les d'introduir cada vegada. Es el `ssh-agent` a Unix o Pageant a Windows. 
**Al BernatLab:** `ssh-add ~/.ssh/id_ed25519` despres d'arrencar l'agent permet fer multiples connexions SSH sense reintroduir la passphrase. 
Veure: capitol 4.

### TLS (Transport Layer Security)
Protocol criptografic que xifra el transit entre client i servidor. Es el successor de SSL. 
**Al BernatLab:** tots els serveis web exposats a Internet haurien d'anar sobre TLS, ja sigui amb Tailscale HTTPS o amb un reverse proxy + Let's Encrypt. 
Veure: capitols 20, 38, 44.

### Certificat (digital)
Document electronic signat per una autoritat de certificacio (CA) que garanteix que una clau publica pertany a un domini concret. 
**Al BernatLab:** els certificats de Let's Encrypt es renoven automaticament cada 90 dies amb un client ACME. 
Veure: capitol 20.

### Let's Encrypt
Autoritat de certificacio gratuita, automatitzada i oberta que emet certificats TLS valids per qualsevol domini. 
**Al BernatLab:** l'usem per exposar serveis amb HTTPS valid (cadenat verd al navegador) sense pagar. 
Veure: capitol 20.

### HTTP / HTTPS
HTTP es el protocol base de la web (port 80). HTTPS es HTTP sobre TLS (port 443), xifrat. 
**Al BernatLab:** Tailscale exposa serveis HTTP que es beneficien d'HTTPS automatic gestionat per Tailscale. 
Veure: capitols 4, 20, 38.

### REST (Representational State Transfer)
Estil d'arquitectura per dissenyar APIs web on cada URL representa un recurs i les operacions es fan amb verbs HTTP (GET, POST, PUT, DELETE). 
**Al BernatLab:** la nostra API publica de dades de sensors segueix principis REST (`GET /api/sensors/temperature?range=24h`). 
Veure: capitol 20.

### API (Application Programming Interface)
Conjunt de definicions i protocols que permeten que dues aplicacions es comuniquin. Una API web es sol exposar sobre HTTP/HTTPS. 
**Al BernatLab:** consumim la API d'Ollama per fer consultes al LLM local i exposem una API propia de dades de sensors. 
Veure: capitols 20, 39.

### JSON (JavaScript Object Notation)
Format de text estructurat en parells clau-valor i llistes, molt utilitzat per intercanviar dades entre serveis. 
**Al BernatLab:** tots els missatges MQTT que publiquen els sensors van en JSON: `{"temp": 21.4, "hum": 58, "ts": 1712345678}`. 
Veure: capitols 12, 14, 20.

### WireGuard
Protocol de VPN modern, rapid i minimalista, basat en criptografia d'elliptic curves. Es el cor de Tailscale. 
**Al BernatLab:** mai no configurem WireGuard directament, pero Tailscale l'utilitza per sota. 
Veure: capitol 4.

### LAN / WAN
LAN (Local Area Network) es la xarxa local de casa; WAN (Wide Area Network) es Internet o la xarxa de l'operador. 
**Al BernatLab:** la Raspberry es a la LAN; el portatil de viatge accedeix a la LAN a traves de Tailscale. 
Veure: capitol 4.

### Port forwarding
Regla al router que redirigeix un port entrant de la WAN a un port concret d'un dispositiu de la LAN. 
**Al BernatLab:** evitem fer-ne servir gracies a Tailscale, que no requereix obrir cap port al router. 
Veure: capitol 4.

---

## Maquinari

### Raspberry Pi
Ordinador de placa unica (SBC) de mida targeta de credit, fabricat per la Raspberry Pi Foundation. Es el cor del BernatLab. 
**Al BernatLab:** la Raspberry Pi 4 amb 4 o 8 GB de RAM allotja tots els serveis via Docker. 
Veure: capitols 2, 57, 59.

### ARM
Arquitectura de processador RISC usada per la Raspberry Pi i per quasi tots els telefoncs. Es diferent de x86 (Intel/AMD) i algunes imatges Docker no hi son compatibles. 
**Al BernatLab:** triem imatges Docker multiarch (linux/arm64 o linux/arm/v7) perque la Pi 4 es ARMv8. 
Veure: capitol 2.

### CPU (Unitat Central de Proces)
El processador principal del sistema. 
**Al BernatLab:** la Pi 4 te un Broadcom BCM2711 amb 4 nuclis Cortex-A72 a 1.8 GHz. 
Veure: capitol 2.

### RAM (Random Access Memory)
Memoria de treball volatil on el sistema i les aplicacions carreguen dades actives. Es perd en apagar. 
**Al BernatLab:** la Pi 4 amb 4 GB limita quants contenidors podem tenir simultanis. Monitoritzem l'us amb Prometheus i Grafana. 
Veure: capitols 2, 52, 67.

### microSD
Targeta de memoria flash on viu el sistema operatiu de la Raspberry. Es l'arrel d'arrencada. 
**Al BernatLab:** usem una microSD de 32 GB o mes, classe A2 per millor rendiment. 
Veure: capitol 2.

### GPIO (General Purpose Input/Output)
Pins fisics de la Raspberry que es poden programar com a entrada o sortida digital per connectar sensors, LEDs, relés, etc. 
**Al BernatLab:** usem GPIO per llegir sensors casolans o controlar un relé d'enllumenat. 
Veure: capítols 2, 28, 59.

### Ethernet
Standard de xarxa per cable (RJ45). Es la connexio mes estable i rapida. 
**Al BernatLab:** la Pi esta connectada per Ethernet al router per minimitzar latencia i desconnexions. 
Veure: capítols 2, 4, 27.

### Wi-Fi
Standard de xarxa sense fils (IEEE 802.11). 
**Al BernatLab:** la Wi-Fi es reserva per a dispositius mobils o per a una Raspberry sense Ethernet. 
Veure: capítols 2, 4.

### USB (Universal Serial Bus)
Standard de connexio per a periferics: tecles, discs, modems, sensors. 
**Al BernatLab:** el gateway LoRa es connecta per USB a la Raspberry. 
Veure: capítols 2, 27.

### HDMI
Connector de video/audio digital. 
**Al BernatLab:** nomes l'usem per instal·lacio inicial; un cop configurada, la Raspberry va sense pantalla. 
Veure: capitol 2.

### Font d'alimentacio
Dispositiu que subministra electricitat al maquinari. La Raspberry Pi 4 necessita 5V i almenys 3A per USB-C. 
**Al BernatLab:** usem la font oficial de 5.1V/3.0A per evitar avisos de baixa tensio que farien throttling. 
Veure: capítols 2, 57.

### Voltatge
Diferencia de potencial electric, mesurat en volts (V). 
**Al BernatLab:** 5V per a la Pi, 3.3V per als GPIO, 12V per a alguns sensors. 
Veure: capitols 2, 24, 28.

### Amperatge
Intensitat del corrent electric, mesurada en ampers (A). 
**Al BernatLab:** una font de 5V/3A pot subministrar fins a 3 ampers, que es el minim recomanat per a la Pi 4 amb disc USB. 
Veure: capítols 2, 28.

### Temperatura
Mesura termica en graus Celsius. Les RPi es poden escalfar molt i afecten el rendiment. 
**Al BernatLab:** grafiquem la temperatura de la CPU per anticipar throttling. 
Veure: capítols 2, 52, 67.

### Throttling
Reduccio automatica de la frequencia del processador per evitar que es faci malbe per calor excessiva. 
**Al BernatLab:** veiem pics de throttling a l'estiu si la Pi es en un armari tancat. La mitigem amb dissipadors o un ventilador. 
Veure: capitols 2, 67.

### Sensor
Dispositiu que mesura una magnitud fisica (temperatura, humitat, llum, etc.) i la converteix en un senyal electric. 
**Al BernatLab:** tenim sensors de temperatura i humitat, sensors de substrat, i un node LoRa amb BME280. 
Veure: capítols 14, 23, 28.

### Actuador
Dispositiu que realitza una accio fisica (obrir una valvula, encendre un LED) a partir d'un senyal electric. 
**Al BernatLab:** tenim un actuador per obrir/tancar el reg del hort, controlat per Node-RED. 
Veure: capítols 17, 18.

### Microcontrolador
Xip que integra CPU, memoria i perifèrics en un sol circuit, optimitzat per controlar dispositius electronics. 
**Al BernatLab:** els nodes LoRa utilitzen un microcontrolador ESP32-S3 o STM32WL. 
Veure: capítols 28, 29.

### ESP32
Familia de microcontroladors de baix cost amb Wi-Fi i Bluetooth integrats, fabricats per Espressif. 
**Al BernatLab:** molt usat en nodes sensors DIY per la seva facilitat de programacio amb Arduino IDE o MicroPython. 
Veure: capítols 28, 29.

### Disc SSD extern
Disc dur d'estat solid connectat per USB, usat com a emmagatzematge persistent per a la Raspberry. 
**Al BernatLab:** l'usem per moure la base de dades d'InfluxDB fora de la microSD i evitar-ne el desgast. 
Veure: capítols 15, 22, 45.

---

## Sistema operatiu Linux

### Kernel
Nucleu del sistema operatiu, el programa que gestiona CPU, memoria, dispositius i processos. 
**Al BernatLab:** fem servir el kernel de Raspberry Pi OS basat en Linux 6.x. 
Veure: capitol 3.

### Distribucio
Paquet que inclou el kernel Linux, un sistema d'instal·lacio, un gestor de paquets i un entorn d'usuari. 
**Al BernatLab:** Raspberry Pi OS Lite (sense escriptori) es la nostra distribucio. 
Veure: capitols 2, 3.

### Debian
Una de les distribucions Linux mes exteses i estables. Es la base de Raspberry Pi OS i d'Ubuntu. 
**Al BernatLab:** la majoria de documentacio de Debian ens serveix directament per a Raspberry Pi OS. 
Veure: capitol 3.

### Raspberry Pi OS
Distribucio oficial basada en Debian optimitzada per a la Raspberry Pi. 
**Al BernatLab:** la versio Lite (sense entorn grafic) es la mes eficient per servidors. 
Veure: capitols 2, 3, 59.

### Sistema de fitxers
Forma en que el sistema operatiu organitza els fitxers en un disc. Exemples: ext4, FAT32, NTFS, btrfs, ZFS. 
**Al BernatLab:** la microSD porta ext4, que es el standard a Linux. 
Veure: capitol 3.

### Particio
Divisio logica d'un disc. Cada particio te el seu propi sistema de fitxers. 
**Al BernatLab:** tenim una particio a la microSD (`/`) i una altra al SSD extern (`/mnt/dades`). 
Veure: capitol 3.

### mount
Accio de fer accessible una particio o un sistema de fitxers dins l'arbre de directoris. 
**Al BernatLab:** muntem el SSD a `/mnt/dades` cada arrencada. 
Veure: capitol 3.

### fstab
Fixer `/etc/fstab` que llista els sistemes de fitxers que es munten automaticament en arrencar. 
**Al BernatLab:** hi afegim el SSD perque es munti automaticament. 
Veure: capítols 3, 22.

### Usuari / grup
Linux es multiusuari. Cada compte te un UID numeric i pertany a un o mes grups. 
**Al BernatLab:** l'usuari `bernat` pertany als grups `sudo`, `docker`, `dialout` i `gpio`. 
Veure: capitols 3, 48, 60.

### Permisos
Sistema que defineix que pot fer cada usuari sobre cada fitxer. Son tres bits: lectura (r), escriptura (w), execucio (x), per a tres actors: propietari (u), grup (g), altres (o). 
**Al BernatLab:** els fitxers de configuracio tenen permisos `600` (només el propietari llegeix i escriu). 
Veure: capitol 3.

### chmod
Comanda per canviar els permisos d'un fitxer o directori. 
**Al BernatLab:** `chmod 600 ~/.ssh/id_ed25519` protegeix la clau privada. 
Veure: capitols 3, 4.

### chown
Comanda per canviar el propietari i el grup d'un fitxer o directori. 
**Al BernatLab:** `sudo chown -R influxdb:influxdb /mnt/dades/influxdb`. 
Veure: capitol 3.

### Sudo
Comanda que permet executar altres comandes amb privilegis de superusuari (root). 
**Al BernatLab:** l'usuari `bernat` pot fer `sudo` gracies a pertanyer al grup `sudo`. 
Veure: capítols 3, 48.

### Root
Superusuari de Linux, amb acces absolut al sistema. UID 0. 
**Al BernatLab:** mai no ens hi connectem directament; sempre usem `sudo`. 
Veure: capítols 3, 48, 60.

### PATH
Variable d'entorn que llista els directoris on el shell busca les comandes. 
**Al BernatLab:** afegim `~/.local/bin` al PATH per tenir les eines de Python. 
Veure: capitol 3.

### Servei
Programa que s'executa en segon pla i ofereix una funcionalitat continua. 
**Al BernatLab:** Docker, Mosquitto, Grafana, Node-RED son serveis. 
Veure: capítols 3, 5, 12.

### systemd
Sistema d'inicialitzacio i gestor de serveis de la majoria de distribucions Linux modernes. 
**Al BernatLab:** gestiona l'arrencada de Docker i dels seus contenidors. 
Veure: capitols 3, 22, 54.

### Unit (unitat systemd)
Definicio d'un recurs que systemd pot gestionar: servei, timer, mount, socket, target, etc. 
**Al BernatLab:** tenim un timer que executa el backup diariament. 
Veure: capítols 22, 45, 54.

### journalctl
Comanda per consultar els logs del sistema que desa systemd. 
**Al BernatLab:** `journalctl -u docker -f` ens mostra els logs de Docker en temps real. 
Veure: capítols 3, 49, 56.

### Proces
Instancia d'un programa en execucio, identificada per un PID unic. 
**Al BernatLab:** cada contenidor Docker es un proces per al sistema operatiu amfitrio. 
Veure: capitol 3.

### PID (Process Identifier)
Numero unic que identifica un proces en el sistema. 
**Al BernatLab:** `ps aux` ens mostra tots els PIDs actius. 
Veure: capitol 3.

### Signal
Senyal que s'envia a un proces per comunicar-li algo (aturar-se, recarregar, etc.). 
**Al BernatLab:** enviem `SIGTERM` (15) per aturar un contenidor de manera neta. 
Veure: capítols 3, 5.

### kill
Comanda per enviar un signal a un proces. 
**Al BernatLab:** `kill 1234` envia SIGTERM al proces amb PID 1234. 
Veure: capitol 3.

### Paquet
Arxiu que conte un programa i les seves metadades, preparat per ser instal·lat pel gestor de paquets. 
**Al BernatLab:** `docker-ce`, `mosquitto`, `curl` son exemples de paquets Debian. 
Veure: capitol 3.

### APT (Advanced Package Tool)
Gestor de paquets de Debian i derivats. 
**Al BernatLab:** `sudo apt install mosquitto-clients` per instal·lar el client MQTT. 
Veure: capitol 3.

### Repositori
Servidor que allotja paquets per a una distribucio concreta. 
**Al BernatLab:** afegim el repositori oficial de Docker per tenir versions actualitzades. 
Veure: capítols 3, 61.

### snap
Sistema d'instal·lacio universal de paquets, gestionat per Canonical. Alternativa als paquets nadius. 
**Al BernatLab:** no l'usem, preferim Docker o APT. 
Veure: capitol 3.

### Shell
Programa que interpreta les comandes de l'usuari. 
**Al BernatLab:** el shell per defecte a la Pi es bash. 
Veure: capitol 3.

### bash
Un dels shells mes estesos a Linux. Es el per defecte a Raspberry Pi OS. 
**Al BernatLab:** els nostres scripts de manteniment son `.sh` executables per bash. 
Veure: capítols 3, 54, 55.

### Terminal
Programa que mostra un shell en una finestra. 
**Al BernatLab:** accedim al terminal de la Pi per SSH amb el terminal nadiu del Mac o amb Windows Terminal. 
Veure: capitol 3.

### stdout / stderr
Canals de sortida estandard d'un proces: stdout per a la sortida normal, stderr per a errors. 
**Al BernatLab:** redirigim `stderr` a un fitxer de log separat. 
Veure: capítols 3, 49, 54.

### pipe
Operador `|` que connecta la sortida d'una comanda amb l'entrada d'una altra. 
**Al BernatLab:** `docker ps | grep mosquitto` filtra els contenidors que contenen "mosquitto". 
Veure: capitol 3.

### Cron
Dimoni que executa comandes programades a hores determinades. 
**Al BernatLab:** el backup diari es programa amb cron (o amb un timer de systemd). 
Veure: capítols 22, 45, 54.

### Cron
Dimoni que executa comandes a intervals regulars segons un fitxer crontab. 
**Al BernatLab:** `0 3 * * * /opt/bernatlab/backup.sh` llança el backup cada nit a les 3:00. 
Veure: capítols 22, 45, 54.

### systemd-timer
Alternativa moderna a cron, integrada amb systemd i els seus logs. 
**Al BernatLab:** preferim timers abans que cron per tenir logs centralitzats a journald. 
Veure: capítols 22, 54, 55.

### entorn grafic / GUI
Entorn d'escriptori amb finestres, icones i ratoli. 
**Al BernatLab:** la Pi no te entorn grafic per estalviar recursos; tot es fa per linia de comandes o via web. 
Veure: capítols 2, 3.

### headless
Servidor sense pantalla, teclat ni ratoli connectats. Es gestiona remotament. 
**Al BernatLab:** la Raspberry opera headless des del primer dia. 
Veure: capítols 2, 4, 59.

### SSH
Veure l'entrada a Xarxa i connectivitat.

---

## Contenidors i Docker

### Contenidor
Instancia aillada d'un programa que s'executa sobre el kernel de l'amfitrio, amb el seu propi sistema de fitxers, xarxa i processos. Es una alternativa mes lleugera a una maquina virtual. 
**Al BernatLab:** cada servei (Grafana, InfluxDB, Mosquitto, Node-RED) corre dins del seu propi contenidor. 
Veure: capítols 5, 6, 61.

### Imatge
Plantilla de solament lectura que serveix com a base per crear un contenidor. Conte el sistema de fitxers, llibreries i el codi de l'aplicacio. 
**Al BernatLab:** la imatge `grafana/grafana:10.4.0` es la que usem per crear el contenidor de Grafana. 
Veure: capitol 5.

### Dockerfile
Fixer de text amb les instruccions per construir una imatge Docker pas a pas. 
**Al BernatLab:** no n'escrivim cap (usem imatges oficials), pero els entenem per a futurs serveis custom. 
Veure: capitol 5.

### Volum
Mecanisme per persistir dades d'un contenidor fora del seu sistema de fitxers temporal. 
**Al BernatLab:** el volum `influxdb-data` manté la base de dades encara que el contenidor es recrei. 
Veure: capítols 5, 15, 22.

### xarxa Docker
Xarxa virtual gestionada per Docker que connecta contenidors entre si. 
**Al BernatLab:** creem una xarxa anomenada `bernatlab` per on es comuniquen tots els serveis. 
Veure: capítols 5, 6, 61.

### link (enllaç)
Connexio entre contenidors que els permet comunicar-se per nom dins la mateixa xarxa Docker. 
**Al BernatLab:** avui dia preferim les xarxes Docker definides explicitament. 
Veure: capitol 5.

### Docker Compose
Eina que permet definir i orquestrar multiples contenidors amb un sol fitxer `docker-compose.yml`. 
**Al BernatLab:** tot el BernatLab es defineix en un o mes fitxers `compose.yaml` que mantenim al repo. 
Veure: capítols 5, 6, 61.

### servei (a Compose)
Bloc dins d'un `docker-compose.yml` que defineix un contenidor concret. 
**Al BernatLab:** el servei `mosquitto` configura el contenidor del broker MQTT. 
Veure: capítols 5, 6, 13, 61.

### stack
Conjunt de serveis que s'executen conjuntament, generalment definits en un `compose.yaml` i desplegats amb Portainer. 
**Al BernatLab:** el "stack bernatlab" conte 12 serveis: mosquitto, influxdb, telegraf, nodered, grafana, prometheus, etc. 
Veure: capítols 5, 6.

### Registre / Hub
Repositori d'imatges Docker accessible per xarxa. Docker Hub es el mes conegut. 
**Al BernatLab:** descarreguem imatges de Docker Hub (`docker pull grafana/grafana`). 
Veure: capitol 5.

### pull / push
`docker pull` descarrega una imatge des d'un registre; `docker push` hi puja una imatge local. 
**Al BernatLab:** `docker compose pull` actualitza totes les imatges del stack. 
Veure: capítols 5, 6, 22.

### Multi-stage build
Tecnica de Dockerfile que permet construir una imatge en multiples etapes per obtenir una imatge final mes petita i segura. 
**Al BernatLab:** l'usem quan escribim imatges custom per allotjar scripts de Python. 
Veure: capitol 5.

### Layer ( capa)
Cada instruccio d'un Dockerfile genera una capa a la imatge. Docker reutilitza capes no modificades per accelerar les construccions. 
**Al BernatLab:** combinar `RUN apt update && apt install` en una sola capa evita imatges inflades. 
Veure: capitol 5.

### Portainer
Eina web per gestionar Docker de forma visual: contenidors, imatges, volums, xarxes, stacks. 
**Al BernatLab:** Portainer es la nostra GUI principal per administrar el stack. 
Veure: capítols 6, 61.

### Traefik
Reverse proxy i balancejador modern pensat per a Docker, amb deteccio automatica de serveis i TLS automatic. 
**Al BernatLab:** es l'opcio que mirem per exposar serveis amb HTTPS valid sense Tailscale. 
Veure: capitol 20.

### Nginx
Servidor web i reverse proxy molt utilizat i madur. 
**Al BernatLab:** l'usem com a reverse proxy dins d'alguns serveis i per allotjar el web estatic del projecte. 
Veure: capítols 8, 20.

### Watchtower
Contenidor que vigila les imatges dels altres contenidors i els actualitza automaticament. 
**Al BernatLab:** el tenim en proves; per entorns productius prefereixo actualitzar manualment. 
Veure: capitol 22.

### restart policy
Regla que defineix quan Docker ha de reiniciar un contenidor: `no`, `on-failure`, `always`, `unless-stopped`. 
**Al BernatLab:** tots els nostres serveis son `restart: unless-stopped` perque es reiniciin si la Pi es reinicia. 
Veure: capítols 5, 6, 22.

### healthcheck
Prova que Docker fa periodica al contenidor per saber si esta sa. 
**Al BernatLab:** Grafana, InfluxDB i Mosquitto porten healthcheck definit al compose. 
Veure: capítols 5, 6, 22.

---

## Dades i bases de dades

### Base de dades
Sistema que permet emmagatzemar, consultar i actualitzar dades de forma persistent i estructurada. 
**Al BernatLab:** tenim InfluxDB per a dades temporals de sensors i, per a metadades, avaluem SQLite. 
Veure: capítols 15, 22.

### SQL (Structured Query Language)
Llenguatge estandard per fer consultes a bases de dades relacionals. 
**Al BernatLab:** les consultes a InfluxDB 1.x usen una variant d'SQL anomenada InfluxQL. 
Veure: capitol 15.

### NoSQL
Categoria de bases de dades que no usen el model relacional: documentals, clau-valor, columnars, graf. 
**Al BernatLab:** InfluxDB es considera NoSQL per la seva estructura de series temporals. 
Veure: capitol 15.

### Taula
Estructura d'una base de dades relacional que organitza les dades en files i columnes. 
**Al BernatLab:** a PostgreSQL (si l'usessim), tindriem una taula `sensors` amb columnes `id`, `nom`, `tipus`, `ubicacio`. 
Veure: capitols 15, 22.

### Columna / fila
Una columna es un camp de la taula; una fila es un registre concret. 
**Al BernatLab:** cada lectura de sensor es una fila amb columnes `sensor_id`, `valor`, `timestamp`. 
Veure: capitol 15.

### Primary key
Columna o conjunt de columnes que identifica univocament cada fila d'una taula. 
**Al BernatLab:** a la taula `lectures`, la primary key es la composicio `(sensor_id, timestamp)`. 
Veure: capitol 15.

### Index
Estructura auxiliar que accelera les consultes a una taula. 
**Al BernatLab:** InfluxDB ja porta un index temporal implicit que fa rapides les consultes per rang. 
Veure: capitol 15.

### SQLite
Base de dades relacional embeguda en un unic fitxer, sense servidor separat. 
**Al BernatLab:** la fem servir per guardar configuracio i metadades petites (per exemple, l'estat del Hort Osona). 
Veure: capítols 21, 22.

### PostgreSQL
Base de dades relacional open source molt robusta i extesa. 
**Al BernatLab:** la considerem per a metadades de llarga vida (cataleg de sensors, usuaris). 
Veure: capitol 22.

### InfluxDB
Base de dades de series temporals open source, pensada per a dades amb marca de temps (metrics, sensors, events). 
**Al BernatLab:** es la base de dades principal del BernatLab. Emmagatzema lectures de temperatura, humitat, etc. 
Veure: capitol 15.

### TimescaleDB
Extensio de PostgreSQL que afegeix capacitats de serie temporal: hypertable, compressio, retencio automatica. 
**Al BernatLab:** l'avaluem com a substitut d'InfluxDB si mai necessitem transaccions SQL. 
Veure: capitol 15.

### Continuous query
Consulta a InfluxDB 1.x que s'executa periodicament i desa el resultat en una nova serie agregada. 
**Al BernatLab:** la fem servir per calcular la mitjana horaria de temperatura. 
Veure: capítols 15, 18, 52.

### Retention policy (politica de retencio)
Regla que defineix quant de temps es guarden les dades d'una serie temporal. 
**Al BernatLab:** tenim una retencio de 90 dies per a dades en cru i 5 anys per a dades agregades. 
Veure: capitols 15, 22, 45.

### Bucket
Contenidor logic dins d'InfluxDB 2.x que agrupa dades amb una politica de retencio. 
**Al BernatLab:** el bucket `sensors` desa les lectures en cru; el bucket `sensors_agregats` desa les mitjanes horaries. 
Veure: capitol 15.

### Measurement
Equivalent a una "taula" a InfluxDB: un tipus de dada amb camps i etiquetes. 
**Al BernatLab:** tenim els measurements `temperature`, `humitat`, `pressio`. 
Veure: capitol 15.

### Tag
A InfluxDB, etiqueta indexada que serveix per filtrar i agrupar (per exemple, `sensor_id`, `ubicacio`). 
**Al BernatLab:** el tag `sensor_id` ens permet filtrar rapidament les dades d'un sensor concret. 
Veure: capítols 14, 15, 19.

### Field
A InfluxDB, valor numeric no indexat associat a un measurement. 
**Al BernatLab:** els camps `value=21.4` contenen la lectura real del sensor. 
Veure: capítols 14, 15.

### Backup
Copia de seguretat de les dades per poder-les restaurar en cas d'incident. 
**Al BernatLab:** backup diari amb Restic de la base de dades, configuracions i volum de Grafana. 
Veure: capítols 22, 45, 50.

### Restore
Accio de recuperar dades des d'un backup. 
**Al BernatLab:** restaurem InfluxDB des del darrer backup valid quan calgui. 
Veure: capítols 22, 45, 50.

### Dump
Exportacio completa d'una base de dades a un fitxer. 
**Al BernatLab:** `influx backup` genera un dump que es pot restaurar en un altre node. 
Veure: capitols 15, 22, 45.

### Snapshot
Estat consistent d'un volum o d'una maquina virtual en un moment donat. 
**Al BernatLab:** abans d'actualitzar InfluxDB fem un snapshot del volum. 
Veure: capítols 22, 45.

### Restic
Eina de backups moderna, xifrada, amb deduplicacio i versionat. 
**Al BernatLab:** Restic es la nostra eina principal de backups, amb desti a un disc extern i a un bucket S3. 
Veure: capítols 22, 45.

### Borg (BorgBackup)
Alternativa a Restic, tambe amb deduplicacio, xifrat i montatge de backups com a sistemes de fitxers. 
**Al BernatLab:** considerat, pero ens quedem amb Restic per la seva simplicitat. 
Veure: capitol 45.

### rsync
Eina classica per sincronitzar fitxers entre maquines de manera incremental. 
**Al BernatLab:** la fem servir per sincronitzar carpetes petites entre la Pi i el Mac. 
Veure: capítols 22, 45.

### Volum persistent
Volum Docker que sobreviu a la recreacio del contenidor i garanteix persistencia. 
**Al BernatLab:** `influxdb-data` es un volum persistent nadiu de Docker. 
Veure: capítols 5, 15, 22.

### Volum muntat
Volum o directori de l'amfitrio muntat dins d'un contenidor, compartint fitxers amb el sistema amfitrio. 
**Al BernatLab:** `/mnt/dades/influxdb` es munta dins del contenidor a `/var/lib/influxdb2`. 
Veure: capítols 5, 15.

### Sharding
Distribucio de dades entre multiples nodes o maquines per escalar. 
**Al BernatLab:** no l'apliquem (un sol node), pero el tenim en compte per al futur. 
Veure: capitol 22.

### Replica
Copia d'una base de dades que es manté sincronitzada amb la principal per alta disponibilitat. 
**Al BernatLab:** avui dia sense replica; en un futur, una replica en un VPS. 
Veure: capitol 22.

### WAL (Write-Ahead Log)
Registre previ a l'escriptura que permet recoverabilitat en cas de crash. 
**Al BernatLab:** InfluxDB escriu primer al WAL i despres compacta; per aixi podem perdre pocs segons de dades en cas de tall. 
Veure: capitol 15.

---

## Monitoritzacio

### Metrica
Valor numeric mesurable d'un sistema, capturat periodicament. 
**Al BernatLab:** CPU, RAM, temperatura, nombre de contenidors, latencia MQTT. 
Veure: capítols 52, 67.

### Log
Registre d'esdeveniments amb marca de temps que un sistema o aplicacio escriu per deixar constancia del que ha passat. 
**Al BernatLab:** els logs de Docker van a journald, els de Grafana al seu fitxer, els de Mosquitto a journald. 
Veure: capítols 49, 56.

### Alerta
Notificacio automatica que s'envia quan una metrica supera un llindar o passa un esdeveniment. 
**Al BernatLab:** rebem una alerta a Telegram si la CPU passa del 85% o si un servei esta down. 
Veure: capítols 53, 67.

### Prometheus
Sistema de monitoritzacio i base de dades de series temporals orientat a metriques, basat en model pull. 
**Al BernatLab:** Prometheus recull metriques de la propia Pi, dels serveis i de l'ESP32. 
Veure: capitol 67.

### Exporter
Petit programa que exposa metriques internes d'un servei en format Prometheus. 
**Al BernatLab:** `node_exporter` exposa metriques de la Pi; `mosquitto-exporter` exposa les del broker. 
Veure: capitol 67.

### scrape
Accio de Prometheus de preguntar a un endpoint per obtenir les metriques actuals. 
**Al BernatLab:** scrapejem `node_exporter:9100` cada 15 segons. 
Veure: capitol 67.

### PromQL
Llenguatge de consultes propi de Prometheus, optimitzat per a metriques. 
**Al BernatLab:** la consulta `rate(cpu_usage[5m])` ens dona la CPU mitjana dels ultims 5 minuts. 
Veure: capitol 67.

### Grafana
Eina de visualitzacio de dades temporals que es connecta a multiples fonts (Prometheus, InfluxDB, Loki). 
**Al BernatLab:** Grafana es la nostra eina de dashboards per a sensors, sistema i operativa. 
Veure: capítols 19, 52, 67.

### Dashboard
Conjunt de panells organitzats en una graella que mostren visualitzacions d'un sistema. 
**Al BernatLab:** el dashboard "BernatLab overview" mostra CPU, RAM, temperatura i estat de serveis. 
Veure: capítols 19, 52, 67.

### Panel
Un element individual dins d'un dashboard: un grafic, una taula, un gauge, etc. 
**Al BernatLab:** un panel mostra la temperatura de la CPU de les ultimes 24 hores. 
Veure: capítols 19, 52, 67.

### Alertmanager
Component de Prometheus que gestiona les alertes: deduplica, agrupa i les redirigeix al canal adequat. 
**Al BernatLab:** Alertmanager envia alertes a Telegram via un webhook. 
Veure: capítols 53, 67.

### Uptime Kuma
Eina self-hosted de monitoritzacio de disponibilitat: comprova periodicament que un servei respon i envia alertes si cau. 
**Al BernatLab:** Uptime Kuma vigila 14 serveis: Portainer, Grafana, Mosquitto, etc. 
Veure: capítols 7, 62.

### SLA (Service Level Agreement)
Acord sobre el nivell de servei esperat, sovint expressat com a percentatge de disponibilitat. 
**Al BernatLab:** ens autoimposem un SLA del 99% per al stack principal. 
Veure: capítols 7, 53.

### Pinging
Comprovacio activa d'un servei enviant una peticio i esperant resposta. 
**Al BernatLab:** Uptime Kuma fa pings HTTP, TCP i ICMP cada 60 segons. 
Veure: capítols 7, 62.

### ELK (Elasticsearch, Logstash, Kibana)
Pila classica de gestio de logs: Elasticsearch indexa, Logstash processa, Kibana visualitza. 
**Al BernatLab:** massa pesada per a la Pi, pero la coneixem per si creixem. 
Veure: capitol 49.

### Loki
Sistema de gestio de logs desenvolupat per Grafana Labs, optimitzat per etiquetar en lloc d'indexar text complet. 
**Al BernatLab:** considerat per substituir journald centralitzat, pero de moment fem servir journald + un parell de scripts. 
Veure: capítols 49, 52.

### journald
Dimoni de systemd que recull els logs del sistema i els serveis. 
**Al BernatLab:** `journalctl -u mosquitto -f` ens mostra els logs en directe del broker. 
Veure: capítols 3, 49, 56.

### Heartbeat
Comprovacio periodica que un sistema esta viu. 
**Al BernatLab:** Grafana i Uptime Kuma s'envien heartbeats per confirmar que un es operatiu. 
Veure: capitol 67.

### Dead man's switch
Alerta que es dispara si un sistema deixa d'emetre un senyal esperat. 
**Al BernatLab:** un script fa ping a Healthchecks.io cada 5 minuts; si deixa de fer-ho, Healthchecks ens avisa. 
Veure: capitols 53, 69.

---

## Seguretat

### Contrasenya
Cadenca secreta que autentica un usuari. 
**Al BernatLab:** mai no usem contrasenyes per a SSH (clau publica); per a serveis web usem contrasenyes llargues desades a Bitwarden. 
Veure: capítols 4, 46, 60.

### Hash
Funcio criptografica unidireccional que transforma una entrada en una cadena de longitud fixa. 
**Al BernatLab:** `/etc/shadow` desa els hashes de les contrasenyes, mai les contrasenyes en clar. 
Veure: capítols 46, 48.

### Salt
Cadena aleatoria que s'afegeix a la contrasenya abans d'aplicar el hash per evitar atacs amb taules precalculades. 
**Al BernatLab:** bcrypt i scrypt fan salts automaticament. 
Veure: capitol 46.

### 2FA / MFA
Segon factor d'autenticacio: a mes de la contrasenya, cal un codi temporal o un dispositiu fisic. 
**Al BernatLab:** activem 2FA a Tailscale, GitHub, Bitwarden, Portainer, Grafana, InfluxDB. 
Veure: capitol 46.

### TOTP (Time-based One-Time Password)
Algorisme que genera codis de 6 digits que caduquen cada 30 segons, basat en un secret compartit i l'hora actual. 
**Al BernatLab:** l'app Aegis o Yubico Authenticator ens genera els TOTPs de Tailscale i Grafana. 
Veure: capitol 46.

### U2F / WebAuthn
Estandard de segon factor amb clau criptografica fisica (YubiKey, Titan Key). 
**Al BernatLab:** considerem afegir una YubiKey per a comptes critics (GitHub, Tailscale admin). 
Veure: capitol 46.

### SSH hardening
Conjunt de practiques per endureir la configuracio SSH: deshabilitar login amb root, deshabilitar contrasenyes, canviar port, etc. 
**Al BernatLab:** editem `/etc/ssh/sshd_config` per aplicar aquestes mesures. 
Veure: capítols 4, 48, 60.

### fail2ban
Eina que vigila els logs i baneja temporalment les IP que fallen massa l'inici de sessio. 
**Al BernatLab:** fail2ban vigila SSH i ens avisa quan una IP es banejada. 
Veure: capitol 47.

### Port knocking
Tecnica que obre ports del tallafoc nomes quan es rep una sequencia especifica de connexions a altres ports. 
**Al BernatLab:** no l'usem (Tailscale ja ens dona seguretat), pero el coneixem. 
Veure: capitol 47.

### UFW (Uncomplicated Firewall)
Tallafoc senzill per a Ubuntu/Debian que simplifica la gestio de iptables. 
**Al BernatLab:** UFW nomes permet SSH (port 22) des de Tailscale; la resta queda tancada. 
Veure: capítols 47, 60.

### iptables
Sistema de tallafoc de baix nivell del kernel Linux. 
**Al BernatLab:** l'entenem pero no l'editem a ma; UFW i Docker gestionen les regles. 
Veure: capitol 47.

### nftables
Successor modern d'iptables, tambe al kernel Linux. 
**Al BernatLab:** Debian 12 ja porta nftables; UFW genera regles nftables. 
Veure: capitol 47.

### Codi malicios (malware)
Programari dissenyat a fer mal: virus, troians, ransomware, spyware. 
**Al BernatLab:** el risc es baix perque la Pi nomes exposa serveis via Tailscale, pero el tenim en compte. 
Veure: capitols 43, 47.

### Virus
Programa que s'auto-replica infectant altres fitxers o sistemes. 
**Al BernatLab:** molt menys prevalent a Linux que a Windows, pero no inexistent. 
Veure: capitol 47.

### Ransomware
Programari que xifra les dades de la victima i demana un rescat per desxifrar-les. 
**Al BernatLab:** el risc es mitiga amb backups desates (Restic + bucket S3 fora de la Raspberry). 
Veure: capítols 22, 45, 50.

### Amenaca
Qualsevol esdeveniment que pugui comprometre la seguretat del sistema. 
**Al BernatLab:** amenaces principals: atac de força bruta a SSH, exposicio accidental d'un servei, robo de credencials. 
Veure: capítols 43, 47, 48.

### Vulnerabilitat
Defecte en un sistema que pot ser explotat per una amenaca. 
**Al BernatLab:** un port obert sense autenticacio es una vulnerabilitat. 
Veure: capítols 43, 48, 49.

### Exploit
Codi o tecnica que aprofita una vulnerabilitat concreta. 
**Al BernatLab:** `apt upgrade` i l'actualitzacio periodica de les imatges Docker ens protegeix dels exploits coneguts. 
Veure: capítols 22, 48.

### CVE (Common Vulnerabilities and Exposures)
Identificador public d'una vulnerabilitat coneguda. 
**Al BernatLab:** el monitoritzem amb un parell d'eines per a les imatges que fem servir. 
Veure: capítols 48, 49.

### Zero-day
Vulnerabilitat que encara no te pegat oficial. 
**Al BernatLab:** el risc es minim gracies a Tailscale i a que no exposem res directament a Internet. 
Veure: capitol 43.

### Xifrat
Transformacio d'una informacio per fer-la illegible sense una clau. 
**Al BernatLab:** xifrem la microSD (LUKS), els backups (Restic), i el transit (Tailscale, TLS). 
Veure: capítols 4, 22, 45, 50.

### GPG (GNU Privacy Guard)
Eina per xifrar i signar dades i correus amb criptografia asimetrica. 
**Al BernatLab:** el fem servir per signar els commits de Git i per xifrar alguns fitxers de configuracio. 
Veure: capítols 9, 45, 48.

### age
Eina moderna de xifratge de fitxers amb criptografia asimetrica, alternativa a GPG mes simple. 
**Al BernatLab:** valorada com a substitut de GPG per a scripts de backup. 
Veure: capitol 45.

### Auditoria
Revisio periodica de la seguretat i l'operativa del sistema. 
**Al BernatLab:** fem una auditoria completa un cop al trimestre, seguint una checklist del llibre. 
Veure: capítols 43, 49, 50.

### Compliance
Conjunt de normes i bones practiques que un sistema ha de complir. 
**Al BernatLab:** no tenim compliance extern obligatori, pero seguim bones practiques de hardening. 
Veure: capítols 43, 48.

### GDPR
Reglament General de Proteccio de Dades de la UE. 
**Al BernatLab:** nomes processem dades personals propies; apliquem minimitzacio i transparencia. 
Veure: capítols 41, 43.

### Bitwarden
Gestor de contrasenyes self-hosted o al núvol. 
**Al BernatLab:** Bitwarden allotja totes les contrasenyes, TOTPs i notes segures del projecte. 
Veure: capítols 4, 46.

### KeePassXC
Alternativa local a Bitwarden, amb un sol fitxer de base de dades xifrat. 
**Al BernatLab:** el tenim com a backup local, pero el dia a dia es amb Bitwarden. 
Veure: capítols 46, 60.

### LUKS (Linux Unified Key Setup)
Standard de xifratge de discs a Linux. 
**Al BernatLab:** xifrem la microSD i el SSD extern amb LUKS. 
Veure: capítols 45, 48, 50.

---

## Intel·ligencia artificial

### LLM (Large Language Model)
Model d'intel·ligencia artificial entrenat amb grans volums de text capaç de generar, resumir, traduir i raonar en llenguatge natural. 
**Al BernatLab:** fem servir LLMs locals via Ollama (Llama 3, Mistral, Phi-3) per a tasques ofimatiques i d'analisi. 
Veure: capítols 33, 35, 39.

### Model (IA)
Arxiu de pesos entrenats que, combinat amb un runtime, pot fer una tasca d'IA. 
**Al BernatLab:** `llama3.1:8b` es el model que usem per defecte al Mac. 
Veure: capítols 33, 34, 35.

### Prompt
Text d'entrada que s'envia a un LLM per obtenir una resposta. 
**Al BernatLab:** els nostres prompts son curts i específics: "Resumeix aquest log en 5 linies". 
Veure: capítols 33, 39, 40.

### Tokens
Unitats minims de text que un LLM processa: aproximadament 4 caracters o 0.75 paraules en angles. 
**Al BernatLab:** amb un model de 8B calen ~5 GB de VRAM o RAM per a context de 4096 tokens. 
Veure: capítols 33, 35, 39.

### Context window
Nombre maxim de tokens que un model pot processar en una sola conversa. 
**Al BernatLab:** Llama 3.1 te una finestra de 128k tokens; per a tasques locals en fem servir 8k-32k. 
Veure: capítols 33, 35, 39.

### Ollama
Runtime per a LLMs locals que descarrega, executa i serveix models amb una sola comanda. 
**Al BernatLab:** Ollama es la nostra eina principal per a inferencia local. 
Veure: capítols 34, 35, 39.

### Llama (Meta)
Familia de LLMs open source de Meta. 
**Al BernatLab:** `llama3.1:8b` ens dona un bon equilibri qualitat/recursos al Mac. 
Veure: capítols 35, 39.

### Mistral
Familia de LLMs open source francesos, amb variants petites pero potents. 
**Al BernatLab:** `mistral:7b` es una alternativa a Llama, molt bona en catala. 
Veure: capitol 35.

### Phi (Microsoft)
Familia de petits LLMs de Microsoft optimitzats per a eficiencia. 
**Al BernatLab:** `phi3:mini` es ideal per ordinadors modestos. 
Veure: capitol 35.

### Gemma (Google)
Familia de LLMs open source de Google, derivats de Gemini. 
**Al BernatLab:** `gemma2:9b` es una bona opcio per al Mac. 
Veure: capitol 35.

### Embedding
Representacio numerica d'un text (o d'una imatge, audio, etc.) en un espai vectorial on la distancia entre vectors indica la similitud semantica. 
**Al BernatLab:** generem embeddings de les fitxes d'hort amb `nomic-embed-text`. 
Veure: capítols 36, 37.

### Vector (IA)
Llista de nombres que representa l'embedding. 
**Al BernatLab:** cada embedding es un vector de 768 o 1024 dimensions. 
Veure: capitol 36.

### Similitud (cosine similarity)
Metrica que mesura l'angle entre dos vectors; 1.0 = identics, 0.0 = ortogonals, -1.0 = oposats. 
**Al BernatLab:** ens indica quan un document es semanticament proper a una consulta. 
Veure: capítols 36, 37.

### RAG (Retrieval-Augmented Generation)
Patron d'IA que combina cerca en una base de coneixement amb generacio de text per part d'un LLM. 
**Al BernatLab:** el RAG ens permet preguntar coses sobre les 76 fitxes d'hort sense entrenar un model nou. 
Veure: capítols 36, 37, 42.

### Retrieval
Pas del RAG en que cerquem els documents mes rellevants per a la pregunta. 
**Al BernatLab:** la cerca es fa per similitud de embeddings. 
Veure: capítols 36, 37.

### Augmented
El LLM rep com a contexte els documents trobats al pas de retrieval, augmentant el seu coneixement. 
**Al BernatLab:** "Augmenta" la resposta del LLM amb dades reals del nostre hort. 
Veure: capitol 37.

### Generation
Pas final del RAG en que el LLM genera la resposta a partir de la pregunta i el contexte. 
**Al BernatLab:** el model genera una resposta en catala citant les fitxes utilitzades. 
Veure: capitol 37.

### Vector database
Base de dades optimitzada per emmagatzemar i cercar vectors d'embedding. 
**Al BernatLab:** ChromaDB ens serveix perfectament per al volum de fitxes que tenim. 
Veure: capítols 36, 37.

### ChromaDB
Base de dades vectorial open source, senzilla i integrable. 
**Al BernatLab:** l'usem per emmagatzemar els embeddings de les fitxes d'hort. 
Veure: capítols 36, 37.

### FAISS
Llibreria de Meta per a cerca de veïns mes propers en grans volums de vectors. 
**Al BernatLab:** valorada per si el volum creix per sobre del que ChromaDB aguanta. 
Veure: capítols 36, 37.

### Fine-tuning
Entrenament addicional d'un model pre-entrenat amb dades especifiques per adaptar-lo a un cas concret. 
**Al BernatLab:** no l'hem fet servir encara; el RAG ens cobreix el cas. 
Veure: capítols 37, 42.

### Transfer learning
Tecnica que reaprofita un model entrenat per a una tasca com a punt de partida per a una altra. 
**Al BernatLab:** els nostres models son pre-entrenats; el fine-tuning n'és un cas. 
Veure: capitol 37.

### Inferencia
Pas de passar una entrada per un model per obtenir una sortida. 
**Al BernatLab:** "Fer inferencia" vol dir executar el model. 
Veure: capítols 33, 35, 39.

### GPU (Graphics Processing Unit)
Processador optimitzat per a calculs en paral·lel, essencial per a inferencia rapida de LLMs grans. 
**Al BernatLab:** al Mac amb Apple Silicon la GPU es unificada amb la CPU i s'anomena "Neural Engine" o "GPU Metal". 
Veure: capítols 33, 35.

### VRAM
Memoria RAM de la GPU. Limita la mida del model i la finestra de contexte. 
**Al BernatLab:** un Mac amb 16 GB de RAM unificada pot servir models de fins a ~12B. 
Veure: capítols 33, 35.

### Neural Engine
Processador dedicat a ML en xip Apple Silicon. 
**Al BernatLab:** CoreML i Ollama l'aprofiten per accelerar la inferencia. 
Veure: capítols 33, 34, 35.

### Whisper
Model d'OpenAI per a transcripcio automatica d'audio a text. 
**Al BernatLab:** valorem integrar-lo per a transcrure audios de camp. 
Veure: capitol 40.

### TTS (Text-to-Speech)
Sintesi de veu a partir de text. 
**Al BernatLab:** valorem XTTS o Piper per a resums en veu alta. 
Veure: capitol 40.

### Hallucinacio
Fenomen pel qual un LLM "inventa" informacio que sona versemblant pero es incorrecta. 
**Al BernatLab:** el RAG redueix les hallucinations perquè el model sempre parteix de dades reals. 
Veure: capítols 37, 41, 42.

### Prompt injection
Atac en que un usuari introdueix instruccions dins d'un prompt per fer que el LLM ignori les seves ordres originals. 
**Al BernatLab:** el risc es minim perque els models son locals i no exposem interfícies publiques. 
Veure: capítols 41, 42.

### Privadesa
Principi de minimitzar l'exposicio de dades personals i de mantenir el control sobre elles. 
**Al BernatLab:** tota la IA es local; cap dada va a núvols de tercers. 
Veure: capitols 33, 41, 43.

---

## IoT i sensors

### Sensor
Veure l'entrada a Maquinari.

### Actuador
Veure l'entrada a Maquinari.

### Microcontrolador
Veure l'entrada a Maquinari.

### MiFlora
Sensor Bluetooth de Xiaomi que mesura temperatura, humitat, lluminositat, conductivitat i fertilitat del substrat. 
**Al BernatLab:** l'integrariem amb un proxy BLE per a l'hort. 
Veure: capítols 14, 21, 28.

### Bluetooth
Standard de comunicacio sense fils de curt abast (2.4 GHz). 
**Al BernatLab:** el fem servir per als sensors MiFlora, que requereixen una pasarel·la BLE. 
Veure: capítols 14, 28.

### BLE (Bluetooth Low Energy)
Variant de Bluetooth optimitzada per a baix consum, ideal per a sensors amb bateria. 
**Al BernatLab:** els MiFlora son BLE; el gateway ha d'estar a prop (~10 m). 
Veure: capítols 14, 28.

### LoRa (Long Range)
Modulacio radio de llarg abast i baix consum, pensada per a IoT. 
**Al BernatLab:** els nostres nodes de camp fan servir LoRa a 868 MHz per arribar a 2-5 km. 
Veure: capítols 23, 24, 25.

### SX1262
Xip de Semtech que implementa la modulacio LoRa, molt usat en nodes moderns. 
**Al BernatLab:** els nostres nodes DIY porten un SX1262 connectat per SPI. 
Veure: capítols 24, 28.

### 868 MHz
Banda de frequencia ISM a Europa per a LoRa i altres tecnologies de llarg abast. 
**Al BernatLab:** a Osona usem 868 MHz, que permet mes potencia que 433 MHz i no interfereix amb Wi-Fi. 
Veure: capítols 24, 25, 28.

### Spreading Factor (SF)
Parametre de LoRa que determina l'abast i el temps a l'aire: SF7 a SF12. Mes SF = mes abast pero menys ample de banda. 
**Al BernatLab:** usem SF7 per defecte i SF12 nomes en casos de cobertura extrema. 
Veure: capítols 24, 28, 32.

### LoRaWAN
Protocol de xarxa sobre LoRa que defineix com els nodes es connecten a una xarxa centralitzada amb un servidor de xarxa (TTN, ChirpStack). 
**Al BernatLab:** tenim una prova pilot amb The Things Network. 
Veure: capítols 25, 26.

### P2P (point-to-point)
Comunicacio directa entre dos nodes LoRa sense servidor de xarxa intermedi. 
**Al BernatLab:** la majoria de nodes del BernatLab son P2P per simplicitat. 
Veure: capítols 25, 31, 32.

### Gateway
Dispositiu que fa de pont entre una xarxa d'area local (Wi-Fi, Ethernet) i una xarxa d'area ampla (LoRa, cellular). 
**Al BernatLab:** la Raspberry amb un SX1303 fa de gateway LoRa i rebeu tots els missatges dels nodes. 
Veure: capítols 26, 27.

### MQTT (Message Queuing Telemetry Transport)
Protocol de missatgeria lleuger, basat en publish/subscribe, pensat per a IoT. 
**Al BernatLab:** tots els nodes publiquen les seves dades via MQTT al broker Mosquitto. 
Veure: capítols 12, 13, 14, 28, 29.

### Mosquitto
Broker MQTT open source lleuger, mantingut per Eclipse Foundation. 
**Al BernatLab:** Mosquitto es el cor de la xarxa IoT: tots els sensors publiquen aqui. 
Veure: capítols 12, 13, 63.

### Broker
Servidor central d'una xarxa MQTT que rep tots els missatges i els redistribueix als subscribers. 
**Al BernatLab:** Mosquitto actua com a broker unic. 
Veure: capítols 12, 13.

### Topic
Cadenca jerarquica que identifica un canal MQTT, per exemple `sensors/hort/temp01`. 
**Al BernatLab:** usem la convencio `bernatlab/<ubicacio>/<sensor>/<tipus>`. 
Veure: capítols 12, 13, 14, 29.

### Publish / Subscribe
Model de missatgeria on els clients "publiquen" missatges a un topic i altres clients es "subscriuen" per rebre'ls. 
**Al BernatLab:** un node publica a `sensors/temp01`; Grafana, Node-RED i Telegraf subscriuen. 
Veure: capítols 12, 13, 17.

### QoS (Quality of Service)
Nivell de garantia d'entrega d'un missatge MQTT: 0 (at most once), 1 (at least once), 2 (exactly once). 
**Al BernatLab:** usem QoS 1 per a dades de sensors normals. 
Veure: capítols 12, 13.

### Retain (flag MQTT)
Si un publisher posa el flag retain, el broker desa l'ultim missatge del topic i l'entrega als nous subscribers. 
**Al BernatLab:** tots els nostres sensors publiquen amb retain=true perque Grafana tingui valor immediat. 
Veure: capítols 12, 13, 14.

### Last Will and Testament (LWT)
Missatge que MQTT envia automaticament quan un client es desconnecta de forma inesperada. 
**Al BernatLab:** si un node es queda sense bateria, podem saber-ho per la LWT. 
Veure: capítols 12, 13, 29.

### Payload
Cos del missatge MQTT, amb la informacio efectiva (temperatura, humitat, etc.). 
**Al BernatLab:** payload en JSON: `{"temp": 21.4, "hum": 58}`. 
Veure: capítols 12, 14, 29.

### JSON
Veure l'entrada a Xarxa i connectivitat.

### Protobuf (Protocol Buffers)
Format de serialitzacio binari desenvolupat per Google, mes compacte i rapid que JSON. 
**Al BernatLab:** el considerem per a nodes amb ample de banda molt limitat. 
Veure: capítols 12, 14.

### BME280
Sensor combinat de Bosch que mesura temperatura, humitat i pressio atmosferica. 
**Al BernatLab:** l'usem als nodes LoRa i al gateway. 
Veure: capítols 14, 28, 65.

### DHT22
Sensor de temperatura i humitat digital de baix cost amb un sol cable de dades. 
**Al BernatLab:** l'usem en prototips ràpids. 
Veure: capitol 14.

### DS18B20
Sensor de temperatura digital amb bus 1-Wire, precís i econòmic. 
**Al BernatLab:** ideal per a mesurar la temperatura del substrat. 
Veure: capitol 14.

---

## Desenvolupament web

### HTML (HyperText Markup Language)
Llenguatge d'etiquetatge que estructura el contingut d'una pagina web. 
**Al BernatLab:** l'index del projecte, la web estàtica i el panell de Grafana son HTML. 
Veure: capítols 8, 38.

### CSS (Cascading Style Sheets)
Llenguatge que defineix l'aparença visual d'una pagina HTML. 
**Al BernatLab:** el `curs.css` aplica colors i tipografies al curs. 
Veure: capítols 8, 38.

### JavaScript
Llenguatge de programacio que s'executa al navegador i dona interactivitat a les pagines. 
**Al BernatLab:** el `curs.js` valida els qüestionaris i la cerca. 
Veure: capítols 17, 38.

### PWA (Progressive Web App)
Aplicacio web que es comporta com una app nativa: es pot instal·lar, funciona offline i envia notificacions. 
**Al BernatLab:** la web del BernatLab es pot instal·lar com a PWA al mobil. 
Veure: capitol 38.

### Service worker
Script que el navegador executa en segon pla i permet缓存, offline mode i notificacions push. 
**Al BernatLab:** el service worker fa que la web del projecte funcioni offline. 
Veure: capitol 38.

### Manifest (web)
Fitxer JSON que defineix el nom, icones, colors i comportament d'una PWA. 
**Al BernatLab:** `manifest.json` permet instal·lar el projecte com a PWA. 
Veure: capitol 38.

### Git
Sistema de control de versions distribuit que ens permet seguir l'historial de canvis i col·laborar. 
**Al BernatLab:** tot el projecte es versiona amb Git i allotjat a GitHub. 
Veure: capítols 9, 60.

### commit
Conjunt de canvis atòmic amb un missatge descriptiu. 
**Al BernatLab:** cada commit al repo segueix Conventional Commits. 
Veure: capítols 9, 60.

### branch
Línia independent de desenvolupament dins d'un repo Git. 
**Al BernatLab:** la `main` es la branca estable; treballem en `feat/xxx` i `fix/xxx`. 
Veure: capítols 9, 60.

### merge
Accio d'integrar els canvis d'una branca dins d'una altra. 
**Al BernatLab:** un PR es fusiona amb `merge commit` o `squash and merge` segons el cas. 
Veure: capitols 9, 60.

### PR (Pull Request)
Proposta de canvis d'una branca a una altra, amb revisio i discussio abans de fusionar. 
**Al BernatLab:** tot canvi al BernatLab passa per una PR amb revisio. 
Veure: capítols 9, 60.

### README
Primer fitxer que es mira d'un projecte: explica que es, com instal·lar-lo i com contribuir-hi. 
**Al BernatLab:** `bernatlab/README.md` es la porta d'entrada al projecte. 
Veure: capítols 9, 60.

### CHANGELOG
Fixer que recull els canvis significatius de cada versio. 
**Al BernatLab:** mantenim un `CHANGELOG.md` per a cada versio del BernatLab. 
Veure: capitol 9.

### LICENSE
Fixer que defineix els termes legals sota els quals es distribueix el projecte. 
**Al BernatLab:** el projecte es publica sota llicencia MIT. 
Veure: capitol 9.

### Markdown
Llenguatge de marcat lleuger que permet escriure text amb format (títols, llistes, enllaços, codi) llegible en pla i convertible a HTML. 
**Al BernatLab:** tots els capitols del llibre son fitxers Markdown. 
Veure: capítols 9, 38.

### YAML
Llenguatge de serialitzacio de dades molt usat en fitxers de configuracio. 
**Al BernatLab:** els nostres `docker-compose.yml` son YAML. 
Veure: capítols 5, 6, 61.

### TOML
Llenguatge de serialitzacio de dades, similar a YAML pero mes simple i consistent. 
**Al BernatLab:** alguns serveis (Vault, Pyproject) l'usen. 
Veure: capítols 5, 22.

### JSON
Veure l'entrada a Xarxa i connectivitat.

### GitHub Pages
Servei de GitHub que publica pagines web estatiques directament des d'un repo. 
**Al BernatLab:** la web publica del projecte es serveix desde GitHub Pages. 
Veure: capitols 9, 60.

### domini
Nom que identifica un lloc a Internet, com `bernatlab.cat`. 
**Al BernatLab:** tenim el domini `bernatlab.cat` registrat a un proveïdor. 
Veure: capítols 20, 44.

### DNS
Veure l'entrada a Xarxa i connectivitat.

### Cloudflare
Empresa que ofereix CDN, DNS, protecció DDoS i serveis d'optimitzacio web. 
**Al BernatLab:** Cloudflare gestiona el DNS de `bernatlab.cat` i ens fa de proxy invers gratuit. 
Veure: capítols 20, 44.

### CDN (Content Delivery Network)
Xarxa de servidors repartits pel mon que serveixen contingut estatic mes a prop de l'usuari. 
**Al BernatLab:** Cloudflare fa de CDN per a la web estàtica. 
Veure: capitol 20.

### HTTPS
Veure l'entrada a Xarxa i connectivitat.

---

## Hort Osona

### Sembra
Accio de posar llavors o planters a la terra per iniciar un cultiu. 
**Al BernatLab:** la sembra de tomàquets es fa al març en safates al viver. 
Veure: capítols 21, 32.

### Trasplantament
Pas de les plàntules del viver al seu lloc definitiu a l'hort. 
**Al BernatLab:** trasplantem els tomàquets a l'exterior a mitjans de maig. 
Veure: capítols 21, 32.

### Collita
Recol·leccio dels fruits o productes un cop madurs. 
**Al BernatLab:** la collita de tomàquets va de juliol a octubre. 
Veure: capítols 21, 32.

### Compost
Material organic descompost que s'afegeix a la terra per millorar-ne l'estructura i la fertilitat. 
**Al BernatLab:** fem compost amb restes de cuina i poda. 
Veure: capitol 21.

### Mulching
Cobriment del sol amb material organic (palla, fullatge, tela) per conservar humitat i evitar males herbes. 
**Al BernatLab:** apliquem mulching de palla als tomàquets. 
Veure: capitol 21.

### Rotacio de cultius
Practica de no plantar la mateixa familia de plantes al mateix lloc any rere any. 
**Al BernatLab:** rotem tomàquets, pebrot i albergínia en parcels diferents cada any. 
Veure: capitol 21.

### Plaga
Poblacio d'insectes o altres organismes que danya els cultius. 
**Al BernatLab:** la plaga mes habitual a Osona es el pugó. 
Veure: capítols 21, 32.

### Malaltia
Alteracio fisiologica de la planta causada per fongs, bacteris o virus. 
**Al BernatLab:** el mildiu i l'oïdi son les malalties mes comuns. 
Veure: capítols 21, 32.

### Tractament fitosanitari
Aplicacio d'un producte (biologic o quimic) per controlar plagues o malalties. 
**Al BernatLab:** prioritzem tractaments biologics (Bacillus thuringiensis, sabó potàssic). 
Veure: capitol 21.

### Conserva
Tecnica per guardar aliments mes enlla de la collita: conserva en vinagre, melmelada, confitat. 
**Al BernatLab:** fem conserva de tomàquet i pebrot cada setembre. 
Veure: capitol 21.

### Fermentacio
Transformacio d'un aliment per accio de microorganismes, que el conserva i en millora el sabor. 
**Al BernatLab:** fermentem col per fer sauerkraut i pebrots per fer ximixurri. 
Veure: capitol 21.

### Assecat
Tecnica de conservacio que elimina l'aigua de l'aliment per evitar-ne la degradacio. 
**Al BernatLab:** assequem herbes aromatiques i pebrot per a l'hivern. 
Veure: capitol 21.

### Calendari de plantacio
Taula que indica quan sembrar i trasplantar cada cultiu segons el clima local. 
**Al BernatLab:** el nostre calendari te en compte les gelades tardanes d'Osona. 
Veure: capítols 21, 32.

### Planificacio
Procés de decidir que plantarem, on i quan, tenint en compte rotacio, espai i temps. 
**Al BernatLab:** planifiquem l'hort cada hivern per a la temporada següent. 
Veure: capítols 21, 32.

### Osona
Comarca de Catalunya, al prepirineu, amb capital a Vic. 
**Al BernatLab:** l'hort del projecte es a Osona, amb un clima especific. 
Veure: capítols 21, 32.

### Prepirineu
Zona de transicio entre la plana i les muntanyes del Pirineu. 
**Al BernatLab:** Osona es considera prepirineu pel seu relleu suau. 
Veure: capitol 21.

### Altitud
Distancia vertical sobre el nivell del mar. Influeix en el clima i el calendari de cultiu. 
**Al BernatLab:** l'hort es a uns 550 m, cosa que retarda les sembres primaverals. 
Veure: capítols 21, 32.

### Clima
Conjunt de condicions meteorologiques habituals d'una zona. 
**Al BernatLab:** Osona te un clima continental humit amb hiverns freds i estius suaus. 
Veure: capítols 21, 32.

### Gelada
Temperatura sota zero que pot malmetre cultius sensibles. 
**Al BernatLab:** les gelades tardanes d'abril-maig son el risc principal. 
Veure: capítols 21, 32.

### Banc de llavors
Col·leccio de llavors conservades per a sembrar temporades futures. 
**Al BernatLab:** mantenim un banc de llavors de varietats locals. 
Veure: capitol 21.

### Hivernacle
Estructura que protegeix els cultius del fred i permet allargar la temporada. 
**Al BernatLab:** tenim un hivernacle petit per als planters. 
Veure: capitol 21.

### Reg
Subministrament d'aigua als cultius. 
**Al BernatLab:** el reg es controla per un actuador connectat al sistema. 
Veure: capítols 17, 18, 21.

### Substrat
Mescla de materials sobre la que creixen les plantes en testos o planters. 
**Al BernatLab:** usem substrat universal amb perlita per als planters. 
Veure: capitol 21.

---

## Termes generals

### Homelab
Conjunt de servidors i serveis que hom allotja a casa seva per aprendre, experimentar o cobrir necessitats personals. 
**Al BernatLab:** el projecte es un homelab complet al voltant d'una Raspberry Pi. 
Veure: capítols 1, 10, 51.

### Servidor
Ordinador que ofereix serveis a altres maquines o usuaris per xarxa. 
**Al BernatLab:** la Raspberry Pi fa de servidor de Grafana, Mosquitto, InfluxDB, etc. 
Veure: capítols 1, 3.

### Cloud
Conjunt de servidors allotjats en centres de dades de tercers, accessibles per Internet. 
**Al BernatLab:** fem servir cloud nomes per a coses puntuals (DNS, mirror de backups). 
Veure: capítols 1, 51.

### Contenidor
Veure l'entrada a Contenidors i Docker.

### Virtualitzacio
Tecnica que permet executar multiples "sistemes operatius convidats" sobre un sol sistema amfitrio amb un hipervisor. 
**Al BernatLab:** no la fem servir (preferim contenidors), pero entenem KVM i Proxmox. 
Veure: capítols 1, 5.

### Hipervisor
Programa que permet crear i executar maquines virtuals. Tipus 1 (bare-metal: Proxmox) o tipus 2 (host: VirtualBox). 
**Al BernatLab:** l'estudiem com a pas previ a Docker en el curs. 
Veure: capítols 1, 5.

### API
Veure l'entrada a Xarxa i connectivitat.

### CLI (Command Line Interface)
Interficie d'usuari basada en linia de comandes. 
**Al BernatLab:** tota l'operativa es fa per CLI (bash, docker, mosquitto_sub...). 
Veure: capítols 3, 5.

### GUI (Graphical User Interface)
Interficie grafica d'usuari, amb finestres, icones i ratoli. 
**Al BernatLab:** Portainer, Grafana i Homepage son GUI web que ens estalvien teclejar. 
Veure: capítols 3, 6, 19.

### TUI (Text-based User Interface)
Interficie d'usuari textual, com `htop`, `vim` o `curses`. 
**Al BernatLab:** `htop` per veure processos, `nano` per editar fitxers. 
Veure: capitol 3.

### Debug
Procés d'identificar i corregir errors en un programa o sistema. 
**Al BernatLab:** debuguem mirant logs, fent `docker exec` i usant `mosquitto_sub -t '#' -v`. 
Veure: capítols 3, 56.

### Log
Veure l'entrada a Monitoritzacio.

### Traça (stack trace)
Llista de crides de funcions que mostra on ha fallat un programa. 
**Al BernatLab:** Node-RED ens mostra traces quan un node falla. 
Veure: capítols 17, 56.

### Error
Esdeveniment que indica que algo no ha anat com esperavem. 
**Al BernatLab:** un error pot ser desde un avís (warning) fins a una fallada critica. 
Veure: capítols 17, 49, 56.

### Exception
Condicio anomala que interrompel'execucio d'un programa. 
**Al BernatLab:** capturem exceptions als nostres scripts per evitar que un error pari el backup. 
Veure: capitol 56.

### Documentacio
Conjunt de textos que expliquen com funciona un sistema, com instal·lar-lo, com usar-lo. 
**Al BernatLab:** la documentacio es al repo, al llibre i al wiki. 
Veure: capítols 9, 10, 55.

### Runbook
Document operatiu que descriu pas a pas com resoldre un problema o dur a terme una tasca. 
**Al BernatLab:** tenim runbooks per a "Restaura InfluxDB", "Recupera la Pi d'una fallada de SD", etc. 
Veure: capítols 55, 56, 68.

### Manual
Document d'us d'un sistema o aplicacio. 
**Al BernatLab:** el manual del BernatLab son els 69 capítols del llibre. 
Veure: capítols 9, 10.

### SOP (Standard Operating Procedure)
Procediment operatiu estandard: checklist per a una tasca repetitiva. 
**Al BernatLab:** SOP per a "Actualitzacio mensual del stack". 
Veure: capítols 22, 55.

### Comunitat
Grup de persones que comparteixen interessos i col·laboren. 
**Al BernatLab:** la comunitat oberta del projecte ens ajuda a millorar i documentar. 
Veure: capítols 9, 51.

### Contribucio
Accio d'afegir valor a un projecte, sovint com a codi o documentacio. 
**Al BernatLab:** tothom pot contribuir amb PRs, traduccions o noves fitxes d'hort. 
Veure: capítols 9, 51.

### Codi obert (open source)
Programari el codi font del qual es public i pot ser estudiat, modificat i redistribuit. 
**Al BernatLab:** tot el que fem servir (Docker, Grafana, InfluxDB, Mosquitto, Node-RED) es open source. 
Veure: capítols 9, 51.

### Llicencia
Document legal que defineix com es pot usar, modificar i redistribuir un programari. 
**Al BernatLab:** el projecte es publica sota MIT; la majoria d'eines que usem son Apache 2.0 o MIT. 
Veure: capitol 9.

### Fork
Copia d'un projecte que es desenvolupa de forma independent. 
**Al BernatLab:** un fork ens permet experimentar sense afectar el projecte principal. 
Veure: capítols 9, 60.

### Issue
Entrada al sistema de seguiment de tasques d'un repo (GitHub Issues, GitLab Issues). 
**Al BernatLab:** cada bug o millora te la seva issue a GitHub. 
Veure: capítols 9, 60.

### Roadmap
Planificacio temporal de les funcionalitats que es desenvoluparan en un projecte. 
**Al BernatLab:** el roadmap esta publicat al README i al capítol 10. 
Veure: capítols 10, 51.

### Stack
Conjunt de tecnologies que componen un sistema. 
**Al BernatLab:** el nostre stack es Raspberry Pi OS + Docker + Tailscale + Mosquitto + InfluxDB + Grafana. 
Veure: capítols 1, 5, 61.

### Tag (a Git o Docker)
Etiqueta que marca un punt a l'historial (Git) o una versio d'imatge (Docker). 
**Al BernatLab:** usem tags semantiques (v1.2.3) per a les releases del BernatLab. 
Veure: capítols 9, 60.

### Versio semantica (SemVer)
Esquema de numeracio MAJOR.MINOR.PATCH que indica tipus de canvis. 
**Al BernatLab:** v1.0.0 es la primera versio estable; v1.1.0 afegirà noves funcionalitats. 
Veure: capítols 9, 22.

### SLA
Veure l'entrada a Monitoritzacio.

### Uptime
Temps durant el qual un sistema esta operatiu. 
**Al BernatLab:** Grafana i Uptime Kuma ens permeten veure l'uptime de cada servei. 
Veure: capítols 7, 19, 62.

### Disponibilitat
Percentatge de temps que un sistema esta operatiu. 
**Al BernatLab:** objectiu del 99% mensual per al stack principal. 
Veure: capítols 7, 53, 67.

### Alta disponibilitat (HA)
Arquitectura que garanteix que un sistema segueix operatiu encara que falli algun component. 
**Al BernatLab:** avui dia no la tenim; en un futur, una replica passiva. 
Veure: capitol 22.

### DRP (Disaster Recovery Plan)
Pla de recuperacio davant desastres: que fer si ho perdem absolutament tot. 
**Al BernatLab:** el DRP inclou restaurar des d'un backup a una microSD nova. 
Veure: capítols 50, 69.

### RPO (Recovery Point Objective)
Quantitat maxima de dades que estem disposats a perdre, mesurada en temps. 
**Al BernatLab:** RPO de 24 h (backup diari). 
Veure: capítols 22, 50.

### RTO (Recovery Time Objective)
Temps maxim que estem disposats a trigar a recuperar el sistema. 
**Al BernatLab:** RTO de 4 hores per al stack principal. 
Veure: capítols 50, 69.

### Post-mortem
Document que analiza un incident passat per aprendre'n i evitar que es repeteixi. 
**Al BernatLab:** escrivim un post-mortem sempre que un servei cau mes d'una hora. 
Veure: capítols 50, 56.

### SRE (Site Reliability Engineering)
Disciplina que aplica enginyeria de software a la operativa de sistemes. 
**Al BernatLab:** ens n'inspiren els principis (SLOs, error budgets, runbooks). 
Veure: capítols 51, 53.

---

## Com contribuir

Si trobes a faltar un terme, una definicio o un enllaç, obre una PR a `bernatlab/book/glossari.md` amb:

1. La paraula nova o la correccio.
2. La definicio curta (1-3 frases) en catala.
3. Si tens, un exemple aplicat al BernatLab.
4. El numero de capitol on sha tractat (M1 a M7).

El glossari es viu: creix amb el projecte.

---

*Ultima revisio: generada automaticament a partir de l'estructura dels 69 capítols del BernatLab.*

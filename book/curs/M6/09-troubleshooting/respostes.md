# Respostes - Capitol 9: Troubleshooting

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Primer pas troubleshooting

**Resposta correcta**: Definir el problema exactament.

**Explicacio**: Abans de tocar res cal saber QUE falla. "La RPi no va" no es informacio. "La RPi no respon al ping desde el meu portatil pero si des d'un altre PC de la xarxa" si que es informacio. Com mes especificsiguis al definir el problema, mes rapid trobaras la solucio.

---

## Pregunta 2: Comanda processos

**Resposta correcta**: top o htop.

**Explicacio**: `top` es la comanda classica de Linux per veure processos en temps real. `htop` es una versio mes amigable amb colors, scroll, i millor visualitzacio. Ambdues mostren CPU%, memoria, temps, i el propietari del proces.

---

## Pregunta 3: Logs contenidor

**Resposta correcta**: `docker logs NOM`.

**Explicacio**: `docker logs` mostra stdout i stderr del contenidor. Es la primera cosa a fer quan un contenidor falla. Opcions utils: `--tail N` (ultimes N linies), `-f` (follow, com tail -f), `--since "1 hour ago"`.

---

## Pregunta 4: Temperatura RPi

**Resposta correcta**: `vcgencmd measure_temp`.

**Explicacio**: `vcgencmd` es la eina especifica de la Raspberry Pi per accedir a informacio del hardware. `measure_temp` llegeix el sensor de temperatura de la CPU. Tambe funciona llegir directament `/sys/thermal/thermal_zone0/temp` (el valor esta en mili-graus).

---

## Pregunta 5: Entrar en contenidor

**Resposta correcta**: `docker exec -it NOM /bin/bash`.

**Explicacio**: `docker exec` executa una comanda dins un contenidor en execucio. `-it` es per interactiu + terminal. Si el contenidor no te bash pots provar `/bin/sh`. La diferencia amb `docker attach` es que `attach` s'uneix al proces principal, mentre que `exec` obra un nou shell.

---

## Pregunta 6: Sistema lent

**Resposta correcta**: Identificar quin proces o servei consumeix mes recursos.

**Explicacio**: Abans d'actuar, cal saber ON esta el problema. Pot ser un proces que es torna boig, un contenidor amb fuita de memoria, la CPU fent throttling per calor, o el disc ple. Cada causa te una solucio diferent. Reiniciar nomes amaga el problema temporalment.

---

## Pregunta 7: Fitxer DNS

**Resposta correcta**: `/etc/resolv.conf`.

**Explicacio**: Aquest fitxer conte la configuracio dels servidors DNS que fa servir el sistema. Per exemple: `nameserver 8.8.8.8`. Es important saber-ho perque si tens problemes de DNS nomes, es aqui on has de mirar primer. Tambe pot ser un fitxer gestionat per systemd-resolved, en aquest cas veuras un link simbolic.

---

## Pregunta 8: Monitor complet

**Resposta correcta**: glances.

**Explicacio**: `glances` es una eina Python que mostra en una sola pantalla: CPU, memoria, swap, xarxa, disc, procesos, i fins i tot contenidors Docker. Es com un `top` esteroides. Pot funcionar en mode client-servidor per monitorar maquines remotes.

---

## Pregunta 9 (oberta): Metodologia de troubleshooting

**Resposta model**:

La **metodologia de troubleshooting** es un enfocament sistematic per resoldre problemes, en lloc de provar coses a l'atzar. Els passos son:

**1. Definir el problema exactament**

No acceptis "no funciona". Mira d'entendre QUE falla:
- "Home Assistant no es accessible des del navegador" (específic)
- "Els llums del menjador no es poden controlar" (molt específic)
- "Va molt lent" (poc específic, cal mes info)

Quant mes precís, mes rapid trobaras la solucio. Si la persona que t'ho explica no pot definir el problema, ajuda-la amb preguntes: "Quan ha passat? Que has fet abans? Es un error concret?"

**2. Recollir dades**

Abans de tocar res, mira el que tens:
- Logs del servei (`docker logs`)
- Metriques (`Grafana`, `htop`, `glances`)
- Estat del sistema (`docker ps`, `uptime`)
- Canvis recents: quina versio hi havia abans? Que has canviat?

**3. Identificar la capa**

On esta el problema?
- Capa fisica: te corrent? els cables?
- Capa hardware: la RPi s'escalfa massa? la microSD falla?
- Capa xarxa: arriba a la IP? els ports son oberts?
- Capa sistema: els serveis basics (docker, ssh) funcionen?
- Capa contenidors: tots els contenidors son UP?
- Capa aplicacio: el servei concret respon?

**4. Aillar la causa**

Un cop saps la capa, fes preguntes binaries:
- "Es la xarxa o el servei?" -> Prova amb ping
- "Es tots els serveis o nomes un?" -> Comprova altres contenidors
- "Es la RPi o la xarxa local?" -> Prova desde un altre PC
- "Ha canviat alguna cosa?" -> Mira el git log o el journal

**5. Aplicar la solucio**

Nomes UN canvi a la vegada. Si canvies 3 coses i tot funciona, no saps quina ha sigut la bona. Si nomes canvies 1 i funciona, saps exactament que fer la propera vegada.

**6. Verificar**

Ha tornat a funcionar? Es estable? Pot tornar a fallar en 5 minuts? Comprova-ho:
- Curl, ping, obre la UI, mira metricas
- Deixa passar temps per confirmar

**7. Documentar**

Escriu al runbook (cap 10) que ha passat. D'aqui 6 mesos, quan torni a passar, no hauras de redescobrir el problema.

**Per que NO s'ha de provar coses a l'atzar:**

1. **No saps que ha funcionat**: si toques 5 coses i tot va be, no saps quina ha sigut la bona. La propera vegada que falli, no recordes que fer.

2. **Pots crear nous problemes**: un canvi "innocent" pot tenir efectes secundaris. Si toques 5 coses i apareix un problema nou, no saps quin dels 5 canvis l'ha causat.

3. **Perds el temps**: sembla que "reinicieu i veieu que pasa" es rapid, pero si reinicies 5 vegades perque no trobes la solucio, has perdut 20 minuts quan amb un enfocament sistematic hauries trigat 5.

4. **No aprens**: el troubleshooting es habilitat que es millora amb la practica. Si nomes "tires coses a la paret", mai aprens els patrons reals dels problemes.

5. **Es perillos en produccio**: en un sistema 24/7 que serveix a altres persones, un canvi aleatori pot deixar el sistema fora de servei 30 minuts mentre reverteixes.

El bon troubleshooting es com la ciencia: observacio, hipotesi, experiment, verificacio. No es magia.

---

## Pregunta 10 (oberta): Diagnostic RPi no respon al ping

**Resposta model**:

Si la meva RPi no respon al ping, seguiria aquest ordre per identificar on esta la fallada:

**Pas 1: Verificar la capa fisica (30 segons)**

El mes basic: te corrent la RPi?
- Els LEDs de la RPi s'encenen? (LED vermell = corrent, LED verd = activitat)
- El cable USB-C de la font esta ben endollat?
- La font d'alimentacio funciona? (prova amb un altre carregador, minim 5V/3A)
- Si la RPi te ventilador, gira?

Si no te corrent, es problema de font d'alimentacio. Canvia-la o comprova el cable.

**Pas 2: Verificar la capa de xarxa (1 minut)**

Si la RPi te corrent pero no respon:
- El cable Ethernet esta ben connectat a la RPi i al router?
- Les llums del port Ethernet del router parpellegen? (si no, es el cable o el port)
- El router esta encès? (pot ser que el router s'hagi penjat)
- Prova amb WiFi si la RPi te (des d'un altre PC fes `ping 192.168.1.X` per veure si la xarxa funciona)

**Pas 3: Verificar la capa de hardware (1-2 minuts)**

Si la RPi te corrent pero no es veu a la xarxa:
- Connecta una pantalla per HDMI. Veus res? 
- Si veus text d'arranc o un missatge d'error, la RPi esta viva pero el SO falla.
- Si la pantalla esta negra, pot ser:
  - La microSD esta mal posada o falla
  - La RPi esta penjada en un bucle d'arranc
  - El sistema operatiu esta corrupte

**Pas 4: Verificar la capa de sistema operatiu (2-5 minuts)**

Si la RPi arranca i veus la consola:
- Arriba al login? Si no, pot ser el sistema de fitxers.
- Pots fer login amb usuari/contrasenya? Si no, pot ser un problema amb els usuaris o el password.
- Un cop dins, escriu `ip a` per veure si la RPi te IP assignada.
- Si no te IP, el DHCP falla. Reinicia la xarxa: `sudo systemctl restart networking`.

**Pas 5: Verificar la capa de servei (1 minut)**

Si tens acces per SSH pero el ping falla:
- El servei SSH esta corrent? `systemctl status ssh`
- El firewall bloqueja el ping? `sudo ufw status`
- Estic fent ping a la IP correcta? `ip a` per confirmar
- Altres PCs de la xarxa la veuen? Si nomes jo no, es el meu PC.

**Pas 6: Si tot falla, reaccio de panico (5-10 minuts)**

Si res funciona:
- Desendolla la RPi, espera 30 segons, reendolla
- Si continua igual, treu la microSD i posa-la en un altre PC. Es pot muntar? Te dades?
- Si la microSD esta corrupta, cal reinstal·lar (tens backup del cap 8, oi?)
- Si la microSD esta be pero la RPi no arranca, pot ser la propia RPi (hardware mort)

**Eines per a cada pas:**

| Pas | Eina principal | Eines secundaries |
|-----|----------------|-------------------|
| Fisica | Ulls, dit | Tester, multimentre |
| Xarxa | Cables | Router, switch |
| Hardware | HDMI + pantalla | LED, segon PC |
| Sistema | `journalctl` | Consola, ssh |
| Servei | `systemctl status` | `ss -tulnp` |

L'objectiu es anar descartant causes. Si trobes que "tinc corrent pero no veig res a la pantalla", ja saps que el problema es entre la font i la sortida de video. Si "tinc video pero no soc a la xarxa", es entre el kernel i el cable de xarxa. Cada descart t'acosta a la solucio.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici desde zero observant cada pas.
- **0-2 encerts**: Repassem junts el capitol abans de continuar.

## Que fer si has encertat totes

- Passa al **Capitol 10** (Runbooks avançats).
- Investiga `tcpdump` per capturar trafic de xarxa.
- Apren a fer un `strace` per seguir les crides al sistema d'un proces.

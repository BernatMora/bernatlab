# Respostes - Capitol 1: Amenaces comunes

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es un atac de bruteforce?

**Resposta correcta**: Un atac que prova milers de combinacions d'usuari i contrasenya automaticament.

**Explicacio**: Un atac de bruteforce es basa en la paciencia automatica. Un script proba "pi/1234", "pi/admin", "pi/raspberry", i aixi milers de combinacions per segon. Funciona nomes si la contrasenya es feble o si l'usuari es un nom per defecte conegut. Es per aixo que als capitols 2 i 3 veurem com protegir-nos amb Tailscale i deshabilitant el login per contrasenya.

---

## Pregunta 2: Port per defecte de SSH

**Resposta correcta**: 22.

**Explicacio**: El port 22 esta assignat oficialment a SSH per la IANA (Internet Assigned Numbers Authority) i l'usen tots els sistemes Unix des de fa decades. Els bots el coneixen perfectament, per canviar-lo (per exemple a 2222) redueix el soroll de scans automatic, pero NO es una mesura de seguretat per si sola. Ho veurem al capitol 3.

---

## Pregunta 3: Superficie d'atac

**Resposta correcta**: El conjunt de punts per on un atacant podria entrar al sistema.

**Explicacio**: Com mes superficie d'atac, mes oportunitats per a un atacant. Cada port obert, cada servei, cada usuari amb permis es un punt d'entrada potencial. L'objectiu de la seguretat es **reduir la superficie d'atac** al minim imprescindible: tancar ports, eliminar serveis no usats, usuaris amb el minim permis possible.

---

## Pregunta 4: Usuari mes atacat a la RPi

**Resposta correcta**: `pi`.

**Explicacio**: L'usuari `pi` es el compte per defecte de Raspberry Pi OS. Esta creat a totes les imatges oficials i es public a Internet. Si la teva RPi te l'usuari `pi` amb la contrasenya per defecte (`raspberry`), es qüestio de minuts que algú hi entri. **El primer que cal fer** es crear un altre usuari amb sudo, assignar-li una bona contrasenya, i desactivar `pi` (o canviar-li la contrasenya). Idealment, deshabilitar el login amb contrasenya i usar nomes claus SSH.

---

## Pregunta 5: Significat de CVE

**Resposta correcta**: Common Vulnerabilities and Exposures.

**Explicacio**: CVE es un sistema estandard per identificar vulnerabilitats de seguretat. Cada CVE te un numero (ex. CVE-2024-6387) i una descripcio tecnica. La base de dades publica es a https://cve.mitre.org/. Si saps quina versio d'un paquet tens, pots buscar si te CVEs coneguts i aplicar el pegat.

---

## Pregunta 6: Ordre per veure logins fallits

**Resposta correcta**: `sudo lastb`.

**Explicacio**: La comanda `lastb` (last bad) llegeix el fitxer `/var/log/btmp` que nomes registra intents de login fallits. Es una de les primeres coses que cal mirar en una auditoria. La comanda `last` (sense la b) llegeix `/var/log/wtmp` i mostra logins exitosos. Si tens un volum alt d'errors al `lastb`, es senyal que el servidor esta sent atacat.

---

## Pregunta 7: Per que es dolent exposar mes ports?

**Resposta correcta**: Perque cada port obert es un posible vector d'entrada per un atacant.

**Explicacio**: Cada port que escolta conexions es potencialment vulnerable: bugs al servei, configuracio incorrecta, contrasenyes febles. Si no necessites un servei, **tanca'l**. Si el necessites nomes localment, fes que escolti nomes a 127.0.0.1. Si el necessites remotament, posa'l darrere d'un firewall o VPN. Al BernatLab nomes hem d'exposar el que realment cal, i la resta queda nomes a la xarxa Tailscale.

---

## Pregunta 8: Eina dels atacants

**Resposta correcta**: nmap.

**Explicacio**: Nmap (Network Mapper) es l'eina de referencia per fer escanejos de xarxa. Es open source i la fan servir tant administradors legítims (per auditar) com atacants (per buscar victimes). Hi ha eines derivades com **masscan** (molt mes rapid) o **zmap** (escaneja tot Internet en minuts). L'analogia: nmap es com un lladre mirant totes les portes i finestres d'un carrer per veure quines son obertes.

---

## Pregunta 9 (oberta): Amenaces principals

**Resposta model**:

Al BernatLab les principals amenaces son les que venen d'Internet, perque la RPi esta exposada per Tailscale i, en alguns casos, per DDNS. Les classificaria en tres nivells.

**Risc alt**: atacs de bruteforce contra SSH. Es la porta d'entrada mes universal i tota RPi amb port 22 obert rep milers d'intents al dia. Si la contrasenya es feble o l'usuari es "pi", es molt probable que algú hi acabi entrant. També es risc alt tenir serveis Dockers amb credencials per defecte (Home Assistant amb admin/admin, Portainer sense contrasenya, etc.).

**Risc mitja**: exploits contra serveis web exposats. Si exposo Gitea, Home Assistant o Nextcloud directament a Internet (o a Tailscale sense autenticacio forta), qualsevol CVE recent podria comprometre el servei. També l'accés fisic: si algú pot tocar la RPi, pot apagar-la, robar-la, o ficar una SD maliciosa.

**Risc baix**: atacs dirigits personalitzats. No soc un objectiu prou interessant perque un atacant dediqui temps a un APT o un atac dirigit contra el BernatLab. Tampoc em preocupen els atacs interns (insiders) perque soc l'unic usuari. Finalment, el ransomware es mes aviat risc mitja: si entro en un enllaç sospitos, podria xifrar-me fitxers, pero tinc backups, aixi que la perdua de dades es limitada.

Aixo em porta a prioritzar: primer tancar SSH (canvi de port + claus), despres firewall, despres monitoratge. I totes aquestes defenses les veurem en aquest modul.

---

## Pregunta 10 (oberta): Defensa en profunditat

**Resposta model**:

La **defensa en profunditat** (defense in depth) es el principi que cap mesura de seguretat es suficient per si sola, i que cal superposar diverses capes perquè si una falla, les altres encara protegeixen. Es la mateixa logica que una caixa forta dins d'un cofre dins d'una habitacio amb porta blindada: si un lladre supera una barrera, en te una altra al davant.

**Per que cal?** Perque cap sistema es perfecte. Un firewall pot tenir un bug. Una contrasenya pot acabar filtrada. Un certificat TLS pot ser fals. Un atacant pot trobar una vulnerabilitat que no coneixies. Si nomes tens una capa, en el moment que falli, el sistema queda exposat. Si tens diverses, l'atacant ha de superar-les totes.

**Exemple concret al BernatLab**: imagina que nomes configures Tailscale i hi confies plenament. Si un dia Tailscale te una caiguda global (ja ha passat), o si una errada de configuracio deixa una ACL massa oberta, el servidor queda exposat. Pero si a mes tens firewall ufw, el firewall continua bloquejant ports. Si a mes tens SSH hardening (nomes claus), encara que el firewall falli, no podran entrar amb contrasenya. Si a mes tens monitoratge, t'assabentaras rapid.

Al llarg d'aquest modul construirem les capes següents: Tailscale (xarxa privada), ufw (firewall), SSH hardening (autenticacio forta), TLS (xifrat de tràfic), secrets (proteccio de credencials), backups xifrats (recuperacio), monitoratge (visibilitat), actualitzacions (reduccio de CVEs) i auditoria (verificacio periodica). Capa a capa, anirem fent el servidor mes robust.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici des de zero observant cada pas.
- **0-2 encerts**: Repassem junts el capitol abans de continuar.

## Que fer si has encertat totes

- Passa al **Capitol 2** (Tailscale ACLs).
- Investiga el projecte **Shodan**: un cercador d'Internet que mostra dispositius exposats. Busca "Raspberry Pi" i sorprendran els resultats.
- Mira els informes anuals de **Verizon DBIR** (Data Breach Investigations Report) per entendre quines son les amenaces mes reals al món.

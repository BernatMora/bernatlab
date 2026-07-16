# Respostes - Capitol 4: Firewall i ufw

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es un firewall?

**Resposta correcta**: Un programa que filtra el trafic de xarxa segons unes regles.

**Explicacio**: Un firewall es un sistema de control d'acces per a paquets de xarxa. Per cada paquet que entra o surt, mira una llista de regles i decideix si el deixa passar o el rebutja. Les regles es basen en IP, port, protocol i interficie. Es la primera barrera tecnica entre la xarxa publica i el teu sistema.

---

## Pregunta 2: Deny-by-default

**Resposta correcta**: Tot esta bloquejat per defecte; nomes es permet el que explicitem obrim.

**Explicacio**: Aquesta es la postura mes segura. Si deixes passar tot per defecte i nomes bloqueges el que recordes, acabaras obrint mes del compte. Al contrari, si tanques tot per defecte i obres nomes el que necessites, tens control absolut. La regla: "el que no esta permes, esta prohibit".

---

## Pregunta 3: Que es ufw?

**Resposta correcta**: Un wrapper d'iptables/nftables amb sintaxi senzilla.

**Explicacio**: ufw (Uncomplicated Firewall) es una eina de Canonical (els d'Ubuntu) que permet definir regles de firewall amb comandes simples. Per sota, genera regles d'iptables o nftables. Es la opcio recomanada per a servidors petits: te la potencia d'iptables sense la complexitat.

---

## Pregunta 4: Permetre un port

**Resposta correcta**: `sudo ufw allow 22/tcp`.

**Explicacio**: La sintaxi es molt natural: `allow` per permetre, `deny` per denegar, seguit del port i el protocol. Tambe es pot fer `sudo ufw allow ssh` i ufw sabra que vols dir el port 22. Per defecte, si no poses protocol, assumeix TCP i UDP (a vegades nomes vols un). Sigues explícit: millor `22/tcp`.

---

## Pregunta 5: tailscale0

**Resposta correcta**: La interficie de xarxa virtual que Tailscale crea.

**Explicacio**: Quan Tailscale arranca, crea una interficie de xarxa anomenada `tailscale0` amb una IP del rang 100.x.y.z. Es com si fos una tarja de xarxa virtual. El sistema la veu com qualsevol altra interficie, per tant pots fer regles de firewall especifiques per a ella: nomes el trafic que entra per aquesta interficie pot arribar a certs ports.

---

## Pregunta 6: Veure les regles

**Resposta correcta**: `sudo ufw status verbose` o `sudo ufw status numbered`.

**Explicacio**: `status` mostra les regles actives. `verbose` afegeix informacio de la politica per defecte. `numbered` enumera cada regla, cosa que es molt util per poder-les esborrar amb `sudo ufw delete 3`. Si vols veure les regles reals (no les de ufw), mira `sudo iptables -L -n` o `sudo nft list ruleset`.

---

## Pregunta 7: default allow incoming

**Resposta correcta**: Tots els ports queden accessibles des de qualsevol xarxa, com si no tinguesis firewall.

**Explicacio**: Si canvies la politica per defecte a `allow incoming`, el firewall no filtra res: tot el que arriba es deixa passar. Es equivalent a tenir-lo desactivat. Es una configuracio perillosa. Sempre `deny incoming` per defecte.

---

## Pregunta 8: Permetre nomes desde Tailscale

**Resposta correcta**: `sudo ufw allow in on tailscale0`.

**Explicacio**: Aquesta regla vol dir: "permet trafic que entra per la interficie tailscale0". Combinat amb una regla de denegacio per defecte, nomes Tailscale pot accedir. Es pot especificar tambe el port: `sudo ufw allow in on tailscale0 to any port 22`. Es la combinacio guanyadora amb Tailscale.

---

## Pregunta 9 (oberta): Regles pel BernatLab

**Resposta model**:

Aquestes son les regles que jo aplicaria al BernatLab. Assumeixo que la RPi te Tailscale instal·lat i que el port SSH es el 22 (o el 5022 si has seguit el capitol 3). L'objectiu es tancar tot el que no cal i obrir nomes el que realment necessito.

```bash
# Primer: politica per defecte
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Segon: SSH nomes desde Tailscale
sudo ufw allow in on tailscale0 to any port 22 proto tcp comment "SSH via Tailscale"

# Tercer: Web (HTTP + HTTPS) nomes desde Tailscale
sudo ufw allow in on tailscale0 to any port 80 proto tcp comment "HTTP via Tailscale"
sudo ufw allow in on tailscale0 to any port 443 proto tcp comment "HTTPS via Tailscale"

# Quart: si vull exposar un servei a Internet (per exemple, per un reverse proxy)
# nomes obro a Internet el que realment cal
# sudo ufw allow 443/tcp comment "HTTPS public per Nextcloud"

# Cinque: DNS nomes per Tailscale (MagicDNS)
sudo ufw allow in on tailscale0 to any port 53 comment "DNS via Tailscale"

# Sise: Home Assistant nomes per Tailscale
sudo ufw allow in on tailscale0 to any port 8123 proto tcp comment "Home Assistant via Tailscale"

# Sete: Gitea nomes per Tailscale
sudo ufw allow in on tailscale0 to any port 3000 proto tcp comment "Gitea via Tailscale"

# Vuite: activar
sudo ufw enable

# Nou: verificar
sudo ufw status verbose
```

Per que cada regla es important:

- **`default deny incoming`**: per defecte, tot esta tancat. Si un servei nou escolta un port, no es accessible fins que una regla ho permeti explicitament. Es la postura mes segura.
- **`allow in on tailscale0 ... port 22`**: SSH nomes per Tailscale. Si la teva xarxa Tailscale es compromesa, nomes tens l'usuari Tailscale com a superficie d'atac. Si vols encara mes seguretat, pots fer servir una etiqueta: nomes els teus portatils etiquetats com `tag:personal` poden accedir.
- **`allow in on tailscale0 ... port 80/443`**: el web nomes des de Tailscale. Si mai vols exposar-ho a Internet, hauras d'afegir una regla `allow 443/tcp` (sense la condicio de tailscale0).
- **Com canviar les regles si cal**: `sudo ufw delete 3` esborra la regla numero 3, o `sudo ufw delete allow 22/tcp` l'esborra per nom.

---

## Pregunta 10 (oberta): Tailscale + ufw

**Resposta model**:

Podries pensar: si Tailscale ja amaga el servidor, per que cal tambe un firewall local? La resposta es **defensa en profunditat**. Son dos capes diferents que protegeixen contra amenaces diferents.

**Tailscale** actua a nivell de xarxa publica. Fa que el port 22 no estigui exposat a Internet: cap persona aliena a la teva xarxa Tailscale pot ni intentar connectar-s'hi. Pero nomes filtra a nivell de xarxa. Si algú entra a la teva xarxa Tailscale (per exemple, robant-te les credencials o un dels teus dispositius), pot accedir a **tots els serveis** que escolten a la maquina.

**ufw** actua a nivell local. Encara que la xarxa Tailscale estigui compromesa, ufw pot limitar quin port pot fer què. Per exemple, puc fer que nomes jo (`tag:personal`) pugui accedir a SSH, o que Portainer nomes sigui accessible desde la xarxa local. Son dues capes amb responsabilitats diferents.

Un altre motiu: **bugs i caigudes**. Tailscale te SLA, pero pot tenir caigudes. Si Tailscale cau i, en un reinici, deixa temporalment algun port obert a Internet abans que es torni a connectar, el firewall local es la salvaguarda. Aixo ha passat real.

Tambe: **errades de configuracio**. Si un dia configures accidentalment un servei (com una base de dades) per escoltar a `0.0.0.0` en lloc de `127.0.0.1`, estara accessible des de qualsevol xarxa. Amb Tailscale nomes, es accessible des de Tailscale. Amb ufw nomes, es accessible des d'Internet. Amb **les dues juntes**, ufw pot bloquejar aquesta errada i pots veure-ho als logs.

Finalment: **segmentacio de serveis**. Amb ufw pots fer que Home Assistant (8123) nomes escolti a Tailscale, pero que la base de dades InfluxDB (8086) nomes escolti a la interficie local (127.0.0.1). Aixi, encara que Home Assistant sigui compromes, l'atacant no pot accedir a la base de dades. Aixo es **microsegmentacio**, i ufw es l'eina per fer-la.

Per tant: Tailscale es la primera barrera (amaga), ufw es la segona (segmenta). No son redundants, son complementaries. Si nomes en tens una, deixa l'altra exposada a un risc innecessari.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici amb un entorn de proves.
- **0-2 encerts**: Practica amb ufw en una maquina virtual abans de tocar la RPi.

## Que fer si has encertat totes

- Passa al **Capitol 5** (TLS i certificats).
- Investiga **nftables directament** (sense ufw) per entendre quines regles es generen.
- Apren sobre **port knocking**: una tecnica per obrir ports nomes quan els toques en un ordre concret.
- Prova **gufw**: la interficie grafica de ufw.

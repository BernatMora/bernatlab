# Qüestionari - Capitol 1: Amenaces comunes al servidor

> 15 preguntes · ~20 min · 7 test + 8 obertes

## Pregunta 1
Que es la "superficie d'atac"?

- [ ] La mida del servidor
- [x] El conjunt de punts per on un atacant podria entrar al sistema
- [ ] El numero d'atacs que rep el servidor
- [ ] La versio del sistema operatiu

## Pregunta 2
Quin es el perill numero 1 al BernatLab?

- [ ] El correu brossa
- [x] Els atacs de bruteforce a SSH
- [ ] Els virus
- [ ] El sobreescalfament

## Pregunta 3
Que es un atac de "bruteforce"?

- [ ] Un atac amb forca bruta fisica al servidor
- [x] Provar milers de combinacions d'usuari i contrasenya fins encertar
- [ ] Un atac que sobrecarrega el servidor
- [ ] Un atac amb virus

## Pregunta 4
Quin usuari es el mes atacat pels bots?

- [ ] bernat
- [x] root, pi, admin (els noms per defecte)
- [ ] guest
- [ ] Els bots no miren l'usuari

## Pregunta 5
Que fa un "port scan" (nmap)?

- [ ] Esborra tots els ports oberts
- [x] Mira quins serveis escolten a quins ports
- [ ] Tanca els ports no segurs
- [ ] Activa el firewall

## Pregunta 6
Quin servei es el mes critic de protegir?

- [ ] HTTP
- [x] SSH (port 22) perque dona acces a la consola
- [ ] DNS
- [ ] MQTT

## Pregunta 7
Que es el "credential stuffing"?

- [ ] Omplir credencials en una base de dades
- [x] Usar combinacions email+contrasenya que han fugit d'altres incidents
- [ ] Guardar credencials en un fitxer
- [ ] Comprimir credencials

## Pregunta 8 (oberta)
Explica amb les teves paraules: que es la "superficie d'atac" i per que es important minimitzar-la? Posa exemples concrets del BernatLab.

Pistes per respondre:
- Cada port obert es un possible punt d'entrada.
- Cada servei exposat es un risc.
- Minimitzar = tancar el que no es necessari.
- Al BernatLab: SSH nomes a Tailscale, serveis interns sense exposar.

## Pregunta 9 (oberta)
Per que creus que hi ha bots que escanegen totes les IPs d'Internet constantment? Que busquen i que fan quan troben una maquina vulnerable?

Pistes per respondre:
- Busquen maquines amb serveis exposats i versions antigues amb vulnerabilitats conegudes.
- Si troben SSH, proven contrasenyes febles.
- Si troben una versio vulnerable, intenten explotar-la.
- Alguns son "research" (Mesura de la Internet), d'altres son criminals.

## Pregunta 10 (oberta)
Imagina que la teva RPi te el port 22 obert a Internet amb contrasenya feble ("raspberry"). Segueix el flux complet d'un atac: des de que el bot troba la maquina fins que entra.

Pistes per respondre:
- Pas 1: nmap troba port 22 obert.
- Pas 2: bruteforce amb llistes de contrasenyes comunes.
- Pas 3: troba la contrasenya "raspberry".
- Pas 4: accedeix al sistema.
- Pas 5: intenta escalar privilegis (sudo, su, etc.).
- Pas 6: instal·la un backdoor o un miner de criptomonedes.

## Pregunta 11 (oberta)
Quina relacio hi ha entre tenir Tailscale i la seguretat del servidor? Tailscale ens fa inmunes a tots els atacs?

Pistes per respondre:
- Tailscale amaga el servidor a Internet: els bots no el veuen.
- Pero si Tailscale falla o les ACLs son permissives, el risc continua.
- Tailscale no substitueix bones contrasenyes, firewall, etc.
- Es una capa mes, no la unica.

## Pregunta 12 (oberta)
Descriu 3 tipus d'atac comuns a un servidor exposat a Internet i quina es la millor defensa per a cadascun.

Pistes per respondre:
- Atac 1: SSH bruteforce -> defensa: claus + fail2ban.
- Atac 2: port scan -> defensa: tancar ports no usats.
- Atac 3: exploit de versio vulnerable -> defensa: actualitzar regularment.
- Cadascun te una defensa especifica.

## Pregunta 13 (oberta)
Com detectaries que el teu servidor esta sent atacat? Quins senyals et posarien en alerta?

Pistes per respondre:
- Senyal 1: molts logins fallits a SSH (veure amb `journalctl`).
- Senyal 2: CPU alta sense causa evident (possible miner de cripto).
- Senyal 3: trafic de xarxa anormal.
- Senyal 4: fitxers nous que no reconeixes.
- Eines: fail2ban, portsentry, auditd.

## Pregunta 14 (oberta)
Quin impacte te un atac reeixit al BernatLab? Pensa en les consequencies mes enlla del servidor: dades personals, hort, reputacio.

Pistes per respondre:
- Impacte 1: perdua de dades personals.
- Impacte 2: control remot de l'hort (modificar regs, etc.).
- Impacte 3: el servidor pot fer atacs a tercers (botnet).
- Impacte 4: pèrdua economica (si hi ha transaccions).
- Impacte 5: perdua de reputacio si es fa public.

## Pregunta 15 (oberta)
Argumenta la teva estrategia: quines son les 3 mesures de seguretat que aplicaries PRIMER al BernatLab abans d'obrir-lo a Internet? Justifica l'ordre.

Pistes per respondre:
- Mesura 1: Tailscale (amaga el servidor).
- Mesura 2: SSH amb claus (no contrasenyes).
- Mesura 3: firewall (ufw, deny-by-default).
- Aplica mesura per mesura, no totes de cop.
- Verificar que cada mesura funciona.

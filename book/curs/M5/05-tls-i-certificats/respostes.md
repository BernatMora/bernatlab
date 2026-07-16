# Respostes - Capitol 5: TLS i certificats

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que fa TLS?

**Resposta correcta**: Xifra la comunicacio entre client i servidor.

**Explicacio**: TLS (Transport Layer Security) es el protocol que hi ha darrere del HTTPS. Permet que client i servidor intercanviin informacio de forma xifrada, de manera que un atacant que escolti la xarxa nomes vegi bytes aleatoris, no el contingut. A mes, el certificat del servidor permet al client verificar la seva identitat.

---

## Pregunta 2: Que es un certificat digital?

**Resposta correcta**: Un document electronic que associa una identitat amb una clau publica, firmat per una CA.

**Explicacio**: Un certificat digital es com un DNI electronic. Conte la clau publica del servidor i l'identitat (el domini). Esta firmat per una autoritat de certificacio (CA) de confianca, cosa que permet als navegadors verificar que el certificat es legitim. Sense aquesta cadena de confianca, no podriem saber si el servidor es realment qui diu ser.

---

## Pregunta 3: Que es Let's Encrypt?

**Resposta correcta**: Una autoritat de certificacio que dona certificats TLS gratuits.

**Explicacio**: Let's Encrypt es una CA sense anim de lucre, mantinguda per la Internet Security Research Group. Emet mes del 80% dels certificats HTTPS del mon. Es gratuita, automatitzada, i oberta. Va ser creada precisament per fer que HTTPS fos universal. No tots els navegadors la reconeixen per defecte, pero si els mes moderns.

---

## Pregunta 4: Validesa dels certificats

**Resposta correcta**: 90 dies.

**Explicacio**: Let's Encrypt dona certificats valids durant 90 dies, no 1 o 2 anys com abans. La raon es tecnica: si un certificat es compromet, nomes esta exposat durant 3 mesos. La bona noticia es que la renovacio es totalment automatitzada (un certbot renew n'hi ha prou), per tant no cal que hi pensis. Es un bon model perque et forca a tenir automatitzacio.

---

## Pregunta 5: Que es Caddy?

**Resposta correcta**: Un servidor web modern que configura TLS automaticament.

**Explicacio**: Caddy es un servidor web escrit en Go que destaca per la seva senzillesa. Si tens un domini apuntant al servidor, nomes cal posar-lo al Caddyfile i Caddy sol·licita i renova el certificat de Let's Encrypt nomes. Es ideal per homelabs perque redueix la complexitat. L'equivalent manual amb Nginx requereix mes feina de configuracio.

---

## Pregunta 6: Eina estandard

**Resposta correcta**: certbot.

**Explicacio**: Certbot es l'eina oficial de l'EFF (Electronic Frontier Foundation) per obtenir certificats de Let's Encrypt. Esta disponible a totes les distribucions Linux. Admet plugins per a Nginx, Apache i altres, que configuren el servidor web automaticament. Alternatives: acme.sh, lego, dehydrated. Totes son clients ACME, pero certbot es el mes popular.

---

## Pregunta 7: Certificat auto-signat

**Resposta correcta**: Un certificat firmat per la propia maquina, no per una autoritat de confianca.

**Explicacio**: Un certificat auto-signat es un que el servidor ha creat i firmat ell mateix. El trafic va xifrat igualment, pero com que cap CA externa el valida, els navegadors mostren un avís. Es valid per a entorns controlats (xarxes privades, proves, IoT). A Tailscale, pots obtenir un certificat firmat per la CA del tailnet, que es mes elegant.

---

## Pregunta 8: TLS minim acceptable

**Resposta correcta**: TLS 1.2.

**Explicacio**: TLS 1.0 i 1.1 tenen vulnerabilitats conegudes (BEAST, POODLE, etc.) i ja no es consideren segurs. El minim acceptable avui es TLS 1.2, i l'ideal es nomes TLS 1.3. Configura sempre `ssl_protocols TLSv1.2 TLSv1.3;` al Nginx. SSL 3.0 esta totalment obsolet.

---

## Pregunta 9 (oberta): HTTPS amb Let's Encrypt

**Resposta model**:

Per configurar HTTPS gratuit al BernatLab amb un domini propi, faria aixo pas a pas. Assumeixo que tinc `bernatlab.cat` apuntant a la IP publica de la RPi.

**Pas 1: Assegurar el domini**. Comprovar que el DNS esta correctament configurat:

```bash
dig bernatlab.cat +short
# Ha de retornar la IP publica
```

**Pas 2: Instal·lar certbot**.

```bash
sudo apt install certbot
```

**Pas 3: Triar el servidor web**. Entre Nginx i Caddy:

- **Caddy**: mes simple, TLS automatic. Recomanat si no tens experiencia. 
- **Nginx**: mes flexible, mes opcions. Recomanat si ja el coneixes.

Si trio Caddy, nomes cal:

```bash
sudo apt install caddy
```

I un Caddyfile:

```caddyfile
bernatlab.cat {
    reverse_proxy localhost:8123
}
```

Caddy sol·licita el certificat, el configura, i el renova automaticament. Magia pura.

Si trio Nginx:

```bash
sudo apt install nginx python3-certbot-nginx
sudo certbot --nginx -d bernatlab.cat
# Et fa totes les preguntes
```

**Pas 4: Verificar**. Des del navegador:

- Obre `https://bernatlab.cat`.
- Comprova el cadenat.
- A les dev tools (F12), veuras que la connexio es TLS 1.3.

**Pas 5: Renovacio automatica**.

```bash
# Comprova que el timer funciona
sudo systemctl status certbot.timer
sudo certbot renew --dry-run
```

**Pas 6: Proves externes**. Un cop configurat, analitza el servidor a:

- https://www.ssllabs.com/ssltest/ (analisi complet, gratis).
- O utilitza testssl.sh des de la linia de comandes.

El resultat hauria de ser una nota A o A+. Si tens B o C, toca revisar la configuracio: tens xifratges antics activats o OCSP Stapling no configurat.

---

## Pregunta 10 (oberta): HTTPS nomes per Tailscale

**Resposta model**:

Quan treballes amb serveis accessibles **nomes** per Tailscale, la gestio de TLS es diferent. El trafic ja va xifrat per WireGuard, per tant la capa TLS es **redundant** en quant a confidencialitat. Pero encara volem TLS per:

- **Autenticacio del servidor**: el client pot verificar que es connecta al servidor correcte.
- **Comoditat**: alguns clients (Home Assistant, app mobils) volen veure un certificat valid.
- **Compatibilitat**: alguns navegadors moderns exigeixen HTTPS per certes funcionalitats.

Tenim tres opcions:

**Opcio 1: HTTP pla (sense TLS)**. Es acceptable si:

- L'aplicacio nomes s'accedeix per Tailscale.
- L'aplicacio ja te autenticacio propia (usuari + contrasenya).
- No hi ha dades especialment sensibles.

Es la opcio mes simple. Per exemple, Portainer nomes per Tailscale pot ser nomes HTTP al port 9000.

**Opcio 2: Certificat auto-signat**. Utilitza `openssl` per generar un certificat. El trafic va xifrat, pero el navegador mostrara un avís. Per evitar l'avís, els usuaris poden afegir manualment el certificat a la llista de confiansa del sistema operatiu.

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

**Opcio 3: Certificat de Tailscale (la millor)**. Tailscale distribueix una CA privada que tots els dispositius del tailnet confien. Pots obtenir un certificat firmat per aquesta CA:

```bash
tailscale cert
# Et dona el certificat per raspberry.tailnet-xxxx.ts.net
```

Aquest certificat funciona transparentment: cap avís de seguretat, xifrat modern, renovacio automatica. Es l'opcio ideal per serveis nomes-Tailscale.

**Exemple practic**: a la RPi, tinc Gitea nomes per Tailscale. Faig:

```bash
sudo tailscale cert gitea.bernatlab.ts.net
# Em dona gitea.bernatlab.ts.net.crt i .key
# Els poso a /etc/ssl/tailscale/
```

Ara el client de Gitea al portatil confia implicitament. Si intento accedir-hi des d'un dispositiu que no te Tailscale, simplement no pot. Si accedeixo des d'un amb Tailscale, veig el cadenat verd. Es la millor de les dues opcions.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Repeteix l'exercici provant almenys dues opcions (Nginx + Caddy).
- **0-2 encerts**: Comença per configurar un proxy invers basic sense TLS, afegeix TLS despres.

## Que fer si has encertat totes

- Passa al **Capitol 6** (Secrets i variables).
- Configura una **pipeline CI** que renovi els certificats automaticament.
- Investiga **OCSP Must-Staple** per millorar la validacio de revocacio.
- Llegeix sobre **HPKP** (HTTP Public Key Pinning), encara que esta obsolet.

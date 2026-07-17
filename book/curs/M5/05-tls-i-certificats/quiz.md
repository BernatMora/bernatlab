# Qüestionari - Capitol 5: TLS i certificats

> 10 preguntes · ~15 min

## Pregunta 1
Que fa TLS?

- [ ] Tradueix noms de domini a IPs
- [x] Xifra la comunicacio entre client i servidor
- [ ] Comprova que la contrasenya es correcta
- [ ] Optimitza la velocitat de la xarxa

## Pregunta 2
Que es un certificat digital?

- [ ] Un document que demostra que tens un bon antivirus
- [x] Un document electronic que associa una identitat amb una clau publica, firmat per una CA
- [ ] Un tipus de DNS
- [ ] Un protocol de xarxa

## Pregunta 3
Que es Let's Encrypt?

- [ ] Un antivirus gratuit
- [x] Una autoritat de certificacio que dona certificats TLS gratuits
- [ ] Un servei de correu segur
- [ ] Un sistema operatiu

## Pregunta 4
Quant de temps es valid un certificat de Let's Encrypt?

- [ ] 1 any
- [ ] 3 anys
- [x] 90 dies
- [ ] 5 anys

## Pregunta 5
Que es Caddy?

- [ ] Un joc de cartes
- [x] Un servidor web modern que configura TLS automaticament
- [ ] Un sistema de backups
- [ ] Un tipus de certificat

## Pregunta 6
Quina eina es l'estandard per obtenir certificats de Let's Encrypt?

- [ ] openssl
- [ ] acme.sh
- [x] certbot
- [ ] nginx

## Pregunta 7
Que vol dir un certificat "auto-signat"?

- [ ] Un certificat que el servidor ha firmat ell mateix, sense una CA
- [x] Un certificat firmat per la propia maquina, no per una autoritat de confianca
- [ ] Un certificat nomes per a servidors petits
- [ ] Un certificat que es renova automaticament

## Pregunta 8
Quin protocol de TLS es el minim acceptable avui dia?

- [ ] TLS 1.0
- [ ] TLS 1.1
- [x] TLS 1.2
- [ ] SSL 3.0

## Pregunta 9 (oberta)
Descriu els pasos per configurar HTTPS gratuit al BernatLab amb un domini propi. Inclou l'obtencio del certificat i la configuracio del servidor web.

Pistes per respondre:
- Primer necessites un domini apuntant a la IP publica de la RPi.
- Instal·la certbot.
- Genera el certificat amb `certbot certonly --standalone` o `--nginx`.
- Configura el servidor web (Nginx o Caddy) per usar-lo.
- Activa la renovacio automatica.
- Esmenta quin servidor web triaries i per que.

## Pregunta 10 (oberta)
Com gestionaries HTTPS per a serveis que nomes son accessibles via Tailscale? Cal certificat public?

Pistes per respondre:
- Dins de Tailscale, el trafic ja esta xifrat per WireGuard.
- Pots fer servir certificats auto-signats o la CA de Tailscale.
- Explica quan NO cal Let's Encrypt.
- Dona un exemple amb `tailscale cert`.


## Pregunta 11
Per que es important tenir HTTPS nomes a dins de la teva xarxa Tailscale? No cal TLS si ja soc jo?

**Pistes**: Pistes: Defensive in depth, atac intern, malware, sniff, futur.

## Pregunta 12
Explica que es un certificat auto-signat i quan pot ser acceptable.

**Pistes**: Pistes: Cost, facil, navegador avisa, xarxa privada.

## Pregunta 13
Quina relacio hi ha entre la validesa dun certificat i la seguretat? Pensa en 1 any, 5 anys, 10 anys.

**Pistes**: Pistes: Renovacio, canvis, revocacio, atac.


## Pregunta 14 (oberta amb pistes)
Per que es important tenir HTTPS nomes a dins de la teva xarxa Tailscale

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
## Pregunta 15 (oberta amb pistes)
Explica que es un certificat auto-signat i quan pot ser acceptable

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).

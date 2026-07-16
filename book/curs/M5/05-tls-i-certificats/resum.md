# Resum - Capitol 5: TLS i certificats

## La idea clau

Quan navegues per HTTP, el contingut viatja en text pla: qualsevol que escolti a la xarxa pot llegir-lo. **TLS** (antic SSL) es el protocol que xifra la comunicacio entre el navegador i el servidor, de manera que nomes ells dos poden entendre el que es diuen. Per fer-ho, el servidor necessita un **certificat digital**: un document que demostra la seva identitat. Al BernatLab usarem **Let's Encrypt** per obtenir certificats gratuits i **Caddy** o **Nginx** com a servidor web que gestiona el TLS.

## Que es TLS

**TLS** (Transport Layer Security), abans conegut com SSL, es el protocol que dona la "S" a HTTPS. Funciona en dos passos:

1. **Handshake**: el client i el servidor intercanvien informacio i acorden un metode de xifratge.
2. **Comunicacio xifrada**: tot el que es diu a partir d'ara es xifrat amb una clau simetrica derivada del handshake.

Gracies a TLS:

- **Confidencialitat**: ningú pot llegir el contingut.
- **Integritat**: ningú pot modificar el contingut sense que es detecti.
- **Autenticacio**: el client pot verificar que el servidor es qui diu ser.

## Que es un certificat digital

Un certificat digital es un document electronic que associa una **identitat** (un domini, com `bernatlab.cat`) amb una **clau publica**. Esta signat per una **autoritat de certificacio** (CA), que es una entitat de confianca (Let's Encrypt, DigiCert, etc.). Quan el navegador veu que el certificat esta firmat per una CA coneguda, confia que el servidor es realment qui diu ser.

Un certificat conte:

- **Subject**: el domini (CN) o dominis (SAN).
- **Issuer**: qui l'ha firmat.
- **Validity**: des de quan i fins quan es valid.
- **Public key**: la clau publica del servidor.
- **Signature**: la firma digital de la CA.

## Tipus de certificats

Hi ha tres tipus principals:

- **DV (Domain Validation)**: nomes verifica que controles el domini. Let's Encrypt nomes dona aquests. Es el minim necessari per HTTPS.
- **OV (Organization Validation)**: a mes, verifica que l'organitzacio existeix. Per a empreses.
- **EV (Extended Validation)**: verificacio maxima. La barra del navegador surt verda (anticament). Cada vegada menys comu.

Al BernatLab, **DV** es mes que suficient.

## Let's Encrypt: certificats gratuits

**Let's Encrypt** es una autoritat de certificacio gratuita i automatica, mantinguda per la Internet Security Research Group (ISRG). Permet obtenir i renovar certificats TLS sense cost.

L'eina standard per obtenir certificats es **Certbot**:

```bash
sudo apt install certbot

# Obtenir un certificat (cal tenir el domini apuntant al servidor)
sudo certbot certonly --standalone -d bernatlab.cat -d www.bernatlab.cat

# Amb Nginx ja funcionant
sudo certbot certonly --nginx -d bernatlab.cat

# Els certificats es guarden a
ls /etc/letsencrypt/live/bernatlab.cat/
# cert.pem     chain.pem    fullchain.pem    privkey.pem
```

Els certificats son valids **90 dies**, pero es poden renovar automaticament:

```bash
# Prova la renovacio
sudo certbot renew --dry-run

# Activar la renovacio automatica amb cron
echo "0 3 * * * certbot renew --quiet" | sudo tee -a /etc/cron.d/certbot-renew
```

## Caddy: el servidor web automatic

**Caddy** es un servidor web modern que configura TLS automaticament. Si tens un domini apuntant al servidor, nomes cal posar:

```caddyfile
bernatlab.cat {
    reverse_proxy localhost:8123
}
```

Caddy obtindra el certificat, el renovara automaticament i configurara TLS nomes. Es magic.

Instal·lacio:

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/caddy-stable-archive-keyring.gpg] https://dl.cloudsmith.io/public/caddy/stable/deb/debian any-version main" | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
```

Configuracio a `/etc/caddy/Caddyfile`:

```caddyfile
bernatlab.cat {
    reverse_proxy localhost:8123
}

gitea.bernatlab.cat {
    reverse_proxy localhost:3000
}
```

```bash
sudo systemctl reload caddy
```

## Nginx: mes flexible pero mes manual

**Nginx** es el mes popular. Es mes flexible pero cal configurar TLS a ma. Cal tenir el certificat i la clau a lloc segur, i configurar un servidor HTTPS:

```nginx
server {
    listen 443 ssl http2;
    server_name bernatlab.cat;

    ssl_certificate     /etc/letsencrypt/live/bernatlab.cat/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/bernatlab.cat/privkey.pem;

    # Protocols moderns nomes
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers off;

    location / {
        proxy_pass http://localhost:8123;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Redireccio de HTTP a HTTPS
server {
    listen 80;
    server_name bernatlab.cat;
    return 301 https://$host$request_uri;
}
```

## Certificats auto-signats (per a Tailscale)

Quan treballes nomes dins de Tailscale, no necessites un certificat de Let's Encrypt per HTTPS: nomes tu hi accedeixes. Pots fer-te un **certificat auto-signat**:

```bash
# Generar un certificat auto-signat
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=raspberry"
```

El navegador es queixara ("Aquest certificat no es de confianca") perque no esta firmat per una CA. Pero el trafic **va xifrat igualment**. Es valid per a usos interns.

Alternativa elegant: la CA de Tailscale. Tailscale ja distribueix una CA per a la teva xarxa privada. Pots veure-la a:

```bash
tailscale cert raspberry.ts.net
# Genera un certificat reconegut pels dispositius Tailscale!
```

## Bones practiques amb TLS

- **TLS 1.2 minim, ideal 1.3 nomes**. Desactiva TLS 1.0 i 1.1.
- **Xifratges moderns**: cap SSLv3, cap RC4, cap MD5.
- **HSTS (HTTP Strict Transport Security)**: indica al navegador que nomes HTTPS sempre.
- **Renovacio automatica**: configura cron o systemd per renovar els certificats.
- **Caps de seguretat**: `Strict-Transport-Security`, `X-Frame-Options`, `Content-Security-Policy`, etc.

Exemple de capçaleres segures amb Nginx:

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

## Com verificar el TLS

Un cop configurat, pots verificar-ho amb eines externes:

- **SSL Labs** (https://www.ssllabs.com/ssltest/): analisi complet, gratis.
- **testssl.sh** (https://testssl.sh/): analisi per linia de comandes.
- **`openssl s_client`**: per connectar-se manualment.

Exemple:

```bash
openssl s_client -connect bernatlab.cat:443 -servername bernatlab.cat
```

Veuras el certificat, els xifratges disponibles, i la versio de TLS.

## Connexions amb altres capitols

- **M1 Cap 6** - Contenidors i Portainer: els serveis Dockers son els que exposaras amb HTTPS.
- **M2 Cap 4** - Docker Compose: serveis que es beneficien d'un reverse proxy.
- **Cap 4 d'aquest modul** - Firewall: HTTPS es el port 443/tcp.
- **Cap 6 d'aquest modul** - Secrets: els certificats son un secret.

## Conclusio

TLS es la **S** d'HTTPS i la base de la comunicacio segura a Internet. Al BernatLab, amb Tailscale, no cal certificat public per als serveis interns (nomes per exposar a Internet). Let's Encrypt + Caddy o Nginx es la combinacio estandard. Recorda: el trafic HTTP en text pla es com enviar postals: tothom al cami les pot llegir. TLS es posar-les dins un sobre lacrat.

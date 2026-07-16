# Exercici practic - Capitol 5: TLS i certificats

> 30-45 min · Real al teu sistema

## Objectiu

Configurar HTTPS a un servei del BernatLab, ja sigui amb Let's Encrypt (si tens domini) o amb certificat auto-signat / CA Tailscale (si nomes es per a us intern).

## Requisits

- Un servei web accessible (Home Assistant, Portainer, Gitea, una app qualsevol)
- 30-45 minuts
- Opcional: un domini propi apuntant a la teva IP publica

## Pas 1: Inventari de serveis web (5 min)

Llista quins serveis web tens actualment:

```bash
sudo ss -tlnp | grep -E ":80|:443|:8000|:8080|:3000|:8123"
```

Apunta'ls: nom, port intern, ruta al fitxer de configuracio.

## Pas 2A: HTTPS amb Let's Encrypt (si tens domini) (20 min)

Si tens un domini tipus `bernatlab.cat` apuntant a la teva IP publica:

```bash
# Instal·la certbot
sudo apt install certbot

# Atura temporalment qualsevol servei al port 80
sudo systemctl stop caddy 2>/dev/null
sudo systemctl stop nginx 2>/dev/null

# Obte el certificat
sudo certbot certonly --standalone -d bernatlab.cat -d www.bernatlab.cat

# Verifica
ls /etc/letsencrypt/live/bernatlab.cat/
# cert.pem, chain.pem, fullchain.pem, privkey.pem

# Configura Nginx per usar-lo
sudo nano /etc/nginx/sites-available/bernatlab
```

Contingut minim:

```nginx
server {
    listen 443 ssl http2;
    server_name bernatlab.cat www.bernatlab.cat;

    ssl_certificate     /etc/letsencrypt/live/bernatlab.cat/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/bernatlab.cat/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    add_header Strict-Transport-Security "max-age=31536000" always;

    location / {
        proxy_pass http://localhost:8123;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 80;
    server_name bernatlab.cat www.bernatlab.cat;
    return 301 https://$host$request_uri;
}
```

```bash
# Activa la configuracio
sudo ln -s /etc/nginx/sites-available/bernatlab /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Comprova
curl -I https://bernatlab.cat
```

## Pas 2B: HTTPS auto-signat o amb Tailscale (si no tens domini) (15 min)

Si nomes treballes amb Tailscale, no cal Let's Encrypt. Tens dues opcions:

**Opcio 1: Certificat auto-signat amb openssl**

```bash
# Crea un directori per als certificats
sudo mkdir -p /etc/ssl/self-signed
cd /etc/ssl/self-signed

# Genera el certificat (valid 1 any)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=raspberry"

# Configura Nginx per usar-lo
sudo nano /etc/nginx/sites-available/intern
```

Contingut:

```nginx
server {
    listen 443 ssl http2;
    server_name raspberry;

    ssl_certificate     /etc/ssl/self-signed/cert.pem;
    ssl_certificate_key /etc/ssl/self-signed/key.pem;

    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        proxy_pass http://localhost:8123;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/intern /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# El navegador es queixara pero el trafic va xifrat
```

**Opcio 2: Certificat de Tailscale (millor!)**

Tailscale distribueix una CA interna. Pots obtenir un certificat firmat per aquesta:

```bash
# Veure la CA del teu tailnet
tailscale cert
# Retorna el certificat i la clau per a raspberry.ts.net

# Desar-los
sudo mkdir -p /etc/ssl/tailscale
sudo cp raspberry.ts.net.crt /etc/ssl/tailscale/cert.pem
sudo cp raspberry.ts.net.key /etc/ssl/tailscale/key.pem
```

Ara els navegadors i clients que tenen Tailscale confien en aquesta CA, per tant **no apareix l'avís de seguretat**.

## Pas 3: Renovacio automatica (5 min)

Per a Let's Encrypt, els certificats caduquen als 90 dies. Configura la renovacio:

```bash
# Prova la renovacio
sudo certbot renew --dry-run

# Activa el timer de systemd
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
sudo systemctl list-timers | grep certbot
```

## Pas 4: Verifica (5 min)

Des del teu portatil:

```bash
# Comprova la versio de TLS
echo | openssl s_client -connect bernatlab.cat:443 2>/dev/null | grep -E "Protocol|Cipher"
# Hauries de veure: TLSv1.3

# O utilitza testssl.sh
docker run --rm -it drwetter/testssl.sh bernatlab.cat
```

Des del navegador:

- Obre https://bernatlab.cat
- Hauries de veure el cadenat
- Comprova el certificat (clic al cadenat > Connection is secure > Certificate is valid)

## Pas 5: Documenta (5 min)

Al fitxer `inventari-seguretat.md`, afegeix una seccio "TLS" amb:

- Quin servidor web fas servir (Nginx, Caddy).
- On es desen els certificats.
- Data d'expiracio del proper certificat.
- Com es renova automaticament.

## Validacio

- [ ] Has configurat HTTPS a almenys un servei.
- [ ] El navegador mostra el cadenat verd (o confia en Tailscale).
- [ ] La versio de TLS es 1.2 o 1.3.
- [ ] La renovacio automatica esta activa.
- [ ] Has documentat la configuracio.

## Per aprofundir

- Prova **Caddy** en lloc de Nginx: nomes amb el Caddyfile ja fa TLS magic.
- Analitza el teu servidor a https://www.ssllabs.com/ssltest/.
- Configura **HSTS** (Strict-Transport-Security) per forçar HTTPS.
- Investiga **OCSP Stapling** per millorar la verificacio de revocacio.

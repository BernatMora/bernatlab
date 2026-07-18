# Exercici practic - M8 Cap 2: MobaXterm

> 20-30 min - Al teu Windows

## Objectiu

Instal·lar MobaXterm i configurar una sessio SSH a la RPi amb claus.

## Requisits

- Clau SSH ja configurada (del capitol anterior).
- Tailscale actiu.
- 50 MB d'espai lliure al disc.

## Pas 1: Descarregar MobaXterm (5 min)

1. Vés a https://mobaxterm.mobatek.net/download.html
2. Click a **Download Home Edition**
3. Tria la versio **Portable** (un sol .exe, sense instal·lacio)
4. Descarrega el .zip

## Pas 2: Descomprimir (1 min)

1. Crea la carpeta `C:\Users\usuari\bin\MobaXterm\`
2. Descomprimeix el .zip a dins
3. Hauries de veure `MobaXterm.exe`

## Pas 3: Crear acces directe (2 min)

1. Click dret a `MobaXterm.exe` > **Enviar a** > **Escriptori (crear accés directe)**
2. Opcionalment, obre **Propietats** i:
   - Canvia el nom a "MobaXterm"
   - A **Icona**, tria una que t'agradi
   - A **Inici a**, posa `C:\Users\usuari\bin\MobaXterm`

## Pas 4: Obrir MobaXterm i crear sessio (5 min)

1. Executa MobaXterm
2. A la pantalla d'inici, click a **Session** (a dalt a l'esquerra)
3. Click a **SSH**
4. Emplena:
   - **Remote host**: `100.x.y.z`
   - **Username**: `bernat`
   - **Port**: `22`
5. A la pestanya **Advanced SSH settings**:
   - Marca **Use private key**
   - Browse: `C:\Users\usuari\.ssh\id_ed25519`
6. Click a **OK**

## Pas 5: Verificar la connexio (2 min)

Si tot va be:
- S'obre una pestanya nova amb la terminal SSH
- Veus el prompt `bernat@hortosona:~$`
- A l'esquerra veus el navegador de fitxers SFTP

## Pas 6: Provar la transferencia de fitxers (3 min)

A la columna de l'esquerra (navegador SFTP):
1. Navega a `/home/bernat/homelab`
2. Arrossega un fitxer qualsevol desde el teu Windows (per exemple, una imatge)
3. Hauria d'apareixer al servidor

## Pas 7: Configurar port forwarding (5 min)

Exemple: accedir a Uptime Kuma (port 3001 de la RPi) des del Windows.

1. Click a **Tunneling** (a dalt)
2. Click a **New SSH tunnel**
3. Configura:
   - **Local clients**: 
     - Local port: `3001`
     - Forwarded host: `localhost`
     - Forwarded port: `3001`
   - **SSH server**: `bernat@100.x.y.z:22`
4. Click a **Save**
5. Torna a la pestanya principal i obre el navegador a `http://localhost:3001`
6. Hauries de veure Uptime Kuma

## Validacio

Has acabat si:
- [ ] MobaXterm descarregat i instal·lat (o portable)
- [ ] Acces directe a l'escriptori
- [ ] Sessio SSH configurada amb clau privada
- [ ] Connexio funciona sense password
- [ ] Has transferit un fitxer via SFTP
- [ ] Has configurat port forwarding per a Uptime Kuma

## Per aprofundir

- Afegeix una **segona sessio** per altres serveis (Portainer, Grafana, etc.).
- Activa **X11 forwarding** si vols provar aplicacions graficament.
- Exporta les sessions per backup.

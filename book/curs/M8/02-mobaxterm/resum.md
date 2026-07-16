# Resum - M8 Cap 2: MobaXterm al Windows

## Per que importa

PowerShell esta be per a comandes puntuals, pero per a **treball diari amb servidors** es queda curt:
- No recorda les connexions.
- No permet transferir fitxers facilment.
- No soporta SSH nadiu en finestres graficament netes.

**MobaXterm** es un client SSH per Windows que te **tot el que necessites**:
- **Sessions guardades** amb un clic.
- **Transferencia de fitxers SFTP** integrada (arrossegar i deixar anar).
- **Multiples pestanyes** amb terminals independents.
- **X11 forwarding** si mai ho necessites.
- **Port forwarding** (tunels SSH).
- **Gratis** en la versio Home Edition (amb limitacions, pero mes que suficient per a un homelab).

## Instalacio

1. Descarrega de https://mobaxterm.mobatek.net/download.html
2. Tria la **Home Edition** (gratuita).
3. Tria **Portable** si no vols instal·lar res (un sol .exe).
4. Executa.

## Configuracio inicial

### Crear una sessio per a la RPi

1. Click a **Session** (a dalt a l'esquerra).
2. Click a **SSH**.
3. Emplena:
   - **Remote host**: `100.115.134.76` (o `hortosona` si tens MagicDNS).
   - **Username**: `bernat`.
   - **Port**: `22`.
   - **Specify username**: marcat.
4. Click a **Advanced SSH settings**:
   - Marca **Use private key**.
   - Busca el fitxer `C:\Users\iadmin\.ssh\id_ed25519`.
5. Click a **OK**.

Et sortira una pestanya nova amb la terminal SSH. A la **esquerra** veuras el navegador de fitxers SFTP.

## Caracteristiques utils

### Transferencia de fitxers

A la **esquerra de la terminal** tens un navegador de fitxers. Pots:
- Arrossegar fitxers del teu PC a la RPi.
- Editar fitxers amb doble click (obre un editor integrat).
- Navegar per carpetes com si fos un explorador.

Aixo **substitueix WinSCP** (una altra eina).

### Multiples pestanyes

Cada sessio s'obre en una pestanya nova. Pots tenir:
- Una pestanya per `ssh hortosona` (RPi principal).
- Una pestanya per `ssh hortosona` amb `tail -f /var/log/syslog`.
- Una pestanya per una altre maquina.

### Port forwarding

Si vols accedir a un port de la RPi des del teu Windows pero nomes tens SSH (per exemple, Grafana al 3000 intern):

1. **Tunneling** > **New SSH tunnel**.
2. Emplena:
   - **Local port**: `3000` (el que obriras al Windows).
   - **Remote port**: `localhost:3000` (el de la RPi).
3. Click a **Start**.

Ara pots obrir `http://localhost:3000` al navegador del Windows i veuras Grafana.

### X11 forwarding (avancat)

Si vols executar aplicacions graficament de la RPi al teu Windows (per exemple, un editor com `gedit`), cal X11. Pero MobaXterm ja te un servidor X11 integrat, nomes cal marcar la opcio a la sessio.

## Emmagatzemant de sessions

Les sessions es guarden a un fitxer `MobaXterm.ini` (o a `%APPDATA%\MobaXterm\`). Pots:
- **Exportar** la teva llista de sessions per sincronitzar entre PCs.
- **Backup** automatic si vols.

## Limitacio de la Home Edition

- **Maxim 12 sessions** guardades (suficient per a un homelab).
- **Maxim 4 sessions SSH simultanies** (aixo si que pot ser limitat).
- **Banner** "MobaXterm Home Edition" al iniciar.

Si necessites mes, la **Professional Edition** son ~70 USD (pagament unic).

## Connexions

- **M8 cap 1** - Les claus SSH que acabes de configurar funcionen aqui.
- **M8 cap 3** - El perfil SSH per a PowerShell com a alternativa.
- **M8 cap 4** - PowerToys Run per trobar MobaXterm rapid.

## Errors habituals

- **Clau privada no carrega** - Has seleccionat malament el fitxer. Ha de ser `id_ed25519` (sense extensio).
- **Caracters raros** - Configura la codificacio a UTF-8: Settings > Configuration > Terminal.
- **Sesions que no es guarden** - Has creat la sessio pero no has fet "Save settings" abans de sortir.

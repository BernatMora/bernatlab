# PC Windows de l'hort (també conegut com "hort")

> Configuracio del PC Windows a l'hort amb Tailscale i acces SSH.

## Dispositiu

- **Hostname**: `hort` (Tailscale)
- **Sistema operatiu**: Windows
- **Usuari SSH**: `hort-osona`
- **Com accedir**: `ssh hort-osona@hort` (des de qualsevol node del tailnet)

## Si encara no esta al tailnet

### 1. Instal·la Tailscale a Windows

Descarrega'l de https://tailscale.com/download/windows

### 2. Login amb el compte del BernatLab

Obre Tailscale, fes login amb el compte que ja tens (bernatmora o similar).

### 3. Comprova que esta al tailnet

```powershell
tailscale status
# Hauries de veure: hort, hortosona, windows, mac, iphone
```

## Configurar el servidor SSH a Windows

Per accedir per SSH al Windows de l'hort, cal tenir el servidor SSH activat:

1. **Settings > Apps > Optional Features** → afegeix **OpenSSH Server**
2. **Services** → inicia el servei **OpenSSH SSH Server**
3. **Settings > System > Optional Features** → configura el servei per arrencar automaticament

Un cop fet:

```powershell
# Provar des de la RPi
ssh hort-osona@hort

# O des del Mac/Windows de la feina
ssh hort-osona@hort
```

## Usos habituals

### Des de la RPi (hortosona)

```bash
# Accedir al Windows de l'hort
ssh hort-osona@hort

# Copiar fitxers de la RPi al Windows
scp /home/bernat/fitxer.txt hort-osona@hort:C:/Users/hort-osona/Documents/
```

### Des del Windows de la feina

```powershell
ssh hort-osona@hort
```

### Des del Mac de casa

```bash
ssh hort-osona@hort
```

## Avantatges de tenir el Windows a l'hort

- **PC sempre a l'hort**: pots treballar sense portar el portatil
- **Interficie grafica**: per fer coses visuals (Grafana, Portainer, etc.)
- **Backup de dades**: pots sincronitzar copies amb la RPi
- **Proves locals**: tens un PC mes per provar coses

## Xarxa Tailscale actual del BernatLab

| Node | Sistema | Usuari | IP Tailscale (aprox) |
|---|---|---|---|
| `windows` | Windows | bernat | 100.82.142.113 |
| `mac` | macOS | bernat | (varia) |
| `iphone` | iOS | - | (varia) |
| `hortosona` | Raspberry Pi | bernat | 100.115.134.76 |
| `hort` | Windows | hort-osona | (la que tingui) |

## Notes

- Tots els nodes estan al mateix compte Tailscale
- Es poden accedir per hostname (Tailscale MagicDNS) o per IP
- Si tens problemes, mira https://login.tailscale.com/admin/machines

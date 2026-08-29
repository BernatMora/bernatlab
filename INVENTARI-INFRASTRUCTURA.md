# Inventari infrastructura BernatLab (actualitzat 29-08-2026)

> Document viu. Si_canvies_res, edita aquest fitxer i fes commit.

## Topologia
| Node | IP LAN | Tailscale | Notes |
|---|---|---|---|
| hortosona (RPi 4B 8GB) | 192.168.1.100 | 100.115.134.76 | Ethernet, Debian 13 |
| MacBook Air M4 | DHCP (192.168.1.104) | 100.86.178.51 | macOS 26.5.2, 16GB |
| bernat-1 (Win) | - | 100.108.101.11 | offline |
| bernat-pc (Linux) | - | 100.121.249.107 | offline |
| bernat (Win) | - | 100.82.142.113 | offline |
| iphone183 | - | 100.111.104.121 | - |
| macbook-pro | - | 100.67.26.116 | offline |
| hort (Linux) | - | 100.97.77.87 | offline |

Acces: `ssh bernat@192.168.1.100` (clau id_ed25519 del Mac; password tancat).
Fora de casa: mateixa comanda pero amb la IP Tailscale 100.115.134.76.

## RPi hortosona - serveis
| Servei | Port | Estat |
|---|---|---|
| Homepage | 3000 | actiu |
| UptimeKuma | 3001 | actiu |
| Grafana | 3002 | actiu (admin/hort2026) |
| Portainer | 9443 | actiu |
| InfluxDB | 8086 | actiu, org/bucket: hortosona |
| Nextcloud | 8080 | actiu, dades a /mnt/nuvol/nextcloud |
| entrenaments-app | 3035 | actiu |
| kettlebell-trainer | 5000 | actiu (systemd kettlebell.service, venv propi) |
| menu_server.py | - | actiu (auto-start) |
| 7 apps musica/jocs | 3010-3016 | actives |

## stacks
- /home/bernat/docker (compose del stack principal)
- /home/bernat/entrenaments-app, kettlebell-trainer (sense remote Git - PENDENT)
- Apps 3010-16: containers standalone (rork-*, jocs-mentals, etc.)

## disc extern /mnt/nuvol (465GB, ext4, fstab nofail)
- nextcloud/ - dades Nextcloud
- kettlebell-data/, entrenaments-backups/, kettlebell-backups/ - dades apps
- projects/, lick-variator-source/ - codi
- credentials/ - credencials (root)
- backups-sistema/ - backup mensual automatic: home+etc+volums docker
  - Script: /home/bernat/bin/backup-mensual.sh, log a ~/bin/backup.log
  - Cron: dia 1 de cada mes 3:00

## manteniment
- apt: unattended-upgrades actiu (seguretat diaria)
- Cron: stop 1:00 / start 6:30 uptime-kuma+portainer; backup dia 1 3:00
- Ollama: gemma3:270m, gemma3:1b, phi3:mini
- BLE bluetooth actiu (Mi Flora EN ESPERA), Mosquitto container EN ESPERA
- LoRa Heltec ABANDONAT; toolchain Arduino Heltec esborrat del Mac (29-08-26)

## MAC (MacBook Air M4)
- Tooling: Hermes, Tailscale, OrbStack, VS Code, Cursor, Ollama, Arduino IDE (sense Heltec)
- iCloud actiu: Desktop i Documents sincronitzats (Hort-Osona)
- Time Machine: NO configurat (pendent, cal disc extern local)
- Neteja 29-08-26: 32GB -> 68GB lliures

## repos Git (agost 2026)
- github.com/BernatMora/bernatlab (aques document dins)
- github.com/BernatMora/kettlebell-trainer (privat, snapshot 29-08-26)
- github.com/BernatMora/entrenaments-app (privat, snapshot 29-08-26)
- Acces RPi: deploy keys (nomes escrit, per repo) a ~/.ssh/gh_deploy_*
  + alies a ~/.ssh/config: github-bernatlab / github-kettlebell / github-entrenaments
- Per clonar des del PC feina: gh repo clone BernatMora/<repo> (gh auth login primer)

## pendents
1. Time Machine al Mac amb disc extern
2. Reactivar Mosquitto + Mi Flora quan toqui (scripts a ~/hort-osona-iot)

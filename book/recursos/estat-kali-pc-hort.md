# Estat del PC hort (Kali) - 2026-08-07 10:35

> Document d'estat del PC hort amb Kali Linux, accessible des del tailnet.

## Connexio rapida

```bash
# Des del Windows (obert en aquesta sessio)
ssh hort-osona@hort

# Des del Mac
ssh hort-osona@hort

# Des de la RPi (saltant)
ssh -J bernat@hortosona hort-osona@hort
```

## Resum del sistema

- **Hostname**: Hort
- **SO**: Kali Linux 6.19.14+kali-amd64
- **Tailscale IP**: 100.97.77.87
- **Usuari**: hort-osona
- **RAM**: 7,7 GB (5,7 GB lliure)
- **Disc**: 448 GB (21 GB usat)

## Lab actiu

| Contenidor | IP | Funcio |
|---|---|---|
| dvwa | 10.10.30.10 | Web vulnerable |
| juice-shop | 10.10.30.20 | Botiga moderna vulnerable |
| metasploitable | 10.10.30.30 | Linux vulnerable |

## Tallafoc

- **Aillament actiu** del lab respecte a la LAN i Internet
- **Servei persistent**: `/etc/systemd/system/isolate-lab.service`
- **Activat** al boot (enabled)

## Eines principals

16 eines trobades, incloent:
- nmap, nikto, sqlmap, hydra
- john, hashcat
- gobuster, dirb, ffuf
- wpscan, burpsuite, nuclei
- wireshark, tcpdump
- searchsploit, netcat

## Usos principals des del BernatLab

1. **Practiques de ciberseguretat** (lab real)
2. **Pen-testing** dels serveis del BernatLab (auditoria)
3. **Proves de configuracio** abans d'aplicar canvis a la RPi
4. **Documentacio de tecniques** (CyberLab AI)

## Fitxers al CyberLab

- **LAB-15-10**: Estat complet del lab
- **EX-08-01**: Nmap Metasploitable (completat)
- **EX-08-02**: SQL Injection DVWA (completat)

## Pendents

- [ ] Moure el servei a /etc/systemd/system/ (FET)
- [ ] Crear docker-compose.yml (pendent)
- [ ] Backup de la configuracio (FET)
- [ ] Documentar el tallafoc (FET al LAB-15-10 v2.0)

## Documentacio completa

Per mes detalls, veure:
- [LAB-15-10 al CyberLab](https://github.com/BernatMora/cyberlab-ai/blob/main/book/labs/lab-15-10-lab-real-muntat.md)
- [PROJECT_STATE-GLOBAL](https://github.com/BernatMora/bernatlab/blob/main/PROJECT_STATE-GLOBAL.md)

---

*Actualitzat: 2026-08-07 10:35*

# Exercici practic - Capitol 10: Auditoria i compliance

> 45-60 min - Fer una auditoria completa del teu BernatLab

## Objectiu

Fer la primera auditoria completa del teu sistema. Documentar troballes.

## Pas 1: Executar Lynis (10 min)

```bash
sudo apt install lynis
sudo lynis audit system
```

Mira el fitxer `/var/log/lynis-report.dat` i el resum.

## Pas 2: Llista dusuaris i serveis (5 min)

```bash
cat /etc/passwd | grep -v nologin
sudo ss -tlnp
```

## Pas 3: Comprovar configuracio de seguretat (15 min)

```bash
# SSH
sudo cat /etc/ssh/sshd_config | grep -v '^#' | grep -v '^$'

# Firewall
sudo ufw status verbose

# Actualitzacions
apt list --upgradable
```

## Pas 4: Verificar els 10 punts de la checklist (10 min)

Recorre la checklist del resum. Marca cada punt.

## Pas 5: Documentar (10 min)

Crea `auditoria-2026-07.md` amb:
- Data
- Troballes (per categoria)
- Accions a fer
- Propera auditoria

## Validacio

Has acabat si:
- [ ] Lynis executat
- [ ] Llista dusuaris revisada
- [ ] Configuracio verificada
- [ ] Checklist completada
- [ ] Document creat

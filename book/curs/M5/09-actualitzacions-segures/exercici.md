# Exercici practic - Capitol 9: Actualitzacions segures

> 30-45 min - Configurar actualitzacions automatiques de seguretat

## Objectiu

Configurar el teu sistema per aplicar nomes **actualitzacions de seguretat** automaticament.

## Pas 1: Backup abans de tot (5 min)

```bash
sudo apt update
sudo apt list --upgradable
```

## Pas 2: Instal·lar unattended-upgrades (5 min)

```bash
sudo apt install unattended-upgrades
```

## Pas 3: Configurar (10 min)

```bash
sudo dpkg-reconfigure -plow unattended-upgrades
```

Edita `/etc/apt/apt.conf.d/50unattended-upgrades`:

```
Unattended-Upgrade::Allowed-Origins {
    "Debian:trixie-security";
};
```

## Pas 4: Verificar (5 min)

```bash
sudo unattended-upgrades --dry-run
```

## Pas 5: Automatitzar Watchtower (10 min)

Crea un contenidor Watchtower:

```yaml
# docker-compose.yml
services:
  watchtower:
    image: containrrr/watchtower
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: --schedule "0 0 4 * * *"
```

## Pas 6: Provar (5 min)

```bash
docker compose up -d watchtower
docker logs watchtower
```

## Validacio

Has acabat si:
- [ ] Backup fet
- [ ] unattended-upgrades configurat
- [ ] Watchtower corrent
- [ ] Rebs un correu de resum

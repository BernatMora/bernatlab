# Exercici pràctic — Capítol 1: Què és BernatLab

> 30-45 min · Real al teu sistema

## Objectiu

Fer un **inventari real del teu BernatLab** — què hi tens, com hi accedeixes, què funciona. Això et servirà com a "foto inicial" del projecte.

## Requisits

- Tailscale instal·lat al teu Windows/Mac/Linux.
- La Raspberry Pi encesos i connectada.
- El terminal a mà (PowerShell o bash).

## Pas 1: Comprova la connectivitat (5 min)

Des del teu PC, obre el terminal i comprova que pots accedir a la Raspberry:

```bash
ssh bernat@hortosona
# o per IP Tailscale:
ssh bernat@100.115.134.76
```

Si no pots, comprova:
- Està la RPi encesos? (LED verd)
- Tailscale està actiu? (`tailscale status`)
- La xarxa WiFi funciona?

## Pas 2: Inventari de serveis (10 min)

Un cop dins, comprova quins serveis estan corrent:

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Copia la sortida a un document. Hauries de veure almenys 4-5 contenidors.

## Pas 3: Comprova els serveis (10 min)

Des del navegador, accedeix a cada servei i fes una captura de pantalla:

- **Homepage**: http://100.115.134.76:3000
- **Portainer**: https://100.115.134.76:9443
- **Uptime Kuma**: http://100.115.134.76:3001

Si algun no carrega, **apunta-ho** — serà un tema per als capítols posteriors.

## Pas 4: Informació del sistema (5 min)

Recull aquesta informació:

```bash
# Versió del sistema
cat /etc/os-release | head -5

# Nucli i arquitectura
uname -a

# Ús de disc
df -h /

# Ús de memòria
free -h

# Temperatura de la CPU
vcgencmd measure_temp 2>/dev/null || echo "No tens vcgencmd"
```

## Pas 5: Documenta-ho (5-10 min)

Crea un fitxer `book/curs/M1/01-que-es-bernatlab/inventari.md` amb:

```markdown
# Inventari del meu BernatLab (data)

## Connexió
- Tailscale: [sí/no]
- IP: [100.115.134.76]
- Puc entrar per SSH: [sí/no]

## Serveis actius
[enganxa la sortida de docker ps]

## Serveis accessibles
- Homepage: [sí/no]
- Portainer: [sí/no]
- Uptime Kuma: [sí/no]

## Sistema
- SO: [la sortida de /etc/os-release]
- Nucli: [la sortida de uname -a]
- Disc lliure: [de df -h]
- RAM lliure: [de free -h]
- Temperatura CPU: [de vcgencmd]

## Observacions
[Cosa que no funcioni, coses que vegis estranyes, etc.]
```

## Validació

Has acabat si:
- [ ] Has pogut accedir a la RPi per SSH.
- [ ] T'ha sortit una llista de contenidors amb `docker ps`.
- [ ] Has accedit a Homepage, Portainer, i Uptime Kuma.
- [ ] Has recollit la informació del sistema.
- [ ] Has creat el fitxer `inventari.md`.

## Per aprofundir

Si tens ganes de més:
- Mira quantes imatges Docker tens descarregades: `docker images | wc -l`
- Comprova l'ús de xarxa: `docker network ls`
- Mira els volums: `docker volume ls`

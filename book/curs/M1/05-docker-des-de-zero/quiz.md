# Qüestionari — Capítol 5: Docker des de zero

> 10 preguntes · ~15 min

## Pregunta 1
Quina és la diferència entre una imatge Docker i un contenidor?

- [ ] Són el mateix
- [x] La imatge és la plantilla de només lectura; el contenidor és la instància viva
- [ ] El contenidor és la plantilla; la imatge és la instància
- [ ] La imatge conté dades, el contenidor no

## Pregunta 2
Què fa `docker run -d`?

- [ ] Esborra el contenidor
- [x] Executa el contenidor en segon pla (detached)
- [ ] Descarrega la imatge
- [ ] Entra dins el contenidor

## Pregunta 3
Quina és la funció d'un volum Docker?

- [ ] Comprimir la imatge
- [ ] Aïllar la xarxa
- [x] Persistir dades més enllà de la vida del contenidor
- [ ] Encriptar el contenidor

## Pregunta 4
Quin és el fitxer estàndard de Docker Compose?

- [ ] docker.yml
- [x] docker-compose.yml
- [ ] compose.yaml
- [ ] stack.json

## Pregunta 5
Què fa `docker compose up -d`?

- [ ] Esborra tots els serveis
- [x] Aixeca tots els serveis definits al fitxer compose en segon pla
- [ ] Reinicia Docker
- [ ] Mostra l'estat dels serveis

## Pregunta 6
Quin avantatge té una imatge Alpine respecte una Debian?

- [ ] És més segura
- [x] Ocupa molt menys espai (5-10x)
- [ ] Té més funcionalitats
- [ ] És oficial

## Pregunta 7
Què fa `docker ps -a`?

- [ ] Mostra només els contenidors actius
- [x] Mostra tots els contenidors, inclosos els aturats
- [ ] Esborra tots els contenidors
- [ ] Mostra les imatges descarregades

## Pregunta 8
Quina opció de Compose fa que un servei es reinici automàticament després d'un reboot de la RPi?

- [ ] always-on: true
- [x] restart: unless-stopped
- [ ] auto-start: yes
- [ ] boot: enabled

## Pregunta 9 (oberta)
Explica amb les teves paraules: per què Docker és útil per a un homelab? Quins problemes resol respecte instal·lar programari "a mà"?

Pistes per respondre:
- Què passa si un programa necessita una versió concreta de Python i un altre la 3.11?
- Què passa si vols actualitzar un servei sense tocar la resta?
- Què passa si vols fer un backup net del sistema?

## Pregunta 10 (oberta)
Descriu el flux per afegir un nou servei al BernatLab (p. ex. un servidor de jocs). Quins passos seguiries al `docker-compose.yml`?

Pistes per respondre:
- Quina estructura té un servei dins el YAML?
- On poses la imatge, ports, volums?
- Comandes per pujar, mirar logs, etc.

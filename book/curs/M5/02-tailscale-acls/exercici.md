# Exercici practic - Capitol 2: Tailscale i ACLs

> 30-45 min · Real al teu sistema

## Objectiu

Configurar Tailscale a la RPi (si no ho tens), crear un grup d'etiquetes, i definir les ACLs mes adequades al BernatLab. Acabaras amb un servidor nomes accessible des de la teva xarxa privada.

## Requisits

- Tailscale instal·lat a la RPi (o disposat a instal·lar-lo)
- Un compte de Tailscale (gratuit)
- 30-45 minuts
- Un altre dispositiu per provar l'acces (portatil, telefon, etc.)

## Pas 1: Verifica o instal·la Tailscale (5 min)

```bash
# Comprova si ja el tens
tailscale status 2>/dev/null || echo "No instal·lat"

# Si no, instal·la
curl -fsSL https://tailscale.com/install.sh | sh

# Arrenca (obre un link al navegador per autenticar-te)
sudo tailscale up

# Verifica
tailscale status
```

Si ja el tens, simplement verifica que esta actiu. La sortida hauria de mostrar totes les teves maquines.

## Pas 2: Dona d'alta una segona maquina (5 min)

Instal·la Tailscale al teu portatil o telefon. Verifica que es veuen entre elles:

```bash
# Des de la RPi, fes ping al portatil
tailscale ping portatil-bernat

# Des del portatil, obre un navegador
# Ves a http://100.x.y.z (la IP de la RPi)
# Hauries de veure algun servei si n'hi ha cap exposat
```

Anota les IPs Tailscale de cada maquina (`tailscale ip`).

## Pas 3: Crea les etiquetes (10 min)

Ves a https://login.tailscale.com/admin/acls/file. Canvia la seccio `tagOwners` per:

```json
{
  "tagOwners": {
    "tag:server":   ["autogroup:admin"],
    "tag:homelab":  ["autogroup:admin"],
    "tag:personal": ["autogroup:admin"]
  }
}
```

Guarda. Ara assigna l'etiqueta `tag:server` a la teva RPi:

1. Ves a https://login.tailscale.com/admin/machines.
2. Fes clic a la maquina RPi.
3. A "Edit machine", busca "Tags" i afegeix `tag:server`.
4. Desa.

Verifica:

```bash
# Comprova l'etiqueta
tailscale status --json | jq '.Self.Tags'
# Hauria de retornar: ["tag:server"]
```

## Pas 4: Escriu les ACLs adequades (10 min)

A https://login.tailscale.com/admin/acls/file, substitueix les regles per:

```json
{
  "tagOwners": {
    "tag:server":   ["autogroup:admin"],
    "tag:homelab":  ["autogroup:admin"],
    "tag:personal": ["autogroup:admin"]
  },
  "acls": [
    {
      "action": "accept",
      "src":    ["tag:personal"],
      "dst":    ["tag:server:22,80,443"]
    },
    {
      "action": "accept",
      "src":    ["tag:personal"],
      "dst":    ["tag:server:8123"]
    },
    {
      "action": "accept",
      "src":    ["tag:homelab"],
      "dst":    ["tag:server:8123"]
    }
  ]
}
```

Guarda. Espera 30 segons. Prova des del portatil:

```bash
# Hauria de funcionar
ssh bernat@raspberry
curl http://raspberry:8123

# Hauria de fallar
curl http://raspberry:3306  # MySQL nomes intern
```

## Pas 5: Documenta la configuracio (10 min)

Crea un fitxer `tailscale-acls.md` al teu repo amb:

- Les IPs de cada maquina i la seva etiqueta.
- Captura de pantalla de la consola Tailscale amb les ACLs.
- Explicacio de cada regla i per que es ahi.
- Data de la propera revisio (3-6 mesos).

## Validacio

- [ ] Tailscale esta actiu a la RPi i a un segon dispositiu.
- [ ] Has creat les etiquetes (tag:server, tag:personal, etc.).
- [ ] Les ACLs permeten nomes el que tu vols.
- [ ] Pots accedir a la RPi des del portatil per Tailscale.
- [ ] Has documentat la configuracio.

## Per aprofundir

- Prova l'ordre `tailscale debug` per veure informacio tecnica de la teva connexio.
- Experimenta amb **Taildrop**: transferir fitxers entre dispositius via Tailscale.
- Activa **MagicDNS** si encara no el tens (a la consola, a "DNS").
- Configura un **exit node**: la RPi com a passarela per sortir a Internet des d'un altre dispositiu.

# Política de seguretat

BernatLab és un projecte públic, però la infraestructura real és privada.

## No publicar

- Contrasenyes, tokens, cookies, claus API o claus SSH.
- Adreces Tailscale reals, IP públiques, números de sèrie o SSID.
- Fitxers `.env`, dades dels volums Docker, còpies de seguretat o configuracions locals.
- Captures o logs sense anonimitzar.

## Patró recomanat

Versiona només plantilles com `.env.example` amb placeholders. Desa els valors reals fora del repositori, dins una carpeta local ignorada o un gestor de contrasenyes.

Abans de cada push:

```bash
git status
git diff --staged
```

Si es publica accidentalment un secret, no n'hi ha prou amb esborrar-lo en un commit posterior: cal revocar-lo o rotar-lo immediatament i després valorar la neteja de l'historial.

# Resum - Capitol 9: Actualitzacions segures

## La idea clau

Mantenir el sistema **actualitzat** es critic. Cada dia es descobreixen noves vulnerabilitats, i les actualitzacions les corregeixen. Pero actualitzar tambe pot trencar coses.

## Tipus d'actualitzacions

- **Seguretat**: critiques, aplicar rapid.
- **Funcionals**: noves funcionalitats, aplicar amb mes cura.
- **Kernel**: requereix reinici.

## Fonts

- `apt update && apt upgrade` (Debian/Ubuntu).
- Renovacio dimatges Docker.
- Renovacio de dependencies en projectes.

## Bones practiques

1. **Mirror de proves**: primer aplica al teu entorn de proves.
2. **Mirror de produccio**: despres al servidor real.
3. **Automatitzacio**: Dependabot, Watchtower, unattended-upgrades.
4. **Copia de seguretat abans**: sempre, per si de cas.
5. **Monitoritzacio despres**: verifica que tot funciona.

## Eines

- **unattended-upgrades**: actualitzacions automatiques a Debian.
- **Watchtower**: actualitza contenidors Docker automaticament.
- **Dependabot**: PRs automatiques per a dependencies.

## Riscos

- Actualitzacio que trenca una funcionalitat.
- Reinici no planificat.
- Conflicts amb altres paquets.

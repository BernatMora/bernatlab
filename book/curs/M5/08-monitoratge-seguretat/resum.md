# Resum - Capitol 8: Monitoratge de seguretat

## La idea clau

Volem **detectar activitat sospitosa** al servidor: intents de login fallits, accessos desde IPs desconegudes, fitxers modificats sense permis, etc.

## Eines principals

### Portsentry
- Detecta escanejos de ports.
- Bloqueja automaticament les IPs que fan escaneig.
- `apt install portsentry`

### auditd
- Registra acces a fitxers sensibles.
- Qui ha llegit/modificat què.
- Regles predefinides al directori `/etc/audit/rules.d/`.

### Logwatch
- Resum diari dels logs.
- Envia per correu o Telegram.
- `apt install logwatch`

### Fail2ban
- Ja cobert al capitol 3.
- Compte intents de SSH fallits.

## Bones practiques

- **Logs centralitzats**: a una maquina separada.
- **Alertes inmediates**: per a coses critiques.
- **Revisio periodica**: setmanal o mensual.
- **No només tecnica**: tambe fisica (qui te acces al hardware?).

## Limitacions

- Un atac sofisticat pot evitar la deteccio.
- Massa alertes son tan dolentes com poques.
- Cal mantenir les regles actualitzades.

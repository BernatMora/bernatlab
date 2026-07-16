# Respostes - Capitol 8: Monitoratge de seguretat

## Pregunta 1: Que es Portsentry?

**Resposta correcta**: Eina que detecta escanejos de ports.

**Explicacio**: Portsentry monitoritza els ports del servidor. Si una IP intenta connectar a molts ports rapidament (caracteristic de l'escaneig), la bloqueja.

## Pregunta 2: Que es auditd?

**Resposta correcta**: Sistema dauditoria del kernel.

**Explicacio**: auditd es part del kernel Linux. Registra acessos a fitxers, crides al sistema, etc. Es el sistema dauditoria oficial.

## Pregunta 3: Que fa Logwatch?

**Resposta correcta**: Envia resum diari.

**Explicacio**: Logwatch llegeix tots els logs i crea un resum estructurat. Pots rebrel per correu o Telegram.

## Pregunta 4: Quina eina del capitol 3?

**Resposta correcta**: Fail2ban.

**Explicacio**: Fail2ban ja sha cobert al capitol 3 de SSH hardening.

## Pregunta 5: On enviar logs?

**Resposta correcta**: Al correu o Telegram.

**Explicacio**: Cal rebre els logs en un lloc que miris sovint. Correu o Telegram son les opcions mes utils.

## Pregunta 6: Risc de masses alertes?

**Resposta correcta**: Fatigue dalerta.

**Explicacio**: Si tens 100 alertes al dia, acabes ignorantles. Cal prioritzar.

## Pregunta 7 (oberta): Per que cal mes que un firewall?

**Resposta model**:

- El firewall es la **primera linia** pero no es suficient.
- Un atac pot venir des de dins (un usuari legitim).
- Un 0-day pot passar el firewall.
- Cal detectar activitat **anomala** un cop dins.
- Cal **resposta** a incidents (logs, analisi forense).

## Pregunta 8 (oberta): Com evitar fatigue?

**Resposta model**:

- **Prioritzacio**: nomes alertes de coses critiques.
- **Thresholds**: alertar nomes si pasa X vegades.
- **Horaris**: no enviar alertes a les 3 de la matinada.
- **Agrupament**: 100 SSH fallits = 1 alerta, no 100.
- **Filtratge**: ignorar soroll (bots, scans coneguts).

## Pregunta 9 (oberta): Logs importants?

**Resposta model**:

- **/var/log/auth.log**: logins, sudo, ssh.
- **/var/log/syslog**: general del sistema.
- **/var/log/kern.log**: kernel (drivers, hardware).
- **/var/log/docker/**: contenidors.
- **Logs aplicacio**: grafana, portainer, etc.

## Pregunta 10 (oberta): Resposta a intrusio?

**Resposta model**:

- **Pas 1: Contenir**. Desconnectar la maquina de la xarxa. Si es Docker, aturar contenidors.
- **Pas 2: Investigar**. Mirar logs, fitxers modificats, connexions obertes. Comprendre que ha passat.
- **Pas 3: Netejar**. Esborrar backdoors, canviar totes les contrasenyes, actualitzar el sistema.
- **Pas 4: Prevenir**. Afegir regles per evitar que torni a passar.

## Que fer si has fallat moltes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Instal·la auditd.
- **0-2 encerts**: Comença mirant els logs.

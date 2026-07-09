# Capítol 49 — Auditoria, logs de seguretat i resposta a incidents

> *"Els logs són la caixa negra del teu sistema. Si no els mires, no tens caixa negra."*

## 49.1 Què és la auditoria de seguretat

**Auditoria** és el procés de revisar periòdicament el sistema per:

- Detectar accessos no autoritzats.
- Identificar configuracions errònies.
- Trobar patrons sospitosos.
- Complir normatives (si escau).

Una bona auditoria és **proactiva**: detecta problemes abans que es converteixin en incidents.

## 49.2 Logs essencials

Al BernatLab, els logs clau són:

### Logs de sistema

- `/var/log/syslog`: missatges generals del sistema.
- `/var/log/auth.log`: autenticació (intents de SSH, sudo).
- `/var/log/kern.log`: missatges del kernel.
- `/var/log/dpkg.log`: instal·lació de paquets.
- `/var/log/cron.log`: tasques programades.

### Logs d'aplicacions

- **Docker**: `docker logs <container>`.
- **Grafana**: `/var/lib/docker/volumes/grafana-data/_data/log/`.
- **InfluxDB**: `docker logs influxdb`.
- **fail2ban**: `/var/log/fail2ban.log`.
- **Uptime Kuma**: interfície web.
- **Tailscale**: `tailscale status`, `tailscale netcheck`.

## 49.3 Comandes bàsiques de logs

### journalctl (systemd)

```bash
# Tots els logs d'avui
journalctl --since today

# Errors
journalctl -p err

# Per un servei específic
journalctl -u sshd

# En temps real
journalctl -f

# Des d'una data
journalctl --since "2026-07-08 10:00"
```

### grep i awk

```bash
# Tots els accessos SSH fallits
grep "Failed password" /var/log/auth.log

# Tots els accessos SSH amb èxit
grep "Accepted" /var/log/auth.log

# IPs que han intentat accedir
awk '/Failed password/ {print $(NF-3)}' /var/log/auth.log | sort -u

# Errors de Docker
docker logs --tail 100 bernatlab_grafana_1
```

## 49.4 Què buscar als logs

Senyals d'alerta:

1. **Molts intents d'autenticació fallits** des d'una IP.
2. **Accesos exitosos** des d'IPs estranyes.
3. **Canvis en fitxers crítics** (`/etc/passwd`, `/etc/shadow`, `/etc/ssh/`).
4. **Serveis nous** que s'han iniciat sense motiu.
5. **Tràfic de xarxa anormal** (especialment cap a IPs externes).
6. **Ús elevat de CPU/RAM** en horaris estranys.
7. **Comandes sospitoses** a l'historial de bash.
8. **Fitxers nous** a directoris sensibles (`/tmp`, `/var/tmp`).

## 49.5 Logs centralitzats

Quan tens múltiples dispositius, els logs centralitzats són clau. Opcions:

### Loki + Grafana

Loki és un sistema de logs de Grafana Labs, lleuger i fàcil d'integrar.

Instal·lació a la Raspberry:

```bash
# Loki
docker run -d --name loki \
    -v /home/bernat/homelab/loki:/etc/loki \
    -p 3100:3100 \
    grafana/loki:2.9.0

# Promtail (agent que envia logs)
docker run -d --name promtail \
    -v /var/log:/var/log \
    -v /home/bernat/homelab/promtail:/etc/promtail \
    grafana/promtail:2.9.0
```

Configuració de Promtail (`/etc/promtail/config.yml`):

```yaml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: syslog
          __path__: /var/log/*.log

  - job_name: auth
    static_configs:
      - targets:
          - localhost
        labels:
          job: auth
          __path__: /var/log/auth.log
```

A Grafana, afegeix Loki com a data source i pots fer cerques com:

```
{job="auth"} |= "Failed password"
```

### Alternatives

- **Graylog**: més pesat, però complet.
- **ELK Stack** (Elasticsearch + Logstash + Kibana): el més potent, però molt pesat.
- **Netdata**: ja l'hem vist al Cap 48.
- **Prometheus + Grafana**: per a mètriques (no logs), però útil per alertes.

## 49.6 Alertes de seguretat

Quan els logs mostren alguna cosa sospitosa, cal **actuar ràpid**. Les alertes automatitzades són la millor eina.

### Alertes amb Grafana + Loki

```yaml
# Alerta: més de 10 intents SSH fallits en 5 minuts
- alert: SSHBruteForce
  expr: |
    sum by (remote_addr) (
      rate({job="auth"} |= "Failed password" [5m])
    ) > 0.1
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Possible atac de força bruta SSH des de {{ $labels.remote_addr }}"
    description: "Més de 10 intents fallits en 5 minuts. IP bloquejada per fail2ban."
```

### Alertes amb Uptime Kuma

Uptime Kuma pot monitorar serveis i alertar via Telegram, correu, etc.

### Alertes amb scripts personalitzats

Un script simple que revisa logs i alerta per Telegram:

```bash
#!/bin/bash
# check_security.sh

# Comprovar intents SSH fallits en l'última hora
FAILED=$(grep "Failed password" /var/log/auth.log | grep "$(date '+%b %e %H' -d '1 hour ago')" | wc -l)

if [ $FAILED -gt 20 ]; then
    curl -X POST "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \
        -d "chat_id=$CHAT_ID" \
        -d "text=⚠️ Alerta BernatLab: $FAILED intents SSH fallits en 1h!"
fi

# Comprovar canvis a fitxers crítics
find /etc -name "*.conf" -mtime -1 2>/dev/null | while read f; do
    curl -X POST "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \
        -d "chat_id=$CHAT_ID" \
        -d "text=📝 Fitxer modificat: $f"
done
```

Afegeix a cron cada hora.

## 49.7 IDS (Intrusion Detection System)

Un **IDS** detecta intrusions comparant el comportament amb patrons coneguts.

### AIDE (Advanced Intrusion Detection Environment)

AIDE revisa canvis en fitxers del sistema:

```bash
sudo apt install aide

# Inicialitzar la base de dades
sudo aideinit
# Això crea /var/lib/aide/aide.db.new

# Comparar amb l'estat actual
sudo aide.wrapper --check

# Actualitzar la base
sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db
```

Configurar a `/etc/aide/aide.conf`:

```
# Directoris a monitorar
/boot Full
/bin Full
/sbin Full
/etc Full
/usr Full
/var/log Full
```

AIDE revisa atributs, mides, hash, etc. Si algun canvia, t'avisa.

### OSSEC / Wazuh

**Wazuh** (abans OSSEC) és un IDS complet amb:

- Monitor de fitxers.
- Detector d'intrusions.
- Anàlisi de logs.
- Alertes.

Per al BernatLab, és overkill, però útil si vols auditar molt.

## 49.8 Resposta a incidents

Quan es detecta un incident, cal un **procediment** clar:

### Les 6 fases de la resposta

1. **Preparació**. Tenim eines, runbooks, contactes.
2. **Detecció**. Hem vist alguna cosa sospitosa.
3. **Anàlisi**. Què ha passat exactament?
4. **Contenció**. Aturar l'atac.
5. **Erradicació**. Treure l'atacant del sistema.
6. **Recuperació**. Tornar a la normalitat.
7. **Post-incident**. Aprendre i millorar.

### Runbook per a una bretxa

Un **runbook** és un procediment pas a pas. Exemple:

```markdown
# Runbook: bretxa de seguretat al BernatLab

## Detecció
- Alerta de Uptime Kuma.
- Logs de fail2ban.
- Canvis a fitxers crítics.

## Pas 1: Contenció immediata
1. Desconnectar la Raspberry de Tailscale.
2. Apagar serveis sospitosos.
3. Canviar TOTES les contrasenyes.
4. Revocar TOTES les claus API.

## Pas 2: Anàlisi
1. Revisar logs d'autenticació.
2. Buscar fitxers nous a /tmp, /var/tmp.
3. Comprovar cron jobs nous.
4. Mirar tràfic de xarxa amb `ss` o `tcpdump`.

## Pas 3: Erradicació
1. Identificar el vector d'entrada.
2. Tancar-lo.
3. Esborrar qualsevol malware.
4. Restaurar des de còpies netes.

## Pas 4: Recuperació
1. Tornar a engegar serveis.
2. Verificar que funcionen correctament.
3. Monitorar intensivament les primeres 24h.

## Pas 5: Post-incident
1. Documentar què ha passat.
2. Identificar millores.
3. Aplicar-les.
4. Comunicar a les parts afectades.
```

## 49.9 Comunicació d'incidents

Si hi ha dades personals afectades, cal:

1. **Notificar els afectats** (tu, en aquest cas).
2. **Si escau, notificar l'APDCAT** (Autoritat Catalana de Protecció de Dades).
3. **Si escau, notificar els Mossos o la Policia Nacional** (si és delicte).
4. **Documentar tot** per a l'auditoria.

## 49.10 Evidències forenses

Si vols investigar a fons, cal preservar evidències:

1. **No apagar el sistema** (perdries memòria volàtil).
2. **Fer còpia del disc** amb `dd` o `ddrescue`.
3. **Capturar memòria** amb `avml` o `LiME`.
4. **Copiar logs** abans que roten.
5. **Documentar l'ordre** de les accions.

Eines útils:

- **The Sleuth Kit** (TSK): anàlisi forense de disc.
- **Volatility**: anàlisi de memòria.
- **Autopsy**: interfície gràfica per a TSK.

## 49.11 Auditories periòdiques

Un calendari d'auditoria recomanat:

| Freqüència | Què auditar |
|---|---|
| **Diàriament** | Alertes de Uptime Kuma, intents SSH. |
| **Setmanalment** | Logs d'auditoria, canvis de paquets. |
| **Mensualment** | Lynis, AIDE, revisió d'usuaris. |
| **Trimestralment** | Auditoria completa, còpies, runbooks. |
| **Anualment** | Penetració testing (si tens temps), disaster recovery drill. |

## 49.12 Errors habituals

**Error 1: no mirar mai els logs**.

Si no mires els logs, els incidents passen sense que te n'adonis. Mira'ls almenys un cop per setmana.

**Error 2: confiar en la seguretat per obscuritat**.

"Ostres, amago el port SSH al 1234" no és seguretat. Només redueix els bots automatitzats.

**Error 3: no tenir cap runbook**.

Quan passa un incident, el pànic et porta a cometre errors. Un runbook t'ajuda a actuar correctament.

**Error 4: no comunicar l'incident**.

Per vergonya o por, alguns ho amaguen. Això és pitjor. Comunica, aprèn, millora.

**Error 5: sobre-reaccionar**.

Si veus un sol intent fallit, no cal apagar tota la infraestructura. Mantén la calma, avalua, respon.

## 49.13 Resum

L'auditoria periòdica i el monitoratge de logs són la cinquena línia de defensa. Logs centralitzats amb Loki + Grafana, alertes automatitzades, IDS com AIDE, i runbooks clars per a la resposta a incidents. La preparació és la clau: quan passa alguna cosa, has de saber què fer sense pensar-ho. En el proper capítol veurem el pla de recuperació davant desastres (DRP), l'última capa de defensa.

## 49.14 Exercicis pràptics

1. Configura Loki + Promtail per centralitzar logs.
2. Crea una alerta a Grafana per a intents SSH fallits.
3. Configura AIDE per monitorar fitxers crítics.
4. Escriu un runbook per a una bretxa de seguretat.
5. Executa Lynis i revisa les advertències.
6. Configura alertes per Telegram via un script.
7. Documenta al README l'estratègia de monitoratge.

Paraules clau: **auditoria, audit, seguretat, security, monitoring, alertes, alerting, detecció, response, incident, runbook, playbook, NIST, SANS, 6 fases, preparació, anàlisi, contenció, erradicació, recuperació, post-incident, post-mortem, blameless, AAR, after action review, lessons learned, millora contínua, logs, syslog, journald, journalctl, rsyslog, syslog-ng, Loki, Promtail, Grafana, alertmanager, alert rules, queries, LogQL, query language, search, filter, regex, parser, label, stream, retention, archive, centralitzat, SIEM, ELK, Elasticsearch, Logstash, Kibana, Graylog, Splunk, Sumo Logic, Datadog, New Relic, Honeycomb, Lightstep, OpenTelemetry, OTLP, span, trace, context, propagator, instrumentation, AIDE, tripwire, file integrity, hash, baseline, compare, scan, update, report, OSSEC, Wazuh, Suricata, Snort, Zeek, Bro, network IDS, host IDS, HIDS, NIDS, malware, virus, rootkit, chkrootkit, rkhunter, ClamAV, clamscan, freshclam, signature, heuristic, anomaly, baseline, deviation, pattern, behavior, signature, IOC, indicator of compromise, TTP, tactics, techniques, procedures, MITRE ATT&CK, kill chain, Lockheed, recon, weaponization, delivery, exploit, install, C2, actions, persist, lateral, evade, cred, discover, collect, exfil, impact, threat hunting, hypothesis, evidence, hunt, analysis, IOC, YARA, Sigma, Elastic rule, detection rule, alert, false positive, true positive, triage, severity, priority, response, escalation, communication, disclosure, GDPR, LOPDGDD, APDCAT, AEPD, notificar, 72h, breach notification, evidence, preservation, chain of custody, forensic, The Sleuth Kit, TSK, Autopsy, Volatility, memory, disk, image, hash, SHA, MD5, integrity, write blocker, bit-stream, dd, ddrescue, dcfldd, Guymager, FTK Imager, EnCase, X-Ways, Magnet AXIOM, Cellebrite, MSAB, mobile, extraction, decoding, analysis, timeline, super timeline, Plaso, log2timeline, reporting, executive summary, technical, findings, recommendations, mitigation, recovery, restore, reimage, rebuild, certificate, rotation, key rotation, secret, password, passphrase, MFA, 2FA, isolation, quarantine, sandbox, containment, eradication, sanitization, secure delete, shred, dd, scrub, NIST 800-88, purge, clear, destroy, degauss, physical destruction, shredder, incinerator, audit trail, log retention, chain of custody, immutable, write once, WORM, S3 Object Lock, Azure Blob Immutable, compliance, GDPR, LOPDGDD, HIPAA, PCI DSS, SOX, ISO 27001, NIST 800-53, NIST CSF, CIS Controls, OWASP, SANS Top 20, PCI, PA-DSS, QSA, auditor, audit report, remediation, gap analysis, maturity model, CMMI, COBIT, ITIL, ISO 27002, ISO 27005, risk management, risk register, risk assessment, likelihood, impact, exposure, residual risk, risk treatment, accept, mitigate, transfer, avoid, control, detective, preventive, corrective, compensating, deterrent, recovery, control objective, statement of applicability, SoA, ISMS, PDCA, plan, do, check, act, continuous improvement, kaizen, lean, agile, dev sec ops, shift left, security by design, secure by default, defense in depth, Zero Trust, least privilege, separation of duties, dual control, two-person integrity, four-eyes, job rotation, mandatory vacation, background check, security awareness, training, education, phishing simulation, tabletop exercise, red team, blue team, purple team, capture the flag, CTF, bug bounty, responsible disclosure, coordinated disclosure, CVE, CNA, vendor, patch, update, fix, hotfix, security advisory, security bulletin, PGP signed, vendor, third-party, supply chain, attack chain, attack vector, attack surface, threat model, STRIDE, PASTA, VAST, LINDDUN, attack tree, misuse case, abuse case, security requirement, security control, security policy, security standard, security procedure, security guideline, security baseline, security architecture, security design, security review, security audit, security assessment, security test, penetration test, pen test, vulnerability assessment, threat assessment, risk assessment, compliance audit, internal audit, external audit, third-party audit, attestation, certification, accreditation, authorization, ATO, IATO, IATT, RMF, NIST 800-37, FedRAMP, DoD, IL, impact level, MAC, classified, secret, top secret, TS, SCI, NOFORN, ORCON, REL TO, ITAR, EAR, export control, dual-use, encryption, ECCN, 5D002, Wassenaar, fundamental research, open publication, dual-use research, DURC, ePPP, export, sanctions, OFAC, BIS, DDTC, foreign person, deemed export, technology transfer, TAA, technical assistance agreement, MLA, manufacturing license agreement**.

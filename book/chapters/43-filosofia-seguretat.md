# Capítol 43 — Filosofia de seguretat al BernatLab

> *"La seguretat no és un producte que compres, és un procés que mantens."*

## 43.1 Per què la seguretat importa, fins i tot a casa

Un homelab no és una empresa amb auditors i equips de seguretat. Però té un risc semblant: dades personals, informació de sensors, possibles accessos externs. La diferència és que **a casa estàs sol** — no tens un departament d'IT que t'avisi.

Arguments per prendre's la seguretat seriosament:

1. **Les dades s'acumulen**. Un cop tens InfluxDB amb mesos de dades, Ollama amb documents personals, i un bot de Telegram, tens molt a perdre.
2. **Els atacs són automatitzats**. Internet és ple de bots que escanen IPs i busquen serveis exposats. No és qüestió de "si et troben", sinó de "quan".
3. **El temps de recuperació pot ser llarg**. Si perds les dades i no tens còpies, trigaràs setmanes a refer-ho.
4. **La reputació importa**. Si tens serveis exposats a Internet, una bretxa pot afectar terceres persones.

## 43.2 Els tres pilars de la seguretat

La seguretat informàtica es basa en tres pilars:

1. **Confidencialitat**. Les dades només les veuen les persones autoritzades.
2. **Integritat**. Les dades no es modifiquen sense permís.
3. **Disponibilitat**. Els serveis funcionen quan toca.

Això s'anomena **triada CIA** (Confidentiality, Integrity, Availability).

Per al BernatLab:

- **Confidencialitat**: Tailscale, autenticació, xifratge.
- **Integritat**: còpies de seguretat, verificació de fitxers, signatures.
- **Disponibilitat**: monitoratge, alertes, redundància.

## 43.3 El model de defenses en profunditat

Una sola capa de seguretat no és prou. Cal aplicar **defenses en profunditat**: múltiples capes que, si una falla, les altres protegeixen.

Per al BernatLab, les capes són:

1. **Xarxa**: Tailscale, tallafocs, segmentació.
2. **Sistema operatiu**: actualitzacions, permisos, audit.
3. **Autenticació**: 2FA, claus SSH, contrasenyes llargues.
4. **Aplicacions**: configuració segura, secrets.
5. **Dades**: xifratge en repòs i en trànsit, còpies.
6. **Monitoratge**: alertes, logs, resposta.

Si un atacant passa la primera capa (per exemple, troba una contrasenya feble), les altres capes l'aturen.

## 43.4 El principi de mínim privilegi

Aplica'l sempre:

> Cada usuari, procés, o sistema ha de tenir **només els permisos que necessita per fer la seva feina**, ni més ni menys.

Exemples:

- El node LoRa no necessita accedir a la base de dades. Només publica a MQTT.
- El bot de Telegram no necessita llegir tots els fitxers. Només la base de dades.
- L'usuari `bernat` no necessita `sudo` per tot. Només per coses específiques.

Al Linux, això es tradueix en:

- Usuaris separats per servei.
- Grups amb permisos mínims.
- `sudo` limitat amb sudoers.
- Capabilities en lloc de root.
- SELinux o AppArmor per confinar processos.

## 43.5 El principi de "no confiïs en ningú"

**Zero Trust** és la filosofia moderna de seguretat:

> No confiïs en cap usuari, dispositiu, o xarxa per defecte. Verifica sempre.

A la pràctica:

- Cada dispositiu ha d'autenticar-se.
- Cada accés ha de ser autoritzat explícitament.
- Totes les comunicacions han d'estar xifrades.
- No hi ha xarxes "de confiança" implícites.

Tailscale implementa Zero Trust de manera natural: cap dispositiu no pot accedir a un altre sense ACL explícita.

## 43.6 Les amenaces més comunes al BernatLab

Vull enumerar les amenaces reals:

1. **Bots d'escaneig**. Escanejen tot Internet buscant serveis oberts. Si tens un port obert amb una versió vulnerable, t'atacaran en qüestió d'hores.

2. **Credencials febles**. Contrasenyes curtes, reutilitzades, o per defecte (admin/admin, root/root).

3. **Software desactualitzat**. Cada aplicació té vulnerabilitats que es corregeixen en actualitzacions. Si no actualitzes, estàs exposat.

4. **Phishing i enginyeria social**. Si tens un correu de contacte públic, rebràs intents de phishing.

5. **Dispositius perduts o robats**. Un portàtil amb cookies i sense xifratge pot comprometre tota la xarxa Tailscale.

6. **Insiders**. Família, amics, o convidats que accedeixen al sistema poden fer mal sense voler.

7. **Atacs físics**. Alguien que accedeixi a la Raspberry pot connectar un USB maliciós o robar la microSD.

8. **Atacs a la cadena de subministrament**. Programari maliciós disfressat d'actualització legítima.

## 43.7 Què NO cal fer

També val la pena enumerar les coses innecessàries:

1. **Antivirus al Linux**. No aporta gaire. Millor configurar bé el sistema.
2. **Auditories externes**. Per a un homelab, és excessiu.
3. **Certificacions (ISO 27001, etc.)**. No apliquen.
4. **VPNs comercials**. Tailscale ja és una VPN bona.
5. **Eines avançades (SIEM, IDS professional)**. Són per a empreses.

## 43.8 Bones pràctiques generals

Aquestes són les 10 regles d'or per al BernatLab:

1. **Actualitza el sistema** cada setmana.
2. **Contrasenyes llargues** (mínim 16 caràcters) i úniques.
3. **Activa 2FA** allà on puguis.
4. **Fes còpies** de tot, xifrades, fora del sistema.
5. **Monitora** els serveis 24/7.
6. **Limita** l'accés: només el que cal, a qui cal.
7. **Xifra** les comunicacions (TLS) i les dades en repòs.
8. **Revisa els logs** periòdicament.
9. **Documenta** el que tens i com està configurat.
10. **Practica** la recuperació: simula una pèrdua de dades.

## 43.9 Quin és el risc acceptable

No tots els sistemes necessiten la mateixa seguretat. Per al BernatLab:

- **Risc acceptable**: que algú accedeixi a les dades dels sensors i les publicacions d'Hort Osona. Són públiques o gairebé.
- **Risc no acceptable**: que algú accedeixi a les credencials de Tailscale, al bot de Telegram, o a les còpies de seguretat. Això donaria accés a tot.

Per tant, les prioritats són:

1. **Credencials** (la porta d'entrada).
2. **Còpies** (per si tot falla).
3. **Dades personals** (que no es perdin ni es filtrin).
4. **Integritat dels serveis** (que no es manipulin).

## 43.10 El factor humà

La part més feble de la seguretat sempre és humana. Al BernatLab:

- **Contrasenyes**: utilitza un gestor (Bitwarden, KeePass).
- **Formació**: aprèn a detectar phishing.
- **Confiança**: no comparteixis contrasenyes per canals no xifrats.
- **Descans**: no configuris coses crítiques quan estàs cansat.

## 43.11 Com aprendràs al llarg del mòdul

El M5 segueix un ordre pràctic:

1. **Cap 44**: Tailscale ACLs i segmentació de xarxa.
2. **Cap 45**: Còpies de seguretat amb restic i BorgBackup.
3. **Cap 46**: 2FA, secrets i gestió de claus.
4. **Cap 47**: fail2ban, rate limiting i tallafocs aplicat.
5. **Cap 48**: Hardening del sistema operatiu.
6. **Cap 49**: Auditoria, logs de seguretat i resposta a incidents.
7. **Cap 50**: Pla de recuperació davant desastres (DRP).

## 43.12 Resum

La seguretat al BernatLab és un procés continu, basat en la defensa en profunditat i el principi de mínim privilegi. Les amenaces principals són externes (bots, credencials febles) i el factor humà és sovint el punt feble. Les prioritats són credencials, còpies, dades personals, i integritat. En els propers capítols veurem com implementar cadascuna d'aquestes capes de manera pràctica.

## 43.13 Exercicis pràctics

1. Inventaria tots els serveis que exposen algun port al BernatLab.
2. Inventaria tots els usuaris i les seves credencials.
3. Inventaria totes les dades emmagatzemades (tipus, mida, ubicació).
4. Fes una llista de les 3 amenaces més probables.
5. Avalua quin és el temps de recuperació si perds cada component.
6. Documenta al README l'estat actual de seguretat.

Paraules clau: **seguretat, security, CIA, confidencialitat, integritat, disponibilitat, defensa en profunditat, defense in depth, mínim privilegi, least privilege, Zero Trust, no confiïs, verificar, autenticació, autorització, comptabilitat, accountability, no-repudiation, threat model, amenaces, atacs, vulnerabilitats, CVE, CVSS, explotació, exposició, superfície d'atac, attack surface, harde ning, bastió, jump box, segmentació, microsegmentation, VLAN, subnet, tallafocs, firewall, ACL, WAF, IDS, IPS, SIEM, monitorització, alertes, detecció, resposta, incident, playbook, runbook, recovery, backup, restore, BC, DR, business continuity, disaster recovery, RTO, RPO, SLA, SLO, error budget, post-mortem, blameless, lessons learned, millora contínua, security awareness, formació, phishing, social engineering, tailgating, dumpster diving, shoulder surfing, pretexting, baiting, spear phishing, whaling, smishing, vishing, MFA, 2FA, TOTP, HOTP, FIDO2, WebAuthn, passkey, password manager, secret manager, hash, bcrypt, Argon2, salt, pepper, key stretching, PBKDF2, scrypt, rendiment, GPU, ASIC, side-channel, timing, power, EM, acoustic, fault injection, glitching, rowhammer, spectre, meltdown, Foreshadow, RIDL, Zombieload, cache, branch prediction, microarchitectural, hardening, benchmark, audit, compliance, GDPR, LOPDGDD, ISO 27001, NIST 800-53, CIS Controls, OWASP, top 10, ASVS, MASVS, SAMM, secure SDLC, dev sec ops, shift left, security by design, privacy by design, fail safe, fail secure, defense, response, mitigation, risk, likelihood, impact, exposure, treatment, accept, mitigate, transfer, avoid, residual risk, risk register, heat map, RAG, red, amber, green, critical, high, medium, low, score, qualitative, quantitative, ALE, annual loss expectancy, asset, valuation, threat intelligence, CTI, IOC, indicator of compromise, TTP, tactics, techniques, procedures, MITRE ATT&CK, kill chain, Lockheed, cyber, kill chain, reconnaissance, weaponization, delivery, exploitation, installation, command and control, actions on objectives, persistence, lateral movement, defense evasion, credential access, discovery, collection, exfiltration, impact, MITRE D3FEND, detect, deny, disrupt, degrade, deceive, contain, harden, isolate, restore, recover, analytics, log, monitoring, alerting, response, automation, orchestration, SOAR, runbook, playbook, integration, threat hunting, hypothesis, anomaly, baseline, deviation, statistical, ML, AI, UEBA, user entity behavior, EDR, XDR, NDR, network detection, response, IOC, YARA, Sigma, Snort, Suricata, Zeek, Wireshark, tcpdump, pcap, NetFlow, sFlow, IPFIX, telemetry, sensor, agent, collector, forwarder, syslog, journald, fluentd, logstash, promtail, vector, parse, normalize, enrich, index, search, query, alert, dashboard, visualization, SIEM, XDR, log management, retention, archive, cold, warm, hot, tier, storage, S3, GCS, Azure, Glacier, S3 IA, intelligent, infrequent, frequent, Glacier Deep Archive, durable, available, consistent, eventual, strong, consistency, ACID, BASE, CAP theorem, partition tolerance, eventual consistency, vector clock, lamport, distributed, system, micro service, kubernetes, docker, container, runtime, vulnerability, CVE-2024-XXXX, exploit, patch, zero day, mitigation, workaround, compensating, control, layered, defense, kill, chain, response, cycle, NIST IR, incident response, lifecycle, preparation, detection, analysis, containment, eradication, recovery, post-incident, lessons learned, blameless, after action, AAR, after action review, improvement, plan, action, track, complete, status, OK, blocked, in progress, todo, done**.

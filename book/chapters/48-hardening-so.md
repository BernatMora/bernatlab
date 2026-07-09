# Capítol 48 — Hardening del sistema operatiu

> *"El sistema operatiu és la base de tot. Si la base és feble, tot el que hi construeixes és feble."*

## 48.1 Què és el hardening

**Hardening** és el procés de fer un sistema operatiu **més segur** reduint la superfície d'atac. Això inclou:

- Desactivar serveis innecessaris.
- Aplicar pegats de seguretat.
- Configurar permisos estrictes.
- Activar proteccions del kernel.
- Limitar capacitats dels processos.

## 48.2 Les 4 fases del hardening

1. **Inventari**: què tens instal·lat, què s'executa, quins ports estan oberts.
2. **Reducció**: elimina tot el que no necessitis.
3. **Configuració**: aplica configuracions segures.
4. **Verificació**: comprova que tot funciona i està protegit.

## 48.3 Inventari inicial

Abans de fer canvis, cal saber què tens:

### Quins serveis s'executen

```bash
sudo systemctl list-units --type=service --state=running
```

### Quins ports escolten

```bash
sudo ss -tulnp
```

### Quins paquets estan instal·lats

```bash
sudo apt list --installed
```

### Quins usuaris existeixen

```bash
cat /etc/passwd | grep -v nologin | grep -v false
```

### Quins grups tenen membres

```bash
sudo getent group sudo admin docker
```

## 48.4 Actualitzacions

El primer pas, sempre: **mantenir el sistema actualitzat**.

```bash
# Actualitza la llista
sudo apt update

# Mostra què hi ha pendent
sudo apt list --upgradable

# Actualitza tot
sudo apt upgrade

# Actualitza amb canvis de kernel
sudo apt full-upgrade

# Neteja paquets obsolets
sudo apt autoremove
```

### Actualitzacions automàtiques

Per no oblidar-te'n:

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

Edita `/etc/apt/apt.conf.d/50unattended-upgrades`:

```
Unattended-Upgrade::Allowed-Origins {
    "Debian bookworm-security";
    "Debian bookworm-updates";
};
Unattended-Upgrade::AutoFixInterruptedDpkg "true";
Unattended-Upgrade::MinimalSteps "true";
Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";
```

Ara el sistema s'actualitza sol cada dia.

## 48.5 Desactivar serveis innecessaris

Cada servei actiu és una porta potencial. Desactiva tot el que no necessitis.

A la Raspberry, serveis típics que pots desactivar:

```bash
sudo systemctl disable --now avahi-daemon  # mDNS
sudo systemctl disable --now bluetooth     # si no uses
sudo systemctl disable --now cups          # impressió
sudo systemctl disable --now ModemManager  # mòdem
sudo systemctl disable --now wpa_supplicant  # si no uses Wi-Fi
```

Per veure què consumeix recursos:

```bash
sudo systemctl list-units --type=service --state=running --no-pager
```

## 48.6 Proteccions del kernel (sysctl)

`sysctl` permet configurar paràmetres del kernel en temps d'execució. Crea `/etc/sysctl.d/99-security.conf`:

```ini
# Protecció contra IP spoofing
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# No acceptar redireccions ICMP
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0

# No enviar redireccions
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# No acceptar IP source routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
net.ipv6.conf.default.accept_source_route = 0

# Habilitar SYN cookies (protecció contra SYN flood)
net.ipv4.tcp_syncookies = 1

# No habilitar IP forwarding (si no ets router)
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0

# Protecció contra martians
net.ipv4.conf.all.log_martians = 1

# Kernel: randomize memory layout (ASLR)
kernel.randomize_va_space = 2

# No exposar informació del kernel
kernel.dmesg_restrict = 1
kernel.kptr_restrict = 2

# Restringir accés a /proc
fs.protected_hardlinks = 1
fs.protected_symlinks = 1
```

Aplica:

```bash
sudo sysctl -p /etc/sysctl.d/99-security.conf
```

## 48.7 Permissos dels fitxers crítics

Molts fitxers del sistema tenen permisos massa oberts. Assegura't que estiguin correctes:

```bash
# Permissos estrictes
sudo chmod 600 /etc/shadow
sudo chmod 600 /etc/gshadow
sudo chmod 644 /etc/passwd
sudo chmod 644 /etc/group
sudo chmod 600 /etc/ssh/sshd_config
sudo chmod 600 /boot/grub/grub.cfg  # si tens GRUB

# Propietaris
sudo chown root:root /etc/shadow /etc/gshadow /etc/passwd /etc/group
```

## 48.8 SSH hardening

L'SSH és una porta d'entrada crítica. Configuració segura a `/etc/ssh/sshd_config`:

```
# Port personalitzat (no és seguretat, però redueix bots)
Port 22

# Protocol modern
Protocol 2

# Desactivar root login
PermitRootLogin no

# Només autenticació per clau
PasswordAuthentication no
PubkeyAuthentication yes
PermitEmptyPasswords no

# Limitar usuaris
AllowUsers bernat

# Limitar intents
MaxAuthTries 3
MaxSessions 3

# Desactivar tunneling innecessari
AllowTcpForwarding no
AllowAgentForwarding no
X11Forwarding no

# Log verbós
LogLevel VERBOSE

# Banner d'avís
Banner /etc/issue.net
```

A `/etc/issue.net`:

```
ALERTA: Aquest sistema és privat. Accés no autoritzat prohibit.
Totes les connexions queden registrades.
```

Reiniciar SSH:

```bash
sudo systemctl restart sshd
```

## 48.9 AppArmor o SELinux

**AppArmor** (Debian/Ubuntu) i **SELinux** (RHEL/Fedora) són sistemes de **control d'accés obligatori** (MAC, Mandatory Access Control). Confinen processos perquè només puguin fer el que han de fer.

Per al BernatLab, **AppArmor** és la millor opció:

```bash
# Comprovar si està actiu
sudo aa-status

# Instal·lar perfils
sudo apt install apparmor apparmor-utils apparmor-profiles
```

Activar per defecte:

```bash
sudo systemctl enable apparmor
sudo systemctl start apparmur
```

Forçar tots els perfils:

```bash
sudo aa-enforce /etc/apparmor.d/*
```

Els perfils estan a `/etc/apparmor.d/`. Cada perfil defineix què pot fer un programa (quins fitxers pot llegir, quines xarxes pot usar, etc.).

Exemple de perfil per a un servei:

```apparmor
#include <tunables/global>

/usr/bin/mosquitto {
    #include <abstractions/base>
    #include <abstractions/nameservice>
    
    capability net_bind_service,
    capability setgid,
    capability setuid,
    
    /etc/mosquitto/mosquitto.conf r,
    /etc/mosquitto/conf.d/ r,
    /etc/mosquitto/conf.d/* r,
    /etc/mosquitto/passwordfile r,
    /var/lib/mosquitto/ r,
    /var/lib/mosquitto/* rwk,
    /var/log/mosquitto/ r,
    /var/log/mosquitto/* w,
    
    network tcp,
    network udp,
}
```

## 48.10 Desactivar USB automàtic

Si la Raspberry és accessible, algú podria connectar un USB maliciós. Desactiva el muntatge automàtic:

```bash
sudo apt remove udisks2
```

O amb regla udev:

```
# /etc/udev/rules.d/01-block-usb.conf
ACTION=="add", SUBSYSTEMS=="usb", ENV{UDISKS_IGNORE}="1"
```

## 48.11 BIOS/UEFI password

Si la teva màquina té BIOS/UEFI, posa-hi contrasenya. Això evita que algú pugui canviar la configuració d'arrencada.

A la Raspberry, no cal (no té BIOS configurable), però al Mac sí:

1. Reinicia el Mac.
2. Manté `Cmd+R` per entrar a recovery.
3. Utilitats → Utilitat de Contrasenyes del Firmware.
4. Activa la contrasenya.

## 48.12 Protecció física

La seguretat física importa:

- La Raspberry ha d'estar en un lloc **tancat** (armari amb clau).
- El Mac ha d'estar en un lloc **segur** (no accessible a convidats).
- Els dispositius extraïbles (USB) han d'estar **guardats**.
- Les còpies externes han d'estar en un **lloc diferent**.

## 48.13 sysctl i el rendiment

Algunes configuracions sysctl poden afectar el rendiment:

- `vm.swappiness = 10` (evita intercanvi excessiu, recomanat per a servidors).
- `net.core.somaxconn = 1024` (més connexions entrants).
- `net.ipv4.tcp_tw_reuse = 1` (reutilitza connexions TIME_WAIT).

Per al BernatLab, el rendiment no és crític (pocs usuaris), però no va malament.

## 48.14 Netdata: monitoratge bàsic

Per veure què passa al sistema, instal·la **Netdata**:

```bash
# A la Raspberry
sudo apt install netdata
```

Això t'ofereix un panell web a `http://localhost:19999` amb gràfiques en temps real de:

- CPU, RAM, disc, xarxa.
- Per procés.
- Per servei.

Molt útil per entendre el sistema.

## 48.15 Auditories automàtiques amb Lynis

**Lynis** és una eina d'auditoria de seguretat per a Linux. Escaneja el sistema i proposa millores:

```bash
sudo apt install lynis
sudo lynis audit system
```

Lynis revisa centenars de controls i et dóna un informe amb advertències i suggeriments. Executa'l mensualment.

## 48.16 Checklist de hardening

Un resum del que cal fer:

- [ ] Actualitzar el sistema regularment.
- [ ] Desactivar serveis innecessaris.
- [ ] Configurar sysctl per a proteccions del kernel.
- [ ] Permisos estrictes als fitxers crítics.
- [ ] SSH: només clau, no root, ports limitats.
- [ ] 2FA a SSH (libpam-google-authenticator).
- [ ] AppArmor actiu amb perfils.
- [ ] Tallafocs configurat (UFW).
- [ ] fail2ban actiu.
- [ ] Logs centralitzats i revisats.
- [ ] Lynis o eina similar cada mes.
- [ ] Documentació de tot al README.

## 48.17 Resum

El hardening és un procés continu: inventari, reducció, configuració, verificació. Les accions clau són actualitzar, desactivar serveis, configurar el kernel amb sysctl, endurir SSH, activar AppArmor, i auditar regularment amb Lynis. Al proper capítol veurem com auditar, monitorar logs de seguretat, i respondre a incidents.

## 48.18 Exercicis pràctics

1. Inventaria serveis, ports, paquets i usuaris de la Raspberry.
2. Configura `unattended-upgrades` per a actualitzacions automàtiques.
3. Desactiva 3 serveis innecessaris.
4. Aplica la configuració sysctl de seguretat.
5. Endureix la configuració SSH.
6. Activa AppArmor amb perfils.
7. Instal·la Lynis i executa'l.
8. Documenta al README l'estat de hardening.

Paraules clau: **hardening, endurement, superfície d'atac, attack surface, sysctl, kernel, paràmetres, rp_filter, martian, redirect, source route, SYN cookies, ASLR, kptr_restrict, dmesg_restrict, fs.protected_hardlinks, fs.protected_symlinks, ip_forward, accept_ra, AppArmor, SELinux, MAC, mandatory access control, perfil, profile, enforce, complain, audit, aa-genprof, aa-logprof, apparmor_parser, aa-status, aa-enforce, aa-complain, abstractions, capability, file, network, mount, ptrace, signal, capability, capabilities, Linux capabilities, CAP_NET_BIND_SERVICE, CAP_SYS_ADMIN, CAP_DAC_OVERRIDE, CAP_CHOWN, CAP_FOWNER, CAP_FSETID, CAP_KILL, CAP_SETGID, CAP_SETUID, CAP_SETPCAP, CAP_LINUX_IMMUTABLE, CAP_NET_BIND_SERVICE, CAP_NET_BROADCAST, CAP_NET_ADMIN, CAP_NET_RAW, CAP_IPC_LOCK, CAP_IPC_OWNER, CAP_SYS_MODULE, CAP_SYS_RAWIO, CAP_SYS_CHROOT, CAP_SYS_PTRACE, CAP_SYS_PACCT, CAP_SYS_ADMIN, CAP_SYS_BOOT, CAP_SYS_NICE, CAP_SYS_RESOURCE, CAP_SYS_TIME, CAP_SYS_TTY_CONFIG, CAP_MKNOD, CAP_LEASE, CAP_AUDIT_WRITE, CAP_AUDIT_CONTROL, CAP_SETFCAP, CAP_MAC_OVERRIDE, MAC, mandatory access control, SELinux, AppArmor, TOMOYO, Yama, seccomp, seccomp-bpf, seccomp-filter, filter, sandbox, prctl, PR_SET_NO_NEW_PRIVS, PR_SET_SECCOMP, namespace, mount namespace, PID namespace, network namespace, user namespace, cgroup namespace, cgroup, control group, cgroup v1, cgroup v2, systemd-cgroup, slice, scope, service, unit, unit file, drop-in, override, sysctl, /etc/sysctl.d/, /proc/sys, /proc/sys/net, /proc/sys/kernel, /proc/sys/fs, mount, /etc/fstab, options, nodev, nosuid, noexec, ro, relatime, noatime, securetty, /etc/securetty, login, faillog, faillock, pam, faillock, pam_faillock, pam_tally2, pam_cracklib, pam_pwquality, password quality, complexity, length, history, reuse, dictionary, cracklib, libpam-pwquality, pwquality.conf, /etc/security/pwquality.conf, minlen, dcredit, ucredit, lcredit, ocredit, difok, dictpath, enforce_for_root, retry, remember, sha512, rounds, pam_unix, pam_pwquality, pam_passwdqc, libpam-pkcs11, smart card, certificate, PIV, CAC, Yubikey, U2F, FIDO2, libpam-u2f, libpam-fido2, libpam-yubikey, Yubico PAM, Yubikey, hardware token, libpam-google-authenticator, OATH, TOTP, RFC 6238, RFC 4226, QR code, otpauth, secret, key URI, otpauth-migration, otp, htop, etc, audit, auditd, auditctl, ausearch, aureport, rules, /etc/audit/rules.d/, watch, syscall, file watch, syscall audit, network audit, execve, fork, connect, accept, bind, listen, open, read, write, close, change, profile, snapshot, report, malware, rootkit, chkrootkit, rkhunter, clamav, clamscan, freshclam, signature, update, scan, alert, notification, AIDE, tripwire, integrity, file integrity, baseline, hash, SHA-256, SHA-512, signature, GPG, signed manifest, Tripwire, OSSEC, Wazuh, ELK, Elasticsearch, Logstash, Kibana, SIEM, log management, retention, archive, tier, search, query, dashboard, alert, contact, template, channel, recipient, trigger, threshold, condition, severity, action, suppression, deduplication, correlation, alert, playbook, runbook, incident, response, NIST, SANS, CREST, OWASP, top 10, CWE, CVE, CVSS, EPSS, KEV, catalog, known exploited, vulnerability, scanner, OpenVAS, Nessus, Qualys, Rapid7, InsightVM, Tenable, cloud, security, posture, CSPM, CWPP, CIEM, IAM, least privilege, Zero Trust, ZTNA, SDP, software defined perimeter, BeyondCorp, BeyondCorp Enterprise, identity-aware proxy, IAP, access proxy, OAuth, OIDC, SAML, JWT, mTLS, certificate, x.509, SPIFFE, SPIRE, identity, attestation, workload, mTLS, mesh, service mesh, Istio, Linkerd, Consul, mTLS, automatic, sidecar, ambient, mesh, multi-cluster, multi-region, federation, multi-cloud, hybrid, multitenancy, tenant, isolation, namespace, policy, authorization, OPA, Open Policy Agent, Rego, Cedar, decision, audit, decision log**.

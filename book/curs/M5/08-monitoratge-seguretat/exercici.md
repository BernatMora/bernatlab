# Exercici practic - Capitol 8: Monitoratge de seguretat

> 30-45 min - Configurar auditd a la RPi

## Objectiu

Instal·lar i configurar auditd per registrar activitat sensible.

## Pas 1: Instal·lar (5 min)

```bash
sudo apt install auditd
sudo systemctl enable auditd
sudo systemctl start auditd
```

## Pas 2: Configurar regles basiques (10 min)

Crea `/etc/audit/rules.d/bernatlab.rules`:

```
# Monitoritzar canvis a /etc
-w /etc -p wa -k etc_changes

# Monitoritzar fitxers de Docker
-w /var/lib/docker -p wa -k docker_changes

# Monitoritzar SSH config
-w /etc/ssh/sshd_config -p wa -k ssh_config_change
```

## Pas 3: Recarregar (3 min)

```bash
sudo augenrules --load
sudo service auditd reload
```

## Pas 4: Verificar (5 min)

```bash
sudo auditctl -l
sudo ausearch -k etc_changes
```

## Pas 5: Configurar Logwatch (10 min)

```bash
sudo apt install logwatch
```

Edita `/etc/logwatch/conf/logwatch.conf`:

```
Output = mail
Format = html
MailTo = bernat@elteudomini.com
```

## Validacio

Has acabat si:
- [ ] auditd instal·lat
- [ ] Regles configurades
- [ ] Logwatch instal·lat
- [ ] Rebs un resum diari

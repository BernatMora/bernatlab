"""
Extracta comandes de tots els capítols del BernatLab.

Llegeix tots els .md de book/chapters/, busca blocs de codi (```bash, ```shell, etc.),
i els organitza per secció segons el capítol on apareixen.

Output: book/cheatsheet-data.json (estructura per a generar HTML/Markdown).
"""
import re
import json
from pathlib import Path
from collections import defaultdict

CHAPTERS = Path(r"C:\Users\iadmin\bernatlab\book\chapters")

# Mapeig capítol -> tema (per organitzar la chuleta per àrea)
CHAPTER_TOPIC = {
    range(1, 11): "Fonaments",
    range(11, 23): "Dades operatives",
    range(23, 33): "LoRa",
    range(33, 43): "IA local",
    range(43, 51): "Seguretat",
    range(51, 58): "Operativa 24/7",
    range(58, 70): "Hort Osona en acció",
}

def topic_for(n):
    for r, t in CHAPTER_TOPIC.items():
        if n in r:
            return t
    return "Altres"

# Regex per trobar blocs de codi
code_block_re = re.compile(r"```(\w*)\n(.*?)\n```", re.DOTALL)

# Comandes que NO volem (massa bàsiques o ja òbvies)
SKIP_COMMANDS = {
    "cd", "ls", "pwd", "whoami", "exit", "clear", "history",
    "uptime", "date", "cal", "echo", "cat /etc/os-release",
}

# Comandes que SÍ volem destacar
PRIORITY_COMMANDS = {
    # SSH
    "ssh-copy-id", "ssh-keygen", "ssh-add",
    # Docker
    "docker", "docker compose", "docker run", "docker exec",
    "docker ps", "docker logs", "docker stop", "docker start",
    "docker rm", "docker system",
    # Apt
    "apt update", "apt upgrade", "apt install", "apt autoremove",
    # Restic
    "restic",
    # MQTT
    "mosquitto_pub", "mosquitto_sub",
    # Curl
    "curl",
    # Systemd
    "systemctl", "journalctl",
    # Tallafocs
    "ufw", "iptables", "fail2ban-client",
    # Editors
    "nano ",
    # Cron
    "crontab",
    # Reboot
    "sudo reboot", "sudo shutdown",
    # Backup
    "dd ",
}

def should_include(line):
    """Decideix si una línia de comanda mereix ser a la chuleta."""
    s = line.strip()
    if not s or s.startswith("#"):
        return False
    if len(s) < 8:  # massa curta
        return False
    # Si comença amb prioritat, sí
    for prio in PRIORITY_COMMANDS:
        if s.startswith(prio):
            return True
    # Si conté paraules clau, sí
    keywords = ["install", "restart", "logs", "ps", "pull", "up -d", "down",
                "restic", "compose", "exec", "edit", "create", "delete",
                "remove", "add", "fail2ban", "mosquitto", "ssh ", "scp",
                "influx", "grafana", "prometheus", "systemctl", "ufw",
                "network", "interface", "service", "deploy", "rollback",
                "enable", "disable", "mask", "unmask", "start", "stop"]
    for kw in keywords:
        if kw in s.lower():
            return True
    return False

def categorize(cmd):
    """Retorna la categoria d'una comanda."""
    c = cmd.lower()
    if c.startswith("ssh") or "ssh-" in c or "sshd" in c:
        return "SSH i accés remot"
    if c.startswith("docker") or "compose" in c:
        return "Docker"
    if c.startswith("apt"):
        return "Paquets (apt)"
    if "restic" in c:
        return "Còpies de seguretat"
    if "mosquitto" in c or "mqtt" in c:
        return "MQTT"
    if "influx" in c:
        return "InfluxDB"
    if "grafana" in c:
        return "Grafana"
    if "prometheus" in c or "alertmanager" in c:
        return "Prometheus"
    if c.startswith("ufw") or c.startswith("iptables") or "fail2ban" in c:
        return "Seguretat i tallafocs"
    if c.startswith("systemctl") or c.startswith("journalctl"):
        return "systemd"
    if c.startswith("nano") or c.startswith("vi ") or c.startswith("cat "):
        return "Fitxers i editors"
    if c.startswith("crontab"):
        return "Cron"
    if c.startswith("curl") or c.startswith("wget"):
        return "Xarxa (curl, wget)"
    if "tailscale" in c:
        return "Tailscale"
    if "node-red" in c or "nodered" in c:
        return "Node-RED"
    if "telegram" in c:
        return "Telegram"
    if "lora" in c or "sx12" in c or "ttn" in c:
        return "LoRa i sensors"
    if "backups" in c or "backup" in c or "dd " in c:
        return "Còpies i imatges"
    if "git " in c:
        return "Git"
    if "python" in c or "pip" in c:
        return "Python"
    if "nodered" in c or "node-red" in c:
        return "Node-RED"
    return "Altres"

# Recollir comandes
by_category = defaultdict(list)
seen = set()  # per desduplicar

for f in sorted(CHAPTERS.glob("*.md")):
    if not f.name[:2].isdigit():
        continue
    n = int(f.name[:2])
    topic = topic_for(n)
    content = f.read_text(encoding="utf-8")
    blocks = code_block_re.findall(content)
    for lang, code in blocks:
        if lang and lang not in ("bash", "shell", "sh", "console", "yaml", "yml", "ini", "toml", "python", ""):
            continue
        for line in code.split("\n"):
            if should_include(line):
                stripped = line.strip()
                if stripped and stripped not in seen:
                    seen.add(stripped)
                    cat = categorize(stripped)
                    by_category[cat].append({"cmd": stripped, "cap": n, "topic": topic})

# Ordenar i limitar
result = {}
for cat, cmds in sorted(by_category.items()):
    result[cat] = cmds[:25]  # màxim 25 per categoria per no fer-ho infinit

# Guardar
out = Path(r"C:\Users\iadmin\bernatlab\book\cheatsheet-data.json")
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

# Estadístiques
total = sum(len(v) for v in result.values())
print(f"Comandes extretes: {total}")
print(f"Categories: {len(result)}")
for cat, cmds in sorted(result.items(), key=lambda x: -len(x[1])):
    print(f"  {cat}: {len(cmds)}")

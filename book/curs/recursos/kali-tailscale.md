# Com afegir Kali al tailnet del BernatLab

## Si encara no esta al tailnet

### 1. Instal·la Tailscale (si cal)

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

### 2. Login amb el compte del BernatLab

```bash
sudo tailscale up
# Segueix les instruccions del navegador
# Utilitza el compte que ja tens (bernatmora o similar)
```

### 3. Comprova que esta al tailnet

```bash
tailscale status
# Hauries de veure: kali, hortosona, windows, mac, iphone
```

### 4. Dona un nom al node (opcional pero recomanable)

A la web de Tailscale (https://login.tailscale.com/admin/machines):
- Canvia el nom del node de "kali" a "kali-hort" o "kali-laptop"

Aixi es mes clar quin dispositiu es.

## Ús desde altres dispositius

Des del Windows, Mac o mòbil:

```bash
# Per SSH
ssh bernat@kali-hort
# o
ssh bernat@<IP-Tailscale>
```

## Avantatges

- Pots accedir al Kali des de qualsevol lloc amb Tailscale
- Pots fer proves de seguretat des de la RPi al Kali
- Tens un PC mes per treballar a l'hort
- Si tens algun problema amb la RPi, pots entrar des del Kali

## Útil per a

- Auditoria de seguretat del router 4G
- Pen-testing de la xarxa local
- Documentar configurations
- Fer proves sense afectar la RPi

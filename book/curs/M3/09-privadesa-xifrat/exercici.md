# Exercici practic — Capitol 9: Privadesa i xifrat de fitxers

> 30-40 min · Real al teu sistema

## Objectiu

Instal·lar age, generar un parell de claus, xifrar i desxifrar un fitxer, practicar amb GPG simetric, i crear un script per xifrar/desxifrar.

## Requisits

- Tailscale actiu
- Connexio SSH a la RPi
- 30-40 minuts

## Pas 1: Instal·la age i GPG (5 min)

```bash
sudo apt update
sudo apt install -y age gpg

age --version
gpg --version
```

## Pas 2: Genera un parell de claus amb age (5 min)

```bash
mkdir -p /home/pi/bernatlab/proves/xifrat
cd /home/pi/bernatlab/proves/xifrat

# Genera les claus
age-keygen -o age-key.txt 2> age-pub.txt

# Mostra la clau publica
cat age-pub.txt

# Mostra la clau privada (NO la comparteixis!)
cat age-key.txt

# Important: dona-li permisos 600
chmod 600 age-key.txt
```

## Pas 3: Xifra i desxifra un fitxer (5 min)

```bash
# Crea un fitxer amb dades sensibles
cat > secrets.txt <<EOF
Les meves contrasenyes importants:
- Email: super-secret-pass-2025
- GitHub: github-token-12345
EOF

# Xifra amb clau publica
PUBKEY=$(cat age-pub.txt)
age -r "$PUBKEY" -o secrets.txt.age secrets.txt

# Comprova
ls -la secrets.txt*
file secrets.txt.age
# Hauria de dir "data"

# Esborra l'original
rm secrets.txt
ls secrets.txt
# ls: cannot access... No such file or directory

# Restaura
age -d -i age-key.txt -o secrets-restored.txt secrets.txt.age
cat secrets-restored.txt
# Hauries de veure les contrasenyes originals
```

## Pas 4: Xifratge simetric amb age (5 min)

```bash
# Crea un altre fitxer
echo "Les meves notes privades sobre l'hort" > notes.txt

# Xifra amb contrasenya
age -p -o notes.age notes.txt
# Et demana una contrasenya

# Desxifra
age -d -o notes-restored.txt notes.age
# Et demana la contrasenya
cat notes-restored.txt
```

## Pas 5: Prova GPG (5 min)

```bash
# Xifra simetricament amb GPG
echo "un altre secret" > gpg-test.txt
gpg --symmetric --batch --passphrase "test-2025" -o gpg-test.txt.gpg gpg-test.txt

# Comprova
file gpg-test.txt.gpg

# Desxifra
gpg --batch --passphrase "test-2025" -o gpg-restored.txt gpg-test.txt.gpg
cat gpg-restored.txt
```

## Pas 6: Crea un script de xifrar/desxifrar (5 min)

```bash
cat > /home/pi/bernatlab/scripts/xifrar.sh <<'EOF'
#!/bin/bash
# Xifra un fitxer amb age

if [ $# -ne 1 ]; then
  echo "Us: $0 <fitxer>"
  exit 1
fi

FITXER=$1
PUBKEY="posa_aqui_la_teva_clau_publica_age"

if [ ! -f "$FITXER" ]; then
  echo "Error: $FITXER no existeix"
  exit 1
fi

age -r "$PUBKEY" -o "$FITXER.age" "$FITXER"
echo "Xifrat: $FITXER.age"
EOF

chmod +x /home/pi/bernatlab/scripts/xifrar.sh

# Prova'l
/home/pi/bernatlab/scripts/xifrar.sh secrets.txt
```

## Validacio

Has acabat si:

- [ ] Has instal·lat age i GPG.
- [ ] Has generat un parell de claus age.
- [ ] Has xifrat i desxifrat un fitxer amb age (clau publica).
- [ ] Has xifrat simetricament amb contrasenya.
- [ ] Has provat GPG simetric.
- [ ] Has creat un script per xifrar.

## Per aprofundir

- Investiga com fer servir **Vaultwarden** (Bitwarden auto-allotjat) per a contrasenyes.
- Prova d'integrar age amb **restic** per a una capa extra de xifrat.
- Investiga **gpg-agent** per gestionar les claus GPG amb cache.
- Compara el rendiment entre age i GPG amb un fitxer gran (100 MB).
- Investiga com fer **signing** de commits de git amb GPG.

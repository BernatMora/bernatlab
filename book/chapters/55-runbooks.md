# Capítol 55 — Runbooks: procediments pas a pas

> *"Un runbook és la diferència entre resoldre un incident en 5 minuts o en 5 hores."*

## 55.1 Què és un runbook

Un **runbook** és un document amb **passes exactes** per resoldre un problema concret. A diferència d'un manual general, és:

- **Específic**: per a un problema concret.
- **Pas a pas**: cada pas té un número i una acció clara.
- **Testejat**: ha estat provat almenys un cop.
- **Actualitzat**: reflecteix l'estat actual del sistema.

Els runbooks són la documentació operativa per excel·lència.

## 55.2 Quan usar un runbook

- **Incidents**: "El Grafana no respon, què faig?"
- **Manteniment**: "Com canvio la còpia de B2 a Wasabi?"
- **Recuperació**: "Com recupero una còpia concreta?"
- **Desplegament**: "Com poso en marxa el node LoRa nou?"
- **Auditoria**: "Com listo tots els usuaris actius?"

## 55.3 Estructura d'un runbook

```markdown
# Runbook: [Títol del problema]

## Símptomes
- Què veus quan passa el problema.
- Com et n'adones que passa.

## Diagnòstic
- Passes per confirmar que és aquest problema.
- Comandes concretes a executar.

## Solució
- Passes per resoldre.
- Cada pas amb un número.

## Verificació
- Com saber que s'ha resolt.
- Què fer si no s'ha resolt.

## Prevenció
- Com evitar que passi de nou.
- Canvis a fer al sistema.

## Contactes
- Qui avisar.
- Enllaços útils.

## Última actualització
- Data i per què.
```

## 55.4 Exemple 1: runbook "El Grafana no respon"

```markdown
# Runbook: Grafana no respon

## Símptomes
- El navegador mostra "connexió refusada" a `http://localhost:3000`.
- Les gràfiques no es carreguen.
- Altres serveis poden estar bé.

## Diagnòstic

1. Comprovar si el contenidor està en marxa:
   ```bash
   docker ps | grep grafana
   ```

2. Si el contenidor està aturat, mirar els logs:
   ```bash
   docker logs grafana --tail 100
   ```

3. Si el contenidor està en marxa però no respon, comprovar el port:
   ```bash
   ss -tulnp | grep 3000
   ```

## Solució

**Cas A: contenidor aturat**

1. Reiniciar:
   ```bash
   docker start grafana
   ```

2. Esperar 30 segons i comprovar:
   ```bash
   docker ps | grep grafana
   curl -s http://localhost:3000/api/health
   ```

**Cas B: contenidor en marxa però no respon**

1. Reiniciar:
   ```bash
   docker restart grafana
   ```

2. Si continua sense respondre, mirar els logs per errors:
   ```bash
   docker logs grafana --tail 200
   ```

3. Si hi ha error de base de dades, restaurar la còpia:
   ```bash
   docker stop grafana
   cp -r ~/backups/grafana/* /var/lib/docker/volumes/grafana-data/_data/
   docker start grafana
   ```

## Verificació

- Cridar a `http://localhost:3000` ha de mostrar el login.
- Fer login ha de funcionar.
- Les gràfiques s'han de carregar.

## Prevenció

- Comprovar espai en disc (Grafana necessita almenys 1 GB lliure).
- Assegurar-se que el contenidor té memòria suficient (mínim 256 MB).
- Configurar auto-restart (`restart: unless-stopped` al compose).

## Contactes

- @bernat a Telegram per a dubtes.

## Última actualització
- 2026-07-09 per Bernat: afegit cas d'error de base de dades.
```

## 55.5 Exemple 2: runbook "Recuperar una còpia de seguretat"

```markdown
# Runbook: Recuperar una còpia amb restic

## Símptomes
- Has esborrat un fitxer per error.
- La Raspberry ha perdut dades.
- Vols comparar amb una versió anterior.

## Diagnòstic

1. Comprovar quines còpies tens:
   ```bash
   restic -r ~/backups/bernatlab snapshots
   ```

2. Trobar la còpia amb el fitxer que vols:
   ```bash
   restic -r ~/backups/bernatlab find fitxer.txt
   ```

## Solució

1. Restaurar un sol fitxer:
   ```bash
   restic -r ~/backups/bernatlab restore latest \
       --target /tmp/restored \
       --include /path/al/fitxer.txt
   cp /tmp/restored/path/al/fitxer.txt /path/al/fitxer.txt
   ```

2. Restaurar tota la còpia més recent:
   ```bash
   restic -r ~/backups/bernatlab restore latest \
       --target /tmp/restored
   ```

3. Restaurar una còpia concreta:
   ```bash
   restic -r ~/backups/bernatlab restore abc1234 \
       --target /tmp/restored
   ```

4. Restaurar només el directori homelab:
   ```bash
   restic -r ~/backups/bernatlab restore latest \
       --target /tmp/restored \
       --include /home/bernat/homelab
   ```

## Verificació

- Comprovar que els fitxers restaurats existeixen.
- Comparar amb l'original (si encara existeix).

## Prevenció

- No esborrar res fins que no hagis comprovat la còpia.
- Fer còpies abans de canvis importants.
```

## 55.6 Exemple 3: runbook "Afegir un nou node LoRa"

```markdown
# Runbook: Afegir un nou node LoRa

## Símptomes
- Tens un node ESP32 + SX1262 nou que vols afegir a la xarxa.
- El node ja està programat amb el firmware del Mòdul 3.

## Diagnòstic

1. Comprovar que el node té el firmware correcte:
   ```bash
   # Connectar el node per USB i obrir el monitor sèrie
   screen /dev/ttyUSB0 115200
   ```

2. Verificar que apareix a TTN:
   - Vés a https://console.thethingsnetwork.org.
   - Applications → bernatlab → Devices.
   - Hauries de veure el nou node.

## Solució

1. Configurar el node a TTN:
   - Application → bernatlab → End devices → Add end device.
   - Seleccionar "Enter end device specifics manually".
   - Posar DevEUI, AppKey, AppEUI.
   - Triar perfil "LoRaWAN 1.0.4 EU868".

2. Configurar el payload decoder:
   - Application → Payload formatters → Uplink.
   - Enganxa el decoder CayenneLPP.

3. Configurar l'integració amb TTN:
   - Application → Integrations → MQTT.
   - Activar i apuntar a `mqtt://localhost:1883`.

4. Verificar que arriba al broker MQTT:
   ```bash
   mosquitto_sub -h localhost -t "ttn/bernatlab/+/up" -v
   ```

5. Verificar que arriba a InfluxDB:
   - Vés a Grafana.
   - Explora → InfluxDB → measurement: `lora_data`.
   - Hauries de veure el node nou.

## Verificació

- El node envia dades cada X minuts.
- Les dades apareixen a Grafana.
- Les alertes funcionen si hi ha valors fora de rang.

## Prevenció

- Documentar el node (nom, ubicació, DevEUI).
- Etiquetar físicament el node.
- Fer una còpia del firmware.
```

## 55.7 On guardar els runbooks

Crea una carpeta `~/homelab/runbooks/` amb un fitxer per runbook. La nomenclatura:

- `RB-001-grafana-down.md`
- `RB-002-backup-restore.md`
- `RB-003-add-lora-node.md`

Index al `README.md`:

```markdown
# Runbooks del BernatLab

## Incidents
- [RB-001](RB-001-grafana-down.md) - Grafana no respon
- [RB-002](RB-002-backup-restore.md) - Recuperar còpia
- [RB-003](RB-003-add-lora-node.md) - Afegir node LoRa

## Manteniment
- [RB-101](RB-101-rotate-secrets.md) - Rotar secrets
- [RB-102](RB-102-update-containers.md) - Actualitzar contenidors

## Recuperació
- [RB-201](RB-201-restore-raspberry.md) - Restaurar Raspberry
- [RB-202](RB-202-data-loss.md) - Pèrdua de dades
```

## 55.8 Com crear un bon runbook

### Característiques

1. **Títol clar**: el problema en 5-10 paraules.
2. **Símptomes concrets**: què veus exactament.
3. **Comandes literals**: copy-paste sense errors.
4. **Branques condicionals**: "si A, fes X. Si B, fes Y."
5. **Verificació**: com saber que s'ha resolt.
6. **Prevenció**: com evitar-ho en el futur.

### Bones pràctiques

- **Escriu'l quan resols un incident**, no abans.
- **Un runbook per incident**, no pas un per categoria.
- **Actualitza'l** quan canvies el sistema.
- **Prova'l** amb un company o tu mateix.
- **Inclou captures** si cal.

## 55.9 Runbook vs documentació general

| Runbook | Documentació general |
|---|---|
| Pas a pas | Explicatiu |
| Per a un problema concret | Per a un tema general |
| Resolt ja | Pot ser teòric |
| Testejat | Pot ser aproximat |
| Llarg (10-20 passes) | Pot ser curt |

## 55.10 Runbooks a GitHub

Al repo del BernatLab, els runbooks són a `homelab/runbooks/`. Això permet:

- **Versionat**: cada canvi queda registrat.
- **Col·laboració**: altres poden millorar-los.
- **Còpia de seguretat**: estan al núvol.
- **Historial**: pots veure com era abans.

## 55.11 Plantilla al repo

Crea `homelab/runbooks/TEMPLATE.md`:

```markdown
# Runbook: [Títol]

## Símptomes
- 

## Diagnòstic
1. 
2. 

## Solució
1. 
2. 

## Verificació
- [ ] 
- [ ] 

## Prevenció
- 

## Contactes
- 

## Última actualització
- Data: 
- Per: 
- Canvis: 
```

## 55.12 Com millorar els runbooks

Cada vegada que resols un incident:

1. **Escriu el runbook** si no existeix.
2. **Actualitza'l** si existeix.
3. **Prova'l** la propera vegada.
4. **Comparteix-lo** amb la família/amics si pot ajudar.

## 55.13 Errors habituals

**Error 1: runbooks massa genèrics**.

"Si tens un problema, mira els logs" no és un runbook. Ha de tenir comandes específiques.

**Error 2: runbooks desactualitzats**.

Si canvies el sistema, el runbook queda obsolet. Cal revisar-los periòdicament.

**Error 3: runbooks que ningú llegeix**.

Guarda'ls on es trobin fàcilment. Referencia'ls a les alertes.

**Error 4: runbooks sense prova**.

Si no l'has provat, pot ser incorrecte. Prova'l!

## 55.14 Resum

Els runbooks són la documentació operativa per excel·lència. Pas a pas, específics, testejats. Es creen quan resols un incident, no pas abans. Al repo del BernatLab, a `homelab/runbooks/`. En el proper capítol veurem com diagnosticar i resoldre problemes quan les coses fallen.

## 55.15 Exercicis pràctics

1. Crea l'estructura `~/homelab/runbooks/`.
2. Escriu 3 runbooks per a incidents que ja has tingut.
3. Crea un README que indexi tots els runbooks.
4. Prova un runbook amb una situació simulada.
5. Enllaça els runbooks a les alertes de Grafana.
6. Fes commit al repo i comparteix-los.

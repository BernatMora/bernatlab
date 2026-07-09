# Capítol 41 — Privadesa i bones pràctiques: què NO enviar a la IA

> *"La privadesa no és una opció, és una responsabilitat. Quan l'IA és al núvol, no saps on van les teves dades. Quan és a casa, saps exactament què passa."*

## 41.1 Per què la privadesa importa, fins i tot en local

Pot semblar que si tens un model local, la privadesa està garantida. Però hi ha paranys:

1. **Dades d'entrada**. Encara que el model no surti del teu Mac, el que hi escrius pot quedar en logs, historial, obert en finestres, capturat per altres aplicacions.

2. **Metadades**. El fet que facis servir IA en determinats moments és informació. Si vols amagar que estàs consultant temes mèdics, o legals, o polítics, cal mesures.

3. **Dades compartides**. Si comparteixes el client amb altres persones (família, veïns), cada usuari pot veure les converses dels altres.

4. **Sortida accidental**. Un model pot filtrar informació privada en les respostes. Per exemple, si els documents contenen dades personals, el RAG els pot reproduir.

5. **Emmagatzematge**. Les converses, si les guardes, contenen dades sensibles. Cal xifrar-les o esborrar-les.

## 41.2 El que NO has d'enviar a una IA al núvol

**Regla d'or**: si una dada és prou sensible per no explicar-la a un desconegut al carrer, no l'enviïs a cap servei d'IA al núvol.

Categories específiques:

1. **Dades mèdiques**: informes, proves, historial, medicació, salut mental.
2. **Dades financeres**: números de compte, salaris, inversions, impostos.
3. **Identificadors personals**: DNI, NIE, passaport, targeta sanitària, número de la Seguretat Social.
4. **Contrasenyes i tokens**: mai, ni tan sols parcials.
5. **Correspondència privada**: cartes, missatges personals, fotos íntimes.
6. **Dades d'algú sense consentiment**: fotos d'altres, informació de tercers.
7. **Secrets comercials o professionals**: receptes, plànols, codi propietari, llistes de clients.
8. **Localització en temps real**: adreça de casa, ubicació de vacances, etc.
9. **Menors**: informació sobre nens, fotos d'escola, dades escolars.
10. **Activitat il·legal**: res que pugui ser delicte, encara que sigui per "curiositat".

Això és vàlid **fins i tot amb empreses que diuen ser privades** (Claude, ChatGPT, Gemini). Les seves polítiques poden canviar, i els seus sistemes poden tenir bretxes.

## 41.3 Avantatges específics de la IA local

Quan el model és a casa teva, els avantatges són clars:

1. **Cap transmissió externa**. Les dades no viatgen per Internet.
2. **Sense terme de servei**. No hi ha cap empresa que decideixi què pots o no pots fer.
3. **Sense canvis de política**. Avui ChatGPT és "privat", demà canvia la política.
4. **Inspeccionable**. Pots mirar exactament què fa el model.
5. **Personalitzable**. Pots afinar-lo amb les teves dades sense compartir-les.
6. **Funciona offline**. Sense Internet, funciona igual.

Això és especialment important per a:

- **Professionals sanitaris** que volen assistència amb casos.
- **Advocats** que treballen amb informació privilegiada.
- **Empresaris** amb dades financeres o clients.
- **Famílies** amb informació sobre menors.
- **Activistes** o periodistes en entorns hostils.

## 41.4 Bones pràctiques amb IA local

Encara que la IA sigui local, cal seguir bones pràctiques:

### 1. Configura bé el tallafocs

Assegura't que Ollama només escolta a les xarxes de confiança:

```bash
# Talla tot el tràfic a Ollama excepte Tailscale
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /Applications/Ollama.app
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --block /Applications/Ollama.app
# Permet només a la xarxa Tailscale
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblock /Applications/Ollama.app
```

### 2. Limita les xarxes

Si vols ser estricte, fes que Ollama escolti només a `100.64.0.0/10` (la xarxa Tailscale):

```bash
OLLAMA_HOST=100.115.134.76:11434 ollama serve
```

### 3. Autentica l'accés

Si exposa l'API a la xarxa, afegeix autenticació amb Caddy o Nginx:

```caddyfile
ollama.bernat.local {
    basicauth {
        bernat $2a$14$...
    }
    reverse_proxy localhost:11434
}
```

### 4. Xifra l'emmagatzematge

Si el teu Mac té FileVault activat (macOS ho activa per defecte), l'emmagatzematge ja està xifrat. Si no:

```bash
# Activar FileVault
fdesetup enable
```

Això xifra tot el disc dur amb la teva contrasenya d'inici de sessió.

### 5. Neteja les dades temporals

Whisper crea fitxers temporals amb l'àudio. Assegura't que s'esborrin:

```python
try:
    # Processar àudio
finally:
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)
```

### 6. Configura la retenció de logs

Per defecte, Ollama no guarda logs de les peticions. Però el servidor web sí:

```python
# A FastAPI, configura el logger per no guardar res sensible
import logging
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
```

### 7. Limita el context

Si el model té accés a molts documents, pot filtrar informació sensible. Configura bé la RAG per limitar l'accés.

### 8. Audita periòdicament

Revisa cada mes:
- Quins documents estan a la base vectorial.
- Quines converses s'han guardat.
- Qui té accés al sistema.
- Si hi ha actualitzacions de seguretat pendents.

## 41.5 Com gestionar converses multi-usuari

Si comparteixes el sistema amb família, amics, o veïns, cal:

1. **Autenticació per usuari**. Cada persona té el seu compte.
2. **Aïllament de dades**. Les converses d'un no es veuen per l'altre.
3. **Auditoria**. Qui ha fet què.
4. **Permisos**. Qui pot accedir a quins documents.

Implementació amb FastAPI:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

USERS = {
    "bernat": "contrasenya_bernat",
    "anna": "contrasenya_anna",
    "joan": "contrasenya_joan"
}

def autenticar(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if username not in USERS or USERS[username] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credencials incorrectes"
        )
    return username

# Cada usuari té la seva col·lecció
@app.get("/api/preguntar")
def preguntar(q: str, usuari: str = Depends(autenticar)):
    col_name = f"hort_osona_{usuari}"
    # ...
```

Ara cada usuari té el seu aïllament.

## 41.6 Com evitar que el RAG filtri informació sensible

Si els documents d'Hort Osona contenen dades personals, el RAG les pot reproduir. Per evitar-ho:

1. **Neteja els documents abans d'indexar**. Esborra noms, adreces, telèfons, DNI.
2. **Filtra els fragments retornats**. Si un fragment conté dades sensibles, exclou-lo.
3. **Limita l'accés per usuari**. Cada usuari té la seva vista.
4. **Marca la informació sensible**. Un sistema de tags per evitar la indexació.

Exemple de filtratge:

```python
def es_sensible(text: str) -> bool:
    """Detecta si un text conté dades sensibles."""
    indicadors = [
        "DNI", "NIE", "targeta", "contrasenya",
        "@gmail.com", "@hotmail.com", "telèfon",
        "adreça", "carrer", "número"
    ]
    text_lower = text.lower()
    return any(ind.lower() in text_lower for ind in indicadors)

def cerca_filtrada(consulta: str, k: int = 4) -> list:
    resultats = collection.query(query_texts=[consulta], n_results=k*2)
    fragments_net = []
    for i, frag in enumerate(resultats['documents'][0]):
        if not es_sensible(frag):
            fragments_net.append({
                "text": frag,
                "font": resultats['metadatas'][0][i]['source'],
                "distancia": resultats['distances'][0][i] if 'distances' in resultats else 0
            })
        if len(fragments_net) >= k:
            break
    return fragments_net
```

## 41.7 Com gestionar el "dret a l'oblit"

Si un usuari vol esborrar totes les seves dades, cal:

1. **Esborrar la seva col·lecció vectorial**.
2. **Esborrar el seu historial de converses**.
3. **Esborrar els seus logs**.
4. **Confirmar per escrit** que s'ha fet.

Script d'esborrat:

```python
def oblidar_usuari(usuari: str):
    """Esborra totes les dades d'un usuari."""
    # Esborrar col·lecció
    col_name = f"hort_osona_{usuari}"
    try:
        client.delete_collection(col_name)
    except:
        pass

    # Esborrar historial
    historial_path = Path(f"./historial/{usuari}.json")
    if historial_path.exists():
        historial_path.unlink()

    # Esborrar logs
    logs_path = Path(f"./logs/{usuari}.log")
    if logs_path.exists():
        logs_path.unlink()

    print(f"Dades de {usuari} esborrades correctament")
```

## 41.8 Bones pràctiques amb prompts

A l'hora de fer prompts, pensa:

1. **No comparteixis informació personal identificable** (PII) si no és estrictament necessari.
2. **Usa noms falsos** per a persones en exemples.
3. **Esborra la informació sensible** de les respostes del model abans de desar-les.
4. **Configura el system prompt** perquè el model eviti inventar dades personals:

```
Si et demanen informació personal d'algú, respon "No tinc aquesta
informació" en lloc d'inventar-la.
```

## 41.9 Com auditar el sistema

Un cop al mes, revisa:

1. **Quins documents estan indexats**: `ls vectorstore/`
2. **Quines converses s'han desat**: `ls historial/`
3. **Quins logs hi ha**: `tail logs/assistant.log`
4. **Qui ha accedit**: revisar logs d'autenticació
5. **Quines actualitzacions hi ha**: `ollama list`, `pip list --outdated`

Un script d'auditoria:

```python
def auditar_sistema():
    print("=== Auditoria mensual del sistema ===\n")
    print(f"Documents indexats: {collection.count()}")
    print(f"Converses guardades: {len(list(Path('historial').glob('*.json')))}")
    print(f"Mida de la base vectorial: {sum(f.stat().st_size for f in Path('vectorstore').rglob('*')) / 1e6:.1f} MB")
    print(f"Mida de l'historial: {sum(f.stat().st_size for f in Path('historial').rglob('*')) / 1e6:.1f} MB")
    # Més coses...
```

## 41.10 Què fer si hi ha una bretxa

Si sospites que algú ha accedit al sistema sense permís:

1. **Desconnecta l'API** (`pkill ollama`).
2. **Canvia les contrasenyes** (Tailscale, sistema, etc.).
3. **Revisa els logs** per veure què s'ha fet.
4. **Notifica als afectats** si hi ha dades personals.
5. **Reinstaŀla Ollama** des de zero.
6. **Re-indexa** els documents.
7. **Documenta la incidència** al README.

## 41.11 Compliment normatiu

A Espanya i la UE, el Reglament General de Protecció de Dades (RGPD) i la Llei Orgànica de Protecció de Dades (LOPDGDD) apliquen. Amb IA local, tens molt bon posicionament, però encara cal:

1. **Consentiment informat**: si altres persones usen el sistema.
2. **Transparència**: explicar què es fa amb les dades.
3. **Minimització**: només recull el que necessitis.
4. **Limitació de la finalitat**: no usar les dades per a altres coses.
5. **Integritat i confidencialitat**: protegir-les.
6. **Responsabilitat proactiva**: poder demostrar que compleixes.

Documenta tot això en una **Política de Privacitat** si el sistema és compartit.

## 41.12 Bones pràctiques amb el backup

Quan fas còpies de seguretat, xifra-les:

```bash
# Backup xifrat amb gpg
tar -czf - ~/bernatlab/asistent/ | gpg -c > backup-asistent-$(date +%Y%m%d).tar.gz.gpg
```

Això xifra la còpia amb una contrasenya. Guarda la contrasenya en un gestor de contrasenyes (1Password, Bitwarden, KeePass).

## 41.13 Resum

Hem après les bones pràctiques de privadesa per a sistemes d'IA local: què no enviar al núvol, com configurar el tallafocs i l'autenticació, com gestionar múltiples usuaris, com evitar filtracions del RAG, com auditar, i com complir la normativa. Al proper capítol veurem 10 consultes reals que pots fer a l'assistent Hort Osona per començar a usar-lo de manera pràctica.

## 41.14 Exercicis pràctics

1. Fes una llista de quines dades personals tens a les fitxes d'Hort Osona.
2. Configura el tallafocs del Mac per permetre Ollama només des de Tailscale.
3. Activa FileVault si no el tens activat.
4. Implementa autenticació bàsica al backend.
5. Configura la neteja automàtica de fitxers temporals.
6. Crea un script d'auditoria mensual.
7. Documenta al README la política de privadesa del sistema.

Paraules clau: **privadesa, privacy, GDPR, RGPD, LOPDGDD, dades personals, PII, identificació, biometria, consentiment, transparència, minimització, finalitat, integritat, confidencialitat, responsabilitat proactiva, política de privadesa, tallafocs, firewall, FileVault, xifrat, encryption, autenticació, basicauth, OAuth, JWT, multi-usuari, aïllament, retenció de dades, dret a l'oblit, esborrat, compliança, auditoria, logs, monitoratge, alerting, backup xifrat, gpg, contrasenya, gestor de contrasenyes, KeePass, Bitwarden, 1Password, model local, Ollama, Tailscale, xarxa privada, IP, tallafocs per IP, subnet, ACL, MAC filtering, port forwarding, NAT, port, 11434, 8080, 0.0.0.0, localhost, 100.x, 192.168, mTLS, TLS, certificat, client certificate, mutual TLS, fingerprint, verificació, prompt injection, sanitization, validació, escape, sandbox, contenidor, Docker, aïllament, recursos, cgroup, namespace, seccomp, AppArmor, SELinux, hardening, CIS, NIST, security baseline, OWASP, top 10, application security, dependency, vulnerabilitat, CVE, update, patch, manteniment**.

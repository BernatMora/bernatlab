# Exercici practic - Capitol 9: Privadesa de la IA

> 30-40 min · Real al teu sistema

## Objectiu
Auditar la privadesa del teu sistema d'IA al BernatLab, identificar possibles fuites, i implementar bones practiques. Acabaras amb un sistema mes segur i un document d'autoavaluacio.

## Requisits

- Ollama ja instal·lat
- 30-40 minuts
- Paciencia per fer una auditoria honesta

## Pas 1: Inventari de dades (10 min)

Crea un fitxer `inventari_dades.md` amb totes les dades que el teu sistema d'IA pot processar o veure:

```markdown
# Inventari de dades - BernatLab IA

## Dades personals
- [ ] Logs del sistema (poden contenir IPs, noms)
- [ ] Correus processats
- [ ] Documents personals
- [ ] Historial de navegacio
- [ ] Configuracio del servidor

## Dades de l'hort
- [ ] Lectures de sensors (temperatura, humitat)
- [ ] Imatges de les plantes
- [ ] Calendari de sembra
- [ ] Inventari d'eines

## Dades de negoci
- [ ] Correus de feina
- [ ] Documents financers
- [ ] Plans estrategics
- [ ] Contractes

## Dades d'altres persones
- [ ] Informacio sobre familia
- [ ] Informacio sobre amics
- [ ] Informacio sobre clients
- [ ] Metadades de comunicacions
```

Marca totes les que apliquin. Aquestes son les dades que NO hauries d'enviar a un LLM al nuvol sense anonimitzar.

## Pas 2: Auditar on s'envien dades (10 min)

```bash
# Comprovar si tens alguna crida a un LLM al nuvol
grep -r "api.openai.com" ~/bernatlab/ 2>/dev/null
grep -r "api.anthropic.com" ~/bernatlab/ 2>/dev/null
grep -r "api.gemini" ~/bernatlab/ 2>/dev/null
grep -r "api.mistral.ai" ~/bernatlab/ 2>/dev/null
```

Si trobes alguna referencia, documenta on i per que.

Ara comprova les connexions actives:

```bash
ss -tnp | grep -E '(443|11434|8080)'
```

Mira quines connexions TCP hi ha obertes. Si veus connexions a servidors externs, son intencionals?

## Pas 3: Auditar Ollama (5 min)

Verifica que Ollama nomes escolta a localhost:

```bash
ss -tlnp | grep 11434
```

Hauria de ser `127.0.0.1:11434` o `[::1]:11434`, NO `0.0.0.0:11434`.

Si escolta a 0.0.0.0, corregeix:

```bash
# Sistema
sudo systemctl edit ollama
# Afegeix: [Service] Environment="OLLAMA_HOST=127.0.0.1:11434"

# O simplement reinicia amb la variable
OLLAMA_HOST=127.0.0.1:11434 ollama serve
```

## Pas 4: Configurar Tailscale per acces remot segur (5 min)

Si vols accedir a Ollama des de fora de la xarxa local, usa Tailscale en lloc d'exposar el port:

```bash
# Instal·la Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Autentica't
sudo tailscale up

# Obten la teva IP a Tailscale
tailscale ip -4
```

Ara pots accedir a Ollama nomes desde dispositius autenticats a la teva xarxa Tailscale.

## Pas 5: Anonimitzar dades abans d'enviar (10 min)

Crea `anonimitzar.py` per netejar dades sensibles:

```python
import re

def anonimitzar(text):
    """Substitueix dades sensibles per placeholders."""
    # Emails
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL]', text)
    # IPs
    text = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[IP]', text)
    # Telefons
    text = re.sub(r'\+?\d{9,15}', '[TELEFON]', text)
    # NIF/DNI
    text = re.sub(r'\b\d{8}[A-Z]\b', '[NIF]', text)
    # Noms propis comuns (basica, no perfecta)
    text = re.sub(r'\b(Bernat|Maria|Joan|Laura)\b', '[NOM]', text)
    return text

# Prova
text_original = "El meu email es bernat@example.com i el meu telefon es 666777888."
text_netejat = anonimitzar(text_original)
print(f"Original: {text_original}")
print(f"Netejat:  {text_netejat}")
```

Integracio en un script RAG:

```python
from anonimitzar import anonimitzar
import ollama

pregunta_usuari = "Que em pots dir sobre bernat@example.com?"
pregunta_netejada = anonimitzar(pregunta_usuari)

# Ara podem enviar al LLM amb mes seguretat
resposta = ollama.chat(model='llama3.2:3b', messages=[
    {'role': 'user', 'content': pregunta_netejada}
])
```

## Pas 6: Xifrar la base de dades ChromaDB (5 min)

Si vols protegir la base de dades en cas de robatori del disc:

```bash
# Crear volum xifrat
sudo cryptsetup luksFormat /dev/sda2
sudo cryptsetup open /dev/sda2 bernatlab_data
sudo mkfs.ext4 /dev/mapper/bernatlab_data
sudo mount /dev/mapper/bernatlab_data /mnt/bernatlab
```

Ara mou ChromaDB a `/mnt/bernatlab/`:

```bash
mv ~/bernatlab-exercicis/M4/08-rag-complet/chroma_db /mnt/bernatlab/
ln -s /mnt/bernatlab/chroma_db ~/bernatlab-exercicis/M4/08-rag-complet/chroma_db
```

## Pas 7: Documentar la politica de privadesa (5 min)

Crea `politica_privadesa.md`:

```markdown
# Politica de privadesa - BernatLab IA

## Dades que processem
- Logs del sistema (anonimitzats)
- Lectures de sensors de l'hort
- Correus que l'usuari decideix processar
- Documents de l'usuari

## Com les processem
- Tots els models s'executen LOCALMENT (Ollama).
- Cap dada surt del servidor sense consentiment explicit.
- Les dades xifrades al disc (LUKS).

## Drets de l'usuari
- Acces: veure totes les dades emmagatzemades.
- Rectificacio: corregir dades incorrectes.
- Supressio: esborrar totes les dades.
- Portabilitat: exportar en format standard.

## Contacte
- Email: bernat@example.com
- Servidor: 100.x.y.z (Tailscale nomes)

## Revisio
- Aquesta politica es revisa cada 6 mesos.
- Ultima revisio: [data actual].
```

## Validacio

Has acabat si:

- [ ] Has inventariat les dades sensibles del sistema.
- [ ] Has auditat on s'envien dades (cap al nuvol sense voler).
- [ ] Has verificat que Ollama nomes escolta a localhost.
- [ ] Has configurat Tailscale (opcional pero recomanat).
- [ ] Has implementat anonimitzacio basica.
- [ ] Has xifrat la base de dades (opcional).
- [ ] Has escrit una politica de privadesa.

## Per aprofundir

- Investiga "differential privacy": tecnica per entrenar models sense veure dades individuals.
- Llegeix sobre "federated learning": entrenar models sense centralitzar dades.
- Compara les politiques de privadesa de OpenAI, Anthropic i Google. Son mes o menys protectores?
- Investiga "on-premise AI" vs "private cloud": opcions per a empreses.

## Ves un pas mes enlla

**Repte avançat**: Implementa un sistema de "data minimization" per al RAG:
1. Abans d'enviar un text al LLM, comprova si conte informacio personal.
2. Si en conte, aplica l'anonimitzacio adequada.
3. Guarda un registre de quines dades s'han enviat i quan.
4. Permet a l'usuari revisar i esborrar aquest registre.

Aixo es la base d'un sistema compliant amb GDPR.

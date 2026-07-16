# Exercici practic - Capitol 4: Prompt engineering

> 30-45 min · Real al teu servidor

## Objectiu

Experimentar amb diferents tecniques de prompt engineering aplicades a un cas real del BernatLab: analitzar logs del sistema. Comparar resultats de prompts dolents, regulars i optimitzats.

## Requisits

- Ollama instal·lat amb `llama3.2:3b` (o similar)
- 30-45 minuts
- ~100 MB d'espai lliure

## Pas 1: Crea un directori amb dades de prova (5 min)

```bash
mkdir -p ~/bernatlab-exercicis/M4/04-prompts/dades
cd ~/bernatlab-exercicis/M4/04-prompts/dades

# Crea un fitxer de logs simulats
cat > logs.txt << 'EOF'
Mar 15 03:42:17 rpi sshd[1234]: Failed password for root from 185.143.223.47 port 44231 ssh2
Mar 15 03:42:18 rpi sshd[1234]: Failed password for root from 185.143.223.47 port 44231 ssh2
Mar 15 03:42:19 rpi sshd[1234]: Failed password for root from 185.143.223.47 port 44231 ssh2
Mar 15 03:42:20 rpi sshd[1234]: Failed password for root from 185.143.223.47 port 44231 ssh2
Mar 15 03:42:21 rpi sshd[1234]: Failed password for root from 185.143.223.47 port 44231 ssh2
Mar 15 03:45:02 rpi sshd[1234]: Failed password for invalid user admin from 92.118.39.11 port 55210 ssh2
Mar 15 08:12:33 rpi cron[5678]: (root) CMD (test -x /usr/sbin/anacron || run-parts /etc/cron.daily)
Mar 15 12:01:00 rpi systemd[1]: Started Daily apt download activities.
Mar 15 12:05:23 rpi apt[9012]: Get:1 http://deb.debian.org/debian trixie/main arm64 libssl3 arm64 3.0.13-1~deb13u1 [2345 kB]
Mar 15 14:30:11 rpi dockerd[789]: containerd starts... container ff123abc started
Mar 15 18:22:45 rpi sshd[1456]: Accepted password for bernat from 192.168.1.50 port 51234 ssh2
Mar 15 18:23:01 rpi sudo: bernat : TTY=pts/0 ; PWD=/home/bernat ; USER=root ; COMMAND=/usr/bin/apt update
Mar 15 20:15:00 rpi ollama[3456]: [GIN] 2024/03/15 20:15:00 | 200 |    1.2s |  127.0.0.1 | POST     "/api/generate"
EOF

# Mostra el contingut
cat logs.txt
```

## Pas 2: Prompt MAL dissenyat (zero-shot sense contexte) (5 min)

```bash
curl -s http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Que hi ha en aquest log?",
  "stream": false
}' | jq -r '.response'
```

Observa la resposta. Probablement es massa generica o no enten que vols.

## Pas 3: Prompt millorat amb rol i contexte (10 min)

```bash
curl -s http://localhost:11434/api/chat -d '{
  "model": "llama3.2:3b",
  "messages": [
    {
      "role": "system",
      "content": "Ets un expert en seguretat informatica. Analitza logs de Linux en angles i respon sempre en catala. Sigues concis pero precís."
    },
    {
      "role": "user",
      "content": "Analitza aquest log d una Raspberry Pi 4 amb SSH obert a Internet. Indica: 1) quines anomalies veus, 2) el nivell de risc (1-5), 3) dues accions concretes a fer.\n\nLOG: '$(cat logs.txt | head -5 | tr "\n" " ")'"
    }
  ],
  "stream": false
}' | jq -r '.message.content'
```

Compara amb el Pas 2. Veus la diferencia?

## Pas 4: Few-shot amb exemples (10 min)

```bash
curl -s http://localhost:11434/api/chat -d '{
  "model": "llama3.2:3b",
  "messages": [
    {
      "role": "system",
      "content": "Ets un expert en seguretat. Classifica cada linia de log segons el risc."
    },
    {
      "role": "user",
      "content": "Exemple 1: '\''Jan 1 10:00 rpi cron[123]: CMD (run-parts /etc/cron.hourly)'\''\nRisc: BAIX. Es una tasca programada normal.\n\nExemple 2: '\''Jan 1 03:00 rpi sshd[456]: Failed password for root from 1.2.3.4 port 12345'\''\nRisc: ALT. Possible atac de força bruta.\n\nAra classifica aquesta linia: '\''Mar 15 03:42:17 rpi sshd[1234]: Failed password for root from 185.143.223.47 port 44231 ssh2'\''\n\nRespon en format:\nRisc: [BAIX/MITJA/ALT]\nMotiu: [1 frase]"
    }
  ],
  "stream": false
}' | jq -r '.message.content'
```

## Pas 5: Chain-of-thought (10 min)

```bash
curl -s http://localhost:11434/api/chat -d '{
  "model": "llama3.2:3b",
  "messages": [
    {
      "role": "system",
      "content": "Ets un expert en seguretat que raona pas a pas."
    },
    {
      "role": "user",
      "content": "Analitza aquesta linia de log:\n'\''Mar 15 03:42:17 rpi sshd[1234]: Failed password for root from 185.143.223.47 port 44231 ssh2'\''\n\nProcediment:\n1. Identifica el servei (sshd? cron? apt?).\n2. Identifica l esdeveniment (login fallit? exit? error?).\n3. Avalua la gravetat: es normal o sospitos?\n4. Recomana una accio concreta.\n\nRaona pas a pas i dona la teva conclusio final."
    }
  ],
  "stream": false
}' | jq -r '.message.content'
```

## Pas 6: Documenta la comparacio (10 min)

Crea `book/curs/M4/04-prompt-engineering/comparacio.md` amb:

| Tecnica | Prompt resum | Qualitat (1-5) | Utilitat |
|---|---|---|---|
| Mal prompt (zero-shot) | "Que hi ha en aquest log?" | ... | ... |
| Amb rol i contexte | ... | ... | ... |
| Few-shot | ... | ... | ... |
| Chain-of-thought | ... | ... | ... |

Afegeix conclusions: quina tecnica ha funcionat millor? Per que?

## Validacio

Has acabat si:
- [ ] Has provat el prompt MAL dissenyat.
- [ ] Has provat el prompt amb rol i contexte.
- [ ] Has provat el prompt amb few-shot.
- [ ] Has provat el prompt amb chain-of-thought.
- [ ] Has documentat la comparacio.

## Per aprofundir

- Prova el mateix amb un model mes gran (phi3:mini) i mira si canvia la qualitat.
- Investiga "self-consistency": fer la mateixa pregunta 5 cops i votar la resposta mes frequent.
- Crea un script Python que automatitzi l'analisi de logs amb el millor prompt que hagis trobat.
- Experimenta amb la "temperature" (0 = mes consistent, 1 = mes creatiu).

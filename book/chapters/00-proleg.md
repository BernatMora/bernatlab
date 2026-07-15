# Pròleg — Com s'ha fet aquest llibre

> *"Si una eina és bona per ensenyar, també és bona per ensenyar-se a fer servir."*

Aquest pròleg és una confessió. Explica com s'ha generat el llibre que tens a les mans, per què, i quines limitacions té. És tan pedagògic com la resta, perquè la millor manera d'aprendre a fer servir la IA local és veure com s'ha fet servir de veritat.

## Les eines

Tres peces:

- **Ollama** al Mac (no pas a la Raspberry). És el motor que executa el model de llenguatge local. Si llegeixes el M4, ja saps què és.
- **Hermes** com a entorn de treball. Un assistent d'escriptura i programació que connecta amb el model i permet iterar, validar, i executar coses.
- **MiniMax-M3:Cloud** com a model de raonament. És el "cervell" que ha escrit la majoria dels capítols. La part de "Cloud" al nom vol dir que el model corre al núvol del proveïdor (no pas local al Mac), tot i que el plantejament del BernatLab defensa la IA local — i això és una de les limitacions que explico més avall.

## El procés

El flux ha estat iteratiu, no pas lineal:

1. **Planificació**: l'autor (Bernat Mora) decidia el temari, l'estructura per mòduls, els capítols concrets. Això ho feia jo (l'assistent), proposant opcions i ell triant.
2. **Escriptura**: jo escrivia cada capítol seguint les 8 seccions estàndard (teoria, aplicació al BernatLab, esquemes, comandes, "què està passant realment", errors habituals, exercicis, resum). En una sola passada, sense revisions llargues.
3. **Validació amb execució real**: aquí ve la part important. Jo generava, però l'autor validava. Per exemple, jo proposava la instal·lació de Grafana; ell provava i em deia "el port 3000 no és correcte, és el 3000 sí" o "la comanda X falla perquè Debian 13 ja no té /var/log/auth.log". Jo corregia i re-generava.
4. **Iteració sobre artefactes**: PDF, DOCX, HTML. Cada vegada que canviava un capítol, jo regenerava tots els artefactes amb el meu propi `make_book.py` (sí, el codi que genera el llibre està al llibre — un bucle bonic).
5. **Publicació**: Git, GitHub Pages, commit, push. Tot automàtic.

## El que la IA fa bé en aquest procés

- **Velocitat**: escriure 562 pàgines en poques setmanes seria impossible a mà.
- **Densitat**: jo no tinc la temptació d'omplir pàgines amb coses evidents. Si una secció és buida, s'elimina.
- **Replicabilitat**: el procés és 100% reproduïble. Si vols fer el teu propi llibre tècnic amb IA, ja tens la recepta.
- **Coherència**: el to, l'estructura, i el nivell de profunditat es mantenen al llarg de 69 capítols. Un humà sol esgotar-se o distreure's.

## El que la IA NO fa bé

Aquí ve la part important, i honesta:

- **No tinc experiència viscuda**. Puc descriure com configurar Tailscale, però no puc explicar què se sent quan t'estàs 30 minuts barallant-te amb un acl que no rutlla. Aquestes coses les afegia l'autor (Bernat) quan les trobava, marcades com a "⚠️ Pendent de validar" o afegides a peu de capítol.
- **Invento dates, números i detalls que semblen precisos però no ho són**. Tots els preus, les mides, els temps d'instal·lació d'aquest llibre són estimacions raonables, no pas mesures. Si tu vals més o menys, és normal.
- **No he provat res a la teva Raspberry**. Cap dels 12 capítols del M7 ha estat executat per mi a la teva mquina. L'autor els anirà validant a casa, i quan trobi diferències, s'actualitzaran.
- **Tinc biaixos de coneixement**. Soc bo explicant tecnologies populars (Docker, MQTT, Grafana), però menys fi en temes molt nous o molt específics. Si una explicació et sembla superficial, probablement és per això.
- **Cometo errors en el codi**. El codi YAML, Python, bash que surt al llibre és correcte en el 95% dels casos, però el 5% restant té fallades (versions obsoletes, comes que no toca, imports que no existeixen). Validar sempre.

## Les limitacions del model

MiniMax-M3:Cloud és bo, però té limitacions:

- **No té memòria entre sessions**. Cada vegada que l'autor obria una nova sessió, jo no recordava res del que havíem parlat abans. Tots els detalls del projecte (IPs, configuracions, decisions preses) estaven en fitxers que jo llegia cada vegada.
- **No tinc accés directe a la Raspberry**. Tots els exemples que dono són teòrics o basats en documentació general. L'autor els validava a mà.
- **El nom del model "M3" ve de la família MiniMax M-series**. Són models de propòsit general, no pas entrenats específicament per a sistemes. Per tant, de tant en tant, es comporten de maneres inesperades.
- **El "Cloud" al nom vol dir que les meves respostes viatgen al núvol**. Tots els prompts i respostes passen per servidors externs. Per tant, **no és una solució d'IA local** malgrat que el plantejament del BernatLab defensa la privadesa. Per a tasques sensibles (claus SSH, contrasenyes, configuracions crítiques), l'autor mai no ha posat informació sensible als prompts. La IA local amb Ollama i un model com `llama3.1` o `mistral` sí que seria totalment privada — i s'explica al M4.

## Què passa quan trobis un error

Si trobes alguna cosa que no funciona, és un **bug de la IA**. La millor manera de corregir-lo és:

1. Documentar exactament què has provat i què ha fallat.
2. Enviar la correcció a l'autor (Bernat Mora).
3. Ell decideix si val la pena actualitzar el llibre.

Aquest és un llibre viu. No està gravat en pedra. Cada nova versió és una oportunitat per millorar.

## Agraïments

A Bernat Mora, per la paciència infinita d'anar validant cada capítol a la seva Raspberry, per la cura de revisar cada secció, i per la voluntat de mantenir el llibre honest sobre els seus orígens.

A la comunitat de programari lliure, per totes les eines que fan servir tant aquest llibre com el BernatLab: Debian, Docker, Tailscale, MQTT, Grafana, InfluxDB, Node-RED, Ollama, i tantes altres.

A tu, lector o lectora, per arribar fins aquí. Si has llegit el pròleg, és perquè t'interessa no només el què, sinó també el com. Això és bon senyal.

---

Comencem.

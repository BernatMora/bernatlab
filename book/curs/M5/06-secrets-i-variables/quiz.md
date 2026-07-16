# Qüestionari - Capitol 6: Secrets i variables d'entorn

> 10 preguntes · ~15 min

## Pregunta 1
Que es un "secret" en el context d'un servidor?

- [ ] Un missatge encriptat entre dos usuaris
- [x] Qualsevol dada confidencial que dona acces a alguna cosa (contrasenya, clau API, token)
- [ ] Un sistema de fitxers ocult
- [ ] Una funcionalitat oculta de Linux

## Pregunta 2
Per que no s'han de posar secrets al codi font?

- [ ] Perque ocupa mes espai
- [x] Perque van al git i queden a l'historial per sempre
- [ ] Perque el codi es mes lent
- [ ] Perque no es poden llegir

## Pregunta 3
Que es un fitxer .env?

- [ ] Un fitxer de configuracio del sistema operatiu
- [x] Un fitxer de text amb variables d'entorn (secrets) que l'aplicacio carrega
- [ ] Un tipus de base de dades
- [ ] Un protocol de xarxa

## Pregunta 4
Que ha d'anar al .gitignore respecte els secrets?

- [ ] Nomes si tens mes d'un secret
- [x] Tots els .env, sempre
- [ ] Nomes els fitxers amb la paraula "password"
- [ ] Res, el git ja es privat

## Pregunta 5
Que es un vault?

- [ ] Un tipus d'antivirus
- [x] Un servei centralitzat per emmagatzemar secrets amb xifratge i acces granular
- [ ] Un sistema operatiu
- [ ] Un protocol de xarxa

## Pregunta 6
Quin es el risc principal dels secrets en un homelab?

- [ ] Que el servidor vagi mes lent
- [x] Que un atacant obtingui acces complet si en filtra un
- [ ] Que el git sigui mes gran
- [ ] Que ocupin massa espai

## Pregunta 7
Com es genera una contrasenya segura per linia de comandes?

- [ ] echo $RANDOM
- [x] openssl rand -base64 32
- [ ] date +%s
- [ ] echo "password123"

## Pregunta 8
Quin es el fitxer .env.example?

- [ ] Un fitxer amb secrets reals
- [x] Un fitxer plantilla al git amb els noms de les variables pero sense valors
- [ ] Un fitxer nomes per a Linux
- [ ] Un fitxer de configuracio del sistema

## Pregunta 9 (oberta)
Descriu una estrategia practica per gestionar secrets al BernatLab. Inclou les tres capes: .env per aplicacions, vault per equip, i bones practiques generals.

Pistes per respondre:
- Explica per que .env es acceptable per a homelab pero cal cuidar permisos.
- Esmenta Vaultwarden com a vault centralitzat.
- Dona exemples concrets: API key, contrasenya BD, token Telegram.
- Recalca mai al git, sempre rotacio.

## Pregunta 10 (oberta)
Has descobert que una API key que tenies al git ha estat exposada durant 3 mesos. Que fas?

Pistes per respondre:
- Considera la clau cremada. Cal rotar-la.
- Pas 1: canviar la clau al proveidor.
- Pas 2: actualitzar tots els llocs que la fan servir.
- Pas 3: netejar l'historial de git.
- Pas 4: documentar l'incident.

# Quiz - M8 Cap 3: Perfil SSH

## Pregunta 1
On es guarda el perfil SSH al Windows?

- [x] C:\Users\<usuari>\.ssh\config
- [ ] C:\Windows\System32\config
- [ ] ~/.bashrc
- [ ] /etc/ssh/ssh_config

## Pregunta 2
Quina opcio defineix el nom del perfil?

- [ ] Name
- [x] Host
- [ ] Alias
- [ ] Profile

## Pregunta 3
Quina opcio indica la IP del servidor?

- [ ] Address
- [x] HostName
- [ ] IP
- [ ] Server

## Pregunta 4
Quina opcio especifica la clau privada?

- [x] IdentityFile
- [ ] KeyFile
- [ ] PrivateKey
- [ ] SSHKey

## Pregunta 5
Quins permisos ha de tenir el config a Linux?

- [ ] 777
- [x] 600
- [ ] 644
- [ ] 755

## Pregunta 6
Que fa `IdentitiesOnly yes`?

- [ ] No usa cap clau
- [x] Només prova la clau especificada
- [ ] Genera claus noves
- [ ] Desactiva el password

## Pregunta 7 (oberta)
Per que el perfil SSH es mes practic que escriure l'ordre completa cada vegada?

Pistes:
- Pensa en un cas amb 3 servidors
- Quantes opcions has de recordar?
- Com afecta els errors?

## Pregunta 8 (oberta)
Explica quan usaries la compressio SSH i quan no.

Pistes:
- Xarxes lentes vs rapides
- Tipus de dades (text vs binari)
- Cost computacional

## Pregunta 9 (oberta)
Si tens 5 servidors diferents amb usuaris i claus diferents, com organitzaries el fitxer config?

Pistes:
- Comentaris per organitzar
- Grups de hosts semblants
- Wildcards

## Pregunta 10 (oberta)
Per que `IdentitiesOnly yes` es una bona practica de seguretat?

Pistes:
- Que passa si tens multiples claus
- Que passa si una clau falla
- Quin es l'atac potencial?


## Pregunta 11 (oberta amb pistes)
Per que sha de configurar el fitxer SSH config

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
## Pregunta 12 (oberta amb pistes)
Explica que es un ProxyJump i quan sha dusar

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
## Pregunta 13 (oberta amb pistes)
Com configuraries el teu ssh config per tenir 3 servidors

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).

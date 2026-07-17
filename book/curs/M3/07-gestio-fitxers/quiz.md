# Qüestionari - Capitol 7: Gestio de fitxers al BernatLab

> 15 preguntes · ~20 min

## Pregunta 1
Quin es el gestor de fitxers web mes simple que es pot instalar al BernatLab?

- [ ] Nextcloud
- [x] File Browser
- [ ] ownCloud
- [ ] Apache

## Pregunta 2
Quin programari ofereix un nuvol personal complet tipus Google Drive?

- [ ] File Browser
- [x] Nextcloud
- [ ] Apache
- [ ] Nginx

## Pregunta 3
Quins permisos hauria de tenir un fitxer .env amb contrasenyes?

- [ ] 644
- [ ] 755
- [x] 600
- [ ] 777

## Pregunta 4
Quin directori arrel es el recomanat per organitzar les dades al BernatLab?

- [ ] /var/lib/bernatlab
- [x] /home/pi/bernatlab
- [ ] /srv/bernatlab
- [ ] /opt/bernatlab

## Pregunta 5
Quin es lavantatge principal de Nextcloud sobre File Browser?

- [ ] Es mes rapid
- [x] Ofereix sincronitzacio multi-dispositiu i apps natives
- [ ] Ocupa menys espai
- [ ] Es mes segur

## Pregunta 6
Quin protocol fan servir els clients de sincronitzacio de Nextcloud?

- [ ] FTP
- [ ] SMB
- [x] WebDAV + API propia
- [ ] SFTP

## Pregunta 7
Quin format de data es el recomanat per noms de fitxers?

- [x] ISO (YYYY-MM-DD)
- [ ] Europeu (DD-MM-YYYY)
- [ ] American (MM/DD/YYYY)
- [ ] Unix timestamp

## Pregunta 8
Quin es linconvenient principal de Nextcloud en una Raspberry Pi 4?

- [ ] No es pot instalar
- [x] Consumeix bastanta RAM
- [ ] No es segur
- [ ] No te clients per a mobil

## Pregunta 9 (oberta)
Dissenya lestructura de carpetes per a un hort amb 5 bancals i 3 sensors per bancal. Com ho organitzaries per a que sigui facil de navegar i backupejar?

Pistes per respondre:
- Quines carpetes principals tindras?
- On posaries les fotos, els documents, les dades?
- Com anomenaries les carpetes de cada bancal?
- On posaries els logs i les configuracions?

## Pregunta 10 (oberta)
Un amic vol muntar un nuvol personal per sincronitzar 200 GB de fotos entre PC, mobil i tablet. Recomanaries File Browser o Nextcloud? Argumenta la decisio.

Pistes per respondre:
- File Browser nomes es per a un sol usuari manualment
- Nextcloud te clients per a tots els sistemes
- La RPi 4 te 4 GB de RAM: pot amb Nextcloud?
- Quin cost te cada opcio?

## Pregunta 11 (oberta)
Per que creus que Nextcloud sha fet tan popular en l'ambit self-hosted tot i la competència (ownCloud, Seafile, etc)? Quin valor afegit te per al BernatLab?

Pistes per respondre:
- Ecosistema gran (apps, integracions).
- Comunitat activa i desenvolupament constant.
- Compatibilitat amb protocols estandard (WebDAV, CalDAV).
- Maduresa vs innovacio: ownCloud va perdre pistonada.

## Pregunta 12 (oberta)
Quina relacio hi ha entre lestructura de carpetes i leficiencia del backup al BernatLab? Com afecta tenir carpetes ben organitzades a la mida i rapidesa dels backups?

Pistes per respondre:
- Carpetes petites es poden comprimir rapidament.
- Backups incrementals son mes eficients amb estructura jerarquica.
- Exclou carpetes temporal o de cache redueix la mida.
- Exemple: separar /home/pi/bernatlab/fotos/ de /home/pi/bernatlab/cache/.

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "per que complicar-te amb carpetes organitzades? Ho deixo tot a /home/pi/Downloads/ i ja esta". Argumenta per que aixo es una mala practica al BernatLab, especialment a llarg termini.

Pistes per respondre:
- Dificil de trobar coses d'aqui 6 mesos.
- Backup massa gran (inclou coses innecessaries).
- Impossibilitat de politiques diferents per tipus de dada.
- Analogy: habitacio desordenada vs endreçada.

## Pregunta 14 (oberta)
Aplica el concepte de gestio de fitxers al cas concret del BernatLab amb lhort IoT i l'aplicacio Hort Osona. Tinc 100 fotos de plantes, 50 fitxers markdown amb informacio, 1 base de dades ChromaDB amb embeddings, 1 script Python. Organitza aquesta estructura de carpetes pensant en la facilidad de backup i en lexposicio publica.

Pistes per respondre:
- Carpeta publica (accessible via web): fotos, markdowns.
- Carpeta privada (no exposada): ChromaDB, scripts.
- Fitxer de configuracio separat (.env).
- Estructura versionada vs no versionada.

## Pregunta 15 (oberta)
Quines consequencies te per a la privacitat tenir fitxers personals al BernatLab (especialment si es accessible des d'internet)? Quines mesures de seguretat aplicaries per defecte? Argumenta amb exemples.

Pistes per respondre:
- Nextcloud o File Browser exposats = porta dentrada.
- Autenticacio obligatoria (no anonymous).
- HTTPS obligatori.
- Permisos de fitxer correctes (600 per secrets).
- Logs d'acces.
- Trade-off: conveniencia vs seguretat.

# Respostes - M8 Cap 2: MobaXterm

## Pregunta 1: Que es MobaXterm?

**Resposta correcta**: Un client SSH grafic per a Windows.

**Explicacio**: MobaXterm es un client de terminal amb funcions SSH avançades per a Windows. Es com tenir una "navalla suissa" per accedir a servidors Linux des de Windows.

---

## Pregunta 2: Edicio gratuita?

**Resposta correcta**: Home Edition.

**Explicacio**: La Home Edition es la versio gratuita. Te limitacions (12 sessions, 4 simultanies, banner) pero es mes que suficient per a la majoria d'usuaris personals.

---

## Pregunta 3: Maxim de sessions simultanies?

**Resposta correcta**: 4.

**Explicacio**: La Home permet maxim 4 sessions SSH actives alhora. Si necessites mes, cal la Professional (70 USD) oberta a "unlimited" o tancar una per obrir una altra.

---

## Pregunta 4: Transferencia de fitxers?

**Resposta correcta**: Arrossegant fitxers al navegador SFTP de l'esquerra.

**Explicacio**: MobaXterm te un navegador SFTP integrat a la columna esquerra. Pots arrossegar i deixar anar fitxers entre el teu PC i el servidor, com si fos l'explorador de Windows.

---

## Pregunta 5: Port forwarding?

**Resposta correcta**: Per accedir a ports interns de la RPi des del Windows.

**Explicacio**: El port forwarding (tunel SSH) et permet obrir un port al teu Windows que redirigeix a un port del servidor. Es molt util per accedir a serveis que nomes escolten internament (com Grafana, Portainer, etc.).

---

## Pregunta 6: On es guarden?

**Resposta correcta**: En un fitxer MobaXterm.ini.

**Explicacio**: Totes les sessions i configuracio es guarden en un fitxer .ini. Es pot fer backup, sincronitzar entre PCs, o versionar amb Git (tot i que no es recomana, te claus i passwords).

---

## Pregunta 7: Codificacio?

**Resposta correcta**: UTF-8.

**Explicacio**: UTF-8 es la codificacio estandard per a la majoria d'idiomes, inclos el catala. Si tens caracters raros (Ã©, Ã±, etc.), es que la codificacio no esta ben configurada.

---

## Pregunta 8 (oberta): Per que millor que PowerShell?

**Resposta model**:

MobaXterm es millor que PowerShell per treballar amb servidors Linux perque:

- **Transferencia de fitxers integrada**: arrossegar i deixar anar, doble click per editar. PowerShell necessita WinSCP o similars.
- **Sessions guardades**: nomes un clic per connectar. PowerShell necessita recordar IP, port, usuari.
- **Port forwarding grafic**: configurar un tunel en 3 camps. PowerShell necessita `netsh` o `ssh -L` per linia de comandes.
- **Multiples pestanyes organitzades**: veus totes les sessions obertes a la barra. PowerShell permet pestanyes pero no es tan net.
- **X11 forwarding**: si vols executar aplicacions graficament de Linux a Windows, nomes funciona amb MobaXterm (o VcXsrv).
- **Navegador de fitxers visual**: veus la estructura de carpetes del servidor com un explorador.

**Per a PowerShell nomes**, tot es mes complicat. Per a scripting, PowerShell pot ser millor (pero per aixo hi ha bash a la RPi).

---

## Pregunta 9 (oberta): Cas d'us real

**Resposta model**:

Un cas molt comu es accedir a **Grafana** (que nomes escolta a `localhost:3000` a la RPi per seguretat).

Sense port forwarding:
- No pots accedir des del Windows (perque Grafana nomes escolta a localhost).
- Hauries de canviar la configuracio de Grafana per escoltar a 0.0.0.0 (menys segur).
- O canviar el port a 3000 al router (encara menys segur).

Amb MobaXterm port forwarding:
1. Configures un tunel: port local 3000 -> localhost:3000 a la RPi.
2. Al navegador del Windows obres `http://localhost:3000`.
3. La connexio viatja xifrada per SSH, nomes tu hi accedeixes, sense tocar el router.

**Altres exemples**:
- Accedir a **Portainer** quan nomes escolta a localhost.
- Accedir a una **base de dades** PostgreSQL amb pgAdmin.
- Accedir a un **Jupyter Notebook** que nomes escolta a localhost.
- **Provar webs** abans de fer deploy.

---

## Pregunta 10 (oberta): Val la pena pagar?

**Resposta model**:

**Arguments a favor de pagar**:
- Mes sessions simultanies (util si tens molts servidors).
- Sense banner d'inici.
- Suport professional.
- No limitacio de 12 sessions guardades.

**Arguments en contra**:
- La Home Edition es mes que suficient per a un homelab personal.
- 4 sessions simultanies es raonable (si en necessites mes, probablement tens massa finestres obertes).
- Hi ha alternatives gratuites:
  - **Tabby** - terminal modern, multiplataforma.
  - **Windows Terminal** - ja l'hauries de tenir, basic pero bo.
  - **WSL (Windows Subsystem for Linux)** - tens un Linux dins el Windows.
  - **VS Code Remote SSH** - si ja uses VS Code.

**La meva recomanacio**:
- Comenca amb la Home Edition.
- Si mai arribes als limits, valora la Professional.
- Si vols maxim control, prova **Tabby** o **VS Code Remote SSH**.

---

## Què fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i provar MobaXterm.
- **3-4 encerts**: Descarrega i instal·la MobaXterm, segueix l'exercici pas a pas.
- **0-2 encerts**: Comença per descarregar MobaXterm i fer la primera connexio.

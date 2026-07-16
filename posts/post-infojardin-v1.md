# Post a Infojardín — Esborrany 1

**Títol:** "M'he muntat un sistema per controlar l'hort amb una Raspberry (i funciona)"

**Secció suggerida:** HORTICULTURA GENERAL / TECNOLOGIA o HERRAMIENTAS DE JARDINERÍA

---

Bon dia a tothom,

Us vull explicar una cosa que he estat fent aquest any al meu hort d'Osona. No soc enginyer ni informàtic, soc pagès. Però sempre m'ha agradat entendre les coses i tenir les dades a mà, així que m'he anat muntant un petit sistema per controlar el meu hort amb una Raspberry Pi. Avui ja funciona, i vull compartir-ho per si algú s'anima.

**Què tinc muntat:**

Al camp tinc uns sensors que mesuren la temperatura, la humitat de l'aire, la humitat de la terra i la pressió. Són sensors petits, barats (tot plegat deu fer uns 50 €), que van amb bateries i envien les dades per ràdio a 868 MHz. No cal posar-los cable.

A casa tinc una Raspberry Pi 4 (ordinador molt petit, 50 €) que rep les dades i les desa. Des del mòbil puc veure gràfiques de com ha estat l'hort els últims dies, i rebo avisos al Telegram quan alguna cosa no va bé (per exemple, si la temperatura baixa de 5 °C o si un sensor deixa d'enviar).

També tinc una web pública on es pot veure l'estat de l'hort: hort-osona.cat (o l'URL que tinguis). No és gaire bonica, però funciona.

**Per què ho explico:**

Perquè quan jo vaig començar no sabia ni per on. Vaig perdre molt de temps buscant informació, mirant fòrums anglesos, comprant coses que no em servien. Si algú altre vol fer una cosa semblant, potser li estalvio uns quants caps de setmana.

**El que NO és:**

No és una cosa professional. No soc cap empresa. No venc res. No és tampoc un sistema "llest per usar" — te l'has de muntar tu, amb paciència, llegint una mica.

**El que SÍ és:**

Un sistema casolà, fet amb eines lliures, que a mi em funciona i que em dóna la tranquil·litat de saber què passa al meu hort quan soc fora o quan dormo.

**Si us animeu:**

He escrit un llibre d'unes 580 pàgines explicant pas a pas com muntar-ho tot, des de com connectar la Raspberry per primer cop fins a com rebre alertes al mòbil. És en català, és gratuït, i el trobareu aquí:

👉 https://bernatmora.github.io/bernatlab/

També tinc una web amb les dades del meu hort concret:

👉 https://bernatmora.github.io/hort-osona/

Si teniu preguntes, o si voleu que expliqui alguna part amb més detall, aquí em tindreu.

Salut!
Bernat

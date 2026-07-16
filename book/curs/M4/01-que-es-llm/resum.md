# Resum - Capitol 1: Que es un LLM

## La idea clau

Un **LLM** (Large Language Model) es un programa que ha après a parlar llegint milers de milions de textos. No "entén" res com nosaltres, pero es molt bo calculant quina paraula ve despres d'una altra. Si li dones prou context, pot semblar que sap de que parla. I aixo es la trampa: semblar que sap no es el mateix que saber.

## Que es exactament un LLM?

Un LLM es una **xarxa neuronal** entrenada amb moltissim text. La gracia esta en que no te cap regla escrita a dins: nomes te milers de milions de numeros (els "pesos") que ha anat ajustant durant l'entrenament. Quan li escrius "Bon dia, com", el model fa els calculs i et diu que probablement la paraula que ve despres es "estàs".

Aixo, repetit milers de vegades, es el que fa que escrigui paragrafs sencers, que resumeixi articles o que t'ajudi a fer un script.

## Com funciona per dins (sense matemàtiques)

Pensa-ho com tres fases:

- **Entrenament**: el llegeix Internet (llibres, articles, codi, forums) i va ajustant els seus numeros per encertar la paraula seguent.
- **Context**: quan li envies un missatge, l'afegeix a una "finestra" de memoria. Tot el que hi cap ho pot fer servir per respondre.
- **Resposta**: va generant paraula a paraula, triant la que estadisticament te mes probabilitats de ser la bona.

**Important**: no consulta cap base de dades en temps real. Tot el que sap ho porta "dins" del model (als pesos). Si li preguntes coses que no son al seu entrenament, s'inventa coses amb cara de veritat (les anomenades "al·lucinacions").

## Per que serveix al BernatLab?

Al nostre homelab, un LLM local ens pot ajudar a:

- **Resumir logs** de la Raspberry Pi per trobar anomalies.
- **Generar scripts** a partir d'una descripcio en llenguatge natural.
- **Respondre preguntes** sobre la base de coneixement de l'Hort Osona (aixo es el RAG que veurem mes endavant).
- **Traduir** correus i documentacio tecnica.
- **Assistir-nos** quan configurem un servei nou.

Tot sense enviar dades a cap servidor extern. Pero per aixo, cal que el model corri **a casa nostra**, no al núvol d'OpenAI o Google. I d'aqui ve Ollama, que es la eina que veurem al capítol 2.

## Diferencia entre LLM, IA i Machine Learning

Hi ha molta confusio amb aquests termes. Posem ordre:

- **IA (Intel·ligència Artificial)**: qualsevol programa que imita comportament intel·ligent. Inclou desde un joc d'escacs dels anys 80 fins al ChatGPT.
- **Machine Learning (ML)**: una branca de la IA on el programa aprenia partir de dades, no de regles escrites a ma.
- **Xarxa neuronal**: un tipus concret de ML inspirat en el cervell.
- **LLM**: una xarxa neuronal entrenada amb molt text per fer feines de llenguatge.

Un LLM es, per tant, una peça molt especifica dins de la gran familia de la IA. I es la que ens interessa per fer-nos la vida mes facil al servidor.

## Limitacions que cal conèixer

- **Al·lucinacions**: s'inventa coses amb tota naturalitat. Mai no li demanis dades exactes sense verificar.
- **Finestra de context**: nomes recorda els ultims N tokens (normalment 4k-128k). Si el text es llarg, l'inici se li oblida.
- **Data de tall**: el model va ser entrenat fins a una data concreta. No sap que ha passat despres.
- **No es determinista**: la mateixa pregunta pot donar respostes diferents. Cal temperatura baixa si vols respostes estables.
- **No raona com un huma**: encara que sembli que raona, nomes fa calculs estadistics.

## Com elegir-ne un? (vista general)

Al capítol 3 ho veurem a fons, pero com a anticip:

- **Models petits (1B-3B)**: corren a qualsevol RPi 4 amb 4 GB de RAM. Poc precisos, pero utils.
- **Models mitjans (7B-13B)**: necessiten 8-16 GB de RAM. Bona qualitat per a textes curts.
- **Models grans (30B+)**: cal maquina potent (GPU o molta RAM). Millor qualitat pero mes lents.

Al BernatLab, amb la RPi 4 de 4 GB, ens mourem amb models petits i alguns mitjans quantitzats.

## Connexions amb altres capítols

- **Cap 2** - Com instalar Ollama, el motor que ens permetra fer anar LLMs a la Raspberry.
- **Cap 3** - Com triar el model adequat segons el teu hardware.
- **Cap 4** - Com parlar be amb un LLM (prompt engineering).
- **Cap 5-8** - RAG, la tecnica per fer que el model consulti les teves dades.
- **Cap 9** - Privadesa: per que es tant important que el model sigui local.
- **Cap 10** - Aplicacio concreta al sistema de l'Hort Osona.

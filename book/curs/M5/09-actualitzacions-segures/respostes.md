# Respostes - Capitol 9: Actualitzacions segures

## Pregunta 1: Tipus d'actualitzacio rapid?

**Resposta correcta**: De seguretat.

**Explicacio**: Les actualitzacions de seguretat corregeixen vulnerabilitats conegudes. Aplicarles rapid minimitza el temps dexposicio.

## Pregunta 2: Abans d'actualitzar?

**Resposta correcta**: Copia de seguretat.

**Explicacio**: Sempre. Si alguna cosa es trenca, pots restaurar.

## Pregunta 3: Que es Watchtower?

**Resposta correcta**: Eina per actualitzar Docker.

**Explicacio**: Watchtower monitoritza els teus contenidors i els actualitza automaticament quan hi ha una nova imatge.

## Pregunta 4: Eina Debian?

**Resposta correcta**: unattended-upgrades.

**Explicacio**: Aquesta eina de Debian permet descarregar i aplicar actualitzacions automaticament.

## Pregunta 5: Risc actualitzacio?

**Resposta correcta**: Trencar funcionalitat.

**Explicacio**: Una actualitzacio pot canviar el comportament d'un paquet, afectant aplicacions que el feien servir.

## Pregunta 6: Despres d'actualitzar?

**Resposta correcta**: Verificar que tot funciona.

**Explicacio**: Cal confirmar que els serveis continuen funcionant correctament.

## Pregunta 7 (oberta): Per que no tot automatic?

**Resposta model**:

- **Riscos**: una actualitzacio pot trencar una funcionalitat critica.
- **Compatibilitat**: alguns paquets no son compatibles amb altres.
- **Sorpresa**: vols saber que canvies al teu sistema.
- **Control**: vols decidir quan aplicar cada cosa.

## Pregunta 8 (oberta): Com organitzar actualitzacions?

**Resposta model**:

- **Dia de la setmana**: per exemple, dimarts a les 4 de la matinada.
- **Ventana de manteniment**: horari de baix trafic.
- **Entorn de proves**: primer aqui, despres a produccio.
- **Documentacio**: quins canvis sha aplicat.

## Pregunta 9 (oberta): Actualitzacio trenca servei?

**Resposta model**:

- **Pas 1: Contenir**. Si es possible, aturar el tràfic al servei.
- **Pas 2: Revertir**. `apt install paquet=versio_anterior` o restaurar backup.
- **Pas 3: Investigar**. Mirar els logs per entendre que ha passat.
- **Pas 4: Planificar**. Decidir si aplicar el canvi mes tard o no.

## Pregunta 10 (oberta): Prioritzar?

**Resposta model**:

- **Seguretat**: SEMPRE primer. Son les que corregeixen 0-days.
- **Kernel**: només si hi ha una raó (vulnerabilitat greu).
- **Aplicacio**: nomes les que son al teu sistema actiu.
- **Funcionals**: les que vulguis provar primer.

## Que fer si has fallat moltes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Configura unattended-upgrades.
- **0-2 encerts**: Comença fent `apt update`.

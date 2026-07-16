# Respostes - Capitol 10: Auditoria i compliance

## Pregunta 1: Que es una auditoria?

**Resposta correcta**: Revisio periodica del sistema.

**Explicacio**: Una auditoria es una revisio sistematica del sistema per verificar que tot es correcte.

## Pregunta 2: Que es GDPR?

**Resposta correcta**: Regulacio europea.

**Explicacio**: El GDPR (General Data Protection Regulation) es la normativa europea que regula el tractament de dades personals.

## Pregunta 3: Eina dauditoria?

**Resposta correcta**: Lynis.

**Explicacio**: Lynis es una eina dauditoria de seguretat per a Linux. Analitza el sistema i proposa millores.

## Pregunta 4: Frequencia dauditoria?

**Resposta correcta**: Mensual o trimestral.

**Explicacio**: Depen de la criticitat del sistema. Per a un homelab, trimestral es raonable. Per a negocis, mensual o setmanal.

## Pregunta 5: Usuaris inactius?

**Resposta correcta**: Eliminar-los.

**Explicacio**: Els usuaris inactius son un risc de seguretat. Millor eliminar-los.

## Pregunta 6: Que documentar?

**Resposta correcta**: Troballes i accions.

**Explicacio**: Cal registrar que sha trobat i que sha fet per corregir-ho. Sense documentacio, lauditoria no serveix.

## Pregunta 7 (oberta): Per que auditar si tot funciona?

**Resposta model**:

- **Detectar configuracio que ha canviat**: algu pot haver tocat alguna cosa.
- **Compliance**: normatives que cal complir.
- **Millora continua**: trobar punts febles.
- **Prevencio**: evitar incidents abans que passin.

## Pregunta 8 (oberta): GDPR a lhort?

**Resposta model**:

- **Consentiment**: si reculls dades, cal dir-ho.
- **Minimitzacio**: nomes les dades que necessites.
- **Dret a loblit**: poder esborrar les dades.
- **Seguretat**: xifrar, contrasenyes, access limitat.
- **Documentacio**: registre de totes les dades que tens.

## Pregunta 9 (oberta): Eines dauditoria?

**Resposta model**:

- **Lynis**: auditoria general.
- **OpenVAS**: scanner de vulnerabilitats.
- **Scripts propis**: bash/python que verifiquen la teva configuracio.
- **Centre de control de cada servei**: Portainer, Uptime Kuma, etc.
- **Proveidors**: dependabot, GitGuardian.

## Pregunta 10 (oberta): Automatitzar?

**Resposta model**:

- **Scripts programats**: cron setmanal que faci les comprovacions basics.
- **CI/CD**: GitHub Actions que validi canvis.
- **Eines de monitoratge**: Uptime Kuma, Grafana.
- **Alertes**: si una comprovacio falla, notificar per Telegram.

## Que fer si has fallat moltes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Executa Lynis.
- **0-2 encerts**: Comença fent la checklist.

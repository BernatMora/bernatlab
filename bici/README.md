# CycleConnect Web (reproductor de la bici)

Pàgina autònoma amb Web Bluetooth. Publicada a <https://bernatmora.github.io/bernatlab/bici/>.
Necessita Chrome o Edge i HTTPS (o `localhost`).

## Obrir-la amb un entrenament des d'una altra web

Qualsevol web pot obrir el reproductor amb un entrenament carregat posant-lo a l'adreça,
després del `#`. No cal compartir origen ni cap servidor: el que va després del `#` no surt
del navegador.

| Adreça | Contingut (en base64url) |
|---|---|
| `…/bici/#ictx=<dades>` | Un fitxer `.ictx` d'icTrainer |
| `…/bici/#zwo=<dades>` | Un fitxer `.zwo` |
| `…/bici/#w=<dades>` | JSON `{ name, ftp?, intervals: [...] }` (web d'intervals) o `{ name, ftp?, steps: [{ dur, p0, p1?, cad?, cue?, label? }] }`, amb `p0`/`p1` com a fracció d'FTP |

Exemple, per a un botó "Fes-lo a la bici" que ja té el text `.ictx` en una variable:

```js
function obreABici(ictxText) {
  const bytes = new TextEncoder().encode(ictxText);
  let bin = '';
  for (const b of bytes) bin += String.fromCharCode(b);
  const dades = btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  window.open('https://bernatmora.github.io/bernatlab/bici/#ictx=' + dades, 'bici');
}
```

L'entrenament rebut queda desat a la llista del reproductor.

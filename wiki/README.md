# Wiki procedurale

La wiki non contiene copie manuali dei valori di gioco. `genera_wiki.py` importa i database Python del bot e ricostruisce il sito a ogni pubblicazione.

## Fonti

- `liste.py`: boss, nemici, location, equipaggiamenti, set, strutture, pesca e pool loot.
- `bilanciamento.py`: `PROC_CLASSI`, `PROC_ANELLI`, `INCANTESIMI_CONFIG`, `DUNGEON_CONFIG`, nuclei, effetti e modificatori weekend.
- `frasi_set.py`, `frasi_anelli.py`, `frasi_incantesimi.py`: descrizioni tecniche parametrizzate.
- `nft.py`: solo per formule runtime non ancora centralizzate (es. scaling boss/dungeon) e per ricavare le azioni delle stanze.
- `turno_assalto.py`: runtime dell'assalto, indicato come fonte per gli edifici.

## Generazione locale

```bash
python wiki/genera_wiki.py --output _site
```

Il risultato è un sito statico senza dipendenze esterne: `_site/index.html`, `_site/data.json` e `.nojekyll`.

## Pubblicazione

`.github/workflows/wiki-pages.yml` valida la generazione sulle pull request e pubblica automaticamente con GitHub Pages a ogni push rilevante su `main`.

Quando cambiano i dizionari di bilanciamento o le liste, la wiki viene quindi ricostruita con gli stessi valori usati dal bot.

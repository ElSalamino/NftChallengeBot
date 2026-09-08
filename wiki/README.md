# Wiki procedurale

La wiki non contiene copie manuali dei valori di gioco. `run_wiki.py` importa i database Python del bot e ricostruisce il sito a ogni pubblicazione.

## Fonti

- `liste.py`: boss, nemici, location, equipaggiamenti, set, strutture, pesca e pool loot.
- `bilanciamento.py`: `PROC_CLASSI`, `PROC_ANELLI`, `INCANTESIMI_CONFIG`, `DUNGEON_CONFIG`, nuclei, effetti e modificatori weekend.
- `frasi_set.py`, `frasi_anelli.py`, `frasi_incantesimi.py`: descrizioni tecniche parametrizzate.
- `nft.py`: solo per formule runtime non ancora centralizzate (es. scaling boss/dungeon) e per ricavare le azioni delle stanze.
- `turno_assalto.py`: runtime dell'assalto, indicato come fonte per gli edifici.
- `locales/it.json`, `locales/en.json`, `locales/es.json`: testi localizzati con fallback italiano.
- `entities.json`: ID stabili e nomi delle entità in italiano, inglese e spagnolo.

## Generazione locale

```bash
python wiki/run_wiki.py --output _site
```

Il risultato è un sito statico senza dipendenze esterne: `_site/index.html`, `_site/data.json`,
`_site/assets/i18n.js`, `_site/entities.json`, i tre cataloghi in `_site/locales/`
e `.nojekyll`. Il selettore in testata conserva la lingua scelta nel browser;
le schede — inclusi gli ingredienti — usano ID negli URL e accettano ancora i
vecchi link basati sul nome.

## Pubblicazione

`.github/workflows/wiki-pages.yml` valida la generazione sulle pull request e pubblica automaticamente con GitHub Pages a ogni push rilevante su `main`.

Quando cambiano i dizionari di bilanciamento o le liste, la wiki viene quindi ricostruita con gli stessi valori usati dal bot.

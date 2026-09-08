# NFT Single Player Playtest

Web app locale per provare il gioco senza Telegram e senza toccare i salvataggi reali.

## Avvio

Dalla root del repository:

```bash
python playtest_web.py
```

Si apre `http://127.0.0.1:8765`.

Il personaggio di test viene salvato solo nel `localStorage` del browser.

## Modalità sfida

La web app prova a importare `nft.py` e usa direttamente `nft.turno` per la logica di combattimento. Per avere il motore 1:1 devono essere disponibili anche le dipendenze che il bot importa (`Pyrogram` e `APScheduler`).

Se non sono installate, la web app resta utilizzabile e mostra esplicitamente `fallback statistico`: serve solo per controllare UI e flusso, non va usato per decisioni di bilanciamento.

Installazione minima per provare l'import del runtime:

```bash
pip install pyrogram apscheduler tgcrypto
python playtest_web.py
```

## Cosa c'è nella v1

- Scheda sandbox con HP/ATK/DEF/AGI editabili.
- Equipaggiamento reale da `liste.py` con livello già incluso nel nome dell'item.
- Rilevamento set e bonus raw.
- Approcci reali, compresi Aggressivo/Spavaldo aggiornati.
- Anelli e incantamenti configurabili.
- Sfida turno per turno contro qualsiasi nemico, boss o boss marino.
- Scaling boss per livello come esposto dalla Wiki.
- Dungeon: estrazione di una delle stanze reali con guida completa e tiro imboscata 0,5%.
- Podio giocabile con formula obiettivi, reward LV3/LV2/LV1 e perdita Gloria.
- Pesca: pool reale per location e sblocco specie tramite Potere di pesca.
- Nessun accesso ai file/player reali del bot: è un ambiente di test isolato.

## Passaggi successivi

L'obiettivo è estrarre progressivamente dal monolite Telegram le funzioni pure di gioco e farle usare sia al bot sia alla web app. In questo modo il playtest web diventa 1:1 anche per dungeon, pesca, loot, inventario, forgia, pozioni e progressione senza duplicare le regole.

# -*- coding: utf-8 -*-
"""Descrizioni tecniche centralizzate degli oggetti usabili.

Le frasi sono separate dalle descrizioni narrative di ``liste.usabili`` e
riassumono il comportamento effettivo del runtime. La wiki le espone insieme
alla descrizione decorativa.
"""

FRASI_USABILI_TECNICHE = {
    "Dell'ambrosia": (
        "Consuma 1 Ambrosia per utilizzo. Aggiunge il boost d'assalto Divino LV1 "
        "con durata +6; usi multipli sommano altri 6 punti di durata ciascuno."
    ),
    "Un eco-locatore": (
        "È riutilizzabile e richiede più di 3651 secondi dall'ultimo utilizzo. "
        "Teletrasporta in una location con meteo Pioggia/Tempesta se ne viene trovata una; "
        "altrimenti sceglie una location casuale. Registra last-eco. Se nello zaino ce ne sono "
        "più di 1, tutte le copie eccedenti vengono convertite 1:1 in Dell'ambrosia e resta 1 eco-locatore."
    ),
    "Un fune di fuga": (
        "Usabile solo mentre è attivo un dungeon. Rimuove immediatamente lo stato dungeon del giocatore, "
        "facendolo uscire, poi consuma 1 copia."
    ),
    "Uno stimpak": (
        "Usabile solo nel dungeon. Sottrae 200 da dungeon.danno, quindi recupera 200 HP rispetto al danno "
        "accumulato, poi consuma 1 copia. Non applica un clamp a zero nel punto di utilizzo."
    ),
    "Candela blu": (
        "Usabile solo nel dungeon. Aggiunge una voce Boss alla lista dungeon.mostri, quindi inserisce un "
        "ulteriore incontro Boss nel percorso, poi consuma 1 copia."
    ),
    "Ultimo barlore": (
        "Usabile solo nel dungeon. Aggiunge a dungeon.mostri una stanza scelta casualmente da liste.stanze, "
        "allungando il percorso di una stanza casuale, poi consuma 1 copia."
    ),
    "Un idoletto": (
        "Richiede un clan. Ogni copia consumata aggiunge +4 potere e +4 punti al clan. Con uso multiplo "
        "può consumare al massimo 10 copie in una volta."
    ),
    "La spezia": (
        "Può essere attivata solo se il giocatore non ha già cariche in trader.preferenziale. Ogni copia "
        "consumata inserisce 4 volte il giocatore in trader.preferenziale e aggiunge +4 durata al boost "
        "sfida Speziato LV1. L'uso multiplo è limitato a 10 copie."
    ),
    "Dell'acqua fresca": (
        "Per ogni copia consumata porta indietro di 320 secondi il timestamp player.last del giocatore. "
        "L'uso multiplo ripete l'effetto per ogni copia disponibile."
    ),
    "Una licenza per animali domestici": (
        "Consuma 1 licenza, sceglie casualmente un pet da liste.animaletti e sostituisce player.pet con il "
        "nuovo animale. Incrementa varie.cambi di 1. Anche con comando multiplo usa una sola licenza."
    ),
    "Del latte in sacchetto": (
        "Se il giocatore è inabilitato, consuma 1 copia e rimuove lo stato da inabilitati. Non può rimuovere "
        "l'inabilitazione speciale causata da Una copia dell'arte della guerra autografata. Se il giocatore "
        "non è inabilitato, non consuma il latte."
    ),
    "Un oggetto incartato": (
        "Apre una ricompensa casuale dal pool corrente; gli eventi mega, zombie, gungeon, magic e tempesta "
        "aggiungono copie dei rispettivi pool e quindi ne aumentano il peso. L'apertura singola ha inoltre "
        "lo 0,1% di essere sostituita da Nulla assoluto. L'apertura multipla accetta fino a 100000 copie per "
        "comando e aggrega i risultati; nel ramo multiplo l'override Nulla assoluto non viene applicato."
    ),
    "Una copia dell'arte della guerra autografata": (
        "Usabile come oggetto errante dopo almeno 1800 secondi dal precedente utilizzo dell'oggetto. "
        "Consuma la copia dell'utilizzatore, consegna una copia a un giocatore casuale e imposta il bersaglio "
        "in inabilitati con lo stato speciale dell'Arte della guerra. La pulizia delle sfide può rimuovere "
        "questo stordimento dopo almeno 600 secondi; l'oggetto errante viene inoltre riallocato automaticamente "
        "dopo 3600 secondi durante la manutenzione delle sfide."
    ),
    "Una mail di spam con anche qualche pene": (
        "Usabile come oggetto errante dopo almeno 1800 secondi. Consuma la copia, la consegna a un giocatore "
        "casuale, sottrae 100 punti sfida al bersaglio indicato e aggiunge 100 punti sfida all'utilizzatore. "
        "L'oggetto errante può essere riallocato automaticamente dopo 3600 secondi."
    ),
    "Un megafono megaenorme": (
        "Usabile come oggetto errante dopo almeno 1800 secondi. Consuma la copia e la passa a un giocatore "
        "casuale. Sul bersaglio indicato disequipaggia arma e protezione, imposta l'approccio a Base e azzera "
        "set e anello; le funzioni di disequipaggiamento rimuovono dalle statistiche i bonus dell'equipaggiamento. "
        "L'oggetto errante può essere riallocato automaticamente dopo 3600 secondi."
    ),
    "un castoro cattivissimo": (
        "Usabile come oggetto errante dopo almeno 1800 secondi. Funziona solo se il bersaglio possiede più di "
        "4 voci nello zaino. Cerca un oggetto non decorativo tra anelli o nomi contenenti 0/1/2/3; dopo 20 "
        "tentativi accetta comunque il candidato purché non decorativo. Trasferisce 1 copia dell'oggetto scelto "
        "dal bersaglio all'utilizzatore, sposta il castoro nello zaino del bersaglio e avvia il nuovo cooldown."
    ),
    "Un hp extra": (
        "Consuma 1 copia e aggiunge permanentemente +1 HP alla scheda. Ogni punto HP usa 1 unità di cap "
        "(liste.valore=1). L'uso è rifiutato se il cap richiesto supera il cap massimo calcolato dal profilo."
    ),
    "Un punto attacco": (
        "Consuma 1 copia e aggiunge permanentemente +1 ATK alla scheda. Ogni punto ATK usa 4 unità di cap "
        "(liste.valore=4). L'uso è rifiutato se il cap richiesto supera il cap massimo calcolato dal profilo."
    ),
    "Un punto difesa": (
        "Consuma 1 copia e aggiunge permanentemente +1 DEF alla scheda. Ogni punto DEF usa 4 unità di cap "
        "(liste.valore=4). L'uso è rifiutato se il cap richiesto supera il cap massimo calcolato dal profilo."
    ),
    "Un punto agilità": (
        "Consuma 1 copia e aggiunge permanentemente +1 AGI alla scheda. Ogni punto AGI usa 20 unità di cap "
        "(liste.valore=20). L'uso è rifiutato se il cap richiesto supera il cap massimo calcolato dal profilo."
    ),
    "Il controller del super raggio mortale a neutroni mega pericolosissimo": (
        "Usabile come oggetto errante dopo almeno 1800 secondi. Consuma la copia e passa il controller a un "
        "giocatore casuale. Il bersaglio indicato viene teletrasportato in una location casuale diversa da Hub. "
        "L'oggetto errante può essere riallocato automaticamente dopo 3600 secondi."
    ),
    "Un biglietto polivalente": (
        "Consuma 1 copia e imposta immediatamente player.location = Hub. Il comando usa una sola copia per volta."
    ),
    "BATH WATER": (
        "Per ogni copia consumata porta indietro player.last di 420 secondi. Se presenti, porta indietro anche "
        "last_dungeon, last_boss e last_assalto di 50 secondi ciascuno e il timer numerico di inabilitazione di "
        "240 secondi. L'uso multiplo ripete tutti questi effetti per copia."
    ),
}

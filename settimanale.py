# -*- coding: utf-8 -*-
"""Configurazione e helper dei premi oro della Settimanale."""
from __future__ import annotations

import random

# Unica fonte per runtime e Wiki: modificare qui mantiene allineati premi e documentazione.
PREMI_ORO_SETTIMANALE = (
    "Uno scudo d'oro LV0",
    "Un pugnale d'oro LV0",
    "Una balestra d'oro LV0",
    "Spada d'oro fortissima LV0",
    "Elmo d'oro fortissimo LV0",
    "Anello d'oro fortissimo",
    "Un rolex oro LV0",
)

# Ogni soglia superata concede un'estrazione aggiuntiva dallo stesso pool.
SOGLIE_PREMI_ORO_SETTIMANALE = (8.4, 8.8, 9.6)

LIVELLO_PREMIO_SETTIMANALE_MIN = 0
LIVELLO_PREMIO_SETTIMANALE_MAX = 4


def base_oggetto(nome):
    """Nome senza suffisso LV, allineato alla logica della Wiki."""
    return str(nome).split(" LV", 1)[0]


def estrai_premio_oro_settimanale(premi=None, rng=None):
    """Estrae un premio oro; gli equipaggiamenti con LV escono tra LV0 e LV4."""
    rng = rng or random
    pool = tuple(premi or PREMI_ORO_SETTIMANALE)
    premio = rng.choice(pool)

    if " LV" not in premio:
        return premio

    base = premio.rsplit(" LV", 1)[0]
    livello = rng.randint(LIVELLO_PREMIO_SETTIMANALE_MIN, LIVELLO_PREMIO_SETTIMANALE_MAX)
    return f"{base} LV{livello}"


def descrizione_ottenimento_oro_settimanale():
    soglie = ", ".join(str(x).replace(".", ",") for x in SOGLIE_PREMI_ORO_SETTIMANALE)
    return (
        "Premio della Settimanale. Superando 8,4 punti ottieni una prima estrazione dal pool oro; "
        "superando 8,8 e 9,6 punti ottieni rispettivamente una seconda e una terza estrazione. "
        f"Le soglie sono {soglie}. Gli oggetti con livello vengono assegnati casualmente tra "
        f"LV{LIVELLO_PREMIO_SETTIMANALE_MIN} e LV{LIVELLO_PREMIO_SETTIMANALE_MAX}."
    )

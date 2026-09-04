# -*- coding: utf-8 -*-
"""Helper puri per le nuove meccaniche dungeon: Podio e imboscate."""
from __future__ import annotations

import random


def podio_probabilita_pct(obiettivi_completati, obiettivi_totali, posizione):
    """Converte il rapporto del Podio in percentuale: rapporto 1 = 100%, con cap al 100%."""
    posizione = int(posizione)
    totale = max(0, int(obiettivi_totali))
    completati = max(0, int(obiettivi_completati))
    if totale <= 0 or posizione <= 0:
        return 0.0
    rapporto = completati / (totale / posizione)
    return min(100.0, max(0.0, rapporto * 100.0))


def podio_livello_premio(posizione, livello_base=4):
    """LV premio = livello_base - posizione: 1°→LV3, 2°→LV2, 3°→LV1."""
    return max(0, int(livello_base) - int(posizione))


def podio_penalita_gloria(posizione, base=6, moltiplicatore=2):
    """Gloria teorica persa = moltiplicatore * (base - posizione)."""
    return max(0, int(moltiplicatore) * (int(base) - int(posizione)))


def podio_applica_penalita(gloria_attuale, penalita):
    """Non permette alla Gloria di scendere sotto zero; ritorna (nuova, persa)."""
    gloria = max(0, int(gloria_attuale))
    perdita = min(gloria, max(0, int(penalita)))
    return gloria - perdita, perdita


def scegli_nemici_imboscata(tutti_nemici, nemici_locali, quantita=2, rng=None):
    """Sceglie nemici esterni alla zona corrente. Evita duplicati quando possibile."""
    rng = rng or random
    locali = set(nemici_locali or [])
    pool = [nome for nome in tutti_nemici if nome not in locali]
    quantita = max(0, int(quantita))
    if not pool or quantita == 0:
        return []
    if len(pool) >= quantita:
        return list(rng.sample(pool, quantita))
    return [rng.choice(pool) for _ in range(quantita)]

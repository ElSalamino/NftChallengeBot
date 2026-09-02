# -*- coding: utf-8 -*-
"""Bilanciamento centralizzato delle statistiche grezze dei set.

Il punteggio usa gli stessi pesi del cap permanente:
HP=1, ATK=4, DEF=4, AGI=20.

Vengono normalizzati SOLO i set che possiedono già almeno una raw stat
positiva. I set con HP=ATK=DEF=AGI=0 restano intenzionalmente a zero: il loro
bilanciamento è affidato agli effetti speciali del set.

I set sotto il target vengono solo potenziati mantenendo il mix statistico
originale. Ogni statistica calcolata viene arrotondata per eccesso.
"""
from __future__ import annotations

import math
from typing import Mapping

SET_RAW_WEIGHTS = {"hp": 1, "atk": 4, "def": 4, "agi": 20}
SET_RAW_TARGET = 1200


def _num(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def set_raw_score(stats: Mapping[str, object] | None) -> int:
    stats = stats or {}
    return int(round(sum(_num(stats.get(stat, 0)) * weight for stat, weight in SET_RAW_WEIGHTS.items())))


def _scaled_profile(profile: Mapping[str, object], target: int) -> dict[str, int]:
    """Scala proporzionalmente un profilo positivo fino al target.

    Ogni singola statistica viene arrotondata con ceil; il punteggio finale può
    quindi superare di pochi punti il target, ma non può mai restare sotto.
    """
    positive = {stat: max(0.0, _num(profile.get(stat, 0))) for stat in SET_RAW_WEIGHTS}
    score = sum(positive[stat] * SET_RAW_WEIGHTS[stat] for stat in SET_RAW_WEIGHTS)
    if score <= 0:
        return {stat: 0 for stat in SET_RAW_WEIGHTS}
    factor = target / score
    return {
        stat: int(math.ceil(positive[stat] * factor)) if positive[stat] > 0 else 0
        for stat in SET_RAW_WEIGHTS
    }


def normalize_set_bonuses(
    classi,
    bonus,
    armi=None,
    armiextra=None,
    protezioni=None,
    protezioniextra=None,
    target: int = SET_RAW_TARGET,
):
    """Restituisce bonus raw uniformati e metadati di audit.

    Regole:
    - un set con tutte le raw stats a zero resta a zero;
    - nessun set sopra target viene nerfato;
    - un set già dotato di raw stats mantiene il proprio mix statistico;
    - ogni valore calcolato viene arrotondato per eccesso.

    I parametri degli equipaggiamenti restano nella firma per compatibilità con
    il chiamante precedente, ma non vengono usati per inventare raw stats ai set
    che ne sono intenzionalmente privi.
    """
    classi = classi or {}
    source_bonus = bonus or {}

    normalized: dict[str, dict[str, int]] = {}
    scores: dict[str, int] = {}
    original_scores: dict[str, int] = {}
    themes: dict[str, str] = {}

    # Comprende anche eventuali bonus orfani per non distruggere dati esistenti.
    names = list(dict.fromkeys(list(classi) + list(source_bonus)))
    for name in names:
        current = {
            stat: int(round(_num((source_bonus.get(name) or {}).get(stat, 0))))
            for stat in SET_RAW_WEIGHTS
        }
        current_score = set_raw_score(current)
        original_scores[name] = current_score

        if current_score == 0:
            # Zero è intenzionale: il set vive dei suoi effetti speciali.
            final = current
            theme_source = current
        elif current_score >= target:
            final = current
            theme_source = current
        else:
            # Mantiene l'identità statistica già scelta dall'autore del set.
            final = _scaled_profile(current, target)
            # Non ridurre mai una statistica esistente per effetto di conversioni.
            final = {stat: max(current[stat], final[stat]) for stat in SET_RAW_WEIGHTS}
            theme_source = current

        final_score = set_raw_score(final)
        if 0 < final_score < target:
            # Con ceil sulle singole stats normalmente non serve, ma HP ha
            # granularità 1 e garantisce comunque che il budget non resti sotto.
            final["hp"] += int(math.ceil(target - final_score))
            final_score = set_raw_score(final)

        normalized[name] = final
        scores[name] = final_score

        weighted_theme = {
            stat: max(0.0, _num(theme_source.get(stat, 0))) * SET_RAW_WEIGHTS[stat]
            for stat in SET_RAW_WEIGHTS
        }
        themes[name] = max(weighted_theme, key=weighted_theme.get).upper() if any(weighted_theme.values()) else "NESSUNO"

    return normalized, scores, original_scores, themes

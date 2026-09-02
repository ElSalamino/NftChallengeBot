# -*- coding: utf-8 -*-
"""Bilanciamento centralizzato delle statistiche grezze dei set.

Il punteggio usa gli stessi pesi del cap permanente:
HP=1, ATK=4, DEF=4, AGI=20.

I set sotto il target vengono solo potenziati. Se hanno già bonus raw, ne
manteniamo la proporzione. Se partono da zero, il profilo viene ricavato dalle
statistiche base dei componenti del set. Ogni statistica calcolata viene
arrotondata per eccesso, come richiesto dal bilanciamento.
"""
from __future__ import annotations

import math
from typing import Mapping

SET_RAW_WEIGHTS = {"hp": 1, "atk": 4, "def": 4, "agi": 20}
SET_RAW_TARGET = 1200

# Set senza componenti: il tema deriva direttamente dalla loro meccanica.
THEME_OVERRIDES = {
    "Forma terra": {"def": 1},
    "Forma fuoco": {"atk": 1},
    "Forma lunare": {"agi": 1},
    "Forma elettro": {"agi": 1},
}


def _num(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def set_raw_score(stats: Mapping[str, object] | None) -> int:
    stats = stats or {}
    return int(round(sum(_num(stats.get(stat, 0)) * weight for stat, weight in SET_RAW_WEIGHTS.items())))


def _base_item(name: object) -> str:
    return str(name).split(" LV", 1)[0]


def _item_stat_map(*collections: Mapping[str, Mapping[str, object]]) -> dict[str, dict[str, object]]:
    """Indicizza le statistiche LV0/base degli equipaggiamenti per nome base."""
    result: dict[str, dict[str, object]] = {}
    priority: dict[str, int] = {}
    for collection in collections:
        for full_name, stats in (collection or {}).items():
            name = _base_item(full_name)
            text = str(full_name)
            token = text.split(" LV", 1)[1] if " LV" in text else "base"
            # Preferenza: voce base esplicita > LV0 > qualunque altro livello.
            p = 2 if token == "base" else 1 if token == "0" else 0
            if name not in result or p >= priority.get(name, -1):
                result[name] = dict(stats or {})
                priority[name] = p
    return result


def _component_theme(components, item_stats) -> dict[str, float]:
    theme = {stat: 0.0 for stat in SET_RAW_WEIGHTS}
    for component in components or []:
        stats = item_stats.get(_base_item(component), {})
        for stat in theme:
            # Le penalità dell'equipaggiamento non devono trasformarsi in un
            # malus raw del set: servono solo i contributi positivi al tema.
            theme[stat] += max(0.0, _num(stats.get(stat, 0)))
    return theme


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
    - nessun set sopra target viene nerfato;
    - un set già dotato di raw stats mantiene il proprio mix statistico;
    - un set a zero usa come mix le stats positive dei suoi componenti;
    - le quattro Forme senza componenti usano THEME_OVERRIDES;
    - ogni valore calcolato viene arrotondato per eccesso.
    """
    classi = classi or {}
    source_bonus = bonus or {}
    item_stats = _item_stat_map(armi or {}, armiextra or {}, protezioni or {}, protezioniextra or {})

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

        if current_score >= target:
            final = current
            theme_source = current
        elif current_score > 0:
            # Mantiene esattamente l'identità già scelta dall'autore del set.
            final = _scaled_profile(current, target)
            # Non ridurre mai per effetto di arrotondamenti/conversioni.
            final = {stat: max(current[stat], final[stat]) for stat in SET_RAW_WEIGHTS}
            theme_source = current
        else:
            profile = dict(THEME_OVERRIDES.get(name, {}))
            if not profile:
                profile = _component_theme(classi.get(name, []), item_stats)
            final = _scaled_profile(profile, target)
            theme_source = profile

        final_score = set_raw_score(final)
        if final_score < target:
            # Fallback deterministico per dati incompleti: HP ha granularità 1,
            # quindi permette di raggiungere il target senza restare sotto.
            final["hp"] += int(math.ceil(target - final_score))
            final_score = set_raw_score(final)

        normalized[name] = final
        scores[name] = final_score

        weighted_theme = {
            stat: max(0.0, _num(theme_source.get(stat, 0))) * SET_RAW_WEIGHTS[stat]
            for stat in SET_RAW_WEIGHTS
        }
        themes[name] = max(weighted_theme, key=weighted_theme.get).upper() if any(weighted_theme.values()) else "HP"

    return normalized, scores, original_scores, themes

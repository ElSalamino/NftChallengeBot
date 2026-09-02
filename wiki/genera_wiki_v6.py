#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wiki v6: chiarisce esattamente la Centrale di cura centralizzata."""
from __future__ import annotations

import genera_wiki_v5 as v5

ROOT = v5.ROOT
v4 = v5.v4
v3 = v5.v3
v2 = v5.v2
bilanciamento = v5.bilanciamento
liste = v5.liste
_prefixed_flatten = v5._prefixed_flatten
HTML = v5.HTML


def _structure_rows(structure_name, mode_name):
    cfg_all = getattr(bilanciamento, "STRUTTURE_CONFIG", {})
    system_cfg = cfg_all.get("generale", {}).get("scaling", {})
    structure_cfg = cfg_all.get(structure_name, {})
    general_cfg = structure_cfg.get("generale", {})
    mode_cfg = structure_cfg.get("modalita", {}).get(mode_name, {})

    rows = []
    rows.extend(_prefixed_flatten("sistema.scaling", system_cfg))
    rows.extend(_prefixed_flatten("generale", general_cfg))
    rows.extend(_prefixed_flatten(f"modalita.{mode_name}", mode_cfg))
    return rows


def _structure_technical(structure_name, mode_name):
    if structure_name != "Centrale di cura centralizzata":
        return v5._structure_technical(structure_name, mode_name)

    cfg = bilanciamento.STRUTTURE_CONFIG[structure_name]
    value = cfg["generale"]["valore_per_livello"]
    threshold = cfg["generale"]["hp_minimo_modifica"]
    rows = _structure_rows(structure_name, mode_name)

    if mode_name == "Sparsa":
        text = (
            f"Cura ogni struttura del villaggio di {value} HP per ogni livello della Centrale. "
            f"Esempio: a LV10 cura ogni struttura di {value * 10} HP. "
            f"La soglia di {threshold} HP riguarda solo il counter Assassino delle ombre, quando la cura viene trasformata in danno."
        )
    elif mode_name == "Concentrata":
        text = (
            f"Sceglie una sola struttura casuale e concentra su di lei tutta la cura: "
            f"{value} HP × livello della Centrale × numero di strutture presenti. "
            f"Esempio: a LV10 con 5 strutture cura un solo bersaglio di {value * 10 * 5} HP. "
            f"La soglia di {threshold} HP riguarda solo il counter Assassino delle ombre, quando la cura viene trasformata in danno."
        )
    else:
        text, _ = v5._structure_technical(structure_name, mode_name)

    return text, rows


def build_data():
    data = v5.build_data()
    for structure in data.get("assault", []):
        if structure.get("name") != "Centrale di cura centralizzata":
            continue
        for mode in structure.get("modes", []):
            technical, rows = _structure_technical(structure["name"], mode["name"])
            mode["technical"] = technical
            mode["technical_params"] = rows
    data["meta"]["wiki_version"] = 6
    return data


def main():
    # Riusa il writer v5 sostituendo temporaneamente i dati generati.
    original = v5.build_data
    try:
        v5.build_data = build_data
        v5.main()
    finally:
        v5.build_data = original


if __name__ == "__main__":
    main()

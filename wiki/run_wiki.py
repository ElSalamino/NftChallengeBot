#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entry point della wiki procedurale pubblicata su GitHub Pages."""
import re
import genera_wiki_v3 as wiki

# Il generatore v3 riusa alcune raccolte del v2: forza anche lì l'elenco
# dei set già filtrato, così eventuali chiavi storiche None non entrano
# nell'ordinamento del catalogo.
wiki.v2.set_names = wiki._valid_set_names

# Alcuni set storici hanno spaziature diverse nel nome dell'approccio
# (es. "Aggressivo +" contro la chiave canonica "Aggressivo+").
# La wiki risolve questi alias al nome realmente presente in liste.Approcci,
# così i backlink restano navigabili senza alterare i dati del gioco.
_original_set_data = wiki.set_data


def _norm_approach(value):
    return re.sub(r"\s+", "", str(value)).casefold()


def _set_data_con_approcci_canonici():
    rows = _original_set_data()
    canonical = {
        _norm_approach(name): name
        for name in getattr(wiki.liste, "Approcci", {})
        if isinstance(name, str)
    }
    for row in rows:
        row["approaches"] = [
            canonical.get(_norm_approach(name), name)
            for name in row.get("approaches", [])
        ]
    return rows


wiki.set_data = _set_data_con_approcci_canonici


if __name__ == "__main__":
    wiki.main()

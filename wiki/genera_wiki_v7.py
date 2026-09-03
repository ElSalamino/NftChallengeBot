#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wiki v7: mostra come ottenere gli equipaggiamenti oro dalla Settimanale."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import genera_wiki_v6 as v6
import settimanale

ROOT = v6.ROOT
v5 = v6.v5
v4 = v6.v4
v3 = v6.v3
v2 = v6.v2
bilanciamento = v6.bilanciamento
liste = v6.liste
_prefixed_flatten = v6._prefixed_flatten
_structure_technical = v6._structure_technical


def build_data():
    data = v6.build_data()
    premi_base = {settimanale.base_oggetto(x) for x in settimanale.PREMI_ORO_SETTIMANALE}

    for item in data.get("items", []):
        if item.get("name") not in premi_base:
            continue
        item["weekly_gold_reward"] = {
            "source": "Settimanale",
            "thresholds": list(settimanale.SOGLIE_PREMI_ORO_SETTIMANALE),
            "level_min": settimanale.LIVELLO_PREMIO_SETTIMANALE_MIN,
            "level_max": settimanale.LIVELLO_PREMIO_SETTIMANALE_MAX,
            "description": settimanale.descrizione_ottenimento_oro_settimanale(),
        }

    data["meta"]["wiki_version"] = 7
    return data


def build_html():
    html = v6.HTML
    old = "function itemDetail(name){const i=find(D.items,name);if(!i)return missing(name);let special='';"
    new = old + r'''if(i.weekly_gold_reward){const w=i.weekly_gold_reward;special+=sectionTitle('Come si ottiene')+`<div class="card"><p><b>${esc(w.source)}:</b> ${esc(w.description)}</p></div>`;}'''
    return v3._must_replace(html, old, new, "ottenimento settimanale equipaggiamenti oro")


HTML = build_html()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="_site")
    args = parser.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        out = ROOT / out
    out.mkdir(parents=True, exist_ok=True)

    data = build_data()
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (out / "index.html").write_text(HTML.replace("__DATA__", payload), encoding="utf-8")
    (out / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    assets = ROOT / "wiki" / "assets"
    if assets.exists():
        shutil.copytree(assets, out / "assets", dirs_exist_ok=True)

    print("Wiki v7 generata:", out)
    print(json.dumps(data["meta"]["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

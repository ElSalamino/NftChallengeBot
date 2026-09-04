#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wiki v12: raw score leggibile per oggetti, nemici e boss."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import genera_wiki_v11 as v11
from set_raw_balance import SET_RAW_WEIGHTS

ROOT = v11.ROOT
v10 = v11.v10
v9 = v11.v9
v8 = v11.v8
v7 = v11.v7
v6 = v11.v6
v5 = v11.v5
v4 = v11.v4
v3 = v11.v3
v2 = v11.v2
bilanciamento = v11.bilanciamento
liste = v11.liste
_prefixed_flatten = v11._prefixed_flatten
_structure_technical = v11._structure_technical

RAW_WEIGHTS = {stat: int(SET_RAW_WEIGHTS[stat]) for stat in ("hp", "atk", "def", "agi")}


def raw_score(stats):
    stats = stats or {}
    total = 0
    for stat, weight in RAW_WEIGHTS.items():
        try:
            value = float(stats.get(stat, 0) or 0)
        except (TypeError, ValueError):
            value = 0
        total += value * weight
    return int(round(total))


def build_data():
    data = v11.build_data()

    for item in data.get("items", []):
        levels = item.get("levels", [])
        for level in levels:
            level["raw_score"] = raw_score(level.get("stats", {}))
        lv0 = next((x for x in levels if x.get("label") == "LV0"), levels[0] if levels else None)
        item["raw_score"] = raw_score(lv0.get("stats", {})) if lv0 else None
        item["raw_score_basis"] = "LV0" if lv0 else None

    for enemy in data.get("enemies", []):
        enemy["raw_score"] = raw_score(enemy.get("stats", {}))

    for boss in data.get("bosses", []):
        boss["raw_score"] = raw_score(boss.get("stats", {}))
        for level in boss.get("levels", []):
            level["raw_score"] = raw_score(level.get("stats", {}))

    # Anche i boss marini usano lo stesso indicatore, così tutte le schede boss
    # espongono la stessa unità di confronto nel JSON della Wiki.
    for boss in data.get("marine_bosses", []):
        boss["raw_score"] = raw_score(boss.get("stats", {}))

    data["raw_score_system"] = {
        "weights": RAW_WEIGHTS,
        "formula": "HP ×1 · ATK ×4 · DEF ×4 · AGI ×20",
        "description": "Somma pesata delle statistiche grezze, usata come indicatore unico per confrontare la quantità di statistiche raw.",
    }
    data["meta"]["wiki_version"] = 12
    return data


EXTRA_JS = r'''
function rawScoreSection(score,basis){
  if(score===null||score===undefined)return '';
  const f=(D.raw_score_system&&D.raw_score_system.formula)||'HP ×1 · ATK ×4 · DEF ×4 · AGI ×20';
  const prefix=basis?`${basis} · `:'';
  return sectionTitle('Punteggio raw')+`<div class="card"><div style="font-size:28px;font-weight:800">${esc(score)}</div><div class="muted">${esc(prefix+f)}</div></div>`;
}
function injectRawScore(html,score,basis){
  const marker='</div><aside class="sidebox">';
  const block=rawScoreSection(score,basis);
  if(!block)return html;
  return html.includes(marker)?html.replace(marker,block+marker):html+block;
}

const _wikiV12ItemDetail=itemDetail;
itemDetail=function(name){
  const i=find(D.items,name);
  const base=_wikiV12ItemDetail(name);
  if(!i)return base;
  return injectRawScore(base,i.raw_score,i.raw_score_basis||'LV0');
};

const _wikiV12EnemyDetail=enemyDetail;
enemyDetail=function(name){
  const e=find(D.enemies,name);
  const base=_wikiV12EnemyDetail(name);
  if(!e)return base;
  return injectRawScore(base,e.raw_score,'Statistiche base');
};

const _wikiV12BossDetail=bossDetail;
bossDetail=function(name){
  const b=find(D.bosses,name);
  const base=_wikiV12BossDetail(name);
  if(!b)return base;
  return injectRawScore(base,b.raw_score,'Statistiche base');
};
'''


def build_html():
    html = v11.HTML
    return v3._must_replace(html, "function render(){", EXTRA_JS + "\nfunction render(){", "Wiki v12 raw score")


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
    print("Wiki v12 generata:", out)
    print(json.dumps(data["meta"]["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

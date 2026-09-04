#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wiki v10: stanza Podio e imboscate casuali nei dungeon."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import genera_wiki_v9 as v9
from dungeon_extra import (
    podio_probabilita_pct,
    podio_livello_premio,
    podio_penalita_gloria,
)

ROOT = v9.ROOT
v8 = v9.v8
v7 = v9.v7
v6 = v9.v6
v5 = v9.v5
v4 = v9.v4
v3 = v9.v3
v2 = v9.v2
bilanciamento = v9.bilanciamento
liste = v9.liste
_prefixed_flatten = v9._prefixed_flatten
_structure_technical = v9._structure_technical


def build_data():
    data = v9.build_data()
    generale = bilanciamento.DUNGEON_CONFIG.get("generale", {})
    totale_obiettivi = len(data.get("achievements", []))

    posizioni = []
    for posizione in (1, 2, 3):
        posizioni.append({
            "position": posizione,
            "choice": f"{posizione}° posto",
            "formula": f"obiettivi completati / ({totale_obiettivi} / {posizione}) %",
            "max_chance_pct": podio_probabilita_pct(
                totale_obiettivi, totale_obiettivi, posizione
            ),
            "reward_level": podio_livello_premio(
                posizione, generale.get("podio_livello_base", 4)
            ),
            "glory_loss": podio_penalita_gloria(
                posizione,
                generale.get("podio_gloria_base", 6),
                generale.get("podio_gloria_moltiplicatore", 2),
            ),
        })

    imboscata = generale.get("imboscata", {"proc": 0.5, "nemici": 2})
    data["dungeon_additions"] = {
        "podium": {
            "room": "Podio",
            "total_achievements": totale_obiettivi,
            "description": (
                "Nel Podio scegli se tentare il 1°, 2° o 3° posto. La probabilità percentuale "
                "è obiettivi completati / (numero totale obiettivi / posizione). Più obiettivi hai, "
                "più la probabilità cresce. In caso di successo ricevi un oggetto livellabile casuale "
                "dal pool dungeon al livello LV(4-posizione). In caso di fallimento perdi "
                "2×(6-posizione) Gloria, ma la Gloria non può scendere sotto zero."
            ),
            "positions": posizioni,
        },
        "ambush": {
            "proc_pct": float(imboscata.get("proc", 0.5)),
            "enemies": int(imboscata.get("nemici", 2)),
            "message": "Mentre giravi per il dungeon un gruppo di loschi figuri si avvicina, è un imboscata!",
            "description": (
                "Ogni volta che entri in una stanza del dungeon c'è lo 0,5% di probabilità di imboscata. "
                "Se scatta, vengono scelti 2 mostri che non appartengono alla zona in cui ti trovi e "
                "vengono inseriti in prima posizione nel percorso, diventando i prossimi incontri dopo "
                "la stanza corrente."
            ),
        },
    }
    data["meta"]["wiki_version"] = 10
    return data


EXTRA_JS = r'''
const _wikiV10DungeonHome=dungeonHome;
dungeonHome=function(){
  const base=_wikiV10DungeonHome();
  const x=D.dungeon_additions,p=x.podium,a=x.ambush;
  const rows=p.positions.map(r=>`<tr><td><b>${r.position}° posto</b></td><td>${esc(r.formula)}</td><td>${r.max_chance_pct}%</td><td>LV${r.reward_level}</td><td>-${r.glory_loss} Gloria</td></tr>`).join('');
  return base
    +sectionTitle('Podio')
    +`<div class="card"><p>${esc(p.description)}</p><p><b>Obiettivi totali attuali:</b> ${p.total_achievements}.</p><div class="tablewrap"><table class="tbl"><thead><tr><th>Scelta</th><th>Probabilità</th><th>Massimo con tutti gli obiettivi</th><th>Premio</th><th>Fallimento</th></tr></thead><tbody>${rows}</tbody></table></div></div>`
    +sectionTitle('Imboscate')
    +`<div class="card"><p>${esc(a.description)}</p><p><b>Probabilità per stanza:</b> ${a.proc_pct}% · <b>Mostri aggiunti:</b> ${a.enemies}.</p><div class="effect human">${esc(a.message)}</div></div>`;
};

const _wikiV10RoomDetail=roomDetail;
roomDetail=function(name){
  if(name!=='Podio')return _wikiV10RoomDetail(name);
  const p=D.dungeon_additions.podium;
  const cards=p.positions.map(r=>`<div class="card"><h3>${r.position}° posto</h3><p><b>Formula:</b> ${esc(r.formula)}</p><p><b>Con tutti gli obiettivi:</b> ${r.max_chance_pct}%</p><p><b>Se vinci:</b> oggetto casuale LV${r.reward_level}.</p><p><b>Se perdi:</b> fino a ${r.glory_loss} Gloria, senza andare sotto 0.</p></div>`).join('');
  return head('Podio','Una stanza basata sui tuoi obiettivi completati.','Dungeon')
    +`<div class="detail"><div><div class="effect human">${esc(p.description)}</div>${sectionTitle('I tre gradini')}<div class="entity-grid">${cards}</div></div><aside class="sidebox">${img('rooms','Podio','🏆')}</aside></div>`;
};
'''


def build_html():
    html = v9.HTML
    html = v3._must_replace(
        html,
        "function render(){",
        EXTRA_JS + "\nfunction render(){",
        "Wiki v10 Podio e imboscate",
    )
    return html


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

    print("Wiki v10 generata:", out)
    print(json.dumps(data["meta"]["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wiki v4: descrizioni tecniche usabili e parametri completi d'assalto."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import genera_wiki_v3 as v3
from frasi_usabili import FRASI_USABILI_TECNICHE

ROOT = v3.ROOT


def _prefixed_flatten(prefix, value):
    rows = []
    for row in v3.v2.flatten(value):
        path = str(row.get("path", "")).strip()
        rows.append({
            "path": f"{prefix}.{path}" if path else prefix,
            "value": row.get("value"),
        })
    return rows


def _display_param(path, value):
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(str(x) for x in value) + "]"
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    leaf = path.rsplit(".", 1)[-1]
    if isinstance(value, (int, float)):
        if leaf.endswith(("_proc", "_pct", "_soglia_pct")):
            return f"{value}%"
        if leaf.endswith("_mul"):
            return f"×{value}"
    return str(value)


def _structure_technical(structure_name, mode_name):
    cfg_all = getattr(v3.bilanciamento, "STRUTTURE_CONFIG", {})
    system_cfg = cfg_all.get("generale", {}).get("scaling", {})
    structure_cfg = cfg_all.get(structure_name, {})
    general_cfg = structure_cfg.get("generale", {})
    mode_cfg = structure_cfg.get("modalita", {}).get(mode_name, {})

    rows = []
    rows.extend(_prefixed_flatten("sistema.scaling", system_cfg))
    rows.extend(_prefixed_flatten("generale", general_cfg))
    rows.extend(_prefixed_flatten(f"modalita.{mode_name}", mode_cfg))

    system_rows = [r for r in rows if r["path"].startswith("sistema.")]
    general_rows = [r for r in rows if r["path"].startswith("generale.")]
    mode_rows = [r for r in rows if r["path"].startswith("modalita.")]

    pieces = []
    if system_rows:
        pieces.append(
            "Sistema: " + "; ".join(
                f"{r['path']}={_display_param(r['path'], r['value'])}" for r in system_rows
            ) + "."
        )
    if general_rows:
        pieces.append(
            "Valori generali, attivi in ogni modalità della struttura: " + "; ".join(
                f"{r['path']}={_display_param(r['path'], r['value'])}" for r in general_rows
            ) + "."
        )
    else:
        pieces.append("La struttura non ha parametri generali aggiuntivi configurati.")
    if mode_rows:
        pieces.append(
            f"Valori specifici della modalità {mode_name}: " + "; ".join(
                f"{r['path']}={_display_param(r['path'], r['value'])}" for r in mode_rows
            ) + "."
        )
    else:
        pieces.append(f"La modalità {mode_name} non aggiunge parametri specifici oltre ai valori generali.")
    return " ".join(pieces), rows


def build_data():
    data = v3.build_data()

    # Descrizione narrativa da liste.usabili + descrizione tecnica centralizzata.
    for item in data.get("items", []):
        if item["name"] in getattr(v3.liste, "usabili", {}):
            item["usable_technical"] = FRASI_USABILI_TECNICHE.get(item["name"], "")
        else:
            item["usable_technical"] = ""

    # Ogni modalità porta con sé TUTTI i parametri che la governano:
    # scaling globale + parametri generali struttura + parametri della modalità.
    for structure in data.get("assault", []):
        for mode in structure.get("modes", []):
            technical, rows = _structure_technical(structure["name"], mode["name"])
            mode["technical"] = technical
            mode["technical_params"] = rows

    data["meta"]["wiki_version"] = 4
    return data


ITEM_DETAIL_JS = r'''function itemDetail(name){const i=find(D.items,name);if(!i)return missing(name);let special='';if(i.ring){const r=find(D.rings,i.ring);if(r)special+=sectionTitle('Effetto anello')+`<div class="effect human">${esc(r.human||'')}</div><div class="effect">${esc(r.technical||'')}</div>`}if(i.book_effect){const c=find(D.incantations,i.book_effect);if(c)special+=sectionTitle('Incantesimo fornito')+`<p>${link('incantation',c.name)}</p><div class="effect">${esc(c.technical||'')}</div>`}if(i.nucleus)special+=sectionTitle('Nucleo')+`<p>${link('nucleus',i.nucleus,'Apri la meccanica completa del nucleo →')}</p>`;if(i.scaglione_source){const s=i.scaglione_source;special+=sectionTitle('Come si ottiene')+`<div class="card"><p><b>Dungeon:</b> ${link('room',s.room)} · azione <b>${esc(s.action)}</b>.</p><p><b>Probabilità nell’evento:</b> <span class="prob">${s.chance_pct}%</span>.</p><p>${esc(s.condition)}</p></div>`}return head(i.name,'Scheda unica dell’oggetto. Gli equipaggiamenti mostrano la progressione reale LV0 → LVMAX.','Oggetti')+`<div class="detail"><div>${i.description?`<div class="effect human">${esc(i.description)}</div>`:''}${i.usable_technical?sectionTitle('Effetto tecnico dell’usabile')+`<div class="effect">${esc(i.usable_technical)}</div>`:''}${sectionTitle('Tipologia')}<div class="chips">${i.types.map(x=>`<span class="chip">${esc(x)}</span>`).join('')}</div>${i.levels.length?sectionTitle('Statistiche LV0 → LVMAX')+levelsTable(i.levels):'<div class="note">Questo oggetto non usa livelli equipaggiamento.</div>'}${i.forging?sectionTitle('Come si ottengono LVX e LVMAX')+`<div class="card"><p><b>LVX:</b> ${esc(i.forging.lvx)}</p><p><b>LVMAX:</b> ${esc(i.forging.lvmax)}</p><p>${link('events','Scaglioni','Vedi dove trovare i quattro scaglioni →')}</p></div>`:''}${i.sets.length?sectionTitle('Set che lo usano')+chipLinks('set',i.sets):''}${i.events.length?sectionTitle('Eventi collegati')+chipLinks('event',i.events):''}${i.boss_drops.length?sectionTitle('Drop dei boss')+`<div class="card">${i.boss_drops.map(x=>`<div class="rowlink" onclick="location.hash='boss/${enc(x.boss)}'"><span>${esc(x.boss)}</span><span class="prob">${x.pct}%</span></div>`).join('')}</div>`:''}${i.location_drops.length?sectionTitle('Pool delle location')+`<div class="card">${i.location_drops.map(x=>`<div class="rowlink" onclick="location.hash='location/${enc(x.location)}'"><span>${esc(x.location)}</span><span class="prob">${x.pct}%</span></div>`).join('')}</div>`:''}${special}</div><aside class="sidebox">${img('items',i.name,i.icon||'🎒')}</aside></div>`}'''


STRUCTURE_DETAIL_JS = r'''function structureDetail(name){const a=find(D.assault,name);if(!a)return missing(name);const first=a.modes[0];return head(a.name,`Struttura d’assalto. Scaling base: stat × (1 + livello/${a.divisor}).`,'Assalto')+`<div class="detail"><div>${sectionTitle('Modalità')}<div class="modebar" id="modebar">${a.modes.map((m,i)=>`<button class="btn ${i===0?'active':''}" data-mode="${esc(m.name)}">${esc(m.name)}</button>`).join('')}</div><div id="modeDesc" class="effect human">${esc(first.description||'—')}</div>${sectionTitle('Funzionamento tecnico completo')}<div id="modeTechnical" class="effect">${esc(first.technical||'—')}</div><div id="modeConfig">${config(first.technical_params)}</div>${sectionTitle('Statistiche della modalità')}<div class="levelbox"><b>LV <span id="structLv">0</span></b><input id="structRange" type="range" min="0" max="50" value="0"></div><div id="structStats">${stats(first.levels[0].stats)}</div>${sectionTitle('Statistiche a ogni livello')}<div id="structTable">${statsTable(first.levels)}</div>${a.set_refs.length?sectionTitle('Set collegati / counter')+chipLinks('set',a.set_refs):''}</div><aside class="sidebox">${img('assault',a.name,'🏰')}<div class="card" style="margin-top:12px"><h3>Stats base</h3>${stats(a.base_stats)}${a.resource_value!=null?`<p class="muted">Valore <code>hps</code> nel database: ${esc(a.resource_value)}</p>`:''}</div></aside></div>`}'''


def build_html():
    html = v3.HTML

    # encodeURIComponent lascia invariato l'apostrofo: dentro gli onclick in
    # apici singoli rompeva nomi come Dell'ambrosia. Lo trasformiamo in %27.
    html = v3._must_replace(
        html,
        "const enc=s=>encodeURIComponent(String(s)), dec=s=>decodeURIComponent(s||''), base=s=>String(s||'').split(' LV')[0];",
        "const enc=s=>encodeURIComponent(String(s)).replace(/'/g,'%27'), dec=s=>decodeURIComponent(s||''), base=s=>String(s||'').split(' LV')[0];",
        "routing apostrofi",
    )

    html = v3._replace_js_function(html, "itemDetail", "setDetail", ITEM_DETAIL_JS)
    html = v3._replace_js_function(html, "structureDetail", "sectionTitle", STRUCTURE_DETAIL_JS)

    old = "document.getElementById('modeDesc').textContent=m.description||'—';document.getElementById('modeConfig').innerHTML=config(m.config);"
    new = "document.getElementById('modeDesc').textContent=m.description||'—';document.getElementById('modeTechnical').textContent=m.technical||'—';document.getElementById('modeConfig').innerHTML=config(m.technical_params||m.config);"
    html = v3._must_replace(html, old, new, "aggiornamento testo tecnico modalità")
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

    print("Wiki v4 generata:", out)
    print(json.dumps(data["meta"]["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

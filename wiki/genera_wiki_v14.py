#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wiki v14: URL con ID stabili e nomi entità localizzati IT/EN/ES."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import genera_wiki_v13 as v13
from entity_registry import resolve_id


ROOT = v13.ROOT
v12 = v13.v12
v11 = v13.v11
v10 = v13.v10
v9 = v13.v9
v8 = v13.v8
v7 = v13.v7
v6 = v13.v6
v5 = v13.v5
v4 = v13.v4
v3 = v13.v3
v2 = v13.v2
bilanciamento = v13.bilanciamento
liste = v13.liste
_prefixed_flatten = v13._prefixed_flatten
_structure_technical = v13._structure_technical


def _add_ids(rows, kind):
    for row in rows or []:
        if not isinstance(row, dict) or not isinstance(row.get("name"), str):
            continue
        entity_id = resolve_id(row["name"], kind)
        if entity_id:
            row["id"] = entity_id


def build_data():
    data = v13.build_data()

    # Gli ingredienti sono veri oggetti dello zaino, ma nelle versioni
    # precedenti comparivano soltanto come testo nella guida pesca. Da v14
    # ricevono una scheda e un URL stabile come tutti gli altri oggetti.
    items = data.setdefault("items", [])
    known_items = {row.get("name") for row in items if isinstance(row, dict)}
    for name in dict.fromkeys(getattr(liste, "ingredienti", [])):
        if not isinstance(name, str) or not name.strip() or name in known_items:
            continue
        items.append({
            "name": name,
            "types": ["Ingrediente"],
            "icon": "🧪",
            "levels": [],
            "sets": [],
            "description": "Ingrediente del sistema delle pozioni.",
            "ring": None,
            "book_effect": None,
            "nucleus": None,
            "events": [],
            "scaglione_source": None,
            "forging": None,
            "boss_drops": [],
            "location_drops": [],
            "usable_technical": "",
            "is_collectible": False,
            "is_usable": False,
            "shop_price": None,
            "arena_sources": [],
            "weekly_gold": False,
            "raw_score": None,
            "raw_score_basis": None,
        })
        known_items.add(name)
    items.sort(key=lambda row: str(row.get("name", "")).casefold())

    collections = {
        "set": data.get("sets", []),
        "ring": data.get("rings", []),
        "incantation": data.get("incantations", []),
        "item": data.get("items", []),
        "boss": data.get("bosses", []),
        "enemy": data.get("enemies", []),
        "location": data.get("locations", []),
        "room": data.get("dungeon", {}).get("rooms", []),
        "structure": data.get("assault", []),
        "approach": data.get("approaches", []),
        "nucleus": data.get("nuclei", []),
        "event": data.get("events", []),
        "modifier": data.get("modifiers", []),
        "scaglione": data.get("scaglioni", []),
        "achievement": data.get("achievements", []),
        "marine_boss": data.get("marine_bosses", []),
    }
    for kind, rows in collections.items():
        _add_ids(rows, kind)

    # Le stesse schede compaiono anche in sezioni aggregate della pesca/weekend.
    _add_ids(data.get("fishing", {}).get("locations", []), "location")
    _add_ids(data.get("fishing", {}).get("marine_encounters", {}).get("bosses", []), "marine_boss")
    _add_ids(data.get("weekend", {}).get("mods", []), "modifier")

    data["meta"]["wiki_version"] = 14
    data["meta"]["entity_schema_version"] = 1
    data["meta"]["counts"]["items"] = len(items)
    return data


def build_html():
    html = v13.HTML
    html = v3._must_replace(
        html,
        "const route=(type,name)=>`#${type}/${enc(name)}`; const link=(type,name,label=name)=>`<a href=\"${route(type,name)}\">${esc(label)}</a>`;",
        "const route=(type,name)=>`#${type}/${enc(NFTI18n.entityId(name,type))}`; const link=(type,name,label=name)=>`<a href=\"${route(type,name)}\">${esc(label)}</a>`;",
        "Wiki v14 route con ID",
    )
    html = v3._must_replace(
        html,
        "const find=(arr,name)=>arr.find(x=>x.name===name);",
        "const find=(arr,name)=>arr.find(x=>x.id===name||x.name===name);",
        "Wiki v14 lookup ID o nome legacy",
    )
    html = v3._must_replace(
        html,
        "function go(hash){location.hash=hash==='home'?'home':hash}",
        "function go(hash,name){location.hash=name===undefined?(hash==='home'?'home':hash):route(hash,name).slice(1)}",
        "Wiki v14 navigazione compatibile",
    )
    old_list = "function listPage(title,sub,arr,type,extra=x=>'',icon='•'){return head(title,sub)+`<div class=\"entity-grid\">${arr.map(x=>`<div class=\"card clickcard\" data-search=\"${esc((x.name+' '+extra(x)).toLowerCase())}\" onclick=\"location.hash='${type}/${enc(x.name)}'\"><h3>${typeof icon==='function'?icon(x):icon} ${esc(x.name)}</h3><div class=\"muted\">${esc(extra(x))}</div></div>`).join('')}</div>`}"
    new_list = "function listPage(title,sub,arr,type,extra=x=>'',icon='•'){return head(title,sub)+`<div class=\"entity-grid\">${arr.map(x=>`<div class=\"card clickcard\" data-search=\"${esc((NFTI18n.entitySearch(x.id||x.name,type)+' '+extra(x)).toLowerCase())}\" onclick=\"location.hash='${route(type,x.id||x.name).slice(1)}'\"><h3>${typeof icon==='function'?icon(x):icon} ${esc(x.name)}</h3><div class=\"muted\">${esc(extra(x))}</div></div>`).join('')}</div>`}"
    html = v3._must_replace(html, old_list, new_list, "Wiki v14 liste con ID")

    route_replacements = (
        ("location.hash='boss/${enc(x.boss)}'", "location.hash='${route('boss',x.boss).slice(1)}'"),
        ("location.hash='location/${enc(x.location)}'", "location.hash='${route('location',x.location).slice(1)}'"),
        ("location.hash='location/${enc(loc)}'", "location.hash='${route('location',loc).slice(1)}'"),
        ("location.hash='event/${enc(x)}'", "location.hash='${route('event',x).slice(1)}'"),
        ("location.hash='event/${enc(e.name)}'", "location.hash='${route('event',e.id||e.name).slice(1)}'"),
        ("location.hash='room/${enc(r.name)}'", "location.hash='${route('room',r.id||r.name).slice(1)}'"),
        ("location.hash='structure/${enc(a.name)}'", "location.hash='${route('structure',a.id||a.name).slice(1)}'"),
        ("location.hash='marineboss/${enc(b.name)}'", "location.hash='${route('marineboss',b.id||b.name).slice(1)}'"),
        ("location.hash='achievement/${enc(a.name)}'", "location.hash='${route('achievement',a.id||a.name).slice(1)}'"),
    )
    for old, new in route_replacements:
        if old not in html:
            raise RuntimeError(f"Patch HTML non applicabile: route legacy {old}")
        html = html.replace(old, new)

    old_ingredients = "<div class=\"chips\">${f.potions_now.ingredients.map(x=>`<span class=\"chip\">${esc(x)}</span>`).join('')||'<span class=\"muted\">—</span>'}</div>"
    new_ingredients = "${chipLinks('item',f.potions_now.ingredients)}"
    html = v3._must_replace(
        html,
        old_ingredients,
        new_ingredients,
        "Wiki v14 link ingredienti",
    )

    old_start = "window.addEventListener('hashchange',render);NFTI18n.init().then(render).catch(error=>{console.error(error);render()});"
    new_start = (
        "function canonicalRender(){"
        "const raw=(location.hash||'#home').slice(1),[type,...rest]=raw.split('/'),ref=dec(rest.join('/'));"
        "if(ref){const id=NFTI18n.entityId(ref,type);if(id&&id!==ref)history.replaceState(null,'',route(type,id));}"
        "render()}"
        "window.addEventListener('hashchange',canonicalRender);"
        "NFTI18n.init().then(canonicalRender).catch(error=>{console.error(error);render()});"
    )
    html = v3._must_replace(html, old_start, new_start, "Wiki v14 canonicalizzazione route")
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
    (out / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "i18n_web.js", out / "assets" / "i18n.js")
    shutil.copy2(ROOT / "entities.json", out / "entities.json")
    shutil.copytree(ROOT / "locales", out / "locales", dirs_exist_ok=True)
    print("Wiki v14 generata:", out)
    print(json.dumps(data["meta"]["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

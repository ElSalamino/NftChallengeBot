#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wiki procedurale navigabile per NftChallengeBot.

Tutti i dati derivano dai moduli reali del gioco. Il sito è una SPA statica con
routing hash: Home -> categoria -> entità -> collegamenti incrociati.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import string
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import liste  # noqa: E402
import bilanciamento  # noqa: E402
from frasi_set import FRASI_SET_TECNICHE  # noqa: E402
from frasi_anelli import FRASI_ANELLI_TECNICHE  # noqa: E402
from frasi_incantesimi import FRASI_INCANTESIMI_TECNICHE  # noqa: E402

STATS = ("hp", "atk", "def", "agi")


def n(value):
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        try:
            v = float(value.strip().replace(",", "."))
            return int(v) if v.is_integer() else v
        except Exception:
            return value
    return value


def base_item(name):
    return str(name).split(" LV", 1)[0]


def level_token(name):
    text = str(name)
    return text.split(" LV", 1)[1] if " LV" in text else "base"


def level_sort(token):
    t = str(token).upper()
    if t == "BASE": return (-1000, "")
    if t == "X": return (99998, "")
    if t == "MAX": return (99999, "")
    try: return (int(t), "")
    except Exception: return (90000, t)


def stat_dict(data):
    data = data or {}
    return {s: n(data.get(s, 0)) for s in STATS}


def weighted(values):
    values = list(values or [])
    total = len(values)
    counts = Counter(values)
    return [
        {"name": k, "weight": v, "pct": round(v * 100 / total, 2) if total else 0}
        for k, v in sorted(counts.items(), key=lambda x: (-x[1], str(x[0]).lower()))
    ]


def flatten(obj, prefix=""):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.extend(flatten(v, f"{prefix}.{k}" if prefix else str(k)))
    elif isinstance(obj, (list, tuple, set)):
        out.append({"path": prefix, "value": list(obj)})
    else:
        out.append({"path": prefix, "value": obj})
    return out


def resolve_path(config, path):
    value = config
    for part in path.split(".") if path else []:
        if not isinstance(value, dict) or part not in value:
            raise KeyError(path)
        value = value[part]
    return value


def num_text(value):
    value = n(value)
    if isinstance(value, float): return f"{value:g}"
    return str(value)


def format_placeholder(value, fmt=""):
    if fmt == "pct": return f"{num_text(value)}%"
    if fmt == "x": return f"{num_text(value)}x"
    if fmt == "signed":
        value = n(value)
        return f"+{num_text(value)}" if isinstance(value, (int, float)) and value > 0 else num_text(value)
    if fmt == "abs":
        value = n(value)
        return num_text(abs(value)) if isinstance(value, (int, float)) else num_text(value)
    if fmt == "bool": return "sì" if value else "no"
    if fmt == "rid_pct": return f"{num_text((1-float(value))*100)}%"
    if fmt == "pct_mul": return f"{num_text(float(value)*100)}%"
    return num_text(value)


def render_template(template, config, bonus=None):
    if not template:
        return ""
    bonus = bonus or {}
    out = []
    for literal, field, fmt, conversion in string.Formatter().parse(template):
        out.append(literal)
        if field is None:
            continue
        try:
            value = resolve_path(bonus, field[6:]) if field.startswith("bonus.") else resolve_path(config, field)
            out.append(format_placeholder(value, fmt))
        except Exception:
            out.append("{" + field + (":" + fmt if fmt else "") + "}")
    return "".join(out)


def clean_human(text):
    text = str(text or "").strip()
    for marker in ("⚙️ Dettagli tecnici", "⚙️ Dettagli del set", "⚙️ Dettagli dell'anello", "⚙️ Dettagli dell'incantesimo"):
        if marker in text:
            text = text.split(marker, 1)[0].rstrip()
    return text


def git_sha():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "unknown"


def source_text(path):
    try: return (ROOT / path).read_text(encoding="utf-8")
    except Exception: return ""


def extract_divisor(block, pattern, fallback):
    m = re.search(pattern, block, re.S)
    return n(m.group(1)) if m else fallback


def set_names():
    return sorted(
        set(getattr(liste, "classi", {}))
        | set(getattr(liste, "bonus", {}))
        | set(getattr(bilanciamento, "PROC_CLASSI", {}))
        | set(FRASI_SET_TECNICHE),
        key=str.lower,
    )


def set_data():
    out = []
    classi = getattr(liste, "classi", {})
    bonus_all = getattr(liste, "bonus", {})
    frasi_umane = getattr(liste, "frasi_set", {})
    approcci = getattr(liste, "Approccini", {})
    for name in set_names():
        cfg = bilanciamento.PROC_CLASSI.get(name, {})
        bonus = bonus_all.get(name, {})
        out.append({
            "name": name,
            "components": [base_item(x) for x in classi.get(name, [])],
            "approaches": list(approcci.get(name, [])),
            "bonus": stat_dict(bonus),
            "human": clean_human(frasi_umane.get(name, "")),
            "technical": render_template(FRASI_SET_TECNICHE.get(name, ""), cfg, bonus),
            "config": flatten(cfg),
        })
    return out


def ring_data():
    names = sorted(set(getattr(liste, "anelli", {})) | set(bilanciamento.PROC_ANELLI) | set(FRASI_ANELLI_TECNICHE), key=str.lower)
    return [{
        "name": name,
        "human": clean_human(getattr(liste, "anelli", {}).get(name, "")),
        "technical": render_template(FRASI_ANELLI_TECNICHE.get(name, ""), bilanciamento.PROC_ANELLI.get(name, {})),
        "config": flatten(bilanciamento.PROC_ANELLI.get(name, {})),
    } for name in names]


def incant_data():
    books_by_effect = defaultdict(list)
    for book, info in getattr(liste, "libri", {}).items():
        if isinstance(info, dict):
            effect = info.get("ef")
            if effect:
                books_by_effect[effect].append(book)
    names = sorted(set(bilanciamento.INCANTESIMI_CONFIG) | set(FRASI_INCANTESIMI_TECNICHE) | set(books_by_effect), key=str.lower)
    return [{
        "name": name,
        "books": sorted(books_by_effect.get(name, []), key=str.lower),
        "technical": render_template(FRASI_INCANTESIMI_TECNICHE.get(name, ""), bilanciamento.INCANTESIMI_CONFIG.get(name, {})),
        "config": flatten(bilanciamento.INCANTESIMI_CONFIG.get(name, {})),
    } for name in names]


def equipment_map():
    grouped = {}
    for kind, collection in [
        ("Arma", getattr(liste, "armi", {})),
        ("Arma", getattr(liste, "armiextra", {})),
        ("Protezione", getattr(liste, "protezioni", {})),
        ("Protezione", getattr(liste, "protezioniextra", {})),
    ]:
        for full, values in collection.items():
            base = base_item(full)
            d = grouped.setdefault(base, {"name": base, "types": set(), "levels": []})
            d["types"].add(kind)
            d["levels"].append({"label": level_token(full), "full_name": full, "stats": stat_dict(values), "raw": values})
    for d in grouped.values():
        d["types"] = sorted(d["types"])
        d["levels"].sort(key=lambda x: level_sort(x["label"]))
    return grouped


def safe_mapping(name):
    value = getattr(liste, name, {})
    return value if isinstance(value, dict) else {}


def item_data(sets):
    equip = equipment_map()
    usage = defaultdict(set)
    for s in sets:
        for c in s["components"]:
            usage[c].add(s["name"])

    locations_by_item = defaultdict(list)
    for loc, pool in getattr(liste, "pool", {}).items():
        for row in weighted(pool):
            locations_by_item[base_item(row["name"])].append({"location": loc, **row})
    bosses_by_item = defaultdict(list)
    for boss, pool in getattr(liste, "premi_boss", {}).items():
        for row in weighted(pool):
            bosses_by_item[base_item(row["name"])].append({"boss": boss, **row})

    names = set(equip)
    for s in sets:
        names.update(s["components"])
    for mapping_name in ("anelli", "libri", "usabili", "decoro", "shop"):
        value = getattr(liste, mapping_name, {})
        if isinstance(value, dict): names.update(base_item(k) for k in value)
        elif isinstance(value, (list, tuple, set)): names.update(base_item(k) for k in value)
    for pool in getattr(liste, "premi_boss", {}).values(): names.update(base_item(x) for x in pool)
    for pool in getattr(liste, "pool", {}).values(): names.update(base_item(x) for x in pool)
    for pool in getattr(liste, "pesciame", {}).values(): names.update(base_item(x) for x in pool)
    names.update(base_item(x) for x in getattr(liste, "pesci", []))

    anelli = safe_mapping("anelli")
    libri = safe_mapping("libri")
    usabili = safe_mapping("usabili")
    decoro = safe_mapping("decoro")
    shop = safe_mapping("shop")
    fish = set(base_item(x) for x in getattr(liste, "pesci", []))

    out = []
    for name in sorted(names, key=str.lower):
        types = set(equip.get(name, {}).get("types", []))
        desc = []
        ring = None
        book_effect = None
        if name in anelli:
            types.add("Anello")
            desc.append(clean_human(anelli.get(name)))
            ring = name
        if name in libri:
            types.add("Libro")
            info = libri[name]
            if isinstance(info, dict):
                book_effect = info.get("ef")
                if info.get("descrizione"): desc.append(clean_human(info.get("descrizione")))
        if name in usabili:
            types.add("Usabile")
            if isinstance(usabili.get(name), str): desc.append(usabili.get(name))
        if name in decoro:
            types.add("Decorativo / lore")
            if isinstance(decoro.get(name), str): desc.append(decoro.get(name))
        if name in shop: types.add("Shop")
        if name in fish: types.add("Pesce")
        if not types: types.add("Oggetto")
        out.append({
            "name": name,
            "types": sorted(types),
            "levels": equip.get(name, {}).get("levels", []),
            "sets": sorted(usage.get(name, []), key=str.lower),
            "description": "\n".join(x for x in desc if x),
            "ring": ring,
            "book_effect": book_effect,
            "boss_drops": sorted(bosses_by_item.get(name, []), key=lambda x: x["boss"].lower()),
            "location_drops": sorted(locations_by_item.get(name, []), key=lambda x: x["location"].lower()),
        })
    return out


def drop_reason(item, boss_data):
    b = base_item(item)
    if b == base_item(boss_data.get("anello")):
        return "È l'anello/gadget equipaggiato dal boss."
    related = []
    for s, comps in getattr(liste, "classi", {}).items():
        if b in [base_item(c) for c in comps or []]: related.append(s)
    if related:
        return "È un componente di set: " + ", ".join(sorted(related, key=str.lower)) + "."
    if b in safe_mapping("decoro"):
        return "È un oggetto lore/decorativo associato al boss."
    if b in safe_mapping("usabili"):
        return "È un usabile nel pool dedicato del boss."
    return "È presente nel pool drop dedicato definito per questo boss."


def boss_data():
    src = source_text("nft.py")
    block = src[src.find("async def bossata("):src.find("def genera_dungeon(")]
    div = extract_divisor(block, r"forza\s*/\s*([0-9]+(?:\.[0-9]+)?)", 12)
    out = []
    for name, b in getattr(liste, "Boss", {}).items():
        base = stat_dict(b)
        levels = []
        for lv in range(51):
            levels.append({"level": lv, "stats": {k: round(float(base[k]) * (1 + lv / float(div))) for k in STATS}})
        drops = []
        for row in weighted(getattr(liste, "premi_boss", {}).get(name, [])):
            row["item"] = base_item(row["name"])
            row["reason"] = drop_reason(row["name"], b)
            drops.append(row)
        out.append({
            "name": name,
            "stats": base,
            "set": b.get("set"),
            "ring": b.get("anello"),
            "approach": b.get("Ap"),
            "scale_divisor": div,
            "levels": levels,
            "drops": drops,
        })
    return sorted(out, key=lambda x: x["name"].lower())


def enemy_data():
    locs = defaultdict(dict)
    for loc, pool in getattr(liste, "casa_nemici", {}).items():
        for row in weighted(pool): locs[row["name"]][loc] = {"weight": row["weight"], "pct": row["pct"]}
    out = []
    for name, e in getattr(liste, "nemici", {}).items():
        out.append({"name": name, "stats": stat_dict(e), "set": e.get("set"), "ring": e.get("anello"), "approach": e.get("Ap"), "locations": locs.get(name, {})})
    return sorted(out, key=lambda x: x["name"].lower())


def location_data():
    names = list(getattr(liste, "location", []))
    for src in (getattr(liste, "move", {}), getattr(liste, "casa_nemici", {}), getattr(liste, "pool", {}), getattr(liste, "pesciame", {})):
        for name in src:
            if name not in names: names.append(name)
    return [{
        "name": loc,
        "emoji": getattr(liste, "moji_posto", {}).get(loc, ""),
        "routes": list(getattr(liste, "move", {}).get(loc, [])),
        "loot": [{**x, "item": base_item(x["name"])} for x in weighted(getattr(liste, "pool", {}).get(loc, []))],
        "enemies": weighted(getattr(liste, "casa_nemici", {}).get(loc, [])),
        "fish": [base_item(x) for x in getattr(liste, "pesciame", {}).get(loc, [])],
    } for loc in names]


def room_actions_from_runtime(src):
    actions = defaultdict(set)
    for action, room in re.findall(r'scelta\s*==\s*["\']([^"\']+)["\'](?:(?!\n\s*if\s).){0,260}?["\']([^"\']+)["\']\s+in\s+player\[username\]\["dungeon"\]\["mostri"\]', src, re.S):
        actions[room].add(action)
    return actions


def room_intro(src, room):
    marker = f'if scelta == "{room}":'
    start = src.find(marker)
    if start < 0:
        marker = f"if scelta == '{room}':"
        start = src.find(marker)
    if start < 0: return ""
    block = src[start:start+2600]
    end_candidates = [x for x in (block.find('\n                if scelta ==', 10), block.find('\n                if fines', 10)) if x > 0]
    if end_candidates: block = block[:min(end_candidates)]
    texts = []
    for m in re.finditer(r'text\s*\+=\s*(?:\(?\s*)?(["\']{1,3})(.*?)(?:\1)', block, re.S):
        raw = m.group(2)
        raw = raw.replace('\\\n', '\n').replace('\\n', '\n')
        raw = re.sub(r'\{[^{}]+\}', '…', raw)
        if raw.strip(): texts.append(raw.strip())
    return "\n".join(texts[:3])


def dungeon_data():
    src = source_text("nft.py")
    actions = room_actions_from_runtime(src)
    cfg_rooms = bilanciamento.DUNGEON_CONFIG.get("stanze", {})
    rooms = list(dict.fromkeys(getattr(liste, "stanze", [])))
    for r in cfg_rooms:
        if r not in rooms: rooms.append(r)
    weights = {x["name"]: x for x in weighted(getattr(liste, "stanze", []))}
    boss_block = src[src.find("async def dungeon_boss("):src.find("async def dungeon_mostro(")]
    normal_block = src[src.find("async def dungeon_mostro("):src.find("ARENA_MATCH_TIMEOUT")]
    boss_div = extract_divisor(boss_block, r'\["piano"\]\s*/\s*([0-9]+(?:\.[0-9]+)?)', 10)
    normal_div = extract_divisor(normal_block, r'\["piano"\]\s*/\s*([0-9]+(?:\.[0-9]+)?)', 8)
    rows = []
    for room in rooms:
        w = weights.get(room, {"weight": 0, "pct": 0})
        cfg = cfg_rooms.get(room, {})
        rows.append({
            "name": room,
            "intro": room_intro(src, room),
            "weight": w["weight"], "pct": w["pct"],
            "actions": sorted(set(actions.get(room, set())) | set(cfg), key=str.lower),
            "config": flatten(cfg),
        })
    return {
        "rooms": rows,
        "global": {k: flatten(v) for k, v in bilanciamento.DUNGEON_CONFIG.items() if k != "stanze"},
        "scaling": {"normal_divisor": normal_div, "boss_divisor": boss_div},
    }


def apply_mode_stats(stats, mode_cfg):
    out = {k: float(stats.get(k, 0)) for k in STATS}
    original = dict(out)
    for stat in STATS:
        if f"{stat}_mul" in mode_cfg: out[stat] *= float(mode_cfg[f"{stat}_mul"])
        if f"{stat}_divisore" in mode_cfg: out[stat] /= float(mode_cfg[f"{stat}_divisore"])
        if f"{stat}_delta" in mode_cfg: out[stat] += float(mode_cfg[f"{stat}_delta"])
        if f"bonus_{stat}" in mode_cfg: out[stat] += float(mode_cfg[f"bonus_{stat}"])
    if "atk_da_def_mul" in mode_cfg:
        out["atk"] = original["def"] * float(mode_cfg["atk_da_def_mul"])
    if "def_da_atk_divisore" in mode_cfg:
        out["def"] = original["atk"] / float(mode_cfg["def_da_atk_divisore"])
    return {k: round(v) for k, v in out.items()}


def assault_data(sets):
    cfg_all = getattr(bilanciamento, "STRUTTURE_CONFIG", {})
    divisor = n(cfg_all.get("generale", {}).get("scaling", {}).get("divisore_livello", 10))
    structures = list(getattr(liste, "order", [])) or list(getattr(liste, "starmi", {}))
    out = []
    for name in structures:
        base = stat_dict(getattr(liste, "starmi", {}).get(name, {}))
        cfg = cfg_all.get(name, {})
        modes = []
        mode_names = list(getattr(liste, "spec", {}).get(name, []))
        for m in cfg.get("modalita", {}):
            if m not in mode_names: mode_names.append(m)
        if not mode_names: mode_names = ["Base"]
        for mode in mode_names:
            mode_cfg = cfg.get("modalita", {}).get(mode, {}) if mode != "Base" else {}
            levels = []
            for lv in range(51):
                scaled = {k: round(float(base[k]) * (1 + lv / float(divisor))) for k in STATS}
                levels.append({"level": lv, "stats": apply_mode_stats(scaled, mode_cfg)})
            modes.append({
                "name": mode,
                "description": getattr(liste, "frasispec", {}).get(mode, "Modalità base della struttura." if mode == "Base" else ""),
                "config": flatten(mode_cfg),
                "levels": levels,
            })
        refs = []
        for s in sets:
            cfg_s = bilanciamento.PROC_CLASSI.get(s["name"], {})
            text = json.dumps(cfg_s, ensure_ascii=False).lower() + " " + s.get("technical", "").lower()
            if name.lower() in text or (len(name.split()[0]) >= 4 and name.split()[0].lower() in text):
                refs.append(s["name"])
        out.append({
            "name": name,
            "base_stats": base,
            "resource_value": n(getattr(liste, "hps", {}).get(name)),
            "general_config": flatten(cfg.get("generale", {})),
            "modes": modes,
            "set_refs": sorted(set(refs), key=str.lower),
            "divisor": divisor,
        })
    return out


def build_data():
    sets = set_data()
    data = {
        "meta": {"generated_at": datetime.now(timezone.utc).isoformat(), "commit": git_sha(), "repository": "ElSalamino/NftChallengeBot"},
        "sets": sets,
        "rings": ring_data(),
        "incantations": incant_data(),
        "items": item_data(sets),
        "bosses": boss_data(),
        "enemies": enemy_data(),
        "locations": location_data(),
        "dungeon": dungeon_data(),
        "assault": assault_data(sets),
    }
    data["meta"]["counts"] = {k: len(data[k]) for k in ("bosses", "enemies", "locations", "items", "sets", "rings", "incantations", "assault")}
    data["meta"]["counts"]["rooms"] = len(data["dungeon"]["rooms"])
    return data


HTML = r'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>NftChallengeBot Wiki</title>
<style>
:root{--bg:#090c12;--panel:#121824;--panel2:#192235;--line:#2a3650;--text:#f2f5ff;--muted:#aab5ca;--accent:#79a9ff;--green:#7be0a4;--gold:#ffd27a;--radius:15px;--shadow:0 18px 50px #0006}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 70% -10%,#1a2742 0,#090c12 42%);color:var(--text);font:15px/1.55 Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif}a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}button,input{font:inherit}.wrap{max-width:1320px;margin:auto;padding:0 22px 70px}.topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:14px;padding:14px 0;background:linear-gradient(#090c12f5 75%,transparent)}.brand{font-weight:900;font-size:18px;cursor:pointer;white-space:nowrap}.search{flex:1;max-width:720px;background:#111827;border:1px solid var(--line);color:var(--text);padding:10px 13px;border-radius:11px}.commit{font:11px ui-monospace,monospace;color:var(--muted)}.hero{min-height:340px;border:1px solid var(--line);border-radius:22px;overflow:hidden;position:relative;background:linear-gradient(135deg,#18243a,#0f1522);box-shadow:var(--shadow);display:grid;align-items:end;margin:10px 0 28px}.hero-media{position:absolute;inset:0}.hero-media img{width:100%;height:100%;object-fit:cover;opacity:.62}.hero-media:after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,#0c111c 5%,#0c111c88 55%,transparent)}.hero-copy{position:relative;padding:34px;max-width:780px}.hero h1{font-size:clamp(34px,7vw,68px);line-height:.95;margin:0 0 12px}.hero p{font-size:17px;color:#d7deed}.eyebrow{letter-spacing:.13em;text-transform:uppercase;color:var(--gold);font-weight:800;font-size:12px}.category-grid,.entity-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}.category{min-height:180px;position:relative;overflow:hidden;border:1px solid var(--line);border-radius:var(--radius);background:var(--panel);cursor:pointer;box-shadow:0 8px 24px #0003}.category:hover{transform:translateY(-2px);border-color:#4d6592}.category img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.38}.category .fallback{position:absolute;inset:0;display:grid;place-items:center;font-size:64px;background:linear-gradient(135deg,#1f2e4b,#101625)}.category .copy{position:absolute;inset:auto 0 0;padding:18px;background:linear-gradient(transparent,#0c111df2)}.category h3{margin:0;font-size:22px}.category p{margin:4px 0 0;color:var(--muted)}.pagehead{display:flex;align-items:end;justify-content:space-between;gap:18px;margin:22px 0}.pagehead h1{font-size:38px;margin:0}.pagehead p{color:var(--muted);margin:5px 0 0;max-width:800px}.breadcrumb{color:var(--muted);font-size:13px;margin:15px 0}.card{border:1px solid var(--line);background:var(--panel);border-radius:var(--radius);padding:17px}.clickcard{cursor:pointer}.clickcard:hover{border-color:#4d6592;background:#151d2c}.card h3{margin:0 0 5px}.muted{color:var(--muted)}.chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}.chip,.btn{display:inline-flex;align-items:center;gap:5px;padding:5px 9px;border:1px solid var(--line);background:var(--panel2);border-radius:999px;color:var(--text);font-size:12px}.chip.link{cursor:pointer;color:#cfe0ff}.btn{font-size:14px;cursor:pointer;padding:7px 12px}.btn.active{border-color:var(--accent);background:#203257}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:12px 0}.stat{background:var(--panel2);border:1px solid #25314a;padding:9px;border-radius:10px;text-align:center}.stat small{color:var(--muted)}.stat b{display:block;font-size:19px}.detail{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(280px,.75fr);gap:18px}.sidebox{position:sticky;top:78px;align-self:start}.imagebox{height:260px;border:1px solid var(--line);background:linear-gradient(135deg,#1c2a43,#101622);border-radius:var(--radius);overflow:hidden;display:grid;place-items:center}.imagebox img{width:100%;height:100%;object-fit:cover}.imagebox .fallback{font-size:68px}.section{margin:18px 0}.section h2{margin:0 0 10px;font-size:23px}.effect{white-space:pre-wrap;border-left:4px solid var(--accent);background:#101827;padding:12px 14px;border-radius:8px;margin:9px 0}.effect.human{border-color:var(--green)}.tablewrap{overflow:auto;border:1px solid var(--line);border-radius:12px}.tbl{width:100%;border-collapse:collapse;min-width:560px}.tbl th,.tbl td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}.tbl th{color:var(--muted);font-size:12px;background:#111827;position:sticky;top:0}.prob{color:var(--green)}.rowlink{display:flex;justify-content:space-between;gap:12px;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:#111824;cursor:pointer}.rowlink:hover{border-color:#4d6592}.modebar{display:flex;gap:7px;flex-wrap:wrap;margin:10px 0}.levelbox{display:flex;gap:12px;align-items:center;flex-wrap:wrap}.levelbox input{width:min(420px,100%)}details{margin:8px 0}summary{cursor:pointer;color:#bcd0ff}.tech{font:12px ui-monospace,SFMono-Regular,Consolas,monospace}.empty{padding:17px;border:1px dashed var(--line);border-radius:10px;color:var(--muted)}.note{padding:11px 13px;border:1px solid #514529;background:#211c10;border-radius:10px;color:#ffe6ae}.back{cursor:pointer;color:var(--accent);font-weight:700}@media(max-width:850px){.detail{grid-template-columns:1fr}.sidebox{position:static}.stats{grid-template-columns:repeat(2,1fr)}.hero{min-height:300px}.hero-copy{padding:24px}.topbar .commit{display:none}.pagehead{align-items:start;flex-direction:column}}
</style></head><body><div class="wrap"><div class="topbar"><div class="brand" onclick="go('home')">NftChallengeBot Wiki</div><input class="search" id="search" placeholder="Cerca in questa pagina…"><span class="commit" id="commit"></span></div><main id="app"></main></div>
<script id="wiki-data" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('wiki-data').textContent), app=document.getElementById('app'), search=document.getElementById('search');
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const enc=s=>encodeURIComponent(String(s)), dec=s=>decodeURIComponent(s||''), base=s=>String(s||'').split(' LV')[0];
const route=(type,name)=>`#${type}/${enc(name)}`; const link=(type,name,label=name)=>`<a href="${route(type,name)}">${esc(label)}</a>`;
const chipLinks=(type,arr)=>arr&&arr.length?`<div class="chips">${arr.map(x=>`<a class="chip link" href="${route(type,x)}">${esc(x)}</a>`).join('')}</div>`:'<span class="muted">—</span>';
const stats=s=>`<div class="stats">${['hp','atk','def','agi'].map(k=>`<div class="stat"><small>${k.toUpperCase()}</small><b>${esc(s?.[k]??0)}</b></div>`).join('')}</div>`;
const slug=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
function img(type,name,icon='🎮',cls='imagebox'){const key=slug(name);return `<div class="${cls}"><div class="fallback">${icon}</div><img alt="${esc(name)}" data-try="0" data-base="assets/${type}/${key}" src="assets/${type}/${key}.webp" onerror="imgFallback(this)"></div>`}
window.imgFallback=function(el){const ex=['.webp','.png','.jpg','.jpeg'];let i=Number(el.dataset.try||0)+1;if(i<ex.length){el.dataset.try=i;el.src=el.dataset.base+ex[i]}else el.style.display='none'};
const config=rows=>rows&&rows.length?`<details><summary>Variabili tecniche (${rows.length})</summary><div class="tablewrap"><table class="tbl tech"><tbody>${rows.map(r=>`<tr><th>${esc(r.path)}</th><td>${esc(Array.isArray(r.value)?r.value.join(', '):JSON.stringify(r.value)??r.value)}</td></tr>`).join('')}</tbody></table></div></details>`:'';
const head=(title,sub='',crumb='Home')=>`<div class="breadcrumb"><span class="back" onclick="history.back()">← Indietro</span> · <a href="#home">Home</a>${crumb&&crumb!=='Home'?' · '+crumb:''}</div><div class="pagehead"><div><h1>${esc(title)}</h1><p>${sub}</p></div></div>`;
const find=(arr,name)=>arr.find(x=>x.name===name);
function filterLocal(){const q=search.value.trim().toLowerCase();document.querySelectorAll('[data-search]').forEach(x=>x.style.display=!q||x.dataset.search.includes(q)?'':'none')}
search.oninput=filterLocal;
function go(hash){location.hash=hash==='home'?'home':hash}
function categoryCard(id,title,desc,icon){return `<div class="category" onclick="go('${id}')"><div class="fallback">${icon}</div><img data-try="0" data-base="assets/home/${id}" src="assets/home/${id}.webp" onerror="imgFallback(this)"><div class="copy"><h3>${title}</h3><p>${desc}</p></div></div>`}
function home(){return `<div class="hero"><div class="hero-media"><div class="fallback"></div><img data-try="0" data-base="assets/home/hero" src="assets/home/hero.webp" onerror="imgFallback(this)"></div><div class="hero-copy"><div class="eyebrow">Guida procedurale</div><h1>NftChallengeBot</h1><p>La wiki legge direttamente i dati del gioco. Ogni nome blu è navigabile: puoi passare da un boss al suo drop, dal drop al set, dal set ai componenti, dalla location ai nemici e tornare indietro.</p><div class="chips"><span class="chip">${D.meta.counts.bosses} Boss</span><span class="chip">${D.meta.counts.enemies} Nemici</span><span class="chip">${D.meta.counts.items} Oggetti</span><span class="chip">${D.meta.counts.sets} Set</span></div></div></div><div class="category-grid">${categoryCard('bosses','Boss','Boss giornalieri, livelli e drop.','👺')}${categoryCard('locations','Location','Collegamenti, loot, pesca e casa nemici.','🗺️')}${categoryCard('items','Oggetti','Oggetti senza LV, livelli, set e provenienza.','⚔️')}${categoryCard('sets','Set','Componenti, descrizione e meccanica tecnica.','🧩')}${categoryCard('enemies','Nemici','Nemici dungeon, statistiche e habitat.','👾')}${categoryCard('dungeon','Dungeon','Scaling, stanze, scelte ed effetti.','🚪')}${categoryCard('assault','Assalto','Strutture, modalità e statistiche per livello.','🏰')}${categoryCard('rings','Anelli','Gadget e proc.','💍')}${categoryCard('incantations','Incantesimi','Libri ed effetti.','📖')}</div>`}
function listPage(title,sub,arr,type,extra=x=>'',icon='•'){return head(title,sub)+`<div class="entity-grid">${arr.map(x=>`<div class="card clickcard" data-search="${esc((x.name+' '+extra(x)).toLowerCase())}" onclick="location.hash='${type}/${enc(x.name)}'"><h3>${icon} ${esc(x.name)}</h3><div class="muted">${esc(extra(x))}</div></div>`).join('')}</div>`}
function bossDetail(name){const b=find(D.bosses,name);if(!b)return missing(name);return head(b.name,'Boss giornaliero: statistiche, crescita e drop cliccabili.','Boss')+`<div class="detail"><div>${sectionTitle('Meccanica di crescita')}<div class="card"><p>Il livello di questo boss è personale. <b>Dopo ogni vittoria aumenta di 1</b>. Le statistiche vengono ricalcolate come <code>stat base × (1 + livello/${b.scale_divisor})</code>.</p><div class="levelbox"><b>Mostra LV <span id="bossLv">0</span></b><input id="bossRange" type="range" min="0" max="50" value="0"></div><div id="bossStats">${stats(b.levels[0].stats)}</div></div>${sectionTitle('Drop')}<div class="card"><div class="tablewrap"><table class="tbl"><thead><tr><th>Oggetto</th><th>Peso</th><th>Prob.</th><th>Perché</th></tr></thead><tbody>${b.drops.map(d=>`<tr><td>${link('item',d.item,d.name)}</td><td>${d.weight}</td><td class="prob">${d.pct}%</td><td>${esc(d.reason)}</td></tr>`).join('')}</tbody></table></div></div>${sectionTitle('Tabella completa LV 0–50')}<div class="tablewrap"><table class="tbl"><thead><tr><th>LV</th><th>HP</th><th>ATK</th><th>DEF</th><th>AGI</th></tr></thead><tbody>${b.levels.map(x=>`<tr><td>${x.level}</td><td>${x.stats.hp}</td><td>${x.stats.atk}</td><td>${x.stats.def}</td><td>${x.stats.agi}</td></tr>`).join('')}</tbody></table></div></div><aside class="sidebox">${img('bosses',b.name,'👺')}<div class="card" style="margin-top:12px">${stats(b.stats)}<p><b>Set:</b> ${b.set?link('set',b.set):'—'}</p><p><b>Anello:</b> ${b.ring?link('ring',b.ring):'—'}</p><p><b>Approccio:</b> ${esc(b.approach||'—')}</p></div></aside></div>`}
function locationDetail(name){const l=find(D.locations,name);if(!l)return missing(name);return head((l.emoji?l.emoji+' ':'')+l.name,'Tutto ciò che puoi raggiungere o trovare qui.','Location')+`<div class="detail"><div>${sectionTitle('Location collegate')}${chipLinks('location',l.routes)}${sectionTitle('Drop pool')}<div class="card">${weightedTable(l.loot,'item')}</div>${sectionTitle('Casa nemici dungeon')}<div class="card">${weightedTable(l.enemies,'enemy')}</div>${sectionTitle('Pesca')}${chipLinks('item',l.fish)}</div><aside class="sidebox">${img('locations',l.name,'🗺️')}</aside></div>`}
function itemDetail(name){const i=find(D.items,name);if(!i)return missing(name);let special='';if(i.ring){const r=find(D.rings,i.ring);if(r)special+=sectionTitle('Effetto anello')+`<div class="effect human">${esc(r.human||'')}</div><div class="effect">${esc(r.technical||'')}</div>${config(r.config)}`}if(i.book_effect){const c=find(D.incantations,i.book_effect);if(c)special+=sectionTitle('Incantesimo fornito')+`<p>${link('incantation',c.name)}</p><div class="effect">${esc(c.technical||'')}</div>`}return head(i.name,'Scheda unica dell’oggetto, indipendente dal livello.','Oggetti')+`<div class="detail"><div>${i.description?`<div class="effect human">${esc(i.description)}</div>`:''}${sectionTitle('Tipologia')}<div class="chips">${i.types.map(x=>`<span class="chip">${esc(x)}</span>`).join('')}</div>${i.levels.length?sectionTitle('Statistiche per livello')+levelsTable(i.levels):'<div class="note">Questo oggetto non ha una progressione LV con statistiche equipaggiamento.</div>'}${sectionTitle('Set che lo usano')}${chipLinks('set',i.sets)}${i.boss_drops.length?sectionTitle('Drop dei boss')+`<div class="card">${i.boss_drops.map(x=>`<div class="rowlink" onclick="location.hash='boss/${enc(x.boss)}'"><span>${esc(x.boss)}</span><span class="prob">${x.pct}%</span></div>`).join('')}</div>`:''}${i.location_drops.length?sectionTitle('Dove compare nei pool location')+`<div class="card">${i.location_drops.map(x=>`<div class="rowlink" onclick="location.hash='location/${enc(x.location)}'"><span>${esc(x.location)}</span><span class="prob">${x.pct}%</span></div>`).join('')}</div>`:''}${special}</div><aside class="sidebox">${img('items',i.name,'⚔️')}</aside></div>`}
function setDetail(name){const s=find(D.sets,name);if(!s)return missing(name);return head(s.name,'Composizione cliccabile, effetto leggibile ed effetto tecnico.','Set')+`<div class="detail"><div>${sectionTitle('Come si compone')}${chipLinks('item',s.components)}${sectionTitle('Effetto')}<div class="effect human">${esc(s.human||'Descrizione narrativa non presente.')}</div><div class="effect">${esc(s.technical||'Descrizione tecnica non presente.')}</div>${Object.values(s.bonus||{}).some(Number)?sectionTitle('Bonus grezzi')+stats(s.bonus):''}${sectionTitle('Approcci disponibili')}<div class="chips">${(s.approaches||[]).map(x=>`<span class="chip">${esc(x)}</span>`).join('')||'<span class="muted">—</span>'}</div>${config(s.config)}</div><aside class="sidebox">${img('sets',s.name,'🧩')}</aside></div>`}
function enemyDetail(name){const e=find(D.enemies,name);if(!e)return missing(name);return head(e.name,'Nemico del dungeon: statistiche, equipaggiamento e location.','Nemici')+`<div class="detail"><div>${sectionTitle('Statistiche base')}${stats(e.stats)}${sectionTitle('Equipaggiamento')}<div class="card"><p><b>Set:</b> ${e.set?link('set',e.set):'—'}</p><p><b>Anello:</b> ${e.ring?link('ring',e.ring):'—'}</p><p><b>Approccio:</b> ${esc(e.approach||'—')}</p></div>${sectionTitle('Dove si trova')}<div class="card">${Object.entries(e.locations).length?Object.entries(e.locations).map(([loc,w])=>`<div class="rowlink" onclick="location.hash='location/${enc(loc)}'"><span>${esc(loc)}</span><span class="prob">${w.pct}% · peso ${w.weight}</span></div>`).join(''):'<div class="empty">Non è assegnato a una casa nemici locale.</div>'}</div></div><aside class="sidebox">${img('enemies',e.name,'👾')}</aside></div>`}
function ringDetail(name){const r=find(D.rings,name);if(!r)return missing(name);return head(r.name,'Descrizione inventario ed effetto tecnico.','Anelli')+`<div class="detail"><div><div class="effect human">${esc(r.human||'—')}</div><div class="effect">${esc(r.technical||'—')}</div>${config(r.config)}</div><aside class="sidebox">${img('rings',r.name,'💍')}</aside></div>`}
function incantDetail(name){const c=find(D.incantations,name);if(!c)return missing(name);return head(c.name,'Incantesimo e libri che lo forniscono.','Incantesimi')+`<div class="detail"><div>${sectionTitle('Libri')}${chipLinks('item',c.books)}${sectionTitle('Effetto tecnico')}<div class="effect">${esc(c.technical||'—')}</div>${config(c.config)}</div><aside class="sidebox">${img('incantations',c.name,'📖')}</aside></div>`}
function dungeonHome(){const dg=D.dungeon;return head('Dungeon','Come vengono generati i piani e cosa fanno le stanze.','Dungeon')+`<div class="card"><h3>Combattimenti</h3><p><b>Nemico normale:</b> HP base dimezzati; ATK/DEF/AGI scalano con <code>1 + piano/${dg.scaling.normal_divisor}</code>.</p><p><b>Boss dungeon:</b> tutte le statistiche scalano con <code>1 + piano/${dg.scaling.boss_divisor}</code>; attacca per primo e riceve un incantamento casuale.</p></div>${sectionTitle('Stanze')}<div class="entity-grid">${dg.rooms.map(r=>`<div class="card clickcard" data-search="${esc((r.name+' '+r.actions.join(' ')).toLowerCase())}" onclick="location.hash='room/${enc(r.name)}'"><h3>🚪 ${esc(r.name)}</h3><div class="muted">${r.actions.length?esc(r.actions.join(' · ')):'Evento automatico'}${r.weight?` · peso ${r.weight}`:''}</div></div>`).join('')}</div>`}
function roomDetail(name){const r=find(D.dungeon.rooms,name);if(!r)return missing(name);return head(r.name,'Stanza del dungeon: presentazione, scelte e variabili.','Dungeon')+`<div class="detail"><div>${r.intro?`<div class="effect human">${esc(r.intro)}</div>`:''}${sectionTitle('Scelte / azioni')}<div class="chips">${r.actions.map(x=>`<span class="chip">${esc(x)}</span>`).join('')||'<span class="muted">Evento automatico</span>'}</div><p class="muted">Peso nel pool generico: ${r.weight} (${r.pct}%). Le location aggiungono inoltre due copie del proprio pool nemici alla generazione.</p>${config(r.config)}</div><aside class="sidebox">${img('rooms',r.name,'🚪')}</aside></div>`}
function assaultHome(){return head('Assalto','Scegli una struttura; nella scheda potrai cambiare modalità con un pulsante e vedere le statistiche di ogni livello.','Assalto')+`<div class="entity-grid">${D.assault.map(a=>`<div class="card clickcard" data-search="${esc((a.name+' '+a.modes.map(x=>x.name).join(' ')).toLowerCase())}" onclick="location.hash='structure/${enc(a.name)}'"><h3>🏰 ${esc(a.name)}</h3>${stats(a.base_stats)}<div class="muted">${esc(a.modes.map(x=>x.name).join(' · '))}</div></div>`).join('')}</div>`}
function structureDetail(name){const a=find(D.assault,name);if(!a)return missing(name);const first=a.modes[0];return head(a.name,`Struttura d’assalto. Scaling base: stat × (1 + livello/${a.divisor}).`,'Assalto')+`<div class="detail"><div>${sectionTitle('Modalità')}<div class="modebar" id="modebar">${a.modes.map((m,i)=>`<button class="btn ${i===0?'active':''}" data-mode="${esc(m.name)}">${esc(m.name)}</button>`).join('')}</div><div id="modeDesc" class="effect human">${esc(first.description||'—')}</div><div id="modeConfig">${config(first.config)}</div>${sectionTitle('Statistiche della modalità')}<div class="levelbox"><b>LV <span id="structLv">0</span></b><input id="structRange" type="range" min="0" max="50" value="0"></div><div id="structStats">${stats(first.levels[0].stats)}</div>${sectionTitle('Statistiche a ogni livello')}<div id="structTable">${statsTable(first.levels)}</div>${a.set_refs.length?sectionTitle('Set collegati / counter')+chipLinks('set',a.set_refs):''}${a.general_config.length?sectionTitle('Variabili generali della struttura')+config(a.general_config):''}</div><aside class="sidebox">${img('assault',a.name,'🏰')}<div class="card" style="margin-top:12px"><h3>Stats base</h3>${stats(a.base_stats)}${a.resource_value!=null?`<p class="muted">Valore <code>hps</code> nel database: ${esc(a.resource_value)}</p>`:''}</div></aside></div>`}
function sectionTitle(t){return `<div class="section"><h2>${esc(t)}</h2></div>`}
function levelsTable(levels){return `<div class="tablewrap"><table class="tbl"><thead><tr><th>Livello</th><th>HP</th><th>ATK</th><th>DEF</th><th>AGI</th></tr></thead><tbody>${levels.map(l=>`<tr><td>${esc(l.label)}</td><td>${l.stats.hp}</td><td>${l.stats.atk}</td><td>${l.stats.def}</td><td>${l.stats.agi}</td></tr>`).join('')}</tbody></table></div>`}
function statsTable(levels){return `<div class="tablewrap"><table class="tbl"><thead><tr><th>LV</th><th>HP</th><th>ATK</th><th>DEF</th><th>AGI</th></tr></thead><tbody>${levels.map(l=>`<tr><td>${l.level}</td><td>${l.stats.hp}</td><td>${l.stats.atk}</td><td>${l.stats.def}</td><td>${l.stats.agi}</td></tr>`).join('')}</tbody></table></div>`}
function weightedTable(rows,type){if(!rows.length)return '<div class="empty">Pool vuoto.</div>';return `<div class="tablewrap"><table class="tbl"><thead><tr><th>Nome</th><th>Peso</th><th>Prob.</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${type==='item'?link('item',r.item||base(r.name),r.name):link(type,r.name)}</td><td>${r.weight}</td><td class="prob">${r.pct}%</td></tr>`).join('')}</tbody></table></div>`}
function missing(name){return head('Non trovato','La voce richiesta non esiste nel commit pubblicato.')+`<div class="empty">${esc(name)}</div>`}
function afterRender(type,name){if(type==='boss'){const b=find(D.bosses,name),range=document.getElementById('bossRange');if(range)range.oninput=()=>{const lv=Number(range.value);document.getElementById('bossLv').textContent=lv;document.getElementById('bossStats').innerHTML=stats(b.levels[lv].stats)}}if(type==='structure'){const a=find(D.assault,name);let current=a?.modes?.[0];const renderMode=m=>{current=m;document.querySelectorAll('#modebar .btn').forEach(b=>b.classList.toggle('active',b.dataset.mode===m.name));document.getElementById('modeDesc').textContent=m.description||'—';document.getElementById('modeConfig').innerHTML=config(m.config);document.getElementById('structTable').innerHTML=statsTable(m.levels);const lv=Number(document.getElementById('structRange').value);document.getElementById('structStats').innerHTML=stats(m.levels[lv].stats)};document.querySelectorAll('#modebar .btn').forEach(b=>b.onclick=()=>renderMode(a.modes.find(m=>m.name===b.dataset.mode)));const range=document.getElementById('structRange');if(range)range.oninput=()=>{const lv=Number(range.value);document.getElementById('structLv').textContent=lv;document.getElementById('structStats').innerHTML=stats(current.levels[lv].stats)}}filterLocal()}
function render(){search.value='';const raw=(location.hash||'#home').slice(1),[type,...rest]=raw.split('/'),name=dec(rest.join('/'));let html='';if(type==='home'||!type)html=home();else if(type==='bosses')html=listPage('Boss','Seleziona un boss per vedere crescita, drop e statistiche.',D.bosses,'boss',x=>`${x.set||''} ${x.ring||''}`,'👺');else if(type==='boss')html=bossDetail(name);else if(type==='locations')html=listPage('Location','Seleziona una location per aprire collegamenti, loot, pesca e casa nemici.',D.locations,'location',x=>`${x.routes.join(' ')} ${x.enemies.map(y=>y.name).join(' ')}`,'🗺️');else if(type==='location')html=locationDetail(name);else if(type==='items')html=listPage('Oggetti','Tutti gli oggetti sono mostrati senza suffisso LV. Apri una voce per i livelli e i collegamenti.',D.items,'item',x=>x.types.join(' · '),'⚔️');else if(type==='item')html=itemDetail(name);else if(type==='sets')html=listPage('Set','Apri un set per componenti, effetto narrativo e meccanica tecnica.',D.sets,'set',x=>x.components.join(' · '),'🧩');else if(type==='set')html=setDetail(name);else if(type==='enemies')html=listPage('Nemici','Nemici del dungeon e location in cui possono apparire.',D.enemies,'enemy',x=>Object.keys(x.locations).join(' · '),'👾');else if(type==='enemy')html=enemyDetail(name);else if(type==='rings')html=listPage('Anelli','Gadget e relativi proc.',D.rings,'ring',x=>x.technical,'💍');else if(type==='ring')html=ringDetail(name);else if(type==='incantations')html=listPage('Incantesimi','Effetti e libri che li forniscono.',D.incantations,'incantation',x=>x.books.join(' · '),'📖');else if(type==='incantation')html=incantDetail(name);else if(type==='dungeon')html=dungeonHome();else if(type==='room')html=roomDetail(name);else if(type==='assault')html=assaultHome();else if(type==='structure')html=structureDetail(name);else html=missing(raw);app.innerHTML=html;document.getElementById('commit').textContent=(D.meta.commit||'').slice(0,8);afterRender(type,name);scrollTo({top:0,behavior:'instant'})}
window.addEventListener('hashchange',render);render();
</script></body></html>'''


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="_site")
    args = p.parse_args()
    out = Path(args.output)
    if not out.is_absolute(): out = ROOT / out
    out.mkdir(parents=True, exist_ok=True)
    data = build_data()
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (out / "index.html").write_text(HTML.replace("__DATA__", payload), encoding="utf-8")
    (out / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    assets = ROOT / "wiki" / "assets"
    if assets.exists():
        shutil.copytree(assets, out / "assets", dirs_exist_ok=True)
    print("Wiki generata:", out)
    print(json.dumps(data["meta"]["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

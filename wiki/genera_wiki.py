#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera la wiki procedurale di NftChallengeBot dai dati reali del repository.

Nessun dato di gioco viene mantenuto in una seconda copia: il sito importa i
moduli dati (liste/bilanciamento/frasi) e legge dal runtime solo le formule che
non sono ancora state centralizzate.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import re
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
    """Normalizza stringhe numeriche senza distruggere i valori testuali."""
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        s = value.strip().replace(",", ".")
        try:
            f = float(s)
            return int(f) if f.is_integer() else f
        except ValueError:
            return value
    return value


def num_text(value):
    value = n(value)
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)


def resolve_path(config, path):
    value = config
    for part in path.split(".") if path else []:
        if not isinstance(value, dict) or part not in value:
            raise KeyError(path)
        value = value[part]
    return value


def format_placeholder(value, fmt=""):
    if fmt == "pct":
        return f"{num_text(value)}%"
    if fmt == "x":
        return f"{num_text(value)}x"
    if fmt == "signed":
        value = n(value)
        if isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0:
            return f"+{num_text(value)}"
        return num_text(value)
    if fmt == "abs":
        value = n(value)
        return num_text(abs(value)) if isinstance(value, (int, float)) else num_text(value)
    if fmt == "bool":
        return "sì" if value else "no"
    if fmt == "rid_pct":
        return f"{num_text((1 - float(value)) * 100)}%"
    if fmt == "pct_mul":
        return f"{num_text(float(value) * 100)}%"
    return num_text(value)


def render_template(template, config, bonus=None):
    if not template:
        return ""
    out = []
    bonus = bonus or {}
    for literal, field, fmt, conversion in string.Formatter().parse(template):
        out.append(literal)
        if field is None:
            continue
        if conversion:
            out.append("{" + field + "}")
            continue
        try:
            if field.startswith("bonus."):
                value = resolve_path(bonus, field[6:])
            else:
                value = resolve_path(config, field)
            out.append(format_placeholder(value, fmt))
        except Exception:
            out.append("{" + field + (":" + fmt if fmt else "") + "}")
    return "".join(out)


def weighted(values):
    values = list(values or [])
    total = len(values)
    counts = Counter(values)
    return [
        {
            "name": name,
            "weight": count,
            "pct": round((count / total) * 100, 2) if total else 0,
        }
        for name, count in sorted(counts.items(), key=lambda x: (-x[1], str(x[0]).lower()))
    ]


def stat_dict(data):
    data = data or {}
    return {s: n(data.get(s, 0)) for s in STATS}


def base_item(name):
    return str(name).split(" LV", 1)[0]


def level_token(name):
    text = str(name)
    return text.split(" LV", 1)[1] if " LV" in text else "base"


def level_sort(token):
    t = str(token).upper()
    if t == "BASE":
        return (-1000, "")
    if t == "MAX":
        return (100000, "")
    if t == "X":
        return (99999, "")
    try:
        return (int(t), "")
    except ValueError:
        return (90000, t)


def flatten(obj, prefix=""):
    rows = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            rows.extend(flatten(value, path))
    elif isinstance(obj, (list, tuple, set)):
        rows.append({"path": prefix, "value": list(obj)})
    else:
        rows.append({"path": prefix, "value": obj})
    return rows


def git_sha():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "unknown"


def runtime_source():
    return (ROOT / "nft.py").read_text(encoding="utf-8")


def section(source, start_marker, end_marker=None):
    start = source.find(start_marker)
    if start < 0:
        return ""
    if end_marker:
        end = source.find(end_marker, start + len(start_marker))
        if end >= 0:
            return source[start:end]
    return source[start:]


def divisor_from(block, variable, fallback):
    hits = re.findall(rf"\b{re.escape(variable)}\s*/\s*([0-9]+(?:\.[0-9]+)?)", block)
    if not hits:
        return fallback
    return n(hits[0])


def room_actions_from_runtime(source):
    actions = defaultdict(set)
    pattern = re.compile(
        r"scelta\s*==\s*[\"']([^\"']+)[\"'](?:(?!\n\s*if\s).){0,220}?"
        r"[\"']([^\"']+)[\"']\s+in\s+player\[username\]\[\"dungeon\"\]\[\"mostri\"\]",
        re.S,
    )
    for action, room in pattern.findall(source):
        actions[room].add(action)
    # Bottoni dichiarati nella presentazione stanza: cattura anche azioni senza branch immediato.
    for room in set(getattr(liste, "stanze", [])):
        block_match = re.search(
            rf'if scelta == [\"\']{re.escape(str(room))}[\"\']:(.*?)(?=\n\s{{16}}if scelta ==|\n\s{{12}}if fines|\n\s{{8}}else:)',
            source,
            re.S,
        )
        if block_match:
            for quoted in re.findall(r'for appz in \[([^\]]+)\]', block_match.group(1)):
                for action in re.findall(r'[\"\']([^\"\']+)[\"\']', quoted):
                    actions[room].add(action)
    return {k: sorted(v, key=str.lower) for k, v in actions.items()}


def refs_for_text(config, needle):
    needle = str(needle).lower()
    matches = []
    for row in flatten(config):
        if needle in str(row["path"]).lower() or needle in str(row["value"]).lower():
            matches.append(row["path"])
    return matches


def equipment_data():
    collections = [
        ("Arma", getattr(liste, "armi", {})),
        ("Arma", getattr(liste, "armiextra", {})),
        ("Protezione", getattr(liste, "protezioni", {})),
        ("Protezione", getattr(liste, "protezioniextra", {})),
    ]
    grouped = {}
    for kind, collection in collections:
        for name, values in collection.items():
            base = base_item(name)
            key = (kind, base)
            grouped.setdefault(key, {"name": base, "kind": kind, "levels": []})
            grouped[key]["levels"].append(
                {
                    "label": level_token(name),
                    "full_name": name,
                    "stats": stat_dict(values),
                    "raw": values,
                }
            )
    component_sets = defaultdict(set)
    for set_name, components in getattr(liste, "classi", {}).items():
        for component in components or []:
            component_sets[base_item(component)].add(set_name)
    out = []
    for data in grouped.values():
        data["levels"].sort(key=lambda x: level_sort(x["label"]))
        data["sets"] = sorted(component_sets.get(data["name"], []), key=str.lower)
        out.append(data)
    return sorted(out, key=lambda x: (x["kind"], x["name"].lower()))


def set_data():
    out = []
    for name, components in getattr(liste, "classi", {}).items():
        cfg = bilanciamento.PROC_CLASSI.get(name, {})
        bonus = getattr(liste, "bonus", {}).get(name, {})
        effect = render_template(FRASI_SET_TECNICHE.get(name, ""), cfg, bonus)
        out.append(
            {
                "name": name,
                "components": list(components or []),
                "approaches": list(getattr(liste, "Approccini", {}).get(name, [])),
                "bonus": stat_dict(bonus),
                "effect": effect,
                "config": flatten(cfg),
                "source": "liste.classi + liste.bonus + bilanciamento.PROC_CLASSI + frasi_set.FRASI_SET_TECNICHE",
            }
        )
    return sorted(out, key=lambda x: str(x["name"]).lower())


def ring_data():
    names = set(getattr(liste, "anelli", {})) | set(bilanciamento.PROC_ANELLI) | set(FRASI_ANELLI_TECNICHE)
    out = []
    for name in names:
        cfg = bilanciamento.PROC_ANELLI.get(name, {})
        out.append(
            {
                "name": name,
                "description": getattr(liste, "anelli", {}).get(name, ""),
                "effect": render_template(FRASI_ANELLI_TECNICHE.get(name, ""), cfg),
                "config": flatten(cfg),
                "source": "liste.anelli + bilanciamento.PROC_ANELLI + frasi_anelli.FRASI_ANELLI_TECNICHE",
            }
        )
    return sorted(out, key=lambda x: str(x["name"]).lower())


def incant_data():
    books_by_effect = defaultdict(list)
    for book, data in getattr(liste, "libri", {}).items():
        if isinstance(data, dict) and data.get("ef"):
            books_by_effect[data["ef"]].append(book)
    names = set(bilanciamento.INCANTESIMI_CONFIG) | set(FRASI_INCANTESIMI_TECNICHE) | set(books_by_effect)
    out = []
    for name in names:
        cfg = bilanciamento.INCANTESIMI_CONFIG.get(name, {})
        out.append(
            {
                "name": name,
                "books": sorted(books_by_effect.get(name, []), key=str.lower),
                "effect": render_template(FRASI_INCANTESIMI_TECNICHE.get(name, ""), cfg),
                "config": flatten(cfg),
                "source": "liste.libri + bilanciamento.INCANTESIMI_CONFIG + frasi_incantesimi.FRASI_INCANTESIMI_TECNICHE",
            }
        )
    return sorted(out, key=lambda x: str(x["name"]).lower())


def drop_reason(item, boss):
    b = base_item(item)
    ring = str(boss.get("anello", ""))
    if b == base_item(ring):
        return "Anello equipaggiato dal boss"
    sets = []
    for set_name, components in getattr(liste, "classi", {}).items():
        if b in [base_item(c) for c in (components or [])]:
            sets.append(set_name)
    if sets:
        return "Componente set: " + ", ".join(sorted(sets, key=str.lower))
    if b in getattr(liste, "decoro", {}):
        desc = getattr(liste, "decoro", {}).get(b, "")
        return "Oggetto decorativo/lore" + (f" — {desc}" if desc else "")
    if b in getattr(liste, "usabili", {}):
        desc = getattr(liste, "usabili", {}).get(b, "")
        return "Usabile" + (f" — {desc}" if desc else "")
    return "Drop dedicato / equipaggiamento"


def boss_data(source):
    block = section(source, "async def bossata(", "def genera_dungeon(")
    scale_div = divisor_from(block, "forza", 12)
    out = []
    for name, data in getattr(liste, "Boss", {}).items():
        drops = []
        for row in weighted(getattr(liste, "premi_boss", {}).get(name, [])):
            row["reason"] = drop_reason(row["name"], data)
            drops.append(row)
        base_stats = stat_dict(data)
        levels = []
        for level in range(0, 51):
            levels.append(
                {
                    "level": level,
                    "stats": {
                        stat: round(float(base_stats[stat]) * (1 + level / float(scale_div)))
                        for stat in STATS
                    },
                }
            )
        set_name = data.get("set")
        ring = data.get("anello")
        out.append(
            {
                "name": name,
                "stats": base_stats,
                "set": set_name,
                "set_effect": render_template(
                    FRASI_SET_TECNICHE.get(set_name, ""),
                    bilanciamento.PROC_CLASSI.get(set_name, {}),
                    getattr(liste, "bonus", {}).get(set_name, {}),
                ),
                "ring": ring,
                "ring_effect": render_template(
                    FRASI_ANELLI_TECNICHE.get(ring, ""), bilanciamento.PROC_ANELLI.get(ring, {})
                ),
                "approach": data.get("Ap"),
                "drops": drops,
                "scale_divisor": scale_div,
                "levels": levels,
                "source": "liste.Boss + liste.premi_boss + runtime nft.bossata",
            }
        )
    return sorted(out, key=lambda x: str(x["name"]).lower()), scale_div


def enemy_data():
    locations = defaultdict(dict)
    for loc, pool in getattr(liste, "casa_nemici", {}).items():
        rows = weighted(pool)
        for row in rows:
            locations[row["name"]][loc] = {"weight": row["weight"], "pct": row["pct"]}
    out = []
    for name, data in getattr(liste, "nemici", {}).items():
        set_name = data.get("set")
        ring = data.get("anello")
        out.append(
            {
                "name": name,
                "stats": stat_dict(data),
                "set": set_name,
                "set_effect": render_template(
                    FRASI_SET_TECNICHE.get(set_name, ""),
                    bilanciamento.PROC_CLASSI.get(set_name, {}),
                    getattr(liste, "bonus", {}).get(set_name, {}),
                ),
                "ring": ring,
                "ring_effect": render_template(
                    FRASI_ANELLI_TECNICHE.get(ring, ""), bilanciamento.PROC_ANELLI.get(ring, {})
                ),
                "approach": data.get("Ap"),
                "locations": locations.get(name, {}),
                "source": "liste.nemici + liste.casa_nemici",
            }
        )
    return sorted(out, key=lambda x: str(x["name"]).lower())


def location_data():
    all_locations = list(getattr(liste, "location", []))
    for key in getattr(liste, "casa_nemici", {}):
        if key not in all_locations:
            all_locations.append(key)
    out = []
    for loc in all_locations:
        out.append(
            {
                "name": loc,
                "emoji": getattr(liste, "moji_posto", {}).get(loc, ""),
                "routes": list(getattr(liste, "move", {}).get(loc, [])),
                "fish": list(getattr(liste, "pesciame", {}).get(loc, [])),
                "enemies": weighted(getattr(liste, "casa_nemici", {}).get(loc, [])),
                "loot": weighted(getattr(liste, "pool", {}).get(loc, [])),
                "source": "liste.location + liste.move + liste.pesciame + liste.casa_nemici + liste.pool",
            }
        )
    return out


def dungeon_data(source):
    rooms = list(dict.fromkeys(getattr(liste, "stanze", [])))
    room_weights = {x["name"]: x for x in weighted(getattr(liste, "stanze", []))}
    actions = room_actions_from_runtime(source)
    cfg_rooms = bilanciamento.DUNGEON_CONFIG.get("stanze", {})
    for room in cfg_rooms:
        if room not in rooms:
            rooms.append(room)
    room_rows = []
    for room in rooms:
        w = room_weights.get(room, {"weight": 0, "pct": 0})
        cfg = cfg_rooms.get(room, {})
        action_names = set(actions.get(room, [])) | set(cfg.keys())
        room_rows.append(
            {
                "name": room,
                "weight": w["weight"],
                "pct": w["pct"],
                "actions": sorted(action_names, key=str.lower),
                "config": flatten(cfg),
                "source": "liste.stanze + bilanciamento.DUNGEON_CONFIG + runtime nft.dungeon_stanze",
            }
        )
    boss_block = section(source, "async def dungeon_boss(", "async def dungeon_mostro(")
    normal_block = section(source, "async def dungeon_mostro(", "ARENA_MATCH_TIMEOUT")
    boss_div = divisor_from(boss_block, 'piano\"][', 10)  # fallback; regex variable non utile qui
    # Lettura mirata delle due formule di scaling rimaste nel runtime.
    boss_hit = re.search(r'\[\"piano\"\]\s*/\s*([0-9]+(?:\.[0-9]+)?)', boss_block)
    normal_hit = re.search(r'\[\"piano\"\]\s*/\s*([0-9]+(?:\.[0-9]+)?)', normal_block)
    boss_div = n(boss_hit.group(1)) if boss_hit else 10
    normal_div = n(normal_hit.group(1)) if normal_hit else 8
    return {
        "rooms": room_rows,
        "global": {k: flatten(v) for k, v in bilanciamento.DUNGEON_CONFIG.items() if k != "stanze"},
        "weekend": [
            {"name": name, "config": flatten(cfg)}
            for name, cfg in getattr(bilanciamento, "WEEKEND_MOD_CONFIG", {}).items()
        ],
        "scaling": {
            "normal": {
                "hp": "HP base / 2",
                "other_stats": f"stat × (1 + piano/{normal_div})",
                "divisor": normal_div,
            },
            "boss": {
                "all_stats": f"stat × (1 + piano/{boss_div})",
                "divisor": boss_div,
                "incantation": "1 incantamento casuale da INCANTESIMI_CONFIG",
                "first_turn": "Il boss attacca per primo",
            },
        },
    }


def assault_data():
    structures = list(getattr(liste, "order", [])) or list(getattr(liste, "strutture", []))
    out = []
    rendered_sets = {
        name: render_template(
            FRASI_SET_TECNICHE.get(name, ""),
            bilanciamento.PROC_CLASSI.get(name, {}),
            getattr(liste, "bonus", {}).get(name, {}),
        )
        for name in getattr(liste, "classi", {})
    }
    for structure in structures:
        modes = []
        for mode in getattr(liste, "spec", {}).get(structure, []):
            modes.append({"name": mode, "description": getattr(liste, "frasispec", {}).get(mode, "")})
        refs = []
        tokens = {structure.lower(), structure.lower().split()[0]}
        for set_name, phrase in rendered_sets.items():
            paths = []
            for token in tokens:
                if len(token) >= 4:
                    paths.extend(refs_for_text(bilanciamento.PROC_CLASSI.get(set_name, {}), token))
            if any(token in phrase.lower() for token in tokens if len(token) >= 4):
                paths.append("frase tecnica")
            if paths:
                refs.append({"set": set_name, "refs": sorted(set(paths))})
        out.append(
            {
                "name": structure,
                "hp_pool": n(getattr(liste, "hps", {}).get(structure)),
                "stats": stat_dict(getattr(liste, "starmi", {}).get(structure, {})),
                "raw_stats": getattr(liste, "starmi", {}).get(structure, {}),
                "modes": modes,
                "set_refs": sorted(refs, key=lambda x: x["set"].lower()),
                "source": "liste.order/spec/frasispec/hps/starmi + bilanciamento.PROC_CLASSI + turno_assalto.py",
            }
        )
    return out


def extra_reference():
    return {
        "approaches": [
            {"name": name, "stats": stat_dict(cfg), "raw": cfg}
            for name, cfg in getattr(liste, "Approcci", {}).items()
        ],
        "nuclei": [
            {"name": name, "config": flatten(cfg)}
            for name, cfg in getattr(bilanciamento, "NUCLEI_CONFIG", {}).items()
        ],
        "effects": [
            {"name": name, "config": flatten(cfg)}
            for name, cfg in getattr(bilanciamento, "EFFETTI_CONFIG", {}).items()
        ],
        "fish_all": list(getattr(liste, "pesci", [])),
        "sea_enemies": getattr(liste, "Nautici", {}),
        "shop": getattr(liste, "shop", {}),
    }


def build_data():
    source = runtime_source()
    bosses, boss_scale = boss_data(source)
    data = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "commit": git_sha(),
            "repository": "ElSalamino/NftChallengeBot",
            "boss_scale_divisor": boss_scale,
        },
        "bosses": bosses,
        "enemies": enemy_data(),
        "locations": location_data(),
        "equipment": equipment_data(),
        "sets": set_data(),
        "rings": ring_data(),
        "incantations": incant_data(),
        "dungeon": dungeon_data(source),
        "assault": assault_data(),
        "extra": extra_reference(),
    }
    data["meta"]["counts"] = {
        "bosses": len(data["bosses"]),
        "enemies": len(data["enemies"]),
        "locations": len(data["locations"]),
        "equipment": len(data["equipment"]),
        "sets": len(data["sets"]),
        "rings": len(data["rings"]),
        "incantations": len(data["incantations"]),
        "rooms": len(data["dungeon"]["rooms"]),
        "structures": len(data["assault"]),
    }
    return data


HTML = r'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark light">
<title>NftChallengeBot — Wiki procedurale</title>
<style>
:root{--bg:#0b0d12;--panel:#131722;--panel2:#1a2030;--text:#eef2ff;--muted:#aeb7ca;--line:#293249;--accent:#78a8ff;--ok:#79d69a;--warn:#ffcf70;--bad:#ff8585;--shadow:0 12px 30px #0005}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif}button,input{font:inherit}.shell{display:grid;grid-template-columns:260px minmax(0,1fr);min-height:100vh}.side{position:sticky;top:0;height:100vh;padding:24px 16px;border-right:1px solid var(--line);background:#0e1119;overflow:auto}.brand{font-size:20px;font-weight:800}.sub{color:var(--muted);font-size:12px;margin:4px 0 18px}.nav button{display:block;width:100%;border:0;background:transparent;color:var(--muted);padding:9px 10px;text-align:left;border-radius:8px;cursor:pointer}.nav button:hover,.nav button.active{background:var(--panel2);color:var(--text)}main{padding:28px;max-width:1600px;width:100%;margin:auto}.top{display:flex;gap:12px;align-items:center;position:sticky;top:0;z-index:3;padding:8px 0 18px;background:linear-gradient(var(--bg) 70%,transparent)}#search{width:min(700px,100%);background:var(--panel);border:1px solid var(--line);color:var(--text);padding:11px 14px;border-radius:10px}.badge{display:inline-block;padding:2px 8px;border-radius:999px;background:var(--panel2);border:1px solid var(--line);color:var(--muted);font-size:12px}.section{display:none}.section.active{display:block}.hero{padding:26px;border:1px solid var(--line);background:linear-gradient(135deg,#151c2a,#11151f);border-radius:16px;box-shadow:var(--shadow);margin-bottom:22px}.hero h1{margin:0 0 8px;font-size:30px}.muted{color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:14px}.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px;overflow:hidden}.card h3{margin:0 0 8px;font-size:17px}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:10px 0}.stat{background:var(--panel2);border-radius:8px;padding:7px;text-align:center}.stat b{display:block;font-size:16px}.kv{width:100%;border-collapse:collapse;margin:8px 0}.kv td,.kv th{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}.kv th{color:var(--muted);font-weight:600}.effect{border-left:3px solid var(--accent);padding:8px 10px;background:#111827;border-radius:5px;margin:8px 0;white-space:pre-wrap}.source{font:11px/1.4 ui-monospace,SFMono-Regular,Consolas,monospace;color:#8490a8;margin-top:10px}.chips{display:flex;flex-wrap:wrap;gap:5px;margin:6px 0}.chip{font-size:12px;padding:3px 7px;border:1px solid var(--line);border-radius:999px;background:var(--panel2)}details{margin:8px 0}summary{cursor:pointer;color:var(--accent)}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#0d1119;border:1px solid var(--line);padding:10px;border-radius:8px;color:#cdd6e8;font-size:12px}.prob{color:var(--ok);font-variant-numeric:tabular-nums}.warn{color:var(--warn)}.counts{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px}.count{padding:14px;border-radius:10px;background:var(--panel);border:1px solid var(--line)}.count b{display:block;font-size:22px}.hidden{display:none!important}.empty{color:var(--muted);padding:20px;border:1px dashed var(--line);border-radius:10px}.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media(max-width:800px){.shell{display:block}.side{position:relative;height:auto;border-right:0;border-bottom:1px solid var(--line)}.nav{display:flex;overflow:auto;gap:5px}.nav button{width:auto;white-space:nowrap}main{padding:18px}.two{grid-template-columns:1fr}.stats{grid-template-columns:repeat(2,1fr)}}
</style>
</head>
<body>
<div class="shell">
<aside class="side">
<div class="brand">NftChallengeBot</div><div class="sub">Wiki procedurale · generata dal codice</div>
<div class="nav" id="nav"></div>
</aside>
<main>
<div class="top"><input id="search" placeholder="Cerca boss, nemico, set, oggetto, stanza, location…"><span class="badge" id="commit"></span></div>
<div id="app"></div>
</main>
</div>
<script id="wiki-data" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('wiki-data').textContent);
const $=s=>document.querySelector(s);const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const stats=s=>`<div class="stats">${['hp','atk','def','agi'].map(k=>`<div class="stat"><span>${k.toUpperCase()}</span><b>${esc(s?.[k]??0)}</b></div>`).join('')}</div>`;
const chips=a=>a&&a.length?`<div class="chips">${a.map(x=>`<span class="chip">${esc(x)}</span>`).join('')}</div>`:'<span class="muted">—</span>';
const config=rows=>rows&&rows.length?`<details><summary>Variabili tecniche (${rows.length})</summary><table class="kv"><tbody>${rows.map(r=>`<tr><th>${esc(r.path)}</th><td>${esc(Array.isArray(r.value)?r.value.join(', '):JSON.stringify(r.value)??r.value)}</td></tr>`).join('')}</tbody></table></details>`:'';
const src=s=>`<div class="source">Fonte: ${esc(s)}</div>`;
const weighted=rows=>rows&&rows.length?`<table class="kv"><thead><tr><th>Voce</th><th>Peso</th><th>Prob.</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${esc(r.name)}</td><td>${r.weight}</td><td class="prob">${r.pct}%</td></tr>`).join('')}</tbody></table>`:'<span class="muted">Pool vuoto</span>';
const section=(id,title,subtitle,body)=>`<section class="section" id="${id}"><div class="hero"><h1>${title}</h1><div class="muted">${subtitle}</div></div>${body}</section>`;
const card=(title,body,search='')=>`<article class="card searchable" data-search="${esc((title+' '+search).toLowerCase())}"><h3>${esc(title)}</h3>${body}</article>`;

const counts=Object.entries(D.meta.counts).map(([k,v])=>`<div class="count"><b>${v}</b><span>${esc(k)}</span></div>`).join('');
let pages=[];
pages.push(['home','Panoramica',section('home','Wiki procedurale','Ogni pagina è ricostruita dai dati del commit pubblicato. Nessuna tabella di bilanciamento è mantenuta a mano.',`<div class="counts">${counts}</div><div class="card" style="margin-top:14px"><h3>Come leggere questa wiki</h3><p>Le percentuali dei pool sono calcolate contando le ripetizioni reali nelle liste. Le frasi tecniche vengono renderizzate usando le variabili di <code>bilanciamento.py</code>. Le statistiche degli equipaggiamenti mostrano ogni chiave LV realmente presente nel database.</p><p class="muted">Generata ${esc(D.meta.generated_at)} · commit ${esc(D.meta.commit)}</p></div>`)]);

pages.push(['bosses','Boss',section('bosses','Boss giornalieri','Statistiche base, scaling per livello, set, gadget e drop pesati.',`<div class="grid">${D.bosses.map(b=>card(b.name,`${stats(b.stats)}<div><b>Set:</b> ${esc(b.set||'—')} · <b>Anello:</b> ${esc(b.ring||'—')} · <b>Approccio:</b> ${esc(b.approach||'—')}</div>${b.set_effect?`<div class="effect"><b>${esc(b.set)}</b> — ${esc(b.set_effect)}</div>`:''}${b.ring_effect?`<div class="effect"><b>${esc(b.ring)}</b> — ${esc(b.ring_effect)}</div>`:''}<details><summary>Statistiche a ogni livello 0–50</summary><div class="muted">Runtime: stat × (1 + livello/${b.scale_divisor})</div><table class="kv"><thead><tr><th>LV</th><th>HP</th><th>ATK</th><th>DEF</th><th>AGI</th></tr></thead><tbody>${b.levels.map(x=>`<tr><td>${x.level}</td><td>${x.stats.hp}</td><td>${x.stats.atk}</td><td>${x.stats.def}</td><td>${x.stats.agi}</td></tr>`).join('')}</tbody></table></details><details open><summary>Drop</summary><table class="kv"><thead><tr><th>Oggetto</th><th>Peso</th><th>Prob.</th><th>Perché è nel pool</th></tr></thead><tbody>${b.drops.map(d=>`<tr><td>${esc(d.name)}</td><td>${d.weight}</td><td class="prob">${d.pct}%</td><td>${esc(d.reason)}</td></tr>`).join('')}</tbody></table></details>${src(b.source)}`,`${b.set} ${b.ring} ${b.drops.map(x=>x.name).join(' ')}`)).join('')}</div>`)]);

pages.push(['enemies','Nemici',section('enemies','Nemici dungeon','Roster completo, statistiche, set/anello e dove possono comparire.',`<div class="grid">${D.enemies.map(e=>card(e.name,`${stats(e.stats)}<div><b>Set:</b> ${esc(e.set||'—')} · <b>Anello:</b> ${esc(e.ring||'—')} · <b>Approccio:</b> ${esc(e.approach||'—')}</div>${e.set_effect?`<div class="effect">${esc(e.set_effect)}</div>`:''}${e.ring_effect?`<div class="effect">${esc(e.ring_effect)}</div>`:''}<details open><summary>Dove si trova</summary>${Object.keys(e.locations).length?`<table class="kv"><tbody>${Object.entries(e.locations).map(([l,w])=>`<tr><td>${esc(l)}</td><td>peso ${w.weight}</td><td class="prob">${w.pct}% nel pool locale</td></tr>`).join('')}</tbody></table>`:'<span class="muted">Non assegnato a una casa_nemici locale; può comunque essere estratto da pool globali che usano nemici.</span>'}</details>${src(e.source)}`,`${e.set} ${e.ring} ${Object.keys(e.locations).join(' ')}`)).join('')}</div>`)]);

pages.push(['locations','Location',section('locations','Location','Percorsi, pesca, nemici locali e pool loot con pesi reali.',`<div class="grid">${D.locations.map(l=>card(`${l.emoji||''} ${l.name}`,`<b>Collegamenti:</b> ${chips(l.routes)}<details open><summary>Nemici locali</summary>${weighted(l.enemies)}</details><details><summary>Pool loot</summary>${weighted(l.loot)}</details><details><summary>Pesci</summary>${chips(l.fish)}</details>${src(l.source)}`,`${l.routes.join(' ')} ${l.fish.join(' ')} ${l.enemies.map(x=>x.name).join(' ')} ${l.loot.map(x=>x.name).join(' ')}`)).join('')}</div>`)]);

pages.push(['equipment','Equipaggiamento',section('equipment','Oggetti ed equipaggiamento','Armi e protezioni raggruppate per oggetto; ogni livello presente nel database mostra le sue statistiche reali.',`<div class="grid">${D.equipment.map(i=>card(i.name,`<span class="badge">${esc(i.kind)}</span>${i.sets.length?`<div style="margin-top:8px"><b>Usato nei set:</b>${chips(i.sets)}</div>`:''}<table class="kv"><thead><tr><th>Livello</th><th>HP</th><th>ATK</th><th>DEF</th><th>AGI</th></tr></thead><tbody>${i.levels.map(l=>`<tr><td>${esc(l.label)}</td><td>${esc(l.stats.hp)}</td><td>${esc(l.stats.atk)}</td><td>${esc(l.stats.def)}</td><td>${esc(l.stats.agi)}</td></tr>`).join('')}</tbody></table>${src('liste.armi/armiextra/protezioni/protezioniextra; equiA/equiP1 usano questi valori direttamente')}`,`${i.kind} ${i.sets.join(' ')} ${i.levels.map(x=>x.full_name).join(' ')}`)).join('')}</div>`)]);

pages.push(['sets','Set',section('sets','Set','Composizione, approcci, bonus grezzi, frase tecnica renderizzata e tutte le variabili del set.',`<div class="grid">${D.sets.map(s=>card(s.name,`<b>Come si compone</b>${chips(s.components)}<b>Approcci</b>${chips(s.approaches)}${Object.values(s.bonus).some(Number)?stats(s.bonus):''}${s.effect?`<div class="effect">${esc(s.effect)}</div>`:'<div class="muted">Nessuna frase tecnica dedicata.</div>'}${config(s.config)}${src(s.source)}`,`${s.components.join(' ')} ${s.approaches.join(' ')} ${s.effect}`)).join('')}</div>`)]);

pages.push(['rings','Anelli',section('rings','Anelli / gadget','Effetti tecnici renderizzati da PROC_ANELLI, più la descrizione inventario.',`<div class="grid">${D.rings.map(r=>card(r.name,`${r.effect?`<div class="effect">${esc(r.effect)}</div>`:''}${r.description?`<p>${esc(r.description)}</p>`:''}${config(r.config)}${src(r.source)}`,`${r.effect} ${r.description}`)).join('')}</div>`)]);

pages.push(['incants','Incantesimi',section('incants','Incantesimi','Libri che li forniscono, effetto tecnico e configurazione completa.',`<div class="grid">${D.incantations.map(i=>card(i.name,`<b>Libri:</b>${chips(i.books)}${i.effect?`<div class="effect">${esc(i.effect)}</div>`:''}${config(i.config)}${src(i.source)}`,`${i.books.join(' ')} ${i.effect}`)).join('')}</div>`)]);

const dg=D.dungeon;
pages.push(['dungeon','Dungeon',section('dungeon','Dungeon e stanze',`Generazione, scaling, ricompense e tutte le stanze. Boss dungeon: ${esc(dg.scaling.boss.all_stats)}; nemici normali: ${esc(dg.scaling.normal.other_stats)}.`,`<div class="two"><div class="card"><h3>Nemico normale</h3><p>${esc(dg.scaling.normal.hp)}; ${esc(dg.scaling.normal.other_stats)}.</p></div><div class="card"><h3>Boss dungeon</h3><p>${esc(dg.scaling.boss.all_stats)}. ${esc(dg.scaling.boss.first_turn)}. ${esc(dg.scaling.boss.incantation)}.</p></div></div><div class="grid" style="margin-top:14px">${dg.rooms.map(r=>card(r.name,`<div>Peso stanza: <b>${r.weight}</b> <span class="prob">(${r.pct}%)</span></div><b>Azioni rilevate:</b>${chips(r.actions)}${config(r.config)}${src(r.source)}`,`${r.actions.join(' ')} ${r.config.map(x=>x.path+' '+x.value).join(' ')}`)).join('')}</div><h2>Configurazione globale</h2><div class="grid">${Object.entries(dg.global).map(([name,rows])=>card(name,config(rows),rows.map(x=>x.path+' '+x.value).join(' '))).join('')}</div><h2>Modificatori weekend</h2><div class="grid">${dg.weekend.map(w=>card(w.name,config(w.config),w.config.map(x=>x.path+' '+x.value).join(' '))).join('')}</div>`)]);

pages.push(['assault','Assalto',section('assault','Assalto e villaggi','Statistiche e scopo degli edifici, modalità e set che li citano/hard-counterano.',`<div class="grid">${D.assault.map(a=>card(a.name,`${a.hp_pool!=null?`<div><b>HP struttura:</b> ${esc(a.hp_pool)}</div>`:''}${stats(a.stats)}<b>Modalità</b>${a.modes.length?`<table class="kv"><tbody>${a.modes.map(m=>`<tr><th>${esc(m.name)}</th><td>${esc(m.description)}</td></tr>`).join('')}</tbody></table>`:'<span class="muted">—</span>'}${a.set_refs.length?`<details><summary>Set collegati / counter (${a.set_refs.length})</summary><table class="kv"><tbody>${a.set_refs.map(x=>`<tr><th>${esc(x.set)}</th><td>${esc(x.refs.join(', '))}</td></tr>`).join('')}</tbody></table></details>`:''}${src(a.source)}`,`${a.modes.map(x=>x.name+' '+x.description).join(' ')} ${a.set_refs.map(x=>x.set).join(' ')}`)).join('')}</div>`)]);

pages.push(['reference','Extra',section('reference','Riferimenti extra','Approcci, nuclei, effetti temporanei, pesca globale e shop: dati centralizzati utili alle altre modalità.',`<h2>Approcci</h2><div class="grid">${D.extra.approaches.map(a=>card(a.name,stats(a.stats),JSON.stringify(a.raw))).join('')}</div><h2>Nuclei</h2><div class="grid">${D.extra.nuclei.map(x=>card(x.name,config(x.config),JSON.stringify(x.config))).join('')}</div><h2>Effetti temporanei</h2><div class="grid">${D.extra.effects.map(x=>card(x.name,config(x.config),JSON.stringify(x.config))).join('')}</div><div class="two" style="margin-top:14px"><div class="card"><h3>Pesci globali</h3>${chips(D.extra.fish_all)}</div><div class="card"><h3>Shop</h3><table class="kv"><tbody>${Object.entries(D.extra.shop||{}).map(([k,v])=>`<tr><th>${esc(k)}</th><td>${esc(v)}</td></tr>`).join('')}</tbody></table></div></div>`)]);

$('#nav').innerHTML=pages.map(([id,label],i)=>`<button data-page="${id}" class="${i===0?'active':''}">${esc(label)}</button>`).join('');
$('#app').innerHTML=pages.map(x=>x[2]).join('');$('#home').classList.add('active');$('#commit').textContent=(D.meta.commit||'').slice(0,8);
function show(id){document.querySelectorAll('.section').forEach(x=>x.classList.toggle('active',x.id===id));document.querySelectorAll('.nav button').forEach(x=>x.classList.toggle('active',x.dataset.page===id));$('#search').value='';filter('');scrollTo({top:0,behavior:'instant'});location.hash=id==='home'?'':id}
document.querySelectorAll('.nav button').forEach(b=>b.onclick=()=>show(b.dataset.page));
function filter(q){q=q.trim().toLowerCase();document.querySelectorAll('.section.active .searchable').forEach(c=>c.classList.toggle('hidden',!!q&&!c.dataset.search.includes(q)))}$('#search').addEventListener('input',e=>filter(e.target.value));
const initial=location.hash.slice(1);if(initial&&pages.some(x=>x[0]===initial))show(initial);
</script>
</body></html>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="_site")
    args = parser.parse_args()
    output = (ROOT / args.output).resolve() if not Path(args.output).is_absolute() else Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    data = build_data()
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (output / "index.html").write_text(HTML.replace("__DATA__", payload), encoding="utf-8")
    (output / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / ".nojekyll").write_text("", encoding="utf-8")
    print("Wiki generata:", output)
    print(json.dumps(data["meta"]["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

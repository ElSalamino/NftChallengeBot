#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controlli di integrità sui collegamenti della wiki procedurale."""
import re
from collections import Counter
import run_wiki

wiki = run_wiki.wiki
data = wiki.build_data()

items = {x["name"] for x in data["items"]}
sets = {x["name"] for x in data["sets"]}
rings = {x["name"] for x in data["rings"]}
enemies = {x["name"] for x in data["enemies"]}
locations = {x["name"] for x in data["locations"]}

errors = []
for s in data["sets"]:
    for item in s["components"]:
        if item not in items:
            errors.append(f"set {s['name']} -> item mancante {item}")

for b in data["bosses"]:
    if b.get("set") and b["set"] not in sets:
        errors.append(f"boss {b['name']} -> set mancante {b['set']}")
    if b.get("ring") and b["ring"] not in rings:
        errors.append(f"boss {b['name']} -> anello mancante {b['ring']}")
    for drop in b["drops"]:
        if drop["item"] not in items:
            errors.append(f"boss {b['name']} -> drop mancante {drop['item']}")

for e in data["enemies"]:
    if e.get("set") and e["set"] not in sets:
        errors.append(f"nemico {e['name']} -> set mancante {e['set']}")
    if e.get("ring") and e["ring"] not in rings:
        errors.append(f"nemico {e['name']} -> anello mancante {e['ring']}")
    for loc in e["locations"]:
        if loc not in locations:
            errors.append(f"nemico {e['name']} -> location mancante {loc}")

for loc in data["locations"]:
    for route in loc["routes"]:
        if route not in locations:
            errors.append(f"location {loc['name']} -> collegamento mancante {route}")
    for drop in loc["loot"]:
        if drop["item"] not in items:
            errors.append(f"location {loc['name']} -> loot mancante {drop['item']}")
    for fish in loc["fish"]:
        if fish not in items:
            errors.append(f"location {loc['name']} -> pesce mancante {fish}")
    for enemy in loc["enemies"]:
        if enemy["name"] not in enemies:
            errors.append(f"location {loc['name']} -> nemico mancante {enemy['name']}")

for structure in data["assault"]:
    if not structure["modes"]:
        errors.append(f"struttura {structure['name']} senza modalità")
    for mode in structure["modes"]:
        if len(mode["levels"]) != 51:
            errors.append(f"struttura {structure['name']} / {mode['name']} livelli={len(mode['levels'])}")

if errors:
    print("ERRORI WIKI:")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

print("Integrità wiki OK")
print(f"{len(items)} oggetti, {len(sets)} set, {len(data['bosses'])} boss, {len(enemies)} nemici, {len(locations)} location")

# PROBE TEMPORANEO: verrà rimosso prima del merge.
src = (wiki.ROOT / "nft.py").read_text(encoding="utf-8")
for fn in ("equiA", "unequiA", "equiP1", "unequiP1"):
    m = re.search(rf"def {fn}\(.*?(?=\ndef |\nasync def |\Z)", src, re.S)
    print(f"\n--- {fn} ---\n{m.group(0)[:5000] if m else 'NON TROVATA'}")
print("\n--- TAVOLO ---")
for coll in ("armi", "armiextra", "protezioni", "protezioniextra"):
    d = getattr(wiki.liste, coll, {})
    print(coll, {k:v for k,v in d.items() if str(k).startswith("Un tavolo speziato")})
print("\n--- APPROCCI ---")
print(getattr(wiki.liste, "Approcci", {}))
print("\n--- NUCLEI ---")
print(getattr(wiki.bilanciamento, "NUCLEI_CONFIG", {}))
print("\n--- WEEKEND ---")
print(getattr(wiki.bilanciamento, "WEEKEND_MOD_CONFIG", {}))
print("POOL", getattr(wiki.bilanciamento, "WEEKEND_MOD_POOL", []))
print("\n--- EVENTI ---")
print(getattr(wiki.liste, "eventi", {}))
print("\n--- SCAGLIONI NEI POOL LOCATION ---")
for loc, pool in getattr(wiki.liste, "pool", {}).items():
    normalized = [wiki.base_item(x) for x in pool]
    c = Counter(normalized)
    if c.get("Scaglioni pesanti"):
        print(loc, c["Scaglioni pesanti"], "/", len(normalized), "=", round(c["Scaglioni pesanti"]*100/len(normalized), 4), "%")
print("\n--- SCAGLIONI ALTRE FONTI ---")
for boss, pool in getattr(wiki.liste, "premi_boss", {}).items():
    c = Counter(wiki.base_item(x) for x in pool)
    if c.get("Scaglioni pesanti"):
        print("boss", boss, c["Scaglioni pesanti"], "/", len(pool), round(c["Scaglioni pesanti"]*100/len(pool), 4), "%")
for arena_name, pool in getattr(wiki.liste, "arenamod", {}).items():
    c = Counter(wiki.base_item(x) for x in pool)
    if c.get("Scaglioni pesanti"):
        print("arena", arena_name, c["Scaglioni pesanti"], "/", len(pool), round(c["Scaglioni pesanti"]*100/len(pool), 4), "%")
print("\n--- BLOCCO LVX/LVMAX ---")
pos = src.find('if "LVX" in x')
if pos < 0: pos = src.find("if 'LVX' in x")
print(src[max(0,pos-3500):pos+5000] if pos >= 0 else "NON TROVATO")

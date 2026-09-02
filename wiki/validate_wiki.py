#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit finale di integrità della wiki procedurale v3."""
import math
import run_wiki

wiki = run_wiki.wiki
data = wiki.build_data()

items = {x["name"] for x in data["items"]}
sets = {x["name"] for x in data["sets"]}
rings = {x["name"] for x in data["rings"]}
enemies = {x["name"] for x in data["enemies"]}
locations = {x["name"] for x in data["locations"]}
approaches = {x["name"] for x in data["approaches"]}
nuclei = {x["name"] for x in data["nuclei"]}
rooms = {x["name"] for x in data["dungeon"]["rooms"]}
events = {x["name"] for x in data["events"]}

errors = []

# Collegamenti set -> oggetti / approcci e pulizia descrizioni tecniche.
for s in data["sets"]:
    for item in s["components"]:
        if item not in items:
            errors.append(f"set {s['name']} -> item mancante {item}")
    for approach in s.get("approaches", []):
        if approach not in approaches:
            errors.append(f"set {s['name']} -> approccio mancante {approach}")
    if "PARAMETRI COMPLETI" in (s.get("technical") or "").upper():
        errors.append(f"set {s['name']} mostra ancora PARAMETRI COMPLETI")

# Boss / nemici.
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
    if e.get("approach") and e["approach"] not in approaches:
        errors.append(f"nemico {e['name']} -> approccio mancante {e['approach']}")
    for loc in e["locations"]:
        if loc not in locations:
            errors.append(f"nemico {e['name']} -> location mancante {loc}")

# Location e Hub.
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

hub = next((x for x in data["locations"] if x["name"] == "Hub"), None)
if not hub:
    errors.append("Hub mancante")
else:
    expected = locations - {"Hub"}
    if set(hub["routes"]) != expected:
        errors.append(f"Hub non collegato a tutte le location: {len(hub['routes'])}/{len(expected)}")

# Equipaggiamenti: esattamente la progressione generata dal runtime.
expected_levels = [f"LV{x}" for x in range(10)] + ["LVX", "LVMAX"]
for item in data["items"]:
    if not item.get("icon"):
        errors.append(f"item {item['name']} senza emoji fallback")
    levels = item.get("levels", [])
    if levels:
        labels = [x["label"] for x in levels]
        if labels != expected_levels:
            errors.append(f"item {item['name']} livelli errati: {labels}")
        if not item.get("forging"):
            errors.append(f"item {item['name']} senza guida LVX/LVMAX")
        # LVX = 200% base e LVMAX = 250% base, con lo stesso round del runtime.
        base = levels[0]["stats"]
        lvx = levels[-2]["stats"]
        lvmax = levels[-1]["stats"]
        for stat, value in base.items():
            if lvx[stat] != round(value * 2):
                errors.append(f"item {item['name']} LVX {stat} incoerente")
            if lvmax[stat] != round(value * 2.5):
                errors.append(f"item {item['name']} LVMAX {stat} incoerente")
    for set_name in item.get("sets", []):
        if set_name not in sets:
            errors.append(f"item {item['name']} -> set mancante {set_name}")
    for event_name in item.get("events", []):
        if event_name not in events:
            errors.append(f"item {item['name']} -> evento mancante {event_name}")
    if item.get("nucleus") and item["nucleus"] not in nuclei:
        errors.append(f"item {item['name']} -> nucleo mancante {item['nucleus']}")

# Approcci: i moltiplicatori devono essere completi e i set backlink validi.
for a in data["approaches"]:
    for stat in ("hp", "atk", "def", "agi"):
        if stat not in a["multipliers"]:
            errors.append(f"approccio {a['name']} senza moltiplicatore {stat}")
    for set_name in a.get("sets", []):
        if set_name not in sets:
            errors.append(f"approccio {a['name']} -> set mancante {set_name}")

# Nuclei e descrizioni estese.
configured_nuclei = set(getattr(wiki.bilanciamento, "NUCLEI_CONFIG", {}))
if not configured_nuclei.issubset(nuclei):
    errors.append(f"nuclei configurati non esposti: {sorted(configured_nuclei - nuclei)}")
for n in data["nuclei"]:
    if not (n.get("mechanic") or "").strip():
        errors.append(f"nucleo {n['name']} senza descrizione meccanica")

# Eventi / weekend.
for event in data["events"]:
    for item in event["items"]:
        if item not in items:
            errors.append(f"evento {event['name']} -> item mancante {item}")
weekend = data["weekend"]
weight_sum = weekend["none_weight"] + sum(x["weight"] for x in weekend["mods"])
if weight_sum != weekend["pool_size"]:
    errors.append(f"pool weekend incoerente: {weight_sum}/{weekend['pool_size']}")

# Scaglioni LVMAX: tutti e quattro, cliccabili e con chance reale positiva.
expected_scaglioni = {"Uno scaglione blu", "Uno scaglione verde", "Uno scaglione giallo", "Uno scaglione nero"}
seen_scaglioni = {x["name"] for x in data["scaglioni"]}
if seen_scaglioni != expected_scaglioni:
    errors.append(f"scaglioni LVMAX errati: {sorted(seen_scaglioni)}")
for s in data["scaglioni"]:
    if s["name"] not in items:
        errors.append(f"scaglione {s['name']} non presente negli item")
    if s["room"] not in rooms:
        errors.append(f"scaglione {s['name']} -> stanza mancante {s['room']}")
    if not (0 < float(s["chance_pct"]) <= 100):
        errors.append(f"scaglione {s['name']} chance non valida {s['chance_pct']}")

# Assalto: tutte le modalità devono avere LV0-50.
for structure in data["assault"]:
    if not structure["modes"]:
        errors.append(f"struttura {structure['name']} senza modalità")
    for mode in structure["modes"]:
        if len(mode["levels"]) != 51:
            errors.append(f"struttura {structure['name']} / {mode['name']} livelli={len(mode['levels'])}")

if errors:
    print("ERRORI WIKI V3:")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

print("Integrità wiki v3 OK")
print(
    f"{len(items)} oggetti, {len(sets)} set, {len(data['bosses'])} boss, "
    f"{len(enemies)} nemici, {len(locations)} location, {len(approaches)} approcci, "
    f"{len(nuclei)} nuclei, {len(events)} eventi"
)

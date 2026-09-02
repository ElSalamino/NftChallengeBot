#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Estensioni della wiki procedurale v2.

La v3 mantiene il renderer esistente ma corregge/aggiunge:
- progressione equipaggiamenti LV0..LV9, LVX, LVMAX come nel runtime;
- fallback emoji per tipologia oggetto;
- Hub con collegamenti globali;
- pagina Approcci;
- pagina Nuclei con descrizioni estese;
- area Weekend / Eventi / Modificatori;
- provenienza degli scaglioni necessari al passaggio LVX -> LVMAX;
- descrizioni set pulite dai dettagli macchina usati solo dall'audit.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import genera_wiki_v2 as v2

ROOT = v2.ROOT
liste = v2.liste
bilanciamento = v2.bilanciamento
STATS = v2.STATS
FRASI_SET_TECNICHE = v2.FRASI_SET_TECNICHE

ITEM_LEVELS = [(f"LV{x}", x) for x in range(10)] + [("LVX", 10), ("LVMAX", 15)]
SCAGLIONI = (
    ("Uno scaglione blu", "Locanda spettrale", "Svegliati"),
    ("Uno scaglione verde", "Parco", "Parlaci"),
    ("Uno scaglione giallo", "Cunicolo", "evento"),
    ("Uno scaglione nero", "Sabbie mobili", "evento"),
)


def _valid_set_names():
    names = (
        set(getattr(liste, "classi", {}))
        | set(getattr(liste, "bonus", {}))
        | set(getattr(bilanciamento, "PROC_CLASSI", {}))
        | set(FRASI_SET_TECNICHE)
    )
    return sorted((x for x in names if isinstance(x, str) and x.strip()), key=str.lower)


def _clean_set_technical(text):
    text = str(text or "").strip()
    text = re.split(r"\s*PARAMETRI\s+COMPLETI\s*(?:—|--|:)?\s*", text, maxsplit=1, flags=re.I)[0]
    return text.strip()


def set_data():
    classi = getattr(liste, "classi", {})
    bonus_all = getattr(liste, "bonus", {})
    human_all = getattr(liste, "frasi_set", {})
    approaches_all = getattr(liste, "Approccini", {})
    score_all = getattr(liste, "bonus_punteggio", {})
    original_score_all = getattr(liste, "bonus_punteggio_originale", {})
    rows = []
    for name in _valid_set_names():
        cfg = bilanciamento.PROC_CLASSI.get(name, {})
        bonus = bonus_all.get(name, {})
        rows.append({
            "name": name,
            "components": [v2.base_item(x) for x in classi.get(name, [])],
            "approaches": list(approaches_all.get(name, [])),
            "bonus": v2.stat_dict(bonus),
            "raw_score": int(score_all.get(name, 0)),
            "raw_score_original": int(original_score_all.get(name, 0)),
            "human": v2.clean_human(human_all.get(name, "")),
            "technical": _clean_set_technical(v2.render_template(FRASI_SET_TECNICHE.get(name, ""), cfg, bonus)),
        })
    return rows


def _runtime_stat(value, level_value):
    try:
        base = int(value)
    except Exception:
        try:
            base = int(float(value))
        except Exception:
            base = 0
    return round(base + base * level_value / 10)


def _generated_levels(values):
    return [
        {
            "label": label,
            "level_value": level,
            "stats": {stat: _runtime_stat((values or {}).get(stat, 0), level) for stat in STATS},
        }
        for label, level in ITEM_LEVELS
    ]


def equipment_map():
    grouped = {}
    for kind, collection in [
        ("Arma", getattr(liste, "armi", {})),
        ("Arma", getattr(liste, "armiextra", {})),
        ("Protezione", getattr(liste, "protezioni", {})),
        ("Protezione", getattr(liste, "protezioniextra", {})),
    ]:
        for full, values in collection.items():
            name = v2.base_item(full)
            row = grouped.setdefault(name, {"name": name, "types": set(), "base_values": values})
            row["types"].add(kind)
            row["base_values"] = values
    for row in grouped.values():
        row["types"] = sorted(row["types"])
        row["levels"] = _generated_levels(row["base_values"])
    return grouped


def item_icon(types):
    values = set(types or [])
    if "Nucleo" in values: return "⚛️"
    if "Anello" in values: return "💍"
    if "Libro" in values: return "📖"
    if "Protezione" in values: return "🛡️"
    if "Arma" in values: return "⚔️"
    if "Pesce" in values: return "🐟"
    if "Usabile" in values: return "🧪"
    if "Decorativo / lore" in values: return "🏺"
    if "Shop" in values: return "🛒"
    return "🎒"


def _scaglione_source_rows():
    rooms_cfg = getattr(bilanciamento, "DUNGEON_CONFIG", {}).get("stanze", {})
    room_pool = v2.weighted(getattr(liste, "stanze", []))
    room_weight = {x["name"]: x for x in room_pool}
    rows = []
    for name, room, action in SCAGLIONI:
        cfg = rooms_cfg.get(room, {}).get(action, {})
        if name.endswith("blu"):
            chance = min(cfg.get("scaglione_soglia_pct", 0), cfg.get("conferma_soglia_pct", 100))
            condition = "Scegli Svegliati nella Locanda spettrale. I due controlli usano lo stesso tiro casuale."
        elif name.endswith("verde"):
            chance = cfg.get("scaglione_soglia_pct", 0)
            condition = "Scegli Parlaci nel Parco."
        elif name.endswith("giallo"):
            chance = min(cfg.get("scaglione_soglia_pct", 0), cfg.get("conferma_scaglione_soglia_pct", 100))
            condition = "Evento automatico del Cunicolo. I due controlli usano lo stesso tiro casuale."
        else:
            chance = min(
                cfg.get("caduta_pct", 100),
                cfg.get("salvataggio_pet_soglia_pct", 100),
                cfg.get("scaglione_soglia_pct", 0),
            )
            condition = f"Sabbie mobili: serve affetto del pet > {cfg.get('pat_min', 666)}; poi il tiro deve rientrare nella soglia dello scaglione."
        w = room_weight.get(room, {"weight": 0, "pct": 0})
        rows.append({
            "name": name,
            "room": room,
            "action": action,
            "chance_pct": chance,
            "condition": condition,
            "room_weight": w.get("weight", 0),
            "room_pool_pct": w.get("pct", 0),
        })
    return rows


def item_data(sets):
    equip = equipment_map()
    usage = defaultdict(set)
    for s in sets:
        for component in s["components"]:
            usage[component].add(s["name"])

    locations_by_item = defaultdict(list)
    for loc, pool in getattr(liste, "pool", {}).items():
        for row in v2.weighted(pool):
            locations_by_item[v2.base_item(row["name"])].append({"location": loc, **row})

    bosses_by_item = defaultdict(list)
    for boss, pool in getattr(liste, "premi_boss", {}).items():
        for row in v2.weighted(pool):
            bosses_by_item[v2.base_item(row["name"])].append({"boss": boss, **row})

    event_by_item = defaultdict(set)
    for item, event_name in getattr(liste, "eventi", {}).items():
        event_by_item[v2.base_item(item)].add(str(event_name))

    scaglione_sources = {x["name"]: x for x in _scaglione_source_rows()}
    nuclei_names = set(getattr(liste, "nuclei", [])) | set(getattr(bilanciamento, "NUCLEI_CONFIG", {}))

    names = set(equip)
    for s in sets: names.update(s["components"])
    for mapping_name in ("anelli", "libri", "usabili", "decoro", "shop"):
        value = getattr(liste, mapping_name, {})
        if isinstance(value, dict): names.update(v2.base_item(k) for k in value)
        elif isinstance(value, (list, tuple, set)): names.update(v2.base_item(k) for k in value)
    for pool in getattr(liste, "premi_boss", {}).values(): names.update(v2.base_item(x) for x in pool)
    for pool in getattr(liste, "pool", {}).values(): names.update(v2.base_item(x) for x in pool)
    for pool in getattr(liste, "pesciame", {}).values(): names.update(v2.base_item(x) for x in pool)
    names.update(v2.base_item(x) for x in getattr(liste, "pesci", []))
    names.update(v2.base_item(x) for x in getattr(liste, "eventi", {}))
    names.update(nuclei_names)
    names.update(scaglione_sources)

    anelli = v2.safe_mapping("anelli")
    libri = v2.safe_mapping("libri")
    usabili = v2.safe_mapping("usabili")
    decoro = v2.safe_mapping("decoro")
    shop = v2.safe_mapping("shop")
    fish = set(v2.base_item(x) for x in getattr(liste, "pesci", []))

    rows = []
    for name in sorted((x for x in names if isinstance(x, str) and x.strip()), key=str.lower):
        types = set(equip.get(name, {}).get("types", []))
        descriptions = []
        ring = None
        book_effect = None
        if name in anelli:
            types.add("Anello")
            descriptions.append(v2.clean_human(anelli.get(name)))
            ring = name
        if name in libri:
            types.add("Libro")
            info = libri[name]
            if isinstance(info, dict):
                book_effect = info.get("ef")
                if info.get("descrizione"): descriptions.append(v2.clean_human(info.get("descrizione")))
        if name in usabili:
            types.add("Usabile")
            if isinstance(usabili.get(name), str): descriptions.append(usabili.get(name))
        if name in decoro:
            types.add("Decorativo / lore")
            if isinstance(decoro.get(name), str): descriptions.append(decoro.get(name))
        if name in shop: types.add("Shop")
        if name in fish: types.add("Pesce")
        if name in nuclei_names: types.add("Nucleo")
        if not types: types.add("Oggetto")
        types = sorted(types)
        is_equipment = bool(equip.get(name))
        forging = None
        if is_equipment:
            forging = {
                "lvx": "Forgia 2 copie LV9 dello stesso oggetto con /forgia. Il costo normale è 90 Gloria e il risultato è 1 LVX. LVX vale il 200% delle statistiche base.",
                "lvmax": "Nel dungeon trova la stanza Fabbro e scegli Approcciala. Devi possedere tutti e quattro gli scaglioni del medaglione celeste e avere un LVX nello zaino: il Fabbro consuma 1 LVX e crea 1 LVMAX. I quattro scaglioni vengono controllati ma non consumati. LVMAX vale il 250% delle statistiche base.",
            }
        rows.append({
            "name": name,
            "types": types,
            "icon": item_icon(types),
            "levels": equip.get(name, {}).get("levels", []),
            "sets": sorted(usage.get(name, []), key=str.lower),
            "description": "\n".join(dict.fromkeys(x for x in descriptions if x)),
            "ring": ring,
            "book_effect": book_effect,
            "nucleus": name if name in nuclei_names else None,
            "events": sorted(event_by_item.get(name, []), key=str.lower),
            "scaglione_source": scaglione_sources.get(name),
            "forging": forging,
            "boss_drops": sorted(bosses_by_item.get(name, []), key=lambda x: x["boss"].lower()),
            "location_drops": sorted(locations_by_item.get(name, []), key=lambda x: x["location"].lower()),
        })
    return rows


def location_data():
    names = list(dict.fromkeys(getattr(liste, "location", [])))
    for source in (getattr(liste, "move", {}), getattr(liste, "casa_nemici", {}), getattr(liste, "pool", {}), getattr(liste, "pesciame", {})):
        for name in source:
            if name not in names: names.append(name)
    rows = []
    for loc in names:
        routes = list(getattr(liste, "move", {}).get(loc, []))
        if loc == "Hub":
            routes = [x for x in names if x != "Hub"]
        rows.append({
            "name": loc,
            "emoji": getattr(liste, "moji_posto", {}).get(loc, ""),
            "routes": routes,
            "loot": [{**x, "item": v2.base_item(x["name"])} for x in v2.weighted(getattr(liste, "pool", {}).get(loc, []))],
            "enemies": v2.weighted(getattr(liste, "casa_nemici", {}).get(loc, [])),
            "fish": [v2.base_item(x) for x in getattr(liste, "pesciame", {}).get(loc, [])],
        })
    return rows


def _approach_description(cfg):
    parts = []
    for stat in STATS:
        multiplier = float(cfg.get(stat, 1))
        delta = round((multiplier - 1) * 100)
        if delta:
            parts.append(f"{stat.upper()} {'+' if delta > 0 else ''}{delta}%")
    if not parts:
        return "Non modifica direttamente HP, ATK, DEF o AGI."
    return "Quando viene applicato, moltiplica e arrotonda le statistiche: " + ", ".join(parts) + "."


def approach_data(sets):
    set_by_approach = defaultdict(set)
    for s in sets:
        for approach in s.get("approaches", []):
            set_by_approach[approach].add(s["name"])
    rows = []
    for name, cfg in getattr(liste, "Approcci", {}).items():
        rows.append({
            "name": name,
            "multipliers": {stat: float(cfg.get(stat, 1)) for stat in STATS},
            "base_approach": cfg.get("Ap", "Base"),
            "description": _approach_description(cfg),
            "sets": sorted(set_by_approach.get(name, []), key=str.lower),
        })
    return sorted(rows, key=lambda x: x["name"].lower())


def nuclei_data():
    cfgs = getattr(bilanciamento, "NUCLEI_CONFIG", {})
    order = list(getattr(liste, "nuclei", []))
    for name in cfgs:
        if name not in order: order.append(name)
    decoro = v2.safe_mapping("decoro")
    rows = []
    for name in order:
        cfg = cfgs.get(name, {})
        assault = cfg.get("assalto", {})
        explanations = []
        per_member = assault.get("stat_per_membro", {})
        if per_member:
            bonus = ", ".join(f"+{value} {stat.upper()}" for stat, value in per_member.items())
            explanations.append(f"All'inizio dell'assalto conta tutti i membri del clan e assegna, per ogni membro, {bonus}. Il bonus dura per l'intero assalto.")
        if "cura_per_struttura" in assault:
            explanations.append(f"Durante l'assalto cura l'assaltatore di {assault['cura_per_struttura']} HP ogni volta che viene processata una struttura difensiva.")
        resurrect = assault.get("resurrezione")
        if resurrect:
            explanations.append(f"All'inizio dell'assalto ha il {resurrect.get('proc', 0)}% di attivare la non-morte del nucleo; se interviene, il valore di ritorno configurato è {resurrect.get('hp', 0)} HP.")
        rows.append({
            "name": name,
            "short": str(decoro.get(name, "")),
            "mechanic": " ".join(explanations) or "Nessun effetto d'assalto configurato.",
            "config": v2.flatten(cfg),
        })
    return rows


def events_data():
    grouped = defaultdict(set)
    for item, event_name in getattr(liste, "eventi", {}).items():
        grouped[str(event_name)].add(v2.base_item(item))
    return [{"name": name, "items": sorted(items, key=str.lower)} for name, items in sorted(grouped.items(), key=lambda x: x[0].lower())]


def weekend_data():
    cfgs = getattr(bilanciamento, "WEEKEND_MOD_CONFIG", {})
    pool = list(getattr(bilanciamento, "WEEKEND_MOD_POOL", []))
    counts = Counter(pool)
    total = len(pool)
    rows = []
    for key, cfg in cfgs.items():
        weight = counts.get(key, 0)
        rows.append({
            "key": key,
            "name": cfg.get("nome", key),
            "description": cfg.get("descrizione", ""),
            "weight": weight,
            "pct": round(weight * 100 / total, 2) if total else 0,
            "values": [{"path": r["path"], "value": r["value"]} for r in v2.flatten(cfg) if r["path"] not in ("nome", "descrizione")],
        })
    none_weight = counts.get(None, 0)
    return {
        "mods": rows,
        "none_weight": none_weight,
        "none_pct": round(none_weight * 100 / total, 2) if total else 0,
        "pool_size": total,
    }


def modifiers_data():
    rows = []
    for name, cfg in getattr(bilanciamento, "EFFETTI_CONFIG", {}).items():
        description = "Modificatore temporaneo applicato al giocatore."
        reward = cfg.get("sfida", {}).get("premio_oggetto", {}) if isinstance(cfg, dict) else {}
        if "bonus_probabilita_per_livello_pct" in reward:
            description = f"In sfida, ogni livello aggiunge {reward['bonus_probabilita_per_livello_pct']} punti percentuali alla probabilità di ottenere un oggetto."
        rows.append({"name": name, "description": description, "config": v2.flatten(cfg)})
    return rows


def build_data():
    sets = set_data()
    data = v2.build_data()
    data["sets"] = sets
    data["items"] = item_data(sets)
    data["locations"] = location_data()
    data["assault"] = v2.assault_data(sets)
    data["approaches"] = approach_data(sets)
    data["nuclei"] = nuclei_data()
    data["events"] = events_data()
    data["weekend"] = weekend_data()
    data["modifiers"] = modifiers_data()
    data["scaglioni"] = _scaglione_source_rows()
    data["meta"] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "commit": v2.git_sha(),
        "repository": "ElSalamino/NftChallengeBot",
    }
    count_keys = ("bosses", "enemies", "locations", "items", "sets", "rings", "incantations", "assault", "approaches", "nuclei", "events", "modifiers")
    data["meta"]["counts"] = {k: len(data[k]) for k in count_keys}
    data["meta"]["counts"]["rooms"] = len(data["dungeon"]["rooms"])
    return data


def _must_replace(text, old, new, label):
    if old not in text:
        raise RuntimeError(f"Patch HTML non applicabile: {label}")
    return text.replace(old, new, 1)


def _replace_js_function(text, name, next_name, replacement):
    pattern = rf"function {re.escape(name)}\(.*?(?=\nfunction {re.escape(next_name)}\()"
    new_text, count = re.subn(pattern, replacement.rstrip() + "\n", text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"Funzione JS non sostituita: {name}")
    return new_text


ITEM_DETAIL_JS = r'''function itemDetail(name){const i=find(D.items,name);if(!i)return missing(name);let special='';if(i.ring){const r=find(D.rings,i.ring);if(r)special+=sectionTitle('Effetto anello')+`<div class="effect human">${esc(r.human||'')}</div><div class="effect">${esc(r.technical||'')}</div>`}if(i.book_effect){const c=find(D.incantations,i.book_effect);if(c)special+=sectionTitle('Incantesimo fornito')+`<p>${link('incantation',c.name)}</p><div class="effect">${esc(c.technical||'')}</div>`}if(i.nucleus)special+=sectionTitle('Nucleo')+`<p>${link('nucleus',i.nucleus,'Apri la meccanica completa del nucleo →')}</p>`;if(i.scaglione_source){const s=i.scaglione_source;special+=sectionTitle('Come si ottiene')+`<div class="card"><p><b>Dungeon:</b> ${link('room',s.room)} · azione <b>${esc(s.action)}</b>.</p><p><b>Probabilità nell’evento:</b> <span class="prob">${s.chance_pct}%</span>.</p><p>${esc(s.condition)}</p></div>`}return head(i.name,'Scheda unica dell’oggetto. Gli equipaggiamenti mostrano la progressione reale LV0 → LVMAX.','Oggetti')+`<div class="detail"><div>${i.description?`<div class="effect human">${esc(i.description)}</div>`:''}${sectionTitle('Tipologia')}<div class="chips">${i.types.map(x=>`<span class="chip">${esc(x)}</span>`).join('')}</div>${i.levels.length?sectionTitle('Statistiche LV0 → LVMAX')+levelsTable(i.levels):'<div class="note">Questo oggetto non usa livelli equipaggiamento.</div>'}${i.forging?sectionTitle('Come si ottengono LVX e LVMAX')+`<div class="card"><p><b>LVX:</b> ${esc(i.forging.lvx)}</p><p><b>LVMAX:</b> ${esc(i.forging.lvmax)}</p><p>${link('events','Scaglioni','Vedi dove trovare i quattro scaglioni →')}</p></div>`:''}${i.sets.length?sectionTitle('Set che lo usano')+chipLinks('set',i.sets):''}${i.events.length?sectionTitle('Eventi collegati')+chipLinks('event',i.events):''}${i.boss_drops.length?sectionTitle('Drop dei boss')+`<div class="card">${i.boss_drops.map(x=>`<div class="rowlink" onclick="location.hash='boss/${enc(x.boss)}'"><span>${esc(x.boss)}</span><span class="prob">${x.pct}%</span></div>`).join('')}</div>`:''}${i.location_drops.length?sectionTitle('Pool delle location')+`<div class="card">${i.location_drops.map(x=>`<div class="rowlink" onclick="location.hash='location/${enc(x.location)}'"><span>${esc(x.location)}</span><span class="prob">${x.pct}%</span></div>`).join('')}</div>`:''}${special}</div><aside class="sidebox">${img('items',i.name,i.icon||'🎒')}</aside></div>`}'''

SET_DETAIL_JS = r'''function setDetail(name){const s=find(D.sets,name);if(!s)return missing(name);const scoreNote=s.raw_score===0?'Questo set non usa statistiche grezze: il suo bilanciamento deriva dagli effetti speciali.':`Target 1200 · HP ×1 · ATK ×4 · DEF ×4 · AGI ×20${s.raw_score>1200?' · valore sopra target dovuto all’arrotondamento per eccesso':''}.`;return head(s.name,'Composizione, approcci ed effetti del set.','Set')+`<div class="detail"><div>${sectionTitle('Come si compone')}${chipLinks('item',s.components)}${sectionTitle('Effetto')}<div class="effect human">${esc(s.human||'Descrizione narrativa non presente.')}</div><div class="effect">${esc(s.technical||'Descrizione tecnica non presente.')}</div>${sectionTitle('Punteggio raw')}<div class="card"><div style="font-size:28px;font-weight:800">${esc(s.raw_score)}</div><div class="muted">${esc(scoreNote)}</div></div>${Object.values(s.bonus||{}).some(Number)?sectionTitle('Bonus grezzi')+stats(s.bonus):''}${s.approaches?.length?sectionTitle('Approcci disponibili')+chipLinks('approach',s.approaches):''}</div><aside class="sidebox">${img('sets',s.name,'🧩')}</aside></div>`}'''

EXTRA_JS = r'''
function approachDetail(name){const a=find(D.approaches,name);if(!a)return missing(name);const row=k=>{const v=a.multipliers[k],d=Math.round((v-1)*100);return `<tr><th>${k.toUpperCase()}</th><td class="mult">×${v}</td><td>${d===0?'nessuna variazione':`${d>0?'+':''}${d}%`}</td></tr>`};return head(a.name,'Come viene applicato l’approccio e quali set lo possono selezionare.','Approcci')+`<div class="detail"><div><div class="effect human">${esc(a.description)}</div>${sectionTitle('Moltiplicatori')}<div class="tablewrap"><table class="tbl"><thead><tr><th>Stat</th><th>Moltiplicatore</th><th>Effetto</th></tr></thead><tbody>${['hp','atk','def','agi'].map(row).join('')}</tbody></table></div>${sectionTitle('Come viene usato')}<div class="card"><p>Il gioco prende l’approccio selezionato e per HP, DEF, ATK e AGI esegue <code>round(stat × moltiplicatore)</code>. L’approccio modifica quindi la copia usata nello scontro, non la statistica base permanente dell’oggetto.</p></div>${sectionTitle('Set che lo hanno')}${chipLinks('set',a.sets)}</div><aside class="sidebox">${img('approaches',a.name,'🎭')}</aside></div>`}
function nucleusDetail(name){const n=find(D.nuclei,name);if(!n)return missing(name);return head(n.name,'Nucleo di clan: effetto pratico e valori reali usati nell’assalto.','Nuclei')+`<div class="detail"><div>${n.short?`<div class="effect human">${esc(n.short)}</div>`:''}<div class="effect">${esc(n.mechanic)}</div>${config(n.config)}</div><aside class="sidebox">${img('nuclei',n.name,'⚛️')}</aside></div>`}
function eventDetail(name){const e=find(D.events,name);if(!e)return missing(name);return head(e.name,'Oggetti associati a questa collezione/evento.','Eventi')+`${sectionTitle('Oggetti')}${chipLinks('item',e.items)}`}
function eventsHome(){const sc=D.scaglioni;return head('Weekend, eventi e modificatori','Area dedicata alle regole temporanee, alle collezioni evento e ai quattro scaglioni per LVMAX.','Eventi')+`${sectionTitle('Weekend')}<div class="card"><p>Il modificatore weekend viene estratto dal pool configurato. <b>Nessun modificatore</b>: peso ${D.weekend.none_weight}/${D.weekend.pool_size}, <span class="prob">${D.weekend.none_pct}%</span>.</p></div><div class="entity-grid">${D.weekend.mods.map(w=>`<div class="card" data-search="${esc((w.name+' '+w.description).toLowerCase())}"><h3>🎲 ${esc(w.name)}</h3><p>${esc(w.description)}</p><div class="muted">peso ${w.weight}/${D.weekend.pool_size} · <span class="prob">${w.pct}%</span></div></div>`).join('')}</div>${sectionTitle('Eventi / collezioni')}<div class="entity-grid">${D.events.map(e=>`<div class="card clickcard" onclick="location.hash='event/${enc(e.name)}'"><h3>🎉 ${esc(e.name)}</h3><div class="muted">${e.items.length} oggetti collegati</div></div>`).join('')}</div>${sectionTitle('Modificatori temporanei')}<div class="entity-grid">${D.modifiers.map(m=>`<div class="card"><h3>✨ ${esc(m.name)}</h3><p>${esc(m.description)}</p></div>`).join('')}</div>${sectionTitle('Scaglioni per LVMAX')}<div class="card"><p>Per trasformare un <b>LVX</b> in <b>LVMAX</b> serve possedere tutti e quattro questi scaglioni e incontrare il <b>Fabbro</b> nel dungeon scegliendo <b>Approcciala</b>. Il controllo del Fabbro non consuma nessuno dei quattro scaglioni.</p><div class="tablewrap"><table class="tbl"><thead><tr><th>Scaglione</th><th>Stanza</th><th>Azione</th><th>Probabilità nell’evento</th><th>Condizione</th></tr></thead><tbody>${sc.map(s=>`<tr><td>${link('item',s.name)}</td><td>${link('room',s.room)}</td><td>${esc(s.action)}</td><td class="prob">${s.chance_pct}%</td><td>${esc(s.condition)}</td></tr>`).join('')}</tbody></table></div><p class="muted">La probabilità indicata è quella del rilascio una volta arrivati alla relativa stanza/azione. La frequenza con cui la stanza compare dipende dalla generazione del dungeon.</p></div>`}
'''


def build_html():
    html = v2.HTML
    html = _must_replace(
        html,
        "<h3>${icon} ${esc(x.name)}</h3>",
        "<h3>${typeof icon==='function'?icon(x):icon} ${esc(x.name)}</h3>",
        "icone dinamiche lista",
    )
    html = _must_replace(
        html,
        "${categoryCard('sets','Set','Componenti, descrizione e meccanica tecnica.','🧩')}",
        "${categoryCard('sets','Set','Componenti, approcci ed effetti.','🧩')}${categoryCard('approaches','Approcci','Moltiplicatori e set che li utilizzano.','🎭')}",
        "home approcci",
    )
    html = _must_replace(
        html,
        "${categoryCard('assault','Assalto','Strutture, modalità e statistiche per livello.','🏰')}",
        "${categoryCard('assault','Assalto','Strutture, modalità e statistiche per livello.','🏰')}${categoryCard('nuclei','Nuclei','Bonus clan e meccaniche di assalto.','⚛️')}",
        "home nuclei",
    )
    html = _must_replace(
        html,
        "${categoryCard('incantations','Incantesimi','Libri ed effetti.','📖')}",
        "${categoryCard('incantations','Incantesimi','Libri ed effetti.','📖')}${categoryCard('events','Weekend, eventi e modificatori','Weekend, collezioni evento, scaglioni ed effetti temporanei.','🎉')}",
        "home eventi",
    )
    html = _must_replace(
        html,
        "D.items,'item',x=>x.types.join(' · '),'⚔️'",
        "D.items,'item',x=>x.types.join(' · '),x=>x.icon||'🎒'",
        "lista item emoji",
    )
    html = _must_replace(html, "<b>Approccio:</b> ${esc(b.approach||'—')}", "<b>Approccio:</b> ${b.approach?link('approach',b.approach):'—'}", "link approccio boss")
    html = _must_replace(html, "<b>Approccio:</b> ${esc(e.approach||'—')}", "<b>Approccio:</b> ${e.approach?link('approach',e.approach):'—'}", "link approccio nemico")
    html = _replace_js_function(html, "itemDetail", "setDetail", ITEM_DETAIL_JS)
    html = _replace_js_function(html, "setDetail", "enemyDetail", SET_DETAIL_JS)
    html = _must_replace(html, "function dungeonHome(){", EXTRA_JS + "\nfunction dungeonHome(){", "funzioni extra")
    html = _must_replace(
        html,
        "else if(type==='sets')html=listPage('Set','Apri un set per componenti, effetto narrativo e meccanica tecnica.',D.sets,'set',x=>x.components.join(' · '),'🧩');else if(type==='set')html=setDetail(name);",
        "else if(type==='sets')html=listPage('Set','Apri un set per componenti, approcci ed effetti.',D.sets,'set',x=>x.components.join(' · '),'🧩');else if(type==='set')html=setDetail(name);else if(type==='approaches')html=listPage('Approcci','Moltiplicatori applicati alle statistiche e set che li rendono disponibili.',D.approaches,'approach',x=>x.sets.join(' · '),'🎭');else if(type==='approach')html=approachDetail(name);",
        "routing approcci",
    )
    html = _must_replace(
        html,
        "else if(type==='assault')html=assaultHome();else if(type==='structure')html=structureDetail(name);else html=missing(raw);",
        "else if(type==='assault')html=assaultHome();else if(type==='structure')html=structureDetail(name);else if(type==='nuclei')html=listPage('Nuclei','Apri un nucleo per vedere l’effetto completo in assalto.',D.nuclei,'nucleus',x=>x.short,'⚛️');else if(type==='nucleus')html=nucleusDetail(name);else if(type==='events')html=eventsHome();else if(type==='event')html=eventDetail(name);else html=missing(raw);",
        "routing nuclei eventi",
    )
    return html


HTML = build_html()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="_site")
    args = parser.parse_args()
    out = Path(args.output)
    if not out.is_absolute(): out = ROOT / out
    out.mkdir(parents=True, exist_ok=True)
    data = build_data()
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (out / "index.html").write_text(HTML.replace("__DATA__", payload), encoding="utf-8")
    (out / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    assets = ROOT / "wiki" / "assets"
    if assets.exists(): shutil.copytree(assets, out / "assets", dirs_exist_ok=True)
    print("Wiki v3 generata:", out)
    print(json.dumps(data["meta"]["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

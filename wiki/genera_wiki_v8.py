#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wiki v8: ricette delle Forme Mega e sezione completa dedicata alla pesca."""
from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
from pathlib import Path

import genera_wiki_v7 as v7

ROOT = v7.ROOT
v6 = v7.v6
v5 = v7.v5
v4 = v7.v4
v3 = v7.v3
v2 = v7.v2
bilanciamento = v7.bilanciamento
liste = v7.liste
_prefixed_flatten = v7._prefixed_flatten
_structure_technical = v7._structure_technical


def _runtime_source():
    return v2.source_text("__init__.py")


def _literal_assignment(name, default):
    """Legge in sicurezza una semplice assegnazione top-level da __init__.py."""
    try:
        tree = ast.parse(_runtime_source())
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            if any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
                return ast.literal_eval(node.value)
    except Exception:
        pass
    return default


def _base(name):
    return v2.base_item(name)


def _regex_pair(pattern, default):
    match = re.search(pattern, _runtime_source(), re.S)
    if not match:
        return list(default)
    return [int(match.group(1)), int(match.group(2))]


def _regex_int(pattern, default):
    match = re.search(pattern, _runtime_source(), re.S)
    return int(match.group(1)) if match else default


def _mega_data():
    mega_runtime = [_base(x) for x in _literal_assignment(
        "megaman",
        ["Neo blaster LV0", "Spada a protoni LV0", "Z-Saber LV0", "Chip terra LV0", "Chip fuoco LV0", "Chip elettro LV0", "Chip lunare LV0"],
    )]
    mega_items = [_base(x) for x in _literal_assignment("megaset", mega_runtime)]
    weapons = [x for x in mega_items if not x.lower().startswith("chip ")]
    chips = [x for x in mega_items if x.lower().startswith("chip ")]
    form_by_chip = {
        "Chip terra": "Forma terra",
        "Chip fuoco": "Forma fuoco",
        "Chip lunare": "Forma lunare",
        "Chip elettro": "Forma elettro",
    }
    return {
        "event": "Megaevento",
        "items": mega_items,
        "weapons": weapons,
        "chips": chips,
        "form_by_chip": form_by_chip,
    }


def _fishing_data():
    source = _runtime_source()
    fishing_items = [_base(x) for x in _literal_assignment(
        "item_pescatore",
        ["Canna rossa", "Canna blu", "Canna magenta", "Cappellino da pescatore", "Armatura di esche", "Secchiello di vermi", "Giubbina con lenze"],
    )]
    fisherman_rewards = [_base(x) for x in _literal_assignment("premi_pescatore", fishing_items)]

    wait_seconds = _regex_pair(r"attesa\s*=\s*random\.randint\((\d+)\s*,\s*(\d+)\)", (1, 2))
    weight_kg = _regex_pair(r"PesoKg\s*=\s*random\.randint\((\d+)\s*,\s*(\d+)\)", (0, 55))
    weight_decimals = _regex_pair(r"PesoG\s*=\s*random\.randint\((\d+)\s*,\s*(\d+)\)", (0, 97))
    reaction_seconds = _regex_int(r"orario_concesso\s*=\s*float\(orario\)\s*\+\s*(\d+)", 3)
    random_power = _regex_pair(r"fs_w\s*\+=\s*random\.randint\((\d+)\s*,\s*(\d+)\)", (0, 2))

    set_bonus = {
        "Pescatore": bilanciamento.PROC_CLASSI.get("Pescatore", {}).get("pesca", {}).get("rarita", {}).get("bonus_rarita", 1),
        "Pescatore di balene": bilanciamento.PROC_CLASSI.get("Pescatore di balene", {}).get("pesca", {}).get("rarita", {}).get("bonus_rarita", 2),
    }

    locations = []
    for location, fish in getattr(liste, "pesciame", {}).items():
        locations.append({
            "name": location,
            "fish": [_base(x) for x in fish],
        })

    fish_all = [_base(x) for x in getattr(liste, "pesci", [])]
    ingredients = list(getattr(liste, "ingredienti", []))

    return {
        "command": "/pesca",
        "requirements": [
            "Si usa in chat privata.",
            "Non puoi pescare dall'Hub.",
            "Non puoi iniziare se sei inabilitato o se hai già una pesca in corso.",
        ],
        "wait_seconds": wait_seconds,
        "reaction_seconds": reaction_seconds,
        "weight_kg": weight_kg,
        "weight_decimals": weight_decimals,
        "power": {
            "base": 1,
            "equipment_bonus_each": 1,
            "equipment": fishing_items,
            "set_bonus": set_bonus,
            "weather": {
                "Pioggia": 1,
                "Tempesta": 2,
                "Caldo torrido": -1,
                "Caldo infernale": -2,
            },
            "random_bonus": random_power,
            "minimum": 1,
            "selection": "Il pesce viene estratto casualmente tra gli elementi dall'indice 0 fino a min(Potere di pesca, ultimo indice) del pool della location. Aumentare il Potere di pesca sblocca quindi progressivamente i pesci più in fondo alla lista, senza escludere quelli comuni.",
        },
        "locations": locations,
        "fish_all": fish_all,
        "records": {
            "micro_max_kg": 2,
            "macro_min_kg": 52,
            "description": "Ogni cattura aggiorna il bestiario: per ogni specie viene conservato il record personale di peso. Il pesce viene narrativamente liberato subito dopo la cattura.",
        },
        "storage": {
            "description": "Il runtime contiene già una sacca materiali: se il giocatore possiede la sacca ed è nel gruppo di test autorizzato, la cattura aggiunge 1 × 'Pesce <specie>' alla sacca. Per gli altri giocatori oggi il pesce resta soltanto nel bestiario/record.",
            "experimental": True,
        },
        "fisherman": {
            "refresh_hours": [0, 6, 12, 18],
            "reward_pool": fisherman_rewards,
            "description": "Quattro volte al giorno il Pescatore assegna a ogni giocatore una specie casuale richiesta. Se quella specie viene pescata, la richiesta si chiude e viene assegnato un oggetto casuale del set da pescatore.",
        },
        "marine_encounters": {
            "chance": [
                {"power": "6", "pct": 3},
                {"power": "7", "pct": 5},
                {"power": "8+", "pct": 20},
            ],
            "bosses": [
                {"name": "Kraken Nautico", "drops": ["Un dente di kraken", "Uncino enorme", "Delle squame viscide"]},
                {"name": "Balena territoriale", "drops": ["Dell'ambrosia", "Un eco-locatore"]},
                {"name": "Granchio da rave", "drops": ["Corona del rave", "Staffa da rave", "Chela animata"]},
            ],
            "description": "Con Potere di pesca alto una normale cattura può trasformarsi in una lotta marina. Il nemico viene scelto casualmente tra i tre boss nautici.",
        },
        "potions_now": {
            "ingredients": ingredients,
            "fish_materials": [f"Pesce {x}" for x in fish_all],
            "requirements_per_potion": 4,
            "description": "Esiste già lo scheletro del futuro sistema pozioni: allneed è formato da tutti i pesci prefissati con 'Pesce ' più liste.ingredienti, e il reset assegna a ogni pozione esistente 4 requisiti casuali da quel pool. La raccolta universale degli ingredienti e una vera interfaccia di preparazione sono però ancora da completare.",
        },
    }


def build_data():
    data = v7.build_data()
    mega = _mega_data()

    for row in data.get("sets", []):
        chip = next((chip for chip, form in mega["form_by_chip"].items() if form == row.get("name")), None)
        if not chip:
            continue
        row["mega_recipe"] = {
            "event": mega["event"],
            "weapons": mega["weapons"],
            "chip": chip,
            "description": (
                f"Mixa/equipaggia insieme 2 item del {mega['event']}: una delle armi Megaevento "
                f"({', '.join(mega['weapons'])}) e {chip}. Il chip è la protezione che determina la Forma. "
                "Non è una ricetta di forgia e gli oggetti non vengono consumati: la Forma si attiva dal mix arma + chip equipaggiato."
            ),
        }

    data["mega_event"] = mega
    data["fishing"] = _fishing_data()
    data["meta"]["wiki_version"] = 8
    return data


EXTRA_JS = r'''
setDetail=function(name){const s=find(D.sets,name);if(!s)return missing(name);const scoreNote=s.raw_score===0?'Questo set non usa statistiche grezze: il suo bilanciamento deriva dagli effetti speciali.':`Target 1200 · HP ×1 · ATK ×4 · DEF ×4 · AGI ×20${s.raw_score>1200?' · valore sopra target dovuto all’arrotondamento per eccesso':''}.`;let composition='';if(s.mega_recipe){const m=s.mega_recipe;composition=sectionTitle('Come si ottiene / attiva la Forma Mega')+`<div class="card"><p>${esc(m.description)}</p><p><b>Arma Megaevento — scegline una:</b></p>${chipLinks('item',m.weapons)}<p><b>Chip richiesto:</b> ${link('item',m.chip)}</p></div>`}else{composition=sectionTitle('Come si compone')+chipLinks('item',s.components)}return head(s.name,'Composizione, approcci ed effetti del set.','Set')+`<div class="detail"><div>${composition}${sectionTitle('Effetto')}<div class="effect human">${esc(s.human||'Descrizione narrativa non presente.')}</div><div class="effect">${esc(s.technical||'Descrizione tecnica non presente.')}</div>${sectionTitle('Punteggio raw')}<div class="card"><div style="font-size:28px;font-weight:800">${esc(s.raw_score)}</div><div class="muted">${esc(scoreNote)}</div></div>${Object.values(s.bonus||{}).some(Number)?sectionTitle('Bonus grezzi')+stats(s.bonus):''}${s.approaches?.length?sectionTitle('Approcci disponibili')+chipLinks('approach',s.approaches):''}</div><aside class="sidebox">${img('sets',s.name,'🧩')}</aside></div>`};

function fishingPage(){const f=D.fishing,p=f.power;const signed=n=>`${n>0?'+':''}${n}`;const weather=Object.entries(p.weather).map(([name,value])=>`<tr><td>${esc(name)}</td><td class="prob">${signed(value)} Potere</td></tr>`).join('');const setRows=Object.entries(p.set_bonus).map(([name,value])=>`<tr><td>${link('set',name)}</td><td class="prob">+${value}</td></tr>`).join('');const marine=f.marine_encounters.chance.map(x=>`<tr><td>${esc(x.power)}</td><td class="prob">${x.pct}%</td></tr>`).join('');const locations=f.locations.map(l=>`<div class="card"><h3>${link('location',l.name)}</h3><div class="muted">Ordine del pool: più il pesce è a destra, più Potere serve per renderlo estraibile.</div>${chipLinks('item',l.fish)}</div>`).join('');const bosses=f.marine_encounters.bosses.map(b=>`<div class="card"><h3>${esc(b.name)}</h3><div class="muted">Possibili premi</div>${chipLinks('item',b.drops)}</div>`).join('');return head('Pesca','Come funziona davvero /pesca: tempismo, Potere di pesca, specie, record e materiali.','Pesca')+`${sectionTitle('Come si pesca')}<div class="card"><p>Usa <code>${esc(f.command)}</code>. Il bot aspetta casualmente <b>${f.wait_seconds[0]}–${f.wait_seconds[1]} secondi</b>, poi compare il pulsante <b>Pesca!</b>: devi premerlo entro <b>${f.reaction_seconds} secondi</b>.</p><div class="chips">${f.requirements.map(x=>`<span class="chip">${esc(x)}</span>`).join('')}</div><p>Il peso viene generato separatamente: parte intera tra ${f.weight_kg[0]} e ${f.weight_kg[1]} kg e parte decimale tra ${f.weight_decimals[0]} e ${f.weight_decimals[1]}.</p></div>${sectionTitle('Potere di pesca')}<div class="card"><p>Parte da <b>${p.base}</b>. Ogni arma/protezione da pescatore equipaggiata aggiunge <b>+${p.equipment_bonus_each}</b>. Poi entrano set, meteo e un bonus casuale di <b>${p.random_bonus[0]}–${p.random_bonus[1]}</b>. Il valore finale non può scendere sotto ${p.minimum}.</p><p><b>Equipaggiamenti da pescatore:</b></p>${chipLinks('item',p.equipment)}<div class="tablewrap"><table class="tbl"><thead><tr><th>Set</th><th>Bonus</th></tr></thead><tbody>${setRows}</tbody></table></div><div class="tablewrap"><table class="tbl"><thead><tr><th>Meteo</th><th>Variazione</th></tr></thead><tbody>${weather}</tbody></table></div><p>${esc(p.selection)}</p></div>${sectionTitle('Pesci per location')}<div class="entity-grid">${locations}</div>${sectionTitle('Record e bestiario')}<div class="card"><p>${esc(f.records.description)}</p><p><b>Micro Pescatore:</b> pesce da ${f.records.micro_max_kg} kg o meno. <b>Macro Pescatore:</b> pesce da ${f.records.macro_min_kg} kg o più.</p></div>${sectionTitle('Sacca e futuro uso come ingredienti')}<div class="card"><p>${esc(f.storage.description)}</p><p>${esc(f.potions_now.description)}</p><p><b>Ingredienti non-pesce già dichiarati:</b></p><div class="chips">${f.potions_now.ingredients.map(x=>`<span class="chip">${esc(x)}</span>`).join('')||'<span class="muted">—</span>'}</div></div>${sectionTitle('Richieste del Pescatore')}<div class="card"><p>${esc(f.fisherman.description)}</p><p><b>Cambio richiesta:</b> ore ${f.fisherman.refresh_hours.join(', ')}.</p><p><b>Premi possibili:</b></p>${chipLinks('item',f.fisherman.reward_pool)}</div>${sectionTitle('Lotte marine')}<div class="card"><p>${esc(f.marine_encounters.description)}</p><div class="tablewrap"><table class="tbl"><thead><tr><th>Potere di pesca</th><th>Probabilità lotta marina</th></tr></thead><tbody>${marine}</tbody></table></div></div><div class="entity-grid">${bosses}</div>`}
'''


def build_html():
    html = v7.HTML
    html = v3._must_replace(
        html,
        "${categoryCard('locations','Location','Collegamenti, loot, pesca e casa nemici.','🗺️')}",
        "${categoryCard('locations','Location','Collegamenti, loot, pesca e casa nemici.','🗺️')}${categoryCard('fishing','Pesca','Potere di pesca, specie, record, Pescatore e lotte marine.','🎣')}",
        "home pesca",
    )
    html = v3._must_replace(
        html,
        "else if(type==='location')html=locationDetail(name);else if(type==='items')",
        "else if(type==='location')html=locationDetail(name);else if(type==='fishing')html=fishingPage();else if(type==='items')",
        "router pesca",
    )
    html = v3._must_replace(
        html,
        "function render(){",
        EXTRA_JS + "\nfunction render(){",
        "pagina pesca e override Forme Mega",
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

    print("Wiki v8 generata:", out)
    print(json.dumps(data["meta"]["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

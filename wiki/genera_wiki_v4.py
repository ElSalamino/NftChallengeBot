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


def _fmt_num(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).replace(".", ",")


def _stat_name(token):
    return {
        "atk": "attacco",
        "def": "difesa",
        "agi": "agilità",
        "hp": "HP",
    }.get(token, token.replace("_", " "))


def _human_param(path, value):
    """Trasforma un parametro runtime in una frase leggibile dal giocatore.

    I booleani non vengono mai esposti come True/False: il loro significato
    viene tradotto direttamente nell'effetto di gioco.
    """
    leaf = path.rsplit(".", 1)[-1]

    # Parametri di sistema.
    if leaf == "divisore_livello":
        pct = 100 / float(value)
        return f"Le statistiche base della struttura aumentano del {_fmt_num(pct)}% per ogni livello."

    # Booleani con significato di gioco esplicito.
    if leaf == "attacco_diretto":
        return (
            "Questa modalità colpisce direttamente l'attaccante."
            if value else
            "Questa modalità non colpisce direttamente l'attaccante: applica invece il proprio effetto speciale."
        )
    if leaf == "rincorsa_disabilitata":
        return "La rincorsa è disattivata in questa modalità." if value else "La rincorsa resta attiva in questa modalità."
    if leaf == "cura":
        return "Questa modalità cura invece di infliggere il normale effetto offensivo." if value else "Questa modalità non applica cure."

    # Probabilità.
    if leaf.endswith("_proc") or leaf.endswith("_pct") or leaf.endswith("_soglia_pct"):
        nome = leaf
        labels = {
            "distrazione_proc": "distrarre l'attaccante",
            "colpito_proc": "attivare l'effetto quando viene colpito",
            "infezione_proc": "infettare l'attaccante",
            "corvi_proc": "evocare i corvi",
            "creatura_proc": "evocare la creatura",
            "rincorsa_proc": "attivare una rincorsa",
            "rincorsa_extra_proc": "attivare ciascuna rincorsa extra",
            "bonus_def_proc": "attivare il bonus difesa",
            "stop_proc": "fermare l'attaccante",
            "roll_bonus_pct": "ottenere il bonus al tiro",
            "drago_proc": "attivare il drago",
            "mamma_proc": "far intervenire la mamma",
        }
        effetto = labels.get(nome, nome.replace("_proc", "").replace("_pct", "").replace("_", " "))
        return f"Ha il {_fmt_num(value)}% di probabilità di {effetto}."

    # Moltiplicatori e divisori.
    if leaf.endswith("_mul"):
        labels = {
            "danno_mul": "Il danno",
            "atk_mul": "L'attacco",
            "def_attaccante_mul": "La difesa dell'attaccante",
            "atk_da_def_mul": "L'attacco ottenuto dalla difesa",
        }
        soggetto = labels.get(leaf, leaf[:-4].replace("_", " ").capitalize())
        return f"{soggetto} viene moltiplicato per {_fmt_num(value)}."
    if leaf.endswith("_divisore"):
        labels = {
            "bonus_def_strutture_divisore": "Il bonus difesa fornito dalle altre strutture",
            "danno_divisore": "Il danno",
            "rincorsa_danno_divisore": "Il danno della rincorsa",
            "atk_divisore": "L'attacco",
            "def_da_atk_divisore": "La difesa ottenuta dall'attacco",
            "agi_difensore_divisore": "L'agilità del difensore usata nel tiro",
        }
        soggetto = labels.get(leaf, leaf[:-10].replace("_", " ").capitalize())
        return f"{soggetto} viene diviso per {_fmt_num(value)}."

    # Variazioni dirette delle statistiche.
    for stat in ("atk", "def", "agi", "hp"):
        if leaf == f"{stat}_delta":
            segno = "+" if float(value) >= 0 else ""
            return f"Modifica {_stat_name(stat)} di {segno}{_fmt_num(value)}."
        if leaf == f"bonus_{stat}":
            return f"Aggiunge {_fmt_num(value)} punti di {_stat_name(stat)}."
        if leaf == f"bonus_{stat}_difese":
            return f"Aggiunge {_fmt_num(value)} punti di {_stat_name(stat)} alle difese."
        if leaf == f"bonus_{stat}_per_livello":
            return f"Aggiunge {_fmt_num(value)} punti di {_stat_name(stat)} per ogni livello della struttura."

    # Casi specifici non riconducibili bene a una formula generica.
    special = {
        "infezione_def_delta": lambda v: f"Quando l'infezione si attiva, la difesa dell'attaccante cambia di {_fmt_num(v)} punti.",
        "danno_bonus": lambda v: f"Aggiunge {_fmt_num(v)} danni all'effetto della modalità.",
        "autodanno": lambda v: f"La struttura subisce {_fmt_num(v)} danni quando usa questo effetto.",
        "bonus_atk_difese_su_mancato_colpo": lambda v: f"Se il colpo manca, le difese ottengono {_fmt_num(v)} punti di attacco.",
        "rincorse_extra_max": lambda v: f"Può effettuare fino a {_fmt_num(v)} rincorse extra.",
        "drago_bonus_agi": lambda v: f"Quando il drago si attiva, aggiunge {_fmt_num(v)} punti di agilità.",
        "mamma_hp_min": lambda v: f"L'intervento della mamma può modificare gli HP a partire da {_fmt_num(v)}.",
        "mamma_hp_max": lambda v: f"L'intervento della mamma può modificare gli HP fino a {_fmt_num(v)}.",
        "valore_per_livello": lambda v: f"L'effetto aumenta di {_fmt_num(v)} punti per ogni livello della struttura.",
        "hp_minimo_modifica": lambda v: f"L'effetto modifica gli HP solo rispettando la soglia minima di {_fmt_num(v)} HP.",
        "bersagli": lambda v: "L'effetto si applica a tutti i bersagli." if str(v) == "tutti" else f"L'effetto si applica a {_fmt_num(v)} bersaglio.",
        "bonus": lambda v: f"Il tiro riceve un bonus fisso di {_fmt_num(v)}.",
        "random_max": lambda v: f"Il tiro casuale può arrivare fino a {_fmt_num(v)}.",
        "random_min": lambda v: f"Il moltiplicatore casuale minimo è {_fmt_num(v)}.",
        "numeratore": lambda v: f"La formula del danno usa come valore base {_fmt_num(v)}.",
        "difesa_base": lambda v: f"La formula considera una difesa base di {_fmt_num(v)}.",
        "danno_minimo": lambda v: f"Un colpo che infligge danno non può scendere sotto {_fmt_num(v)} danni.",
    }
    if leaf in special:
        return special[leaf](value)

    # Fallback leggibile: mai path tecnici, mai booleani grezzi.
    label = leaf.replace("_", " ")
    if isinstance(value, bool):
        return f"{label.capitalize()}: {'attivo' if value else 'disattivato'}."
    if isinstance(value, (list, tuple)):
        return f"{label.capitalize()}: {', '.join(str(x) for x in value)}."
    return f"{label.capitalize()}: {_fmt_num(value)}."


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
        pieces.extend(_human_param(r["path"], r["value"]) for r in system_rows)
    if general_rows:
        pieces.append("Effetti sempre attivi per questa struttura:")
        pieces.extend(_human_param(r["path"], r["value"]) for r in general_rows)
    if mode_rows:
        pieces.append(f"In modalità {mode_name}:")
        pieces.extend(_human_param(r["path"], r["value"]) for r in mode_rows)
    elif not general_rows:
        pieces.append(f"La modalità {mode_name} non aggiunge effetti speciali oltre alle statistiche della struttura.")

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
    # technical_params resta nel JSON per audit/validazione, ma non viene mostrato
    # nella pagina giocatore: lì compare soltanto la spiegazione leggibile.
    for structure in data.get("assault", []):
        for mode in structure.get("modes", []):
            technical, rows = _structure_technical(structure["name"], mode["name"])
            mode["technical"] = technical
            mode["technical_params"] = rows

    data["meta"]["wiki_version"] = 4
    return data


ITEM_DETAIL_JS = r'''function itemDetail(name){const i=find(D.items,name);if(!i)return missing(name);let special='';if(i.ring){const r=find(D.rings,i.ring);if(r)special+=sectionTitle('Effetto anello')+`<div class="effect human">${esc(r.human||'')}</div><div class="effect">${esc(r.technical||'')}</div>`}if(i.book_effect){const c=find(D.incantations,i.book_effect);if(c)special+=sectionTitle('Incantesimo fornito')+`<p>${link('incantation',c.name)}</p><div class="effect">${esc(c.technical||'')}</div>`}if(i.nucleus)special+=sectionTitle('Nucleo')+`<p>${link('nucleus',i.nucleus,'Apri la meccanica completa del nucleo →')}</p>`;if(i.scaglione_source){const s=i.scaglione_source;special+=sectionTitle('Come si ottiene')+`<div class="card"><p><b>Dungeon:</b> ${link('room',s.room)} · azione <b>${esc(s.action)}</b>.</p><p><b>Probabilità nell’evento:</b> <span class="prob">${s.chance_pct}%</span>.</p><p>${esc(s.condition)}</p></div>`}return head(i.name,'Scheda unica dell’oggetto. Gli equipaggiamenti mostrano la progressione reale LV0 → LVMAX.','Oggetti')+`<div class="detail"><div>${i.description?`<div class="effect human">${esc(i.description)}</div>`:''}${i.usable_technical?sectionTitle('Effetto tecnico dell’usabile')+`<div class="effect">${esc(i.usable_technical)}</div>`:''}${sectionTitle('Tipologia')}<div class="chips">${i.types.map(x=>`<span class="chip">${esc(x)}</span>`).join('')}</div>${i.levels.length?sectionTitle('Statistiche LV0 → LVMAX')+levelsTable(i.levels):'<div class="note">Questo oggetto non usa livelli equipaggiamento.</div>'}${i.forging?sectionTitle('Come si ottengono LVX e LVMAX')+`<div class="card"><p><b>LVX:</b> ${esc(i.forging.lvx)}</p><p><b>LVMAX:</b> ${esc(i.forging.lvmax)}</p><p>${link('events','Scaglioni','Vedi dove trovare i quattro scaglioni →')}</p></div>`:''}${i.sets.length?sectionTitle('Set che lo usano')+chipLinks('set',i.sets):''}${i.events.length?sectionTitle('Eventi collegati')+chipLinks('event',i.events):''}${i.boss_drops.length?sectionTitle('Drop dei boss')+`<div class="card">${i.boss_drops.map(x=>`<div class="rowlink" onclick="location.hash='boss/${enc(x.boss)}'"><span>${esc(x.boss)}</span><span class="prob">${x.pct}%</span></div>`).join('')}</div>`:''}${i.location_drops.length?sectionTitle('Pool delle location')+`<div class="card">${i.location_drops.map(x=>`<div class="rowlink" onclick="location.hash='location/${enc(x.location)}'"><span>${esc(x.location)}</span><span class="prob">${x.pct}%</span></div>`).join('')}</div>`:''}${special}</div><aside class="sidebox">${img('items',i.name,i.icon||'🎒')}</aside></div>`}'''


STRUCTURE_DETAIL_JS = r'''function structureDetail(name){const a=find(D.assault,name);if(!a)return missing(name);const first=a.modes[0];return head(a.name,`Struttura d’assalto. Le statistiche crescono con il livello della struttura.`,'Assalto')+`<div class="detail"><div>${sectionTitle('Modalità')}<div class="modebar" id="modebar">${a.modes.map((m,i)=>`<button class="btn ${i===0?'active':''}" data-mode="${esc(m.name)}">${esc(m.name)}</button>`).join('')}</div><div id="modeDesc" class="effect human">${esc(first.description||'—')}</div>${sectionTitle('Funzionamento tecnico completo')}<div id="modeTechnical" class="effect">${esc(first.technical||'—')}</div>${sectionTitle('Statistiche della modalità')}<div class="levelbox"><b>LV <span id="structLv">0</span></b><input id="structRange" type="range" min="0" max="50" value="0"></div><div id="structStats">${stats(first.levels[0].stats)}</div>${sectionTitle('Statistiche a ogni livello')}<div id="structTable">${statsTable(first.levels)}</div>${a.set_refs.length?sectionTitle('Set collegati / counter')+chipLinks('set',a.set_refs):''}</div><aside class="sidebox">${img('assault',a.name,'🏰')}<div class="card" style="margin-top:12px"><h3>Stats base</h3>${stats(a.base_stats)}${a.resource_value!=null?`<p class="muted">Valore <code>hps</code> nel database: ${esc(a.resource_value)}</p>`:''}</div></aside></div>`}'''


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
    new = "document.getElementById('modeDesc').textContent=m.description||'—';document.getElementById('modeTechnical').textContent=m.technical||'—';"
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

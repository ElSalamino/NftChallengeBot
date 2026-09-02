#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wiki v5: descrizioni d'assalto compatte, contestuali e senza ripetizioni."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import genera_wiki_v4 as v4

ROOT = v4.ROOT
v3 = v4.v3
bilanciamento = v3.bilanciamento
liste = v3.liste
v2 = v3.v2
_prefixed_flatten = v4._prefixed_flatten


def _fmt_num(value):
    return v4._fmt_num(value)


def _signed(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    prefix = "+" if number >= 0 else ""
    return prefix + _fmt_num(number)


def _stat_bonus_text(cfg):
    values = []
    for key, label in (("bonus_atk", "ATK"), ("bonus_def", "DEF"), ("bonus_agi", "AGI"), ("bonus_hp", "HP")):
        if key in cfg:
            values.append(f"{_signed(cfg[key])} {label}")
    return ", ".join(values)


def _describe_effects(structure_name, mode_name, source):
    """Converte un blocco config in poche frasi, raggruppando gli effetti legati."""
    cfg = dict(source or {})
    phrases = []

    # Effetti che prima risultavano particolarmente incomprensibili.
    if structure_name == "Sedimento del cucciolo" and all(k in cfg for k in ("mamma_proc", "mamma_hp_min", "mamma_hp_max")):
        proc = cfg.pop("mamma_proc")
        hp_min = cfg.pop("mamma_hp_min")
        hp_max = cfg.pop("mamma_hp_max")
        phrases.append(
            f"C'è il {_fmt_num(proc)}% di probabilità che intervenga la madre del cucciolo: "
            f"gli HP dell'attaccante vengono impostati a un valore casuale tra {_fmt_num(hp_min)} e {_fmt_num(hp_max)}."
        )

    if structure_name == "Cannoncino":
        base_agi = cfg.pop("bonus_agi_difese", None)
        proc = cfg.pop("drago_proc", None)
        extra_agi = cfg.pop("drago_bonus_agi", None)
        if base_agi is not None and proc is not None and extra_agi is not None:
            phrases.append(
                f"Fornisce {_signed(base_agi)} AGI alle difese; inoltre, con il {_fmt_num(proc)}% di probabilità "
                f"sveglia il drago e assegna altri {_signed(extra_agi)} AGI alle difese."
            )
        else:
            if base_agi is not None:
                phrases.append(f"Fornisce {_signed(base_agi)} AGI alle difese.")
            if proc is not None:
                if extra_agi is not None:
                    phrases.append(f"Con il {_fmt_num(proc)}% di probabilità sveglia il drago e dà {_signed(extra_agi)} AGI alle difese.")
                else:
                    phrases.append(f"Con il {_fmt_num(proc)}% di probabilità sveglia il drago.")

    # Bersaglio enorme: "distrazione" significa forzare il bersaglio dell'attacco.
    if structure_name == "Bersaglio enorme" and "distrazione_proc" in cfg:
        proc = cfg.pop("distrazione_proc")
        phrases.append(f"Ha il {_fmt_num(proc)}% di probabilità di forzare l'attaccante a colpire il Bersaglio enorme.")

    if structure_name == "Bersaglio enorme" and mode_name == "Movibile" and "colpito_proc" in cfg:
        proc = cfg.pop("colpito_proc")
        damage = cfg.pop("danno_mul", None)
        text = f"Quando viene bersagliato ha il {_fmt_num(proc)}% di probabilità di essere colpito"
        if damage is not None:
            text += f"; se il colpo entra, il danno viene moltiplicato per {_fmt_num(damage)}"
        phrases.append(text + ".")

    # Muraglione: raccoglie in una sola frase infezione e bonus difensivo.
    if "infezione_proc" in cfg:
        proc = cfg.pop("infezione_proc")
        delta = cfg.pop("infezione_def_delta", None)
        if delta is None:
            phrases.append(f"Ha il {_fmt_num(proc)}% di probabilità di infettare l'attaccante.")
        else:
            phrases.append(f"Ha il {_fmt_num(proc)}% di probabilità di infettare l'attaccante, modificandone la DEF di {_signed(delta)}.")

    if "bonus_def_per_livello" in cfg and "bonus_def_strutture_divisore" in cfg:
        per_level = cfg.pop("bonus_def_per_livello")
        divisor = cfg.pop("bonus_def_strutture_divisore")
        phrases.append(
            f"Il bonus difensivo vale {_signed(per_level)} DEF per livello della struttura, "
            f"con un contributo aggiuntivo legato al numero di strutture presenti diviso per {_fmt_num(divisor)}."
        )

    # Evocazioni: probabilità e bonus vanno spiegati insieme.
    if "creatura_proc" in cfg:
        proc = cfg.pop("creatura_proc")
        bonus = _stat_bonus_text(cfg)
        for key in ("bonus_atk", "bonus_def", "bonus_agi", "bonus_hp"):
            cfg.pop(key, None)
        if bonus:
            phrases.append(f"Con il {_fmt_num(proc)}% di probabilità evoca una creatura che dà alle difese {bonus}.")
        else:
            phrases.append(f"Con il {_fmt_num(proc)}% di probabilità evoca una creatura.")

    if "corvi_proc" in cfg:
        proc = cfg.pop("corvi_proc")
        phrases.append(f"Ha il {_fmt_num(proc)}% di probabilità di evocare i corvi.")

    # Probabilità + relativo bonus difensivo in un'unica frase.
    if "bonus_def_proc" in cfg:
        proc = cfg.pop("bonus_def_proc")
        bonus = cfg.pop("bonus_def", None)
        if bonus is not None:
            phrases.append(f"Con il {_fmt_num(proc)}% di probabilità le difese ottengono {_signed(bonus)} DEF.")
        else:
            phrases.append(f"Con il {_fmt_num(proc)}% di probabilità attiva il bonus difensivo.")

    # Rincorse: una sola spiegazione invece di tre/quattro frasi scollegate.
    if "rincorsa_proc" in cfg:
        proc = cfg.pop("rincorsa_proc")
        damage_div = cfg.pop("rincorsa_danno_divisore", None)
        text = f"Dopo il colpo ha il {_fmt_num(proc)}% di probabilità di effettuare una rincorsa"
        if damage_div is not None:
            text += f" che infligge un danno pari a 1/{_fmt_num(damage_div)} del normale"
        phrases.append(text + ".")
    if "rincorsa_extra_proc" in cfg:
        proc = cfg.pop("rincorsa_extra_proc")
        max_extra = cfg.pop("rincorse_extra_max", None)
        text = f"Ogni rincorsa successiva ha il {_fmt_num(proc)}% di probabilità di partire"
        if max_extra is not None:
            text += f", fino a {_fmt_num(max_extra)} rincorse extra"
        phrases.append(text + ".")

    # Effetti opposti che hanno senso solo se letti insieme.
    if "danno_bonus" in cfg or "autodanno" in cfg:
        damage = cfg.pop("danno_bonus", None)
        self_damage = cfg.pop("autodanno", None)
        chunks = []
        if damage is not None:
            chunks.append(f"aggiunge {_signed(damage)} danni")
        if self_damage is not None:
            chunks.append(f"la struttura perde {_fmt_num(self_damage)} HP quando l'effetto si attiva")
        phrases.append("; ".join(chunks).capitalize() + ".")

    # Conversione ATK/DEF della stazione laser.
    if "atk_da_def_mul" in cfg or "def_da_atk_divisore" in cfg:
        atk_from_def = cfg.pop("atk_da_def_mul", None)
        def_from_atk = cfg.pop("def_da_atk_divisore", None)
        chunks = []
        if atk_from_def is not None:
            chunks.append(f"usa la DEF base ×{_fmt_num(atk_from_def)} come ATK")
        if def_from_atk is not None:
            chunks.append(f"usa l'ATK base /{_fmt_num(def_from_atk)} come DEF")
        phrases.append(" e ".join(chunks).capitalize() + ".")

    # Centrale di cura: valore e soglia sono una sola regola.
    if structure_name == "Centrale di cura centralizzata" and "valore_per_livello" in cfg:
        value = cfg.pop("valore_per_livello")
        threshold = cfg.pop("hp_minimo_modifica", None)
        text = f"L'effetto vale {_fmt_num(value)} HP per livello della Centrale"
        if threshold is not None:
            text += f" e interviene sulle strutture che hanno più di {_fmt_num(threshold)} HP"
        phrases.append(text + ".")

    # Bersagli della centrale.
    if structure_name == "Centrale di cura centralizzata" and "bersagli" in cfg:
        targets = cfg.pop("bersagli")
        if str(targets) == "tutti":
            phrases.append("Applica l'effetto a tutte le strutture valide.")
        else:
            phrases.append(f"Applica l'effetto a {_fmt_num(targets)} sola struttura valida.")

    # Le modifiche statistiche semplici rimaste vengono rese in forma compatta.
    stat_parts = []
    for key, label in (("atk_delta", "ATK"), ("def_delta", "DEF"), ("agi_delta", "AGI"), ("hp_delta", "HP")):
        if key in cfg:
            stat_parts.append(f"{label} {_signed(cfg.pop(key))}")
    for key, label in (("atk_mul", "ATK"), ("def_mul", "DEF"), ("agi_mul", "AGI"), ("hp_mul", "HP")):
        if key in cfg:
            stat_parts.append(f"{label} ×{_fmt_num(cfg.pop(key))}")
    for key, label in (("atk_divisore", "ATK"), ("def_divisore", "DEF"), ("agi_divisore", "AGI"), ("hp_divisore", "HP")):
        if key in cfg:
            stat_parts.append(f"{label} /{_fmt_num(cfg.pop(key))}")
    if stat_parts:
        phrases.append("Modifica le statistiche della struttura: " + ", ".join(stat_parts) + ".")

    # Booleani: frase breve e non ridondante.
    if "attacco_diretto" in cfg:
        direct = cfg.pop("attacco_diretto")
        phrases.append("Attacca direttamente l'attaccante." if direct else "Non effettua un attacco diretto.")
    if "rincorsa_disabilitata" in cfg:
        disabled = cfg.pop("rincorsa_disabilitata")
        if disabled:
            phrases.append("Non può effettuare rincorse in questa modalità.")
    if "cura" in cfg:
        healing = cfg.pop("cura")
        if healing:
            phrases.append("Questa modalità usa un effetto di cura invece dell'attacco normale.")

    # Ultimi parametri: usiamo il traduttore v4, ma senza ricreare la frase
    # globale del +10% per livello e senza duplicati.
    for key, value in cfg.items():
        if key == "divisore_livello":
            continue
        phrase = v4._human_param(key, value)
        if phrase and phrase not in phrases:
            phrases.append(phrase)

    return phrases


def _structure_technical(structure_name, mode_name):
    cfg_all = getattr(bilanciamento, "STRUTTURE_CONFIG", {})
    system_cfg = cfg_all.get("generale", {}).get("scaling", {})
    structure_cfg = cfg_all.get(structure_name, {})
    general_cfg = structure_cfg.get("generale", {})
    mode_cfg = structure_cfg.get("modalita", {}).get(mode_name, {})

    # I parametri completi restano nel JSON per audit, compreso lo scaling.
    rows = []
    rows.extend(_prefixed_flatten("sistema.scaling", system_cfg))
    rows.extend(_prefixed_flatten("generale", general_cfg))
    rows.extend(_prefixed_flatten(f"modalita.{mode_name}", mode_cfg))

    phrases = []
    phrases.extend(_describe_effects(structure_name, mode_name, general_cfg))
    phrases.extend(_describe_effects(structure_name, mode_name, mode_cfg))

    # Deduplica mantenendo l'ordine.
    clean = []
    for phrase in phrases:
        phrase = str(phrase or "").strip()
        if phrase and phrase not in clean:
            clean.append(phrase)

    if not clean:
        clean.append("Questa modalità non aggiunge effetti speciali: usa soltanto le statistiche mostrate sotto.")

    return " ".join(clean), rows


def build_data():
    data = v4.build_data()
    for structure in data.get("assault", []):
        for mode in structure.get("modes", []):
            technical, rows = _structure_technical(structure["name"], mode["name"])
            mode["technical"] = technical
            mode["technical_params"] = rows
    data["meta"]["wiki_version"] = 5
    return data


STRUCTURE_DETAIL_JS = r'''function structureDetail(name){const a=find(D.assault,name);if(!a)return missing(name);const first=a.modes[0];return head(a.name,'Struttura d’assalto: scegli una modalità per vedere direttamente cosa fa.','Assalto')+`<div class="detail"><div>${sectionTitle('Modalità')}<div class="modebar" id="modebar">${a.modes.map((m,i)=>`<button class="btn ${i===0?'active':''}" data-mode="${esc(m.name)}">${esc(m.name)}</button>`).join('')}</div>${sectionTitle('Effetto della modalità')}<div id="modeTechnical" class="effect human">${esc(first.technical||'—')}</div>${sectionTitle('Statistiche della modalità')}<div class="levelbox"><b>LV <span id="structLv">0</span></b><input id="structRange" type="range" min="0" max="50" value="0"></div><div id="structStats">${stats(first.levels[0].stats)}</div>${sectionTitle('Statistiche a ogni livello')}<div id="structTable">${statsTable(first.levels)}</div>${a.set_refs.length?sectionTitle('Set collegati / counter')+chipLinks('set',a.set_refs):''}</div><aside class="sidebox">${img('assault',a.name,'🏰')}<div class="card" style="margin-top:12px"><h3>Stats base</h3>${stats(a.base_stats)}${a.resource_value!=null?`<p class="muted">Valore <code>hps</code> nel database: ${esc(a.resource_value)}</p>`:''}</div></aside></div>`}'''


def build_html():
    html = v4.HTML
    html = v3._replace_js_function(html, "structureDetail", "sectionTitle", STRUCTURE_DETAIL_JS)
    html = v3._must_replace(
        html,
        "document.getElementById('modeDesc').textContent=m.description||'—';document.getElementById('modeTechnical').textContent=m.technical||'—';",
        "document.getElementById('modeTechnical').textContent=m.technical||'—';",
        "rimuove descrizione assalto duplicata",
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

    print("Wiki v5 generata:", out)
    print(json.dumps(data["meta"]["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

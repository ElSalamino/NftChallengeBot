#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica registro entità, route Wiki e migrazione dei salvataggi."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI_DIR = ROOT / "wiki"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(WIKI_DIR))

from entity_registry import (  # noqa: E402
    decode_players,
    display_name,
    encode_players,
    legacy_name,
    normalize_entity_names,
    registry,
    resolve_id,
)


ID_RE = re.compile(r"^[a-z][a-z0-9_]*\.[a-z0-9][a-z0-9-]*$")
BAD_MARKERS = ("ZXQ", "⁇", "♪", "√", " @-@ ")
LANGUAGES = ("it", "en", "es")


def wiki_collections(data):
    return {
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


def main():
    errors = []
    records = registry()
    if not records:
        errors.append("registro vuoto")

    by_kind_translation = defaultdict(list)
    global_translation = defaultdict(set)
    for entity_id, record in records.items():
        if not ID_RE.fullmatch(entity_id):
            errors.append(f"ID non valido: {entity_id}")
        names = record.get("names", {})
        for language in LANGUAGES:
            value = names.get(language)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{entity_id}: nome {language} vuoto")
                continue
            if any(marker in value for marker in BAD_MARKERS):
                errors.append(f"{entity_id}/{language}: marcatore anomalo {value!r}")

        kinds = record.get("kinds", []) or [record.get("kind")]
        legacy = record.get("legacy_name")
        for kind in kinds:
            if resolve_id(legacy, kind) != entity_id:
                errors.append(f"round-trip legacy fallito: {kind}/{legacy} -> {entity_id}")
            for language in LANGUAGES:
                shown = display_name(entity_id, language, kind)
                if legacy_name(shown, kind) != legacy:
                    errors.append(f"round-trip {language} fallito: {kind}/{entity_id}/{shown}")
                by_kind_translation[(kind, language, shown.casefold())].append(entity_id)
                global_translation[(language, shown.casefold())].add(legacy)

        leveled = f"{entity_id}@lv0"
        if resolve_id(legacy_name(leveled), record.get("kind")) != leveled:
            errors.append(f"round-trip livello fallito: {entity_id}")

    for (kind, language, shown), ids in by_kind_translation.items():
        distinct = sorted(set(ids))
        if len(distinct) > 1:
            errors.append(
                f"collisione nome {language}/{kind}/{shown!r}: {', '.join(distinct)}"
            )
    for (language, shown), legacy_names in global_translation.items():
        if len(legacy_names) > 1:
            errors.append(
                f"collisione globale {language}/{shown!r}: {', '.join(sorted(legacy_names))}"
            )

    import genera_wiki_v14 as wiki

    wiki.v3.v2.set_names = wiki.v3._valid_set_names
    data = wiki.build_data()
    if data.get("meta", {}).get("wiki_version") != 14:
        errors.append("Wiki non configurata come v14")
    for kind, rows in wiki_collections(data).items():
        for row in rows:
            expected = resolve_id(row.get("name"), kind)
            if not expected or row.get("id") != expected:
                errors.append(f"Wiki senza ID coerente: {kind}/{row.get('name')}")
    html = wiki.build_html()
    if re.search(
        r"location\.hash='(?:boss|location|event|room|structure|marineboss|achievement)/\$\{enc\(",
        html,
    ):
        errors.append("Wiki con collegamenti interni ancora basati sul nome")
    if "chipLinks('item',f.potions_now.ingredients)" not in html:
        errors.append("ingredienti Wiki non collegati alle rispettive schede")

    import liste

    runtime_collections = {
        "item": getattr(liste, "ingredienti", []),
        "pet": getattr(liste, "animaletti", []),
        "weather": getattr(liste, "Metei", []),
        "choice": getattr(liste, "scelte", []),
        "role": ["Nullatenente"],
    }
    for kind, values in runtime_collections.items():
        for value in values:
            if not resolve_id(value, kind):
                errors.append(f"termine runtime senza ID: {kind}/{value}")

    sample = {
        "utente": {
            "da": "Anello dell'occulto",
            "vuole": "Anello perfezionista",
            "location": "Antico deserto",
            "scheda": {
                "arma": "Spada LV0",
                "protezione": "Dono stellare LV4",
                "set": "Macellaio",
                "anello": "Anello dell'occulto",
                "Ap": "Base",
            },
            "pet": "Una bottiglia di birra senza schiuma 🍺",
            "classe": "Nullatenente",
            "zaino": {"Spada LV0": 2, "Melograno": 3, "valore sconosciuto": 1},
            "sacca": {"Pesce Drago": 1, "custom.id": 2},
            "bestiario": {"Drago": "12.3"},
            "boss": {"Carl": 1, "Kraken Nautico": 2},
            "richiesta_pescatore": "Drago",
            "incantamenti": {"Spada LV0": "Critico"},
            "setvisti": ["Macellaio"],
            "obbiettivi": ["A metà strada"],
            "Approcci": {"rivale": "Aggressivo"},
            "arena": {
                "arma": "Spada LV0",
                "protezione": "Dono stellare LV4",
                "set": "Macellaio",
                "anello": "Anello dell'occulto",
                "Ap": "Base",
                "incantamenti": ["Critico"],
            },
            "dungeon": {
                "mostri": ["Arena", "Accolito del dolore", "Boss"],
                "Boss": "Carl",
            },
        }
    }
    encoded = encode_players(sample)
    if encoded == sample or not encoded["utente"]["scheda"]["arma"].startswith("item."):
        errors.append("il salvataggio non viene convertito a ID")
    if not all(str(key).startswith(("boss.", "marine_boss.")) for key in encoded["utente"]["boss"]):
        errors.append("i progressi boss non vengono convertiti a ID")
    if not str(encoded["utente"]["arena"]["arma"]).startswith("item."):
        errors.append("lo stato arena non viene convertito a ID")
    if decode_players(encoded) != sample:
        errors.append("migrazione salvataggio ID -> legacy non reversibile")

    for language in ("en", "es"):
        translated = display_name("item.spada@lv0", language, "item")
        sentence = f"/equip {translated}"
        normalized = normalize_entity_names(sentence, language)
        if normalized != "/equip Spada LV0":
            errors.append(f"normalizzazione comando {language} fallita: {normalized!r}")

    with (ROOT / "locales" / "en.json").open(encoding="utf-8") as stream:
        english = json.load(stream)
    with (ROOT / "locales" / "es.json").open(encoding="utf-8") as stream:
        spanish = json.load(stream)
    expected_labels = {
        "wiki.label.books": ("Books", "Libros"),
        "wiki.label.technical_effect": ("Technical effect", "Efecto técnico"),
        "wiki.label.usables": ("Usable items", "Objetos usables"),
        "wiki.label.ingredient": ("Ingredient", "Ingrediente"),
        "wiki.label.fish": ("Fish", "Pez"),
    }
    for key, (en, es) in expected_labels.items():
        if english.get(key) != en or spanish.get(key) != es:
            errors.append(f"etichetta Wiki non localizzata: {key}")

    if errors:
        print("ERRORI ENTITÀ:")
        for error in errors:
            print("-", error)
        raise SystemExit(1)

    active = sum(not record.get("retired") for record in records.values())
    print(
        f"Entità OK: {active} ID; nomi IT/EN/ES, route Wiki e save ID reversibili"
    )


if __name__ == "__main__":
    main()

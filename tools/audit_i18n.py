#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica copertura e integrità dei cataloghi IT/EN/ES."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from bootstrap_i18n import EXPLICIT, ROOT, collect_phrases, translation_is_safe

sys.path.insert(0, str(ROOT))
from i18n import clear_caches, normalize_input, tr, translate_text  # noqa: E402


PLACEHOLDERS = re.compile(r"\{[^{}]+\}")
LANGUAGES = ("it", "en", "es")


def load_catalog(language: str) -> dict[str, str]:
    with (ROOT / "locales" / f"{language}.json").open(encoding="utf-8") as stream:
        return json.load(stream)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki-dir", type=Path)
    args = parser.parse_args()

    catalogs = {language: load_catalog(language) for language in LANGUAGES}
    entries = {
        language: {key: value for key, value in values.items() if not key.startswith("_")}
        for language, values in catalogs.items()
    }
    errors: list[str] = []

    expected_keys = set(entries["it"])
    for language in LANGUAGES:
        if set(entries[language]) != expected_keys:
            missing = sorted(expected_keys - set(entries[language]))
            extra = sorted(set(entries[language]) - expected_keys)
            errors.append(f"{language}: chiavi mancanti={missing[:5]}, extra={extra[:5]}")
        if catalogs[language].get("_meta", {}).get("language") != language:
            errors.append(f"{language}: metadati lingua errati")

    for key in sorted(expected_keys):
        source = entries["it"][key]
        for language in ("en", "es"):
            target = entries[language].get(key, "")
            if not target:
                errors.append(f"{language}/{key}: traduzione vuota")
                continue
            if not translation_is_safe(source, target):
                errors.append(f"{language}/{key}: traduzione strutturalmente non sicura")

    phrases, _ = collect_phrases(args.wiki_dir)
    indexed_sources = set(entries["it"].values())
    missing_phrases = sorted(phrases - indexed_sources)
    if missing_phrases:
        errors.append(f"frasi senza catalogo={len(missing_phrases)}: {missing_phrases[:8]}")
    for key in EXPLICIT:
        if key not in expected_keys:
            errors.append(f"chiave esplicita mancante: {key}")

    clear_caches()
    if tr("language.choose", "en") == tr("language.choose", "it"):
        errors.append("selettore inglese non tradotto")
    if tr("language.choose", "es") == tr("language.choose", "it"):
        errors.append("selettore spagnolo non tradotto")
    if normalize_input("Language 🌐", "en") != "Lingua 🌐":
        errors.append("round-trip pulsante inglese non valido")
    if normalize_input("Idioma 🌐", "es") != "Lingua 🌐":
        errors.append("round-trip pulsante spagnolo non valido")
    for language in ("en", "es"):
        rendered = translate_text("Mancano 5 secondi!", language)
        if "5" not in rendered or rendered == "Mancano 5 secondi!":
            errors.append(f"{language}: template dinamico countdown non tradotto")
        localized_item = translate_text("Pesce Drago", language)
        if normalize_input(localized_item, language) != "Pesce Drago":
            errors.append(f"{language}: round-trip template dinamico non valido")
    if translate_text("Set del Abitante equipaggiato!", "en") != "Resident set equipped!":
        errors.append("frase scenica set inglese non localizzata")
    if translate_text("Set del Abitante equipaggiato!", "es") != "¡Set de Habitante equipado!":
        errors.append("frase scenica set spagnola non localizzata")

    if errors:
        print("ERRORI I18N:")
        for error in errors:
            print("-", error)
        raise SystemExit(1)

    print(
        f"I18N OK: {len(expected_keys)} frasi × {len(LANGUAGES)} lingue; "
        "placeholder, fallback e input localizzati validi"
    )


if __name__ == "__main__":
    main()

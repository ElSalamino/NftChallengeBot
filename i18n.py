# -*- coding: utf-8 -*-
"""Localizzazione condivisa per Telegram, Wiki e playtest.

Le chiavi di gameplay restano in italiano per compatibilità con i salvataggi.
Questo modulo traduce esclusivamente il livello di presentazione e usa sempre
l'italiano come fallback quando una lingua o una frase non sono disponibili.
"""
from __future__ import annotations

import json
import re
import string
from collections import Counter
from functools import lru_cache
from pathlib import Path

from entity_registry import (
    clear_caches as clear_entity_caches,
    display_name as display_entity_name,
    normalize_entity_names,
    resolve_id as resolve_entity_id,
    translate_entity_names,
)


ROOT = Path(__file__).resolve().parent
LOCALES_DIR = ROOT / "locales"
DEFAULT_LANGUAGE = "it"
SUPPORTED_LANGUAGES = ("it", "en", "es")

_LANGUAGE_ALIASES = {
    "it": "it",
    "ita": "it",
    "italian": "it",
    "italiano": "it",
    "en": "en",
    "eng": "en",
    "english": "en",
    "es": "es",
    "spa": "es",
    "spanish": "es",
    "espanol": "es",
    "español": "es",
}


def normalize_language(language: object, default: str = DEFAULT_LANGUAGE) -> str:
    """Riduce codici Telegram/HTML come ``en-US`` ai tre codici supportati."""
    raw = str(language or "").strip().lower().replace("_", "-")
    if raw in _LANGUAGE_ALIASES:
        return _LANGUAGE_ALIASES[raw]
    base = raw.split("-", 1)[0]
    return _LANGUAGE_ALIASES.get(base, default)


@lru_cache(maxsize=None)
def load_catalog(language: str) -> dict[str, str]:
    language = normalize_language(language)
    path = LOCALES_DIR / f"{language}.json"
    try:
        with path.open(encoding="utf-8") as stream:
            data = json.load(stream)
    except (OSError, ValueError, TypeError):
        if language != DEFAULT_LANGUAGE:
            return load_catalog(DEFAULT_LANGUAGE)
        return {}
    return {str(key): str(value) for key, value in data.items() if not str(key).startswith("_")}


def tr(key: str, language: str = DEFAULT_LANGUAGE, **values: object) -> str:
    """Traduce una chiave esplicita, con fallback italiano e placeholder sicuri."""
    language = normalize_language(language)
    italian = load_catalog(DEFAULT_LANGUAGE)
    text = load_catalog(language).get(key, italian.get(key, key))
    if not values:
        return text
    try:
        return text.format_map(_SafeValues(values))
    except (ValueError, IndexError):
        fallback = italian.get(key, key)
        try:
            return fallback.format_map(_SafeValues(values))
        except (ValueError, IndexError):
            return fallback


class _SafeValues(dict):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


@lru_cache(maxsize=None)
def _source_index(language: str) -> dict[str, str]:
    italian = load_catalog(DEFAULT_LANGUAGE)
    translated = load_catalog(language)
    return {source: translated.get(key, source) for key, source in italian.items()}


def translate_source(source: object, language: str = DEFAULT_LANGUAGE) -> object:
    """Traduce una frase sorgente intera senza interpretarla come ID di gioco."""
    if not isinstance(source, str):
        return source
    language = normalize_language(language)
    if language == DEFAULT_LANGUAGE:
        return source
    return _source_index(language).get(source, source)


def _template_fields(template: str) -> list[str]:
    fields = []
    try:
        parsed = string.Formatter().parse(template)
        for _, field, _, _ in parsed:
            if field is not None:
                fields.append(field)
    except ValueError:
        return []
    return fields


def _compile_template(template: str):
    fields: list[str] = []
    pattern: list[str] = []
    try:
        parsed = string.Formatter().parse(template)
        for literal, field, _, _ in parsed:
            pattern.append(re.escape(literal))
            if field is not None:
                fields.append(field)
                pattern.append(f"(?P<p{len(fields) - 1}>.*?)")
    except ValueError:
        return None
    if not fields:
        return None
    try:
        return re.compile("^" + "".join(pattern) + "$"), fields
    except re.error:
        return None


def _render_template(template: str, values: dict[str, str], language: str) -> str:
    out: list[str] = []
    try:
        for literal, field, _, _ in string.Formatter().parse(template):
            out.append(literal)
            if field is not None:
                out.append(translate_text(values.get(field, ""), language))
    except ValueError:
        return template
    return "".join(out)


@lru_cache(maxsize=None)
def _template_index(language: str):
    if normalize_language(language) == DEFAULT_LANGUAGE:
        return ()
    italian = load_catalog(DEFAULT_LANGUAGE)
    translated = load_catalog(language)
    entries = []
    for key, source in italian.items():
        target = translated.get(key, source)
        compiled = _compile_template(source)
        if compiled is None:
            continue
        regex, fields = compiled
        if Counter(fields) != Counter(_template_fields(target)):
            continue
        entries.append((regex, fields, target))
    # Prima i template più specifici: riduce i match ambigui con placeholder iniziali.
    entries.sort(key=lambda item: len(item[0].pattern), reverse=True)
    return tuple(entries)


@lru_cache(maxsize=None)
def _constant_replacer(language: str):
    language = normalize_language(language)
    if language == DEFAULT_LANGUAGE:
        return None, {}
    pairs = {
        source: target
        for source, target in _source_index(language).items()
        if (
            source != target
            and "{" not in source
            and "}" not in source
            and len(source) >= 8
            and (" " in source or any(char in source for char in ".!?:;,…"))
        )
    }
    if not pairs:
        return None, {}
    # Un'unica regex è sensibilmente più rapida di migliaia di replace consecutivi.
    choices = sorted(pairs, key=len, reverse=True)
    return re.compile("|".join(re.escape(value) for value in choices)), pairs


def _translate_segment(segment: str, language: str) -> str:
    equipped = re.fullmatch(
        r"Set (?:del|della|dell'|dei|degli|delle)\s*(.+?) equipaggiato!",
        segment,
        re.IGNORECASE,
    )
    if equipped:
        entity_id = resolve_entity_id(equipped.group(1), "set")
        if entity_id:
            shown = display_entity_name(entity_id, language, "set")
            if language == "en":
                return f"{shown} set equipped!"
            if language == "es":
                return f"¡Set de {shown} equipado!"

    direct = translate_source(segment, language)
    if direct != segment:
        return str(direct)

    for regex, fields, target in _template_index(language):
        match = regex.fullmatch(segment)
        if not match:
            continue
        values = {field: match.group(f"p{index}") for index, field in enumerate(fields)}
        return _render_template(target, values, language)

    regex, pairs = _constant_replacer(language)
    if regex is not None:
        return regex.sub(lambda match: pairs[match.group(0)], segment)
    return segment


def translate_text(text: object, language: str = DEFAULT_LANGUAGE) -> object:
    """Traduce testo già composto, inclusi i template con valori dinamici.

    La traduzione riga per riga permette di localizzare anche i vecchi messaggi
    costruiti con concatenazioni, senza cambiare le formule o i callback.
    """
    if not isinstance(text, str):
        return text
    language = normalize_language(language)
    if language == DEFAULT_LANGUAGE or not text:
        return text
    parts = text.splitlines(keepends=True)
    translated: list[str] = []
    for part in parts:
        body = part.rstrip("\r\n")
        ending = part[len(body):]
        leading = body[: len(body) - len(body.lstrip())]
        trailing = body[len(body.rstrip()):]
        core_end = len(body) - len(trailing) if trailing else len(body)
        core = body[len(leading):core_end]
        rendered = _translate_segment(core, language)
        translated.append(
            leading + str(translate_entity_names(rendered, language)) + trailing + ending
        )
    return "".join(translated)


@lru_cache(maxsize=None)
def _reverse_index(language: str) -> dict[str, str]:
    language = normalize_language(language)
    if language == DEFAULT_LANGUAGE:
        return {}
    italian = load_catalog(DEFAULT_LANGUAGE)
    translated = load_catalog(language)
    reverse: dict[str, str] = {}
    for key, source in italian.items():
        target = translated.get(key)
        if not target or target == source or "{" in target or "}" in target:
            continue
        # Le risposte brevi coprono pulsanti, opzioni e nomi digitabili.
        if len(target) <= 120 and "\n" not in target:
            reverse.setdefault(target.casefold(), source)
    return reverse


@lru_cache(maxsize=None)
def _reverse_template_index(language: str):
    language = normalize_language(language)
    if language == DEFAULT_LANGUAGE:
        return ()
    italian = load_catalog(DEFAULT_LANGUAGE)
    translated = load_catalog(language)
    entries = []
    for key, source in italian.items():
        target = translated.get(key, source)
        compiled = _compile_template(target)
        if compiled is None:
            continue
        regex, fields = compiled
        if Counter(fields) != Counter(_template_fields(source)):
            continue
        entries.append((regex, fields, source))
    entries.sort(key=lambda item: len(item[0].pattern), reverse=True)
    return tuple(entries)


def normalize_input(text: object, language: str = DEFAULT_LANGUAGE) -> object:
    """Riporta pulsanti/opzioni tradotti alla chiave italiana usata dal runtime."""
    if not isinstance(text, str):
        return text
    language = normalize_language(language)
    text = str(normalize_entity_names(text, language))
    direct = _reverse_index(language).get(text.casefold())
    if direct is not None:
        return direct
    for regex, fields, source in _reverse_template_index(language):
        match = regex.fullmatch(text)
        if not match:
            continue
        values = {field: match.group(f"p{index}") for index, field in enumerate(fields)}
        return _render_template(source, values, DEFAULT_LANGUAGE)
    return text


def clear_caches() -> None:
    """Utile nei test o dopo l'aggiornamento locale dei cataloghi."""
    load_catalog.cache_clear()
    _source_index.cache_clear()
    _template_index.cache_clear()
    _constant_replacer.cache_clear()
    _reverse_index.cache_clear()
    _reverse_template_index.cache_clear()
    clear_entity_caches()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Registro stabile delle entità di gioco e ponte con i nomi storici.

Il runtime originale usa nomi italiani come chiavi. Il registro assegna a ogni
entità un ID immutabile, espone il nome nella lingua scelta e converte i dati
persistiti senza obbligare il motore a cambiare tutto in un solo rilascio.
"""
from __future__ import annotations

import copy
import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
REGISTRY_PATH = ROOT / "entities.json"
SUPPORTED_LANGUAGES = ("it", "en", "es")

KIND_ALIASES = {
    "items": "item",
    "rings": "ring",
    "sets": "set",
    "bosses": "boss",
    "enemies": "enemy",
    "locations": "location",
    "rooms": "room",
    "structures": "structure",
    "assault": "structure",
    "incantations": "incantation",
    "approaches": "approach",
    "nuclei": "nucleus",
    "events": "event",
    "modifiers": "modifier",
    "achievements": "achievement",
    "pets": "pet",
    "weathers": "weather",
    "choices": "choice",
    "roles": "role",
    "marine": "marine_boss",
    "marine-boss": "marine_boss",
    "marine_bosses": "marine_boss",
    "scaglioni": "scaglione",
}

_LEGACY_LEVEL_RE = re.compile(r"^(?P<base>.+?)\s+LV(?P<level>MAX|X|\d+)$", re.IGNORECASE)
_ID_LEVEL_RE = re.compile(r"^(?P<base>[a-z][a-z0-9_]*\.[a-z0-9][a-z0-9-]*)(?:@lv(?P<level>max|x|\d+))?$", re.IGNORECASE)


def normalize_kind(kind: object | None) -> str | None:
    if kind is None:
        return None
    raw = str(kind).strip().lower().replace(" ", "_")
    return KIND_ALIASES.get(raw, raw)


def normalize_language(language: object) -> str:
    raw = str(language or "it").strip().lower().replace("_", "-").split("-", 1)[0]
    return raw if raw in SUPPORTED_LANGUAGES else "it"


@lru_cache(maxsize=1)
def registry() -> dict[str, dict[str, Any]]:
    try:
        with REGISTRY_PATH.open(encoding="utf-8") as stream:
            payload = json.load(stream)
    except (OSError, ValueError, TypeError):
        return {}
    raw = payload.get("entities", payload) if isinstance(payload, dict) else {}
    return {
        str(entity_id): value
        for entity_id, value in raw.items()
        if isinstance(value, dict) and not str(entity_id).startswith("_")
    }


def _record_matches_kind(record: dict[str, Any], kind: str | None) -> bool:
    if kind is None:
        return True
    wanted = normalize_kind(kind)
    kinds = {normalize_kind(value) for value in record.get("kinds", [])}
    primary = normalize_kind(record.get("kind"))
    return wanted == primary or wanted in kinds


@lru_cache(maxsize=1)
def _indexes():
    by_name: dict[str, list[str]] = {}
    by_kind_name: dict[tuple[str, str], str] = {}
    for entity_id, record in registry().items():
        names = record.get("names", {})
        aliases = record.get("aliases", []) if isinstance(record.get("aliases"), list) else []
        variants = {
            record.get("legacy_name"),
            *(names.values() if isinstance(names, dict) else []),
            *aliases,
        }
        kinds = {normalize_kind(record.get("kind")), *(normalize_kind(x) for x in record.get("kinds", []))}
        for value in variants:
            if not isinstance(value, str) or not value.strip():
                continue
            folded = value.strip().casefold()
            by_name.setdefault(folded, []).append(entity_id)
            for kind in kinds:
                if kind:
                    by_kind_name.setdefault((kind, folded), entity_id)
    return by_name, by_kind_name


def split_level(value: object) -> tuple[str, str | None]:
    text = str(value or "").strip()
    match = _ID_LEVEL_RE.fullmatch(text)
    if match:
        level = match.group("level")
        return match.group("base"), level.upper() if level else None
    match = _LEGACY_LEVEL_RE.fullmatch(text)
    if match:
        return match.group("base"), match.group("level").upper()
    return text, None


def _with_level(value: str, level: str | None, *, identifier: bool) -> str:
    if not level:
        return value
    return f"{value}@lv{level.lower()}" if identifier else f"{value} LV{level.upper()}"


def resolve_id(value: object, kind: object | None = None) -> str | None:
    """Restituisce l'ID stabile da ID, nome IT/EN/ES o nome con suffisso LV."""
    base, level = split_level(value)
    records = registry()
    if base in records and _record_matches_kind(records[base], normalize_kind(kind)):
        return _with_level(base, level, identifier=True)

    by_name, by_kind_name = _indexes()
    folded = base.casefold()
    normalized_kind = normalize_kind(kind)
    entity_id = by_kind_name.get((normalized_kind, folded)) if normalized_kind else None
    if entity_id is None:
        matches = list(dict.fromkeys(by_name.get(folded, [])))
        if normalized_kind:
            matches = [item for item in matches if _record_matches_kind(records[item], normalized_kind)]
        if len(matches) == 1:
            entity_id = matches[0]
    return _with_level(entity_id, level, identifier=True) if entity_id else None


def legacy_name(value: object, kind: object | None = None) -> str:
    """Converte un ID o un nome tradotto nel nome italiano atteso dal runtime."""
    text = str(value or "")
    resolved = resolve_id(text, kind)
    if not resolved:
        return text
    entity_id, level = split_level(resolved)
    record = registry().get(entity_id, {})
    italian = str(record.get("legacy_name") or record.get("names", {}).get("it") or text)
    return _with_level(italian, level, identifier=False)


def display_name(value: object, language: object = "it", kind: object | None = None) -> str:
    """Nome localizzato; mantiene LV0/LVX/LVMAX separato dall'identità."""
    text = str(value or "")
    resolved = resolve_id(text, kind)
    if not resolved:
        return text
    entity_id, level = split_level(resolved)
    record = registry().get(entity_id, {})
    names = record.get("names", {})
    language = normalize_language(language)
    shown = str(names.get(language) or names.get("it") or record.get("legacy_name") or text)
    return _with_level(shown, level, identifier=False)


@lru_cache(maxsize=None)
def _entity_replacer(language: str):
    language = normalize_language(language)
    if language == "it":
        return None, {}
    pairs: dict[str, str] = {}
    for record in registry().values():
        source = str(record.get("legacy_name") or record.get("names", {}).get("it") or "")
        target = str(record.get("names", {}).get(language) or source)
        if source and target and source != target:
            pairs.setdefault(source, target)
    if not pairs:
        return None, {}
    choices = sorted(pairs, key=len, reverse=True)
    pattern = re.compile(
        r"(?<![\w.])(?:" + "|".join(re.escape(value) for value in choices) + r")(?![\w-])"
    )
    return pattern, pairs


def translate_entity_names(text: object, language: object = "it") -> object:
    if not isinstance(text, str) or normalize_language(language) == "it":
        return text
    direct = display_name(text, language)
    if direct != text:
        return direct
    pattern, pairs = _entity_replacer(normalize_language(language))
    if pattern is None:
        return text
    return pattern.sub(lambda match: pairs[match.group(0)], text)


@lru_cache(maxsize=None)
def _entity_reverse_replacer(language: str):
    """Indice inverso non ambiguo per nomi localizzati dentro una frase."""
    language = normalize_language(language)
    if language == "it":
        return None, {}
    candidates: dict[str, set[str]] = {}
    spelling: dict[str, str] = {}
    for record in registry().values():
        source = str(record.get("legacy_name") or record.get("names", {}).get("it") or "")
        target = str(record.get("names", {}).get(language) or source)
        if not source or not target or source == target:
            continue
        folded = target.casefold()
        candidates.setdefault(folded, set()).add(source)
        spelling.setdefault(folded, target)
    pairs = {
        spelling[folded]: next(iter(sources))
        for folded, sources in candidates.items()
        if len(sources) == 1
    }
    if not pairs:
        return None, {}
    choices = sorted(pairs, key=len, reverse=True)
    pattern = re.compile(
        r"(?<![\w.])(?:" + "|".join(re.escape(value) for value in choices) + r")(?![\w-])",
        re.IGNORECASE,
    )
    return pattern, {key.casefold(): value for key, value in pairs.items()}


def normalize_entity_names(text: object, language: object = "it") -> object:
    """Riporta a italiano i nomi localizzati, anche se inclusi in comandi/testi."""
    if not isinstance(text, str):
        return text
    language = normalize_language(language)
    direct = resolve_id(text)
    if direct:
        return legacy_name(direct)
    pattern, pairs = _entity_reverse_replacer(language)
    if pattern is None:
        return text
    return pattern.sub(lambda match: pairs[match.group(0).casefold()], text)


def normalize_entity_input(
    text: object,
    kind: object | None = None,
    language: object = "it",
) -> object:
    if not isinstance(text, str):
        return text
    resolved = resolve_id(text, kind)
    if resolved:
        return legacy_name(resolved, kind)
    return normalize_entity_names(text, language)


_PLAYER_DIRECT_FIELDS = {
    "da": "item",
    "vuole": "item",
    "location": "location",
    "pet": "pet",
    "classe": "role",
}
_SHEET_FIELDS = {
    "arma": "item",
    "protezione": "item",
    "set": "set",
    "anello": "ring",
    "Ap": "approach",
}


def _convert_ref(value: object, kind: str, encode: bool):
    if value is None:
        return None
    if not isinstance(value, str):
        return value
    if encode:
        return resolve_id(value, kind) or value
    return legacy_name(value, kind)


def _convert_mixed_ref(value: object, kinds: tuple[str, ...], encode: bool):
    if value is None or not isinstance(value, str):
        return value
    if not encode:
        return legacy_name(value)
    for kind in kinds:
        entity_id = resolve_id(value, kind)
        if entity_id:
            return entity_id
    return value


def _convert_map_keys(values: object, kind: str, encode: bool):
    if not isinstance(values, dict):
        return values
    converted = {}
    for key, value in values.items():
        new_key = _convert_ref(key, kind, encode)
        converted[new_key] = converted.get(new_key, 0) + value if isinstance(value, (int, float)) else value
    return converted


def _convert_mixed_map_keys(values: object, kinds: tuple[str, ...], encode: bool):
    if not isinstance(values, dict):
        return values
    converted = {}
    for key, value in values.items():
        new_key = _convert_mixed_ref(key, kinds, encode)
        converted[new_key] = converted.get(new_key, 0) + value if isinstance(value, (int, float)) else value
    return converted


def _convert_fish_bag(values: object, encode: bool):
    if not isinstance(values, dict):
        return values
    converted = {}
    for key, value in values.items():
        if encode and isinstance(key, str) and key.startswith("Pesce "):
            entity_id = resolve_id(key.removeprefix("Pesce "), "item")
            new_key = entity_id or key
        elif (
            not encode
            and isinstance(key, str)
            and _ID_LEVEL_RE.fullmatch(key)
            and resolve_id(key, "item")
        ):
            new_key = "Pesce " + legacy_name(key, "item")
        else:
            new_key = key
        converted[new_key] = converted.get(new_key, 0) + value if isinstance(value, (int, float)) else value
    return converted


def _convert_player_record(record: dict[str, Any], encode: bool) -> None:
    for field, kind in _PLAYER_DIRECT_FIELDS.items():
        if field in record:
            record[field] = _convert_ref(record[field], kind, encode)

    sheet = record.get("scheda")
    if isinstance(sheet, dict):
        for field, kind in _SHEET_FIELDS.items():
            if field in sheet:
                sheet[field] = _convert_ref(sheet[field], kind, encode)

    inventory = record.get("zaino")
    if isinstance(inventory, dict):
        record["zaino"] = _convert_map_keys(inventory, "item", encode)

    if isinstance(record.get("sacca"), dict):
        record["sacca"] = _convert_fish_bag(record["sacca"], encode)
    if isinstance(record.get("bestiario"), dict):
        record["bestiario"] = _convert_map_keys(record["bestiario"], "item", encode)
    if isinstance(record.get("boss"), dict):
        record["boss"] = _convert_mixed_map_keys(
            record["boss"], ("boss", "marine_boss"), encode
        )
    if record.get("richiesta_pescatore") is not None:
        record["richiesta_pescatore"] = _convert_ref(
            record["richiesta_pescatore"], "item", encode
        )

    enchantments = record.get("incantamenti")
    if isinstance(enchantments, dict):
        record["incantamenti"] = {
            _convert_ref(key, "item", encode): _convert_ref(value, "incantation", encode)
            for key, value in enchantments.items()
        }

    if isinstance(record.get("setvisti"), list):
        record["setvisti"] = [_convert_ref(value, "set", encode) for value in record["setvisti"]]
    if isinstance(record.get("obbiettivi"), list):
        record["obbiettivi"] = [
            _convert_ref(value, "achievement", encode) for value in record["obbiettivi"]
        ]
    if isinstance(record.get("Approcci"), dict):
        record["Approcci"] = {
            key: _convert_ref(value, "approach", encode)
            for key, value in record["Approcci"].items()
        }

    arena = record.get("arena")
    if isinstance(arena, dict):
        for field, kind in _SHEET_FIELDS.items():
            if field in arena:
                arena[field] = _convert_ref(arena[field], kind, encode)
        if isinstance(arena.get("incantamenti"), list):
            arena["incantamenti"] = [
                _convert_ref(value, "incantation", encode)
                for value in arena["incantamenti"]
            ]

    dungeon = record.get("dungeon")
    if isinstance(dungeon, dict):
        if isinstance(dungeon.get("mostri"), list):
            dungeon["mostri"] = [
                _convert_mixed_ref(value, ("room", "enemy"), encode)
                for value in dungeon["mostri"]
            ]
        if dungeon.get("Boss") is not None:
            dungeon["Boss"] = _convert_ref(dungeon["Boss"], "boss", encode)


def convert_players(players: object, *, encode: bool) -> object:
    """Copia e converte soltanto i campi entità noti del database giocatori."""
    converted = copy.deepcopy(players)
    if not isinstance(converted, dict):
        return converted
    for record in converted.values():
        if isinstance(record, dict):
            _convert_player_record(record, encode)
    return converted


def encode_players(players: object) -> object:
    return convert_players(players, encode=True)


def decode_players(players: object) -> object:
    return convert_players(players, encode=False)


def clear_caches() -> None:
    registry.cache_clear()
    _indexes.cache_clear()
    _entity_replacer.cache_clear()
    _entity_reverse_replacer.cache_clear()

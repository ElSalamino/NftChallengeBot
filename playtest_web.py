#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NFT Single Player Playtest.

Web app locale, senza database e senza dipendenze web esterne.
Usa direttamente ``liste.py``/``bilanciamento.py`` e, quando l'ambiente del bot
ha Pyrogram/APScheduler disponibili, richiama il vero ``nft.turno`` per le sfide.

Avvio:
    python playtest_web.py

Poi apre automaticamente http://127.0.0.1:8765
"""
from __future__ import annotations

import argparse
import copy
import json
import random
import sys
import threading
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
PLAYTEST_DIR = ROOT / "playtest"
STATS = ("hp", "atk", "def", "agi")
RAW_WEIGHTS = {"hp": 1, "atk": 4, "def": 4, "agi": 20}

import liste
from dungeon_extra import (
    podio_applica_penalita,
    podio_livello_premio,
    podio_penalita_gloria,
    podio_probabilita_pct,
    scegli_nemici_imboscata,
)

_RUNTIME = None
_RUNTIME_ERROR = None
_WIKI_DATA = None


def base_item(name):
    return str(name or "").split(" LV", 1)[0]


def raw_score(stats):
    return int(round(sum(float((stats or {}).get(k, 0) or 0) * RAW_WEIGHTS[k] for k in STATS)))


def _runtime():
    """Carica il runtime Telegram solo quando serve una sfida 1:1."""
    global _RUNTIME, _RUNTIME_ERROR
    if _RUNTIME is not None:
        return _RUNTIME
    if _RUNTIME_ERROR is not None:
        return None
    try:
        import nft as runtime
        _RUNTIME = runtime
        return runtime
    except Exception as exc:  # l'app resta utilizzabile anche senza dipendenze bot
        _RUNTIME_ERROR = f"{type(exc).__name__}: {exc}"
        return None


def runtime_status():
    runtime = _runtime()
    return {
        "exact_runtime": runtime is not None and callable(getattr(runtime, "turno", None)),
        "runtime_error": _RUNTIME_ERROR,
        "mode": "runtime nft.turno" if runtime is not None else "fallback statistico",
    }


def _wiki_data():
    global _WIKI_DATA
    if _WIKI_DATA is not None:
        return _WIKI_DATA
    wiki_dir = ROOT / "wiki"
    if str(wiki_dir) not in sys.path:
        sys.path.insert(0, str(wiki_dir))
    import genera_wiki_v13 as wiki
    wiki.v3.v2.set_names = wiki.v3._valid_set_names
    _WIKI_DATA = wiki.build_data()
    return _WIKI_DATA


def equipment_catalog():
    rows = []
    for kind, collection in (
        ("Arma", getattr(liste, "armi", {})),
        ("Arma", getattr(liste, "armiextra", {})),
        ("Protezione", getattr(liste, "protezioni", {})),
        ("Protezione", getattr(liste, "protezioniextra", {})),
    ):
        for full_name, data in collection.items():
            rows.append({
                "name": str(full_name),
                "base": base_item(full_name),
                "kind": kind,
                "stats": {k: data.get(k, 0) for k in STATS},
                "raw_score": raw_score(data),
            })
    rows.sort(key=lambda x: (x["kind"], x["base"].lower(), x["name"].lower()))
    return rows


def catalog():
    wiki = _wiki_data()
    return {
        "equipment": equipment_catalog(),
        "rings": sorted([str(x) for x in getattr(liste, "anelli", {})], key=str.lower),
        "approaches": [
            {"name": str(name), "stats": {k: cfg.get(k, 1) for k in STATS}}
            for name, cfg in getattr(liste, "Approcci", {}).items()
        ],
        "sets": [
            {
                "name": str(name),
                "components": [base_item(x) for x in (components or [])],
                "bonus": {k: getattr(liste, "bonus", {}).get(name, {}).get(k, 0) for k in STATS},
            }
            for name, components in getattr(liste, "classi", {}).items()
            if name is not None
        ],
        "enemies": sorted([str(x) for x in getattr(liste, "nemici", {})], key=str.lower),
        "bosses": sorted([str(x) for x in getattr(liste, "Boss", {})], key=str.lower),
        "marine_bosses": sorted([str(x) for x in getattr(liste, "Nautici", {})], key=str.lower),
        "locations": [str(x) for x in getattr(liste, "location", [])],
        "rooms": [str(x) for x in getattr(liste, "stanze", [])],
        "counts": wiki.get("meta", {}).get("counts", {}),
        "raw_formula": "HP ×1 · ATK ×4 · DEF ×4 · AGI ×20",
    }


def _find_equipment(full_name):
    if not full_name:
        return None
    for collection in (
        getattr(liste, "armi", {}),
        getattr(liste, "armiextra", {}),
        getattr(liste, "protezioni", {}),
        getattr(liste, "protezioniextra", {}),
    ):
        if full_name in collection:
            return collection[full_name]
    return None


def detect_set(weapon, protection):
    equipped = {base_item(weapon), base_item(protection)} - {""}
    matches = []
    for set_name, components in getattr(liste, "classi", {}).items():
        if set_name is None:
            continue
        needed = {base_item(x) for x in (components or [])}
        if needed and needed.issubset(equipped):
            matches.append((len(needed), str(set_name)))
    if not matches:
        return None
    matches.sort(key=lambda x: (-x[0], x[1].lower()))
    return matches[0][1]


def build_fighter(config):
    config = config or {}
    stats = {
        "hp": float(config.get("hp", 1000) or 0),
        "atk": float(config.get("atk", 100) or 0),
        "def": float(config.get("def", 100) or 0),
        "agi": float(config.get("agi", 50) or 0),
    }
    weapon = config.get("weapon") or None
    protection = config.get("protection") or None
    for selected in (weapon, protection):
        item = _find_equipment(selected)
        if item:
            for stat in STATS:
                stats[stat] += float(item.get(stat, 0) or 0)

    set_name = detect_set(weapon, protection)
    if set_name:
        set_bonus = getattr(liste, "bonus", {}).get(set_name, {})
        for stat in STATS:
            stats[stat] += float(set_bonus.get(stat, 0) or 0)

    approach = config.get("approach") or "Base"
    app_cfg = getattr(liste, "Approcci", {}).get(approach, getattr(liste, "Approcci", {}).get("Base", {}))
    for stat in STATS:
        stats[stat] = round(stats[stat] * float(app_cfg.get(stat, 1) or 1), 4)

    incantamenti = config.get("incantamenti") or []
    if isinstance(incantamenti, str):
        incantamenti = [x.strip() for x in incantamenti.split(",") if x.strip()]

    fighter = {
        "Nome": str(config.get("name") or "Playtester"),
        **stats,
        "set": set_name,
        "anello": config.get("ring") or None,
        "Ap": approach,
        "arma": weapon,
        "protezione": protection,
        "incantamenti": list(incantamenti),
        "boost": {"sfida": {}, "assalto": {}, "dungeon": {}},
        "schivato": False,
        "fatto": 0,
    }
    fighter["raw_score"] = raw_score(fighter)
    return fighter


def _opponent_source(kind, name):
    if kind == "boss":
        return getattr(liste, "Boss", {}).get(name)
    if kind == "marine":
        return getattr(liste, "Nautici", {}).get(name)
    return getattr(liste, "nemici", {}).get(name)


def build_opponent(kind, name, level=0):
    src = _opponent_source(kind, name)
    if not isinstance(src, dict):
        raise ValueError(f"Avversario non trovato: {kind}/{name}")
    fighter = copy.deepcopy(src)
    fighter.setdefault("Nome", name)
    fighter.setdefault("set", None)
    fighter.setdefault("anello", None)
    fighter.setdefault("Ap", "Base")
    fighter.setdefault("schivato", False)
    fighter.setdefault("boost", {"sfida": {}, "assalto": {}, "dungeon": {}})
    fighter.setdefault("incantamenti", [])
    fighter.setdefault("arma", None)
    fighter.setdefault("protezione", None)
    fighter.setdefault("fatto", 0)
    for stat in STATS:
        fighter[stat] = float(fighter.get(stat, 0) or 0)

    if kind == "boss" and int(level or 0) > 0:
        # Stesso scaling esposto dalla Wiki/runtime bossata: base × (1 + LV / 12).
        factor = 1 + int(level) / 12
        for stat in STATS:
            fighter[stat] = round(fighter[stat] * factor)
    fighter["raw_score"] = raw_score(fighter)
    fighter["_playtest_kind"] = kind
    fighter["_playtest_level"] = int(level or 0)
    return fighter


def _fallback_attack(attacker, defender):
    """Fallback trasparente: serve solo se nft.py non è importabile."""
    a_agi = float(attacker.get("agi", 0) or 0)
    d_agi = float(defender.get("agi", 0) or 0)
    hit = max(0.10, min(0.95, 0.72 + (a_agi - d_agi) / 500.0))
    if random.random() > hit:
        return f"{attacker['Nome']} manca {defender['Nome']} (fallback)."
    atk = max(0.0, float(attacker.get("atk", 0) or 0))
    defense = max(0.0, float(defender.get("def", 0) or 0))
    damage = max(1, round(atk * (160.0 / (160.0 + defense)) * random.uniform(0.85, 1.15)))
    defender["hp"] -= damage
    return f"{attacker['Nome']} infligge {damage} danni a {defender['Nome']} (fallback)."


def _exact_attack(attacker, defender):
    runtime = _runtime()
    if runtime is None or not callable(getattr(runtime, "turno", None)):
        raise RuntimeError(_RUNTIME_ERROR or "nft.turno non disponibile")
    result = runtime.turno(attacker, defender)
    return str(result or "").strip()


def start_fight(payload):
    player = build_fighter(payload.get("player") or {})
    enemy = build_opponent(
        payload.get("target_kind") or "enemy",
        payload.get("target_name") or "",
        payload.get("target_level") or 0,
    )
    log = []
    runtime = _runtime()
    if runtime is not None:
        try:
            intro = getattr(runtime, "_applica_valvola_inizio_sfida", lambda x: "")(player)
            if intro:
                log.append(str(intro).strip())
        except Exception:
            pass
    return {
        "player": player,
        "enemy": enemy,
        "round": 0,
        "winner": None,
        "log": log,
        "engine": runtime_status(),
    }


def fight_round(payload):
    state = copy.deepcopy(payload.get("state") or {})
    player = state.get("player") or {}
    enemy = state.get("enemy") or {}
    if state.get("winner"):
        return state
    state["round"] = int(state.get("round", 0)) + 1
    lines = [f"— Turno {state['round']} —"]

    exact = runtime_status()["exact_runtime"]
    try:
        lines.append(_exact_attack(player, enemy) if exact else _fallback_attack(player, enemy))
    except Exception as exc:
        exact = False
        lines.append(f"Runtime 1:1 non riuscito: {type(exc).__name__}: {exc}")
        lines.append(_fallback_attack(player, enemy))

    if float(enemy.get("hp", 0) or 0) <= 0:
        state["winner"] = "player"
    else:
        try:
            lines.append(_exact_attack(enemy, player) if exact else _fallback_attack(enemy, player))
        except Exception as exc:
            exact = False
            lines.append(f"Runtime 1:1 nemico non riuscito: {type(exc).__name__}: {exc}")
            lines.append(_fallback_attack(enemy, player))
        if float(player.get("hp", 0) or 0) <= 0:
            state["winner"] = "enemy"

    state["player"] = player
    state["enemy"] = enemy
    state.setdefault("log", []).extend([x for x in lines if x])
    state["engine"] = runtime_status() | {"round_exact": exact}
    return state


def dungeon_room(payload):
    rooms = list(getattr(liste, "stanze", []))
    room = random.choice(rooms)
    wiki_rooms = {x.get("name"): x for x in _wiki_data().get("dungeon", {}).get("rooms", [])}
    result = {"room": room, "data": wiki_rooms.get(room, {})}

    # La nuova imboscata è realmente testabile qui: 0,5%, 2 mostri fuori zona.
    location = payload.get("location")
    proc = random.random() < 0.005
    result["ambush"] = None
    if proc:
        local = list(getattr(liste, "casa_nemici", {}).get(location, []))
        all_enemies = list(getattr(liste, "nemici", {}))
        picked = scegli_nemici_imboscata(all_enemies, local, 2, random)
        result["ambush"] = {
            "message": "Mentre giravi per il dungeon un gruppo di loschi figuri si avvicina, è un imboscata!",
            "enemies": picked,
        }
    return result


def podium_try(payload):
    total = max(1, int(payload.get("total_achievements") or len(getattr(liste, "descri", {})) or 1))
    done = max(0, int(payload.get("achievements") or 0))
    pos = int(payload.get("position") or 1)
    glory = max(0, int(payload.get("glory") or 0))
    chance = podio_probabilita_pct(done, total, pos)
    won = random.random() < chance / 100
    reward_level = podio_livello_premio(pos)
    loss = 0
    new_glory = glory
    if not won:
        penalty = podio_penalita_gloria(pos)
        new_glory, loss = podio_applica_penalita(glory, penalty)
    return {
        "won": won,
        "chance_pct": chance,
        "reward_level": reward_level if won else None,
        "glory_before": glory,
        "glory_after": new_glory,
        "glory_lost": loss,
    }


def fishing_try(payload):
    location = payload.get("location")
    power = max(1, int(payload.get("power") or 1))
    pool = list(getattr(liste, "pesciame", {}).get(location, []))
    if not pool:
        raise ValueError(f"Nessun pool pesca per {location}")
    max_index = min(power, len(pool) - 1)
    index = random.randint(0, max_index)
    species = pool[index]
    return {
        "location": location,
        "power": power,
        "max_unlocked_index": max_index,
        "index": index,
        "species": species,
        "item_name": f"Pesce {species}",
        "note": "Selezione specie secondo il pool corrente; peso/record verranno agganciati al runtime nel prossimo passaggio.",
    }


def api_result(path, payload):
    if path == "/api/fighter":
        return build_fighter(payload)
    if path == "/api/fight/start":
        return start_fight(payload)
    if path == "/api/fight/round":
        return fight_round(payload)
    if path == "/api/dungeon/room":
        return dungeon_room(payload)
    if path == "/api/dungeon/podium":
        return podium_try(payload)
    if path == "/api/fishing":
        return fishing_try(payload)
    raise KeyError(path)


class Handler(BaseHTTPRequestHandler):
    server_version = "NFTPlaytest/1.0"

    def _json(self, obj, status=200):
        data = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _file(self, path, content_type):
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlparse(self.path).path
        try:
            if path in ("/", "/index.html"):
                return self._file(PLAYTEST_DIR / "index.html", "text/html; charset=utf-8")
            if path == "/assets/i18n.js":
                return self._file(ROOT / "i18n_web.js", "text/javascript; charset=utf-8")
            if path in {f"/locales/{language}.json" for language in ("it", "en", "es")}:
                return self._file(ROOT / path.lstrip("/"), "application/json; charset=utf-8")
            if path == "/api/status":
                return self._json(runtime_status())
            if path == "/api/catalog":
                return self._json(catalog())
            self.send_error(404)
        except Exception as exc:
            self._json({"error": f"{type(exc).__name__}: {exc}"}, 500)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            length = int(self.headers.get("Content-Length", "0") or 0)
            body = self.rfile.read(length) if length else b"{}"
            payload = json.loads(body.decode("utf-8") or "{}")
            return self._json(api_result(path, payload))
        except KeyError:
            self._json({"error": "Endpoint non trovato"}, 404)
        except Exception as exc:
            self._json({
                "error": f"{type(exc).__name__}: {exc}",
                "trace": traceback.format_exc(limit=5),
            }, 500)

    def log_message(self, fmt, *args):
        print(f"[playtest] {self.address_string()} - {fmt % args}")


def self_test():
    assert (ROOT / "i18n_web.js").exists()
    assert all((ROOT / "locales" / f"{language}.json").exists() for language in ("it", "en", "es"))
    c = catalog()
    assert c["equipment"] and c["approaches"] and c["enemies"] and c["bosses"]
    p = build_fighter({"name": "Test", "hp": 1000, "atk": 100, "def": 100, "agi": 50, "approach": "Base"})
    assert p["Nome"] == "Test" and p["hp"] > 0
    target = build_opponent("enemy", c["enemies"][0], 0)
    state = {"player": p, "enemy": target, "round": 0, "winner": None, "log": []}
    # Forza il fallback nel test strutturale: verifica che la web app funzioni anche senza Telegram.
    _fallback_attack(state["player"], state["enemy"])
    fish_locations = [x for x in c["locations"] if x in getattr(liste, "pesciame", {})]
    if fish_locations:
        assert fishing_try({"location": fish_locations[0], "power": 1})["species"]
    assert podium_try({"achievements": 52, "total_achievements": 52, "position": 1, "glory": 20})["chance_pct"] == 100
    print("Playtest web: self-test OK")
    print(json.dumps({"runtime": runtime_status(), "counts": c["counts"]}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="NFT Single Player Playtest Web App")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    if not (PLAYTEST_DIR / "index.html").exists():
        raise SystemExit("Manca playtest/index.html")
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    url = f"http://{args.host}:{args.port}/"
    print(f"NFT Single Player Playtest: {url}")
    print("Il salvataggio del personaggio resta nel localStorage del browser.")
    if not args.no_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nPlaytest chiuso.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

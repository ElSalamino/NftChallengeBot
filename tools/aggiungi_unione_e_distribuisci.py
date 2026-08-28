# -*- coding: utf-8 -*-
import ast
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parents[1]

SPELL = "Unione dello spirito"
BOOK = "Fumetto hot degli anni 70"
LORE = "Unisci il tuo spirito a quello dei compagni e trasforma il gruppo in una sola forza."
NEW_RINGS = [
    "Polimerizzazione",
    'Valvola da 4"',
    "Roulette russa",
    "Roulette tibetana",
    "Sasso rotolante",
    "WuWuWuuurm",
    "Dance Dance Revolution",
    "GDR semplificato",
]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def write(name, text):
    (ROOT / name).write_text(text, encoding="utf-8")


def find_assign(tree, name):
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return node
    raise AssertionError(f"Assegnazione {name!r} non trovata")


def byte_line_starts(source):
    raw = source.encode("utf-8")
    starts = [0]
    for i, b in enumerate(raw):
        if b == 10:
            starts.append(i + 1)
    return raw, starts


def insert_before_close(source, node, payload):
    raw, starts = byte_line_starts(source)
    pos = starts[node.end_lineno - 1] + node.end_col_offset - 1
    return (raw[:pos] + payload.encode("utf-8") + raw[pos:]).decode("utf-8")


def insert_many_before_closes(source, inserts):
    raw, starts = byte_line_starts(source)
    edits = []
    for node, payload in inserts:
        pos = starts[node.end_lineno - 1] + node.end_col_offset - 1
        edits.append((pos, payload.encode("utf-8")))
    for pos, payload in sorted(edits, reverse=True):
        raw = raw[:pos] + payload + raw[pos:]
    return raw.decode("utf-8")


# ------------------------------------------------------------
# bilanciamento.py: nuovo incantesimo
# ------------------------------------------------------------
bil = read("bilanciamento.py")
if f'    "{SPELL}":' not in bil:
    anchor = "\n}\n\n\n# Effetti temporanei non legati agli incantesimi."
    assert anchor in bil
    block = (
        f'    "{SPELL}": {{\n'
        '        "assalto": {\n'
        '            "unione": {\n'
        '                "proc": 100,\n'
        '                "percento_stat": 20,\n'
        '                "stats": ["atk", "def", "agi"],\n'
        '            }\n'
        '        },\n'
        '    },\n\n'
    )
    bil = bil.replace(anchor, "\n" + block + "}\n\n\n# Effetti temporanei non legati agli incantesimi.", 1)
write("bilanciamento.py", bil)


# ------------------------------------------------------------
# frasi_incantesimi.py
# ------------------------------------------------------------
frasi = read("frasi_incantesimi.py")
if f'    "{SPELL}":' not in frasi:
    anchor = "\n\n}"
    assert anchor in frasi
    frase = (
        f'    "{SPELL}": "ASSALTO — se possiedi Unione dello spirito, ogni altro membro del clan che possiede lo stesso incantesimo ti cede il '
        '{assalto.unione.percento_stat:pct} del proprio ATK, DEF e AGI all\'inizio dell\'assalto. I contributi dei diversi compagni si sommano.",\n'
    )
    frasi = frasi.replace(anchor, "\n" + frase + "\n}", 1)
write("frasi_incantesimi.py", frasi)


# ------------------------------------------------------------
# liste.py: libro, distribuzione libro e distribuzione anelli
# ------------------------------------------------------------
liste_src = read("liste.py")
tree = ast.parse(liste_src)

# Aggiunge il libro rispettando automaticamente la struttura attuale di `libri`.
libri_node = find_assign(tree, "libri")
libri_data = ast.literal_eval(libri_node.value)

if BOOK not in libri_data and SPELL not in libri_data:
    if "Manuale di meccanica pt 3" in libri_data:
        # Forma: libro -> dati incantesimo
        sample = libri_data["Manuale di meccanica pt 3"]
        if isinstance(sample, str):
            new_value = SPELL
        elif isinstance(sample, list):
            new_value = list(sample)
            replaced = False
            for i, value in enumerate(new_value):
                if value == "Caricato":
                    new_value[i] = SPELL
                    replaced = True
            for i, value in enumerate(new_value):
                if isinstance(value, str) and value not in (SPELL, BOOK) and (replaced or len(new_value) > 1):
                    new_value[i] = LORE
            if not replaced and new_value:
                new_value[0] = SPELL
        elif isinstance(sample, tuple):
            temp = list(sample)
            replaced = False
            for i, value in enumerate(temp):
                if value == "Caricato":
                    temp[i] = SPELL
                    replaced = True
            for i, value in enumerate(temp):
                if isinstance(value, str) and value not in (SPELL, BOOK) and (replaced or len(temp) > 1):
                    temp[i] = LORE
            new_value = tuple(temp)
        elif isinstance(sample, dict):
            new_value = dict(sample)
            for key, value in list(new_value.items()):
                if value == "Caricato":
                    new_value[key] = SPELL
                elif str(key).lower() in {"descrizione", "description", "lore", "desc"}:
                    new_value[key] = LORE
        else:
            raise AssertionError(f"Formato libri non gestito: {type(sample)}")
        payload = f"    {BOOK!r}: {new_value!r},\n"
    elif "Caricato" in libri_data:
        # Forma: incantesimo -> dati libro
        sample = libri_data["Caricato"]
        if isinstance(sample, str):
            new_value = BOOK
        elif isinstance(sample, list):
            new_value = [BOOK if x == "Manuale di meccanica pt 3" else x for x in sample]
            for i, value in enumerate(new_value):
                if isinstance(value, str) and value != BOOK:
                    new_value[i] = LORE
        elif isinstance(sample, tuple):
            temp = [BOOK if x == "Manuale di meccanica pt 3" else x for x in sample]
            for i, value in enumerate(temp):
                if isinstance(value, str) and value != BOOK:
                    temp[i] = LORE
            new_value = tuple(temp)
        elif isinstance(sample, dict):
            new_value = dict(sample)
            for key, value in list(new_value.items()):
                if value == "Manuale di meccanica pt 3":
                    new_value[key] = BOOK
                elif str(key).lower() in {"descrizione", "description", "lore", "desc"}:
                    new_value[key] = LORE
        else:
            raise AssertionError(f"Formato libri non gestito: {type(sample)}")
        payload = f"    {SPELL!r}: {new_value!r},\n"
    else:
        raise AssertionError("Non trovo Caricato/Manuale di meccanica pt 3 per dedurre il formato di libri")

    liste_src = insert_before_close(liste_src, libri_node.value, payload)

# Rianalizza dopo l'inserimento del libro.
tree = ast.parse(liste_src)

# Aggiunge il nuovo libro a ogni modalità Arena che già distribuisce i libri standard.
arenamod_node = find_assign(tree, "arenamod")
assert isinstance(arenamod_node.value, ast.Dict)
arena_inserts = []
for key_node, value_node in zip(arenamod_node.value.keys, arenamod_node.value.values):
    if not isinstance(key_node, ast.Constant) or not isinstance(value_node, ast.List):
        continue
    values = ast.literal_eval(value_node)
    if "Libro del bene e del male" in values and BOOK not in values:
        arena_inserts.append((value_node, f", {BOOK!r}"))
if not arena_inserts:
    # Può essere idempotente se il libro era già stato inserito.
    arena_data = ast.literal_eval(arenamod_node.value)
    assert any(BOOK in values for values in arena_data.values() if isinstance(values, list))
else:
    liste_src = insert_many_before_closes(liste_src, arena_inserts)

# Rianalizza prima di distribuire gli anelli.
tree = ast.parse(liste_src)
pool_node = find_assign(tree, "pool")
assert isinstance(pool_node.value, ast.Dict)
pool_data = ast.literal_eval(pool_node.value)
zone = list(pool_data.keys())
assert len(zone) >= len(NEW_RINGS)

# Seed fisso: estrazione casuale riproducibile e 8 zone distinte.
rng = random.Random(1970)
zone_scelte = rng.sample(zone, len(NEW_RINGS))
distribuzione = dict(zip(NEW_RINGS, zone_scelte))

# Se lo script viene rilanciato, non duplica gli anelli già distribuiti.
already = {}
for ring in NEW_RINGS:
    for zona, items in pool_data.items():
        if ring in items:
            already[ring] = zona
            break

pool_inserts = []
for key_node, value_node in zip(pool_node.value.keys, pool_node.value.values):
    if not isinstance(key_node, ast.Constant) or not isinstance(value_node, ast.List):
        continue
    zona = key_node.value
    rings_here = [ring for ring, target in distribuzione.items() if target == zona and ring not in already]
    if rings_here:
        pool_inserts.append((value_node, "".join(f", {ring!r}" for ring in rings_here)))

if pool_inserts:
    liste_src = insert_many_before_closes(liste_src, pool_inserts)

write("liste.py", liste_src)


# ------------------------------------------------------------
# nft.py: applicazione Unione dello spirito durante l'assalto
# ------------------------------------------------------------
nft = read("nft.py")
if 'incantesimo_cfg("Unione dello spirito", "assalto", "unione")' not in nft:
    anchor = '            if aniel in PROC_ANELLI and "aura" in PROC_ANELLI[aniel].get("assalto", {}):\n'
    assert anchor in nft
    block = (
        '            if (\n'
        '                "Unione dello spirito" in player.get("incantamenti", [])\n'
        '                and pl != nome\n'
        '                and "Unione dello spirito" in get_ench(playerg[pl])\n'
        '                and incantesimo_ok(random.random(), "Unione dello spirito", "assalto", "unione")\n'
        '            ):\n'
        '                cfg_unione = incantesimo_cfg("Unione dello spirito", "assalto", "unione")\n'
        '                bonus_unione = {}\n'
        '                for stat_unione in cfg_unione["stats"]:\n'
        '                    valore_unione = scheda_membro.get(stat_unione, 0) * cfg_unione["percento_stat"] / 100\n'
        '                    player[stat_unione] += valore_unione\n'
        '                    bonus_unione[stat_unione] = valore_unione\n'
        '                text += (\n'
        '                    f"Lo spirito di {pl} si unisce al tuo, dandoti "\n'
        '                    f"{_numero_placeholder_tecnico(bonus_unione[\'atk\'])} atk "\n'
        '                    f"{_numero_placeholder_tecnico(bonus_unione[\'def\'])} def e "\n'
        '                    f"{_numero_placeholder_tecnico(bonus_unione[\'agi\'])} agilità!\\n"\n'
        '                )\n\n'
    )
    nft = nft.replace(anchor, block + anchor, 1)
write("nft.py", nft)


# ------------------------------------------------------------
# Validazioni statiche / semantiche
# ------------------------------------------------------------
for filename in ["bilanciamento.py", "frasi_incantesimi.py", "liste.py", "nft.py"]:
    ast.parse(read(filename), filename=filename)

# Importiamo solo moduli senza dipendenze esterne runtime.
ns_bil = {}
exec(compile(read("bilanciamento.py"), "bilanciamento.py", "exec"), ns_bil)
ns_frasi = {}
exec(compile(read("frasi_incantesimi.py"), "frasi_incantesimi.py", "exec"), ns_frasi)
ns_liste = {}
exec(compile(read("liste.py"), "liste.py", "exec"), ns_liste)

cfg = ns_bil["INCANTESIMI_CONFIG"][SPELL]["assalto"]["unione"]
assert cfg == {"proc": 100, "percento_stat": 20, "stats": ["atk", "def", "agi"]}
assert SPELL in ns_frasi["FRASI_INCANTESIMI_TECNICHE"]

libri = ns_liste["libri"]
assert BOOK in libri or SPELL in libri
assert any(BOOK in values for values in ns_liste["arenamod"].values() if isinstance(values, list))

pool_finale = ns_liste["pool"]
found = {}
for ring in NEW_RINGS:
    zones = [zona for zona, items in pool_finale.items() if ring in items]
    assert len(zones) == 1, (ring, zones)
    found[ring] = zones[0]
assert len(set(found.values())) == len(NEW_RINGS), found

nft_finale = read("nft.py")
assert '"Unione dello spirito" in get_ench(playerg[pl])' in nft_finale
assert 'incantesimo_cfg("Unione dello spirito", "assalto", "unione")' in nft_finale

print("LIBRO_FORMATO=", repr(libri.get(BOOK, libri.get(SPELL))))
print("DISTRIBUZIONE_ANELLI=", repr(found))
print("OK: Unione dello spirito + distribuzione anelli")

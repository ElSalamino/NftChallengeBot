# -*- coding: utf-8 -*-
import ast
from pathlib import Path

NUOVI = [
    "Polimerizzazione",
    'Valvola da 4"',
    "Roulette russa",
    "Roulette tibetana",
    "Sasso rotolante",
    "WuWuWuuurm",
    "Dance Dance Revolution",
    "GDR semplificato",
]


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    Path(path).write_text(text, encoding="utf-8")


def find_assign(source, name):
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return node
    raise RuntimeError(f"Assegnazione {name} non trovata")


def insert_before_literal_close(path, var_name, block):
    source = read(path)
    if all(repr(n) in source or f'"{n}"' in source for n in NUOVI):
        return
    node = find_assign(source, var_name)
    literal = node.value
    lines = source.splitlines(keepends=True)
    idx = literal.end_lineno - 1
    lines.insert(idx, block)
    write(path, "".join(lines))


# ---------------------------------------------------------------------------
# bilanciamento.py / PROC_ANELLI
# ---------------------------------------------------------------------------
config_block = '''    "Polimerizzazione": {
        "assalto": {"polimerizzazione": {"proc": 100, "percento_stat": 20, "stats": ["atk", "def", "agi"]}},
    },
    "Valvola da 4\\\"": {
        "sfida": {"inizio": {"proc": 100, "atk": 100, "def": 100, "agi": 1}},
    },
    "Roulette russa": {
        "turno": {"roulette": {"proc": 16.6666666667, "lati": 6, "danno": 100}},
    },
    "Roulette tibetana": {
        "turno": {"roulette": {"proc": 16.6666666667, "lati": 6, "cura": 100}},
    },
    "Sasso rotolante": {
        "turno": {"valanga": {"proc": 10, "carica_per_turno": 1, "danno_per_carica": 2, "reset_dopo_proc": True}},
    },
    "WuWuWuuurm": {
        "turno": {"presa_schivata": {"proc": 30, "atk_base": 144, "danno_min": 20, "aggiungi_int": True}},
    },
    "Dance Dance Revolution": {
        "turno": {"combo": {"proc": 100, "incremento": 1, "bonus_danno_per_combo_pct": 10, "reset_su_mancata_schivata": True}},
    },
    "GDR semplificato": {
        "turno": {"formula": {"proc": 100, "attivo_per_entrambi": True, "danno_min": 0}},
    },
'''
insert_before_literal_close("bilanciamento.py", "PROC_ANELLI", config_block)

# ---------------------------------------------------------------------------
# frasi_anelli.py
# ---------------------------------------------------------------------------
frasi_block = '''    "Polimerizzazione": "ASSALTO — se indossi Polimerizzazione, ogni altro membro del clan che indossa lo stesso anello ti trasferisce il {assalto.polimerizzazione.percento_stat:pct} del proprio ATK, DEF e AGI all'inizio dell'assalto. Ogni compagno contribuisce separatamente e i bonus si sommano.",
    "Valvola da 4\\\"": "All'inizio della sfida la valvola ti concede {sfida.inizio.atk:signed} ATK, {sfida.inizio.def:signed} DEF e {sfida.inizio.agi:signed} AGI una sola volta per quella sfida.",
    "Roulette russa": "A ogni inizio turno ogni Roulette russa presente tira indipendentemente: hai 1 possibilità su {turno.roulette.lati} di far perdere {turno.roulette.danno} HP al combattente di turno, anche se l'anello appartiene all'altro giocatore.",
    "Roulette tibetana": "A ogni inizio turno ogni Roulette tibetana presente tira indipendentemente: hai 1 possibilità su {turno.roulette.lati} di curare di {turno.roulette.cura} HP il combattente di turno, anche se l'anello appartiene all'altro giocatore.",
    "Sasso rotolante": "Ogni turno del combattimento il tuo sasso ottiene {turno.valanga.carica_per_turno} carica. A ogni turno ha il {turno.valanga.proc:pct} di colpire l'altro combattente per {turno.valanga.danno_per_carica} danni per carica; quando colpisce, le cariche tornano a zero.",
    "WuWuWuuurm": "Quando il nemico schiva hai il {turno.presa_schivata.proc:pct} di farlo acchiappare dal wurm. Il morso usa la normale formula del danno con un ATK virtuale di {turno.presa_schivata.atk_base} + la tua INT, con almeno {turno.presa_schivata.danno_min} danni se il calcolo va troppo in basso.",
    "Dance Dance Revolution": "Ogni tua schivata consecutiva aumenta la CCCompo di {turno.combo.incremento}; appena non schivi la combo torna a zero. Quando attacchi, ogni punto combo aumenta il danno del {turno.combo.bonus_danno_per_combo_pct:pct}.",
    "GDR semplificato": "Se almeno uno dei due combattenti indossa questo anello, la formula base vale per entrambi: danno = max({turno.formula.danno_min}, ATK - DEF nemica), senza oscillazione casuale. Le schivate e gli effetti successivi continuano a funzionare; i danni ottenuti da questa formula sono marcati con F.",
'''
insert_before_literal_close("frasi_anelli.py", "FRASI_ANELLI_TECNICHE", frasi_block)

# ---------------------------------------------------------------------------
# liste.py: catalogo anelli + descrizioni lore.
# ---------------------------------------------------------------------------
source = read("liste.py")
node = find_assign(source, "anellic")
if not all(n in source[node.lineno-1:node.value.end_lineno] for n in NUOVI):
    lines = source.splitlines(keepends=True)
    idx = node.value.end_lineno - 1
    block = "".join(f"    {n!r},\n" for n in NUOVI)
    lines.insert(idx, block)
    source = "".join(lines)
    write("liste.py", source)

source = read("liste.py")
tree = ast.parse(source)
desc_node = None
for node in tree.body:
    if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict):
        keys = [k.value for k in node.value.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
        if "Scudo levitante" in keys and "Cuffia da boia" in keys:
            desc_node = node.value
            break
if desc_node is None:
    raise RuntimeError("Dizionario descrizioni anelli in liste.py non trovato")
if not all(n in [k.value for k in desc_node.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)] for n in NUOVI):
    lines = source.splitlines(keepends=True)
    idx = desc_node.end_lineno - 1
    lore = {
        "Polimerizzazione": "Unisciti ai tuoi compagni ed assicurati di vincere.",
        'Valvola da 4"': "Concettualmente un blocco di ottone.",
        "Roulette russa": "1/6 di spararti o 1/6 di sparare",
        "Roulette tibetana": "1/6 di curarti o 1/6 di curare",
        "Sasso rotolante": "Crea lentamente una valanga ogni turno, quando il sasso arriva arriva!",
        "WuWuWuuurm": "Un piccolo wurm che ti aiuta a prendere gli avversari al volo!",
        "Dance Dance Revolution": "CCCompo di schivate!",
        "GDR semplificato": "Trasforma le sfide in matematica, ora il danno è attacco - difesa!",
    }
    block = "".join(f"    {k!r}: {v!r},\n" for k, v in lore.items())
    lines.insert(idx, block)
    write("liste.py", "".join(lines))

# ---------------------------------------------------------------------------
# nft.py: logica runtime.
# ---------------------------------------------------------------------------
src = read("nft.py")

helpers = r'''

def _applica_valvola_inizio_sfida(personaggio):
    """Applica una sola volta il bonus iniziale della Valvola da 4\" alla copia dello scontro."""
    nome_anello = 'Valvola da 4"'
    marker = "_valvola4_applicata"
    if personaggio.get("anello") != nome_anello or personaggio.get(marker):
        return ""
    if not anello_ok(random.random(), nome_anello, "sfida", "inizio"):
        return ""
    cfg = anello_cfg(nome_anello, "sfida", "inizio")
    personaggio["atk"] += cfg["atk"]
    personaggio["def"] += cfg["def"]
    personaggio["agi"] += cfg["agi"]
    personaggio[marker] = True
    return f"{personaggio['Nome']} si presenta alla sfida con una valvola enorme!\n"


def _effetti_anelli_inizio_turno(main, oppo, anello, anellon):
    """Effetti che scattano all'inizio di ogni turno usando gli anelli locali post-Leggiadra."""
    text = ""

    # Ogni copia della roulette tira indipendentemente e agisce sul combattente di turno.
    for ring in (anello, anellon):
        if ring == "Roulette russa" and anello_ok(random.random(), ring, "turno", "roulette"):
            danno = anello_val(ring, "turno", "roulette", "danno")
            main["hp"] -= danno
            text += f"{main['Nome']} ha perso la roulette russa, {danno} danni!\n"
        elif ring == "Roulette tibetana" and anello_ok(random.random(), ring, "turno", "roulette"):
            cura = anello_val(ring, "turno", "roulette", "cura")
            main["hp"] += cura
            text += f"{main['Nome']} ha vinto la roulette tibetana, {cura} cure!\n"

    # Ogni Sasso carica a ogni turno, anche quando il proprietario sta difendendo.
    for proprietario, bersaglio, ring in ((main, oppo, anello), (oppo, main, anellon)):
        if ring != "Sasso rotolante":
            continue
        cfg = anello_cfg(ring, "turno", "valanga")
        proprietario["_sasso_cariche"] = proprietario.get("_sasso_cariche", 0) + cfg["carica_per_turno"]
        cariche = proprietario["_sasso_cariche"]
        if anello_ok(random.random(), ring, "turno", "valanga"):
            danni = cariche * cfg["danno_per_carica"]
            bersaglio["hp"] -= danni
            proprietario["_sasso_cariche"] = 0
            text += f"Un sasso becca {bersaglio['Nome']} per {danni} danni!\n"
        else:
            text += f"Senti un sasso in lontananza... ({cariche} Cariche)\n"
    return text
'''

if "def _applica_valvola_inizio_sfida" not in src:
    marker = "\n\ndef incantesimo_cfg"
    if marker not in src:
        raise RuntimeError("Marker incantesimo_cfg non trovato")
    src = src.replace(marker, helpers + marker, 1)

# Valvola: prima di Leggiadra e prima di qualunque turno.
if "text += _applica_valvola_inizio_sfida(main)" not in src:
    marker = '    anello = main["anello"]\n'
    pos = src.find("def turno(main, oppo,cond=None):")
    idx = src.find(marker, pos)
    if idx < 0:
        raise RuntimeError("Marker anello main in turno non trovato")
    add = (
        '    text += _applica_valvola_inizio_sfida(main)\n'
        '    text += _applica_valvola_inizio_sfida(oppo)\n\n'
    )
    src = src[:idx] + add + src[idx:]

# Roulette/Sasso: dopo Leggiadra, così un turno neutralizzato non usa i gadget.
if "_effetti_anelli_inizio_turno(main, oppo, anello, anellon)" not in src[src.find("def turno(main, oppo,cond=None):"):]:
    pos = src.find("def turno(main, oppo,cond=None):")
    marker = '    dps = main["atk"]\n'
    idx = src.find(marker, pos)
    if idx < 0:
        raise RuntimeError("Marker dps iniziale turno non trovato")
    add = (
        '    text += _effetti_anelli_inizio_turno(main, oppo, anello, anellon)\n'
        '    if main["hp"] <= 0 or oppo["hp"] <= 0:\n'
        '        return text\n\n'
    )
    src = src[:idx] + add + src[idx:]

# DDR + WuWuWuuurm sulla schivata.
old = '''        oppo["schivato"] = True
        if anello == "Coda demoniaca":
'''
new = '''        oppo["schivato"] = True
        if anellon == "Dance Dance Revolution":
            incremento_combo = anello_val(anellon, "turno", "combo", "incremento")
            oppo["_ddr_combo"] = oppo.get("_ddr_combo", 0) + incremento_combo
            text += f"CCCompo a {oppo['_ddr_combo']}!\\n"
        if anello == "WuWuWuuurm" and anello_ok(random.random(), anello, "turno", "presa_schivata"):
            cfg_wurm = anello_cfg(anello, "turno", "presa_schivata")
            atk_wurm = cfg_wurm["atk_base"] + (main.get("int", 0) if cfg_wurm.get("aggiungi_int", True) else 0)
            def_wurm = max(0, difesan)
            danni_wurm = random.uniform(
                atk_wurm * (100 / ((100 + def_wurm * 1.5) + 1)),
                atk_wurm * (100 / ((100 + def_wurm) + 1)),
            )
            danni_wurm = round(max(cfg_wurm["danno_min"], danni_wurm))
            oppo["hp"] -= danni_wurm
            text += f"Il wurm prende al volo {nome2}, mordendolo per {danni_wurm} danni!\\n"
        if anello == "Coda demoniaca":
'''
if old in src and "CCCompo a" not in src:
    src = src.replace(old, new, 1)

old = '''        oppo["schivato"] = False
        num = random.random()
'''
new = '''        oppo["schivato"] = False
        if anellon == "Dance Dance Revolution" and oppo.get("_ddr_combo", 0) > 0:
            oppo["_ddr_combo"] = 0
            text += "CCCompo persa!\\n"
        num = random.random()
'''
if old in src and "CCCompo persa" not in src:
    src = src.replace(old, new, 1)

# Formula GDR + bonus danno DDR.
old = '''    danno = random.uniform(
                dps * (100 / ((100 + difesan * 1.5)+1)), dps * (100 / ((100 + difesan)+1))
            )

    if danno <= 20:
        danno = 20
'''
new = '''    formula_gdr = anello == "GDR semplificato" or anellon == "GDR semplificato"
    if formula_gdr:
        danno = max(anello_val("GDR semplificato", "turno", "formula", "danno_min", 0), dps - difesan)
        if mod > 0:
            mod = 1
    else:
        danno = random.uniform(
                    dps * (100 / ((100 + difesan * 1.5)+1)), dps * (100 / ((100 + difesan)+1))
                )
        if danno <= 20:
            danno = 20

    if anello == "Dance Dance Revolution" and mod > 0:
        combo_ddr = main.get("_ddr_combo", 0)
        if combo_ddr > 0:
            bonus_combo = anello_val(anello, "turno", "combo", "bonus_danno_per_combo_pct")
            danno *= 1 + ((combo_ddr * bonus_combo) / 100)
'''
if old not in src:
    if "formula_gdr = anello == \"GDR semplificato\"" not in src:
        raise RuntimeError("Blocco formula danno standard non trovato")
else:
    src = src.replace(old, new, 1)

# Marca F sui danni che derivano dalla formula base semplificata.
if 'formula_tag = "F" if formula_gdr else ""' not in src:
    marker = '    dannov = round(danno * mod)\n'
    pos = src.find("def turno(main, oppo,cond=None):")
    idx = src.find(marker, pos)
    if idx < 0:
        raise RuntimeError("Marker dannov non trovato")
    src = src[:idx] + '    formula_tag = "F" if formula_gdr else ""\n' + src[idx:]

src = src.replace('{dannov} danno allo scudo di {nome2}', '{dannov}{formula_tag} danno allo scudo di {nome2}')
src = src.replace('{dannov} danni a {nome2}', '{dannov}{formula_tag} danni a {nome2}')

# Polimerizzazione nell'aura di clan dell'assalto.
if "La polimerizzazione di {pl} eccheggia" not in src:
    old = '''            aniel = scheda_membro["anello"]
            if aniel in PROC_ANELLI and "aura" in PROC_ANELLI[aniel].get("assalto", {}):
'''
    new = '''            aniel = scheda_membro["anello"]

            if anello == "Polimerizzazione" and pl != nome and aniel == "Polimerizzazione":
                cfg_poly = anello_cfg("Polimerizzazione", "assalto", "polimerizzazione")
                bonus_poly = {}
                for stat_poly in cfg_poly["stats"]:
                    valore_poly = scheda_membro.get(stat_poly, 0) * cfg_poly["percento_stat"] / 100
                    player[stat_poly] += valore_poly
                    bonus_poly[stat_poly] = valore_poly
                text += (
                    f"La polimerizzazione di {pl} eccheggia, dandoti "
                    f"{_numero_placeholder_tecnico(bonus_poly['atk'])} atk "
                    f"{_numero_placeholder_tecnico(bonus_poly['def'])} def e "
                    f"{_numero_placeholder_tecnico(bonus_poly['agi'])} agilità!\\n"
                )

            if aniel in PROC_ANELLI and "aura" in PROC_ANELLI[aniel].get("assalto", {}):
'''
    if old not in src:
        raise RuntimeError("Blocco aura clan non trovato")
    src = src.replace(old, new, 1)

write("nft.py", src)

print("Patch nuovi anelli applicata")

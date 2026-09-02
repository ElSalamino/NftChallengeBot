from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_required(text, old, new, label=None):
    if old not in text:
        raise SystemExit(f"Pattern non trovato: {label or old[:100]!r}")
    return text.replace(old, new)


CONFIG = r'''

# ============================================================
# CONFIGURAZIONE STRUTTURE D'ASSALTO
# ============================================================
# I valori base HP/statistiche e le modalita' disponibili restano in liste.py
# (hps, starmi, spec, frasispec). Qui vive tutto il tuning numerico che prima
# era hardcodato dentro assedio(), cosi' runtime e wiki leggono la stessa fonte.
STRUTTURE_CONFIG = {
    "generale": {
        "scaling": {"divisore_livello": 10},
        "ultima_struttura": {"atk_delta": -100, "agi_delta": -10, "def_delta": -300},
        "tiro": {"agi_difensore_divisore": 2, "bonus": 1, "random_max": 102},
        "danno": {
            "difesa": {"numeratore": 100, "difesa_base": 1, "random_min": 0.7, "random_max": 1.5},
            "spuntone": {"numeratore": 100, "difesa_base": 50, "random_min": 0.7, "random_max": 1.5},
            "attaccante": {"numeratore": 100, "difesa_base": 1, "random_min": 0.7, "random_max": 1.3},
        },
        "danno_minimo": 5,
    },
    "Bersaglio enorme": {
        "generale": {"distrazione_proc": 20},
        "modalita": {
            "Classico": {},
            "Movibile": {"colpito_proc": 30, "danno_mul": 4},
        },
    },
    "Muraglione extra": {
        "generale": {
            "def_attaccante_mul": 0.5,
            "bonus_def_per_livello": 5,
            "bonus_def_strutture_divisore": 4,
            "infezione_proc": 10,
            "infezione_def_delta": -50,
        },
        "modalita": {
            "Possente": {},
            "Infiammato": {"danno_bonus": 250, "autodanno": 100},
        },
    },
    "Spaventapasseri ornamentale": {
        "modalita": {
            "Magico": {"attacco_diretto": False, "corvi_proc": 10},
            "Animato": {"attacco_diretto": True},
        },
    },
    "Clone": {
        "generale": {"bonus_atk_difese_su_mancato_colpo": 20},
        "modalita": {
            "Aggressivo": {},
            "Difensivo": {"agi_delta": -40},
        },
    },
    "Chiesa": {
        "modalita": {
            "Credente": {"attacco_diretto": True},
            "Orribile": {
                "attacco_diretto": False,
                "creatura_proc": 10,
                "bonus_atk": 250,
                "bonus_def": 250,
                "bonus_agi": 25,
            },
        },
    },
    "Accampamento": {
        "modalita": {
            "Trappole danneggianti": {},
            "Trappole demoralizzanti": {"danno_divisore": 1.3, "bonus_atk_difese": 50},
        },
    },
    "Cane da guardia": {
        "generale": {"rincorsa_proc": 30, "rincorsa_danno_divisore": 2},
        "modalita": {
            "Cane possente": {},
            "Cane rapido": {"danno_divisore": 1.3, "rincorse_extra_max": 4, "rincorsa_extra_proc": 50},
            "Orso": {"danno_mul": 1.5, "rincorsa_disabilitata": True},
        },
    },
    "Stazione laser di sicurezza": {
        "generale": {"bonus_def_proc": 10, "bonus_def_per_livello": 10},
        "modalita": {
            "Mitragliatrice laser": {},
            "Difesa laser": {"atk_da_def_mul": 2, "def_da_atk_divisore": 2},
            "Suicidio laser": {"autodanno": 55, "atk_mul": 2.5, "agi_delta": -26},
        },
    },
    "Spuntone malefico": {
        "generale": {"stop_proc": 60, "bonus_def_per_livello": 2},
        "modalita": {
            "Palese": {"roll_bonus_pct": 0},
            "Sotterraneo": {"agi_delta": -25, "roll_bonus_pct": 20},
        },
    },
    "Cannoncino": {
        "generale": {"bonus_agi_difese": 5, "drago_proc": 10, "drago_bonus_agi": 20},
        "modalita": {
            "Rumoroso": {},
            "Danneggiante": {"danno_mul": 2},
        },
    },
    "Sedimento del cucciolo": {
        "generale": {"mamma_proc": 10, "mamma_hp_min": -2, "mamma_hp_max": 10},
        "modalita": {
            "Assonnato": {},
            "Affamato": {"agi_delta": 55, "atk_divisore": 1.5},
        },
    },
    "Centrale di cura centralizzata": {
        "generale": {"valore_per_livello": 3, "hp_minimo_modifica": 50},
        "modalita": {
            "Sparsa": {"bersagli": "tutti"},
            "Concentrata": {"bersagli": 1},
        },
    },
    "Fabbro incantaspade": {
        "generale": {"bonus_atk_per_livello": 25, "bonus_def_per_livello": 25},
        "modalita": {
            "Malevolo": {"attacco_diretto": True},
            "Curativo": {"attacco_diretto": False, "cura": True},
        },
    },
}
'''

# 1) bilanciamento.py: unica fonte dei magic number delle strutture.
bil = ROOT / "bilanciamento.py"
bil_text = bil.read_text(encoding="utf-8")
if "STRUTTURE_CONFIG =" in bil_text:
    raise SystemExit("STRUTTURE_CONFIG esiste gia'")
bil.write_text(bil_text.rstrip() + CONFIG + "\n", encoding="utf-8")

# 2) nft.py: importa config e fornisce accessor/formula condivisi.
nft = ROOT / "nft.py"
nft_text = nft.read_text(encoding="utf-8")
nft_text = replace_required(
    nft_text,
    "from bilanciamento import PROC_CLASSI, PROC_ANELLI, NUCLEI_CONFIG, DUNGEON_CONFIG, INCANTESIMI_CONFIG, EFFETTI_CONFIG, WEEKEND_MOD_CONFIG, WEEKEND_MOD_POOL",
    "from bilanciamento import PROC_CLASSI, PROC_ANELLI, NUCLEI_CONFIG, DUNGEON_CONFIG, INCANTESIMI_CONFIG, EFFETTI_CONFIG, WEEKEND_MOD_CONFIG, WEEKEND_MOD_POOL, STRUTTURE_CONFIG",
    "import bilanciamento",
)
anchor = '''def anello_val(anello, contesto, nome, chiave, default=None):\n    \"\"\"Legge un valore di tuning dell'anello.\"\"\"\n    return anello_cfg(anello, contesto, nome).get(chiave, default)\n'''
helpers = anchor + r'''


def struttura_val(nome, *percorso, default=None):
    """Legge un valore della configurazione strutture d'assalto."""
    valore = STRUTTURE_CONFIG.get(nome, {})
    for parte in percorso:
        if not isinstance(valore, dict) or parte not in valore:
            return default
        valore = valore[parte]
    return valore


def struttura_ok(numero_casuale, nome, *percorso, default=0):
    """Confronta un random 0..1 con una probabilita' percentuale della struttura."""
    valore = struttura_val(nome, *percorso, default=default)
    return numero_casuale < (valore / 100)


def struttura_danno(attacco, difesa, profilo="difesa"):
    """Formula danno d'assalto data-driven; non estrae random extra rispetto al runtime storico."""
    cfg = struttura_val("generale", "danno", profilo)
    return round(
        float(attacco)
        * (
            cfg["numeratore"]
            / (cfg["difesa_base"] + float(difesa))
            * random.uniform(cfg["random_min"], cfg["random_max"])
        )
    )
'''
nft_text = replace_required(nft_text, anchor, helpers, "helper anello_val")
nft.write_text(nft_text, encoding="utf-8")

# 3) turno_assalto.py: sostituisce solo la prima implementazione base di assedio().
ta = ROOT / "turno_assalto.py"
text = ta.read_text(encoding="utf-8")
start = text.index("def assedio(")
end = text.index("\ndef turno(", start)
assedio = text[start:end]

replacements = [
    ('if "Bersaglio enorme" in list(nemico) and 0.2 > num:', 'if "Bersaglio enorme" in list(nemico) and struttura_ok(num, "Bersaglio enorme", "generale", "distrazione_proc"):'),
    ('player["atk"] += 25 * clan[team]["villaggio"]["Fabbro incantaspade"]["lv"]', 'player["atk"] += struttura_val("Fabbro incantaspade", "generale", "bonus_atk_per_livello") * clan[team]["villaggio"]["Fabbro incantaspade"]["lv"]'),
    ('player["def"] += 25 * clan[team]["villaggio"]["Fabbro incantaspade"]["lv"]', 'player["def"] += struttura_val("Fabbro incantaspade", "generale", "bonus_def_per_livello") * clan[team]["villaggio"]["Fabbro incantaspade"]["lv"]'),
    ('(nemico[difesa]["lv"] / 10)', '(nemico[difesa]["lv"] / struttura_val("generale", "scaling", "divisore_livello"))'),
    ('attaccon -= 100\n                    agin -= 10\n                    difesan -= 300', 'attaccon += struttura_val("generale", "ultima_struttura", "atk_delta")\n                    agin += struttura_val("generale", "ultima_struttura", "agi_delta")\n                    difesan += struttura_val("generale", "ultima_struttura", "def_delta")'),
    ('agin -= 40\n                                text += f"{nomeclone} cerca di correre alla pulsantiera!\\n"', 'agin += struttura_val("Clone", "modalita", "Difensivo", "agi_delta")\n                                text += f"{nomeclone} cerca di correre alla pulsantiera!\\n"'),
    ('agin += 55\n                    text += "__Si sente un gorgoglio...__\\n"\n                    attaccon = attaccon//1.5', 'agin += struttura_val("Sedimento del cucciolo", "modalita", "Affamato", "agi_delta")\n                    text += "__Si sente un gorgoglio...__\\n"\n                    attaccon = attaccon // struttura_val("Sedimento del cucciolo", "modalita", "Affamato", "atk_divisore")'),
    ('agin -= 25\n\n                elif setting["Stazione laser di sicurezza"]', 'agin += struttura_val("Spuntone malefico", "modalita", "Sotterraneo", "agi_delta")\n\n                elif setting["Stazione laser di sicurezza"]'),
    ('attaccon = difesan * 2\n                    difesan = old//2', 'attaccon = difesan * struttura_val("Stazione laser di sicurezza", "modalita", "Difesa laser", "atk_da_def_mul")\n                    difesan = old // struttura_val("Stazione laser di sicurezza", "modalita", "Difesa laser", "def_da_atk_divisore")'),
    ('nemico[difesa]["hp"] -= 55\n                    attaccon = round(attaccon * 2.5)\n                    agin -= 26', 'nemico[difesa]["hp"] -= struttura_val("Stazione laser di sicurezza", "modalita", "Suicidio laser", "autodanno")\n                    attaccon = round(attaccon * struttura_val("Stazione laser di sicurezza", "modalita", "Suicidio laser", "atk_mul"))\n                    agin += struttura_val("Stazione laser di sicurezza", "modalita", "Suicidio laser", "agi_delta")'),
    ('colpito = round(agi - (agin / 2) + 1)\n                \n                if colpito > random.randint(0, 102):', 'colpito = round(agi - (agin / struttura_val("generale", "tiro", "agi_difensore_divisore")) + struttura_val("generale", "tiro", "bonus"))\n                \n                if colpito > random.randint(0, struttura_val("generale", "tiro", "random_max")):'),
    ('if 0.1 > num:\n                                    num = random.random()\n                                    bonus["atk"] += 250\n                                    bonus["def"] += 250\n                                    bonus["agi"] += 25', 'if struttura_ok(num, "Chiesa", "modalita", "Orribile", "creatura_proc"):\n                                    num = random.random()\n                                    bonus["atk"] += struttura_val("Chiesa", "modalita", "Orribile", "bonus_atk")\n                                    bonus["def"] += struttura_val("Chiesa", "modalita", "Orribile", "bonus_def")\n                                    bonus["agi"] += struttura_val("Chiesa", "modalita", "Orribile", "bonus_agi")'),
    ('bonus["def"] += 5 * (nemico[difesa]["lv"] + (len(nemico)/4))', 'bonus["def"] += struttura_val("Muraglione extra", "generale", "bonus_def_per_livello") * (nemico[difesa]["lv"] + (len(nemico) / struttura_val("Muraglione extra", "generale", "bonus_def_strutture_divisore")))'),
    ('num += .2', 'num += struttura_val("Spuntone malefico", "modalita", "Sotterraneo", "roll_bonus_pct") / 100'),
    ('if 0.6 > num:', 'if (struttura_val("Spuntone malefico", "generale", "stop_proc") / 100) > num:'),
    ('dannissimi = round(float(attaccon)* (100 / (50 + float(defense))* random.uniform(0.7, 1.5)))', 'dannissimi = struttura_danno(attaccon, defense, "spuntone")'),
    ('bonus["atk"] += 20\n                    elif difesa == "Centrale di cura centralizzata":', 'bonus["atk"] += struttura_val("Clone", "generale", "bonus_atk_difese_su_mancato_colpo")\n                    elif difesa == "Centrale di cura centralizzata":'),
    ('defense *= 0.5', 'defense *= struttura_val("Muraglione extra", "generale", "def_attaccante_mul")'),
    ('dannissimi = round(float(attaccon)* (100 / (1 +float(defense)) * random.uniform(0.7, 1.5)))', 'dannissimi = struttura_danno(attaccon, defense, "difesa")'),
    ('dannissimi = dannissimi//1.3', 'dannissimi = dannissimi // struttura_val("Accampamento", "modalita", "Trappole demoralizzanti", "danno_divisore")'),
    ('dannissimi =round( dannissimi//1.3)', 'dannissimi = round(dannissimi // struttura_val("Cane da guardia", "modalita", "Cane rapido", "danno_divisore"))'),
    ('dannissimi =round( dannissimi * 1.5)', 'dannissimi = round(dannissimi * struttura_val("Cane da guardia", "modalita", "Orso", "danno_mul"))'),
    ('dannissimi = dannissimi * 2\n                                text += "BOOM!\\n"', 'dannissimi = dannissimi * struttura_val("Cannoncino", "modalita", "Danneggiante", "danno_mul")\n                                text += "BOOM!\\n"'),
    ('dannissimi += 250\n                                nemico[difesa]["hp"] -= 100', 'dannissimi += struttura_val("Muraglione extra", "modalita", "Infiammato", "danno_bonus")\n                                nemico[difesa]["hp"] -= struttura_val("Muraglione extra", "modalita", "Infiammato", "autodanno")'),
    ('dannissimi = 5', 'dannissimi = struttura_val("generale", "danno_minimo")'),
    ('bonus["atk"] += 50\n                                text += f"Delle trappole', 'bonus["atk"] += struttura_val("Accampamento", "modalita", "Trappole demoralizzanti", "bonus_atk_difese")\n                                text += f"Delle trappole'),
    ('if difesa == "Muraglione extra" and 0.1 > num:', 'if difesa == "Muraglione extra" and struttura_ok(num, "Muraglione extra", "generale", "infezione_proc"):'),
    ('player["def"] -= 50', 'player["def"] += struttura_val("Muraglione extra", "generale", "infezione_def_delta")'),
    ('elif difesa == "Spaventapasseri ornamentale" and 0.1 > num and setting["Spaventapasseri ornamentale"] != "Animato":', 'elif difesa == "Spaventapasseri ornamentale" and struttura_ok(num, "Spaventapasseri ornamentale", "modalita", "Magico", "corvi_proc") and setting["Spaventapasseri ornamentale"] != "Animato":'),
    ('elif difesa == "Stazione laser di sicurezza" and 0.1 > num:\n                            bonus["def"] += 10 * nemico[difesa]["lv"]', 'elif difesa == "Stazione laser di sicurezza" and struttura_ok(num, "Stazione laser di sicurezza", "generale", "bonus_def_proc"):\n                            bonus["def"] += struttura_val("Stazione laser di sicurezza", "generale", "bonus_def_per_livello") * nemico[difesa]["lv"]'),
    ('elif difesa == "Cane da guardia" and 0.3 > num and setting["Cane da guardia"] != "Orso":', 'elif difesa == "Cane da guardia" and struttura_ok(num, "Cane da guardia", "generale", "rincorsa_proc") and setting["Cane da guardia"] != "Orso":'),
    ('dannissimi = round(dannissimi//2)\n                            for g in range(4):\n                                if difesa == "Cane da guardia" and 0.5 > num and setting["Cane da guardia"] == "Cane rapido":', 'dannissimi = round(dannissimi // struttura_val("Cane da guardia", "generale", "rincorsa_danno_divisore"))\n                            for g in range(struttura_val("Cane da guardia", "modalita", "Cane rapido", "rincorse_extra_max")):\n                                if difesa == "Cane da guardia" and struttura_ok(num, "Cane da guardia", "modalita", "Cane rapido", "rincorsa_extra_proc") and setting["Cane da guardia"] == "Cane rapido":'),
    ('bonus["agi"] += 5\n                            if 0.1 > num:', 'bonus["agi"] += struttura_val("Cannoncino", "generale", "bonus_agi_difese")\n                            if struttura_ok(num, "Cannoncino", "generale", "drago_proc"):'),
    ('bonus["agi"] += 20', 'bonus["agi"] += struttura_val("Cannoncino", "generale", "drago_bonus_agi")'),
    ('bonus["def"] += 2 * nemico[difesa]["lv"]', 'bonus["def"] += struttura_val("Spuntone malefico", "generale", "bonus_def_per_livello") * nemico[difesa]["lv"]'),
    ('elif difesa == "Sedimento del cucciolo" and 0.1 > num:', 'elif difesa == "Sedimento del cucciolo" and struttura_ok(num, "Sedimento del cucciolo", "generale", "mamma_proc"):'),
    ('player["hp"] = random.randint(-2, 10)', 'player["hp"] = random.randint(struttura_val("Sedimento del cucciolo", "generale", "mamma_hp_min"), struttura_val("Sedimento del cucciolo", "generale", "mamma_hp_max"))'),
    ('if setting["Bersaglio enorme"] == "Movibile" and num >= 0.3 and target == "Bersaglio enorme":', 'if setting["Bersaglio enorme"] == "Movibile" and not struttura_ok(num, "Bersaglio enorme", "modalita", "Movibile", "colpito_proc") and target == "Bersaglio enorme":'),
    ('dannissimi *= 4', 'dannissimi *= struttura_val("Bersaglio enorme", "modalita", "Movibile", "danno_mul")'),
    ('dannissimi = round(float(dps) * (100 / (float(1 + difesan)) * random.uniform(0.7, 1.3)))', 'dannissimi = struttura_danno(dps, difesan, "attaccante")'),
]

for old, new in replacements:
    assedio = replace_required(assedio, old, new)

# Centrale: gli stessi due numeri compaiono in piu' rami (cura e inversione Assassino delle ombre).
assedio = assedio.replace(
    '3 * int(nemico[difesa]["lv"])',
    'struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])',
)
assedio = assedio.replace(
    'nemico[dife]["hp"] > 50',
    'nemico[dife]["hp"] > struttura_val("Centrale di cura centralizzata", "generale", "hp_minimo_modifica")',
)
assedio = assedio.replace(
    'nemico[news]["hp"] > 50',
    'nemico[news]["hp"] > struttura_val("Centrale di cura centralizzata", "generale", "hp_minimo_modifica")',
)

# Chiesa Orribile compare in due rami quasi identici; il secondo ha indentazione diversa.
assedio = assedio.replace(
    'if 0.1 > num:\n                                    num = random.random()\n                                    bonus["atk"] += 250\n                                    bonus["def"] += 250\n                                    bonus["agi"] += 25',
    'if struttura_ok(num, "Chiesa", "modalita", "Orribile", "creatura_proc"):\n                                    num = random.random()\n                                    bonus["atk"] += struttura_val("Chiesa", "modalita", "Orribile", "bonus_atk")\n                                    bonus["def"] += struttura_val("Chiesa", "modalita", "Orribile", "bonus_def")\n                                    bonus["agi"] += struttura_val("Chiesa", "modalita", "Orribile", "bonus_agi")',
)

# Verifiche mirate: questi magic number non devono piu' governare le strutture nell'assedio base.
for forbidden in (
    'and 0.2 > num',
    'nemico[difesa]["lv"] / 10',
    'agin -= 40',
    'agin += 55',
    'agin -= 25',
    'nemico[difesa]["hp"] -= 55',
    'attaccon * 2.5',
    'dannissimi += 250',
    'nemico[difesa]["hp"] -= 100',
    'dannissimi *= 4',
    'random.randint(-2, 10)',
):
    if forbidden in assedio:
        raise SystemExit(f"Magic number struttura ancora presente: {forbidden}")

text = text[:start] + assedio + text[end:]
ta.write_text(text, encoding="utf-8")

print("Refactor strutture completato")

# -*- coding: utf-8 -*-
from pathlib import Path
import re


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: atteso 1, trovato {count}")
    return text.replace(old, new, 1)


def replace_count(text, old, new, expected, label):
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"{label}: atteso {expected}, trovato {count}")
    return text.replace(old, new)


# -----------------------------------------------------------------------------
# bilanciamento.py: database incantesimi ed effetto Fortunello
# -----------------------------------------------------------------------------
bil_path = Path("bilanciamento.py")
bil = bil_path.read_text(encoding="utf-8")

bil = bil.replace(
    "Contiene esclusivamente dati di tuning per classi, anelli e dungeon.",
    "Contiene esclusivamente dati di tuning per classi, anelli, dungeon, incantesimi ed effetti temporanei.",
    1,
)

if "INCANTESIMI_CONFIG =" in bil or "EFFETTI_CONFIG =" in bil:
    raise SystemExit("Config incantesimi/effetti già presente: interrompo per non duplicare")

# Rimuove la vecchia soglia duplicata di Smateriabile da Fire lord: il vecchio
# flow usava lo stesso tiro dell'8% di Muori insetto e poi controllava <10%,
# quindi quando Muori insetto partiva Smateriabile lo bloccava sempre.
bil, n = re.subn(
    r"('muori_insetto': \{'proc': 8, 'danno': 80), 'smateriabile_proc': 10(\})",
    r"\1\2",
    bil,
    count=1,
)
if n != 1:
    raise SystemExit(f"Fire lord/smateriabile_proc: atteso 1, trovato {n}")

bil += r'''

# ============================================================
# INCANTESIMI
# Valori numerici usati dagli incantesimi. Le probabilità sono
# sempre espresse in percentuale 0..100.
# ============================================================
INCANTESIMI_CONFIG = {
    "Icore": {
        "turno": {"penetrazione": {"proc": 5, "difesa_target_mul": 0.6}},
    },
    "Ingrossamento": {
        "turno": {
            "crescita": {
                "proc": 2,
                "atk_min": 20,
                "atk_max": 100,
                "agi_min": -20,
                "agi_max": -2,
            }
        },
    },
    "Predominio": {
        "turno": {
            "difesa": {
                "dps_attaccante_mul": 0.8,
                "agi_attaccante": 30,
            }
        },
    },
    "Duraturo": {
        "turno": {"difesa": {"proc": 10, "difesa_mul": 1.7}},
    },
    "Smateriabile": {
        "turno": {
            "annulla_colpo": {"proc": 10},
            "tempesta_sabbia": {"proc": 30},
        },
        "interazioni": {
            "fire_lord": {"blocca": True},
        },
    },
    "Tocco fantasma": {
        "turno": {
            "colpo_schivato": {
                "proc": 2,
                "dps_percento_min": 5,
                "dps_percento_max": 10,
                "danno_min": 30,
            }
        },
    },
    "Leggiadra": {
        "turno": {"annulla_colpo_proprio": {"proc": 10}},
    },
    "Speranza": {
        "turno": {"salvezza": {"hp_min": 1, "hp_max": 60, "hp_porta_a": 100}},
    },
    "Velenoso": {
        "turno": {"veleno": {"proc": 5, "stack": 1, "danno_per_stack": 5}},
    },
    "Iridescente": {
        "turno": {"cura": {"proc": 5, "cura": 85}},
    },
    "Minimista": {
        "turno": {"danno_minimo": {"mod_min": 0.1, "danno_base_min": 10}},
    },
    "Mimico": {
        "turno": {"copia": {"attivo": True}},
    },
    "Affilatezza": {
        "turno": {"affila": {"proc": 10, "atk_mul": 1.2}},
    },
    "Legione": {
        "turno": {"duello_legione": {"dps_mul": 10}},
    },
    "Critico": {
        "turno": {"critico": {"proc": 8, "danno_mul": 1.5}},
    },
    "Primo impatto": {
        "turno": {"primo_colpo": {"danno_mul": 1.7}},
    },
    "Multiplo": {
        "turno": {"difesa": {"proc": 10, "agi": 8}},
    },
    "Legaccio": {
        "turno": {"lega": {"proc": 5, "agi_target_mul": 0.75}},
    },
    "Urlo di drago": {
        "turno": {"terrore": {"proc": 5}},
    },
    "Evocabilità": {
        "dungeon": {"supporto": {"atk": 40, "def": 40, "agi": 10}},
    },
}


# Effetti temporanei non legati agli incantesimi.
EFFETTI_CONFIG = {
    "Fortunello": {
        "sfida": {
            "premio_oggetto": {
                "bonus_probabilita_per_livello_pct": 5,
            }
        }
    }
}
'''

bil_path.write_text(bil, encoding="utf-8")


# -----------------------------------------------------------------------------
# frasi_incantesimi.py: una frase umana dedicata a ciascun incantesimo
# -----------------------------------------------------------------------------
Path("frasi_incantesimi.py").write_text(r'''# -*- coding: utf-8 -*-
"""Frasi leggibili degli incantesimi, con valori presi da INCANTESIMI_CONFIG."""

FRASI_INCANTESIMI_TECNICHE = {
    "Icore": "Quando attacchi hai il {turno.penetrazione.proc:pct} di portare la difesa usata dal nemico al {turno.penetrazione.difesa_target_mul:pct_mul} per quel colpo.",
    "Ingrossamento": "A ogni attacco hai il {turno.crescita.proc:pct} di far crescere l'arma: guadagni tra {turno.crescita.atk_min} e {turno.crescita.atk_max} ATK, ma perdi tra {turno.crescita.agi_max:abs} e {turno.crescita.agi_min:abs} AGI.",
    "Predominio": "Se chi ti attacca ha meno o gli stessi HP di te, riduci il suo potenziale offensivo del {turno.difesa.dps_attaccante_mul:rid_pct}; nello stesso calcolo però gli concedi {turno.difesa.agi_attaccante:signed} AGI, rendendolo più difficile da schivare.",
    "Duraturo": "Quando difendi hai il {turno.difesa.proc:pct} di far valere la tua DEF al {turno.difesa.difesa_mul:pct_mul} per quel colpo.",
    "Smateriabile": "Quando difendi hai il {turno.annulla_colpo.proc:pct} di annullare completamente un colpo normale; contro la tempesta di sabbia la possibilità sale al {turno.tempesta_sabbia.proc:pct}. Inoltre blocca sempre Muori insetto di Fire lord quando quel colpo speciale riesce ad attivarsi.",
    "Tocco fantasma": "Se il nemico schiva, hai il {turno.colpo_schivato.proc:pct} di colpirlo comunque per un danno tra il {turno.colpo_schivato.dps_percento_min:pct} e il {turno.colpo_schivato.dps_percento_max:pct} del tuo DPS, con un minimo di {turno.colpo_schivato.danno_min} danni.",
    "Leggiadra": "Quando un tuo colpo stava per andare a segno, hai il {turno.annulla_colpo_proprio.proc:pct} di azzerare volontariamente danno e modificatore di quel colpo; se il nemico aveva già schivato non cambia nulla.",
    "Speranza": "Quando difendi e resti tra {turno.salvezza.hp_min} e {turno.salvezza.hp_max} HP, torni subito a {turno.salvezza.hp_porta_a} HP prima di risolvere il colpo in arrivo.",
    "Velenoso": "Ogni tuo colpo ha il {turno.veleno.proc:pct} di aggiungere {turno.veleno.stack} carica di veleno. Ogni carica infligge {turno.veleno.danno_per_stack} danni ogni volta che quel bersaglio torna a subire un tuo turno.",
    "Iridescente": "Non serve che ci sia il sole: quando vieni attaccato hai il {turno.cura.proc:pct} di recuperare {turno.cura.cura} HP.",
    "Minimista": "Se un colpo verrebbe annullato, riporta il modificatore a {turno.danno_minimo.mod_min:pct_mul}; se anche il danno base è a zero lo porta a {turno.danno_minimo.danno_base_min}, così il colpo può ancora lasciare il segno.",
    "Mimico": "Quando entra in gioco, sostituisce i tuoi incantesimi con quelli dell'avversario per il resto di quella copia dello scontro.",
    "Affilatezza": "A ogni attacco hai il {turno.affila.proc:pct} di portare il tuo ATK al {turno.affila.atk_mul:pct_mul} del valore attuale. L'aumento resta nello scontro e può attivarsi più volte.",
    "Legione": "Se anche l'avversario possiede Legione, il DPS del tuo colpo viene moltiplicato per {turno.duello_legione.dps_mul:x}.",
    "Critico": "Ogni colpo ha il {turno.critico.proc:pct} di diventare critico e portare il danno al {turno.critico.danno_mul:pct_mul} del valore normale.",
    "Primo impatto": "Il primo colpo dello scontro porta il danno al {turno.primo_colpo.danno_mul:pct_mul}; poi Primo impatto si consuma per quello scontro.",
    "Multiplo": "Quando difendi hai il {turno.difesa.proc:pct} di ottenere {turno.difesa.agi:signed} AGI solo nel calcolo della schivata di quel colpo.",
    "Legaccio": "A ogni attacco hai il {turno.lega.proc:pct} di portare l'AGI attuale del nemico al {turno.lega.agi_target_mul:pct_mul}. La riduzione resta nello scontro e può accumularsi.",
    "Urlo di drago": "A ogni attacco hai il {turno.terrore.proc:pct} di terrorizzare il nemico: al suo prossimo turno non infligge il colpo e poi il terrore svanisce.",
    "Evocabilità": "Se vieni evocato come supporto contro un boss del dungeon, chi ti ha chiamato riceve {dungeon.supporto.atk:signed} ATK, {dungeon.supporto.def:signed} DEF e {dungeon.supporto.agi:signed} AGI.",
}
''', encoding="utf-8")


# -----------------------------------------------------------------------------
# nft.py: helper, descrizioni e sostituzione dei magic number
# -----------------------------------------------------------------------------
nft_path = Path("nft.py")
nft = nft_path.read_text(encoding="utf-8")

nft = replace_once(
    nft,
    "from bilanciamento import PROC_CLASSI, PROC_ANELLI, DUNGEON_CONFIG",
    "from bilanciamento import PROC_CLASSI, PROC_ANELLI, DUNGEON_CONFIG, INCANTESIMI_CONFIG, EFFETTI_CONFIG",
    "import bilanciamento",
)
nft = replace_once(
    nft,
    "from frasi_anelli import FRASI_ANELLI_TECNICHE",
    "from frasi_anelli import FRASI_ANELLI_TECNICHE\nfrom frasi_incantesimi import FRASI_INCANTESIMI_TECNICHE",
    "import frasi incantesimi",
)

helper = r'''

def incantesimo_cfg(incantesimo, contesto, nome):
    """Restituisce la configurazione di un effetto di incantesimo."""
    return INCANTESIMI_CONFIG.get(incantesimo, {}).get(contesto, {}).get(nome, {})


def incantesimo_percent(incantesimo, contesto, nome, default=0):
    """Probabilità dell'incantesimo espressa in percentuale 0..100."""
    return incantesimo_cfg(incantesimo, contesto, nome).get("proc", default)


def incantesimo_ok(numero_casuale, incantesimo, contesto, nome, default=0):
    """Usa il random già estratto per mantenere il flow storico."""
    return numero_casuale < (incantesimo_percent(incantesimo, contesto, nome, default) / 100)


def incantesimo_val(incantesimo, contesto, nome, chiave, default=None):
    """Legge un valore di tuning di un incantesimo."""
    return incantesimo_cfg(incantesimo, contesto, nome).get(chiave, default)


def effetto_cfg(effetto, contesto, nome):
    """Restituisce la configurazione di un effetto temporaneo."""
    return EFFETTI_CONFIG.get(effetto, {}).get(contesto, {}).get(nome, {})


def effetto_val(effetto, contesto, nome, chiave, default=None):
    """Legge un valore di tuning di un effetto temporaneo."""
    return effetto_cfg(effetto, contesto, nome).get(chiave, default)
'''

marker = '\n\ndef dungeon_cfg(stanza, azione="evento"):\n'
if marker not in nft:
    raise SystemExit("marker dungeon_cfg non trovato")
nft = nft.replace(marker, helper + marker, 1)

renderer = r'''

def _valore_placeholder_incantesimo(nome, percorso):
    valore = INCANTESIMI_CONFIG.get(nome, {})
    for parte in percorso.split("."):
        if not isinstance(valore, dict) or parte not in valore:
            raise KeyError(f"Placeholder incantesimo non valido: {nome}.{percorso}")
        valore = valore[parte]
    return valore


def render_frase_incantesimo_tecnica(nome):
    template = FRASI_INCANTESIMI_TECNICHE.get(nome, "")
    if not template:
        return ""
    parti = []
    for letterale, campo, formato, conversione in string.Formatter().parse(template):
        parti.append(letterale)
        if campo is None:
            continue
        if conversione:
            raise ValueError(f"Conversione placeholder non supportata: {conversione}")
        valore = _valore_placeholder_incantesimo(nome, campo)
        parti.append(_format_placeholder_set(valore, formato))
    return "".join(parti)


def descrizione_incantesimo_tecnica(nome):
    """Descrizione umana dell'incantesimo, allineata a INCANTESIMI_CONFIG."""
    righe = ["⚙️ Dettagli dell'incantesimo"]
    frase = render_frase_incantesimo_tecnica(nome)
    if frase:
        righe.append(frase)
    return "\n".join(righe)
'''

marker = "\n\ndef aggiorna_descrizioni_bilanciamento(liste_module):\n"
if marker not in nft:
    raise SystemExit("marker aggiorna_descrizioni_bilanciamento non trovato")
nft = nft.replace(marker, renderer + marker, 1)

old_markers = 'markers = ("\\n\\n⚙️ Dettagli tecnici", "\\n\\n⚙️ Dettagli del set", "\\n\\n⚙️ Dettagli dell\'anello")'
new_markers = 'markers = ("\\n\\n⚙️ Dettagli tecnici", "\\n\\n⚙️ Dettagli del set", "\\n\\n⚙️ Dettagli dell\'anello", "\\n\\n⚙️ Dettagli dell\'incantesimo")'
nft = replace_once(nft, old_markers, new_markers, "marker descrizioni")

book_loop = r'''

    for _, dati_libro in getattr(liste_module, "libri", {}).items():
        effetto = dati_libro.get("ef")
        if effetto not in INCANTESIMI_CONFIG:
            continue
        base = dati_libro.get("descrizione", "")
        for marker in markers:
            base = base.split(marker, 1)[0]
        base = base.rstrip()
        dati_libro["descrizione"] = base + "\n\n" + descrizione_incantesimo_tecnica(effetto)
'''
marker = "\n\ndef testo_lista_set(liste_module):\n"
if marker not in nft:
    raise SystemExit("marker testo_lista_set non trovato")
nft = nft.replace(marker, book_loop + marker, 1)

# Proc e valori degli incantesimi: manteniamo gli stessi random già estratti.
nft = replace_once(nft, "if 'Urlo di drago' in main[\"incantamenti\"] and 0.05 > num:", "if 'Urlo di drago' in main[\"incantamenti\"] and incantesimo_ok(num, \"Urlo di drago\", \"turno\", \"terrore\"):", "Urlo di drago")
nft = replace_once(nft, 'if "Mimico" in main["incantamenti"]:', 'if "Mimico" in main["incantamenti"] and incantesimo_val("Mimico", "turno", "copia", "attivo", True):', "Mimico")
nft = replace_once(nft, "if 'Legaccio' in main[\"incantamenti\"] and 0.05 > num:", "if 'Legaccio' in main[\"incantamenti\"] and incantesimo_ok(num, \"Legaccio\", \"turno\", \"lega\"):", "Legaccio proc")
nft = replace_once(nft, 'oppo["agi"] = oppo["agi"] * 0.75', 'oppo["agi"] = oppo["agi"] * incantesimo_val("Legaccio", "turno", "lega", "agi_target_mul")', "Legaccio valore")
nft = replace_once(nft, 'if "Affilatezza" in main["incantamenti"] and 0.1 > num:', 'if "Affilatezza" in main["incantamenti"] and incantesimo_ok(num, "Affilatezza", "turno", "affila"):', "Affilatezza proc")
nft = replace_once(nft, 'main["atk"] = main["atk"] * 1.2', 'main["atk"] = main["atk"] * incantesimo_val("Affilatezza", "turno", "affila", "atk_mul")', "Affilatezza valore")
nft = replace_once(nft, 'dps = dps * 10', 'dps = dps * incantesimo_val("Legione", "turno", "duello_legione", "dps_mul")', "Legione valore")
nft = replace_once(nft, 'if "Ingrossamento" in main["incantamenti"] and 0.02 > num:', 'if "Ingrossamento" in main["incantamenti"] and incantesimo_ok(num, "Ingrossamento", "turno", "crescita"):', "Ingrossamento proc")
nft = replace_once(nft, 'main["atk"] += random.randint(20,100)', 'main["atk"] += random.randint(incantesimo_val("Ingrossamento", "turno", "crescita", "atk_min"), incantesimo_val("Ingrossamento", "turno", "crescita", "atk_max"))', "Ingrossamento ATK")
nft = replace_once(nft, 'main["agi"] += random.randint(-20,-2)', 'main["agi"] += random.randint(incantesimo_val("Ingrossamento", "turno", "crescita", "agi_min"), incantesimo_val("Ingrossamento", "turno", "crescita", "agi_max"))', "Ingrossamento AGI")
nft = replace_once(nft, 'if "Icore" in main["incantamenti"] and 0.05 > num:', 'if "Icore" in main["incantamenti"] and incantesimo_ok(num, "Icore", "turno", "penetrazione"):', "Icore proc")
nft = replace_once(nft, 'difesan = difesan * 0.6', 'difesan = difesan * incantesimo_val("Icore", "turno", "penetrazione", "difesa_target_mul")', "Icore valore")
nft = replace_once(nft, 'dps = dps * 0.8', 'dps = dps * incantesimo_val("Predominio", "turno", "difesa", "dps_attaccante_mul")', "Predominio DPS")
nft = replace_once(nft, 'agi += 30', 'agi += incantesimo_val("Predominio", "turno", "difesa", "agi_attaccante")', "Predominio AGI")
nft = replace_once(nft, 'if "Duraturo" in oppo["incantamenti"] and 0.1 > num:', 'if "Duraturo" in oppo["incantamenti"] and incantesimo_ok(num, "Duraturo", "turno", "difesa"):', "Duraturo proc")
nft = replace_once(nft, 'difesan = difesan * 1.7', 'difesan = difesan * incantesimo_val("Duraturo", "turno", "difesa", "difesa_mul")', "Duraturo valore")
nft = replace_once(nft, 'if "Multiplo" in oppo["incantamenti"] and 0.1 > num:', 'if "Multiplo" in oppo["incantamenti"] and incantesimo_ok(num, "Multiplo", "turno", "difesa"):', "Multiplo proc")
nft = replace_once(nft, 'agin += 8', 'agin += incantesimo_val("Multiplo", "turno", "difesa", "agi")', "Multiplo valore")

nft = replace_once(nft, 'danno = round(danno + (danno * 0.7))', 'danno = round(danno * incantesimo_val("Primo impatto", "turno", "primo_colpo", "danno_mul"))', "Primo impatto")
nft = replace_once(nft, "if 'Critico' in main[\"incantamenti\"] and 0.08 > num:", "if 'Critico' in main[\"incantamenti\"] and incantesimo_ok(num, \"Critico\", \"turno\", \"critico\"):", "Critico proc")
nft = replace_once(nft, 'danno = round(danno + (danno * 0.5))', 'danno = round(danno * incantesimo_val("Critico", "turno", "critico", "danno_mul"))', "Critico valore")
nft = replace_once(nft, 'if "Velenoso" in main["incantamenti"] and 0.05 > num:', 'if "Velenoso" in main["incantamenti"] and incantesimo_ok(num, "Velenoso", "turno", "veleno"):', "Velenoso proc")
nft = replace_once(nft, 'oppo["veleno"] += 1', 'oppo["veleno"] += incantesimo_val("Velenoso", "turno", "veleno", "stack")', "Velenoso stack")
nft = replace_once(nft, 'oppo["veleno"] = 1', 'oppo["veleno"] = incantesimo_val("Velenoso", "turno", "veleno", "stack")', "Velenoso iniziale")
nft = replace_once(nft, 'oppo["hp"] -= oppo["veleno"] * 5', 'oppo["hp"] -= oppo["veleno"] * incantesimo_val("Velenoso", "turno", "veleno", "danno_per_stack")', "Velenoso danno")

old_min = '''if "Minimista" in main["incantamenti"] and mod <= 0:\n        mod = 0.1\n        text += "+"\n        if danno <= 0:\n            danno = 10'''
new_min = '''if "Minimista" in main["incantamenti"] and mod <= 0:\n        mod = incantesimo_val("Minimista", "turno", "danno_minimo", "mod_min")\n        text += "+"\n        if danno <= 0:\n            danno = incantesimo_val("Minimista", "turno", "danno_minimo", "danno_base_min")'''
nft = replace_once(nft, old_min, new_min, "Minimista")

nft = replace_once(nft, 'if "Iridescente" in oppo["incantamenti"] and 0.05 > num:', 'if "Iridescente" in oppo["incantamenti"] and incantesimo_ok(num, "Iridescente", "turno", "cura"):', "Iridescente proc")
nft = replace_once(nft, 'oppo["hp"] += 85', 'oppo["hp"] += incantesimo_val("Iridescente", "turno", "cura", "cura")', "Iridescente cura")

old_speranza = 'if "Speranza" in oppo["incantamenti"] and oppo["hp"] <= 60 and oppo["hp"] >= 1:\n                oppo["hp"] = 100'
new_speranza = 'if "Speranza" in oppo["incantamenti"] and oppo["hp"] <= incantesimo_val("Speranza", "turno", "salvezza", "hp_max") and oppo["hp"] >= incantesimo_val("Speranza", "turno", "salvezza", "hp_min"):\n                oppo["hp"] = incantesimo_val("Speranza", "turno", "salvezza", "hp_porta_a")'
nft = replace_once(nft, old_speranza, new_speranza, "Speranza")

nft = replace_once(nft, 'if "Smateriabile" in oppo["incantamenti"] and 0.1 > num:', 'if "Smateriabile" in oppo["incantamenti"] and incantesimo_ok(num, "Smateriabile", "turno", "annulla_colpo"):', "Smateriabile normale")
nft = replace_count(nft, 'if "Smateriabile" in oppo["incantamenti"] and 0.3 > num:', 'if "Smateriabile" in oppo["incantamenti"] and incantesimo_ok(num, "Smateriabile", "turno", "tempesta_sabbia"):', 2, "Smateriabile sabbia")
nft = replace_once(nft, 'if "Smateriabile" in oppo["incantamenti"] and num < (proc_val(set, "turno", "muori_insetto", "smateriabile_proc") / 100):', 'if "Smateriabile" in oppo["incantamenti"] and incantesimo_val("Smateriabile", "interazioni", "fire_lord", "blocca", False):', "Smateriabile Fire lord")

nft = replace_once(nft, 'if "Tocco fantasma" in main["incantamenti"] and 0.02 > num:', 'if "Tocco fantasma" in main["incantamenti"] and incantesimo_ok(num, "Tocco fantasma", "turno", "colpo_schivato"):', "Tocco fantasma proc")
old_tocco = 'danni = round(dps / 10 * random.uniform(0.5, 1))\n                    if danni <= 30:\n                        danni = 30'
new_tocco = 'danni = round(dps * random.uniform(incantesimo_val("Tocco fantasma", "turno", "colpo_schivato", "dps_percento_min"), incantesimo_val("Tocco fantasma", "turno", "colpo_schivato", "dps_percento_max")) / 100)\n                    if danni <= incantesimo_val("Tocco fantasma", "turno", "colpo_schivato", "danno_min"):\n                        danni = incantesimo_val("Tocco fantasma", "turno", "colpo_schivato", "danno_min")'
nft = replace_once(nft, old_tocco, new_tocco, "Tocco fantasma valori")
nft = replace_once(nft, 'if "Leggiadra" in main["incantamenti"] and 0.1 > num:', 'if "Leggiadra" in main["incantamenti"] and incantesimo_ok(num, "Leggiadra", "turno", "annulla_colpo_proprio"):', "Leggiadra")

old_evo = '''if 'Evocabilità' in user3["incantamenti"]:\n                    text += "Evocazione bomba!\\n"\n                    user1["atk"] += 40\n                    user1["def"] += 40\n                    user1["agi"] += 10'''
new_evo = '''if 'Evocabilità' in user3["incantamenti"]:\n                    text += "Evocazione bomba!\\n"\n                    user1["atk"] += incantesimo_val("Evocabilità", "dungeon", "supporto", "atk")\n                    user1["def"] += incantesimo_val("Evocabilità", "dungeon", "supporto", "def")\n                    user1["agi"] += incantesimo_val("Evocabilità", "dungeon", "supporto", "agi")'''
nft = replace_once(nft, old_evo, new_evo, "Evocabilità")

# Necron: ripristina l'effetto storico corretto, 1000 HP.
old_necron = '''elif necron and player["hp"] <= 0:\n        text += "\\\n**Il nucleo necron sprigiona un aura oscura che riporta in vita il malcapitato, per ora...**"\n        player["hp"] = proc_val(set, "assalto", "resurrezione", "hp")'''
new_necron = '''elif necron and player["hp"] <= 0:\n        text += "\\\n**Il nucleo necron sprigiona un aura oscura che riporta in vita il malcapitato, per ora...**"\n        player["hp"] = 1000'''
nft = replace_once(nft, old_necron, new_necron, "resurrezione Necron")

nft_path.write_text(nft, encoding="utf-8")


# -----------------------------------------------------------------------------
# __init__.py: Fortunello usa il livello del giocatore corretto
# -----------------------------------------------------------------------------
init_path = Path("__init__.py")
init = init_path.read_text(encoding="utf-8")
old_fortunello = '''    if "Fortunello" in a["scheda"]["boost"]["sfida"]:\n        possibilia += 0.05 * a["scheda"]["boost"]["sfida"]["Fortunello"]["lv"]\n        \n    if "Fortunello" in b["scheda"]["boost"]["sfida"]:\n        possibilib += 0.05 * a["scheda"]["boost"]["sfida"]["Fortunello"]["lv"]'''
new_fortunello = '''    bonus_fortunello = nft.effetto_val("Fortunello", "sfida", "premio_oggetto", "bonus_probabilita_per_livello_pct") / 100\n    if "Fortunello" in a["scheda"]["boost"]["sfida"]:\n        possibilia += bonus_fortunello * a["scheda"]["boost"]["sfida"]["Fortunello"].get("lv", 0)\n        \n    if "Fortunello" in b["scheda"]["boost"]["sfida"]:\n        possibilib += bonus_fortunello * b["scheda"]["boost"]["sfida"]["Fortunello"].get("lv", 0)'''
init = replace_once(init, old_fortunello, new_fortunello, "Fortunello")
init_path.write_text(init, encoding="utf-8")

print("Trasformazione completata")

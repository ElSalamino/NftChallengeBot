from pathlib import Path


def replace_once(path, old, new):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"Blocco non trovato in {path}: {old[:100]!r}")
    if text.count(old) != 1:
        raise SystemExit(f"Blocco non univoco in {path}: {text.count(old)} occorrenze")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_once(
    "bilanciamento.py",
    '''    "Cangiante": {\n        "turno": {\n            "attacco": {"proc": 99},\n            "difesa": {"proc": 99},\n        },\n    },''',
    '''    "Cangiante": {\n        "generale": {\n            "selezione_set": {"escludi_solo_bonus_base": True},\n        },\n        "turno": {\n            "attacco": {"proc": 99},\n            "difesa": {"proc": 99},\n        },\n    },''',
)

replace_once(
    "nft.py",
    '''def incantesimo_val(incantesimo, contesto, nome, chiave, default=None):\n    """Legge un valore di tuning di un incantesimo."""\n    return incantesimo_cfg(incantesimo, contesto, nome).get(chiave, default)\n''',
    '''def incantesimo_val(incantesimo, contesto, nome, chiave, default=None):\n    """Legge un valore di tuning di un incantesimo."""\n    return incantesimo_cfg(incantesimo, contesto, nome).get(chiave, default)\n\n\ndef set_cangiante_disponibili():\n    """Set copiabili da Cangiante: esclude quelli che forniscono solo bonus base alle statistiche."""\n    escludi_solo_bonus = incantesimo_val(\n        "Cangiante", "generale", "selezione_set", "escludi_solo_bonus_base", True\n    )\n    return [\n        nome_set\n        for nome_set in classi\n        if not (\n            escludi_solo_bonus\n            and proc_val(nome_set, "generale", "set_base", "solo_bonus_base", False)\n        )\n    ]\n''',
)

text = Path("nft.py").read_text(encoding="utf-8")
old = 'random.choice(list(classi))'
if text.count(old) != 2:
    raise SystemExit(f"Attese 2 estrazioni Cangiante da classi, trovate {text.count(old)}")
Path("nft.py").write_text(text.replace(old, 'random.choice(set_cangiante_disponibili())'), encoding="utf-8")

replace_once(
    "frasi_incantesimi.py",
    '''    "Cangiante": "Quando attacchi hai il {turno.attacco.proc:pct} di assumere un set casuale e quando difendi hai il {turno.difesa.proc:pct}. Il nuovo set sostituisce quello usato nella copia dello scontro fino alla successiva attivazione di Cangiante.",''',
    '''    "Cangiante": "Quando attacchi hai il {turno.attacco.proc:pct} di assumere un set casuale e quando difendi hai il {turno.difesa.proc:pct}. I set che danno soltanto statistiche base vengono esclusi dall'estrazione: Cangiante copia le abilità del set, non i suoi bonus base. Il nuovo set resta nella copia dello scontro fino alla successiva attivazione.",''',
)

replace_once(
    "liste.py",
    '''"Le migliori location per il surf": {"ef": "Onde dell'abisso", "descrizione": "Impara a mimetizzarti tra le persone e le giungle ti lasceranno in pace."},''',
    '''"Le migliori location per il surf": {"ef": "Onde dell'abisso", "descrizione": "Cavalca le onde dell'abisso e lascia che sia il mare a sfondare le difese davanti a te."},''',
)

print("Filtro Cangiante e descrizione Onde applicati")

from pathlib import Path


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: attesa 1 occorrenza, trovate {count}")
    return text.replace(old, new, 1)


# ============================================================
# bilanciamento.py
# ============================================================
path = Path("bilanciamento.py")
text = path.read_text(encoding="utf-8")

replacements = [
    ("'assalto': {'tridente': {'proc': 50, 'danno': 80, 'hp_min': 80}}",
     "'assalto': {'tridente': {'proc': 80, 'danno': 80, 'decremento': 10, 'hp_min': 80}}",
     "Lanciatore olimpico"),
    ("'assalto': {'distrazione': {'proc': 10, 'agi': 10}}",
     "'assalto': {'distrazione': {'proc': 100, 'agi': 10}}",
     "Manipolatore di morte"),
    ("'assalto': {'massa_nemici': {'proc': 30, 'atk_per_nemico': 5, 'def_per_nemico': 5}}",
     "'assalto': {'massa_nemici': {'proc': 100, 'atk_per_nemico': 5, 'def_per_nemico': 5}}",
     "Cacciatore della feccia"),
    ("'assalto': {'bersaglio_enorme': {'agi': 30}}",
     "'assalto': {'bersaglio_enorme': {'agi': 130}}",
     "Serial killer"),
    ("'assalto': {'cannoncino': {'proc': 50, 'def': 70}}",
     "'assalto': {'cannoncino': {'proc': 100, 'def': 70}}",
     "Cercatore di reliquie"),
    ("'assalto': {'fabbro': {'proc': 30, 'atk_per_livello': 5, 'def_per_livello': 5}}",
     "'assalto': {'fabbro': {'proc': 100, 'atk_per_livello': 5, 'def_per_livello': 5}}",
     "Arciere di prima linea"),
    ("'assalto': {'spumeggiante': {'proc': 35, 'agi_difesa': -40}}",
     "'assalto': {'spumeggiante': {'proc': 50, 'agi_difesa': -40}}",
     "Uomo di classe"),
    ("'assalto': {'carapace': {'proc': 10, 'def': 35}}",
     "'assalto': {'carapace': {'proc': 50, 'def': 35}}",
     "Maestro delle tartarughe"),
    ("'assalto': {'fauna': {'proc': 10, 'atk': 35}}",
     "'assalto': {'fauna': {'proc': 50, 'atk': 35}}",
     "Difensore delle mareggiate"),
    ("'assalto': {'vitalita': {'hp': 5}}",
     "'assalto': {'vitalita': {'hp': 55}}",
     "Uomo di un tempo"),
    ("'assalto': {'cura': {'proc': 10, 'cura': 15}}",
     "'assalto': {'cura': {'proc': 100, 'cura': 150}}",
     "Chierico"),
    ("'assalto': {'cura': {'proc': 10, 'cura': 50}}",
     "'assalto': {'cura': {'proc': 100, 'cura': 500}}",
     "Medico improvvisato"),
    ("'assalto': {'cura': {'proc': 20, 'cura': 7}}",
     "'assalto': {'cura': {'proc': 100, 'cura': 70}}",
     "Guaritore da campo"),
    ("'assalto': {'natura': {'proc': 30, 'atk': 15, 'def': 15, 'agi': 7}}",
     "'assalto': {'natura': {'proc': 80, 'atk': 15, 'def': 15, 'agi': 7}}",
     "Druido della selva"),
    ("'assalto': {'previsione': {'proc': 30, 'agi': 60}}",
     "'assalto': {'previsione': {'proc': 100, 'agi': 60}}",
     "Cacciatore di bestie"),
    ("'assalto': {'pipistrello': {'proc': 20, 'agi': 30}}",
     "'assalto': {'pipistrello': {'proc': 100, 'agi': 30}}",
     "Vampiro"),
    ("'assalto': {'adrenalina': {'proc': 30, 'atk': 20}}",
     "'assalto': {'adrenalina': {'proc': 100, 'atk': 20}}",
     "Ricercatore del pericolo"),
    ("'assalto': {'alberelli': {'proc': 20, 'bonus_atk_nemici': -20}}",
     "'assalto': {'alberelli': {'proc': 100, 'bonus_atk_nemici': -20}}",
     "Abitante"),
    ("'assalto': {'copie': {'proc': 15, 'agi_difesa': -30}}",
     "'assalto': {'copie': {'proc': 50, 'agi_difesa': -30}}",
     "Illusionista"),
    ("'assalto': {'paura': {'proc': 30, 'bonus_def_nemico': -10}}",
     "'assalto': {'paura': {'proc': 50, 'bonus_def_nemico': -150}}",
     "Ultima speranza"),
    ("'assalto': {'sangue': {'proc': 12, 'divisore_atk': 8, 'divisore_def': 8}}",
     "'assalto': {'sangue': {'proc': 80, 'divisore_atk': 8, 'divisore_def': 8}}",
     "Sanguinolento"),
]

for old, new, label in replacements:
    text = replace_once(text, old, new, label)

path.write_text(text, encoding="utf-8")


# ============================================================
# nft.py
# ============================================================
path = Path("nft.py")
text = path.read_text(encoding="utf-8")

old_lanciatore = '''        elif set == 'Lanciatore olimpico' and proc_ok(num, set, "assalto", "tridente"):
            if nemico[target]["hp"] > proc_val(set, "assalto", "tridente", "hp_min"):
                nemico[target]["hp"] -= proc_val(set, "assalto", "tridente", "danno")
                text += f"{nome} lancia il tridente fortissimo e colpisce {target}!\\n"
'''

new_lanciatore = '''        elif set == 'Lanciatore olimpico' and proc_ok(num, set, "assalto", "tridente"):
            cfg_tridente = proc_cfg(set, "assalto", "tridente")
            danno_tridente = cfg_tridente["danno"]
            if target in nemico and nemico[target]["hp"] > cfg_tridente["hp_min"]:
                try:
                    indice_target = order.index(target)
                except ValueError:
                    indice_target = -1

                bersagli_tridente = order[indice_target:] if indice_target >= 0 else [target]
                for struttura_tridente in bersagli_tridente:
                    if danno_tridente <= 0:
                        break
                    if struttura_tridente not in nemico or struttura_tridente == "inguerra":
                        continue
                    nemico[struttura_tridente]["hp"] -= danno_tridente
                    player["fatto"] += danno_tridente
                    text += f"{nome} lancia il tridente fortissimo e colpisce {struttura_tridente} per {danno_tridente} danni!\\n"
                    danno_tridente -= cfg_tridente["decremento"]
'''
text = replace_once(text, old_lanciatore, new_lanciatore, "logica Lanciatore olimpico")

old_gate = '''    if anello != None:
        for pl in clan[team]['membri']:
'''
new_gate = '''    if clan[team].get("membri"):
        for pl in clan[team]['membri']:
'''
text = replace_once(text, old_gate, new_gate, "gate aure anelli e Re dei pirati")

path.write_text(text, encoding="utf-8")


# ============================================================
# frasi_set.py
# ============================================================
path = Path("frasi_set.py")
text = path.read_text(encoding="utf-8")
old_frase = '    "Lanciatore olimpico": "In assalto hai il {assalto.tridente.proc:pct} di centrare in pieno la struttura con il tridente e infliggere {assalto.tridente.danno} danni.",'
new_frase = '    "Lanciatore olimpico": "In assalto hai il {assalto.tridente.proc:pct} di iniziare una raffica se la struttura scelta ha più di {assalto.tridente.hp_min} HP: il primo tridente infligge {assalto.tridente.danno} danni e poi colpisce le strutture successive perdendo {assalto.tridente.decremento} danni a ogni passaggio, fino a 0 o alla fine delle strutture.",'
text = replace_once(text, old_frase, new_frase, "frase Lanciatore olimpico")
path.write_text(text, encoding="utf-8")

print("Patch assalto applicata")

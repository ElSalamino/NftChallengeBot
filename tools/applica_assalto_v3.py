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
    ("'assalto': {'terrore_clone': {'proc': 15, 'atk_clone': -30, 'def_clone': -50}}", "'assalto': {'terrore_clone': {'proc': 100, 'atk_clone': -30, 'def_clone': -50}}", "Ghoul"),
    ("'assalto': {'laser': {'proc': 80}}", "'assalto': {'laser': {'proc': 100}}", "Contrabbandiere"),
    ("'assalto': {'cannoncino': {'proc': 50}}", "'assalto': {'cannoncino': {'proc': 100}}", "IppoFan"),
    ("'assalto': {'fabbro': {'proc': 90, 'atk': 30, 'def': 20}}", "'assalto': {'fabbro': {'proc': 100, 'atk': 30, 'def': 20}}", "Campione del sole"),
    ("'assalto': {'cucciolo': {'proc': 10, 'atk': 50}}", "'assalto': {'cucciolo': {'proc': 100, 'atk': 50}}", "Drago"),
    ("'assalto': {'fabbro': {'proc': 30}}", "'assalto': {'fabbro': {'proc': 100}}", "Anima oscura"),
    ("'assalto': {'cucciolo_drago': {'proc': 12, 'atk': 33}}", "'assalto': {'cucciolo_drago': {'proc': 100, 'atk': 33}}", "PiroIncantatore"),
    ("'assalto': {'accampamento': {'proc': 10, 'atk': 20}}", "'assalto': {'accampamento': {'proc': 100, 'atk': 20}}", "Cercatore"),
    ("'assalto': {'spuntone_schivato': {'proc': 30, 'def': 22, 'atk': 22},\n                                       'spuntone_colpito': {'proc': 30, 'def': 33}}", "'assalto': {'spuntone_schivato': {'proc': 100, 'def': 22, 'atk': 22},\n                                       'spuntone_colpito': {'proc': 100, 'def': 33}}", "Cavaliere delle spine"),
    ("'assalto': {'clone': {'proc': 20}}", "'assalto': {'clone': {'proc': 100}}", "Regina golgari"),
    ("'assalto': {'cane': {'proc': 10}}", "'assalto': {'cane': {'proc': 100}}", "Juggernaut"),
    ("'assalto': {'cucciolo': {'proc': 15}}", "'assalto': {'cucciolo': {'proc': 100}}", "Guerriero 3D"),
    ("'assalto': {'centrale': {'proc': 90, 'atk': 150}}", "'assalto': {'centrale': {'proc': 100, 'atk': 150}}", "Ombra silenziosa"),
    ("'assalto': {'muraglione': {'proc': 50, 'moltiplicatore_extra': 4}}", "'assalto': {'muraglione': {'proc': 100, 'moltiplicatore_extra': 9}}", "Crociato"),
    ("'assalto': {'draghetto': {'proc': 50, 'dps': 1000}}", "'assalto': {'draghetto': {'proc': 100, 'dps': 1000}}", "Cacciatore"),
    ("'assalto': {'clone': {'proc': 50, 'dps': 1000}}", "'assalto': {'clone': {'proc': 100, 'dps': 1000}}", "Spacca Mostri"),
    ("'assalto': {'cannoncino': {'proc': 30, 'dps': 1400}}", "'assalto': {'cannoncino': {'proc': 100, 'dps': 1400}}", "Primo alla bandiera"),
    ("'assalto': {'drago_scaccia_drago': {'proc': 50, 'dps': 700}}", "'assalto': {'drago_scaccia_drago': {'proc': 100, 'dps': 700}}", "Ice and fire"),
    ("'assalto': {'spada_beta': {'proc': 20, 'dps': 1033}}", "'assalto': {'spada_beta': {'proc': 20, 'dps': 1333}}", "Betatester"),
    ("'assalto': {'maledizione': {'proc': 40, 'percento_hp': 8}}", "'assalto': {'maledizione': {'proc': 100, 'percento_hp': 8}}", "Maledetto"),
    ("'assalto': {'doppio_colpo': {'proc': 20, 'denominatore': 55, 'random_min': 0.7, 'random_max': 1.3}}", "'assalto': {'doppio_colpo': {'proc': 100, 'denominatore': 55, 'random_min': 0.7, 'random_max': 1.3}}", "Shogun moderno"),
    ("'assalto': {'raggio_lunare': {'proc': 20, 'denominatore': 75, 'random_min': 1, 'random_max': 1.7}}", "'assalto': {'raggio_lunare': {'proc': 100, 'denominatore': 75, 'random_min': 1, 'random_max': 1.7}}", "Combattente 2D"),
    ("'assalto': {'cura_target': {'proc': 70}}", "'assalto': {'cura_target': {'proc': 80}}", "Pazzoide glamour"),
    ("'assalto': {'target': {'proc': 20,", "'assalto': {'target': {'proc': 80,", "Bug Abuser"),
    ("'assalto': {'ultimo_colpo': {'proc': 8, 'danno': 100, 'hp_min': 100}}", "'assalto': {'ultimo_colpo': {'proc': 80, 'danno': 100, 'hp_min': 100}}", "Cultista pazzo"),
    ("'assalto': {'danno_fisso': {'danno': 15}}", "'assalto': {'danno_fisso': {'hp_massimi_divisore': 100, 'danno_minimo': 75}}", "Cavaliere d'argento"),
    ("'assalto': {'esplosione_morte': {'proc': 60, 'danno_struttura': 45, 'hp_min_struttura': 45}}", "'assalto': {'esplosione_morte': {'proc': 1000, 'hp_massimi_divisore': 100, 'danno_minimo': 45}}", "Fiamma pura"),
]

for old, new, label in replacements:
    text = replace_once(text, old, new, label)

# Anelli d'assalto: aura = max(minimo, percentuale stat proprietario)
text = replace_once(
    text,
    '"Scudo levitante": {\n        "assalto": {"aura": {"stat": "def", "valore": 20}},\n    },\n    "Stemma del leader": {\n        "assalto": {"aura": {"stat": "atk", "valore": 20}},\n    },\n    "Occhio del falco": {\n        "assalto": {"aura": {"stat": "agi", "valore": 5}},\n    },\n    "Carica mobile": {\n        "assalto": {"esplosione": {"proc": 20, "danno_min": 20, "danno_max": 150}},\n    },',
    '"Scudo levitante": {\n        "assalto": {"aura": {"stat": "def", "minimo": 20, "percento_stat": 1}},\n    },\n    "Stemma del leader": {\n        "assalto": {"aura": {"stat": "atk", "minimo": 20, "percento_stat": 1}},\n    },\n    "Occhio del falco": {\n        "assalto": {"aura": {"stat": "agi", "minimo": 20, "percento_stat": 1}},\n    },\n    "Carica mobile": {\n        "assalto": {"esplosione": {"proc": 50, "danno_min": 20, "danno_max": 150}},\n    },',
    "anelli assalto",
)

# Config nuclei centralizzata.
marker = "\n\n# ============================================================\n# DATABASE HARDCODATO DUNGEON\n"
nuclei_config = '''\n\n# ============================================================\n# DATABASE HARDCODATO DEI NUCLEI\n# ============================================================\nNUCLEI_CONFIG = {\n    "Nucleo elettrico instabile": {"assalto": {"stat_per_membro": {"agi": 30}}},\n    "Nucleo marittimo instabile": {"assalto": {"stat_per_membro": {"hp": 300}}},\n    "Nucleo demoniaco instabile": {"assalto": {"stat_per_membro": {"atk": 80}}},\n    "Nucleo terrestre instabile": {"assalto": {"stat_per_membro": {"def": 80}}},\n    "Nucleo selvaggio instabile": {\n        "assalto": {"stat_per_membro": {"hp": 30, "atk": 30, "def": 30, "agi": 5}}\n    },\n    "Nucleo di bacon instabile": {"assalto": {"cura_per_struttura": 11}},\n    "Nucleo Necron instabile": {"assalto": {"resurrezione": {"proc": 8, "hp": 1000}}},\n}\n'''
if "NUCLEI_CONFIG =" not in text:
    text = replace_once(text, marker, nuclei_config + marker, "inserimento NUCLEI_CONFIG")

path.write_text(text, encoding="utf-8")


# ============================================================
# nft.py
# ============================================================
path = Path("nft.py")
text = path.read_text(encoding="utf-8")

text = replace_once(
    text,
    "from bilanciamento import PROC_CLASSI, PROC_ANELLI, DUNGEON_CONFIG, INCANTESIMI_CONFIG, EFFETTI_CONFIG",
    "from bilanciamento import PROC_CLASSI, PROC_ANELLI, NUCLEI_CONFIG, DUNGEON_CONFIG, INCANTESIMI_CONFIG, EFFETTI_CONFIG",
    "import NUCLEI_CONFIG",
)

old_nuclei = '''    num = random.random()\n    bacon = False\n    necron = False\n    if "nucleo" in clan[team]:\n        nuc = clan[team]["nucleo"]\n        text += f"\\nIl nucleo {nuc} sprigiona la sua forza!\\n\\n"\n        \n        if nuc not in nuclei:\n            print(nuc)\n        elif nuc == "Nucleo elettrico instabile":\n                player["agi"] += 25\n        elif nuc == "Nucleo marittimo instabile":\n                player["hp"] += 300\n        elif nuc == "Nucleo demoniaco instabile":\n                player["atk"] += 185\n        elif nuc == "Nucleo terrestre instabile":\n                player["def"] += 185\n        elif nuc == "Nucleo selvaggio instabile":\n                player["agi"] += 5\n                player["hp"] += 30\n                player["atk"] += 25\n                player["def"] += 25\n        elif clan[team]["nucleo"] == "Nucleo di bacon instabile":\n                bacon = True\n        elif nuc == "Nucleo Necron instabile" and 0.08 > num:\n            necron = True\n'''
new_nuclei = '''    num = random.random()\n    bacon = False\n    necron = False\n    nuc = clan[team].get("nucleo")\n    numero_membri_clan = len(clan[team].get("membri", []))\n    if nuc is not None:\n        text += f"\\nIl nucleo {nuc} sprigiona la sua forza!\\n\\n"\n        cfg_nucleo = NUCLEI_CONFIG.get(nuc, {}).get("assalto", {})\n        if not cfg_nucleo:\n            print(nuc)\n        for stat_nucleo, valore_per_membro in cfg_nucleo.get("stat_per_membro", {}).items():\n            player[stat_nucleo] += numero_membri_clan * valore_per_membro\n        if "cura_per_struttura" in cfg_nucleo:\n            bacon = True\n        cfg_necron = cfg_nucleo.get("resurrezione")\n        if cfg_necron and num < (cfg_necron.get("proc", 0) / 100):\n            necron = True\n\n    # HP massimi dell'assalto: includono omini/set già applicati dal chiamante e il nucleo.\n    hp_massimi_assalto = player["hp"]\n'''
text = replace_once(text, old_nuclei, new_nuclei, "logica nuclei")

old_aure = '''    if clan[team].get("membri"):\n        for pl in clan[team]['membri']:\n            aniel = playerg[pl]["scheda"]["anello"]\n            if aniel in PROC_ANELLI and "aura" in PROC_ANELLI[aniel].get("assalto", {}):\n                cfg_anello = anello_cfg(aniel, "assalto", "aura")\n                stat_anello = cfg_anello["stat"]\n                valore_anello = cfg_anello["valore"]\n                moltiplicatore = 1\n                if set == "Portatore di morte":\n                    moltiplicatore = proc_val(set, "assalto", "bonus_gadget", "moltiplicatore", 2)\n                player[stat_anello] += valore_anello * moltiplicatore\n                if set == "Portatore di morte" and aniel == "Occhio del falco":\n                    text += "L'anello si raddoppia!\\n"\n\n            if playerg[pl]["scheda"]["set"] == "Re dei pirati" and pl != nome:\n'''
new_aure = '''    if clan[team].get("membri"):\n        for pl in clan[team]['membri']:\n            scheda_membro = playerg[pl]["scheda"]\n            aniel = scheda_membro["anello"]\n            if aniel in PROC_ANELLI and "aura" in PROC_ANELLI[aniel].get("assalto", {}):\n                cfg_anello = anello_cfg(aniel, "assalto", "aura")\n                stat_anello = cfg_anello["stat"]\n                stat_proprietario = scheda_membro.get(stat_anello, 0)\n                valore_anello = max(\n                    cfg_anello["minimo"],\n                    stat_proprietario * cfg_anello["percento_stat"] / 100,\n                )\n                moltiplicatore = 1\n                if set == "Portatore di morte":\n                    moltiplicatore = proc_val(set, "assalto", "bonus_gadget", "moltiplicatore", 2)\n                bonus_aura = valore_anello * moltiplicatore\n                player[stat_anello] += bonus_aura\n                bonus_testo = _numero_placeholder_tecnico(bonus_aura)\n                text += f"L'anello di {pl} ti dona {bonus_testo} {stat_anello.upper()}!\\n"\n\n            if scheda_membro["set"] == "Re dei pirati" and pl != nome:\n'''
text = replace_once(text, old_aure, new_aure, "aure anelli")

text = replace_once(
    text,
    '''            if bacon:\n                player["hp"] += 11\n''',
    '''            if bacon:\n                player["hp"] += NUCLEI_CONFIG["Nucleo di bacon instabile"]["assalto"]["cura_per_struttura"]\n''',
    "bacon config",
)

text = replace_once(
    text,
    '''    text += "\\n"\n    for difesa in order:\n''',
    '''    text += "\\n"\n    try:\n        indice_target_ordine = order.index(target)\n    except ValueError:\n        indice_target_ordine = len(order)\n    for difesa in order:\n''',
    "indice target assalto",
)

text = replace_once(
    text,
    '''                        elif set == "Orrido" and proc_ok(num, set, "assalto", "sgignolo"):\n''',
    '''                        elif (\n                            set == "Orrido"\n                            and order.index(difesa) < indice_target_ordine\n                            and proc_ok(num, set, "assalto", "sgignolo")\n                        ):\n''',
    "Orrido prima del target",
)

text = replace_once(
    text,
    '''                        elif (set == "Crociato" and target == "Muraglione extra" and proc_ok(num, set, "assalto", "muraglione")):\n                            text += f"__{nome} grazie al potere della luce incendia questo blocco!__\\n"\n                            dps += dps + dps + dps + dps\n''',
    '''                        elif (set == "Crociato" and target == "Muraglione extra" and proc_ok(num, set, "assalto", "muraglione")):\n                            text += f"__{nome} grazie al potere della luce incendia questo blocco!__\\n"\n                            dps += dps * proc_val(set, "assalto", "muraglione", "moltiplicatore_extra")\n''',
    "Crociato 10x",
)

text = replace_once(
    text,
    '''                        if set == "Cavaliere d'argento":\n                            dannissimi += proc_val(set, "assalto", "danno_fisso", "danno")\n''',
    '''                        if set == "Cavaliere d'argento":\n                            cfg_argento = proc_cfg(set, "assalto", "danno_fisso")\n                            danno_argento = round(max(\n                                hp_massimi_assalto / cfg_argento["hp_massimi_divisore"],\n                                cfg_argento["danno_minimo"],\n                            ))\n                            dannissimi += danno_argento\n''',
    "Cavaliere argento maxhp",
)

text = replace_once(
    text,
    '''    elif necron and player["hp"] <= 0:\n        text += "\\n**Il nucleo necron sprigiona un aura oscura che riporta in vita il malcapitato, per ora...**"\n        player["hp"] = 1000\n''',
    '''    elif necron and player["hp"] <= 0:\n        text += "\\n**Il nucleo necron sprigiona un aura oscura che riporta in vita il malcapitato, per ora...**"\n        player["hp"] = NUCLEI_CONFIG["Nucleo Necron instabile"]["assalto"]["resurrezione"]["hp"]\n''',
    "Necron config hp",
)

old_fiamma = '''    elif set == "Fiamma pura" and player["hp"] <= 0 and proc_ok(num, set, "assalto", "esplosione_morte"):\n        text += f"\\n{nome} esplode in un esplosione di fuoco dannegiando tutte le strutture!"\n        for dife in nemico:\n            if dife == "inguerra":\n                pass\n            else:\n                if nemico[dife]["hp"] > proc_val(set, "assalto", "esplosione_morte", "hp_min_struttura"):\n                    nemico[dife]["hp"] -= proc_val(set, "assalto", "esplosione_morte", "danno_struttura")\n            player["fatto"] += proc_val(set, "assalto", "esplosione_morte", "danno_struttura")\n'''
new_fiamma = '''    elif set == "Fiamma pura" and player["hp"] <= 0 and proc_ok(num, set, "assalto", "esplosione_morte"):\n        text += f"\\n{nome} esplode in un esplosione di fuoco dannegiando tutte le strutture!"\n        cfg_fiamma = proc_cfg(set, "assalto", "esplosione_morte")\n        danno_fiamma = round(max(\n            hp_massimi_assalto / cfg_fiamma["hp_massimi_divisore"],\n            cfg_fiamma["danno_minimo"],\n        ))\n        for dife in list(nemico):\n            if dife == "inguerra":\n                continue\n            if nemico[dife]["hp"] > danno_fiamma:\n                nemico[dife]["hp"] -= danno_fiamma\n                player["fatto"] += danno_fiamma\n'''
text = replace_once(text, old_fiamma, new_fiamma, "Fiamma pura maxhp")

path.write_text(text, encoding="utf-8")


# ============================================================
# frasi_anelli.py
# ============================================================
path = Path("frasi_anelli.py")
text = path.read_text(encoding="utf-8")
text = replace_once(
    text,
    '    "Occhio del falco": "Negli assalti tieni d\'occhio il campo per tutto il clan e aggiungi {assalto.aura.valore:signed} agilità alla squadra.",',
    '    "Occhio del falco": "Negli assalti aiuti ogni compagno con almeno {assalto.aura.minimo} AGI, oppure con il {assalto.aura.percento_stat:pct} della tua AGI se il risultato è maggiore.",',
    "frase Occhio",
)
text = replace_once(
    text,
    '    "Stemma del leader": "Negli assalti guidi il clan in prima linea e dai a tutta la squadra {assalto.aura.valore:signed} attacco.",',
    '    "Stemma del leader": "Negli assalti aiuti ogni compagno con almeno {assalto.aura.minimo} ATK, oppure con il {assalto.aura.percento_stat:pct} del tuo ATK se il risultato è maggiore.",',
    "frase Stemma",
)
text = replace_once(
    text,
    '    "Scudo levitante": "Negli assalti fai da esempio a tutto il clan e regali alla squadra {assalto.aura.valore:signed} difesa.",',
    '    "Scudo levitante": "Negli assalti aiuti ogni compagno con almeno {assalto.aura.minimo} DEF, oppure con il {assalto.aura.percento_stat:pct} della tua DEF se il risultato è maggiore.",',
    "frase Scudo",
)
path.write_text(text, encoding="utf-8")


# ============================================================
# frasi_set.py
# ============================================================
path = Path("frasi_set.py")
text = path.read_text(encoding="utf-8")
text = replace_once(
    text,
    '    "Cavaliere d\'argento": "Se il tuo colpo esce troppo debole, recuperi fino a {turno.recupero_colpo.mod_bonus:signed} sul modificatore. In assalto aggiungi sempre {assalto.danno_fisso.danno} danni.",',
    '    "Cavaliere d\'argento": "Se il tuo colpo esce troppo debole, recuperi fino a {turno.recupero_colpo.mod_bonus:signed} sul modificatore. In assalto, quando il colpo va a segno, aggiungi danno diretto pari al maggiore tra {assalto.danno_fisso.danno_minimo} e un centesimo dei tuoi HP massimi.",',
    "frase Cavaliere argento",
)
text = replace_once(
    text,
    '    "Fiamma pura": "Hai il {turno.arena_brucia.proc:pct} di incendiare entrambi e togliere {turno.arena_brucia.danno_main} HP a testa. Se muori durante un assalto, hai il {assalto.esplosione_morte.proc:pct} di esplodere e fare {assalto.esplosione_morte.danno_struttura} danni alla struttura.",',
    '    "Fiamma pura": "Hai il {turno.arena_brucia.proc:pct} di incendiare entrambi e togliere {turno.arena_brucia.danno_main} HP a testa. Se muori durante un assalto, hai il {assalto.esplosione_morte.proc:pct} di esplodere: ogni struttura con abbastanza vita subisce il maggiore tra {assalto.esplosione_morte.danno_minimo} danni e un centesimo dei tuoi HP massimi.",',
    "frase Fiamma pura",
)
text = replace_once(
    text,
    '    "Crociato": "Se il nemico schiva, hai il {turno.punizione_schivata.proc:pct} di punirlo comunque con almeno {turno.punizione_schivata.danno_min} danni. In assalto il Muraglione ha il {assalto.muraglione.proc:pct} di moltiplicare pesantemente il tuo contributo.",',
    '    "Crociato": "Se il nemico schiva, hai il {turno.punizione_schivata.proc:pct} di punirlo comunque con almeno {turno.punizione_schivata.danno_min} danni. In assalto contro il Muraglione hai il {assalto.muraglione.proc:pct} di aggiungere altre {assalto.muraglione.moltiplicatore_extra} volte il tuo DPS, arrivando a 10× il colpo originale.",',
    "frase Crociato",
)
path.write_text(text, encoding="utf-8")

print("Patch assalto v3 applicata")

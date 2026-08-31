from pathlib import Path

SETS = {
    "Anima persa": ["Bastone del folle", "Anima dispersa"],
    "Disabilitatore provetto": ["Cacciavite multiuso", "Delle squame viscide"],
    "Controllore del cielo": ["Artiglio di Drago", "Ali piumate"],
    "Eterna sventura": ["Guanti di cormorant", "Corona maledetta"],
    "Pescatore alternativo": ["Ascia bipenne", "Cappellino da pescatore"],
    "Esca vivente": ["Canna blu", "Armatura di carne"],
    "Giustiziere a V": ["Frusta telaia", "Armatura del folle"],
}


def append_once(path, marker, block):
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    if marker in s:
        raise SystemExit(f"{marker} gia presente")
    p.write_text(s + "\n\n" + block.strip() + "\n", encoding="utf-8")


append_once("liste.py", "# --- SECONDA ONDATA SET: CATALOGO ---", r'''
# --- SECONDA ONDATA SET: CATALOGO ---
classi.update({
    "Anima persa": ["Bastone del folle", "Anima dispersa"],
    "Disabilitatore provetto": ["Cacciavite multiuso", "Delle squame viscide"],
    "Controllore del cielo": ["Artiglio di Drago", "Ali piumate"],
    "Eterna sventura": ["Guanti di cormorant", "Corona maledetta"],
    "Pescatore alternativo": ["Ascia bipenne", "Cappellino da pescatore"],
    "Esca vivente": ["Canna blu", "Armatura di carne"],
    "Giustiziere a V": ["Frusta telaia", "Armatura del folle"],
})
Approccini.update({
    "Anima persa": ["Conservativo", "Difensivo", "Impavido"],
    "Disabilitatore provetto": ["Aggressivo", "Spinto", "Autorevole"],
    "Controllore del cielo": ["Agile", "Schivo", "Conservativo"],
    "Eterna sventura": ["Malevolo", "Aggressivo", "Vendicativo"],
    "Pescatore alternativo": ["Rischioso", "Aggressivo", "Spavaldo"],
    "Esca vivente": ["Rischioso", "Impavido", "Conservativo"],
    "Giustiziere a V": ["Agile", "Vendicativo", "Spinto"],
})
bonus.update({nome: {"hp": 0, "def": 0, "atk": 0, "agi": 0} for nome in [
    "Anima persa", "Disabilitatore provetto", "Controllore del cielo", "Eterna sventura",
    "Pescatore alternativo", "Esca vivente", "Giustiziere a V"
]})
frasi_set.update({
    "Anima persa": "Non puoi più scappare dal colpo: quando il corpo proverebbe a schivare, l'anima resta e ti regala vita per continuare a combattere.",
    "Disabilitatore provetto": "Viti, cavi e un pessimo rapporto con i muri: in assalto sai esattamente cosa smontare per farli crollare.",
    "Controllore del cielo": "Ogni cura ti porta più in alto: recuperare vita alimenta anche attacco e difesa fino a renderti padrone del cielo.",
    "Eterna sventura": "Ogni colpo può lasciare qualcosa di peggio di una ferita: l'avversario perde lentamente la capacità di reagire.",
    "Pescatore alternativo": "La pesca è secondaria: ogni turno puoi buttare via prudenza e difesa per trasformarti in una macchina d'attacco.",
    "Esca vivente": "La difesa non serve se sei tu l'esca: entri in sfida e in assalto completamente scoperto.",
    "Giustiziere a V": "Il giudizio arriva dopo qualche turno: diventi molto più agile e contro gli accampamenti non conosci mezze misure.",
})
''')

append_once("bilanciamento.py", "# --- SECONDA ONDATA SET: BILANCIAMENTO ---", r'''
# --- SECONDA ONDATA SET: BILANCIAMENTO ---
PROC_CLASSI.update({
    "Anima persa": {"sfida": {"schivata_negata": {"hp": 200}}},
    "Disabilitatore provetto": {"assalto": {"muraglione": {"atk_mul": 4}}},
    "Controllore del cielo": {"sfida": {"cura_in_potere": {"atk_divisore": 2, "def_divisore": 2}}},
    "Eterna sventura": {"sfida": {"sventura": {"proc": 20, "atk_target": -10, "def_target": -10, "agi_target": -10}}},
    "Pescatore alternativo": {"sfida": {"azzardo": {"proc": 50, "atk_mul": 2, "def_mul": 0.5}}},
    "Esca vivente": {"sfida": {"esca": {"def": 0}}, "assalto": {"esca": {"def": 0}}},
    "Giustiziere a V": {"sfida": {"giudizio": {"turno_min": 4, "agi_mul": 2}}, "assalto": {"accampamento": {"atk_mul": 6}}},
})
''')

append_once("frasi_set.py", "# --- SECONDA ONDATA SET: FRASI TECNICHE ---", r'''
# --- SECONDA ONDATA SET: FRASI TECNICHE ---
FRASI_SET_TECNICHE.update({
    "Anima persa": "Sfida: non può schivare. Ogni tiro che sarebbe stato una schivata concede {sfida.schivata_negata.hp} HP e il colpo prosegue normalmente.",
    "Disabilitatore provetto": "ASSALTO — HARD COUNTER del Muraglione extra: se lo scegli come bersaglio, il tuo ATK viene moltiplicato per {assalto.muraglione.atk_mul:x} per quell'assalto.",
    "Controllore del cielo": "Sfida: a fine di ogni turno, se hai guadagnato HP durante quel turno, guadagni ATK pari agli HP recuperati/{sfida.cura_in_potere.atk_divisore} e DEF pari agli HP recuperati/{sfida.cura_in_potere.def_divisore}.",
    "Eterna sventura": "Sfida: quando un tuo colpo va a segno hai il {sfida.sventura.proc:pct} di togliere {sfida.sventura.atk_target:abs} ATK, {sfida.sventura.def_target:abs} DEF e {sfida.sventura.agi_target:abs} AGI all'avversario.",
    "Pescatore alternativo": "Sfida: a ogni tuo turno hai il {sfida.azzardo.proc:pct} di moltiplicare permanentemente per {sfida.azzardo.atk_mul:x} l'ATK e per {sfida.azzardo.def_mul:x} la DEF. I proc successivi si accumulano fino a fine sfida.",
    "Esca vivente": "Sfida: all'inizio la DEF viene impostata a {sfida.esca.def}. Assalto: anche la DEF dell'assaltatore viene impostata a {assalto.esca.def}.",
    "Giustiziere a V": "Sfida: dal proprio turno {sfida.giudizio.turno_min} in poi l'AGI è moltiplicata una volta per {sfida.giudizio.agi_mul:x} e resta così fino a fine sfida. ASSALTO — HARD COUNTER dell'Accampamento: se lo bersagli, ATK ×{assalto.accampamento.atk_mul}.",
})
''')

p = Path("nft.py")
s = p.read_text(encoding="utf-8")
old = "if possibile > random.randint(0, 100):"
if s.count(old) != 1:
    raise SystemExit(f"Tiro schivata inatteso: {s.count(old)}")
s = s.replace(old, "if _tiro_schivata_seconda_ondata(possibile, oppo):", 1)
if "# --- SECONDA ONDATA SET: RUNTIME ---" in s:
    raise SystemExit("Runtime seconda ondata gia presente")
s += r'''

# --- SECONDA ONDATA SET: RUNTIME ---
_turno_seconda_ondata_base = turno
_assedio_seconda_ondata_base = assedio

def _tiro_schivata_seconda_ondata(possibile, difensore):
    successo = possibile > random.randint(0, 100)
    if successo and difensore.get("set") == "Anima persa":
        hp = proc_val("Anima persa", "sfida", "schivata_negata", "hp")
        difensore["hp"] += hp
        difensore["_anima_persa_hp"] = difensore.get("_anima_persa_hp", 0) + hp
        return False
    return successo

def _inizializza_seconda_ondata_sfida(p):
    if p.get("set") == "Esca vivente" and not p.get("_esca_vivente_inizializzata"):
        p["def"] = proc_val("Esca vivente", "sfida", "esca", "def")
        p["_esca_vivente_inizializzata"] = True
        return f"🪱 {p['Nome']} si offre come esca e rinuncia completamente alla difesa!\n"
    return ""

def turno(main, oppo, cond=None):
    if not _e_sfida_pvp(main, oppo, cond):
        return _turno_seconda_ondata_base(main, oppo, cond)
    prefisso = _inizializza_seconda_ondata_sfida(main) + _inizializza_seconda_ondata_sfida(oppo)
    if main.get("set") == "Giustiziere a V":
        main["_giustiziere_turni"] = main.get("_giustiziere_turni", 0) + 1
        if main["_giustiziere_turni"] >= proc_val("Giustiziere a V", "sfida", "giudizio", "turno_min") and not main.get("_giustiziere_agilita_attiva"):
            main["agi"] *= proc_val("Giustiziere a V", "sfida", "giudizio", "agi_mul")
            main["_giustiziere_agilita_attiva"] = True
            prefisso += f"⚖️ {main['Nome']} entra nella fase del giudizio: agilità raddoppiata!\n"
    if main.get("set") == "Pescatore alternativo" and proc_ok(random.random(), "Pescatore alternativo", "sfida", "azzardo"):
        main["atk"] *= proc_val("Pescatore alternativo", "sfida", "azzardo", "atk_mul")
        main["def"] *= proc_val("Pescatore alternativo", "sfida", "azzardo", "def_mul")
        prefisso += f"🎣 {main['Nome']} rischia tutto: attacco raddoppiato e difesa dimezzata!\n"
    hp_prima = {id(main): main.get("hp", 0), id(oppo): oppo.get("hp", 0)}
    fatto_prima = main.get("fatto", 0)
    anima_prima = oppo.get("_anima_persa_hp", 0)
    testo = _turno_seconda_ondata_base(main, oppo, cond)
    anima_dopo = oppo.get("_anima_persa_hp", 0)
    if anima_dopo > anima_prima:
        testo += f"👻 {oppo['Nome']} avrebbe schivato, ma l'Anima persa gli concede {anima_dopo-anima_prima} HP e il colpo continua!\n"
    for combattente in (main, oppo):
        if combattente.get("set") == "Controllore del cielo":
            guadagno = combattente.get("hp", 0) - hp_prima[id(combattente)]
            if guadagno > 0:
                atk_gain = guadagno / proc_val("Controllore del cielo", "sfida", "cura_in_potere", "atk_divisore")
                def_gain = guadagno / proc_val("Controllore del cielo", "sfida", "cura_in_potere", "def_divisore")
                combattente["atk"] += atk_gain
                combattente["def"] += def_gain
                testo += f"🪽 {combattente['Nome']} converte {guadagno:g} HP in +{atk_gain:g} ATK e +{def_gain:g} DEF!\n"
    if main.get("set") == "Eterna sventura" and main.get("fatto", 0) > fatto_prima and not oppo.get("schivato", False) and proc_ok(random.random(), "Eterna sventura", "sfida", "sventura"):
        for stat, key in (("atk", "atk_target"), ("def", "def_target"), ("agi", "agi_target")):
            oppo[stat] += proc_val("Eterna sventura", "sfida", "sventura", key)
        testo += f"☠️ La sventura di {main['Nome']} corrode {oppo['Nome']}: -10 ATK, -10 DEF e -10 AGI!\n"
    return prefisso + testo

def assedio(playerg, player, nemico, target, team, order, clan, meteo=None, setting=dict()):
    prefisso = ""
    nome_set = player.get("set")
    if nome_set == "Esca vivente":
        player["def"] = proc_val("Esca vivente", "assalto", "esca", "def")
        prefisso += "🪱 Ti presenti come esca vivente: difesa azzerata!\n"
    if nome_set == "Disabilitatore provetto" and target == "Muraglione extra":
        player["atk"] *= proc_val("Disabilitatore provetto", "assalto", "muraglione", "atk_mul")
        prefisso += "🔧 Smonti il Muraglione extra pezzo per pezzo: attacco ×4!\n"
    if nome_set == "Giustiziere a V" and target == "Accampamento":
        player["atk"] *= proc_val("Giustiziere a V", "assalto", "accampamento", "atk_mul")
        prefisso += "⚖️ L'Accampamento è sotto giudizio: attacco ×6!\n"
    return prefisso + _assedio_seconda_ondata_base(playerg, player, nemico, target, team, order, clan, meteo, setting)
'''
p.write_text(s, encoding="utf-8")

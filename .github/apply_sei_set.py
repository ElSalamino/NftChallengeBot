from pathlib import Path

MARKER = "# --- QUARTA ONDATA SET: SEI SET ---"

# liste.py
p = Path("liste.py")
text = p.read_text(encoding="utf-8")
if MARKER not in text:
    text += r'''

# --- QUARTA ONDATA SET: SEI SET ---
classi.update({
    "Primo alla torre": ["NotteSferza", "Un machete"],
    "Pazzo temporale": ["Lama temporale", "Maschera del folle"],
    "Evocatore del vero potere": ["Stocco magico", "Piuma vulcanica"],
    "GunSlingher": ["Pistola del west", "Pessime idee"],
    "Arcidemone": ["Zweihander", "Marchio del dannato"],
    "Big Game Hunter": ["Arco pesante", "Un libro su tutte le creature"],
})

Approccini.update({
    "Primo alla torre": ["Aggressivo", "Spinto", "Autorevole"],
    "Pazzo temporale": ["Rischioso", "Ingannevole", "Agile"],
    "Evocatore del vero potere": ["Conservativo", "Autorevole", "Spavaldo"],
    "GunSlingher": ["Aggressivo", "Agile", "Spavaldo"],
    "Arcidemone": ["Malevolo", "Vendicativo", "Aggressivo"],
    "Big Game Hunter": ["Agile", "Conservativo", "Distaccato"],
})

bonus.update({nome: {"hp": 0, "def": 0, "atk": 0, "agi": 0} for nome in [
    "Primo alla torre", "Pazzo temporale", "Evocatore del vero potere",
    "GunSlingher", "Arcidemone", "Big Game Hunter"
]})

frasi_set.update({
    "Primo alla torre": "Il primo colpo decide chi comanda: apri lo scontro con una botta doppia e i cloni imparano subito a non stare sulla tua strada.",
    "Pazzo temporale": "Snap. Il caso smette di essere caso e per un attimo il tempo decide di ripetersi esattamente come vuoi tu.",
    "Evocatore del vero potere": "Ogni attacco merita un canto. Quasi sempre resta solo una canzone, ma ogni tanto risponde qualcosa di decisamente troppo potente.",
    "GunSlingher": "Prima si spara, poi eventualmente si fanno le presentazioni: una raffica apre lo scontro prima che qualcuno possa reagire.",
    "Arcidemone": "La cura degli altri è un insulto personale: ogni volta che il nemico recupera vita, la tua rabbia diventa potenza.",
    "Big Game Hunter": "Prima di cacciare una bestia bisogna muoversi come lei: all'inizio dello scontro ne copi immediatamente l'agilità.",
})
'''
    p.write_text(text, encoding="utf-8")

# bilanciamento.py
p = Path("bilanciamento.py")
text = p.read_text(encoding="utf-8")
if MARKER not in text:
    text += r'''

# --- QUARTA ONDATA SET: SEI SET ---
PROC_CLASSI.update({
    "Primo alla torre": {
        "combattimento": {"primo_colpo": {"moltiplicatore_danno": 2}},
        "assalto": {"clone": {"atk_mul": 4}},
    },
    "Pazzo temporale": {
        "combattimento": {"seed": {"proc": 90, "seed": "Anello perfezionista"}},
        "assalto": {"seed": {"proc": 90, "seed": "Anello perfezionista"}},
    },
    "Evocatore del vero potere": {
        "combattimento": {"canto": {"proc": 1, "anello": "Anello superfortissimo ma proprio rotto sgravatissimo"}},
    },
    "GunSlingher": {
        "combattimento": {"raffica": {"colpi_min": 1, "colpi_max": 6, "danno_per_colpo": 20}},
        "assalto": {"raffica_clone": {"colpi_min": 1, "colpi_max": 6, "danno_per_colpo": 60}},
    },
    "Arcidemone": {
        "combattimento": {"cura_nemica": {"atk": 4000}},
    },
    "Big Game Hunter": {
        "combattimento": {"copia_agilita": {"attivo": True}},
    },
})
'''
    p.write_text(text, encoding="utf-8")

# frasi_set.py
p = Path("frasi_set.py")
text = p.read_text(encoding="utf-8")
if MARKER not in text:
    text += r'''

# --- QUARTA ONDATA SET: SEI SET ---
FRASI_SET_TECNICHE.update({
    "Primo alla torre": "COMBATTIMENTO (vale anche in dungeon e boss): il primo colpo che va a segno infligge il danno totale ×{combattimento.primo_colpo.moltiplicatore_danno}. ASSALTO — HARD COUNTER del Clone: se lo bersagli, ATK ×{assalto.clone.atk_mul}.",
    "Pazzo temporale": "COMBATTIMENTO (vale anche in dungeon e boss): a inizio scontro compare Snap! e hai il {combattimento.seed.proc:pct} di fissare il seed a {combattimento.seed.seed} per tutta la sequenza casuale dello scontro. ASSALTO: stessa logica con il {assalto.seed.proc:pct}.",
    "Evocatore del vero potere": "COMBATTIMENTO (vale anche in dungeon e boss): prima di ogni tuo attacco compare un canto; hai il {combattimento.canto.proc:pct} di sostituire il tuo anello per il resto dello scontro con {combattimento.canto.anello}.",
    "GunSlingher": "COMBATTIMENTO (vale anche in dungeon e boss): a inizio scontro spari da {combattimento.raffica.colpi_min} a {combattimento.raffica.colpi_max} colpi prima della normale azione, ciascuno da {combattimento.raffica.danno_per_colpo} danni. ASSALTO: se esiste un Clone gli spari da {assalto.raffica_clone.colpi_min} a {assalto.raffica_clone.colpi_max} colpi da {assalto.raffica_clone.danno_per_colpo} danni prima che reagisca.",
    "Arcidemone": "COMBATTIMENTO (vale anche in dungeon e boss): quando l'avversario recupera HP durante un turno, guadagni {combattimento.cura_nemica.atk:signed} ATK per il resto dello scontro.",
    "Big Game Hunter": "COMBATTIMENTO (vale anche in dungeon e boss): all'inizio dello scontro imposti la tua AGI uguale all'AGI corrente dell'avversario.",
})
'''
    p.write_text(text, encoding="utf-8")

# nft.py
p = Path("nft.py")
text = p.read_text(encoding="utf-8")
if MARKER not in text:
    text += r'''

# --- QUARTA ONDATA SET: SEI SET ---
_turno_quarta_ondata_base = turno
_assedio_quarta_ondata_base = assedio


def _inizializza_pazzo_temporale_quarta(proprietario, avversario):
    if proprietario.get("set") != "Pazzo temporale" or proprietario.get("_pazzo_temporale_init"):
        return ""
    proprietario["_pazzo_temporale_init"] = True
    testo = "**Snap!**\n"
    if proc_ok(random.random(), "Pazzo temporale", "combattimento", "seed"):
        seed = proc_val("Pazzo temporale", "combattimento", "seed", "seed")
        stato = random.Random(seed).getstate()
        proprietario["_pazzo_temporale_seed_attivo"] = True
        avversario["_pazzo_temporale_seed_attivo"] = True
        proprietario["_pazzo_temporale_rng_state"] = stato
        avversario["_pazzo_temporale_rng_state"] = stato
        testo += "⏳ Il tempo si spezza: il destino dello scontro è stato fissato!\n"
    return testo


def _inizializza_big_game_hunter_quarta(proprietario, agilita_avversario):
    if proprietario.get("set") != "Big Game Hunter" or proprietario.get("_big_game_hunter_init"):
        return ""
    proprietario["_big_game_hunter_init"] = True
    proprietario["agi"] = agilita_avversario
    return f"🏹 {proprietario['Nome']} studia la preda e ne copia l'agilità: {agilita_avversario} AGI!\n"


def _inizializza_gunslingher_quarta(proprietario, avversario):
    if proprietario.get("set") != "GunSlingher" or proprietario.get("_gunslingher_init"):
        return ""
    proprietario["_gunslingher_init"] = True
    cfg = proc_cfg("GunSlingher", "combattimento", "raffica")
    colpi = random.randint(cfg["colpi_min"], cfg["colpi_max"])
    danno = colpi * cfg["danno_per_colpo"]
    avversario["hp"] -= danno
    proprietario["fatto"] = proprietario.get("fatto", 0) + danno
    return f"🔫 {proprietario['Nome']} apre lo scontro con {colpi} colpi: {danno} danni prima di reagire!\n"


def _canto_vero_potere_quarta(proprietario):
    if proprietario.get("set") != "Evocatore del vero potere":
        return ""
    testo = "🎶 Il canto del vero potere risuona prima dell'attacco...\n"
    if proc_ok(random.random(), "Evocatore del vero potere", "combattimento", "canto"):
        anello = proc_val("Evocatore del vero potere", "combattimento", "canto", "anello")
        proprietario["anello"] = anello
        testo += f"💍 QUALCOSA HA RISPOSTO AL CANTO: {anello}!\n"
    return testo


def turno(main, oppo, cond=None):
    prefisso = _inizializza_pazzo_temporale_quarta(main, oppo)
    prefisso += _inizializza_pazzo_temporale_quarta(oppo, main)

    stato_seed = main.get("_pazzo_temporale_rng_state") or oppo.get("_pazzo_temporale_rng_state")
    stato_globale = None
    if stato_seed is not None:
        stato_globale = random.getstate()
        random.setstate(stato_seed)

    try:
        agi_main_iniziale = main.get("agi", 0)
        agi_oppo_iniziale = oppo.get("agi", 0)
        prefisso += _inizializza_big_game_hunter_quarta(main, agi_oppo_iniziale)
        prefisso += _inizializza_big_game_hunter_quarta(oppo, agi_main_iniziale)
        prefisso += _inizializza_gunslingher_quarta(main, oppo)
        prefisso += _inizializza_gunslingher_quarta(oppo, main)

        if is_dead(main) or is_dead(oppo):
            return prefisso

        prefisso += _canto_vero_potere_quarta(main)

        hp_main_prima = main.get("hp", 0)
        hp_oppo_prima = oppo.get("hp", 0)
        scudo_oppo_prima = oppo.get("Scudo") if "Scudo" in oppo else None

        testo = _turno_quarta_ondata_base(main, oppo, cond)
        danno_base = _danno_su_bersaglio_terza(hp_oppo_prima, scudo_oppo_prima, oppo)

        if main.get("set") == "Primo alla torre" and not main.get("_primo_alla_torre_usato") and danno_base > 0:
            mol = proc_val("Primo alla torre", "combattimento", "primo_colpo", "moltiplicatore_danno")
            extra_pct = (mol - 1) * 100
            testo += _aggiungi_extra_terza(main, oppo, danno_base, extra_pct, "🗼 Il primo colpo domina la torre:")
            main["_primo_alla_torre_usato"] = True

        hp_main_dopo = main.get("hp", 0)
        hp_oppo_dopo = oppo.get("hp", 0)
        bonus_atk = proc_val("Arcidemone", "combattimento", "cura_nemica", "atk")
        if main.get("set") == "Arcidemone" and hp_oppo_dopo > hp_oppo_prima:
            main["atk"] += bonus_atk
            testo += f"😈 La cura del nemico alimenta l'Arcidemone: +{bonus_atk} ATK!\n"
        if oppo.get("set") == "Arcidemone" and hp_main_dopo > hp_main_prima:
            oppo["atk"] += bonus_atk
            testo += f"😈 La cura di {main['Nome']} alimenta {oppo['Nome']}: +{bonus_atk} ATK!\n"

        return prefisso + testo
    finally:
        if stato_globale is not None:
            nuovo_stato = random.getstate()
            main["_pazzo_temporale_rng_state"] = nuovo_stato
            oppo["_pazzo_temporale_rng_state"] = nuovo_stato
            random.setstate(stato_globale)


def assedio(playerg, player, nemico, target, team, order, clan, meteo=None, setting=dict()):
    prefisso = ""
    stato_globale = None
    nome_set = player.get("set")

    if nome_set == "Pazzo temporale":
        prefisso += "**Snap!**\n"
        if proc_ok(random.random(), nome_set, "assalto", "seed"):
            stato_globale = random.getstate()
            random.seed(proc_val(nome_set, "assalto", "seed", "seed"))
            prefisso += "⏳ Il seed dell'assalto è stato fissato!\n"

    try:
        if nome_set == "Primo alla torre" and target == "Clone":
            mol = proc_val(nome_set, "assalto", "clone", "atk_mul")
            player["atk"] *= mol
            prefisso += f"🗼 Il Clone è il bersaglio perfetto: ATK ×{mol}!\n"

        if nome_set == "GunSlingher" and "Clone" in nemico and isinstance(nemico.get("Clone"), dict):
            cfg = proc_cfg(nome_set, "assalto", "raffica_clone")
            colpi = random.randint(cfg["colpi_min"], cfg["colpi_max"])
            danno = colpi * cfg["danno_per_colpo"]
            nemico["Clone"]["hp"] -= danno
            player["fatto"] = player.get("fatto", 0) + danno
            prefisso += f"🔫 Raffica preventiva sul Clone: {colpi} colpi, {danno} danni!\n"

        return prefisso + _assedio_quarta_ondata_base(playerg, player, nemico, target, team, order, clan, meteo, setting)
    finally:
        if stato_globale is not None:
            random.setstate(stato_globale)
'''
    p.write_text(text, encoding="utf-8")

# -*- coding: utf-8 -*-
from pathlib import Path
import string


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{label}: atteso 1, trovato {n}")
    return text.replace(old, new, 1)


# -----------------------------------------------------------------------------
# bilanciamento.py
# -----------------------------------------------------------------------------
bil_path = Path("bilanciamento.py")
bil = bil_path.read_text(encoding="utf-8")
if '"Cangiante": {' in bil:
    raise SystemExit("Nuovi incantesimi già presenti in bilanciamento.py")

start = bil.index("INCANTESIMI_CONFIG = {")
end = bil.index("\n}\n\n\n# Effetti temporanei non legati agli incantesimi.", start)
nuovi_config = r'''
    "Cangiante": {
        "turno": {
            "attacco": {"proc": 99},
            "difesa": {"proc": 99},
        },
    },
    "Inevitabile": {
        "turno": {"difesa": {"proc": 100, "danno_attaccante": 5, "danno_difensore": 5}},
    },
    "Spumeggiante": {
        "turno": {
            "attacco": {"proc": 8},
            "difesa": {"proc": 8},
        },
    },
    "Onde dell'abisso": {
        "assalto": {"onda": {"proc": 100, "atk_pct_min": 30, "atk_pct_max": 70}},
    },
    "Armadillibilità": {
        "assalto": {"morte": {"proc": 100, "def_pct": 100}},
    },
    "Giallo": {
        "assalto": {"aiutanti": {"proc": 50, "aiutanti_extra": 10}},
    },
    "Dominio semplice": {
        "turno": {
            "attacco": {"proc": 50, "costo_hp": 3},
            "difesa": {"proc": 50, "costo_hp": 3},
        },
    },
    "Caricato": {
        "turno": {
            "attacco": {
                "proc": 10,
                "cariche_per_proc": 1,
                "hp_sotto": 100,
                "danno_per_carica": 5,
                "reset_cariche": 0,
            }
        },
    },
'''
bil = bil[:end] + nuovi_config + bil[end:]
bil_path.write_text(bil, encoding="utf-8")


# -----------------------------------------------------------------------------
# frasi_incantesimi.py
# -----------------------------------------------------------------------------
fr_path = Path("frasi_incantesimi.py")
fr = fr_path.read_text(encoding="utf-8")
if '"Cangiante":' in fr:
    raise SystemExit("Nuove frasi già presenti")
idx = fr.rfind("\n}")
if idx < 0:
    raise SystemExit("Chiusura FRASI_INCANTESIMI_TECNICHE non trovata")
nuove_frasi = r'''
    "Cangiante": "Quando attacchi hai il {turno.attacco.proc:pct} di assumere un set casuale e quando difendi hai il {turno.difesa.proc:pct}. Il nuovo set sostituisce quello usato nella copia dello scontro fino alla successiva attivazione di Cangiante.",
    "Inevitabile": "Ogni volta che difendi si attiva al {turno.difesa.proc:pct}: prima del resto del turno infligge {turno.difesa.danno_attaccante} danni all'attaccante e {turno.difesa.danno_difensore} danni a te.",
    "Spumeggiante": "A ogni turno hai il {turno.attacco.proc:pct} quando attacchi e il {turno.difesa.proc:pct} quando difendi di scambiare l'ATK dei due combattenti prima di calcolare il colpo. Se entrambi lo possiedono e almeno uno dei due proc riesce, lo scambio avviene una sola volta.",
    "Onde dell'abisso": "In assalto si attiva al {assalto.onda.proc:pct}: se resta almeno una struttura, un'onda colpisce una struttura casuale infliggendo direttamente tra il {assalto.onda.atk_pct_min:pct} e il {assalto.onda.atk_pct_max:pct} del tuo ATK attuale.",
    "Armadillibilità": "Quando muori in assalto si attiva al {assalto.morte.proc:pct}, prima delle eventuali resurrezioni: una struttura casuale subisce un danno diretto pari al {assalto.morte.def_pct:pct} della tua DEF attuale.",
    "Giallo": "All'inizio dell'assalto, prima di tutti i bonus che dipendono dal numero di compagni, hai il {assalto.aiutanti.proc:pct} di aggiungere {assalto.aiutanti.aiutanti_extra} aiutanti virtuali al conteggio. Non sono giocatori reali: valgono solo per quei calcoli.",
    "Dominio semplice": "A ogni turno hai il {turno.attacco.proc:pct} quando attacchi e il {turno.difesa.proc:pct} quando difendi di spendere {turno.attacco.costo_hp} HP e rendere vuoto il set avversario per quel turno. Se entrambi lo attivano, entrambi pagano il costo e vengono bloccati entrambi i set.",
    "Caricato": "A ogni attacco hai il {turno.attacco.proc:pct} di ottenere {turno.attacco.cariche_per_proc} carica. Se dopo il controllo hai meno di {turno.attacco.hp_sotto} HP e almeno una carica, le scarichi tutte infliggendo {turno.attacco.danno_per_carica} danni diretti per carica, poi il contatore torna a {turno.attacco.reset_cariche}.",
'''
fr = fr[:idx] + nuove_frasi + fr[idx:]
fr_path.write_text(fr, encoding="utf-8")


# -----------------------------------------------------------------------------
# liste.py - libri e descrizioni dell'autore
# -----------------------------------------------------------------------------
liste_path = Path("liste.py")
liste = liste_path.read_text(encoding="utf-8")
if '"101 pattern sociali"' in liste:
    raise SystemExit("Nuovi libri già presenti")
lib_start = liste.index("libri = {")
lib_end_marker = "\n\n\nMetei ="
lib_end = liste.index(lib_end_marker, lib_start)
outer_close = liste.rfind("}", lib_start, lib_end)
if outer_close < 0:
    raise SystemExit("Chiusura dizionario libri non trovata")
nuovi_libri = r''',
           "101 pattern sociali": {"ef": "Cangiante", "descrizione": "Impara a mimetizzarti tra le persone e le giungle ti lasceranno in pace."},
           "Misture storiche e dove trovarle": {"ef": "Inevitabile", "descrizione": "Le tue armi sono velenose, forse fin troppo."},
           "The mask: Il libro": {"ef": "Spumeggiante", "descrizione": "Proprio come nel film!"},
           "Le migliori location per il surf": {"ef": "Onde dell'abisso", "descrizione": "Impara a mimetizzarti tra le persone e le giungle ti lasceranno in pace."},
           "Yoga estremo per persone comuni ma non troppo": {"ef": "Armadillibilità", "descrizione": "Combattere è un arte tanto quanto morire con stile."},
           "Il re in giallo": {"ef": "Giallo", "descrizione": "Essere gialli è un arte, tanto quanto avere altri 9 amici gialli."},
           "Cerficato della nuova ombra": {"ef": "Dominio semplice", "descrizione": "Nuova ombra acquisita, per poca forza vitale blocca tecniche strane nemiche"},
           "Manuale di meccanica pt 3": {"ef": "Caricato", "descrizione": "Prepara il colpo e assicurati di finire il lavoro"}
'''
liste = liste[:outer_close] + nuovi_libri + liste[outer_close:]

# Rende i nuovi libri disponibili negli stessi pool arena che già distribuiscono
# i libri storici, senza alterare le modalità che non hanno libri.
availability = r'''

# Mantiene automaticamente completi i pool arena che già distribuiscono libri.
for _arena_pool in arenamod.values():
    if "Libro del bene e del male" in _arena_pool:
        for _libro in libri:
            if _libro not in _arena_pool:
                _arena_pool.append(_libro)
'''
liste = liste[:lib_end + len(nuovi_libri)] if False else liste
# Inserimento subito dopo il dizionario libri e prima di Metei.
lib_end = liste.index(lib_end_marker, lib_start)
liste = liste[:lib_end] + availability + liste[lib_end:]
liste_path.write_text(liste, encoding="utf-8")


# -----------------------------------------------------------------------------
# nft.py - combattimento e assalto
# -----------------------------------------------------------------------------
nft_path = Path("nft.py")
nft = nft_path.read_text(encoding="utf-8")
if "Cangiante assegna" in nft:
    raise SystemExit("Logica nuovi incantesimi già presente")

# 1) Incantesimi di turno che devono risolversi prima dei set.
old = '''    set = main.get("set",None)\n    setN = oppo.get("set",None)\n\n    # I set con blocco_set disattivano le abilità di entrambi prima di qualsiasi proc.\n'''
new = r'''    set = main.get("set",None)
    setN = oppo.get("set",None)

    # Incantesimi che devono risolversi prima di qualsiasi abilità di set.
    # Cangiante assegna il set alla sola copia di combattimento.
    if "Cangiante" in main.get("incantamenti", []) and incantesimo_ok(random.random(), "Cangiante", "turno", "attacco"):
        set = random.choice(list(classi))
        main["set"] = set
        if set == "Paladino":
            main.setdefault("Scudo", 0)
        text += f"Per {nome1} è ora di comportarsi come {set}!\n"

    if "Cangiante" in oppo.get("incantamenti", []) and incantesimo_ok(random.random(), "Cangiante", "turno", "difesa"):
        setN = random.choice(list(classi))
        oppo["set"] = setN
        if setN == "Paladino":
            oppo.setdefault("Scudo", 0)
        text += f"Per {nome2} è ora di comportarsi come {setN}!\n"

    # Inevitabile è un effetto difensivo certo: il difensore avvelena entrambi.
    if "Inevitabile" in oppo.get("incantamenti", []) and incantesimo_ok(random.random(), "Inevitabile", "turno", "difesa"):
        main["hp"] -= incantesimo_val("Inevitabile", "turno", "difesa", "danno_attaccante")
        oppo["hp"] -= incantesimo_val("Inevitabile", "turno", "difesa", "danno_difensore")
        text += "**5 danni vengono fatti ad entrambi!**\n"

    # Dominio semplice paga vita del possessore e neutralizza solo il set nemico
    # nel turno corrente, senza cancellarlo dalla scheda.
    if "Dominio semplice" in main.get("incantamenti", []) and incantesimo_ok(random.random(), "Dominio semplice", "turno", "attacco"):
        main["hp"] -= incantesimo_val("Dominio semplice", "turno", "attacco", "costo_hp")
        setN = None
        text += "**Arte della nuova ombra, Dominio semplice!**\n"

    if "Dominio semplice" in oppo.get("incantamenti", []) and incantesimo_ok(random.random(), "Dominio semplice", "turno", "difesa"):
        oppo["hp"] -= incantesimo_val("Dominio semplice", "turno", "difesa", "costo_hp")
        set = None
        text += "**Arte della nuova ombra, Dominio semplice!**\n"

    # Spumeggiante: un proc di uno dei due è sufficiente; lo swap avviene una volta.
    spumeggiante_attivo = False
    if "Spumeggiante" in main.get("incantamenti", []):
        spumeggiante_attivo = incantesimo_ok(random.random(), "Spumeggiante", "turno", "attacco")
    if "Spumeggiante" in oppo.get("incantamenti", []):
        spumeggiante_attivo = spumeggiante_attivo or incantesimo_ok(random.random(), "Spumeggiante", "turno", "difesa")
    if spumeggiante_attivo:
        main["atk"], oppo["atk"] = oppo["atk"], main["atk"]
        dps = main["atk"]
        text += "**Spumeggiante!**\n"

    # Caricato accumula sul combattente e scarica automaticamente sotto soglia.
    if "Caricato" in main.get("incantamenti", []):
        cfg_caricato = incantesimo_cfg("Caricato", "turno", "attacco")
        stato_incantesimi = main.setdefault("_stato_incantesimi", {})
        cariche = stato_incantesimi.get("Caricato", 0)
        if incantesimo_ok(random.random(), "Caricato", "turno", "attacco"):
            cariche += cfg_caricato["cariche_per_proc"]
            stato_incantesimi["Caricato"] = cariche
            text += f"**{nome1} carica il colpo finale! ({cariche} cariche)**\n"
        if main["hp"] < cfg_caricato["hp_sotto"] and cariche > 0:
            danni_caricati = cariche * cfg_caricato["danno_per_carica"]
            oppo["hp"] -= danni_caricati
            stato_incantesimi["Caricato"] = cfg_caricato["reset_cariche"]
            text += f"**{nome1} rilascia il colpo caricato e infligge {danni_caricati} danni a {nome2} ({oppo['hp']} HP)! ({cariche} cariche)**\n"

    # I set con blocco_set disattivano le abilità di entrambi prima di qualsiasi proc.
'''
nft = replace_once(nft, old, new, "blocco pre-set turno")

# Dominio deve valere anche nei pochi punti che leggevano direttamente main["set"].
nft = replace_once(
    nft,
    '''    elif main["set"] == 'Avventuriero delle praterie' and proc_ok(1 - num, main["set"], "turno", "respira"):\n''',
    '''    elif set == 'Avventuriero delle praterie' and proc_ok(1 - num, set, "turno", "respira"):\n''',
    "Avventuriero usa set locale",
)

# 2) Rende disponibili gli incantesimi al flusso di assalto e applica Giallo
# prima di qualsiasi calcolo basato sugli aiutanti.
old = '''                                    giocatore = copy.deepcopy(player[username]["scheda"])\n                                    if "pet" in player[username]:\n'''
new = '''                                    giocatore = copy.deepcopy(player[username]["scheda"])\n                                    giocatore["incantamenti"] = get_ench(player[username])\n                                    if "pet" in player[username]:\n'''
nft = replace_once(nft, old, new, "incantamenti in assalto")

old = '''                                    serv = matx\n                                    if matx < proc_val("Eroe caduto", "assalto", "supporto_clan", "compagni_soglia") and giocatore["set"] == 'Eroe caduto':\n                                        serv += proc_val("Eroe caduto", "assalto", "supporto_clan", "serv_bonus_nft")\n                                        \n                                    if giocatore["set"] == 'Eroe della rivolta':\n                                        serv = serv * proc_val("Eroe della rivolta", "assalto", "supporto_clan", "serv_mul")\n                                    if player[username]["setta"]["benedizione"] == 'Orso polare' and  matx > 2:\n'''
new = r'''                                    matx_effettivo = matx
                                    messaggio_giallo = ""
                                    if "Giallo" in giocatore.get("incantamenti", []) and incantesimo_ok(random.random(), "Giallo", "assalto", "aiutanti"):
                                        matx_effettivo += incantesimo_val("Giallo", "assalto", "aiutanti", "aiutanti_extra")
                                        messaggio_giallo = "Venite a me ~~Minions~~ giallini, è ora di distruggere questo posto!\n"

                                    serv = matx_effettivo
                                    if matx_effettivo < proc_val("Eroe caduto", "assalto", "supporto_clan", "compagni_soglia") and giocatore["set"] == 'Eroe caduto':
                                        serv += proc_val("Eroe caduto", "assalto", "supporto_clan", "serv_bonus_nft")
                                        
                                    if giocatore["set"] == 'Eroe della rivolta':
                                        serv = serv * proc_val("Eroe della rivolta", "assalto", "supporto_clan", "serv_mul")
                                    if player[username]["setta"]["benedizione"] == 'Orso polare' and matx_effettivo > 2:
'''
nft = replace_once(nft, old, new, "Giallo e conteggio aiutanti")

nft = replace_once(
    nft,
    '''                                    if player[username]["setta"]["benedizione"] == 'Kaimano' and  matx <= 2:\n''',
    '''                                    if player[username]["setta"]["benedizione"] == 'Kaimano' and matx_effettivo <= 2:\n''',
    "Kaimano usa conteggio effettivo",
)

nft = replace_once(
    nft,
    '''                                    output = assedio(player,\n''',
    '''                                    output = messaggio_giallo + assedio(player,\n''',
    "messaggio Giallo prima assedio",
)

nft = replace_once(
    nft,
    '''                                    output += f"\\n{matx} persone assaltano con te!"\n''',
    '''                                    output += f"\\n{matx} persone assaltano con te!"\n                                    if matx_effettivo != matx:\n                                        output += f" ({matx_effettivo} considerate nei calcoli grazie a Giallo)"\n''',
    "recap aiutanti Giallo",
)

# 3) Onde dell'abisso: una volta per assalto, dopo i bonus iniziali del set e
# prima di iniziare a percorrere le strutture.
marker = '''    num = random.random()    \n    \n    if "Bersaglio enorme" in list(nemico) and 0.2 > num:\n'''
insert = r'''    # Incantesimi offensivi d'assalto.
    if "Onde dell'abisso" in player.get("incantamenti", []) and incantesimo_ok(random.random(), "Onde dell'abisso", "assalto", "onda"):
        strutture_valide = [
            nome_struttura for nome_struttura, dati_struttura in nemico.items()
            if nome_struttura != "inguerra" and isinstance(dati_struttura, dict) and dati_struttura.get("hp", 0) > 0
        ]
        if strutture_valide:
            struttura_onda = random.choice(strutture_valide)
            cfg_onda = incantesimo_cfg("Onde dell'abisso", "assalto", "onda")
            danno_onda = round(player["atk"] * random.uniform(cfg_onda["atk_pct_min"], cfg_onda["atk_pct_max"]) / 100)
            nemico[struttura_onda]["hp"] -= danno_onda
            player["fatto"] += danno_onda
            text += f"🌊 Un'onda si alza e si schianta contro {struttura_onda} per ben {danno_onda} danni!\n"
            if nemico[struttura_onda]["hp"] <= 0:
                nemico.pop(struttura_onda)
                text += "**E' andata!!**\n"

    num = random.random()    
    
    if "Bersaglio enorme" in list(nemico) and 0.2 > num:
'''
nft = replace_once(nft, marker, insert, "Onde dell'abisso")

# 4) Armadillibilità: trigger di morte prima della catena di resurrezione.
marker = '''    num = random.random()\n    if set == "Mariachi" and player["hp"] <= 0 and proc_ok(num, set, "assalto", "resurrezione"):\n'''
insert = r'''    # Armadillibilità è un trigger di morte e si risolve prima delle resurrezioni.
    if player["hp"] <= 0 and "Armadillibilità" in player.get("incantamenti", []) and incantesimo_ok(random.random(), "Armadillibilità", "assalto", "morte"):
        strutture_valide = [
            nome_struttura for nome_struttura, dati_struttura in nemico.items()
            if nome_struttura != "inguerra" and isinstance(dati_struttura, dict) and dati_struttura.get("hp", 0) > 0
        ]
        if strutture_valide:
            struttura_armadillo = random.choice(strutture_valide)
            danno_armadillo = round(player["def"] * incantesimo_val("Armadillibilità", "assalto", "morte", "def_pct") / 100)
            nemico[struttura_armadillo]["hp"] -= danno_armadillo
            player["fatto"] += danno_armadillo
            text += f"🦔 Ora del rotolamento contro {struttura_armadillo} per piantargli {danno_armadillo} danni!\n"
            if nemico[struttura_armadillo]["hp"] <= 0:
                nemico.pop(struttura_armadillo)
                text += "**E' andata!!**\n"

    num = random.random()
    if set == "Mariachi" and player["hp"] <= 0 and proc_ok(num, set, "assalto", "resurrezione"):
'''
nft = replace_once(nft, marker, insert, "Armadillibilità")

nft_path.write_text(nft, encoding="utf-8")

print("Trasformazione nuovi incantesimi completata")

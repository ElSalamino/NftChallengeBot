from pathlib import Path

MARKER = "# --- QUINTA ONDATA SET: TREDICI SET ---"

# -----------------------------------------------------------------------------
# liste.py
# -----------------------------------------------------------------------------
p = Path("liste.py")
text = p.read_text(encoding="utf-8")
if MARKER not in text:
    text += r'''

# --- QUINTA ONDATA SET: TREDICI SET ---
classi.update({
    "Nucleo dell'uragano": ["Uncino rituale", "Origine della tempesta"],
    "Tormento di fuoco": ["Spada del dio della fucina", "Origine della tempesta"],
    "Girarrosto": ["Frusta di salsiccia", "Bastone sferico"],
    "Venere di ferro": ["Spina insanguinata", "Scaglioni pesanti"],
    "Rosso D'ossidina": ["Canna rossa", "Scudo d'ossidiana"],
    "Oltraggioso": ["Blasfemia", "Armatura pesantissima"],
    "Festante oscuro": ["Palla Ombra", "Corona del rave"],
    "Legionaro di Evelin": ["Corvo amichevole", "Scudo del comandante"],
    "Neo Genesi": ["Spada a protoni", "Piuma celeste"],
    "Intermezzo": ["Lancia celeste", "Palla chiodata"],
    "Obscurio": ["Palla Ombra", "Velo di catena"],
    "Primo al comando": ["Martello del folle", "Scudo del comandante"],
    "Luce persa": ["Spada del crociato", "Anima dispersa"],
})

Approccini.update({
    "Nucleo dell'uragano": ["Agile", "Spinto", "Impavido"],
    "Tormento di fuoco": ["Aggressivo", "Malevolo", "Spinto"],
    "Girarrosto": ["Conservativo", "Impavido", "Spavaldo"],
    "Venere di ferro": ["Difensivo", "Conservativo", "Impavido"],
    "Rosso D'ossidina": ["Aggressivo", "Spavaldo", "Agile"],
    "Oltraggioso": ["Malevolo", "Spavaldo", "Impavido"],
    "Festante oscuro": ["Conservativo", "Ingannevole", "Agile"],
    "Legionaro di Evelin": ["Autorevole", "Aggressivo", "Spinto"],
    "Neo Genesi": ["Agile", "Spinto", "Autorevole"],
    "Intermezzo": ["Agile", "Conservativo", "Difensivo"],
    "Obscurio": ["Ingannevole", "Malevolo", "Conservativo"],
    "Primo al comando": ["Autorevole", "Spinto", "Impavido"],
    "Luce persa": ["Aggressivo", "Impavido", "Spinto"],
})

bonus.update({nome: {"hp": 0, "def": 0, "atk": 0, "agi": 0} for nome in [
    "Nucleo dell'uragano", "Tormento di fuoco", "Girarrosto", "Venere di ferro",
    "Rosso D'ossidina", "Oltraggioso", "Festante oscuro", "Legionaro di Evelin",
    "Neo Genesi", "Intermezzo", "Obscurio", "Primo al comando", "Luce persa"
]})

frasi_set.update({
    "Nucleo dell'uragano": "Il vento aspetta che il nemico si affidi al proprio anello: appena il potere si manifesta, l'uragano gli si rivolta contro.",
    "Tormento di fuoco": "Ogni scintilla di potere avversaria alimenta un tormento che brucia usando la forza stessa di chi lo ha evocato.",
    "Girarrosto": "Puoi cuocere lentamente quanto vuoi: la prima volta che sembri davvero cotto, torni improvvisamente in perfetta forma.",
    "Venere di ferro": "Ogni colpo affonda meno del previsto: spine e ferro assorbono una parte costante della violenza in arrivo.",
    "Rosso D'ossidina": "Ogni colpo riuscito ti convince ancora di più della tua strategia: diventi sempre più simile al tuo stesso approccio.",
    "Oltraggioso": "Oltraggi perfino il concetto di danno: nessun singolo colpo riesce a superare il limite che imponi allo scontro.",
    "Festante oscuro": "Dentro di te festeggiano ombre senza fine: prendono i colpi al tuo posto, ma a ogni turno una parte del loro dolore torna a reclamarti.",
    "Legionaro di Evelin": "Evelin detta il ritmo: nei turni dispari il colpo trova sempre un rinforzo, mentre gli accampamenti preferiscono non discutere.",
    "Neo Genesi": "La nuova genesi procede a impulsi regolari: nei turni pari libera una scarica pulita che accompagna il colpo.",
    "Intermezzo": "Ogni schivata è una nota accumulata. A tre, cinque e otto cariche il crescendo diventa sempre più difficile da fermare.",
    "Obscurio": "La luce della guarigione non trova strada nell'oscurità: davanti a te recuperare vita diventa semplicemente impossibile.",
    "Primo al comando": "Ogni anello che osa attivarsi diventa un segnale per il comandante: il caos degli altri si trasforma immediatamente in nuova vita.",
    "Luce persa": "Abbandoni ogni agilità e la trasformi in potere puro: niente più evasione, soltanto attacco e difesa alimentati dalla luce perduta.",
})
'''
    p.write_text(text, encoding="utf-8")

# -----------------------------------------------------------------------------
# bilanciamento.py
# -----------------------------------------------------------------------------
p = Path("bilanciamento.py")
text = p.read_text(encoding="utf-8")
if MARKER not in text:
    text += r'''

# --- QUINTA ONDATA SET: TREDICI SET ---
PROC_CLASSI.update({
    "Nucleo dell'uragano": {
        "combattimento": {"proc_anello_avversario": {"percento_atk_proprio": 10}},
        "assalto": {"immunita": {"struttura": "Spuntone malefico", "messaggio": "🌪 Il vento spazza via la trappola dello Spuntone malefico!"}},
    },
    "Tormento di fuoco": {
        "combattimento": {"proc_anello_avversario": {"percento_atk_avversario": 10}},
        "assalto": {"immunita": {"struttura": "Fabbro incantaspade", "messaggio": "🔥 Il Fabbro incantaspade non riesce a scalfirti: il tormento di fuoco lo sovrasta!"}},
    },
    "Girarrosto": {
        "combattimento": {"salvezza": {"hp_soglia_percento": 50, "hp_ripristino_percento": 100, "usi": 1}},
        "assalto": {"salvezza": {"hp_soglia_percento": 50, "hp_ripristino_percento": 100, "usi": 1}},
    },
    "Venere di ferro": {
        "combattimento": {"riduzione_danno": {"percento": 20}},
        "assalto": {"riduzione_danno": {"percento": 30}},
    },
    "Rosso D'ossidina": {
        "combattimento": {"riuso_approccio": {"attivo": True}},
        "assalto": {"immunita": {"struttura": "Sedimento del cucciolo", "messaggio": "🔴 Il drago è troppo arrabbiato per riuscire a farti del male!"}},
    },
    "Oltraggioso": {
        "combattimento": {"cap_danno": {"massimo": 50}},
        "assalto": {"immunita": {"struttura": "Chiesa", "messaggio": "⛪ L'oltraggio è tale che perfino la Chiesa rinuncia a danneggiarti!"}},
    },
    "Festante oscuro": {
        "combattimento": {"fantasmi": {"percento_ritorno": 50}},
        "assalto": {"immunita": {"struttura": "Cane da guardia", "messaggio": "👻 Il Cane da guardia si perde tra le ombre e non riesce a colpirti!"}},
    },
    "Legionaro di Evelin": {
        "combattimento": {"danno_turno": {"parita": "dispari", "danno": 50}},
        "assalto": {"immunita": {"struttura": "Accampamento", "messaggio": "🦅 Nessuno nell'Accampamento vuole mettersi contro Evelin!"}},
    },
    "Neo Genesi": {
        "combattimento": {"danno_turno": {"parita": "pari", "danno": 50}},
        "assalto": {"immunita": {"struttura": "Spaventapasseri ornamentale", "messaggio": "✨ Lo Spaventapasseri ornamentale non osa muoversi davanti a cotanta potenza!"}},
    },
    "Intermezzo": {
        "combattimento": {"cariche_schivata": {"soglia_1": 3, "bonus_1": 5, "soglia_2": 5, "bonus_2": 15, "soglia_3": 8, "moltiplicatore": 2}},
        "assalto": {"immunita": {"struttura": "Muraglione extra", "messaggio": "🪽 Fluttui oltre il Muraglione extra in completa tranquillità!"}},
    },
    "Obscurio": {
        "combattimento": {"anti_cura": {"attivo": True}},
        "assalto": {"immunita": {"struttura": "Stazione laser di sicurezza", "messaggio": "🌑 La luce compressa della Stazione laser non riesce a illuminarti!"}},
    },
    "Primo al comando": {
        "combattimento": {"proc_anello": {"cura": 30}},
        "assalto": {"immunita": {"struttura": "Clone", "messaggio": "🫡 Il Clone riconosce il Primo al comando e non riesce a danneggiarlo!"}},
    },
    "Luce persa": {
        "combattimento": {"conversione": {"agi_mul": 4, "quota_atk": 0.5, "quota_def": 0.5}},
        "assalto": {"conversione": {"agi_mul": 4, "quota_atk": 0.5, "quota_def": 0.5}},
    },
})
'''
    p.write_text(text, encoding="utf-8")

# -----------------------------------------------------------------------------
# frasi_set.py
# -----------------------------------------------------------------------------
p = Path("frasi_set.py")
text = p.read_text(encoding="utf-8")
if MARKER not in text:
    text += r'''

# --- QUINTA ONDATA SET: TREDICI SET ---
FRASI_SET_TECNICHE.update({
    "Nucleo dell'uragano": "COMBATTIMENTO (anche dungeon/boss): ogni volta che un anello avversario procca, il vento infligge al proprietario dell'anello danni puliti pari al {combattimento.proc_anello_avversario.percento_atk_proprio:pct} del tuo ATK. ASSALTO: non subisci danni dallo {assalto.immunita.struttura}.",
    "Tormento di fuoco": "COMBATTIMENTO (anche dungeon/boss): ogni volta che un anello avversario procca, il proprietario dell'anello subisce danni puliti pari al {combattimento.proc_anello_avversario.percento_atk_avversario:pct} del proprio ATK. ASSALTO: non subisci danni dal {assalto.immunita.struttura}.",
    "Girarrosto": "COMBATTIMENTO (anche dungeon/boss): la prima volta che scendi sotto il {combattimento.salvezza.hp_soglia_percento:pct} degli HP iniziali torni al {combattimento.salvezza.hp_ripristino_percento:pct}. ASSALTO: stessa salvezza, una volta per assalto.",
    "Venere di ferro": "COMBATTIMENTO (anche dungeon/boss): ogni perdita di HP viene ridotta del {combattimento.riduzione_danno.percento:pct}. ASSALTO: la riduzione sale al {assalto.riduzione_danno.percento:pct}.",
    "Rosso D'ossidina": "COMBATTIMENTO (anche dungeon/boss): dopo ogni colpo riuscito riapplichi il tuo approccio e il log mostra in cosa stai diventando più estremo. ASSALTO: non subisci danni dal {assalto.immunita.struttura}.",
    "Oltraggioso": "COMBATTIMENTO (anche dungeon/boss): finché partecipi allo scontro, ogni singola perdita di HP o Scudo di entrambi i combattenti è limitata a un massimo di {combattimento.cap_danno.massimo} danni. ASSALTO: non subisci danni dalla {assalto.immunita.struttura}.",
    "Festante oscuro": "COMBATTIMENTO (anche dungeon/boss): i fantasmi assorbono al posto tuo ogni perdita di HP; all'inizio di ogni tuo turno subisci il {combattimento.fantasmi.percento_ritorno:pct} del danno ancora accumulato nei fantasmi e quel valore viene rimosso dal loro accumulo. ASSALTO: non subisci danni dal {assalto.immunita.struttura}.",
    "Legionaro di Evelin": "COMBATTIMENTO (anche dungeon/boss): nei tuoi turni {combattimento.danno_turno.parita}, se il colpo non viene schivato e va a segno, infliggi altri {combattimento.danno_turno.danno} danni puliti. ASSALTO: non subisci danni dall'{assalto.immunita.struttura}.",
    "Neo Genesi": "COMBATTIMENTO (anche dungeon/boss): nei tuoi turni {combattimento.danno_turno.parita}, se il colpo non viene schivato e va a segno, infliggi altri {combattimento.danno_turno.danno} danni puliti. ASSALTO: non subisci danni dallo {assalto.immunita.struttura}.",
    "Intermezzo": "COMBATTIMENTO (anche dungeon/boss): ogni schivata concede una carica. Da {combattimento.cariche_schivata.soglia_1} cariche aggiungi {combattimento.cariche_schivata.bonus_1} danni; da {combattimento.cariche_schivata.soglia_2} aggiungi anche altri {combattimento.cariche_schivata.bonus_2}; da {combattimento.cariche_schivata.soglia_3} il danno risultante viene inoltre moltiplicato ×{combattimento.cariche_schivata.moltiplicatore}. ASSALTO: non subisci danni dal {assalto.immunita.struttura}.",
    "Obscurio": "COMBATTIMENTO (anche dungeon/boss): l'avversario non può aumentare i propri HP tramite cure finché è vivo; le resurrezioni da 0 HP o meno restano possibili. ASSALTO: non subisci danni dalla {assalto.immunita.struttura}.",
    "Primo al comando": "COMBATTIMENTO (anche dungeon/boss): ogni proc di qualsiasi anello nello scontro ti cura di {combattimento.proc_anello.cura} HP. ASSALTO: non subisci danni dal {assalto.immunita.struttura}.",
    "Luce persa": "COMBATTIMENTO (anche dungeon/boss): a inizio scontro calcoli AGI ×{combattimento.conversione.agi_mul}; il {combattimento.conversione.quota_atk:pct_mul} va in ATK e il {combattimento.conversione.quota_def:pct_mul} in DEF, poi AGI diventa 0. ASSALTO: stessa conversione prima dell'assalto.",
})
'''
    p.write_text(text, encoding="utf-8")

# -----------------------------------------------------------------------------
# nft.py
# -----------------------------------------------------------------------------
p = Path("nft.py")
text = p.read_text(encoding="utf-8")
if MARKER not in text:
    text += r'''

# --- QUINTA ONDATA SET: TREDICI SET ---
# Questa ondata aggiunge due primitive riusabili:
# 1) tracciamento dei proc degli anelli tramite il punto centrale anello_ok();
# 2) un proxy di combattimento che intercetta le variazioni HP/Scudo senza
#    duplicare la gigantesca logica storica di turno()/assedio().
import contextvars as _contextvars_quinta
import inspect as _inspect_quinta
import math as _math_quinta

_turno_quinta_ondata_base = turno
_assedio_quinta_ondata_base = assedio
_anello_ok_quinta_ondata_base = anello_ok
_eventi_anello_quinta = _contextvars_quinta.ContextVar("eventi_anello_quinta", default=None)


def _trova_proprietario_anello_quinta(frame, nome_anello):
    """Best effort: individua quale copia di combattimento possiede l'anello che ha procato."""
    profondita = 0
    while frame is not None and profondita < 10:
        loc = frame.f_locals
        proprietario = loc.get("proprietario")
        if isinstance(proprietario, dict) and loc.get("ring") == nome_anello:
            return proprietario

        main = loc.get("main")
        oppo = loc.get("oppo")
        if isinstance(main, dict) and isinstance(oppo, dict):
            anello_main = loc.get("anello")
            anello_oppo = loc.get("anellon")
            if anello_main == nome_anello and anello_oppo != nome_anello:
                return main
            if anello_oppo == nome_anello and anello_main != nome_anello:
                return oppo
            if main.get("anello") == nome_anello and oppo.get("anello") != nome_anello:
                return main
            if oppo.get("anello") == nome_anello and main.get("anello") != nome_anello:
                return oppo
        frame = frame.f_back
        profondita += 1
    return None


def anello_ok(numero_casuale, anello, contesto, nome, default=0):
    """Versione tracciata: conserva la semantica storica e registra solo i proc riusciti."""
    esito = _anello_ok_quinta_ondata_base(numero_casuale, anello, contesto, nome, default)
    eventi = _eventi_anello_quinta.get()
    if esito and eventi is not None:
        frame = _inspect_quinta.currentframe()
        proprietario = _trova_proprietario_anello_quinta(frame.f_back if frame else None, anello)
        eventi.append({
            "owner_id": id(proprietario) if proprietario is not None else None,
            "anello": anello,
            "contesto": contesto,
            "effetto": nome,
        })
    return esito


def _struttura_corrente_quinta():
    """Legge la struttura che sta applicando il danno dall'assedio storico."""
    frame = _inspect_quinta.currentframe()
    frame = frame.f_back if frame else None
    profondita = 0
    while frame is not None and profondita < 12:
        difesa = frame.f_locals.get("difesa")
        if difesa in strutture:
            return difesa
        frame = frame.f_back
        profondita += 1
    return None


def _numero_quinta(valore):
    return isinstance(valore, (int, float)) and not isinstance(valore, bool)


def _cap_globale_quinta(a, b):
    valori = []
    for personaggio in (a, b):
        if personaggio.get("set") == "Oltraggioso":
            valore = proc_val("Oltraggioso", "combattimento", "cap_danno", "massimo")
            if valore is not None:
                valori.append(valore)
    return min(valori) if valori else None


def _inizializza_luce_persa_quinta(personaggio, contesto):
    if personaggio.get("set") != "Luce persa":
        return ""
    marker = f"_luce_persa_{contesto}"
    if personaggio.get(marker):
        return ""
    cfg = proc_cfg("Luce persa", contesto, "conversione")
    agi = personaggio.get("agi", 0)
    totale = agi * cfg["agi_mul"]
    bonus_atk = totale * cfg["quota_atk"]
    bonus_def = totale * cfg["quota_def"]
    personaggio["atk"] += bonus_atk
    personaggio["def"] += bonus_def
    personaggio["agi"] = 0
    personaggio[marker] = True
    return f"💡 {personaggio['Nome']} sacrifica {agi} AGI: +{bonus_atk:g} ATK e +{bonus_def:g} DEF!\n"


class _CombattenteQuinta(dict):
    """Copia trasparente che rende data-driven danno, cure e immunità della quinta ondata."""
    def __init__(self, originale, avversario_set=None, contesto="combattimento", cap_globale=None):
        super().__init__(originale)
        self._originale = originale
        self._avversario_set = avversario_set
        self._contesto = contesto
        self._cap_globale = cap_globale
        self._log_quinta = []
        self._immunita_gia_loggata = set()
        self._bypass_fantasmi = False

        if self.get("set") == "Girarrosto":
            marker_max = f"_girarrosto_hp_max_{contesto}"
            if marker_max not in self:
                dict.__setitem__(self, marker_max, self.get("hp", 0))

    def _log(self, testo):
        if testo:
            self._log_quinta.append(testo if testo.endswith("\n") else testo + "\n")

    def _immunita_struttura(self):
        if self._contesto != "assalto" or not self.get("set"):
            return None
        return proc_val(self.get("set"), "assalto", "immunita", "struttura")

    def _prova_girarrosto(self, nuovo_hp):
        if self.get("set") != "Girarrosto":
            return nuovo_hp
        marker_usato = f"_girarrosto_usato_{self._contesto}"
        if self.get(marker_usato):
            return nuovo_hp
        cfg = proc_cfg("Girarrosto", self._contesto, "salvezza")
        marker_max = f"_girarrosto_hp_max_{self._contesto}"
        hp_max = self.get(marker_max, self.get("hp", 0))
        soglia = hp_max * cfg["hp_soglia_percento"] / 100
        if nuovo_hp < soglia:
            ripristino = hp_max * cfg["hp_ripristino_percento"] / 100
            dict.__setitem__(self, marker_usato, True)
            self._log(f"🍖 Girarrosto! {self.get('Nome', 'Il combattente')} scende sotto il {cfg['hp_soglia_percento']}% e torna a {ripristino:g} HP!")
            return ripristino
        return nuovo_hp

    def __setitem__(self, chiave, valore):
        if chiave not in ("hp", "Scudo") or chiave not in self or not _numero_quinta(self.get(chiave)) or not _numero_quinta(valore):
            return dict.__setitem__(self, chiave, valore)

        vecchio = self.get(chiave)

        # Obscurio blocca le cure, ma non una vera resurrezione da 0 HP o meno.
        if chiave == "hp" and valore > vecchio and self._avversario_set == "Obscurio" and vecchio > 0:
            self._log(f"🌑 Obscurio inghiotte la cura di {self.get('Nome', 'un combattente')}: gli HP non aumentano!")
            return dict.__setitem__(self, chiave, vecchio)

        if valore >= vecchio:
            return dict.__setitem__(self, chiave, valore)

        perdita = vecchio - valore

        # Immunità precisa: vale solo mentre l'assedio storico sta applicando danno dalla struttura configurata.
        if chiave == "hp" and self._contesto == "assalto":
            struttura = _struttura_corrente_quinta()
            immunita = self._immunita_struttura()
            if struttura and immunita == struttura:
                if struttura not in self._immunita_gia_loggata:
                    messaggio = proc_val(self.get("set"), "assalto", "immunita", "messaggio", f"Immunità a {struttura}!")
                    self._log(messaggio)
                    self._immunita_gia_loggata.add(struttura)
                return dict.__setitem__(self, chiave, vecchio)

        # Oltraggioso impone il cap a entrambi i combattenti in combattimento.
        if self._contesto == "combattimento" and self._cap_globale is not None and perdita > self._cap_globale:
            originale = perdita
            perdita = self._cap_globale
            valore = vecchio - perdita
            self._log(f"😤 Oltraggioso limita il colpo da {originale:g} a {perdita:g} danni!")

        # Venere di ferro riduce ogni perdita di HP del proprietario.
        if chiave == "hp" and self.get("set") == "Venere di ferro":
            pct = proc_val("Venere di ferro", self._contesto, "riduzione_danno", "percento", 0)
            ridotta = round(perdita * (100 - pct) / 100)
            ridotta = max(0, ridotta)
            if ridotta != perdita:
                self._log(f"🌹 Venere di ferro riduce il danno da {perdita:g} a {ridotta:g}!")
            perdita = ridotta
            valore = vecchio - perdita

        # Festante oscuro devia ogni perdita HP nel serbatoio dei fantasmi.
        if chiave == "hp" and self.get("set") == "Festante oscuro" and self._contesto == "combattimento" and not self._bypass_fantasmi:
            accumulo = self.get("_festante_fantasmi", 0) + perdita
            dict.__setitem__(self, "_festante_fantasmi", accumulo)
            self._log(f"👻 I fantasmi assorbono {perdita:g} danni al tuo posto! ({accumulo:g} danni nelle ombre)")
            return dict.__setitem__(self, chiave, vecchio)

        if chiave == "hp":
            valore = self._prova_girarrosto(valore)

        return dict.__setitem__(self, chiave, valore)

    def applica_fantasmi_inizio_turno(self):
        if self.get("set") != "Festante oscuro" or self._contesto != "combattimento":
            return
        accumulo = self.get("_festante_fantasmi", 0)
        if accumulo <= 0:
            return
        pct = proc_val("Festante oscuro", "combattimento", "fantasmi", "percento_ritorno")
        richiesto = max(1, _math_quinta.ceil(accumulo * pct / 100))
        prima = self.get("hp", 0)
        self._bypass_fantasmi = True
        try:
            self["hp"] = prima - richiesto
        finally:
            self._bypass_fantasmi = False
        applicato = max(0, prima - self.get("hp", prima))
        dict.__setitem__(self, "_festante_fantasmi", max(0, accumulo - applicato))
        self._log(f"👻 Le ombre restituiscono {applicato:g} danni a {self.get('Nome', 'te')}! ({self.get('_festante_fantasmi', 0):g} restano nei fantasmi)")

    def sincronizza(self):
        self._originale.clear()
        self._originale.update(self)


def _danno_pulito_quinta(attaccante, bersaglio, danno, etichetta):
    danno = max(0, round(danno))
    if danno <= 0:
        return ""
    prima = bersaglio.get("hp", 0)
    bersaglio["hp"] = prima - danno
    attaccante["fatto"] = attaccante.get("fatto", 0) + danno
    return f"{etichetta} {danno} danni!\n"


def _extra_intermezzo_quinta(attaccante, bersaglio, danno_base):
    if attaccante.get("set") != "Intermezzo" or danno_base <= 0:
        return ""
    cfg = proc_cfg("Intermezzo", "combattimento", "cariche_schivata")
    cariche = attaccante.get("_intermezzo_cariche", 0)
    bonus = 0
    if cariche >= cfg["soglia_1"]:
        bonus += cfg["bonus_1"]
    if cariche >= cfg["soglia_2"]:
        bonus += cfg["bonus_2"]
    moltiplicatore = cfg["moltiplicatore"] if cariche >= cfg["soglia_3"] else 1
    totale = (danno_base + bonus) * moltiplicatore
    extra = max(0, round(totale - danno_base))
    if extra <= 0:
        return ""

    # Intermezzo modifica il colpo: se c'è ancora uno Scudo, l'extra continua sullo Scudo.
    if "Scudo" in bersaglio and bersaglio.get("Scudo", -1) >= 0:
        bersaglio["Scudo"] = bersaglio.get("Scudo", 0) - extra
    else:
        bersaglio["hp"] = bersaglio.get("hp", 0) - extra
    attaccante["fatto"] = attaccante.get("fatto", 0) + extra
    return f"🎼 Intermezzo scarica {cariche} cariche: +{extra} danni!\n"


def _risolvi_proc_anelli_quinta(eventi, main, oppo):
    testo = ""
    per_id = {id(main): main, id(oppo): oppo}
    for evento in eventi:
        proprietario = per_id.get(evento.get("owner_id"))
        if proprietario is None:
            candidati = [p for p in (main, oppo) if p.get("anello") == evento.get("anello")]
            proprietario = candidati[0] if len(candidati) == 1 else None

        # Primo al comando reagisce a ogni proc di qualunque anello, indipendentemente dal proprietario.
        cura = proc_val("Primo al comando", "combattimento", "proc_anello", "cura", 0)
        for comandante, altro in ((main, oppo), (oppo, main)):
            if comandante.get("set") == "Primo al comando" and cura:
                prima = comandante.get("hp", 0)
                comandante["hp"] = prima + cura
                curato = max(0, comandante.get("hp", prima) - prima)
                if curato > 0:
                    testo += f"🫡 Un anello si attiva: {comandante['Nome']} recupera {curato:g} HP!\n"

        if proprietario is None:
            continue
        avversario = oppo if proprietario is main else main

        if avversario.get("set") == "Nucleo dell'uragano":
            pct = proc_val("Nucleo dell'uragano", "combattimento", "proc_anello_avversario", "percento_atk_proprio")
            danno = avversario.get("atk", 0) * pct / 100
            testo += _danno_pulito_quinta(avversario, proprietario, danno, "🌪 Il vento punisce il proc dell'anello:")

        if avversario.get("set") == "Tormento di fuoco":
            pct = proc_val("Tormento di fuoco", "combattimento", "proc_anello_avversario", "percento_atk_avversario")
            danno = proprietario.get("atk", 0) * pct / 100
            testo += _danno_pulito_quinta(avversario, proprietario, danno, "🔥 Il potere dell'anello alimenta il tormento:")
    return testo


def turno(main, oppo, cond=None):
    prefisso = _inizializza_luce_persa_quinta(main, "combattimento")
    prefisso += _inizializza_luce_persa_quinta(oppo, "combattimento")

    cap = _cap_globale_quinta(main, oppo)
    main_q = _CombattenteQuinta(main, avversario_set=oppo.get("set"), contesto="combattimento", cap_globale=cap)
    oppo_q = _CombattenteQuinta(oppo, avversario_set=main.get("set"), contesto="combattimento", cap_globale=cap)

    # Contatore dei soli turni propri: usato da dispari/pari.
    main_q["_quinto_turni_propri"] = main_q.get("_quinto_turni_propri", 0) + 1
    main_q.applica_fantasmi_inizio_turno()

    eventi = []
    token = _eventi_anello_quinta.set(eventi)
    testo = ""
    try:
        hp_prima = oppo_q.get("hp", 0)
        scudo_prima = oppo_q.get("Scudo") if "Scudo" in oppo_q else None
        testo = _turno_quinta_ondata_base(main_q, oppo_q, cond)
        danno_base = _danno_su_bersaglio_terza(hp_prima, scudo_prima, oppo_q)
        schivata = "schiva il colpo" in testo

        # Reazioni ai proc anello registrati durante tutta la risoluzione storica del turno.
        testo += _risolvi_proc_anelli_quinta(eventi, main_q, oppo_q)

        if danno_base > 0 and not schivata:
            if main_q.get("set") == "Rosso D'ossidina":
                try:
                    boost(main_q, Approcci)
                    testo += f"🔴 Il colpo riesce: {main_q['Nome']} diventa ancora più *{main_q.get('Ap', 'estremo')}*!\n"
                except Exception:
                    pass

            if main_q.get("set") in ("Legionaro di Evelin", "Neo Genesi"):
                cfg = proc_cfg(main_q.get("set"), "combattimento", "danno_turno")
                turno_proprio = main_q.get("_quinto_turni_propri", 1)
                corretto = (cfg.get("parita") == "dispari" and turno_proprio % 2 == 1) or (cfg.get("parita") == "pari" and turno_proprio % 2 == 0)
                if corretto:
                    testo += _danno_pulito_quinta(main_q, oppo_q, cfg.get("danno", 0), "🦅 Colpo di ritmo:")

            testo += _extra_intermezzo_quinta(main_q, oppo_q, danno_base)

        if oppo_q.get("set") == "Intermezzo" and schivata:
            oppo_q["_intermezzo_cariche"] = oppo_q.get("_intermezzo_cariche", 0) + 1
            testo += f"🎼 {oppo_q['Nome']} trasforma la schivata in una carica di Intermezzo! ({oppo_q['_intermezzo_cariche']} cariche)\n"

        log_proxy = "".join(main_q._log_quinta + oppo_q._log_quinta)
        return prefisso + testo + log_proxy
    finally:
        _eventi_anello_quinta.reset(token)
        main_q.sincronizza()
        oppo_q.sincronizza()


def assedio(playerg, player, nemico, target, team, order, clan, meteo=None, setting=dict()):
    prefisso = _inizializza_luce_persa_quinta(player, "assalto")
    player_q = _CombattenteQuinta(player, contesto="assalto")
    try:
        testo = _assedio_quinta_ondata_base(playerg, player_q, nemico, target, team, order, clan, meteo, setting)
        return prefisso + testo + "".join(player_q._log_quinta)
    finally:
        player_q.sincronizza()
'''
    p.write_text(text, encoding="utf-8")

print("Patch quinta ondata applicata")

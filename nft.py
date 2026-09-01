import random,copy,time,string
from apscheduler.schedulers.background import BackgroundScheduler
from pyrogram import Client, ContinuePropagation, filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import date
from liste import *
from bilanciamento import PROC_CLASSI, PROC_ANELLI, NUCLEI_CONFIG, DUNGEON_CONFIG, INCANTESIMI_CONFIG, EFFETTI_CONFIG, WEEKEND_MOD_CONFIG, WEEKEND_MOD_POOL
from frasi_set import FRASI_SET_TECNICHE
from frasi_anelli import FRASI_ANELLI_TECNICHE
from frasi_incantesimi import FRASI_INCANTESIMI_TECNICHE
from pyrogram.errors import FloodWait

def proc_cfg(classe, contesto, nome):
    """Restituisce la configurazione di un proc di classe."""
    return PROC_CLASSI.get(classe, {}).get(contesto, {}).get(nome, {})


def proc_percent(classe, contesto, nome, default=0):
    """Probabilita' del proc espressa in percentuale (0..100)."""
    return proc_cfg(classe, contesto, nome).get("proc", default)


def proc_ok(numero_casuale, classe, contesto, nome, default=0):
    """Usa un random gia' estratto per non alterare la semantica dei vecchi elif."""
    return numero_casuale < (proc_percent(classe, contesto, nome, default) / 100)


def proc_val(classe, contesto, nome, chiave, default=None):
    """Legge un valore di tuning del proc."""
    return proc_cfg(classe, contesto, nome).get(chiave, default)


def anello_cfg(anello, contesto, nome):
    """Restituisce la configurazione di un effetto di anello."""
    return PROC_ANELLI.get(anello, {}).get(contesto, {}).get(nome, {})


def anello_percent(anello, contesto, nome, default=0):
    """Probabilita' del proc dell'anello espressa in percentuale (0..100)."""
    return anello_cfg(anello, contesto, nome).get("proc", default)


def anello_ok(numero_casuale, anello, contesto, nome, default=0):
    """Usa un random gia' estratto, come i vecchi confronti 0.x > num."""
    return numero_casuale < (anello_percent(anello, contesto, nome, default) / 100)


def anello_val(anello, contesto, nome, chiave, default=None):
    """Legge un valore di tuning dell'anello."""
    return anello_cfg(anello, contesto, nome).get(chiave, default)


_WEEKEND_MOD_ATTIVO = None


def weekend_mod_cfg(mod):
    return WEEKEND_MOD_CONFIG.get(mod, {})


def weekend_mod_val(mod, chiave, default=None):
    return weekend_mod_cfg(mod).get(chiave, default)


def weekend_mod_descrizione(mod):
    cfg = weekend_mod_cfg(mod)
    if not cfg:
        return "Nessun modificatore."
    return f"{cfg.get('nome', mod)} — {cfg.get('descrizione', '')}".strip()


def set_weekend_mod(mod):
    global _WEEKEND_MOD_ATTIVO
    _WEEKEND_MOD_ATTIVO = mod


def tempo_movimento_corrente(player, username, trader):
    """Cooldown reale per il movimento, condiviso tra UI e callback."""
    ccc = 3600
    if _WEEKEND_MOD_ATTIVO == "senza_frontiere":
        return weekend_mod_val(_WEEKEND_MOD_ATTIVO, "tempo_movimento", 5)
    if player[username]["setta"]["benedizione"] == "Verme delle sabbie":
        a = round(
            trader["sette"][player[username]["setta"]["loc"]]["power"]
            * (trader["sette"][player[username]["setta"]["loc"]]["%"] / 100)
        )
        ccc *= 1 - (a / 100)
    return ccc


def _snapshot_premi_dungeon(giocatore):
    exp = giocatore.get("exp", {}).get("expattuale", 0)
    return {
        "zaino": copy.deepcopy(giocatore.get("zaino", {})),
        "gloria": giocatore.get("gloria", 0),
        "grado": giocatore.get("grado", 0),
        "exp": exp,
    }


def _duplica_premi_dungeon_da_snapshot(giocatore, prima, evento):
    """Duplica solo i delta positivi prodotti dal dungeon; costi/perdite restano invariati."""
    mod = evento.get("mod") if isinstance(evento, dict) else None
    moltiplicatore = weekend_mod_val(mod, "moltiplicatore_premi_dungeon", 1)
    if not prima or moltiplicatore <= 1:
        return
    extra = moltiplicatore - 1

    zaino = giocatore.setdefault("zaino", {})
    prima_zaino = prima.get("zaino", {})
    for oggetto, quantita in list(zaino.items()):
        try:
            delta = quantita - prima_zaino.get(oggetto, 0)
        except TypeError:
            continue
        if delta > 0:
            zaino[oggetto] += delta * extra

    for chiave in ("gloria", "grado"):
        adesso = giocatore.get(chiave, 0)
        delta = adesso - prima.get(chiave, 0)
        if delta > 0:
            giocatore[chiave] = adesso + delta * extra

    exp_now = giocatore.get("exp", {}).get("expattuale", 0)
    delta_exp = exp_now - prima.get("exp", 0)
    if delta_exp > 0:
        giocatore["exp"]["expattuale"] = exp_now + delta_exp * extra


def _applica_stat_dungeon_evento(personaggio, evento):
    mod = evento.get("mod") if isinstance(evento, dict) else None
    moltiplicatore = weekend_mod_val(mod, "moltiplicatore_stat_dungeon", 1)
    if moltiplicatore == 1:
        return
    for stat in ("hp", "def", "atk", "agi"):
        personaggio[stat] = round(personaggio.get(stat, 0) * moltiplicatore)



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


def set_cangiante_disponibili():
    """Set copiabili da Cangiante: esclude quelli che forniscono solo bonus base alle statistiche."""
    escludi_solo_bonus = incantesimo_val(
        "Cangiante", "generale", "selezione_set", "escludi_solo_bonus_base", True
    )
    return [
        nome_set
        for nome_set in classi
        if not (
            escludi_solo_bonus
            and proc_val(nome_set, "generale", "set_base", "solo_bonus_base", False)
        )
    ]


def calcola_omini_assalto(giocatore, username, last_clan):
    """Conta gli assaltatori recenti e applica gli stack condivisi di Giallo.

    Ogni proc di Giallo crea entry fittizie distinte dentro lo stesso `last`
    usato dagli assaltatori reali. In questo modo gli stack sono condivisi
    dal clan e scadono con la normale finestra di 301 secondi.
    """
    ora_omini = time.time()
    prefisso_giallo = "__giallo__"

    # Rimuove solo i giallini scaduti; le entry dei giocatori reali restano
    # gestite esattamente come nello storico.
    for pl, timestamp in list(last_clan.items()):
        if str(pl).startswith(prefisso_giallo) and (ora_omini - timestamp) >= 301:
            last_clan.pop(pl, None)

    messaggio_giallo = ""
    if "Giallo" in giocatore.get("incantamenti", []) and incantesimo_ok(
        random.random(), "Giallo", "assalto", "aiutanti"
    ):
        quanti_giallini = incantesimo_val("Giallo", "assalto", "aiutanti", "aiutanti_extra")
        token_giallo = time.time_ns()
        for indice_giallo in range(quanti_giallini):
            chiave_giallo = f"{prefisso_giallo}{username}__{token_giallo}__{indice_giallo}"
            last_clan[chiave_giallo] = ora_omini
        messaggio_giallo = "Venite a me ~~Minions~~ giallini, è ora di distruggere questo posto!\n"

    matx = 0
    omini_reali = 0
    giallini_attivi = 0
    for pl, timestamp in last_clan.items():
        elapsed = ora_omini - timestamp
        if elapsed < 301 and username != pl:
            matx += 1
            if str(pl).startswith(prefisso_giallo):
                giallini_attivi += 1
            else:
                omini_reali += 1

    return matx, omini_reali, giallini_attivi, messaggio_giallo


def effetto_cfg(effetto, contesto, nome):
    """Restituisce la configurazione di un effetto temporaneo."""
    return EFFETTI_CONFIG.get(effetto, {}).get(contesto, {}).get(nome, {})


def effetto_val(effetto, contesto, nome, chiave, default=None):
    """Legge un valore di tuning di un effetto temporaneo."""
    return effetto_cfg(effetto, contesto, nome).get(chiave, default)


def dungeon_cfg(stanza, azione="evento"):
    """Configurazione di una stanza/azione del dungeon."""
    return DUNGEON_CONFIG.get("stanze", {}).get(stanza, {}).get(azione, {})


def dungeon_val(stanza, azione, chiave, default=None):
    """Legge un valore di tuning di una stanza."""
    return dungeon_cfg(stanza, azione).get(chiave, default)


def dungeon_pct(stanza, azione, chiave, default=0):
    """Legge una percentuale/soglia percentuale 0..100."""
    return float(dungeon_val(stanza, azione, chiave, default))


def dungeon_under(numero_casuale, stanza, azione, chiave, default=0):
    """Equivalente data-driven dei vecchi confronti `0.x > num`."""
    return numero_casuale < (dungeon_pct(stanza, azione, chiave, default) / 100)


def dungeon_over(numero_casuale, stanza, azione, chiave, default=0):
    """Evento sui roll alti: in config si salva la chance effettiva."""
    return numero_casuale > (1 - (dungeon_pct(stanza, azione, chiave, default) / 100))


def dungeon_test(numero_casuale, valore, stanza, azione, chiave="difficolta", default=0):
    """Prova parametrica: valore >= difficolta * roll casuale."""
    return valore >= (float(dungeon_val(stanza, azione, chiave, default)) * numero_casuale)


def dungeon_test_percent(valore, stanza, azione, chiave="difficolta", default=0):
    """Percentuale teorica di superamento di una prova STAT >= difficolta * roll."""
    difficolta = float(dungeon_val(stanza, azione, chiave, default))
    if difficolta <= 0:
        return 100.0
    return max(0.0, min(100.0, (float(valore) / difficolta) * 100.0))


def dungeon_global(sezione, chiave, default=None):
    """Legge impostazioni generali/generazione/boss/mostro del dungeon."""
    return DUNGEON_CONFIG.get(sezione, {}).get(chiave, default)


def _titolo_parametro_tecnico(chiave):
    """Converte le chiavi del database in etichette leggibili senza alterarne il significato."""
    speciali = {
        "proc": "Probabilità",
        "atk": "ATK",
        "def": "DEF",
        "agi": "AGI",
        "hp": "HP",
        "dps": "DPS",
        "powa_min": "POWA minima",
        "powe_min": "POWE minima",
        "powa_per_turno": "POWA per turno",
        "powe_per_turno": "POWE per turno",
        "cura": "Cura",
        "danno": "Danno",
        "moltiplicatore": "Moltiplicatore",
        "divisore": "Divisore",
        "hp_max": "HP massimi",
        "hp_min": "HP minimi",
        "hp_target_max": "HP bersaglio max",
        "hp_target_min": "HP bersaglio min",
        "danno_fatto_min": "Danno fatto minimo",
        "random_min": "Random minimo",
        "random_max": "Random massimo",
    }
    return speciali.get(chiave, str(chiave).replace("_", " ").strip().capitalize())


def _is_percentuale_tecnica(chiave):
    chiave = str(chiave).lower()
    return (
        chiave == "proc"
        or chiave.startswith("proc_")
        or chiave.endswith("_proc")
        or "percento" in chiave
        or chiave.endswith("_pct")
        or chiave.startswith("soglia")
        or (len(chiave) > 1 and chiave[0] == "s" and chiave[1:].isdigit())
    )


def _format_valore_tecnico(chiave, valore):
    if isinstance(valore, bool):
        return "sì" if valore else "no"
    if isinstance(valore, (list, tuple, set)):
        return ", ".join(str(x) for x in valore)
    if isinstance(valore, float) and valore.is_integer():
        valore = int(valore)
    if _is_percentuale_tecnica(chiave) and isinstance(valore, (int, float)):
        return f"{valore}%"
    return str(valore)


def _righe_config_tecnica(config):
    righe = []
    for contesto, dati in config.items():
        if not isinstance(dati, dict):
            continue

        titolo_contesto = str(contesto).replace("_", " ").capitalize()
        effetti = [(nome, parametri) for nome, parametri in dati.items() if isinstance(parametri, dict)]
        diretti = [(chiave, valore) for chiave, valore in dati.items() if not isinstance(valore, dict)]

        for effetto, parametri in effetti:
            dettagli = []
            for chiave, valore in parametri.items():
                if chiave == "nomi_equivalenti":
                    continue
                dettagli.append(
                    f"{_titolo_parametro_tecnico(chiave)}: {_format_valore_tecnico(chiave, valore)}"
                )
            if dettagli:
                nome_effetto = str(effetto).replace("_", " ").capitalize()
                righe.append(f"• {titolo_contesto} / {nome_effetto}: " + "; ".join(dettagli))

        if diretti:
            dettagli = []
            for chiave, valore in diretti:
                if chiave == "nomi_equivalenti":
                    continue
                dettagli.append(
                    f"{_titolo_parametro_tecnico(chiave)}: {_format_valore_tecnico(chiave, valore)}"
                )
            if dettagli:
                righe.append(f"• {titolo_contesto}: " + "; ".join(dettagli))
    return righe


def _numero_placeholder_tecnico(valore):
    if isinstance(valore, float) and valore.is_integer():
        return str(int(valore))
    if isinstance(valore, float):
        return f"{valore:g}"
    return str(valore)


def _valore_placeholder_set(nome, bonus, percorso):
    parti = percorso.split(".")
    if parti[0] == "bonus":
        valore = bonus or {}
        parti = parti[1:]
    else:
        valore = PROC_CLASSI.get(nome, {})
    for parte in parti:
        if not isinstance(valore, dict) or parte not in valore:
            raise KeyError(f"Placeholder set non valido: {nome}.{percorso}")
        valore = valore[parte]
    return valore


def _format_placeholder_set(valore, formato=""):
    if formato == "pct":
        return f"{_numero_placeholder_tecnico(valore)}%"
    if formato == "x":
        return f"{_numero_placeholder_tecnico(valore)}x"
    if formato == "signed":
        if isinstance(valore, (int, float)) and not isinstance(valore, bool) and valore > 0:
            return "+" + _numero_placeholder_tecnico(valore)
        return _numero_placeholder_tecnico(valore)
    if formato == "abs":
        return _numero_placeholder_tecnico(abs(valore))
    if formato == "bool":
        return "sì" if valore else "no"
    if formato == "rid_pct":
        return f"{_numero_placeholder_tecnico((1 - float(valore)) * 100)}%"
    if formato == "pct_mul":
        return f"{_numero_placeholder_tecnico(float(valore) * 100)}%"
    if formato:
        raise ValueError(f"Formato placeholder non supportato: {formato}")
    return _numero_placeholder_tecnico(valore)


def render_frase_set_tecnica(nome, bonus=None):
    template = FRASI_SET_TECNICHE.get(nome, "")
    if not template:
        return ""
    parti = []
    for letterale, campo, formato, conversione in string.Formatter().parse(template):
        parti.append(letterale)
        if campo is None:
            continue
        if conversione:
            raise ValueError(f"Conversione placeholder non supportata: {conversione}")
        valore = _valore_placeholder_set(nome, bonus or {}, campo)
        parti.append(_format_placeholder_set(valore, formato))
    return "".join(parti)


def descrizione_set_tecnica(nome, bonus=None):
    """Descrizione meccanica del set, con frase custom e dati analitici."""
    righe = ["⚙️ Dettagli del set"]
    bonus = bonus or {}
    frase_custom = render_frase_set_tecnica(nome, bonus)
    if frase_custom:
        righe.append(frase_custom)
    bonus_testo = []
    for stat in ("hp", "atk", "def", "agi"):
        valore = bonus.get(stat, 0)
        if valore:
            segno = "+" if valore > 0 else ""
            bonus_testo.append(f"{stat.upper()} {segno}{valore}")
    if bonus_testo:
        righe.append("• Bonus base: " + " | ".join(bonus_testo))

    return "\n".join(righe)


def _valore_placeholder_anello(nome, percorso):
    valore = PROC_ANELLI.get(nome, {})
    for parte in percorso.split("."):
        if not isinstance(valore, dict) or parte not in valore:
            raise KeyError(f"Placeholder anello non valido: {nome}.{percorso}")
        valore = valore[parte]
    return valore


def render_frase_anello_tecnica(nome):
    template = FRASI_ANELLI_TECNICHE.get(nome, "")
    if not template:
        return ""
    parti = []
    for letterale, campo, formato, conversione in string.Formatter().parse(template):
        parti.append(letterale)
        if campo is None:
            continue
        if conversione:
            raise ValueError(f"Conversione placeholder non supportata: {conversione}")
        valore = _valore_placeholder_anello(nome, campo)
        parti.append(_format_placeholder_set(valore, formato))
    return "".join(parti)


def descrizione_anello_tecnica(nome):
    """Descrizione leggibile dell'anello, sempre allineata a PROC_ANELLI."""
    righe = ["⚙️ Dettagli dell'anello"]
    frase = render_frase_anello_tecnica(nome)
    if frase:
        righe.append(frase)
    return "\n".join(righe)


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


def aggiorna_descrizioni_bilanciamento(liste_module):
    """Aggiunge alle descrizioni esistenti un blocco tecnico sempre allineato al bilanciamento."""
    markers = ("\n\n⚙️ Dettagli tecnici", "\n\n⚙️ Dettagli del set", "\n\n⚙️ Dettagli dell'anello", "\n\n⚙️ Dettagli dell'incantesimo")

    for nome in liste_module.classi:
        base = liste_module.frasi_set.get(nome, f"Set del {nome}.")
        for marker in markers:
            base = base.split(marker, 1)[0]
        base = base.rstrip()
        bonus_set = getattr(liste_module, "bonus", {}).get(nome, {})
        liste_module.frasi_set[nome] = base + "\n\n" + descrizione_set_tecnica(nome, bonus_set)

    for nome in list(liste_module.anelli):
        base = liste_module.anelli[nome]
        for marker in markers:
            base = base.split(marker, 1)[0]
        base = base.rstrip()
        liste_module.anelli[nome] = base + "\n\n" + descrizione_anello_tecnica(nome)


    for _, dati_libro in getattr(liste_module, "libri", {}).items():
        effetto = dati_libro.get("ef")
        if effetto not in INCANTESIMI_CONFIG:
            continue
        base = dati_libro.get("descrizione", "")
        for marker in markers:
            base = base.split(marker, 1)[0]
        base = base.rstrip()
        dati_libro["descrizione"] = base + "\n\n" + descrizione_incantesimo_tecnica(effetto)


def testo_lista_set(liste_module):
    """Catalogo completo dei set con i componenti richiesti per completarli."""
    righe = ["🧩 **SET E COMPONENTI**", ""]
    for nome in sorted(liste_module.classi, key=lambda x: str(x).lower()):
        componenti = liste_module.classi[nome]
        righe.append(f"**{nome}**")
        if componenti:
            for componente in componenti:
                righe.append(f"• `{componente}`")
        else:
            righe.append("• _Nessun componente definito_")
        righe.append("")
    return "\n".join(righe)


def take_boss(lista, numero):
    copi = copy.deepcopy(list(lista))
    out = list()
    for g in range(len(lista)):
        a = random.choice(copi)
        if a not in out:
            out.append(a)
            copi.remove(a)
        if len(out) == numero:
            break
    return out
def split(l, n):
    """
    Split a list into n chunks.
    """
    return [l[i:i+n] for i in range(0, len(l), n)]
def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z

def gestione_zaino(zaino,operazione,item,qt):
    '''Zaino ---> Zaino
    Operazione ----> Add - Remove
    item ----> Nome
    qt -----> Quantità, sempre maggiore di 0'''
    if operazione.lower() == "add":
        try:
            zaino[item] += int(qt)
        except:
            zaino[item] = int(qt)
    else:
        zaino[item] -= qt
        if zaino[item] <= 0:
            zaino.pop(item)

def is_in(tochek,big):
    value = len(tochek)
    for x in tochek:
        if x in big:
            value -= 1
    if value == 0:
        return True
    else:
        return False

def rissa(picchiatori):
    text = str()
    azioni = [" lancia una sedia a "," manda nello Shadow Realm "," ruba le patatine a "," spazia                    "," estorce il pizzo a "," fa un avance molto spinta a ",' tira un mattone a ', ' decide di ignorare ', " starnutisce in faccia a ",' tira un cazzotto ', ' ironizza sul completo di ', ' prende a padellate ', ' lega con una fune umidiccia ', ' saccagna di botte ', ' strappa le sopracciglia a ', ' fa la ceretta a ', ' infilza con uno spiedino vegano ', ' lancia una mucca di passaggio a '," soffoca con un cuscino "," tira un calcio volante in bocca "," ruba "," lancia nel burrone ", ' investe in bici ', ' richiama godzilla a mangiare ', ' lancia un gatto esplosivo ', ' implode senza morire per colpire ', ' da fuoco a ', ' >>>>>>>>>>> ', ' con un arco lunghissimo soffoca '," morde un capezzolo a "," sputa in un occhio ad "," lancia un meteorite a "," lega ad una centralina elettrica "," evoca il drago sherron per schiacciare "," si sente di poter escludere "," tira na testata assurda a "," atterra di petto su "," mangiucchia "," tira la sua stessa testa in testa a "," pone domande sbagliate a "]
    scolte = ["","","","","","","","","",""," ma qui le risse non si fanno da sole!"," ma il potere di cose non lo permette"," oppure no",", ma non finisce qui per il disgraziat*!",", ma evita tutto",", ciò non lo tange!"]
    while True:
        if len(picchiatori) == 1:
            
            break
        primo = random.choice(list(picchiatori))
        while True:
            secondo = random.choice(list(picchiatori))
            if secondo != primo:
                break
        azione = random.choice(azioni)
        svolta = random.choice(scolte)
        text += f"**{primo}**{azione}**{secondo}**__{svolta}__\n"
        if svolta == "":
            picchiatori.remove(secondo)

    text += f"\n{picchiatori[0]} è il vincitore di questa rissa!"
    return {"t":text,"p":picchiatori[0]}

def findo(nome, lista):
    for x in lista:
        if x.lower() == nome.lower():
            break
        else:
            x = None
    return x


def pairwise(it):
    listone = []
    lista = []
    rep = 0
    
    for x in it:

        lista.append(x)
        rep += 1
        if rep == 8:
            rep = 0
            listone.append(lista)
            lista = list()
    listone.append(lista)
    return listone

def match(sorters, nome):

    sortes = [a[0] for a in sorters]
    posizione = sortes.index(nome)

    if posizione < 5:
        oppo = posizione + random.randint(-posizione, 6)

    else:
        oppo = posizione + random.randint(-6, 6)

    if oppo == posizione:
        oppo += 1
    while True:

        if oppo > len(sortes):
            oppo -= 2
        else:
            break

    if oppo == posizione:
        oppo += 1

    try:
        sfidante = sortes[int(oppo)]
    except:
        sfidante = random.choice(sortes)

    return sfidante


def match_clan(sorters, nome):

    sortes = [a[0] for a in sorters]
    posizione = sortes.index(nome)

    if posizione < 5:
        oppo = posizione + random.randint(-posizione, 4)

    else:
        oppo = posizione + random.randint(-4, 4)

    if oppo == posizione:
        oppo += 1
    while True:

        if oppo > len(sortes):
            oppo -= 2
        else:
            break

    if oppo == posizione:
        oppo += 1

    sfidante = sortes[int(oppo)]

    return sfidante


def search(test_list, subs):
    rep = list()
    parts = subs.split(" ")
    for a in test_list:
        
        check = len(parts)
        value = 0
        for part in parts:
            if part.lower() in a.lower():
                value += 1
        if value >= check:
            rep.append(a)
    return rep

def is_dead(a):
    if a["hp"] <= 0:
        return True
    else:
        return False

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))

def listToString(s):

    str1 = ""
    for ele in s:
        str1 += f"{ele} "

    return str1[:-1]


def separatore(text):
    returner = list()

    contante = 0
    testo = ""

    righe = text.split("\n")
    for riga in righe:
        testo += f"{riga}\n"
        contante += len(riga)
        if contante > 3800:
            returner.append(testo)
            testo = ""
            contante = 0

    returner.append(testo)
    return returner


def incarico_premi(scelte):
    if "Togliere le trappole" not in scelte or "Fare da palo" not in scelte or "Prendere il nucleo" not in scelte:
        return "Incarico perso","L'incarico è stato perso, siete si arrivati vivi alla fine ma l'intera struttura crolla su di voi...\nTutti morti.."
    else:
        recap = dict()
        v = list()
        n = list()
        for x in scelte:
            
            recap[x] = scelte.count(x)
            if x not in v:
                v.append(x)
            if scelte.count(x) not in n:
                n.append(scelte.count(x))
        
        for g in ["Cercare una caverna","Cercare cibo",'Cercare acqua',"Fare da palo","Andare in gruppo","Ignora","Curarlo da se","Accendere il fuoco","Foraggiare la legna","Trovare la via","Dividersi","Vedere la zona circostante","Creare le tende","Chiamare aiuti","Lasciarlo in pace","Soccombere nella neve"]:
            if g not in recap:
                recap[g] = 0
            
        if len(v) == 18:
            return 'Nucleo demoniaco instabile',"Genialità"

        elif len(v) == 8:
            return 'Nucleo di bacon instabile',"Banalità"

        elif recap["Chiamare aiuti"] == 4:
            return 'Nucleo selvaggio instabile',"Amicizia"

        elif recap["Foraggiare la legna"] == 4 and recap["Creare le tende"] == 2:
            return 'Nucleo terrestre instabile',"Preparazione"

        
        elif recap["Lasciarlo in pace"] >= 3 and recap["Soccombere nella neve"] >=3:
            return 'Nucleo demoniaco instabile',"Odio"

        elif recap["Trovare la via"] >= 2 and recap["Vedere la zona circostante"] >= 2 and  recap["Dividersi"] <= 1:
            return 'Nucleo selvaggio instabile',"Curiosità"

        elif recap["Cercare una caverna"] >= 2 and recap["Ignora"] >= 2 and  recap["Curarlo da se"] >= 3:
            return 'Nucleo marittimo instabile',"Premura"

        elif n == [1,2] or n == [2,1]:        
            return 'Nucleo terrestre instabile',"Ricerca"

        elif "Accendere il fuoco" in v and recap["Accendere il fuoco"] >= 3 and recap["Cercare cibo"] >= 3:
            return 'Nucleo demoniaco instabile',"Sintonia"

        elif recap["Prendere il nucleo"] >= 2:
            return "Nucleo Necron instabile","Avarizia"

        elif recap["Andare in gruppo"] >= 2 and recap["Cercare acqua"] >= 2 and recap["Trovare la via"] >= 2:
            return "Nucleo di bacon instabile","Conoscenza"

        
        elif 2 in n and 3 in n and 4 in n:
            return 'Nucleo elettrico instabile',"Schematicità"

        elif v.count(2) > 5:
            return "Nucleo di bacon instabile","Amore"

        elif "Ignora" in v and "Accendere il fuoco" in v and "Foraggiare la legna" in v and recap["Fare da palo"] >= 2:
            return 'Nucleo terrestre instabile',"Preparazione"

        elif 1 in n and 2 in n and 4 in n:
            return "Nucleo Necron instabile","Tutto o niente"

        elif recap["Curarlo da se"] >= 4:
            return 'Nucleo elettrico instabile',"Premura"
        
        elif recap["Creare le tende"] <= 1 and recap["Trovare la via"] >= 3:
            return 'Nucleo elettrico instabile',"Sbrigatività"
        
        elif recap["Vedere la zona circostante"] >= 1 and recap["Trovare la via"] >= 3:
            return 'Nucleo elettrico instabile',"Lungimiranza"
        
        elif 4 in n:
            return 'Nucleo marittimo instabile',"Organizzazione"

        else:
            return "Nulla","Il gruppo non ha saputo organizzarsi, siete arrivati al nucleo ma esso non ha compreso la vostra natura, prefendo implodere anzichè legarsi a voi..."


def incarichiamo(cla,clan,player,app):
    if "incarico" in clan[cla]:
            elapsed = time.time() - clan[cla]["incarico"]["inizio"]
            timecc = round(elapsed//60)
            if timecc >= 480:
                for g in clan[cla]["incarico"]["partecipanti"]:
                    try:
                        app.send_message(g,"Dannazione, riuscite a decidervi o no?!\nIl nucleo impazzisce ed alza una tempesta di neve che vi caccia tutti!")
                    except:
                        pass
                clan[cla].pop("incarico")
                
            else:
                
                elapsed = time.time() - clan[cla]["incarico"]["ultima"]
                timecc = round(elapsed//60)
                
                if timecc >= 35: #2100
                    if len(clan[cla]["incarico"]["mancano"]) >= len(clan[cla]["incarico"]["partecipanti"]) and int(clan[cla]["incarico"]["scelta"]) < 7:
                        scelta = int(clan[cla]["incarico"]["scelta"])
                        clan[cla]["incarico"]["mancano"] = []
                        bottoni = list()
                        for appz in esp[scelta]:
                            bottoni.append([InlineKeyboardButton(appz, callback_data=f"inca_{appz}")])
                        casuale = random.choice(clan[cla]["incarico"]["partecipanti"])
                        
                       

                        reply_markup = InlineKeyboardMarkup(bottoni)
                        testi = {1:"""Arrivati al monte iniziate la scalata, raggiunti i 9743 m di altitudine vi fate in un pochino stanchini...\nDecidete che è ora di fare un campo base ma non è che il tempo sia esattamente favorevole, potete provare a raccattare tutto il necessario ma anche concentrarsi in molti su qualcosa può avere i suoi lati positivi.""",
                            2:"""Mentre siete intenti a fondare il campo base don perignon, primo campo alpino a più di 9020 metri con vasca idromassaggio, una strana figura inizia a farsi notare dai boschi linitrofi.\nTutti vi sentite osservati ed in pericolo.\nNon è che realmente vi faccia qualcosa, anche perchè nessuno di voi è sicuro di vederla per davvero.\nDecidete ognuno di andare avanti col campo, tanto sarà solo un Orsodruido casuale""",
                            3:f"Tutto va a gonfie vele, il campo pare ormai pronto!\nQuesto vi permetterà di cercare il nucleo per diversi giorni!\nTutto va bene, fino a quando non si sente {casuale} urlare!\nL'oscura figura l'ha attaccato e bisogna fare qualcosa, non potete permettermi di soccombere sotto di essa sotto questa nevischia!",
                            4:f"State cercando la creatura e la neve aumenta...\nPersi e senza la minima idea di cosa fare {casuale} urla per un adunata...\nLa situazione è critica, il nucleo non si trova, la tempesta aumenta e il campo è ormai lontano\nSiete destinati a soccombere?",
                            5:f"Insieme vi muovete uniti, la neve non vi ostacola ed un allegra cantilena vi spinge a muovervi all'unisolo.\nNessuno sa la via ma sa che fin quando si è riuniti nulla può bloccarvi.\nSentite un potere scorrere dentro di voi e anche se la tempesta non si placa il freddo non vi tange!\nTutto d'un tratto {casuale} cade...\nSembra spaventato e terrorizzato da qualcosa, preso dal panico corre nella foresta gelata!\n...\nLo ritrovate diverso tempo dopo gelato e spaventato",
                            6:f"Rimettete in sesto il malcapitato, che vi rivela di sapere del nucleo.\nLo seguite ed insie,e trovate un antico tempio Nori nella montagna!\nLa strana creatura è ancora chissà dove, ma il nucleo è lì davanti a voi!\nCi sono un casino di cose da fare ma poco tempo per farle!"}

                        testo = testi[scelta]
                        for g in clan[cla]["incarico"]["partecipanti"]:
                            
                            try:
                                app.send_message(g,testo,reply_markup=reply_markup)
                            except:
                                pass
                        clan[cla]["incarico"]["ultima"] = time.time()
                        clan[cla]["incarico"]["scelta"] = int(clan[cla]["incarico"]["scelta"]) + 1
                        
                    if len(clan[cla]["incarico"]["mancano"]) >= len(clan[cla]["incarico"]["partecipanti"]) and int(clan[cla]["incarico"]["scelta"]) == 7:
                        a = incarico_premi(clan[cla]["incarico"]["scelte"])
                        premio =  a[0]
                        seme = a[1]
                        frasi = {"Curiosità":f"Avete esplorato in lungo ed in largo, il nucleo bianco apprezza questa caratteristica e diventa {premio}"
    ,"Preparazione":f"Vi siete giustamente preparati al peggio, avete tenuto in considerazione tutto il possibile, come premio ottenete {premio}",
    "Organizzazione":f"Avete preparato come muovervi, siete scesi in campo convinti e fiduciosi delle vostra capacità,il nucleo bianco varia in {premio} per voi",
    "Avarizia":f"Avete cercato di prendere il più possibile, una scelta coraggiosa e rischiosa...\nIl nucleo vi premia con {premio}",
    "Lungimiranza":f"Avete osservato il luogo per il futuro, si sa mai che serva, questa lungimiranza è stata premiata con {premio}",
    "Odio":f"Avete preferito abbandonare un compagno che supportarlo...\nUna scelta non condivisibile da nessuno se non da {premio}",
    "Sbrigatività":f"Avete corso per finire, bruciato le tappe e cercato il grande premio...\nPer cosa? PEr {premio}",
    "Ricerca":f"Avete esplorato la zona, mossi cautamente e dimostrato il vero significato di queste avventure, il nucleo si converte in un {premio} per voi",
    "Amicizia":f"Cercando di salvare il vostro miglior amico e compagno di team avete dimostrato un legame fortissimo, non potreste meritarvi meno di un {premio}",
    "Premura":f"Avete ambito ad arrivare assieme, qualsiasi problema vi si ponesse davanti.\nNessun ostacolo è mai troppo per il vostro gruppo.\n{premio} totalmente meritato",
    "Conoscenza":f"Avete mosso le vostre pedine in una maniera visionaria, le vostre scelte ben ponderate ed il vostro lavoro di squadra si è distinto.\nIl nucleo bianco si converte in {premio} per voi",
    "Sintonia":f"Mosse armoniose ed uniche, un esplorazione precisa e con un senso ben distinto.\nUn armonia unica per {premio} unico.",
    "Genialità":f"Avete spaccato, un patter originale e mai visto prima, ottime reazioni ai problemi ed ai disagi, il nucleo bianco si trasforma in {premio} per voi",
    "Amore":f"2 di voi hanno sempre fatto le stesse scelte, che questo sia amore?\nNon vi dirò chi ma il nucleo si trasforma in {premio} per questo",
    "Tutto o niente":f"Gready quanto basta dove serve ma non ovunque, mi siete piaciuti.\nIl nucleo varia in {premio} per voi",
    "Schematicità":f"Ordine e rigore in un esplorazione assurda, davvero interessante, complimenti.\n{premio} è un onore per voi.",
    "Banalità":f"Una mossa un pò così, siete andati sul sicuro...\nPotevate puntare più in alto ma al nucleo non importa, che diventa così {premio}"}
                        
                        
                        if seme in frasi:
                            testo = frasi[seme]
                        else:
                            testo = seme
                        
                        if premio in nuclei:
                            pino = random.choice(clan[cla]["incarico"]["partecipanti"])
                            player[pino]["zaino"][premio] = 1
                            testo += f"\n{pino} prende il nucleo felice e contento"
                        
                        for g in clan[cla]["incarico"]["partecipanti"]:
                            
                            try:
                                app.send_message(g,testo)
                            except:
                                pass
                        
                        clan[cla].pop("incarico")





async def gestione_risse(message,app,trader,mediotourizzati,player,scelta,username):
    if scelta == "Inizia!" and username in mediotourizzati:
            dic = rissa(trader["rissa"])
            text = dic["t"]
            await message.message.delete()
            messaggini = separatore(text)
            for mess in messaggini:
                try:
                   await app.send_message(message.message.chat.id , mess)
                except Exception as r:
                    print(r)
            if "Super smash sbros sbrau" not in player[dic["p"]]["obbiettivi"]:
                player[dic["p"]]["obbiettivi"].append("Super smash sbros sbrau")
                try:
                       await app.send_message(
                            dic["p"], "Obbiettivo completato!\n**Super smash sbros sbrau**, hai vinto una rissa!"
                        )
                except:
                    pass
            await message.answer("Fatta")
    
            
    else:
            if username in trader["rissa"]:
                trader["rissa"].remove(username)
                text = "E' in corso una rissona, unisci presto!\n\n"
                stati = ["è carico","si sta riscaldando","flexa","beve un succhino","si prepara al peggio","affila le armi","è pronto","prega"]
                for x in trader["rissa"]:
                    stato = random.choice(stati)
                    text += f"{x} {stato}!\n"
                bottoni = list()
                for appz in ["Io!", "Inizia!"]:
                    bottoni.append([InlineKeyboardButton(appz, callback_data=f"rissa_{appz}")])

                reply_markup = InlineKeyboardMarkup(bottoni)
                try:
                    await message.message.edit(text, reply_markup = reply_markup)
                except FloodWait as e:
                    pass
                await message.answer("Tolto")
            else:
                if username not in []:
                    trader["rissa"].append(username)
                    text = "E' in corso una rissona, unisci presto!\n\n"
                    stati = ["è carico","si sta riscaldando","flexa","beve un succhino","si prepara al peggio","affila le armi","è pronto","prega"]
                    for x in trader["rissa"]:
                        stato = random.choice(stati)
                        text += f"{x} {stato}!\n"
                    bottoni = list()
                    for appz in ["Io!", "Inizia!"]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"rissa_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)
                    try:
                        await message.message.edit(text, reply_markup = reply_markup)
                    except FloodWait as e:
                        pass
                await message.answer("Unito")
                
async def make_party_inline(scelta,player,username,clan,message,app):
    cla = scelta.split("_")[1]
    if cla ==  player[username]["team"]:
            if "incarico" in clan[cla]:
                await message.message.edit("Non puoi lasciare vuoto il villaggio!")
            else:
                
                if username in clan[cla]["pronti"]:
                    clan[cla]["pronti"].remove(username)
                else:
                    clan[cla]["pronti"].append(username)
                if len(clan[cla]["pronti"]) == 4:
                    await message.message.edit("Siiii parte!")
                    clan[cla]["incarico"] = {"partecipanti": clan[cla]["pronti"],"mancano":clan[cla]["pronti"],"ultima":time.time(),"inizio":time.time(),"scelte":[],"scelta":1, "tipo":"Monte"}
                    for h in clan[cla]["pronti"]:
                       await app.send_message(h,"Parti per il monte innevato, nessuno sa cosa si cela al suo interno ma tutti sanno del nucleo bianco...\nNon è difficile da trovare ma una volta entrati non è possibile uscirne se non con un nucleo o morti...")
                    clan[cla].pop("pronti")
                else:
                    ps = player[username]["team"]
                    text = f"{username} cerca validi compagni per ricercare il nucleo bianco!\nChi è pronto?\n"
                    for h in clan[cla]["pronti"]:
                        text += f"-{h}\n"
                    text += "A 4 si parte subitissimo!"
                    bottoni = [InlineKeyboardButton(text="Io", callback_data=f"spedizione_{ps}")]
                    reply_markup = InlineKeyboardMarkup([bottoni])
                    await message.message.edit(text=text, reply_markup=reply_markup)
                await message.answer("Annamoo")

async def incarico(scelta,player,username,clan,message,app):
    cla = player[username]["team"]
    if "incarico" in clan[cla]:
            if username not in clan[cla]["incarico"]["mancano"]:
                clan[cla]["incarico"]["scelte"].append(scelta)
                clan[cla]["incarico"]["mancano"].append(username)
                if len( clan[cla]["incarico"]["mancano"]) >= len( clan[cla]["incarico"]["partecipanti"]):                    
                    for h in clan[cla]["incarico"]["partecipanti"]:
                        try:
                            await app.send_message(h,"Vi siete organizzati, è ora di agire!")
                        except:
                            pass
                        clan[cla]["incarico"]["ultima"] = time.time()
                    
                    
                await message.message.edit(message.message.text + f"\nDecidi {scelta}, attendiamo il resto del gruppo...")
            else:
                await message.message.edit(message.message.text)
        
    else:
            await message.message.delete()
    await message.answer(scelta)
    


async def suggerimenti_inline(scelta,username,message,trader,app):
    idx = scelta.split("_")[1]
    azione = scelta.split("_")[0]
    if username in trader["Suggerimenti"][idx]["Votanti"] and trader["Suggerimenti"][idx]["Votanti"][username] == azione:
            try:
                await message.answer("Hai già votato")
            except:
                pass
    else:
        try:
                plus = trader["Suggerimenti"][idx]["Votanti"][username]
        except:
                plus = 0
        if 1 == 1:
                
            if azione == "Chiudi" and username == "ElSalamino":
                    await message.message.edit(message.message.text + "\nChiuso!")
                    await app.send_message(trader["Suggerimenti"][idx]["Creatore"],f"Chiuso il suggerimento {idx}!")
            else:
                    if azione != "Chiudi":
                        trader["Suggerimenti"][idx]["Votanti"][username] = azione
                    bottoni = list()
                    
                    bottoni.append([InlineKeyboardButton("1", callback_data=f"suggerisci*1_{idx}"),InlineKeyboardButton("2", callback_data=f"suggerisci*2_{idx}")])
                    bottoni.append([InlineKeyboardButton("3", callback_data=f"suggerisci*3_{idx}"),InlineKeyboardButton("4", callback_data=f"suggerisci*4_{idx}")])
                    bottoni.append([InlineKeyboardButton("5", callback_data=f"suggerisci*5_{idx}"),])
                    bottoni.append([InlineKeyboardButton("Chiudi", callback_data=f"suggerisci*Chiudi_{idx}")])
                    
                    reply_markup = InlineKeyboardMarkup(bottoni)
                    valoremax= 5
                    SCORE = 0
                    for g in trader["Suggerimenti"][idx]["Votanti"]:
                        SCORE += int(trader["Suggerimenti"][idx]["Votanti"][g])
                    inp = SCORE / len(trader["Suggerimenti"][idx]["Votanti"])                    
                    h = list()
                    for g in range(10):
                        if inp == 0:
                            break
                        elif inp >= 1:
                            h.append(1)
                            inp -= 1
                        elif inp < 1:
                            h.append(round(inp*4)/4)
                            inp = 0
                    voto = ""
                    valuelune = {1:"🌕",0.75:"🌖",0.5:"🌗",.25:"🌘",0.0:"🌑"}
                    for g in h:
                        voto += valuelune[g]      
                    voto += "🌑" * (valoremax - len(voto))                

                    try:
                        await message.message.edit(message.message.text.split("|")[0] + "| " + str(voto), reply_markup = reply_markup)
                    except FloodWait as e:
                        pass
        try:
                await message.answer(f"Hai votato {azione}")
        except:
                pass

  
async def riassalto(scelta,username,message,trader,clan,app,player,last_assalto,inabilitati):
    target = scelta
    if 1 == 1:   
        if player[message.from_user.username]["team"] != None:
            other_time = last_assalto.get(username,1)
            elapsed = time.time() - other_time
            
            user = player[username]
            if player[username]["setta"]["benedizione"] == 'Gufo':
                a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
                elapsed += a
            if elapsed > random.randint(25, 44):
                if clan[user["team"]]["inguerra"] != None:
                    if username not in inabilitati:
                        last_assalto[username] = time.time()
                        g = True
                        if "incarico" in clan[user["team"]]:
                            if username in clan[user["team"]]["incarico"]["partecipanti"]:
                                g = False
                        nemico = clan[user["team"]]["nemico"]
                        if len(nemico) != 0 and g:
                            if 2 == 2:
                                if 4 == 4:                                    
                                    ordine = clan[user["team"]]["orderN"]
                                    giocatore = copy.deepcopy(player[username]["scheda"])
                                    giocatore["incantamenti"] = get_ench(player[username])
                                    if "pet" in player[username]:
                                        giocatore["animale"] = player[username]["pet"]
                                    matx, omini_reali, giallini_attivi, messaggio_giallo = calcola_omini_assalto(
                                        giocatore, username, clan[user["team"]]["last"]
                                    )

                                    serv = matx
                                    # Anima della festa potenzia solo il contributo di last.
                                    if giocatore.get("set") == "Anima della festa":
                                        serv *= proc_val("Anima della festa", "assalto", "last", "moltiplicatore")
                                    if matx < proc_val("Eroe caduto", "assalto", "supporto_clan", "compagni_soglia") and giocatore["set"] == 'Eroe caduto':
                                        serv += proc_val("Eroe caduto", "assalto", "supporto_clan", "serv_bonus_nft")
                                        
                                    if giocatore["set"] == 'Eroe della rivolta':
                                        serv = serv * proc_val("Eroe della rivolta", "assalto", "supporto_clan", "serv_mul")
                                    if player[username]["setta"]["benedizione"] == 'Orso polare' and matx > 2:
                                        
                                        a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"] /100))
                                        serv += (a/4)
                                    if player[username]["setta"]["benedizione"] == 'Kaimano' and matx <= 2:
                                        a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"] /100))
                                        serv += (a/4)
                                    bostabile = ["def", "atk", "agi"]
                                    for stat in bostabile:
    
                                        giocatore[stat] = round(giocatore[stat] + (giocatore[stat] * (serv / 12)))
                                        
                                    classe(giocatore,giocatore["set"],bonus)
                                    
                                    output = messaggio_giallo + assedio(player,
                                        giocatore,
                                        nemico,
                                        target,
                                        user["team"],
                                        ordine,
                                        clan,
                                        trader["meteo"][player[username]["location"]],
                                        clan[clan[user["team"]]["inguerra"]]["setting"]
                                        
                                    )
                                    output += f"\n{omini_reali} persone assaltano con te!"
                                    if giallini_attivi:
                                        output += f" (+{giallini_attivi} giallini attivi)"
                                    player[username]["aigettoni"]["assalti"] += 1
                                    if player[username]["aigettoni"]["assalti"] >= 70:
                                        try:
                                            player[username]["zaino"]["Gettone arena"] += 1
                                        except:
                                            player[username]["zaino"]["Gettone arena"] = 1
                                            
                                        player[username]["aigettoni"]["assalti"] = 0
                                        output += "\nA terra trovi un gettone arena!"
                                    controllo_effetti_assalto(username,player)
                                    clan[user["team"]]["last"][username] = time.time()
                                    
                                    
                                    if (
                                        "Ottima kill" not in player[username]["obbiettivi"]
                                        and "E' andata!!" in output
                                    ):
                                        player[username]["obbiettivi"].append("Ottima kill")
                                        try:
                                           await app.send_message(
                                                username,
                                                "Obbiettivo completato!\n**Ottima kill**, hai demolito una struttura!",
                                            )
                                        except:
                                            pass
                                    if giocatore["hp"] <= 0:
                                        output += "\n\nHai subito troppo danno per continuare, devi riposarti!"
                                        await message.message.edit(output)
                                        if (
                                            "Quasi tuto perfetto"
                                            not in player[username]["obbiettivi"]
                                        ):
                                            player[username]["obbiettivi"].append(
                                                "Quasi tuto perfetto"
                                            )
                                            try:
                                               await app.send_message(
                                                    username,
                                                    "Obbiettivo completato!\n**Quasi tuto perfetto**, avevi un piano perfetto, mancava poco!",
                                                )
                                            except:
                                                pass
                                        tim = user["team"]
                                        oppo = clan[tim]["inguerra"]
                                        try:
                                           await app.send_message(
                                                clan[oppo]["Creatore"],
                                                f"Le vostre difese hanno fatto fuori {username}!\n+1 potere!",
                                            )
                                        except:
                                            pass
                                        clan[oppo]["potere"] += 1
                                        inabilitati[username] = time.time()
                                    else:
                                        bottoni = list()
                                        for appz in [target]:
                                            bottoni.append([InlineKeyboardButton("Ancora!", callback_data=f"ancora_{appz}")])
                                        reply_markup = InlineKeyboardMarkup(bottoni)
                                        
                                        try:
                                            await message.message.edit(text = output,reply_markup=reply_markup)
                                        except:
                                            pass
                                    if len(nemico) == 0:
                                        if (
                                            "Ultima kill"
                                            not in player[username]["obbiettivi"]
                                        ):
                                            player[username]["obbiettivi"].append(
                                                "Ultima kill"
                                            )
                                            try:
                                               await app.send_message(
                                                    username,
                                                    "Obbiettivo completato!\n**Ultima kill**, hai distrutto tu l'ultima struttura!",
                                                )
                                            except:
                                                pass
                                        for cosetto in clan[user["team"]]["membri"]:
                                            try:
                                               await app.send_message(
                                                    cosetto,
                                                    "L'intero villaggio nemico è stato abbattuto!",
                                                )
                                            except:
                                                pass
                                        try:
                                           await app.send_message(
                                                clan[oppo]["Creatore"],
                                                f"Le vostre difese hanno fatto un orribile lavoro, sono morte tutte!",
                                            )
                                        except:
                                            pass
                                        
                                    if "fatto" in giocatore:
                                        try:
                                            clan[user["team"]]["danno"][
                                                username
                                            ] += giocatore["fatto"]
                                        except:
                                            clan[user["team"]]["danno"][
                                                username
                                            ] = giocatore["fatto"]
                                        if (
                                            "DPS" not in player[username]["obbiettivi"]
                                            and clan[user["team"]]["danno"][username]
                                            >= 30000
                                        ):
                                            player[username]["obbiettivi"].append("DPS")
                                            try:
                                               await app.send_message(
                                                    username,
                                                    "Obbiettivo completato!\n**DPS**, sei stato fortissimo in assalto, complimenti!",
                                                )
                                            except:
                                                pass
                        else:
                           await message.message.edit("Non è proprio il momento adatto per assaltare") 
                    else:
                        await message.message.edit("Sei ancora morto...")
                else:
                    await message.message.edit("Non sei in guerra!")
            else:
                
                try:
                    await message.answer("Aspetta un attimo!") 
                except:
                    pass
        else:
            await message.message.edit("Non hai un team.")

async def muoveeere(scelta,location,player,message,app, username,trader):
    if 1 == 1:
        other_time = player[username]["last"]
        now = time.time()

        elapsed = now - other_time
        ccc = tempo_movimento_corrente(player, username, trader)
        
        if elapsed > ccc:
            if scelta in move[player[username]["location"]] or player[username]["location"] == "Hub":
                player[username]["last"] = time.time()
                player[username]["location"] = scelta
                await app.edit_message_text(
                            chat_id=message.message.chat.id,
                            message_id=message.message.message_id,
                            text=f"Diretti a {scelta}!",
                        )
                await app.send_sticker(message.message.chat.id,"CAACAgIAAxkBAAEcXvhhe-08hbyQi-vw5bYll7OMCb_DNwACS1YAAp7OCwABMi4vEKi8_ZweBA")
            else:
                await app.edit_message_text(
                            chat_id=message.message.chat.id,
                            message_id=message.message.message_id,
                            text=f"Riprova!",
                    )
        else:
            
            ty_res = time.gmtime(ccc - elapsed)
            tempo = time.strftime("%H:%M:%S", ty_res)
            await app.edit_message_text(
                            chat_id=message.message.chat.id,
                            message_id=message.message.message_id,
                            text=f"Devi aspettare ancora {tempo} per muoverti!",
                    ) 

async def commerciante_inline(scelta,player,username,app,message):
    if 1 == 1:
        if scelta == "Accetta":
            if player[username]["conosciuto"] == "si":
                await app.edit_message_text(
                    chat_id=message.message.chat.id,
                    message_id=message.message.message_id,
                    text="Con te ho scambiato poco fa...",
                )
            else:

                richiesto = player[username]["vuole"]
                dato = player[username]["da"]
                if dato in anelli:
                    qt = 2
                else:
                    qt = 1
                if richiesto in player[username]["zaino"]:
                    if player[username]["zaino"][richiesto] >= 2:
                        player[username]["zaino"][richiesto] -= 2
                        if player[username]["zaino"][richiesto] <= 0:
                            player[username]["zaino"].pop(richiesto)

                        try:
                            player[username]["zaino"][dato] += qt
                        except:
                            player[username]["zaino"][dato] = qt

                        player[username]["conosciuto"] = "si"
                        tisto = f"Affare fatto, ora {dato} è tuo!"
                        player[username]["aigettoni"]["commerci"] += 1
                        if player[username]["aigettoni"]["commerci"] >= 8:
                            try:
                                player[username]["zaino"]["Gettone arena"] += 1
                            except:
                                player[username]["zaino"]["Gettone arena"] = 1
                                
                            player[username]["aigettoni"]["commerci"] = 0
                            tisto += "\nTieni ioltre questo gettone arena, a me non serve!"
                        
                        await app.edit_message_text(
                            chat_id=message.message.chat.id,
                            message_id=message.message.message_id,
                            text=tisto,
                        )
                        try:
                            player[username]["varie"]["trade"] += 1
                        except:
                            player[username]["varie"]["trade"] = 1

                    else:
                        await app.edit_message_text(
                            chat_id=message.message.chat.id,
                            message_id=message.message.message_id,
                            text="Non ne hai abbastanza, magari prima o poi li avrai...",
                        )
                else:
                    await app.edit_message_text(
                        chat_id=message.message.chat.id,
                        message_id=message.message.message_id,
                        text="Non hai quello che viene richiesto.",
                    )
        else:
            await app.edit_message_text(
                chat_id=message.message.chat.id,
                message_id=message.message.message_id,
                text="Torno sempre con nuove offerte, ricorda di farti vivo.",
            )

async def regale(regali,scelta,username,player,app,message):
        cosa = regali[scelta]["cosa"]
        datore = regali[scelta]["dachi"]

        if username != datore:
            regali.pop(scelta)
            try:
                player[username]["zaino"][cosa] += 1
            except:
                player[username]["zaino"][cosa] = 1

            esito = f"{username} prende per primo {cosa}!"
            await app.edit_message_text(
                chat_id=message.message.chat.id,
                message_id=message.message.message_id,
                text=esito,
            )

            if "Dito lesto" not in player[username]["obbiettivi"]:
                player[username]["obbiettivi"].append("Dito lesto")
                try:
                   await app.send_message(
                        username,
                        "Obbiettivo completato!\n**Dito lesto**, sei bravissimo a toccare un pulsante!",
                    )
                except:
                    pass

async def cambio_approccio(scelta,player,username,app,message):
    if 1 == 1:
        idx = scelta.split("_")[1]
        scelta = scelta.split("_")[0]
        if scelta in Approccini[player[username]["scheda"]["set"]] or scelta == "Base":
            player[username]["scheda"]["Ap"] = scelta
            if "Approcci" not in player[username]:
                player[username]["Approcci"] = dict()
            player[username]["Approcci"][idx] = scelta 
            esito = f"Hai scelto {scelta}!\n"
            try:
                text =message.message.text + "\n" + esito
            except:
                pass
            try:

                await app.edit_message_text(
                    chat_id=message.message.chat.id,
                    message_id=message.message.message_id,
                    text=text,
                )
            except:
                pass
        else:
            try:

                await app.edit_message_text(
                    chat_id=message.message.chat.id,
                    message_id=message.message.message_id,
                    text="Forse questo approccio non è adatto al tuo set",
                )
            except:
                pass
def split_list(lst, n):
    """
    Split a list into n parts
    """
    return [lst[i::n] for i in range(n)]
      
async def cambio_not(scelta,player,username,app,message):
    if 1 == 1:
        if player[username]["notifiche"][scelta] == "no":
            player[username]["notifiche"][scelta] = "si"
        elif player[username]["notifiche"][scelta] == "si":
            player[username]["notifiche"][scelta] = "no"

        
        testo = "Centro gestione notifche:\n"
        bottoni = list()
        notifichez = player[username]["notifiche"]
        v = list(split(list(notifichez),2))
        print(v)
        for x in v:
            try:
                bottoni.append([InlineKeyboardButton(x[0], callback_data=f"notifiche_{x[0]}"),InlineKeyboardButton(x[1], callback_data=f"notifiche_{x[1]}")])
                if notifichez[x[0]] == "si":
                        sz = "🔉"
                else:
                        sz = "🔇"
                if notifichez[x[1]] == "si":
                        sf = "🔉"
                else:
                    sf = "🔇"
                a = f"{x[0]} {sz}" + (((15 - len(f"{x[0]}{sz}")) * " "))
                b = f"{x[1]} {sf}"
                testo += f"{a}|{b}\n"
            except:
                bottoni.append([InlineKeyboardButton(x[0], callback_data=f"notifiche_{x[0]}")])
                if notifichez[x[0]] == "si":
                        sz = "🔉"
                else:
                        sz = "🔇"
                a = f"{x[0]} {sz}" + (((15 - len(f"{x[0]}{sz}")) * " "))
                testo += f"{a}| Soon...\n"
                    
                    

        reply_markup = InlineKeyboardMarkup(bottoni)
        await app.edit_message_text(
            chat_id=message.message.chat.id,
            message_id=message.message.message_id,
            text=testo,
            reply_markup=reply_markup,
        )


def domandami(difficoltà, risposte,max):
    
    calcolo = str()
    for g in range(difficoltà):
        calcolo += str(random.randint(0,max))
        calcolo += random.choice(["+","-","*","+","-","*","/"])      
    
    risultato = float(round(eval(calcolo[:-1])))
    rispondo = [risultato]
    for g in range(risposte):
        rispondo.append(risultato//(random.random() + random.random() + random.random()))
    random.shuffle(rispondo)
    return {"text": f"Calcola:\n{calcolo[:-1]}=","Risposte":rispondo,"corretta":risultato}    


async def shoping(scelta,player,username,app,message):
    prezzo = shop[scelta]
    if "gloria" in player[username]:

            if player[username]["gloria"] < prezzo:
                messaggio = ""
                try:

                    await app.edit_message_text(
                        chat_id=message.message.chat.id,
                        message_id=message.message.message_id,
                        text="Non hai abbastanza gloria!",
                    )
                except:
                    pass
            
            else:
                if "Prima compera" not in player[username]["obbiettivi"]:
                    player[username]["obbiettivi"].append("Prima compera")
                    try:
                       await app.send_message(
                            username,
                            "Obbiettivo completato!\n**Prima compera**, hai comprato del negozio, ottimo, fai girare l'economia!",
                        )
                    except:
                        pass

                try:
                    player[username]["zaino"][scelta] += 1
                except:
                    player[username]["zaino"][scelta] = 1

                player[username]["gloria"] -= shop[scelta]
                messaggio = f"Comprato {scelta}!"
                await message.answer(scelta)
    
async def riordino(scelta,clan,username,app,message,player):
    user = player[username]
    if user["team"] != "nessuno":
            if 1 == 1:
                if (
                    clan[user["team"]]["Creatore"] == username
                    or clan[user["team"]]["Architetto"] == username
                ):

                    clan[user["team"]]["order"].remove(scelta)
                    clan[user["team"]]["order"].append(scelta)

                    text = "Ordine strutture:\n🏃‍♂️\n"
                    for stru in clan[user["team"]]["order"]:
                        text += f"-{stru}\n"
                    text += "🚩"
                    bottoni = list()
                    for appz in clan[user["team"]]["order"]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"ordine_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)
                    try:

                        await app.edit_message_text(
                            chat_id=message.message.chat.id,
                            message_id=message.message.message_id,
                            text=text,
                            reply_markup=reply_markup,
                        )
                    except:
                        pass

async def nucealte(scelta,player,username,message,clan):
    if scelta in player[username]["zaino"]:
            player[username]["zaino"][scelta] -= 1
            if player[username]["zaino"][scelta] <= 0:
                player[username]["zaino"].pop(scelta)
            clan[player[username]["team"]]["nucleo"] = scelta
            await message.message.edit(f"{scelta} inserita!\n{decoro[scelta]}")
    else:
        await message.message.edit("MMMM, non credo tu abbia questo nucleo!")

async def bossata(scelta,player,username,app,message,last_boss,inabilitati,armi,trader):
    if 1 == 1:
            other_time = last_boss.get(username,1)

            now = time.time()

            elapsed = now - other_time
            manca = round(35 - elapsed)
            if elapsed > 35:
                manca = 0
                last_boss[username] = now

                try:
                    forza = player[username]["boss"][scelta]

                except:
                    forza = 0

                if username in list(inabilitati):
                    try:

                        await app.edit_message_text(
                            chat_id=message.message.chat.id,
                            message_id=message.message.message_id,
                            text="Non sei in grado di combattere!",
                        )
                    except:
                        pass

                else:
                    if player[username]["preso"] == True:
                        try:

                            await app.edit_message_text(
                                chat_id=message.message.chat.id,
                                message_id=message.message.message_id,
                                text="Sei in attesa di una sfida!",
                            )
                        except:
                            pass

                    
                    else:

                        nome1 = username
                        nome2 = scelta

                        user1 = copy.deepcopy(player[username]["scheda"])
                        user2 = copy.deepcopy(Boss[scelta])
                        if user1["set"] == "Paladino":
                            user1["Scudo"] = proc_val("Paladino", "boss", "scudo", "hp_scudo")
                        if user1["set"] == "Serial killer":
                            user2["hp"] = round(user2["hp"] * (proc_val("Serial killer", "generale", "inizio", "hp_target_percento") / 100))

                        controllo_effetti_sfida(username,player)
                        bostabile = ["hp", "def", "atk", "agi"]
                        user1["fatto"] = 0
                        user2["fatto"] = 0
                        user1["incantamenti"] = get_ench(player[username])
                        user2["incantamenti"] = []
                        classe(user1, user1["set"],bonus)
                        text = f"Sfida tra {nome1} e {nome2} lv {forza}, uno dei terribili boss!!\n\n"

                        if player[username]["setta"]["benedizione"] == "Caprone":
                            a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))                       
                            for stat in bostabile:
                                print(user1[stat])
                                user1[stat] = round(
                                    user1[stat] + (user1[stat] * (a / 100))
                                )
                                
                            text += "La setta ti potenzia!\n"
                            
                        for stat in bostabile:

                            user2[stat] = round(
                                user2[stat] + (user2[stat] * (forza / 12))
                            )
                        

                        approccio1 = user1["Ap"]
                        approccio2 = user2["Ap"]
                        
                        if user1["protezione"] == "armatura sakuretsu LV0":
                            stats = ["hp", "def", "atk", "agi"]
                            try:

                                arma = user1["arma"]
                                for st in stats:
                                    user1[st] += armi[arma][st]
                                text += f"L'armatura di {nome1} muta!\n"

                            except:
                                pass
                        if 1 == 1:

                            x = 0
                            while True:
                                x += 1
                                if x == 150:
                                    b = "player"
                                    a = "Boss"
                                    text += f"{nome1} cade a terra sfinito!\n"
                                    break

                                text += turno(user2, user1)
                                if is_dead(user1):
                                    b = "player"
                                    a = "Boss"

                                    break
                                elif is_dead(user2):
                                    a = "player"
                                    b = "Boss"

                                    break
                                text += turno(user1, user2)
                                if is_dead(user2):
                                    a = "player"
                                    b = "Boss"

                                    break
                                elif is_dead(user1):
                                    b = "player"
                                    a = "Boss"

                                    break

                            
                            if a == "Boss":

                                text += f"\nIl Boss lancia a terra {nome1}, ci metterà un po a riprendersi!"
                                inabilitati[nome1] = time.time()

                                if (
                                    "Non è andata meglio"
                                    not in player[username]["obbiettivi"]
                                    and "Andrà meglio la prossima volta"
                                    in player[username]["obbiettivi"]
                                ):
                                    player[username]["obbiettivi"].append(
                                        "Non è andata meglio"
                                    )
                                    try:
                                       await app.send_message(
                                            username,
                                            "Obbiettivo completato!\n**Non è andata meglio**, effettivamente non è andata meglio!",
                                        )
                                    except:
                                        pass

                                if (
                                    "Andrà meglio la prossima volta"
                                    not in player[username]["obbiettivi"]
                                ):
                                    player[username]["obbiettivi"].append(
                                        "Andrà meglio la prossima volta"
                                    )
                                    try:
                                       await app.send_message(
                                            username,
                                            "Obbiettivo completato!\n**Andrà meglio la prossima volta**, hai perso da un boss, ma la prossima volta andrà meglio!",
                                        )
                                    except:
                                        pass

                            if a == "player":
                                listina = premi_boss[scelta]
                                item = random.choice(listina).replace(
                                    "0",
                                    random.choice(
                                        [
                                            "0",
                                            "0",
                                            "0",
                                            "0",
                                            "0",
                                            "0",
                                            "0",
                                            "0",
                                            "0",
                                            "0",
                                            "0",
                                            "1",
                                            "0",
                                            "1",
                                            "1",
                                            "1",
                                            "1",
                                            "2",
                                            "2",
                                        ]
                                    ),
                                )

                                gestione_zaino(player[username]["zaino"],"add",item,1)

                                try:
                                    player[username]["gloria"] += round(
                                        10 + (10 * forza / 15)
                                    )
                                except:
                                    player[username]["gloria"] = round(
                                        10 + (10 * forza / 15)
                                    )

                                if "Boss buster" not in player[username]["obbiettivi"]:
                                    player[username]["obbiettivi"].append("Boss buster")
                                    try:
                                       await app.send_message(
                                            username,
                                            "Obbiettivo completato!\n**Boss buster**,hai battuto il tuo primo boss!",
                                        )
                                    except:
                                        pass
                                if (
                                    "Boss slayer" not in player[username]["obbiettivi"]
                                    and forza >= 5
                                ):
                                    player[username]["obbiettivi"].append("Boss slayer")
                                    try:
                                       await app.send_message(
                                            username,
                                            "Obbiettivo completato!\n**Boss slayer**,hai battuto il tuo primo boss lv 5!",
                                        )
                                    except:
                                        pass
                                if (
                                    "Capo del boss"
                                    not in player[username]["obbiettivi"]
                                    and forza >= 15
                                ):
                                    player[username]["obbiettivi"].append(
                                        "Capo del boss"
                                    )
                                    try:
                                       await app.send_message(
                                            username,
                                            "Obbiettivo completato!\n**Capo del boss**,sei fortissimo a picchiare questo boss!",
                                        )
                                    except:
                                        pass
                                if (
                                    "Maestro dei boss"
                                    not in player[username]["obbiettivi"]
                                    and forza >= 45
                                ):
                                    player[username]["obbiettivi"].append(
                                        "Maestro dei boss"
                                    )
                                    try:
                                       await app.send_message(
                                            username,
                                            "Obbiettivo completato!\n**Maestro dei boss**, ormai nulla può fermarti!",
                                        )
                                    except:
                                        pass

                                try:
                                    player[username]["boss"][scelta] += 1

                                except:
                                    player[username]["boss"][scelta] = 1

                                text += f"{nome1} batte il boss!\nAppena cade a terra coglie al volo la possibiltà e ruba {item} e gloria!"

                            await message.message.delete()
                            messaggini = separatore(text)
                            for mess in messaggini:
                                try:

                                   await app.send_message(username, mess)
                                except:
                                    pass
            else:
                await message.answer("Devi ancora respirare un pochino")
                if "Voglioso di perdere" not in player[username]["obbiettivi"]:
                    player[username]["obbiettivi"].append("Voglioso di perdere")
                    try:
                       await app.send_message(
                            username,
                            "Obbiettivo completato!\n**Voglioso di perdere**, sei in ansia di farti picchiare da un boss?",
                        )
                    except:
                        pass

                pass




def genera_dungeon(player,username,c=None):
    if c != None:
        nemicii = random.randint(dungeon_global("generazione", "stanze_min", 2), dungeon_global("generazione", "stanze_max", 8))
        visibility = random.randint(dungeon_global("generazione", "visibilita_min", 1), dungeon_global("generazione", "visibilita_max", 9))
        avvi = casa_nemici[player[username]["location"]]
        mostri = take_boss((list(casa_nemici[player[username]["location"]])+ list(casa_nemici[player[username]["location"]])+ stanze), nemicii)
        dungeon =  {"piano": 0,"mostri": mostri,"danno": 0,
        "visibility": visibility}
        
    else:
        
        
        nemicii = random.randint(dungeon_global("generazione", "stanze_min", 2), dungeon_global("generazione", "stanze_max", 8)) + (player[username]["dungeon"]["piano"] * dungeon_global("generazione", "stanze_extra_per_piano", 1))
        visibility = random.randint(dungeon_global("generazione", "visibilita_min", 1), dungeon_global("generazione", "visibilita_max", 9))
        mostri = take_boss((list(casa_nemici[player[username]["location"]])+ list(casa_nemici[player[username]["location"]])+ stanze), nemicii)
        dungeon =  {"piano": player[username]["dungeon"]["piano"] + 1,"mostri": mostri,"danno": player[username]["dungeon"]["danno"],
        "visibility": visibility
                    }
    
    return dungeon


frasi = {"miss":{
    "Bersaglio enorme":"Il bersagio non pare essere protetto!\n",
    "Spaventapasseri ornamentale":"__Lo spaventapasseri non fa nulla__",
    "Stazione laser di sicurezza" : "Nessun laser colpisce\n",
    "Accampamento" : "L'accampamento è vuoto\n",
    "Muraglione extra":"Il muraglione garantisce difesa extra a tutte le strutture!\nMa non ci tange!\n",
    "Cane da guardia":"Il cane da guardia non riesce a seguirti\n",
    "Spuntone malefico":"Lo spuntone è palesemente visibile, è impossibile caderci sopra",
    "Clone":"Compare un oscura figura alle tue spalle!\n",
    "Cannoncino":"Schivi tutte e 44 le palle di cannone!\n",
    "Fabbro incantaspade":"Il fabbro non vuole avere a che fare con te...\n",
    "Sedimento del cucciolo":"Il cucciolo di drago dorme...\n",
    "Chiesa":"La chiesa è vuota\n",
    "Centrale di cura centralizzata":"La centrale si carica fortissimo e...\n"
},
"preso":{"Bersaglio enorme":f"Il bersagio è ben difeso e non aspettandotelo subisci %s danni!(%s)\n",
    "Spaventapasseri ornamentale":f"__Lo spaventapasseri non fa nulla, ma è in mezzo__\n",
    "Stazione laser di sicurezza" : f"La stazione laser si attiva, colpendoti ripetutamente,perdi %s hp!(%s)\n",
    "Accampamento" : f"Attraversando l'accampamento cade trappola degli avversari!\n Fugge, ma questo gli costa %s hp! (%s)",
    "Muraglione extra":f"Il muraglione garantisce difesa extra a tutte le strutture!\nRmane impigliato nel muraglione, subendo %s danni!(%s)\n",
    "Cane da guardia":f"Il Cane da guardia ti morde facendoti malissimo, %s danni !(%s)\nZoppichi via!\n",
    "Spuntone malefico":f"Cadi sullo spuntone subendo %s danni, questo ti invalida un pochino!(%s)\n",
    "Clone":f"Il clone ti colpisce con un mazzuolo, subisci ben %s danni!(%s)!\n",
    "Cannoncino":f"Il cannoncino è carico e pronto a colpire!!\nVieni fatto volare via, subendo %s danni!(%s)\n",
    "Fabbro incantaspade":f"Il fabbro esce a difendere il suo villaggio e a randellate ti fa perde %s hp!(%s)\n",
    "Sedimento del cucciolo":f"Il cucciolo di drago si sveglia, e spaventato ti dà fuoco, bruciandoti per %s danni!(%s)\n",
    "Chiesa":f"Dalla chiesa escono dei credenti che colpiscono %s volte!(%s)\n",
    "Centrale di cura centralizzata":f"In qualche modo prendi %s danni dalla centrale di cura!(%s)\n"

}}

# assedio() spostato in turno_assalto.py

              

async def dungeon_boss(app, message,player,scelta,nop,username,evento,last_dungeon,inabilitati,tuttov):
    _snapshot_premi_weekend = _snapshot_premi_dungeon(player[username])
    _supporter_nome_weekend = None
    _snapshot_supporter_weekend = None
    try:
        _supporter_nome_weekend = player[username].get("supporto", {}).get("Nome")
        if _supporter_nome_weekend and _supporter_nome_weekend != username and _supporter_nome_weekend in player:
            _snapshot_supporter_weekend = _snapshot_premi_dungeon(player[_supporter_nome_weekend])
    except Exception:
        pass
    if ("Affronta" in scelta and "Boss" in player[username]["dungeon"]["mostri"]):
        other_time = last_dungeon.get(username,0)
        now = time.time() 
        modificatore = weekend_mod_val(evento.get("mod"), "mod_dungeon", 0)
        if username in nop:
            modificatore -= 60
        
        elapsed = now - other_time + modificatore 
        manca = 3 - int(elapsed) 
        if elapsed > 3:
            last_dungeon[username] = now
            nome1 = username
            try:
                player[username]["dungeon"].pop("Boss")
            except:
                pass

            user1 = copy.deepcopy(player[username]["scheda"])
            user1["incantamenti"] = get_ench(player[username])



            bossino = listToString(scelta.split(" ")[1:])
            user2 = copy.deepcopy(nemici[bossino])
            user2["incantamenti"] = []

            nome2 = user2["Nome"]
            if user1["set"] == "Paladino":
                user1["Scudo"] = proc_val("Paladino", "dungeon", "scudo", "hp_scudo")
            if user2["set"] == "Paladino":
                user2["Scudo"] = proc_val("Paladino", "dungeon", "scudo", "hp_scudo")
            if user1["set"] == "Serial killer":
                user2["hp"] = round(user2["hp"] * (proc_val("Serial killer", "generale", "inizio", "hp_target_percento") / 100))
            if user2["set"] == "Serial killer":
                user1["hp"] = round(user1["hp"] * (proc_val("Serial killer", "generale", "inizio", "hp_target_percento") / 100))
            if "supporto" in player[username]:
                if nome1 != player[username]["supporto"]["Nome"]:
                    user3 = copy.deepcopy(player[username]["supporto"])
                    user3["incantamenti"] = get_ench(player[player[username]["supporto"]["Nome"]])
                    nome3 = user3["Nome"]
                    user3["fatto"] = 0
                    if user3["set"] == "Paladino":
                        user3["Scudo"] = proc_val("Paladino", "dungeon", "scudo", "hp_scudo")
                    if user3["set"] == "Serial killer":
                        user2["hp"] = round(user2["hp"] * (proc_val("Serial killer", "generale", "inizio", "hp_target_percento") / 100))
                    classe(user3,user3["set"],bonus)
                else:
                    player[username].pop("supporto")
            
            controllo_effetti_sfida(username,player)
            bostabile = ["hp", "def", "atk", "agi"]
            inizio = user1["hp"]
            user1["hp"] -= player[username]["dungeon"]["danno"]
            user1["fatto"] = 0
            user2["fatto"] = 0
            classe(user1, user1["set"],bonus)
            classe(user2, user2["set"],bonus)


            for stat in bostabile:

                user2[stat] = round(
                    user2[stat]
                    + (
            user2[stat]
            * (player[username]["dungeon"]["piano"] / 10)
                    )
                )

            _applica_stat_dungeon_evento(user2, evento)

            if "supporto" in player[username]:
                player[username].pop("supporto")

                text = f"{nome1} incontri {nome2}, un enorme boss, nel dungeon!\nMa riesce ad evocare {nome3} di supporto!\n\n\n"
                if 'Evocabilità' in user3["incantamenti"]:
                    text += "Evocazione bomba!\n"
                    user1["atk"] += incantesimo_val("Evocabilità", "dungeon", "supporto", "atk")
                    user1["def"] += incantesimo_val("Evocabilità", "dungeon", "supporto", "def")
                    user1["agi"] += incantesimo_val("Evocabilità", "dungeon", "supporto", "agi")
                x = 0
                while True:
                    x += 1
                    if x == 350:
                        b = "player"
                        a = "Boss"
                        text += (
                            f"{nome1} cade a terra sfinito!\n"
                        )
                        break

                    text += turno(user2, user1)
                    if is_dead(user1):
                        b = "player"
                        a = "Boss"
                        if user3["set"] == 'Difensore del popolo':
                            if user3["hp"] < 0:
                                user3["hp"] = 100
                            user3["set"] = None
                            user1["hp"] += (user3["hp"]/2)
                            if user1["hp"] < 0:
                                user1["hp"] = 1
                            user3["hp"] = -1000
                            text += f"**You will not die, not yet amigo!**\n"
                        else:
                            break
                    elif is_dead(user2):
                        a = "player"
                        b = "Boss"

                        break
                    text += turno(user1, user2)
                    if is_dead(user2):
                        a = "player"
                        b = "Boss"

                        break
                    elif is_dead(user1):
                        b = "player"
                        a = "Boss"

                        if user3["set"] == 'Difensore del popolo':
                            if user3["hp"] < 0:
                                user3["hp"] = 100
                            user3["set"] = None
                            user1["hp"] += (user3["hp"]/2)
                            if user1["hp"] < 0:
                                user1["hp"] = 1
                            user3["hp"] = -1000
                            text += f"**You will not die, not yet amigo!**\n"
                        else:
                            break
                    if user3["hp"] > 0:
                        text += turno(user2, user3)
                        text += turno(user3, user2)
                        if is_dead(user2):
                            a = "player"
                            b = "Boss"

                            break
                        elif is_dead(user3):
                            text += (f"\n**{nome3} cade a terra!**\n")
            else:
                text = f"{nome1} incontri {nome2}, un enorme boss, nel dungeon!\n\n"
                x = 0
                while True:
                        x += 1
                        if x == 350:
                                b = "player"
                                a = "Boss"
                                text += (
                                    f"{nome1} cade a terra sfinito!\n"
                                )
                                break

                        text += turno(user2, user1)
                        if is_dead(user1):
                                b = "player"
                                a = "Boss"

                                break
                        elif is_dead(user2):
                                a = "player"
                                b = "Boss"

                                break
                        text += turno(user1, user2)
                        if is_dead(user2):
                                a = "player"
                                b = "Boss"

                                break
                        elif is_dead(user1):
                                b = "player"
                                a = "Boss"

                                break
            #here
            if a == "Boss":
                text += f"\n{nome1} è sfinito, non può andare avanti, viene cacciato dal dungeon!"
                player[nome1].pop("dungeon")
                inabilitati[nome1] = time.time()
                messaggini = separatore(text)
                await message.message.delete()
                for mess in messaggini:
                        await app.send_message(username, mess)
                await app.send_sticker(username,"CAACAgEAAxkBAAE2gwhg-Fa3ceNqyZc0HXkqxpXMZu2xtwACTQEAAj8RFRHiILNZLpFUfB4E",)
                
                try:
                    await app.send_message(nome3,f"Sei stato evocato da {username} contro {nome2}, ma è andata male!",)
                    await app.send_sticker(nome3,"CAACAgEAAxkBAAE2gwhg-Fa3ceNqyZc0HXkqxpXMZu2xtwACTQEAAj8RFRHiILNZLpFUfB4E",)

                except:
                    pass
            else:
                if a == "player":
                    danno = inizio - user1["hp"]
                    player[username]["dungeon"]["danno"] = danno
                    player[username]["dungeon"]["mostri"].remove("Boss")
                    manca = len(player[username]["dungeon"]["mostri"])
                    text += f"{nome1} elimina il suo nemico, può procedere l'esplorazione!\nMancano {manca} stanze!\n(Danno subito {danno})\n"
                    if random.random() > (1 - dungeon_global("boss", "exp_pct", 80) / 100):
                        player[username]["exp"]["expattuale"] += dungeon_global("boss", "exp", 3)
                        text += "\n+ 3 Exp"
                    try:
                        player[username]["grado"] += dungeon_global("boss", "grado", 2)
                    except:
                        player[username]["grado"] = dungeon_global("boss", "grado", 2)
                    
                    if manca == 0:
                        player[username]["dungeon"] = genera_dungeon(player,username)
                        text += "Hai finito questo piano, ti avventuri al successivo..."
                        await app.send_sticker(username,"CAACAgIAAxkBAAEcXvdhe-0VQLjGDUwqfcUGnMeDvh57pgACUFYAAp7OCwAB99_coLvdsZ4eBA")
                    lv = str(round(player[username]["dungeon"]["piano"] / dungeon_global("boss", "lv_divisore_piano", 2.6)))
                    eventuale = ""
                    if int(lv) > dungeon_global("boss", "lv_max_normale", 4):
                        if random.random() > (1 - dungeon_global("boss", "lv_alto_pct", 50) / 100):
                            lv = dungeon_global("boss", "lv_alto", "4")

                        else:
                            lv = dungeon_global("boss", "lv_basso", "3")
                            eventuale = "data la complessità ottieni ben 20 gloria, si so proprio sprecati..."
                    player[username]["gloria"] += dungeon_global("boss", "gloria", 20)

                    contentino = random.choice(list(tuttov)).replace("0", lv)
                    if contentino == "Dell'acqua fresca":
                        contentino = "BATH WATER"
                    text += f"\nData l'ardua sfida ottieni anche un **{contentino}** {eventuale}"
                    try:
                        player[username]["zaino"][contentino] += 1
                    except:
                        player[username]["zaino"][contentino] = 1
                    try:
                        player[username]["grado"] += 3
                    except:
                        player[username]["grado"] = 3

                    try:                        
                        text += f"\nAnche {nome3} ottiene lo stesso premio!"
                        try:
                            player[nome3]["zaino"][contentino] += 1
                        except:
                            player[nome3]["zaino"][contentino] = 1
                        try:
                            player[nome3]["grado"] += 3
                        except:
                            player[nome3]["grado"] = 3
                        await app.send_message(nome3,f"Data l'ardua sfida al fianco di {username} contro {nome2} ottieni un **{contentino}** ed 1 exp!",)
                        if "Aiuto dungeon" not in player[nome3]["obbiettivi"] and player[username]["dungeon"]["piano"] >= 8:
                            player[nome3]["obbiettivi"].append("Aiuto dungeon")
                            try:
                                await app.send_message(
                                        nome3, "Obbiettivo completato!\n**Aiuto dungeon**, hai aiutato a battere un boss di un piano alto!"
                                    )
                            except:
                                pass
                        if "MEGA aiutino" not in player[nome3]["obbiettivi"] and player[username]["dungeon"]["piano"] >= 18:
                            player[nome3]["obbiettivi"].append("MEGA aiutino")
                            try:
                                await app.send_message(
                                        nome3, "Obbiettivo completato!\n**MEGA aiutino**, hai aiutato a battere un boss di un piano molto alto!"
                                    )
                            except:
                                pass
                        
                    except:
                        pass
                    player[username]["exp"]["expattuale"] += 1
                    messaggini = separatore(text)
                    await message.message.delete()
                    for mess in messaggini:
                        await app.send_message(username, mess)
                        


        else:
            await message.answer(f"Mancano {manca} secondi!")



    _duplica_premi_dungeon_da_snapshot(player[username], _snapshot_premi_weekend, evento)
    if _snapshot_supporter_weekend is not None and _supporter_nome_weekend in player:
        _duplica_premi_dungeon_da_snapshot(player[_supporter_nome_weekend], _snapshot_supporter_weekend, evento)

async def dungeon_mostro(app, message,player,scelta,nop,username,evento,last_dungeon,nemici,inabilitati,trader):
    _snapshot_premi_weekend = _snapshot_premi_dungeon(player[username])
    if scelta in nemici:
        other_time = last_dungeon.get(username,0)
        now = time.time() 
        modificatore = weekend_mod_val(evento.get("mod"), "mod_dungeon", 0)
        if username in nop:
            modificatore -= 60
        if player[username]["setta"]["benedizione"] == "Giaguaro":
            a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
            modificatore += a
        elapsed = now - other_time + modificatore 
        
        manca = 35 - int(elapsed) 
        
        if elapsed > 35:
            last_dungeon[username] = now
            await message.message.delete()
            
            last_dungeon[username] = now
            nome1 = username
            nome2 = scelta

            user1 = copy.deepcopy(player[username]["scheda"])
            user2 = copy.deepcopy(nemici[scelta])
            if user1["set"] == "Paladino":
                user1["Scudo"] = proc_val("Paladino", "dungeon", "scudo", "hp_scudo")
            if user2["set"] == "Paladino":
                user2["Scudo"] = proc_val("Paladino", "dungeon", "scudo", "hp_scudo")
            if user1["set"] == "Serial killer":
                user2["hp"] = round(user2["hp"] * (proc_val("Serial killer", "generale", "inizio", "hp_target_percento") / 100))
            if user2["set"] == "Serial killer":
                user1["hp"] -= proc_val("Serial killer", "dungeon", "contro_serial", "danno")
            controllo_effetti_sfida(username,player)
            inizio = user1["hp"]
            user1["hp"] -= player[username]["dungeon"]["danno"]
            user1["fatto"] = 0
            user2["fatto"] = 0
            classe(user1, user1["set"],bonus)
            classe(user2, user2["set"],bonus)
                        
            user2["hp"] = user2["hp"] / 2
            stats = ["def", "atk", "agi"]
            for g in stats:
                user2[g] = round(
                    user2[g]
                    + (
            user2[g]
            * (player[username]["dungeon"]["piano"] / 8)
                    )
                )
            _applica_stat_dungeon_evento(user2, evento)
            user1["incantamenti"] = get_ench(player[username])
            user2["incantamenti"] = []
            text = f"{nome1} incontri {nome2} nel dungeon!\n\n"

            if user1["protezione"] == "armatura sakuretsu LV0":
                stats = ["hp", "def", "atk", "agi"]
                try:

                    arma = user1["arma"]
                    for st in stats:
                        user1[st] += armi[arma][st]
                    text += f"L'armatura di {nome1} muta!\n"

                except:
                    pass
            x = 0
            while True:
                    x += 1
                    if x == 350:
                        b = "player"
                        a = "Boss"
                        text += f"{nome1} cade a terra sfinito!\n"
                        break

                    text += turno(user2, user1)
                    if is_dead(user1):
                        b = "player"
                        a = "Boss"

                        break
                    elif is_dead(user2):
                        a = "player"
                        b = "Boss"

                        break
                    text += turno(user1, user2)
                    if is_dead(user2):
                        a = "player"
                        b = "Boss"

                        break
                    elif is_dead(user1):
                        b = "player"
                        a = "Boss"

                        break

            if a == "Boss":

                    text += f"\n{nome1} è sfinito, non può andare avanti, viene cacciato dal dungeon!"
                    player[nome1].pop("dungeon")
                    inabilitati[nome1] = time.time()
            else:
                if a != "Boss":
                    danno = inizio - user1["hp"]
                    player[username]["dungeon"]["danno"] = danno
                    player[username]["dungeon"]["mostri"].remove(
                        scelta
                    )
                    manca = len(
                        player[username]["dungeon"]["mostri"]
                    )
                    text += f"{nome1} elimina il suo nemico, può procedere l'esplorazione!\nMancano {manca} stanze!\n(Danno subito {danno})\n"
                    if random.random() > (1 - dungeon_global("mostro", "exp_pct", 50) / 100):
                        player[username]["exp"]["expattuale"] += dungeon_global("mostro", "exp", 2)
                        text += "\n+ 2 Exp"


                    try:
                        player[username]["grado"] += dungeon_global("mostro", "grado", 2)
                    except:
                        player[username]["grado"] = dungeon_global("mostro", "grado", 2)
                    
                    if manca == 0:
                        player[username]["dungeon"] = genera_dungeon(player,username)
                        text += "Hai finito questo piano, ti avventuri al successivo..."
                        await app.send_sticker(username,"CAACAgIAAxkBAAEcXvdhe-0VQLjGDUwqfcUGnMeDvh57pgACUFYAAp7OCwAB99_coLvdsZ4eBA")
            messaggini = separatore(text)
            for mess in messaggini:
                    try:

                        await app.send_message(username, mess)
                    except:
                        pass
                    else:

                        pass

        else:
            await message.answer(f"Mancano {manca} secondi!")



    _duplica_premi_dungeon_da_snapshot(player[username], _snapshot_premi_weekend, evento)

ARENA_MATCH_TIMEOUT = 600
ARENA_BOT_NAME = "Ermenegildo"

def _arena_round(scheda):
    return int(scheda.get("W", 0)) + int(scheda.get("L", 0))

def _arena_coda(trader):
    coda = trader.get("arena_matchmaking")
    if not isinstance(coda, dict):
        coda = {}
        trader["arena_matchmaking"] = coda
    return coda

def _arena_base_item(item):
    if item is None:
        return None
    return str(item).split(" LV")[0]

def _arena_incrementa_livello_scelta(item):
    try:
        base, livello = item.rsplit(" LV", 1)
        return f"{base} LV{int(livello) + 1}"
    except Exception:
        return item

def _arena_aggiorna_set_bot(scheda, classi):
    arma = scheda.get("arma")
    protezione = scheda.get("protezione")
    if arma is None or protezione is None:
        return

    to_c = [_arena_base_item(arma), _arena_base_item(protezione)]
    for tipo, need in classi.items():
        if to_c == need:
            scheda["set"] = tipo

    megaset = ['Neo blaster', 'Spada a protoni', 'Z-Saber', 'Chip terra', 'Chip fuoco', 'Chip elettro', 'Chip lunare']
    if is_in(to_c, megaset):
        chip = to_c[1]
        forme = {
            'Chip terra': "Forma terra",
            'Chip fuoco': "Forma fuoco",
            'Chip lunare': "Forma lunare",
            'Chip elettro': "Forma elettro",
        }
        if chip in forme:
            scheda["set"] = forme[chip]

def _arena_applica_pick_bot(scheda, scelta, armi, protezioni, Approcci, classi, trader):
    if scelta in armi:
        scheda["set"] = None
        scelta_effettiva = scelta
        arma_attuale = scheda.get("arma")
        if arma_attuale is not None:
            if _arena_base_item(arma_attuale) == _arena_base_item(scelta):
                scelta_effettiva = _arena_incrementa_livello_scelta(scelta)
            unequiA(scheda, arma_attuale, armi)
        equiA(scheda, scelta_effettiva, armi)

    elif scelta in libri:
        scheda["set"] = None
        scheda.setdefault("incantamenti", []).append(libri[scelta]["ef"])
        if len(scheda["incantamenti"]) > 2:
            scheda["incantamenti"].pop(0)

    elif scelta in protezioni:
        scheda["set"] = None
        scelta_effettiva = scelta
        protezione_attuale = scheda.get("protezione")
        if protezione_attuale is not None:
            if _arena_base_item(protezione_attuale) == _arena_base_item(scelta):
                scelta_effettiva = _arena_incrementa_livello_scelta(scelta)
            unequiP1(scheda, protezione_attuale, protezioni)
        equiP1(scheda, scelta_effettiva, protezioni)

    elif scelta in anelli:
        scheda["set"] = None
        scheda["anello"] = scelta

    elif scelta in Approcci:
        scheda["set"] = None
        scheda["Ap"] = scelta

    elif scelta == "Nulla":
        scheda["set"] = None
        if trader.get("stagione") == "nulla per tutto":
            scheda["set"] = random.choice(list(classi))

    _arena_aggiorna_set_bot(scheda, classi)

    if trader.get("stagione") == "la classe è acqua":
        scheda["set"] = random.choice(list(classi))

def _arena_opzioni_pick_bot(arenaitem, trader):
    opzioni = take_boss(arenaitem, 3) + ["Nulla"]
    if trader.get("stagione") == "scelta variagate":
        opzioni += take_boss(arenaitem, 3)
    return opzioni

def _arena_genera_ermenegildo(scheda_player, arenaitem, armi, protezioni, Approcci, classi, trader):
    partite = _arena_round(scheda_player)
    pick_umani_teorici = 4 + partite
    pick_bot = max(1, ((pick_umani_teorici * 120) + 99) // 100)

    bot = {
        "Nome": ARENA_BOT_NAME,
        "hp": 1000,
        "def": 100,
        "atk": 100,
        "agi": 20,
        "int": 0,
        "Ap": "Base",
        "schivato": False,
        "anello": None,
        "protezione": None,
        "arma": None,
        "boost": {"sfida": {}, "assalto": {}},
        "set": None,
        "draw": 0,
        "W": 0,
        "L": 0,
        "incantamenti": [],
    }

    for _ in range(pick_bot):
        scelta = random.choice(_arena_opzioni_pick_bot(arenaitem, trader))
        _arena_applica_pick_bot(bot, scelta, armi, protezioni, Approcci, classi, trader)

    return bot, pick_bot

def _arena_prepara_combattente(user, armi, Approcci):
    if user.get("protezione") == "armatura sakuretsu LV0":
        arma = user.get("arma")
        if arma in armi:
            for stat in ["hp", "def", "atk", "agi"]:
                user[stat] += armi[arma][stat]

    if user.get("set") == "Paladino":
        user["Scudo"] = proc_val("Paladino", "arena", "scudo", "hp_scudo")

    boost(user, Approcci)
    user["fatto"] = 0
    if user.get("set") in bonus:
        classe(user, user["set"], bonus)
    user.setdefault("incantamenti", [])

async def _arena_scontro_bot(app, player, username, armi, protezioni, Approcci, classi, trader):
    if username not in player or "arena" not in player[username]:
        return False

    scheda = player[username]["arena"]
    if scheda.get("W", 0) >= 10 or scheda.get("L", 0) >= 3:
        return False

    arenaitem = arenamod[trader["stagione"].lower()]
    user1 = copy.deepcopy(scheda)
    user2, pick_bot = _arena_genera_ermenegildo(
        scheda, arenaitem, armi, protezioni, Approcci, classi, trader
    )

    nome1 = username
    nome2 = ARENA_BOT_NAME
    text = (
        f"Sfida tra {nome1} e {nome2}!\n"
        f"{nome2} arriva con {pick_bot} pick completamente casuali.\n"
        f"{nome1} sceglie: {user1['Ap']}, mentre {nome2} usa {user2['Ap']}!\n\n"
    )

    if user1.get("set") == "Serial killer":
        user2["hp"] = round(user2["hp"] * (proc_val("Serial killer", "generale", "inizio", "hp_target_percento") / 100))
    if user2.get("set") == "Serial killer":
        user1["hp"] = round(user1["hp"] * (proc_val("Serial killer", "generale", "inizio", "hp_target_percento") / 100))

    _arena_prepara_combattente(user1, armi, Approcci)
    _arena_prepara_combattente(user2, armi, Approcci)

    if user1.get("anello") == "Pegno di amicizia":
        text += f"\nPartendo dal presupposto che {nome1} è un grande amico di {nome2}...\n"
    if user2.get("anello") == "Pegno di amicizia":
        text += f"\nConsiderando che {nome2} è un grande amico di {nome1}...\n"
    if user1.get("anello") == "Fascette luminose":
        text += f"\nEntra sul ring {nome1}!\n\n"
    if user2.get("anello") == "Fascette luminose":
        text += f"\nE si presenta a noi {nome2}!\n\n"

    vittoria = False
    for rip in range(1, 151):
        text += turno(user2, user1, "eventzo")
        if is_dead(user1):
            vittoria = False
            break
        if is_dead(user2):
            vittoria = True
            break

        text += turno(user1, user2, "eventzo")
        if is_dead(user2):
            vittoria = True
            break
        if is_dead(user1):
            vittoria = False
            break

        if rip == 150:
            text += f"\nLa battaglia ha stremato {nome1}, che cade a terra sfinito!\n"
            vittoria = False

    scheda = player[username]["arena"]
    if vittoria:
        scheda["W"] += 1
        esito = f"\nHai così vinto un draft contro {nome2}!\nSei a {scheda['W']} win!"
    else:
        scheda["L"] += 1
        esito = f"\nHai perso contro {nome2}, migliorati però con questo draft!\nSei a {scheda['L']} perse!"
    scheda["draw"] += 1

    if len(text) >= 3500:
        text = text[:1500] + "\n...\n" + text[-2000:]

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Avanti", callback_data="arena_Avanti")]
    ])
    chat_id = player[username].get("id", username)
    pin = scheda.get("pin")
    try:
        await app.edit_message_text(chat_id, pin, text + esito, reply_markup=reply_markup)
    except Exception:
        await app.send_message(chat_id, text + esito, reply_markup=reply_markup)
    return True

async def _arena_risolvi_scaduti(app, player, armi, protezioni, Approcci, classi, trader, escludi=None):
    coda = _arena_coda(trader)
    ora = time.time()

    for chiave, voce in list(coda.items()):
        if not isinstance(voce, dict):
            coda.pop(chiave, None)
            continue

        nome = voce.get("username")
        if not nome or nome == escludi:
            continue
        if nome not in player or "arena" not in player[nome]:
            coda.pop(chiave, None)
            continue

        scheda = player[nome]["arena"]
        if str(_arena_round(scheda)) != str(chiave) or scheda.get("draw") != 0:
            coda.pop(chiave, None)
            continue
        if scheda.get("W", 0) >= 10 or scheda.get("L", 0) >= 3:
            coda.pop(chiave, None)
            continue

        try:
            attesa = ora - float(voce.get("time", ora))
        except Exception:
            attesa = 0

        if attesa >= ARENA_MATCH_TIMEOUT:
            coda.pop(chiave, None)
            await _arena_scontro_bot(app, player, nome, armi, protezioni, Approcci, classi, trader)

async def arena(client, app, message, player, scelta, armi, protezioni, armieprot, Approcci, classi, trader, username):
    arenaitem = arenamod[trader["stagione"].lower()]
    megaset = ['Neo blaster', 'Spada a protoni', 'Z-Saber', 'Chip terra', 'Chip fuoco', 'Chip elettro', 'Chip lunare']
    scheda = player[username]["arena"]
    
    if scelta == "...":
        coda = _arena_coda(trader)
        chiave = str(_arena_round(scheda))
        voce = coda.get(chiave)
        if isinstance(voce, dict) and voce.get("username") == username:
            elapsed = time.time() - float(voce.get("time", time.time()))
            if elapsed >= ARENA_MATCH_TIMEOUT:
                coda.pop(chiave, None)
                await _arena_scontro_bot(app, player, username, armi, protezioni, Approcci, classi, trader)
                return
            manca = max(0, int(ARENA_MATCH_TIMEOUT - elapsed))
            await message.answer(f"Attendiamo ancora un avversario reale. Ermenegildo sarà disponibile tra {manca} secondi.")
        else:
            bottoni = list()
            for appz in ["Avanti"]:
                bottoni.append(
                        [InlineKeyboardButton(f"{appz}", callback_data=f"arena_{appz}")]
                    )

            reply_markup = InlineKeyboardMarkup(bottoni)
            await message.message.edit("Ricerchiamo!",reply_markup=reply_markup)


    if scelta == "Entra":
        a = scheda["atk"]
        aa = scheda["def"]
        aaa = scheda["agi"]
        aaaa = scheda["hp"]
        arma = scheda["arma"]
        protv = scheda["protezione"]
        anello = scheda["anello"]
        classed = scheda["set"]
        inca = ""
        try:
            for g in scheda["incantamenti"]:
                inca += f"{g} "
        except:
            pass
        try:

            armaa = armi[arma]["atk"]
            armad = armi[arma]["def"]
            armag = armi[arma]["agi"]
        except:
            armaa = 0
            armad = 0
            armag = 0
        try:

            armaas = protezioni[protv]["atk"]
            armads = protezioni[protv]["def"]
            armags = protezioni[protv]["agi"]
        except:
            armaas = 0
            armads = 0
            armags = 0
        approccio = scheda["Ap"]
        schedas = f"""Questo sei tu:
{classed} {approccio}
❤️ Vitalità: {aaaa}
🪓 Attacco: {a}
🥋 Difesa: {aa}
🌪️ Agilità: {aaa}

Arma: {arma}
{armaa}/{armad}/{armag}
Protezione: {protv}
{armaas}/{armads}/{armags}
Anello: {anello}
{inca}"""
        bottoni = list()
        for appz in take_boss(arenaitem, 3) + ["Nulla"]:
              
            if appz in armi:
                tip = "🗡"
            elif appz in libri:
                tip = "🪄"
            elif appz in protezioni:
                tip = "🛡"
            elif appz in Approcci:
                tip = "🤜"
            elif appz == "Nulla":
                tip = ""
            elif appz in decoro:
                tip = "✨🔄"
            
            else:
                tip = "⚙️"
            bottoni.append(
                [InlineKeyboardButton(f"{appz} {tip}", callback_data=f"arena_{appz}")]
            )
        
        if trader["stagione"] == "scelta variagate":
            for appz in take_boss(arenaitem, 3):
                  
                if appz in armi:
                    tip = "🗡"
                elif appz in libri:
                    tip = "🪄"
                elif appz in protezioni:
                    tip = "🛡"
                elif appz in Approcci:
                    tip = "🤜"
                elif appz == "Nulla":
                    tip = ""
                elif appz in decoro:
                    tip = "✨🔄"
                
                else:
                    tip = "⚙️"
                bottoni.append(
                    [InlineKeyboardButton(f"{appz} {tip}", callback_data=f"arena_{appz}")]
                )
        
        reply_markup = InlineKeyboardMarkup(bottoni)
        await message.message.edit(
            f"=====⚔️=====\nEccoci nell'arena, qui tutti sono obbligati a denudarsi e combattere con cosa trovano!\nSei davvero 1400 iq come credi?\nLe regole sono semplici, si esce solo a 10 vittorie o 3 sfide perse.\nPrenditi tutto il tempo necessario per effettuare le tue scelte armose!\n\n{schedas}", reply_markup=reply_markup)
    
    ttesto = "=====⚔️=====\n"

    if scelta in armi:
        scheda["draw"] -= 1
        scheda["set"] = None
        if scheda["arma"] != None:
            scheda["set"] = None
            arma = scheda["arma"]
            if arma.split(" LV")[0] == scelta.split(" LV")[0]:
                scelta = scelta.replace(scelta.split(
                    " LV")[1], str(int(scelta.split(" LV")[1])+1))
            unequiA(scheda, arma, armi)
        ttesto += equiA(scheda, scelta, armi)
        
    elif scelta in libri:
        scheda["draw"] -= 1
        scheda["set"] = None
        try:
            scheda["incantamenti"].append(libri[scelta]["ef"])
        except:
            scheda["incantamenti"] = [libri[scelta]["ef"]]
        
        if len(scheda["incantamenti"]) > 2:
            scheda["incantamenti"].pop(0)
        
        ttesto += f"Ora sei incantato con {scelta}\n"
    
    elif scelta in protezioni:
        scheda["draw"] -= 1
        scheda["set"] = None
        if scheda["protezione"] != None:
            prot = scheda["protezione"]
            if prot.split(" LV")[0] == scelta.split(" LV")[0]:
                scelta = scelta.replace(scelta.split(
                    " LV")[1], str(int(scelta.split(" LV")[1])+1))
            unequiP1(scheda, prot, protezioni)
        ttesto += equiP1(scheda, scelta, protezioni)
    
    elif scelta in anelli:
        scheda["draw"] -= 1
        scheda["set"] = None
        ttesto += f"Il tuo anello è ora {scelta}"
        scheda["anello"] = scelta
        
    elif scelta in Approcci:
        scheda["draw"] -= 1
        scheda["set"] = None
        ttesto += f"Il tuo apporccio è ora {scelta}"
        scheda["Ap"] = scelta
        
    elif scelta == "Nulla":
        scheda["draw"] -= 1
        scheda["set"] = None
        ttesto += "Nulla di interessante\n"
        if trader["stagione"] == "nulla per tutto":
            tipi = random.choice(list(classi))
            scheda["set"] = tipi
            ttesto += "\n" + frasi_set[tipi]
    else:
        ttesto += "Non hai scelto niente!!\n"
    arma = scheda["arma"]
    protezione = scheda["protezione"]
    
    if protezione != None and arma != None:
        listina = arma.split(" LV")
        coso = listina[0]
        listina2 = protezione.split(" LV")
        ricercato = listina2[0]
        to_c = [coso, ricercato]
        for tipi in classi:
            need = classi[tipi]
            if to_c == need:
                scheda["set"] = tipi
                ttesto += "\n" + frasi_set[tipi]
        if is_in(to_c,megaset):
            if ricercato == 'Chip terra':
                                scheda["set"] = "Forma terra"
            if ricercato == 'Chip fuoco':
                                scheda["set"] = "Forma fuoco"
            if ricercato == 'Chip lunare':
                                scheda["set"] = "Forma lunare"
            if ricercato == 'Chip elettro':
                                scheda["set"] = "Forma elettro"
            ttesto += "\n" + "Set mega equipaggiato!\nAbilità chip attivate!"
    
    if trader["stagione"] == "la classe è acqua":
        tipi = random.choice(list(classi))
        scheda["set"] = tipi
        ttesto += "\n" + frasi_set[tipi]
    
    if scelta == "Andiamo!":
        a = scheda["atk"]
        if 1 == 1:
            aa = scheda["def"]
            aaa = scheda["agi"]
            aaaa = scheda["hp"]
            arma = scheda["arma"]
            prot = scheda["protezione"]
            anello = scheda["anello"]
            classed = scheda["set"]
            inca = ""
            try:
                for g in scheda["incantamenti"]:
                    inca += f"{g} "
            except:
                pass
            try:

                armaa = armi[arma]["atk"]
                armad = armi[arma]["def"]
                armag = armi[arma]["agi"]
            except:
                armaa = 0
                armad = 0
                armag = 0 #popo
            try:

                armaas = protezioni[prot]["atk"]
                armads = protezioni[prot]["def"]
                armags = protezioni[prot]["agi"]
            except:
                armaas = 0
                armads = 0
                armags = 0
            approccio = scheda["Ap"]
            schedas = f"""Questo sei tu:
{classed} {approccio}
❤️ Vitalità: {aaaa}
🪓 Attacco: {a}
🥋 Difesa: {aa}
🌪️ Agilità: {aaa}

Arma: {arma}
{armaa}/{armad}/{armag}
Protezione: {prot}
{armaas}/{armads}/{armags}
Anello: {anello}
{inca}"""

        await _arena_risolvi_scaduti(
            app, player, armi, protezioni, Approcci, classi, trader, escludi=username
        )
        coda = _arena_coda(trader)
        chiave = str(_arena_round(scheda))
        attesa = coda.get(chiave)
        avversario_reale = None
        if isinstance(attesa, dict):
            candidato = attesa.get("username")
            if (
                candidato
                and candidato != username
                and candidato in player
                and "arena" in player[candidato]
                and player[candidato]["arena"].get("draw") == 0
                and str(_arena_round(player[candidato]["arena"])) == chiave
            ):
                avversario_reale = candidato
            elif candidato != username:
                coda.pop(chiave, None)

        if avversario_reale is not None:
            nome1 = username
            nome2 = avversario_reale
            coda.pop(chiave, None)
            user1 = copy.deepcopy(player[username]["arena"])
            user2 = copy.deepcopy(player[nome2]["arena"])
            approccio1 = user1["Ap"]
            approccio2 = user2["Ap"]
            text = f"Sfida tra {nome1} e {nome2}!\n{nome1} sceglie: {approccio1}, mentre {nome2} su {approccio2}!\n\n"
            if user1["protezione"] == "armatura sakuretsu LV0":
                stats = ["hp", "def", "atk", "agi"]
            try:
                arma = user1["arma"]
                for st in stats:
                    user1[st] += armi[arma][st]
                text += f"L'armatura di {nome1} muta!\n"

            except:
                pass

            if user2["protezione"] == "armatura sakuretsu LV0":
                stats = ["hp", "def", "atk", "agi"]
                try:
                    arma = user2["arma"]
                    for st in stats:
                        user2[st] += armi[arma][st]
                    text += f"L'armatura di {nome2} muta!\n"
                except:
                    pass

            if user1["set"] == "Paladino":
                user1["Scudo"] = proc_val("Paladino", "arena", "scudo", "hp_scudo")

            if user2["set"] == "Paladino":
                    user2["Scudo"] = proc_val("Paladino", "arena", "scudo", "hp_scudo")
            if user1["set"] == "Serial killer":
                    user2["hp"] = round(user2["hp"] * (proc_val("Serial killer", "generale", "inizio", "hp_target_percento") / 100))
            if user2["set"] == "Serial killer":
                    user1["hp"] = round(user1["hp"] * (proc_val("Serial killer", "generale", "inizio", "hp_target_percento") / 100))
            boost(user1, Approcci)
            boost(user2, Approcci)
            user1["fatto"] = 0
            user2["fatto"] = 0
            classe(user1, user1["set"], bonus)
            classe(user2, user2["set"], bonus)
            try:
                user1["incantamenti"]
            except:
                user1["incantamenti"] = []
            
            try:
                user2["incantamenti"]
            except:
                user2["incantamenti"] = []
            
            
            if user1["anello"] == "Pegno di amicizia":
                    text += f"\nPartendo dal presupposto che {nome1} è un grande amico di {nome2}...\n"

            if user2["anello"] == "Pegno di amicizia":
                    text += f"\nConsiderando che {nome2} è un grande amico di {nome1}...\n"

            if user1["anello"] == "Fascette luminose":
                    text += f"\nEntra sul ring {nome1}!\n\n"
            if user2["anello"] == "Pegno di amicizia":
                    text += f"\nE si presenta a noi {nome2}!\n\n"
            rip = 0
            sfidante = nome2
            while True:
                rip += 1
                text += turno(user2, user1,"eventzo")
                if is_dead(user1):
                    b = player[username]
                    a = player[sfidante]
                    break
                if is_dead(user2):
                    a = player[username]
                    b = player[sfidante]
                    break
                text += turno(user1, user2,"eventzo")
                if is_dead(user2):
                    a = player[username]
                    b = player[sfidante]
                    break
                if is_dead(user1):
                    b = player[username]
                    a = player[sfidante]
                    break

                if rip == 150:
                    text += f"\nLa battaglia ha stremato {nome1}, che cade a terra sfinito!\n"
                    a = player[sfidante]
                    b = player[username]
                    break
            
            a["arena"]["W"] += 1
            b["arena"]["L"] += 1
            a["arena"]["draw"] += 1
            b["arena"]["draw"] += 1
            
            if len(text) >= 3500:
                text = text[:1500] + "\n...\n" +  text[-2000:] 
            ww = a["arena"]["W"]
            wint = text + f"\nHai così vinto un draft!\nSei a {ww} win!"
            ll = b["arena"]["L"]
            lint = text + f"\nHai perso, migliorati però con questo draft!\nSei a {ll} perse!"
            bottoni = list()
            for appz in ["Avanti"]:
                bottoni.append(
                        [InlineKeyboardButton(f"{appz}", callback_data=f"arena_{appz}")]
                    )

            reply_markup = InlineKeyboardMarkup(bottoni)
            await app.edit_message_text(a["id"], a["arena"]["pin"], wint,reply_markup=reply_markup)
            await app.edit_message_text(b["id"], b["arena"]["pin"], lint,reply_markup=reply_markup)
                
                
            
        else:
            bottoni = list()
            voce_attuale = coda.get(chiave)
            if not (isinstance(voce_attuale, dict) and voce_attuale.get("username") == username):
                coda[chiave] = {"username": username, "time": time.time()}
            for appz in ["..."]:
                bottoni.append(
                        [InlineKeyboardButton(f"{appz}", callback_data=f"arena_{appz}")]
                    )
            reply_markup = InlineKeyboardMarkup(bottoni)
            await message.message.edit(
                f"Attendiamo un avversario con {_arena_round(scheda)} partite giocate!\n"
                "Dopo 10 minuti potrà intervenire Ermenegildo.",
                reply_markup=reply_markup,
            )

    if scheda["W"] < 10 and scheda["L"] < 3:

        if scheda["draw"] < 0:
            player[username].pop("arena")
            await message.message.edit("Arena chiusa!\nNon provare a barare!")
            
        elif scheda["draw"] == 0 and scelta != "Andiamo!" and scelta != "...":

            bottoni = list()
            for appz in ["Andiamo!"]:
                bottoni.append(
                    [InlineKeyboardButton(f"{appz}", callback_data=f"arena_{appz}")]
                )

            reply_markup = InlineKeyboardMarkup(bottoni)
            ik = scheda["draw"]
            if 1 == 1:
                a = scheda["atk"]
                aa = scheda["def"]
                aaa = scheda["agi"]
                aaaa = scheda["hp"]
                arma = scheda["arma"]
                prot = scheda["protezione"]
                anello = scheda["anello"]
                classed = scheda["set"]
                
                inca = ""
                try:
                    for g in scheda["incantamenti"]:
                        inca += f"{g} "
                except:
                    pass
                try:

                    armaa = armi[arma]["atk"]
                    armad = armi[arma]["def"]
                    armag = armi[arma]["agi"]
                except:
                    armaa = 0
                    armad = 0
                    armag = 0
                try:

                    armaas = protezioni[prot]["atk"]
                    armads = protezioni[prot]["def"]
                    armags = protezioni[prot]["agi"]
                except:
                    armaas = 0
                    armads = 0
                    armags = 0
                approccio = scheda["Ap"]
                schedas = f"""Questo sei tu:
{classed} {approccio}
❤️ Vitalità: {aaaa}
🪓 Attacco: {a}
🥋 Difesa: {aa}
🌪️ Agilità: {aaa}

Arma: {arma}
{armaa}/{armad}/{armag}
Protezione: {prot}
{armaas}/{armads}/{armags}
Anello: {anello}
{inca}"""
            win = scheda["W"]
            lose = scheda["L"]
            ttesto += f"\n\nHai a disposizione ancora {ik} scelte, sei pronto ad entrare nell'arena?\n{schedas}\n{win} vinte /{lose} perse"
            if classed != None and "Set all'improvviso" not in player[username]["obbiettivi"]:
                player[username]["obbiettivi"].append("Set all'improvviso")
                try:
                       await app.send_message(
                            username, "Obbiettivo completato!\n**Set all'improvviso**, trova un set in arena!"
                        )
                except:
                    pass
            
            await message.message.edit(ttesto, reply_markup=reply_markup)
        else:
            
            if scelta != "Entra" and scelta != "Andiamo!" and scelta != "...":
                a = scheda["atk"]
                aa = scheda["def"]
                aaa = scheda["agi"]
                aaaa = scheda["hp"]
                arma = scheda["arma"]
                prot = scheda["protezione"]
                anello = scheda["anello"]
                classed = scheda["set"]
                
                inca = ""
                try:
                    for g in scheda["incantamenti"]:
                        inca += f"{g} "
                except:
                    pass
                try:

                    armaa = armi[arma]["atk"]
                    armad = armi[arma]["def"]
                    armag = armi[arma]["agi"]
                except:
                    armaa = 0
                    armad = 0
                    armag = 0
                try:

                    armaas = protezioni[prot]["atk"]
                    armads = protezioni[prot]["def"]
                    armags = protezioni[prot]["agi"]
                except:
                    armaas = 0
                    armads = 0
                    armags = 0
                approccio = scheda["Ap"]
                schedas = f"""Questo sei tu:\n
{classed} {approccio}
❤️ Vitalità: {aaaa}
🪓 Attacco: {a}
🥋 Difesa: {aa}
🌪️ Agilità: {aaa}

Arma: {arma}
{armaa}/{armad}/{armag}
Protezione: {prot}
{armaas}/{armads}/{armags}
Anello: {anello}
{inca}"""
                bottoni = list()
                for appz in take_boss(arenaitem, 3) + ["Nulla"]:
                    if appz in armi:
                        tip = "🗡"
                    elif appz in libri:
                        tip = "🪄"
                    elif appz in protezioni:
                        tip = "🛡"
                    elif appz in Approcci:
                        tip = "🤜"
                    elif appz == "Nulla":
                        tip = ""
                    elif appz in decoro:
                        tip = "✨🔄"
                    else:
                        tip = "⚙️"
                    bottoni.append(
                        [InlineKeyboardButton(
                            f"{appz} {tip}", callback_data=f"arena_{appz}")]
                    )
                if trader["stagione"] == "scelta variagate":
                    for appz in take_boss(arenaitem, 3):
                    
                        if appz in armi:
                            tip = "🗡"
                        elif appz in libri:
                            tip = "🪄"
                        elif appz in protezioni:
                            tip = "🛡"
                        elif appz in Approcci:
                            tip = "🤜"
                        elif appz == "Nulla":
                            tip = ""
                        elif appz in decoro:
                            tip = "✨🔄"
                        
                        else:
                            tip = "⚙️"
                        bottoni.append(
                        [InlineKeyboardButton(f"{appz} {tip}", callback_data=f"arena_{appz}")]
                    )
                reply_markup = InlineKeyboardMarkup(bottoni)
                ik = scheda["draw"]
                ttesto += f"\nHai a disposizione ancora {ik} scelte, ora che indossiamo?{schedas}"
                await message.message.edit(ttesto, reply_markup=reply_markup)
    else:
        if scelta != "Andiamo!":
            a = scheda["atk"]
            aa = scheda["def"]
            aaa = scheda["agi"]
            aaaa = scheda["hp"]
            arma = scheda["arma"]
            prot = scheda["protezione"]
            anello = scheda["anello"]
            classed = scheda["set"]
            inca = ""
            try:
                for g in scheda["incantamenti"]:
                    inca += f"{g} "
            except:
                pass
            approccio = scheda["Ap"]
            schedas = f"""Questo sei tu:
{classed} {approccio}
❤️ Vitalità: {aaaa}
🪓 Attacco: {a}
🥋 Difesa: {aa}
🌪️ Agilità: {aaa}

Arma: {arma}
Protezione: {prot}
Anello: {anello}
{inca}"""
            win = scheda["W"]
            lose = scheda["L"]
            if win == 10 and "Lo vincitor" not in player[username]["obbiettivi"]:
                player[username]["obbiettivi"].append("Lo vincitor")
                try:
                       await app.send_message(
                            username, "Obbiettivo completato!\n**Lo vincitor**, ben 10 win in un arena, gg!"
                        )
                except:
                    pass
            
             
            if lose == 3 and "Stessa storia" not in player[username]["obbiettivi"]:
                player[username]["obbiettivi"].append("Stessa storia")
                try:
                       await app.send_message(
                            username, "Obbiettivo completato!\n**Stessa storia**, ben 3 lose in un arena, gg!"
                        )
                except:
                    pass
            
            punti = int(win) - (int(lose)/2)
            glori = round(25 * punti)
            if glori <= 0:
                glori = 25
            try:
                scheda["arenagratis"]
            except:
                scheda["arenagratis"] = False
                
            if scheda["arenagratis"] == True:
                player[username]["gloria"] += glori//2
            else:
                player[username]["gloria"] += glori
             
            inc = 0            
            if punti > -4:
                inc += 2
                
            if punti > 0:
                inc += 2
            if punti > 1:
                inc += 1
            
            if punti > 3:
                inc += 1
            if punti > 4:
                inc += 1
            if punti > 5:
                inc += 1
            
            if punti > 7:
                inc += 2
            
            if scheda["arenagratis"] == True:
                try:
                    player[username]["zaino"]["Un oggetto incartato"] += inc//2
                except:
                    player[username]["zaino"]["Un oggetto incartato"] = inc//2
            else:
                try:
                    player[username]["zaino"]["Un oggetto incartato"] += inc
                except:
                    player[username]["zaino"]["Un oggetto incartato"] = inc
                    
            exp = int(win) + int(lose)
            if scheda["arenagratis"] == True:
                player[username]["exp"]['expattuale'] += exp//2
            else:
                player[username]["exp"]['expattuale'] += exp
             
            altro = str()
            premi = [
            "Uno scudo d'oro LV0",
            "Un pugnale d'oro LV0",
            "Una balestra d'oro LV0",
            "Spada d'oro fortissima LV0",
            "Elmo d'oro fortissimo LV0",
            "Anello d'oro fortissimo",
            "Un rolex oro LV0"
        ]
            if punti > 8.4:
                mio = random.choice(premi)
                altro += f"{mio}"
                try:
                    player[username]["zaino"][mio] += 1
                except:
                    player[username]["zaino"][mio] = 1
                 
            if punti > 8.8:
                mio = random.choice(premi)
                altro += f"\n{mio}"
                try:
                    player[username]["zaino"][mio] += 1
                except:
                    player[username]["zaino"][mio] = 1
                 
            if punti > 9.6:
                mio = random.choice(premi)
                altro += f"\n{mio}"
                try:
                    player[username]["zaino"][mio] += 1
                except:
                    player[username]["zaino"][mio] = 1
                 
            
            if 0.05 > random.random() and punti >= 5:
                altro += "\nVinci anche un gettone arena!"
                mio = "Gettone arena"
                try:
                    player[username]["zaino"][mio] += 1
                except:
                    player[username]["zaino"][mio] = 1
                 
            
            premio = f"Premi:\n{glori} gloria\n{inc} incartati\n{exp} exp\n{altro}"
            
            
            if scheda["arenagratis"] == True:
                gratis = "\nI premi sono ridotti del 50% a causa della run gratuita"
            else:
                gratis = ""
            try:
                await message.message.delete()
            except:
                await message.message.edit("-Arena chiusa-")
            await app.send_message(username,f"=====⚔️=====\n{premio}\n============\n\n{schedas}\n{win} vinte /{lose} perse{gratis}")
            if win == 12:
                await app.send_sticker(username,"CAACAgIAAxkBAAEcXvlhe-1yrPdkJJZsWDPOIq2q0yazSgACIlYAAp7OCwABBSdJlvTSffIeBA")
            else:
                await app.send_sticker(username,"CAACAgIAAxkBAAEcXvphe-3WXV6dPMTbAU7gl6tJpMaPlQACIVYAAp7OCwABK-we4CtFSPQeBA")
            
            player[username].pop("arena")
            
    await message.answer("")

def boost(user,Approcci):
    bostabile = ["hp", "def", "atk", "agi"]

    for stat in bostabile:
        scelto = user["Ap"]
        user[stat] = round(user[stat] * Approcci[scelto][stat])

def controllo_effetti_sfida(username,player):
    finder = player[username]["scheda"]["boost"]["sfida"]
    remove = list()
    for eff in finder:
        finder[eff]["dur"] -= 1
        if finder[eff]["dur"] <= 0:
            remove.append(eff)
    for togli in remove:
        finder.pop(togli)

def controllo_effetti_assalto(username,player):
    finder = player[username]["scheda"]["boost"]["assalto"]
    remove = list()
    for eff in finder:
        finder[eff]["dur"] -= 1
        if finder[eff]["dur"] <= 0:
            remove.append(eff)
    for togli in remove:
        finder.pop(togli)


def correggiemoji(figura, emojiz,item_boss,item_pescatore):
    text = ""
    try:
        if figura[:-4] in emojiz:
            eventoz = emojiz[figura[:-4]]
            text = f"{eventoz}"
    except:
        pass
    if figura in emojiz:
        eventoz = emojiz[figura]
        text = f"{eventoz}"
    try:
        if figura[:-4] in item_pescatore:
            
            text = f"🎣"
    except:
        pass
    
    try:
        if figura[:-4] in item_boss:
            
            text = f"👺"
        if figura in item_boss:
            
            text = f"👺"
    except:
        pass
    
    
    return text

def equiA(user, arma, armi):
    
    stats = ["hp", "def", "atk", "agi"]
    if user["arma"] == None:
        user["arma"] = arma
        for st in stats:
            user[st] += armi[arma][st]
        text = f"Equipaggiata con successo {arma}!"
    else:
        text = "Hai già una arma addosso!"

    return text


def classe(user, setz,bonus):
    
    stats = ["hp", "def", "atk", "agi"]
    for st in stats:

        user[st] += bonus[setz][st]


def unequiA(user, arma, armi):
    
    stats = ["hp", "def", "atk", "agi"]
    if user["arma"] == None:
        text = "Non hai armi equipaggiate!"
    else:
        for st in stats:
            user[st] -= armi[arma][st]
        user["arma"] = None
        text = f"Rimossa con successo {arma}!"
    return text

def equiP1(user, protezione, protezioni):
    
    stats = ["hp", "def", "atk", "agi"]
    if user["protezione"] == None:
        user["protezione"] = protezione
        for st in stats:
            user[st] += protezioni[protezione][st]
        text = f"Equipaggiata con successo {protezione}!"
    else:
        text = f"Hai già una protezione addosso!"
    return text


def unequiP1(user, protezione, protezioni):
    
    stats = ["hp", "def", "atk", "agi"]
    if user["protezione"] == None:
        text = f"Non hai protezioni da togliere!"
    else:
        for st in stats:
            user[st] -= protezioni[protezione][st]
        user["protezione"] = None
        text = f"Rimossa con successo {protezione}!"
    return text

def intel(zaino,decoro):
      return len([x for x in zaino if x in decoro])

def take_but_not(lista,non_v):
    now = copy.deepcopy(lista)
    ash = list()
    for x in now:
        if x not in ash:
            ash.append(x)
            
    if len(ash)>1:
        while True:
            chosen = random.choice(ash)
            if chosen != non_v:
                break
        return chosen

    else:
        if ash[0] != non_v:
            return ash[0]
        else:
            return None

def get_ench(user):
    ench = list()
    scheda = user["scheda"]
    try:
        arma = scheda["arma"].split(" LV")[0]
        ench.append(user["incantamenti"][arma])
    except:
        pass
    try:
        protezione = scheda["protezione"].split(" LV")[0]
        ench.append(user["incantamenti"][protezione])
    except:
        pass
    
    return ench

def possibiles(agin, agi):

    possibile = agin - (agi / 2)

    hard = 1

    while possibile >= 0:
        possibile -= hard * 10        
        hard += 1

    finale = hard * 10 + (possibile / 10)

    return finale


def possi(quantio):
    if possi < random.randint(0,101):
        return True
    else:
        return False


# turno() spostato in turno_assalto.py



async def dungeon_stanze(app, message,player,scelta,nop,username,evento,last_dungeon,globali,inabilitati,scelte,tutto,tuttov,megaman,zombie,gungeon,magic,protezioni,armi,trader):
    _snapshot_premi_weekend = _snapshot_premi_dungeon(player[username])
    if scelta not in nemici:
        other_time = last_dungeon.get(username,0)
        now = time.time() 
        modificatore = weekend_mod_val(evento.get("mod"), "mod_dungeon", 0)
        if username in nop:
            modificatore += dungeon_global("generale", "mod_nop", -60)
        if player[username]["setta"]["benedizione"] == "Avventuriero":
            a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
            modificatore += a
        elapsed = now - other_time + modificatore 
        manca = dungeon_global("generale", "cooldown_stanza", 35) - int(elapsed)
        if (elapsed > dungeon_global("generale", "cooldown_stanza", 35) and scelta in stanze) or (elapsed > dungeon_global("generale", "cooldown_scelta", 1.1) and scelta in scelte):
            num = random.random()
            last_dungeon[username] = now
            if scelta in scelte:
                text = f"Scegli {scelta}\n"
                if (scelta == "Tocchi la crepa"
                    and "Crepaccio"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Crepaccio"
                    if dungeon_under(num, "Crepaccio", "Tocchi la crepa", "espansione_pct"):
                        text += "Il piano si deforma ed espande sotto i tuoi piedi"
                        player[username]["dungeon"]["mostri"].append(random.choice(stanze)
                        )
                    else:
                        text += "Il piano si deforma e compatta sotto i tuoi piedi"

                        sce = take_but_not(player[username]["dungeon"]["mostri"],"Crepaccio")
                        try:
                                        player[username]["dungeon"]["mostri"].remove(sce)
                        except :
                            text += "\nLe stanze erano però troppe poche, poteva succedere qualcosa ma non stavolta!\n"
                if (scelta == "Sali"
                    and "Stanza"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Stanza"
                    if dungeon_under(num, "Stanza", "Sali", "click_inerte_pct"):
                        text += "\nClicci, beh figo si è cliccabile"
                    else:
                        text += "Il piano parte in alto velocissimo, aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n\nNonostante ciò ti senti ristorato!"
                        player[username]["dungeon"]["danno"] -= dungeon_val("Stanza", "Sali", "cura", 450)
                        player[username]["dungeon"]["piano"] += dungeon_val("Stanza", "Sali", "piani", -1)


                if (scelta == "Scendi"
                    and "Stanza"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Stanza"
                    if dungeon_under(num, "Stanza", "Scendi", "click_inerte_pct"):
                        text += "\nClicci, beh figo si è cliccabile"
                    else:
                        text += "Il piano parte in basso velocissimo, aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n\nNonostante ciò ti senti orribilmente male!"   
                        if player[username]["dungeon"]["danno"] > dungeon_val("Stanza", "Scendi", "danno", 500):
                            player[username]["dungeon"]["danno"] += dungeon_val("Stanza", "Scendi", "danno", 500)
                        else:
                            player[username]["dungeon"]["danno"] = dungeon_val("Stanza", "Scendi", "danno", 500)
                            player[username]["dungeon"]["piano"] += dungeon_val("Stanza", "Scendi", "piani", 1)
                if (scelta == "Non cliccare"
                    and "Stanza"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Stanza"
                    text += "\nSi apre una porta davanti a te, ora di levarsi da qui!"

                if (scelta == "Non ora"
                    and "Spada conficcata"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Spada conficcata"
                    text += "\nok ma sappi che il tempo stringe"

                if (scelta == "Estrai la spada"
                    and "Spada conficcata"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Spada conficcata"
                    text += "\nOggi è il giorno\nIl giorno tanto atteso...\nLiberati dai tuoi pesi e sii finalmente libero!"
                    today = date.today()
                    d1 = today.strftime("%d")
                    if int(d1) in dungeon_val("Spada conficcata", "Estrai la spada", "giorni_validi", [17, 21]):
                        user = player[username]
                        scheda = user["scheda"]
                        arma = scheda["arma"]
                        prot = scheda["protezione"]
                        scheda["Ap"] = "Base"
                        scheda["set"] = None
                        unequiP1(scheda, prot, protezioni)
                        unequiA(scheda, arma, armi)
                        scheda["anello"] = None
                        user["cap"] = 0
                        pt = {"hp":"Un hp extra","atk":"Un punto attacco","def":"Un punto difesa","agi":"Un punto agilità"}
                        base = dungeon_val("Spada conficcata", "Estrai la spada", "stat_base", {"hp":1000,"atk":100,"def":100,"agi":20})
                        for x in ["hp","atk","def","agi"]:
                            dif = scheda[x] - base[x]
                            scheda[x] = base[x]
                            if dif != 0:
                                try:
                                                player[username]["zaino"][pt[x]] += dif
                                except:
                                                player[username]["zaino"][pt[x]] = dif
                    else:
                        text += "\nCosa?\nCome non è il momento?!\nERA IL MIO MOMENTO\nNOOOOOOOOOOOOOOOOOOO"
                
                if (scelta == "Metti monetina" and "Distributore" in player[username]["dungeon"]["mostri"]):
                    stanza = "Distributore"

                    if player[username]["gloria"] >= dungeon_val("Distributore", "Metti monetina", "gloria_min", 2):
                        player[username]["gloria"] -= dungeon_val("Distributore", "Metti monetina", "costo_gloria", 1)
                        if dungeon_under(num, "Distributore", "Metti monetina", "fragola_soglia_pct"):
                            text += "Metti la monetina ed esce una caramella alla fragola, nice!"
                            player[username]["dungeon"]["danno"] -= dungeon_val("Distributore", "Metti monetina", "cura_fragola", 20)
                        elif dungeon_under(num, "Distributore", "Metti monetina", "kiwi_soglia_pct"):
                            text += "Metti la monetina ed esce una caramella al kiwi e mango, nice!"
                            player[username]["dungeon"]["danno"] -= dungeon_val("Distributore", "Metti monetina", "cura_kiwi", 25)
                        elif dungeon_under(num, "Distributore", "Metti monetina", "stanza_soglia_pct"):
                            text += "Metti la monetina ed esce una caramella labirintica bianca, nice!"
                            player[username]["dungeon"]["mostri"].append(random.choice(stanze))
                        elif dungeon_under(num, "Distributore", "Metti monetina", "nemico_soglia_pct"):
                            text += "Metti la monetina ed esce una caramella labirintica bianca, nice!"
                            player[username]["dungeon"]["mostri"].append(random.choice(list(nemici)))
                        elif dungeon_under(num, "Distributore", "Metti monetina", "pesce_soglia_pct"):
                            text += "Metti la monetina ed esce una caramella al pesce, no pessimo!"
                            player[username]["dungeon"]["danno"] -= dungeon_val("Distributore", "Metti monetina", "cura_pesce", 5)

                        elif dungeon_under(num, "Distributore", "Metti monetina", "latte_soglia_pct"):
                            text += "Metti la monetina ed esce una caramella al latte, credo..."
                            player[username]["dungeon"]["danno"] += dungeon_val("Distributore", "Metti monetina", "danno_latte", 35)

                        elif dungeon_under(num, "Distributore", "Metti monetina", "gloria_soglia_pct"):
                            text += "Metti la monetina ed esce una monetina da 4 gloria, nice?"
                            player[username]["gloria"] += dungeon_val("Distributore", "Metti monetina", "premio_gloria", 4)

                        else:
                            text += "Cavolo la monetina si è bloccata nel distributore..."

                    else:
                        text += "Non hai spicci!"
                if (scelta == "Anche no" and "Distributore" in player[username]["dungeon"]["mostri"]):
                    stanza = "Distributore"
                    text += "Ti allontani senza toccare nulla, sarà una trappola"


                if (scelta == "Scommetti" and "Bisca" in player[username]["dungeon"]["mostri"]):
                    stanza = "Bisca"
                    if player[username]["gloria"] > dungeon_val("Bisca", "Scommetti", "puntata", 150):

                        tuo = random.randint(dungeon_val("Bisca", "Scommetti", "carta_min", 1), dungeon_val("Bisca", "Scommetti", "carta_max", 15))
                        suo = random.randint(dungeon_val("Bisca", "Scommetti", "carta_min", 1), dungeon_val("Bisca", "Scommetti", "carta_max", 15))
                        if tuo > suo:
                            text += f"Il tuo {tuo} batte il suo {suo}, qua si che è stata fortuna!"
                            player[username]["gloria"] += dungeon_val("Bisca", "Scommetti", "puntata", 150)
                        elif tuo == suo:
                            text += f"A quanto pare sia te che lui avete fatto {tuo}!"
                        else:
                            player[username]["gloria"] -= dungeon_val("Bisca", "Scommetti", "puntata", 150)
                            text += f"Dannazione il tuo {tuo} è più basso del suo {suo}..."

                    else:
                        text += "Cerchi di fregarmi?!"

                if (scelta == "N'altra volta" and "Bisca" in player[username]["dungeon"]["mostri"]):
                    stanza = "Bisca"
                    text += "No grazie gentilissimo torna al tuo paese che qui non abbiamo abbastanza posti di lavoro neanche per noi sfidatori onesti, lascia sta guarda non me fa parlà de politica che davvero che ha in testa il dev?"
                
                if (scelta == "Ti allontani" and "Crepaccio" in player[username]["dungeon"]["mostri"]):
                    stanza = "Crepaccio"
                    text += "Ti allontani senza toccare nulla"

                if (scelta == "Avvicinati"
                    and "Fabbro"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Fabbro"
                    if dungeon_under(num, "Fabbro", "Avvicinati", "interazione_pct"):
                        cosette = ["Una spilla rossa","Un teschio antico","Un piccolo uccellino scheletrico","Una tempesta in barattolo",]
                        random.shuffle(cosette)
                        
                        for x in cosette:
                            if x in list(player[username]["zaino"]):
                                if player[username]["zaino"][x] > dungeon_val("Fabbro", "Avvicinati", "quantita_grande", 5):
                                    quanta = round(dungeon_val("Fabbro", "Avvicinati", "base_gloria", 150) / player[username]["zaino"][x]) * dungeon_val("Fabbro", "Avvicinati", "quantita_grande", 5)
                                    player[username]["gloria"] += quanta
                                    player[username]["zaino"][x] -= dungeon_val("Fabbro", "Avvicinati", "quantita_grande", 5)
                                    text += f"\nIl fabbro nota i 5 {x} che usi come portachiavi.\nAl volo lo ruba e in cambio ti cede **{quanta} gloria**."
                                    break
                                elif player[username]["zaino"][x] >= dungeon_val("Fabbro", "Avvicinati", "quantita_minima", 2):
                                    quanta = round(dungeon_val("Fabbro", "Avvicinati", "base_gloria", 150) / player[username]["zaino"][x])
                                    player[username]["gloria"] += quanta
                                    player[username]["zaino"][x] -= 1                                    
                                    text += f"\nIl fabbro nota il {x} che usi come portachiavi.\nAl volo lo ruba e in cambio ti cede **{quanta} gloria**."
                                    break
                                else:
                                    pass
                            else:
                                text += "Meh...\n"
                    else:
                        text += "Il fabbro ti nota e non dice nulla"
                
                if (scelta == "Allontanati"
                    and "Fabbro"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Fabbro"
                    text += "Silenziosamente ti allontani, chissà che mai è qui"

                if (scelta == "Approcciala"
                    and "Fabbro"
                    in player[username]["dungeon"]["mostri"]):  
                    stanza = "Fabbro"
                    if is_in(["Uno scaglione blu","Uno scaglione verde","Uno scaglione giallo","Uno scaglione nero"], list(player[username]["zaino"])):
                        text += "Il fabbro vede gli scaglioni del medaglione celeste intorno a te e capisce."
                        male = True
                        for x in player[username]["zaino"]:
                            if "LVX" in x:
                                male = False
                                break
                        if male == True:
                            text += "\nAppena avrei equip massimi non esitare a chiedermi."
                        else:
                            player[username]["zaino"][x] -= 1
                            if player[username]["zaino"][x] == 0:
                                player[username]["zaino"].pop(x)
                            try:
                                            player[username]["zaino"][x.replace("LVX","LVMAX")] += 1
                            except:
                                            player[username]["zaino"][x.replace("LVX","LVMAX")] += 1
                            text += "\nA lei...\nSpero la mia forgiatura sia di suo gradimento"
                    else:
                        text+= "Cosa guardi?\nFatti i fatti tuoi e torna quando avrai qualcosa di utile per me!"
                
                if (scelta == "Nah"
                    and "Piedistallo"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Piedistallo"
                    text += "Ottima idea, te ne vai tranquillo"

                if (scelta == "Nutri le mucche"
                    and "Fattoria"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Fattoria"
                    text += "Ottima idea, nutri le mucche e tutto va bene.\nIl tuo karma sale, fai bene a fare buone azioni"

                    globali["Mucche"] = True

                if (scelta == "Mungi le mucche"
                    and "Fattoria"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Fattoria"
                    if globali["Mucche"] == True:
                        globali["Mucche"] = False
                        text += "Cerchi di mungere le mucche ma una ti si avvicina e lascia **2 litri di latte** in mano, che brava!"
                        try:
                                        player[username]["zaino"]["Del latte in sacchetto"] += dungeon_val("Fattoria", "Mungi le mucche", "latte", 2)
                        except:
                                        player[username]["zaino"]["Del latte in sacchetto"] = dungeon_val("Fattoria", "Mungi le mucche", "latte", 2)
                    else:
                        text += "Un mandria di mucche ti assalta, cerchi inutilmente di mungerle, non hanno cibo e mangiano te!"
                        inabilitati[username] = time.time()
                if (scelta == "Corri via" and "Stanza del sonno" in player[username]["dungeon"]["mostri"]):
                    stanza = "Stanza del sonno"
                    text += "Gas sospetti, cosa sono scemo?!"

                if (scelta == "Immergitici"
                    and "Stanza del sonno"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Stanza del sonno"
                    if dungeon_under(num, "Stanza del sonno", "Immergitici", "perdi_oggetto_soglia_pct"):
                        mas = 0
                        while True:
                            preso = random.choice(list(player[username]["zaino"]))
                            if ("Anello" in preso
                                or "1" in preso
                                or "2" in preso
                                or "3" in preso
                                or "0" in preso
                                or mas == 5
                            ) and preso not in decoro:
                                break
                            mas += 1

                        player[username]["zaino"][preso] -= 1
                        if player[username]["zaino"][preso] <= 0:
                            player[username]["zaino"].pop(preso)
                        text += f"Cadi a terra, addormentato e privo di forze...\nSenti però qualcosa muoversi nelle vicinaze!\n\nAl tuo risveglio noti di aver **perso **{preso}**..."
                    elif dungeon_under(num, "Stanza del sonno", "Immergitici", "danno_soglia_pct"):
                        text += "Un sonno stravolgente ti assorbe, non riesci a stare in piedi!\nDurante la tua caduta colpisci una libreria..."
                        player[username]["dungeon"]["danno"] += dungeon_val("Stanza del sonno", "Immergitici", "danno", 100)
                    elif dungeon_under(num, "Stanza del sonno", "Immergitici", "cura_soglia_pct"):
                        text += "Un sonno ristoratore ti avvolge, ti senti curato dai tuoi danni!"
                        player[username]["dungeon"]["danno"] -= dungeon_val("Stanza del sonno", "Immergitici", "cura", 200)
                    elif dungeon_under(num, "Stanza del sonno", "Immergitici", "duplica_soglia_pct"):
                        mas = 0
                        while True:
                            preso = random.choice(
                                list(player[username]["zaino"])
                            )
                            if (
                                "Anello" in preso
                                or "1" in preso
                                or "2" in preso
                                or "3" in preso
                                or "0" in preso
                                or mas == 5
                            ) and preso not in decoro:
                                break
                            mas += 1

                        player[username]["zaino"][preso] += 1
                        text += f"Nel sonno senti il tuo zaino muoversi, appare di fronte a te **{preso}** in sogno!\nAl tuo risveglio preoccupato provi a cercarla e spettacolarmente **ne trovi 2!**"
                    else:
                        text += "Ok era solo nebbiolina"
                        if "Milano tutta la vita" not in player[username]["obbiettivi"]:
                            player[username]["obbiettivi"].append("Milano tutta la vita")
                            try:
                                await app.send_message(
                                        username, "Obbiettivo completato!\n**Milano tutta la vita**, trova Milano nei dungeon e taac obbiettivo!"
                                    )
                            except:
                                pass

                if (scelta == "Ritirati"
                    and "Chiesa"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Chiesa"
                    text += "Ti giri e ti allontani, che se ne vadano al diavolo sti creduloni"
                if (scelta == "Prega"
                    and "Chiesa"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Chiesa"
                    sit = player[username]["scheda"]["set"]
                    if sit in dungeon_val("Chiesa", "Prega", "classi_gradite", []):
                        lib = random.choice(list(libri))
                        gestione_zaino(player[username]["zaino"],"add",lib,1)
                        text += f"Ti avvicini all'altare e il gran sacerdote ti concede una copia di {lib}, che onore!"
                    else:
                        if dungeon_over(num, "Chiesa", "Prega", "guardie_fermano_pct"):
                            text += "Le guardie ti fermano, non sei degno"
                        else:
                            text += "Le guardie ti bloccano a terra, ti colpiscono ripetutamente e infine ti cacciano!"
                            player[username]["dungeon"]["danno"] += dungeon_val("Chiesa", "Prega", "danno_cacciata", 123)
                if (scelta == "Fuggi!"
                    and "Pilastri"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Pilastri"
                    text += "Ottima idea, non ti dò torto.\nSono altamente sospetti quei sette cosi, come fai ad avvicinarti?!"

                if (scelta == "Gira per la locanda"
                    and "Bar" in player[username]["dungeon"]["mostri"]):
                    stanza = "Bar"
                    if dungeon_under(num, "Bar", "Gira per la locanda", "acqua_soglia_pct"):
                        text += f"Girando per la locanda finisci nel magazzino, dove riesci ad intascarti 5 bottiglie di acqua fresca!"
                        try:
                                        player[username]["zaino"]["Dell'acqua fresca"] += dungeon_val("Bar", "Gira per la locanda", "acqua", 5)
                        except:
                                        player[username]["zaino"]["Dell'acqua fresca"] = dungeon_val("Bar", "Gira per la locanda", "acqua", 5)
                    elif dungeon_under(num, "Bar", "Gira per la locanda", "latte_soglia_pct"):
        
                        text += f"Girando per la locanda finisci nel magazzino, guaarda quanto latte!\nMica si offenderà per 2 mancanti!"
                        try:
                                        player[username]["zaino"]["Del latte in sacchetto"] += dungeon_val("Bar", "Gira per la locanda", "latte", 2)
                        except:
                                        player[username]["zaino"]["Del latte in sacchetto"] = dungeon_val("Bar", "Gira per la locanda", "latte", 2)

                    elif dungeon_under(num, "Bar", "Gira per la locanda", "loop_soglia_pct"):
                        text += "\nGirando per la taverna incontri un portale loop temporale,Girando per la taverna incontri un portale loop temporaleGirando per la taverna incontri un portale loop temporaleGirando per la taverna incontri un portale loop temporaleGirando per la taverna incontri un portale loop temporaleGirando per la taverna incontri un portale loop temporaleGirando per la taverna incontri un portale loop temporaleGirando per la taverna incontri un portale loop temporaleGirando per la taverna incontri un portale loop temporaleGirando per la taverna incontri un portale loop temporale"
                        for x in range(dungeon_val("Bar", "Gira per la locanda", "stanze_loop", 2)):
                            player[username]["dungeon"]["mostri"].append("Bar")
                    else:
                        text += "\nGirando per la locanda sbatti a caso contro uno, tutta la sua crew ti segue e si aggiunge alle prossime stanze!"
                        for x in range(dungeon_val("Bar", "Gira per la locanda", "nemici_crew", 3)):
                            player[username]["dungeon"]["mostri"].append(random.choice(list(nemici)))
                        if dungeon_under(num, "Bar", "Gira per la locanda", "boss_soglia_pct"):
                            text += "\nE come non bastasse si aggiunge anche un boss!"
                            player[username]["dungeon"]["mostri"].append("Boss")
                if (scelta == "Passa"
                    and "Bar" in player[username]["dungeon"]["mostri"]):
                    stanza = "Bar"
                    text += "No grazie sto apposto, ho la mia borraccia d'acqua fresca inutilissima"

                if (scelta == "Bevi"
                    and "Bar" in player[username]["dungeon"]["mostri"]):
                    stanza = "Bar"
                    text += "Bevi la bevanda offerta!\n\n"
                    if dungeon_under(num, "Bar", "Bevi", "salta_stanza_soglia_pct"):
                        text += "Sta bevanda ti da una botta di vita assurda, corri velocissimo e ignori almeno 1 stanza!"
                        sce = take_but_not(player[username]["dungeon"]["mostri"],"Bar")
                        try:
                                        player[username]["dungeon"]["mostri"].remove(sce)
                        except:
                            text += "\nLe stanze erano però troppe poche, quindi sei semplicemente corso a vuoto!\n"
                    elif dungeon_under(num, "Bar", "Bevi", "randomizza_danno_soglia_pct"):
                        text += "Non è che voglio dire ma forse era una pozione casualina, i tuoi danni cambiano totalmente a caso!"
                        player[username]["dungeon"]["danno"] = random.randint(dungeon_val("Bar", "Bevi", "danno_random_min", -501), dungeon_val("Bar", "Bevi", "danno_random_max", 1500))

                    else:
                        text += "Forse non era il top, ecco..."
                        inabilitati[username] = time.time()

                if (scelta == "Subito"
                    and "Piedistallo"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Piedistallo"
                    text += "Provi a prendere al volo l'oggetto misterioso, ma un masso parte a caso ed inizia ad inseguirti!\n\n"
                    if dungeon_under(num, "Piedistallo", "Subito", "successo_pct"):
                        premio = random.choice(usabilitutti)
                        text += (
                f"Riesci a fuggire, te con 2x **{premio}**!"
                        )
                        try:
                            player[username]["zaino"][premio] += dungeon_val("Piedistallo", "Subito", "quantita_premio", 2)
                        except:
                            player[username]["zaino"][premio] = dungeon_val("Piedistallo", "Subito", "quantita_premio", 2)
                    else:
                        text += "Sei schiacciato dal masso..."
                        inabilitati[username] = time.time()

                if (scelta == "Ne prendo una"
                    and "Cucina"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Cucina"
                    text += "Provi ad intascarti qualche spezia senza che nessuno ti noti\n\n"
                    if dungeon_under(num, "Cucina", "Ne prendo una", "successo_pct"):
                        text += "Ce l'hai fatta!"
                        try:
                            player[username]["zaino"]["La spezia"] += dungeon_val("Cucina", "Ne prendo una", "spezie", 1)
                        except:
                            player[username]["zaino"]["La spezia"] = dungeon_val("Cucina", "Ne prendo una", "spezie", 1)
                    else:
                        text += "Mentre correvi con le spezie una porta si apre al volo, cadi a terra stordito.\nAl tuo risveglio sei senza spezie..."
                        if dungeon_under(num, "Cucina", "Ne prendo una", "incapacita_pct"):
                            inabilitati[username] = time.time()

                if (scelta == "Ne prendo 5"
                    and "Cucina"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Cucina"
                    text += "Provi ad intascarti qualche spezia senza che nessuno ti noti\n\n"
                    if dungeon_under(num, "Cucina", "Ne prendo 5", "successo_pct"):
                        text += "Ce l'hai fatta!"
                        try:
                            player[username]["zaino"]["La spezia"] += dungeon_val("Cucina", "Ne prendo 5", "spezie", 1)
                        except:
                            player[username]["zaino"]["La spezia"] = dungeon_val("Cucina", "Ne prendo 5", "spezie", 1)
                    else:
                        text += "Mentre correvi con le spezie una porta si apre al volo, cadi a terra stordito.\nAl tuo risveglio sei senza spezie..."
                        if dungeon_under(num, "Cucina", "Ne prendo 5", "incapacita_pct"):
                            inabilitati[username] = time.time()

                if (scelta == "Ne prendo 10"
                    and "Cucina"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Cucina"
                    text += "Provi ad intascarti qualche spezia senza che nessuno ti noti\n\n"
                    if dungeon_under(num, "Cucina", "Ne prendo 10", "successo_pct"):
                        text += "Ce l'hai fatta!"
                        try:
                            player[username]["zaino"]["La spezia"] += dungeon_val("Cucina", "Ne prendo 10", "spezie", 1)
                        except:
                            player[username]["zaino"]["La spezia"] = dungeon_val("Cucina", "Ne prendo 10", "spezie", 1)
                        if "Fuga col sacco" not in player[username]["obbiettivi"]:
                            player[username]["obbiettivi"].append("Fuga col sacco")
                            try:
                                await app.send_message(
                                        username, "Obbiettivo completato!\n**Fuga col sacco**, scappa con 10+ spezie!"
                                    )
                            except:
                                pass
                    else:
                        text += "Mentre correvi con le spezie una porta si apre al volo, cadi a terra stordito.\nAl tuo risveglio sei senza spezie..."
                        if dungeon_under(num, "Cucina", "Ne prendo 10", "incapacita_pct"):
                            inabilitati[username] = time.time()


                if (scelta == "Prendo il tavolo intero"
                    and "Cucina"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Cucina"
                    text += "Provi ad intascarti qualche spezia senza che nessuno ti noti\n\n"
                    if dungeon_under(num, "Cucina", "Prendo il tavolo intero", "successo_pct"):
                        text += "Ce l'hai fatta!"
                        try:
                            player[username]["zaino"]["La spezia"] += dungeon_val("Cucina", "Prendo il tavolo intero", "spezie", 1)
                        except:
                            player[username]["zaino"]["La spezia"] = dungeon_val("Cucina", "Prendo il tavolo intero", "spezie", 1)
                        if "Fuga col sacco" not in player[username]["obbiettivi"]:
                            player[username]["obbiettivi"].append("Fuga col sacco")
                            try:
                                await app.send_message(
                                        username, "Obbiettivo completato!\n**Fuga col sacco**, scappa con 10+ spezie!"
                                    )
                            except:
                                pass
                    else:
                        text += "Mentre correvi con le spezie una porta si apre al volo, cadi a terra stordito con anche il tavolo.\nAl tuo risveglio sei senza spezie..."
                        inabilitati[username] = time.time()

                if (scelta == "Peschiamo!"
                    and "Stagno"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Stagno"
                    forza = player[username]["scheda"]["atk"]
                    peso = random.randint(0, forza)
                    if dungeon_test(num, peso, "Stagno", "Peschiamo!"):
                        gloria = round(peso * dungeon_val("Stagno", "Peschiamo!", "gloria_per_kg", 0.4))
                        text += f"\nPeschi un pesce drago di {peso}kg!\nUn signore si stupisce e in cambio del tuo malloppo ti fornisce **{gloria} gloria!**"
                        try:
                            player[username]["gloria"] += gloria
                        except:
                            player[username]["gloria"] = gloria
                    else:
                        if dungeon_under(num, "Stagno", "Peschiamo!", "morte_soglia_pct"):
                            text += "Peschi per diverso tempo fin quando un pesce decide di pescare te!\nTi mangia in un sol boccone!"
                            inabilitati[username] = time.time()
                        else:
                            text += "Peschi per diverso tempo ma aimè non trovi nulla"

                if (scelta == "Non è il caso"
                    and "Stagno"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Stagno"
                    text += "Sarà per un altra volta!"

                if (scelta == "Entraci"
                    and "Locanda spettrale"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Locanda spettrale"
                    text += "Entri nella locanda che stranamente compare dal nulla.\nCerto il personale fantasma non è proprio lo spirito delle festa, però sono gentili ed accoglienti.\nTi offrono la camera 709:\n"
                    if dungeon_under(num, "Locanda spettrale", "Entraci", "evento_negativo_pct"):
                        if dungeon_under(num, "Locanda spettrale", "Entraci", "fantasmi_soglia_pct"):
                            text += "\nTi svegli nel pieno della notte, tutti i fantasmi sono pronti a farti fuori!\n\nTe la cavi, ma non molto..."
                            player[username]["dungeon"]["danno"] = (
                    player[username]["dungeon"]["danno"] * dungeon_val("Locanda spettrale", "Entraci", "moltiplicatore_danno_fantasmi", 2)
                )
                        else:
                            text += "\nNel mezzo della notte la locanda scompare e cadi dal 5 piano!"
                            player[username]["dungeon"]["danno"] += dungeon_val("Locanda spettrale", "Entraci", "danno_caduta", 100)
                    else:
                        text += "\nCavolo che stanza chic!\nColazione continentale la mattina dopo e taac 5 stelle su gostadvisor"
                        player[username]["dungeon"]["danno"] -= dungeon_val("Locanda spettrale", "Entraci", "cura_riposo", 300)

                if (scelta == "Ti ci avvicini"
                    and "Pilastri"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Pilastri"
                    text += "Ti avvicini ai pilastri, speranzoso di un miracolo\n"
                    if dungeon_under(num, "Pilastri", "Ti ci avvicini", "fulmine_pct"):
                        text += "Vieni decisamente fulminato, subisci **tanto ma tanto dolore**"
                        player[username]["dungeon"]["danno"] = dungeon_val("Pilastri", "Ti ci avvicini", "danno_fulmine", 999)

                    else:
                        text += "I 7 pilastri premiano il tuo coraggio, che sia tu libero di uscire da questo posto!"
                        player[username]["dungeon"]["danno"] = dungeon_val("Pilastri", "Ti ci avvicini", "danno_premio", -300)

                if (scelta == "Ignorala"
                    and "Locanda spettrale"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Locanda spettrale"
                    text += "Sarà una trappola, palesemente"

                if (scelta == "Svegliati"
                    and "Locanda spettrale"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Locanda spettrale"
                    text += (
                        "Ti alzi da terra terrorizzato, cos'è reale?!"
                    )
                    if dungeon_under(num, "Locanda spettrale", "Svegliati", "scaglione_soglia_pct"):
                        if dungeon_under(num, "Locanda spettrale", "Svegliati", "conferma_soglia_pct"):
                            text += "\nOttieni uno scaglione celeste...\nUsalo con cura."
                            player[username]["zaino"][        "Uno scaglione blu"
                    ] = 1

                if (scelta == "Fuggi"
                    and "Parco" in player[username]["dungeon"]["mostri"]):
                    stanza = "Parco"
                    forza = player[username]["scheda"]["agi"]
                    if dungeon_test(num, forza, "Parco", "Fuggi"):
                        contentino = random.choice(tutto)
                        if dungeon_under(num, "Parco", "Fuggi", "lv1_soglia_pct"):
                            contentino = contentino.replace("LV0", "LV1"
                )

                        elif dungeon_under(num, "Parco", "Fuggi", "lv2_soglia_pct"):
                            contentino = contentino.replace("LV0", "LV2"
                )

                        else:
                            pass

                        try:
                            player[username]["zaino"][contentino] += 1
                        except:
                            player[username]["zaino"][contentino] = 1

                        text += f"Riesci a fuggire, nella fuga trovi **{contentino}**!\nChe fortuna!"
                    else:
                        text += "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                        if dungeon_under(num, "Parco", "Fuggi", "incapacita_soglia_pct"):
                            player[username].pop("dungeon")
                            inabilitati[username] = time.time()

                if (scelta == "Fermali"
                    and "Parco" in player[username]["dungeon"]["mostri"]):
                    stanza = "Parco"
                    forza = player[username]["scheda"]["def"]
                    text += "Ti giri di scatto, punti il più grande di loro e ci corri contro.\n"
                    if dungeon_test(num, forza, "Parco", "Fermali"):
                        contentino = random.choice(tutto)
                        if dungeon_under(num, "Parco", "Fermali", "lv1_soglia_pct"):
                            contentino = contentino.replace("LV0", "LV1")

                        elif dungeon_under(num, "Parco", "Fermali", "lv2_soglia_pct"):
                            contentino = contentino.replace("LV0", "LV2")

                        else:
                            pass

                        try:
                            player[username]["zaino"][contentino] += 1
                        except:
                            player[username]["zaino"][contentino] = 1

                        text += f"Lo blocchi ed il branco intero per paura fugge!\nMentre ti incammini verso la porta trovi **{contentino}**"
                    else:
                        player[username].pop("dungeon")
                        inabilitati[username] = time.time()
                        text += "Pessima idea, pessima idea, pessimaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                
                if (scelta == "Parlaci" and "Parco" in player[username]["dungeon"]["mostri"]):
                    stanza = "Parco"
                    text += "Che idea del cazzo."
                    player[username].pop("dungeon")

                    if dungeon_under(num, "Parco", "Parlaci", "incapacita_pct"):
                        inabilitati[username] = time.time()
                        await app.send_sticker(username,"CAACAgEAAxkBAAE2gwhg-Fa3ceNqyZc0HXkqxpXMZu2xtwACTQEAAj8RFRHiILNZLpFUfB4E",)
                        
                        if dungeon_under(num, "Parco", "Parlaci", "scaglione_soglia_pct"):
                            text += "\nOttieni uno scaglione della speranza...\nUsalo con cura."
                            player[username]["zaino"][                "Uno scaglione verde"
                            ] = 1

                if (scelta == "Disco ricurvo"
                    and "Arena" in player[username]["dungeon"]["mostri"]):
                    stanza = "Arena"
                    text += (
                        "Lanci il disco con tutta la forza che hai.\n"
                    )
                    forza = player[username]["scheda"]["atk"]
                    if dungeon_test(num, forza, "Arena", "Disco ricurvo"):
                        text += "il tuo disco colpisce qualche volta l'avversario, fino a farlo finire a terra...\nHAI VINTO!"
                        contentino = random.choice(tutto)

                        try:
                            player[username]["zaino"][contentino] += 1
                        except:
                            player[username]["zaino"][contentino] = 1
                        text += f"\nOttieni **{contentino}**"
                    else:
                        text += "il tuo disco perisce sotto l'avversario, fino a farti finire a terra...\nHAI PERSO!"

                if (scelta == "Disco acuminato"
                    and "Arena" in player[username]["dungeon"]["mostri"]):
                    stanza = "Arena"
                    text += (
                        "Lanci il disco con tutta la forza che hai.\n"
                    )
                    forza = player[username]["scheda"]["agi"]
                    if dungeon_test(num, forza, "Arena", "Disco acuminato"):
                        text += "il tuo disco colpisce qualche volta l'avversario, fino a farlo finire a terra...\nHAI VINTO!"
                        contentino = random.choice(tutto)

                        try:
                            player[username]["zaino"][contentino] += 1
                        except:
                            player[username]["zaino"][contentino] = 1
                        text += f"\nOttieni **{contentino}**"
                    else:
                        text += "il tuo disco perisce sotto l'avversario, fino a farti finire a terra...\nHAI PERSO!"

                if (scelta == "Disco bilanciato"
                    and "Arena" in player[username]["dungeon"]["mostri"]):
                    stanza = "Arena"
                    text += (
                        "Lanci il disco con tutta la forza che hai.\n"
                    )
                    forza = player[username]["scheda"]["def"]
                    if dungeon_test(num, forza, "Arena", "Disco bilanciato"):
                        text += "il tuo disco colpisce qualche volta l'avversario, fino a farlo finire a terra...\nHAI VINTO!"
                        contentino = random.choice(tutto)

                        try:
                            player[username]["zaino"][contentino] += 1
                        except:
                            player[username]["zaino"][contentino] = 1
                        text += f"\nOttieni **{contentino}**"
                    else:
                        text += "il tuo disco perisce sotto l'avversario, fino a farti finire a terra...\nHAI PERSO!"

                if (scelta == "Un mattone ancestrale"
                    and "Tempio azteco"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Tempio azteco"
                    text += "DELICATAMENTE provi a sostituire l'idoletto...\n"
                    forza = len(player[username]["bestiario"])
                    if dungeon_test(num, forza, "Tempio azteco", "Un mattone ancestrale"):
                        text += "Ci riesci, ti porti a casa le tue chiappette intere e l'idoletto.\nHAI VINTO!"
                        contentino = "Un idoletto"

                        try:
                            player[username]["zaino"][contentino] += 1
                        except:
                            player[username]["zaino"][contentino] = 1
                        text += f"\nOttieni **{contentino}**"
                    else:
                        text += "Ti impegni al massimo ma non riesci a controbilanciare il peso...\nPrima che sia troppo tardi lasci stare.\nHAI PERSO!"

                if (scelta == "Una piuma azteca"
                    and "Tempio azteco"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Tempio azteco"
                    text += "DELICATAMENTE provi a sostituire l'idoletto...\n"
                    forza = player[username]["livello"]
                    if dungeon_test(num, forza, "Tempio azteco", "Una piuma azteca"):
                        text += "Ci riesci, ti porti a casa le tue chiappette intere e l'idoletto.\nHAI VINTO!"
                        contentino = "Un idoletto"

                        try:
                            player[username]["zaino"][contentino] += 1
                        except:
                            player[username]["zaino"][contentino] = 1
                        text += f"\nOttieni **{contentino}**"
                    else:
                        text += "Ti impegni al massimo ma non riesci a controbilanciare il peso...\nPrima che sia troppo tardi lasci stare.\nHAI PERSO!"

                if (scelta == "Un cappello da esploratore"
                    and "Tempio azteco"
                    in player[username]["dungeon"]["mostri"]):
                    stanza = "Tempio azteco"
                    text += "DELICATAMENTE provi a sostituire l'idoletto...\n"
                    forza = player[username]["grado"]
                    if dungeon_test(num, forza, "Tempio azteco", "Un cappello da esploratore"):
                        text += "Ci riesci, ti porti a casa le tue chiappette intere e l'idoletto.\nHAI VINTO!"
                        contentino = "Un idoletto"

                        try:
                            player[username]["zaino"][contentino] += 1
                        except:
                            player[username]["zaino"][contentino] = 1
                        text += f"\nOttieni **{contentino}**"
                    else:
                        text += "Ti impegni al massimo ma non riesci a controbilanciare il peso...\nPrima che sia troppo tardi lasci stare.\nHAI PERSO!"
                try:
                    player[username]["dungeon"]["mostri"].remove(stanza)
                    manca = len(player[username]["dungeon"]["mostri"])
                    player[username]["dungeon"]["danno"] -= dungeon_global("generale", "cura_fine_scelta", 20)
                    danno = player[username]["dungeon"]["danno"]
                    text += f"\nMancano {manca} stanze!\n(Danno subito {danno})\n"
                except:
                    manca = 10000
                try:
                                player[username]["grado"] += dungeon_global("generale", "grado_fine_scelta", 1)
                except:
                                player[username]["grado"] = dungeon_global("generale", "grado_fine_scelta", 1)

                if manca == 0:
                    player[username]["dungeon"] = genera_dungeon(player,username)
                    text += "Hai finito questo piano, ti avventuri al successivo..."
                    await app.send_sticker(username,"CAACAgIAAxkBAAEcXvdhe-0VQLjGDUwqfcUGnMeDvh57pgACUFYAAp7OCwAB99_coLvdsZ4eBA")
                await app.edit_message_text(
                    chat_id=message.message.chat.id,
                    message_id=message.message.message_id,
                    text=text,)
            else:
                fines = False
                text = f"Esplorando il dungeon raggiungi {scelta}!\n"
                if scelta == "Stanza del sonno":
                    text += "Una strana nebbia si alza e l'intera stanza si riempe..."
                    bottoni = list()
                    for appz in ["Corri via", "Immergitici"]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )
                try:
                                await message.message.delete()
                except:
                                pass
                if scelta == "Crepaccio":
                    text += "Davanti a te si presenta un enorme crepa sul muro, decidi di avvicinarti per vedere cosa sta succedendo quando l'intero piano si muove...\n"
                    text += "Cosa vuoi fare?"
                    bottoni = list()
                    for appz in ["Tocchi la crepa", "Ti allontani"]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )

                if scelta == "Stanza":
                    text += "Entri in una stanza bianca, totalmente bianca!\nIlluminati da una luce divina nel suo mezzo si pongono 3 bottoni, su, giù e fuga rapida.\nQuale premiamo?\n"
                    text += "Cosa vuoi fare?"
                    bottoni = list()
                    for appz in ["Sali","Scendi","Non cliccare"]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )

                if scelta == "Chiesa":
                    text += "Entri nella sacra chiesa di msx80, custodi dell'antico sapere di altri bot...\nLa sacra vetrata di cristalli e pel top illumina la via al loro altare, cosa vuoi fare?"
                    bottoni = list()
                    for appz in ["Prega", "Ritirati"]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )
                if scelta == "Distributore":
                    text += "Assurdo, un distributore di caramelle!\n1 gloria per 1 caramella?"
                    bottoni = list()
                    for appz in ["Metti monetina", "Anche no"]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )
                if scelta == "Bisca":
                    text += "150 gloria, 2 carte, se la tua è più alta della mia guadagni 150 pulissima gloria, altrimenti è tutta mia.\nChe si fà signò?"
                    bottoni = list()
                    for appz in ["Scommetti", "N'altra volta"]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )

                if scelta == "Pilastri":
                    text += (
                        "7 cupi pilastri neri fluttuano nella stanza.\n"
                    )
                    text += "Cosa vuoi fare?"
                    bottoni = list()
                    for appz in ["Ti ci avvicini", "Fuggi!"]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )

                if scelta == "Bar":
                    text += "Benvenuto nella locanda di Bob, un posto mistico interdimensionale che ignora le regole dei mondi di gioco!\nIl baldo barista ti offfre una bibita, accetti?"

                    bottoni = list()
                    for appz in ["Bevi","Passa","Gira per la locanda",]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )

                if scelta == "Fattoria":
                    text += "Ad un certo punto ti ritrovi dentro la fattoria Muccallina.\nCi sono diverse mucche ma nessun fattore.\n"
                    text += "Cosa dovresti fare?"
                    bottoni = list()
                    for appz in ["Nutri le mucche", "Mungi le mucche"]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )

                if scelta == "Cancello":

                    text += "Davanti a te si presenta un massiccio cancello incantato\n"
                    if globali["Cancello"] == True:
                        text += "Esso è aperto e ti permette di accedere ai tesori dietro di esso\n"
                        vertutto = (tuttov + megaman + zombie + gungeon + magic)
                        contentino = random.choice(vertutto).replace("0", "2")
                        text += f"Prendi **{contentino}** e corri via prima che il cancello si richiuda!\n"
                        try:
                            player[username]["zaino"][contentino] += 1
                        except:
                            player[username]["zaino"][contentino] = 1
                        globali["Cancello"] = False
                    else:
                        text += "Il cancello è chiuso, ti allontani deluso...\nSi sentono orribili rumori di sottofondo"

                        globali["Cancello"] = True
                    fines = True

                if scelta == "Fonte magica":
                    text += "Entri nella fonte per cercare di recuperare qualche hp...\n"
                    if dungeon_under(num, "Fonte magica", "evento", "cura_pct"):
                        text += "Ti senti meglio!"
                        player[username]["dungeon"]["danno"] -= dungeon_val("Fonte magica", "evento", "cura", 200)
                    else:
                        text += "Nulla"
                    fines = True

                if scelta == "Lupo solitario":
                    text += "...\n"
                    if dungeon_under(num, "Lupo solitario", "evento", "nessun_lupo_soglia_pct"):
                        text += "Qui non c'è nessun lupo!"
                        player[username]["dungeon"]["danno"] -= dungeon_val("Lupo solitario", "evento", "cura", 50)
                    elif dungeon_under(num, "Lupo solitario", "evento", "attacco_lupo_soglia_pct"):
                        text += "Il lupo ti attacca!"
                        player[username]["dungeon"]["danno"] += dungeon_val("Lupo solitario", "evento", "danno", 70)
                    else:
                        text += "Nulla"
                    fines = True

                if scelta == "Segreta abbandonata":
                    text += "Trovi una cella abbandonata, un cadavere giace sul pavimento...\n"
                    if dungeon_under(num, "Segreta abbandonata", "evento", "loot_pct"):
                        coso = random.choice(dungeon_val("Segreta abbandonata", "evento", "loot", ["Un fune di fuga", "Uno stimpak", "Candela blu", "Ultimo barlore"]))
                        text += f"Nella sua tasca c'è **{coso}**!"
                        try:
                            player[username]["zaino"][coso] += 1
                        except:
                            player[username]["zaino"][coso] = 1
                    else:
                        text += "Te ne vai schifato"
                    fines = True

                if scelta == "Fabbro":
                    text += "Un fabbro sta lavorando in mezzo a zampilli di lava e fiamme.\n"
                    bottoni = list()
                    for appz in ["Avvicinati","Allontanati","Approcciala",]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )

                if scelta == "Arena":
                    oppo = random.choice(list(player))
                    text += f"EEEEED ECCO A VOI L'ENTRATA IN SCENA DI {username} A CUI TOCCA AFFRONTARE {oppo} NELL'ARENA CIRCOLARE!\nPreso dal panico noti 3 dischetti, quale scegli di lanciare?"
                    bottoni = list()
                    for appz in ["Disco acuminato","Disco ricurvo","Disco bilanciato",]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )

                if scelta == "Stagno":
                    text += "Entri in uno strano parco, un enorme lago si presenta davanti a te.\nVuoi provare a pescare?"
                    bottoni = list()
                    for appz in ["Peschiamo!", "Non è il caso"]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )

                if scelta == "Piedistallo":
                    text += "Un piedistallo in centro alla stanza contiene un usabile casuale in duplice copia.\nTe la rischi?"
                    bottoni = list()
                    for appz in ["Subito", "Nah"]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )

                if scelta == "Cucina":
                    text += "Arrivi in un immensa cucina gigante, attirato dall'odore.\nSul tavolo di fonte a te un casino di spezie giaciono senza guardia,cosa fai?"
                    bottoni = list()
                    for appz in ["Ne prendo una","Ne prendo 5","Ne prendo 10","Prendo il tavolo intero",]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )

                if scelta == "Tempio azteco":
                    text += "Compare d'innanzi a te un vecchio tempio.\nUn idoletto è al centro della stanza, sembra che sia sopra ad un meccanismo a scatto.\nDevi controbilanciare il suo peso per evitare la trappola, cosa scegli?"

                    bottoni = list()
                    for appz in ["Un mattone ancestrale","Una piuma azteca","Un cappello da esploratore",]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )

                if scelta == "Luci ed ombre":
                    approccio = player[username]["scheda"]["Ap"]
                    mas = 0
                    while True:
                        preso = random.choice(list(player[username]["zaino"]))
                        if ("Anello" in preso or "5" in preso or "4" in preso or "2" in preso or "3" in preso or "1" in preso or mas == 5):

                            break
                        mas += 1

                    text += f"Il tuo fato è stato da te scelto giovane {username}, non c'è nulla che può bloccare questa sentenza!\n\n"

                    if approccio in dungeon_val("Luci ed ombre", "evento", "approcci_oscuri", []) and dungeon_over(num, "Luci ed ombre", "evento", "punizione_pct"):
                        player[username]["zaino"][preso] -= 1
                        if player[username]["zaino"][preso] <= 0:
                            player[username]["zaino"].pop(preso)
                        text += f"L'oscurità ti sommerge...\nTi viene tolto **{preso}** come punizione!\n"
                    else:
                        text += f"La luce ti abbraccia...\nTi viene aggiunto **{preso}** come ricompensa!\n"
                        player[username]["zaino"][preso] += 1
                    fines = True

                if scelta == "Parco":
                    text += "Un parco verde si apre davanti a te colmo di animali.\nCamminando a caso cercando l'uscita noti un branco di OrsoDruidi seguirti, che fai?"
                    bottoni = list()
                    for appz in ["Fuggi", "Fermali", "Parlaci"]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )

                if scelta == "Locanda spettrale":
                    text += "Un insolita locanda compare dal mezzo della nebbia.\n"
                    bottoni = list()
                    for appz in ["Entraci", "Ignorala", "Svegliati"]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )

                if scelta == "Boss":
                    text += "Un portone enorme si presenta davanti a te, dietro ci sarà sicuramente qualcosa di molto brutto...\nIn questi casi poi usare /aiuta in un gruppo per richiedere un supporto!\nNon perdere l'occasione!\nQuando sei pronto apri pure la porta!"
                    bottoni = list()
                    if "Boss" in player[username]["dungeon"]:
                        nemicio = player[username]["dungeon"]["Boss"]
                    else:
                        nemicio = random.choice(list(nemici))
                        player[username]["dungeon"]["Boss"] = nemicio

                    for appz in [f"Affronta {nemicio}"]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )

                if scelta == "Armeria":
                    text += "Entri in un antica armeria, il tutto è un poco polveroso ma qualcosa si potrà pur trovare!\n"
                    try:
                                    seet = player[username]["scheda"]["set"]
                    except:
                                    seet = None         
                    if seet == None or dungeon_under(num, "Armeria", "evento", "nessun_evento_pct"):
                        text += "Il tuo set non richiama nessun evento, vabbè succede"
                    elif "Forma" in seet or ("Pescatore" == seet and not proc_val("Pescatore", "dungeon", "armeria", "compatibile")):
                        text += "Il tuo set è troppo recente, non può interagire con questi rottami..."
                    else:
                        cosa = random.choice(classi[seet]) + " LV0"
                        text += f"Davanti a te un manichino porta il tuo set, il {seet}!\nRiesci a prendere però solo **{cosa}**"
                        try:
                            player[username]["zaino"][cosa] += 1
                        except:
                            player[username]["zaino"][cosa] = 1
                    fines = True
                if scelta == "Spada conficcata":
                    text += "Non credo si possa fare qualcosa per estrarla, la spada del folle titano è troppo pesante e maledetta..."
                    today = date.today()
                    d1 = today.strftime("%d")
                    if int(d1) == 17 or int(d1) == 21:
                        bottoni = list()
                        for appz in [f"Estrai la spada","Non ora"]:
                            bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])

                        reply_markup = InlineKeyboardMarkup(bottoni)

                        await app.send_message(
                chat_id=username,
                text=text,
                reply_markup=reply_markup,
                        )

                    else:

                        fines = True

                if scelta == "MetaMusicoteca":
                    text += "Sarò sincero ragazzo, non mi piaci, nessuno mi piace e nessuno mi piacera.\nTi aspettavi una stanza chissà come, con della musica, magari sei pure entrato da mariaci o musico sciamano ma la verità è solo questa:\nQuesta è una meta stanza che ti sta dicendo che forse stai giocando troppo e dovresti che ne so, bagnare i fiori o fare i letti?\nVabè qui è tipo così;\nHai l'1% di ottenere una copia di crack musica della DPG versione platinum oro, in modo da ottenere un intelligenza, o niente.\nNon aspettarti altro perde molto sta stanza dopo la prima volta, ma ormai vuoi crack musica quindi rifarai sta stanza ancora ed ancora fino ad ottenerlo.\n"

                    if dungeon_under(num, "MetaMusicoteca", "evento", "crack_musica_pct"):


                        try:
                            player[username]["zaino"]["crack musica"] += 1
                        except:
                            player[username]["zaino"]["crack musica"] = 1

                    else:
                        pass
                    fines = True

                if scelta == "Biblioteca":
                    text += "Entri nella vecchia biblioteca regale, il tutto è un poco polveroso ma qualcosa si potrà pur trovare!\n"


                    if dungeon_under(num, "Biblioteca", "evento", "vuota_pct"):
                        text += "O forse no..."
                    else:
                        cosa = random.choice(list(libri)) 
                        text += f"\nGirovagando senti un fondo vicino a te, è dal cielo caduto un **{cosa}** intatto!\n"
                        gestione_zaino(player[username]["zaino"],"add",cosa,1)
                    fines = True

                if scelta == "Cunicolo":
                    text += (
                        "Strisci in mezzo ad uno stretto cunicolo..."
                    )
                    if dungeon_under(num, "Cunicolo", "evento", "scaglione_soglia_pct"):
                        if dungeon_under(num, "Cunicolo", "evento", "conferma_scaglione_soglia_pct"):
                            text += "\nOttieni uno scaglione glorioso...\nUsalo con cura."
                            player[username]["zaino"]["Uno scaglione giallo"
                    ] = 1
                    if dungeon_under(num, "Cunicolo", "evento", "crollo_pct"):
                        text += "\nIl cunicolo si stringe tantissimo e no aspetta non è il cunicolo che si stringe ma il soffitto che sta cedendo..."
                        player[username]["dungeon"]["piano"] += dungeon_val("Cunicolo", "evento", "piani_crollo", -1)

                    fines = True

                if scelta == "Sabbie mobili":
                    try:
                                    pat = player[username]["varie"]["pat"]
                    except:
                                    pat = 0
                    if dungeon_under(num, "Sabbie mobili", "evento", "caduta_pct"):
                        if pat > dungeon_val("Sabbie mobili", "evento", "pat_min", 666) and dungeon_under(num, "Sabbie mobili", "evento", "salvataggio_pet_soglia_pct"):
                            text += "Stavi per cadere nelle sabbie mobili ma il tuo animaletto ti blocca prima!\n"
                            if dungeon_under(num, "Sabbie mobili", "evento", "scaglione_soglia_pct"):
                                text += "\nOttieni uno scaglione oscuro...\nUsalo con cura."
                                player[username]["zaino"]["Uno scaglione nero"] = 1
                        else:
                            mas = 0
                            while True:
                                preso = random.choice(
                                    list(player[username]["zaino"])
                                )
                                if (
                                    "Anello" in preso
                                    or "1" in preso
                                    or "2" in preso
                                    or "3" in preso
                                    or "0" in preso
                                    or mas == 5
                                ) and preso not in decoro:
                                    break
                                mas += 1

                            player[username]["zaino"][preso] -= 1
                            if player[username]["zaino"][preso] <= 0:
                                player[username]["zaino"].pop(preso)
                            text += f"Salti oltre le sabbie mobili, nello slancio ti cade però **{preso}**.\nIrrecuperabile..."
                    else:
                        text += "Salti oltre le sabbie mobili..."
                    fines = True

                if fines == True:
                    player[username]["dungeon"]["mostri"].remove(scelta)
                    manca = len(player[username]["dungeon"]["mostri"])
                    danno = player[username]["dungeon"]["danno"]
                    text += f"\nMancano {manca} stanze!\n(Danno subito {danno})\n"
                    try:
                                    player[username]["grado"] += dungeon_global("generale", "grado_fine_scelta", 1)
                    except:
                                    player[username]["grado"] = dungeon_global("generale", "grado_fine_scelta", 1)

                    if manca == 0:
                        player[username]["dungeon"] = genera_dungeon(player,username)
                        text += "Hai finito questo piano, ti avventuri al successivo..."
                        await app.send_sticker(username,"CAACAgIAAxkBAAEcXvdhe-0VQLjGDUwqfcUGnMeDvh57pgACUFYAAp7OCwAB99_coLvdsZ4eBA")
                    messaggini = separatore(text)
                    for mess in messaggini:
                        try:
                            await app.send_message(username, mess)
                        except:
                            pass
                #here
                pass
            

        else:
            await message.answer(f"Mancano {manca} secondi!")
    _duplica_premi_dungeon_da_snapshot(player[username], _snapshot_premi_weekend, evento)

# --- SET EROI DELLA TEMPESTA: RUNTIME ---

# --- TURNO E ASSALTO CARICATI DA MODULO DEDICATO ---
# Esecuzione nello stesso namespace: evita import circolari e mantiene invariati
# lookup globali, alias delle ondate e comportamento delle funzioni storiche.
from pathlib import Path as _TurnoAssaltoPath
_turno_assalto_file = _TurnoAssaltoPath(__file__).with_name("turno_assalto.py")
with _turno_assalto_file.open("r", encoding="utf-8") as _turno_assalto_stream:
    exec(
        compile(_turno_assalto_stream.read(), str(_turno_assalto_file), "exec"),
        globals(),
        globals(),
    )
del _turno_assalto_stream, _turno_assalto_file, _TurnoAssaltoPath

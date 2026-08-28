import random,copy,time,string
from apscheduler.schedulers.background import BackgroundScheduler
from pyrogram import Client, ContinuePropagation, filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import date
from liste import *
from bilanciamento import PROC_CLASSI, PROC_ANELLI, DUNGEON_CONFIG, INCANTESIMI_CONFIG, EFFETTI_CONFIG
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
                                    if "pet" in player[username]:
                                        giocatore["animale"] = player[username]["pet"]
                                    matx = 0
                                    for pl in clan[user["team"]]["last"]:
                                        elapsed = time.time() - clan[user["team"]]["last"][pl]
                                        if elapsed < 301 and username != pl:
                                            matx += 1
                                            
                                    serv = matx
                                    if matx < proc_val("Eroe caduto", "assalto", "supporto_clan", "compagni_soglia") and giocatore["set"] == 'Eroe caduto':
                                        serv += proc_val("Eroe caduto", "assalto", "supporto_clan", "serv_bonus_nft")
                                        
                                    if giocatore["set"] == 'Eroe della rivolta':
                                        serv = serv * proc_val("Eroe della rivolta", "assalto", "supporto_clan", "serv_mul")
                                    if player[username]["setta"]["benedizione"] == 'Orso polare' and  matx > 2:
                                        
                                        a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
                                        serv += (a/4)
                                    if player[username]["setta"]["benedizione"] == 'Kaimano' and  matx <= 2:
                                        a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
                                        serv += (a/4)
                                    
                                    bostabile = ["def", "atk", "agi"]
                                    for stat in bostabile:
    
                                        giocatore[stat] = round(giocatore[stat] + (giocatore[stat] * (serv / 12)))
                                        
                                    classe(giocatore,giocatore["set"],bonus)
                                    
                                    output = assedio(player,
                                        giocatore,
                                        nemico,
                                        target,
                                        user["team"],
                                        ordine,
                                        clan,
                                        trader["meteo"][player[username]["location"]],
                                        clan[clan[user["team"]]["inguerra"]]["setting"]
                                        
                                    )
                                    output += f"\n{matx} persone assaltano con te!"
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
        ccc = 3600
        if player[username]["setta"]["benedizione"] == "Verme delle sabbie":
            a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
            ccc *= 1 - (a/100)
        
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
                            text=f"Devi aspettare un'ora per muoverti, diciamo che circa ti manca {tempo} ore!",
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

def assedio(playerg,player, nemico, target, team, order, clan,meteo = None, setting = dict()):
    player["fatto"] = 0
    nome = player["Nome"]
    set = player.get("set",None)
    bonus = {"agi": 0, "atk": 0, "def": 0}
    anello = player["anello"]
    defense = player["def"]
    dps = player["atk"]
    agi = player["agi"]
    effetti = player["boost"]["assalto"]
    text = "Inizia il turno d'assedio!\n"
    if player["anello"] == "Anello perfezionista":
        random.seed(PROC_ANELLI["Anello perfezionista"]["generale"]["seed"])
    num = random.random()
    bacon = False
    necron = False
    if "nucleo" in clan[team]:
        nuc = clan[team]["nucleo"]
        text += f"\nIl nucleo {nuc} sprigiona la sua forza!\n\n"
        
        if nuc not in nuclei:
            print(nuc)
        elif nuc == "Nucleo elettrico instabile":
                player["agi"] += 25
        elif nuc == "Nucleo marittimo instabile":
                player["hp"] += 300
        elif nuc == "Nucleo demoniaco instabile":
                player["atk"] += 185
        elif nuc == "Nucleo terrestre instabile":
                player["def"] += 185
        elif nuc == "Nucleo selvaggio instabile":
                player["agi"] += 5
                player["hp"] += 30
                player["atk"] += 25
                player["def"] += 25
        elif clan[team]["nucleo"] == "Nucleo di bacon instabile":
                bacon = True
        elif nuc == "Nucleo Necron instabile" and 0.08 > num:
            necron = True

    if meteo in ["Arieggiato","Caldo infernale","Caldo torrido","Tempesta","Arcobaleno","Pioggia"]:
        if meteo == 'Caldo infernale':
            bonus["agi"] -= 30
            text += "Il caldo sovraccarica le difese!\n"
            if set == "Re del raaave":
                bonus["agi"] += proc_val(set, "assalto", "meteo", "caldo_infernale_agi")
        elif meteo == 'Caldo torrido':
            bonus["atk"] -= 50
            text += "Il caldo blocca le difese!\n"
            if set == "Re del raaave":
                bonus["atk"] += proc_val(set, "assalto", "meteo", "caldo_torrido_atk")
        elif meteo == 'Tempesta':
            bonus["agi"] += 30
            text += f"La tempesta blocca {nome} a terra!\n"
        elif meteo == 'Pioggia':
            bonus["atk"] += 50
            text += f"La pioggia raffredda {nome}!\n"
        elif meteo == 'Arcobaleno':
            text += f"Sia {nome} che le difese si potenziano per il meteo!"
            player["atk"] += 75
            bonus["atk"] += 75
            if set == "Re del raaave":
                player["atk"] += proc_val(set, "assalto", "meteo", "arcobaleno_atk")
        elif meteo == "Arieggiato":
            text += f"Il meteo è troppo forte, {nome} non riesce a tenere il proprio equip!\n"
            set = None
    
    if set != None:
        num = random.random()
        if set == "Inferno risvegliato":
            bonus["atk"] += proc_val(set, "assalto", "inferno", "atk_bonus")
            player["atk"] += proc_val(set, "assalto", "inferno", "atk_player")
        elif set == "Thunderlord" and proc_ok(num, set, "assalto", "tuono"):
            for g in range(proc_val(set, "assalto", "tuono", "colpi")):
                try:
                    news = random.choice(list(nemico))
                    if nemico[news]["hp"] < proc_val(set, "assalto", "tuono", "hp_min"):
                        break
                    
                    danno_tuono = proc_val(set, "assalto", "tuono", "danno")
                    nemico[news]["hp"] -= danno_tuono
                    
                    text += f"\n**{nome} evoca un tuono e infligge {danno_tuono} danni a {news}!**\n"
                    player["fatto"] += danno_tuono
                except:
                    break
        
        elif set == 'Lanciatore olimpico' and proc_ok(num, set, "assalto", "tridente"):
            if nemico[target]["hp"] > proc_val(set, "assalto", "tridente", "hp_min"):
                nemico[target]["hp"] -= proc_val(set, "assalto", "tridente", "danno")
                text += f"{nome} lancia il tridente fortissimo e colpisce {target}!\n"
        elif (set == "Cercatore di reliquie" and proc_ok(num, set, "assalto", "cannoncino") and target == "Cannoncino"):
            text += "__Oddio una reliquia GIGANTE!__\n"
            player["def"] += proc_val(set, "assalto", "cannoncino", "def")

        elif set == "Manipolatore di morte" and proc_ok(num, set, "assalto", "distrazione"):
            text += "__Andate miei cari, distraete le difese!__\n"
            player["agi"] += proc_val(set, "assalto", "distrazione", "agi")
        elif set == "Cacciatore della feccia" and proc_ok(num, set, "assalto", "massa_nemici"):
            player["def"] += proc_val(set, "assalto", "massa_nemici", "def_per_nemico") * len(nemico)
            player["atk"] += proc_val(set, "assalto", "massa_nemici", "atk_per_nemico") * len(nemico)
            text += "🆙" * len(nemico) + "\n"
    
    num = random.random()    
    
    if "Bersaglio enorme" in list(nemico) and 0.2 > num:
        if set == "Vigilante":
            text += "__Nessuna distrazione__"
        else:
            target = "Bersaglio enorme"
            if set == "Serial killer":
                text += f"Anche se sa di aver sbagliato bersaglio {nome} è deciso ad arrivarci!"
                player["agi"] += proc_val(set, "assalto", "bersaglio_enorme", "agi")
    
    if "Divino" in effetti:
        player["atk"] = player["atk"] * 10
        player["def"] = player["def"] * 10000
    
    if anello != None:
        for pl in clan[team]['membri']:
            aniel = playerg[pl]["scheda"]["anello"]
            if aniel in PROC_ANELLI and "aura" in PROC_ANELLI[aniel].get("assalto", {}):
                cfg_anello = anello_cfg(aniel, "assalto", "aura")
                stat_anello = cfg_anello["stat"]
                valore_anello = cfg_anello["valore"]
                moltiplicatore = 1
                if set == "Portatore di morte":
                    moltiplicatore = proc_val(set, "assalto", "bonus_gadget", "moltiplicatore", 2)
                player[stat_anello] += valore_anello * moltiplicatore
                if set == "Portatore di morte" and aniel == "Occhio del falco":
                    text += "L'anello si raddoppia!\n"

            if playerg[pl]["scheda"]["set"] == "Re dei pirati" and pl != nome:
                dmg = round(max(proc_val("Re dei pirati", "assalto", "supporto_ciurma", "danno_min"), playerg[pl]["scheda"]["atk"] // proc_val("Re dei pirati", "assalto", "supporto_ciurma", "atk_divisore")))
                cosa = news = random.choice(list(nemico))
                nemico[cosa]["hp"] -= dmg
                text += f"**I\'M IN CHARGEEE NOW, {pl} infligge {dmg} a {cosa}**\n"
                try:
                    clan[team]["danno"][pl] += dmg
                except:
                    clan[team]["danno"][pl] = dmg
        if set == "Portatore di morte":
            text += "I gadget si raddoppiano!\n"
    
    if "Fabbro incantaspade" in clan[team]["villaggio"]:
        player["atk"] += 25 * clan[team]["villaggio"]["Fabbro incantaspade"]["lv"]
        player["def"] += 25 * clan[team]["villaggio"]["Fabbro incantaspade"]["lv"]
        if set == "Arciere di prima linea" and proc_ok(num, set, "assalto", "fabbro"):
            player["atk"] += proc_val(set, "assalto", "fabbro", "atk_per_livello") * clan[team]["villaggio"]["Fabbro incantaspade"]["lv"]
            player["def"] += proc_val(set, "assalto", "fabbro", "def_per_livello") * clan[team]["villaggio"]["Fabbro incantaspade"]["lv"]
            text += "Fabbro potenziato dal set "
        text += "⚔️"
    text += "\n"
    for difesa in order:
        
        if difesa in nemico:
            text += "\n"
            if bacon:
                player["hp"] += 11
            if nemico[difesa]["hp"] <= 0:
                nemico.pop(difesa)
            else:
                defense = player["def"]
                dps = player["atk"]
                agi = player["agi"]
                attaccon = (starmi[difesa]["atk"] + starmi[difesa]["atk"] * (nemico[difesa]["lv"] / 10) + bonus["atk"])
                difesan = (starmi[difesa]["def"] + starmi[difesa]["def"] * (nemico[difesa]["lv"] / 10) + bonus["def"])
                agin = (starmi[difesa]["agi"] + starmi[difesa]["agi"] * (nemico[difesa]["lv"] / 10) + bonus["agi"])
                    
                if set != None:
                    num = random.random()
                    if set == "Ultima speranza" and proc_ok(num, set, "assalto", "paura"):
                        text += "__Il fatto che non sei morto spaventa i nemici!__\n"
                        bonus["def"] += proc_val(set, "assalto", "paura", "bonus_def_nemico")
                    elif set == "Macellaio":
                        defense += player["hp"] / proc_val(set, "assalto", "carne", "hp_divisore")
                    elif set == 'Spadaccino Musashi':
                        defense = defense * proc_val(set, "assalto", "difesa", "def_mul")                    
                    elif set == "Proiettile":
                        defense += proc_val(set, "assalto", "difesa", "def")
                    elif set == "Illusionista" and proc_ok(num, set, "assalto", "copie"):
                        agin += proc_val(set, "assalto", "copie", "agi_difesa")
                        text += f"Copie di {nome} si spargono a caso!\n"

                    elif set == "Uomo di classe" and proc_ok(num, set, "assalto", "spumeggiante"):
                        dps = attaccon
                        defense = difesan
                        agin += proc_val(set, "assalto", "spumeggiante", "agi_difesa")
                        text += "**Spumeggiante!**\n"

                    elif set == "Maestro delle tartarughe" and proc_ok(num, set, "assalto", "carapace"):
                        player["def"] += proc_val(set, "assalto", "carapace", "def")
                        text += f"__{nome} sfrutta il carapace come difesa!__\n"

                    elif set == "Difensore delle mareggiate" and proc_ok(num, set, "assalto", "fauna"):
                        player["atk"] += proc_val(set, "assalto", "fauna", "atk")
                        text += f"__{nome} viene supportato dalla fauna ittica!__\n"

                    elif set == "Uomo di un tempo":
                        player["hp"] += proc_val(set, "assalto", "vitalita", "hp")

                    elif set == "Chierico" and proc_ok(num, set, "assalto", "cura"):
                        player["hp"] += proc_val(set, "assalto", "cura", "cura")
                        text += "__Una luce aiuta nel recupero delle forze ☦️__\n"

                    elif set == "Medico improvvisato" and proc_ok(num, set, "assalto", "cura"):
                        player["hp"] += proc_val(set, "assalto", "cura", "cura")
                        text += "__Il totem cura un poco ☦️__\n"

                    elif set == "Guaritore da campo" and proc_ok(num, set, "assalto", "cura"):
                        player["hp"] += proc_val(set, "assalto", "cura", "cura")
                        text += "__Della cura viene dispersa nell'aria ☦️__\n"

                    elif set == "Druido della selva" and proc_ok(num, set, "assalto", "natura"):
                        player["atk"] += proc_val(set, "assalto", "natura", "atk")
                        player["def"] += proc_val(set, "assalto", "natura", "def")
                        player["agi"] += proc_val(set, "assalto", "natura", "agi")
                        text += f"__{nome} usa il potere della natura per crescere!__\n"

                    elif set == "Cacciatore di bestie" and proc_ok(num, set, "assalto", "previsione"):
                        agi += proc_val(set, "assalto", "previsione", "agi")
                        text += f"__{nome} capisce cosa sta per succedere!__\n"

                    elif set == "Vampiro" and proc_ok(num, set, "assalto", "pipistrello"):
                        agi += proc_val(set, "assalto", "pipistrello", "agi")
                        text += f"__{nome} si trasforma in un pipistrello per provare ad eludere le difese!__\n"

                    elif set == "Ricercatore del pericolo" and proc_ok(num, set, "assalto", "adrenalina"):
                        player["atk"] += proc_val(set, "assalto", "adrenalina", "atk")
                        text += f"__{nome} carica con l'adrenalina il colpo!__\n"
                    elif set == "Abitante" and proc_ok(num, set, "assalto", "alberelli"):
                        bonus["atk"] += proc_val(set, "assalto", "alberelli", "bonus_atk_nemici")
                        text += f"__{nome} pianta alberelli e scava buce per difendersi!__\n"
                    elif set == "Elfo silvano" and proc_ok(num, set, "assalto", "evasione"):
                        bonus["agi"] *= proc_val(set, "assalto", "evasione", "moltiplicatore_bonus_agi")
                
                if len(nemico) == 1:
                    text += "Ormai resta poco da fare per le difese...\n\n"
                    attaccon -= 100
                    agin -= 10
                    difesan -= 300
                    if difesan < 0:
                        difesan = 0
                
                if difesa == "Clone":
                    try:
                        cattivoni = clan[team]["inguerra"]
                        if cattivoni == None:
                            cattivoni = nemico["inguerra"]
                        nomeclone = clan[cattivoni]["Sacrificio"]
                        if nomeclone != None:

                            attaccon = nemico["Clone"]["atk"]
                            difesan = nemico["Clone"]["def"]
                            agin = nemico["Clone"]["agi"]
                            if setting["Clone"] == "Difensivo":
                                agin -= 40
                                text += f"{nomeclone} cerca di correre alla pulsantiera!\n"
                        else:
                            nomeclone = "Una massa informe"
                            attaccon = 0
                            difesan = 0
                            agin = 0

                        if set == "Ghoul" and proc_ok(num, set, "assalto", "terrore_clone"):
                            text += f"__{nomeclone} è terrorizzato da {nome}__"
                            attaccon += proc_val(set, "assalto", "terrore_clone", "atk_clone")
                            difesan += proc_val(set, "assalto", "terrore_clone", "def_clone")
                    except:
                        nomeclone = "Una massa informe"
                        attaccon = 0
                        difesan = 0
                        agin = 0
                
                elif difesa == "Sedimento del cucciolo" and setting["Sedimento del cucciolo"] == "Affamato":
                    agin += 55
                    text += "__Si sente un gorgoglio...__\n"
                    attaccon = attaccon//1.5
                
                elif setting["Spuntone malefico"] == "Sotterraneo" and difesa == "Spuntone malefico":
                    text += "Stranamente lo spuntone non è qui!\n"
                    agin -= 25

                elif setting["Stazione laser di sicurezza"] == "Difesa laser" and difesa == "Stazione laser di sicurezza":
                    old = attaccon
                    attaccon = difesan * 2
                    difesan = old//2
                    text += "La difesa laser si alza sotto la stazione!\n"
                    
                elif setting["Stazione laser di sicurezza"] == "Suicidio laser" and difesa == "Stazione laser di sicurezza":
                    nemico[difesa]["hp"] -= 55
                    attaccon = round(attaccon * 2.5)
                    agin -= 26
                    
                    text += "La torre laser si sovraccarica!\n"
                
                colpito = round(agi - (agin / 2) + 1)
                
                if colpito > random.randint(0, 102):
                    if setting["Sedimento del cucciolo"] == "Affamato" and difesa == "Sedimento del cucciolo":
                        text += "Il cucciolo di drago sta mangiando altro..\n"
                    elif setting["Spuntone malefico"] == "Sotterraneo" and difesa == "Spuntone malefico":
                        text += "No, nessuno spuntone!\n"
                    elif setting["Chiesa"] == "Orribile" and difesa == "Chiesa":
                        if 0.1 > num:
                                    num = random.random()
                                    bonus["atk"] += 250
                                    bonus["def"] += 250
                                    bonus["agi"] += 25
                                    text += f"Una creatura orribile esce dalla chiesa, pronta seminare il chaos!\n"
                        else:
                            text += "Un antica creatura riposa nella chiesa\n"
                    else:
                        text += frasi["miss"][difesa]
                    if difesa == "Muraglione extra":
                        bonus["def"] += 5 * (nemico[difesa]["lv"] + (len(nemico)/4))
                    elif difesa == "Spuntone malefico":
                        text += "\n**Si apre al volo una botola sotto i tuoi piedi!**\n"
                        for x in range(nemico[difesa]["lv"]):
                            num = random.random()
                            if setting["Spuntone malefico"] == "Sotterraneo":
                                num += .2
                            if 0.6 > num:
                                break
                            else:
                                if defense < 0:
                                    attaccon -= defense
                                    defense = 0
                                dannissimi = round(float(attaccon)* (100 / (50 + float(defense))* random.uniform(0.7, 1.5)))
                                player["hp"] -= dannissimi
                                nos = player["hp"]
                                text += f"Cade così sul {x+1}° spuntone! ({nos})\n"                            
                            if set == "Cavaliere delle spine" and proc_ok(num, set, "assalto", "spuntone_schivato"):
                                text += f"\n{nome} prende spuntoni extra per la sua armatura e prosegue!\n"
                                player["def"] += proc_val(set, "assalto", "spuntone_schivato", "def")
                                player["atk"] += proc_val(set, "assalto", "spuntone_schivato", "atk")
                                player["hp"] += dannissimi
                    elif difesa == "Clone":
                        text += f"{nomeclone} non riesce a farti nulla, ma direziona le difese verso di te!\n"
                        bonus["atk"] += 20
                    elif difesa == "Centrale di cura centralizzata":
                        if set == "Ombra silenziosa" and proc_ok(num, set, "assalto", "centrale"):
                            text += "__Arrivi giusto in tempo alla centrale prima che emetta il suo impulso e la (silenzi)!__\n"
                            player["atk"] += proc_val(set, "assalto", "centrale", "atk")

                        else:
                            if setting["Centrale di cura centralizzata"] == "Sparsa":
                                if set == "Assassino delle ombre" and proc_ok(num, set, "assalto", "centrale"):
                                    text += (
                                        f"La centrale di cura danneggia tutte le strutture!\n"
                                    )
                                    for dife in nemico:
                                        if dife == "inguerra":
                                            pass
                                        else:
                                            player["fatto"] += 3 * int(nemico[difesa]["lv"])
                                            if nemico[dife]["hp"] > 50:
                                                nemico[dife]["hp"] += -3 * int(nemico[difesa]["lv"])
                                else:
                                    text += (
                                        f"La centrale cura tutte le difese!\n"
                                    )
                                    for dife in nemico:
                                        if dife == "inguerra":
                                            pass
                                        else:
                                            nemico[dife]["hp"] += 3 * int(nemico[difesa]["lv"])
                            else:
                                news = random.choice(list(nemico))
                                if set == "Assassino delle ombre" and proc_ok(num, set, "assalto", "centrale"):
                                    text += (
                                        f"La centrale di cura danneggia {news}!\n"
                                    )
                                    for dife in nemico:
                                        if dife == "inguerra":
                                            pass
                                        else:
                                            player["fatto"] += 3 * int(nemico[difesa]["lv"])
                                            if nemico[news]["hp"] > 50:
                                                nemico[news]["hp"] += -3 * int(nemico[difesa]["lv"])
                                else:
                                    text += (
                                        f"La centrale cura {news}!\n"
                                    )
                                    for dife in nemico:
                                        if dife == "inguerra":
                                            pass
                                        else:
                                            nemico[news]["hp"] += 3 * int(nemico[difesa]["lv"])
                    
                else:
                    num = random.random()
                    if "animale" in player and 0.05 > num:
                        nima = player["animale"]
                        player["def"] += 20
                        text += f"{nima} si schiera con {nome} contro la difesa!\n"
                    serve = False
                    if set != None:
                        if difesa == "Clone" and set == "Regina golgari" and proc_ok(num, set, "assalto", "clone"):
                            text += "Il clone è pietrificato!\n"
                        elif difesa == "Accampamento" and set == "Cercatore" and proc_ok(num, set, "assalto", "accampamento"):
                            text += "__L'accampamento è pieno di cose utili!__\n\n"
                            player["atk"] += proc_val(set, "assalto", "accampamento", "atk")
                        
                        elif difesa == "Spaventapasseri ornamentale" and set == "Scudiero del boschetto":
                            text += (f"Lo spaventapasseri inizia a muoversi e aiutare {nome}!\n")
                            player["atk"] += proc_val(set, "assalto", "spaventapasseri", "atk")
                            player["def"] += proc_val(set, "assalto", "spaventapasseri", "def")
                        
                        elif set == "Anima oscura" and proc_ok(num, set, "assalto", "fabbro") and difesa == "Fabbro incantaspade":
                            text += f"__Il fabbro riconosce {nome} e visto che suo fido alievo evita di menarlo fortissimo!__\n"
                        
                        elif set == "Campione del sole" and proc_ok(num, set, "assalto", "fabbro") and difesa == "Fabbro incantaspade":
                            text += f"__Il fabbro nota {nome}, non si può colpire un amico! Lo si può solo armare!__\n"
                            player["atk"] += proc_val(set, "assalto", "fabbro", "atk")
                            player["def"] += proc_val(set, "assalto", "fabbro", "def")
                        
                        elif difesa == "Stazione laser di sicurezza" and set == "Contrabbandiere" and proc_ok(num, set, "assalto", "laser"):
                            text += f"{nome} conosce benissimo questo laser, non avrà problemi!\n"
                        
                        elif difesa == "Cane da guardia" and set == "Juggernaut" and proc_ok(num, set, "assalto", "cane"):
                            text += f"__Il cane non riesce a morderti a causa della tua spessa armatura!__\n"
                        
                        elif difesa == "Spuntone malefico" and set == "Cavaliere delle spine" and proc_ok(num, set, "assalto", "spuntone_colpito"):
                            text += f"\n{nome} prende spuntoni extra per la sua armatura e prosegue!\n"
                            player["def"] += proc_val(set, "assalto", "spuntone_colpito", "def")
                        
                        elif difesa == "Cannoncino" and set == "IppoFan" and proc_ok(num, set, "assalto", "cannoncino"):
                            text += "__Confondi il cannone e fuggi velocissimo!__"
                        
                        elif difesa == "Sedimento del cucciolo" and set == "Drago" and proc_ok(num, set, "assalto", "cucciolo"):
                            player["atk"] += proc_val(set, "assalto", "cucciolo", "atk")
                            text += f"__Il cucciolo di drago si sveglia e amicizza con {nome}!__\n"
                        
                        elif difesa == "Sedimento del cucciolo" and set == "Guerriero 3D" and proc_ok(num, set, "assalto", "cucciolo"):
                            text += f"__Il cucciolo di drago si sveglia, e spaventato da {nome} lo infiamma, ma prontamente si spegne con un secchio d'acqua!__\n"
    
                        elif difesa == "Sedimento del cucciolo" and set == "PiroIncantatore" and proc_ok(num, set, "assalto", "cucciolo_drago"):
                            player["atk"] += proc_val(set, "assalto", "cucciolo_drago", "atk")
                            text += f"__Il cucciolo di drago si sveglia ma non può usare le fiamme contro di te!__\n"

                        elif difesa == "Centrale di cura centralizzata" and set == "Ombra silenziosa" and proc_ok(num, set, "assalto", "centrale"):
                            text += "__Arrivi giusto in tempo alla centrale prima che emetta il suo impulso e la (silenzi)!__\n"
                            player["atk"] += proc_val(set, "assalto", "centrale", "atk")
                        elif difesa == "Centrale di cura centralizzata" and set == "Assassino delle ombre" and proc_ok(num, set, "assalto", "centrale"):
                            if setting["Centrale di cura centralizzata"] == "Sparsa":
                                text += f"La centrale di cura danneggia tutte le strutture!\n"
                                for dife in nemico:
                                    if dife == "inguerra":
                                        pass
                                    else:
                                        
                                        player["fatto"] += 3 * int(nemico[difesa]["lv"])
                                        if nemico[dife]["hp"] > 50:
                                            nemico[dife]["hp"] += -3 * int(nemico[difesa]["lv"])      
                            else:
                                
                                news = random.choice(list(nemico))
                                text += (
                                        f"La centrale di cura danneggia {news}!\n"
                                    )
                                for dife in nemico:
                                        if dife == "inguerra":
                                            pass
                                        else:
                                            player["fatto"] += 3 * int(nemico[difesa]["lv"])
                                            if nemico[news]["hp"] > 50:
                                                nemico[news]["hp"] += -3 * int(nemico[difesa]["lv"])                  
                        else:
                            serve = True

                    else:
                        serve = True

                    if player["hp"] <= 0:
                        text += f"\n{nome} cade a terra, un granchio gigante di soccorso lo raccoglie al volo e fugge in mare velocissimo!\n"
                        break
                    
                    if serve:
                        num = random.random()
                        if difesa != "Spaventapasseri ornamentale":
                            if difesa == "Muraglione extra":
                                defense *= 0.5
                            
                            if defense < 0:
                                attaccon -= defense
                                defense = 0
                            
                            dannissimi = round(float(attaccon)* (100 / (1 +float(defense)) * random.uniform(0.7, 1.5)))
                            
                            if setting["Accampamento"] == "Trappole demoralizzanti" and difesa == "Accampamento":
                                dannissimi = dannissimi//1.3
                            
                            elif setting["Cane da guardia"] == "Cane rapido" and difesa == "Cane da guardia":
                                dannissimi =round( dannissimi//1.3)
                            elif setting["Cane da guardia"] == "Orso" and difesa == "Cane da guardia":
                                dannissimi =round( dannissimi * 1.5)
                            
                            elif setting["Cannoncino"] == "Danneggiante" and difesa == "Cannoncino":
                                dannissimi = dannissimi * 2
                                text += "BOOM!\n"
                            

                            elif setting["Muraglione extra"] == "Infiammato" and difesa == "Muraglione extra":
                                dannissimi += 250
                                nemico[difesa]["hp"] -= 100
                            
                            if dannissimi <= 0:
                                dannissimi = 5
                                
                            if setting["Fabbro incantaspade"] == "Curativo" and difesa == "Fabbro incantaspade":
                                dannissimi = 0
                            elif setting["Chiesa"] == "Orribile" and difesa == "Chiesa":
                                dannissimi = 0
                                text += "La chiesa pare contenere un antico male...\n"
                            
                            player["hp"] -= dannissimi
                            nos = player["hp"]
                        
                        else:
                            nos = 0
                            dannissimi = 0
                        try:
                            if setting["Accampamento"] == "Trappole demoralizzanti" and difesa == "Accampamento":
                                bonus["atk"] += 50
                                text += f"Delle trappole escono a iosa dalle tende, infliggendo {dannissimi} danni ({nos})\n"
                            elif setting["Chiesa"] == "Orribile" and difesa == "Chiesa":
                                if 0.1 > num:
                                    num = random.random()
                                    bonus["atk"] += 250
                                    bonus["def"] += 250
                                    bonus["agi"] += 25
                                    text += f"Una creatura orribile esce dalla chiesa, pronta seminare il chaos!\n"
                            
                            elif setting["Fabbro incantaspade"] == "Curativo" and difesa == "Fabbro incantaspade":
                                news = random.choice(list(nemico))
                                dannissimi = round(float(attaccon)* (100 / (1 +float(defense)) * random.uniform(0.7, 1.5)))
                                nemico[news]["hp"] += dannissimi
                                nos = nemico[news]["hp"]
                                text += f"Il fabbro ripara un poco {news} per {dannissimi} hp, ne ha ora {nos}\n"
                            
                            elif setting["Spaventapasseri ornamentale"] == "Animato" and difesa == "Spaventapasseri ornamentale":
                                
                                dannissimi = round(float(attaccon)* (100 / (1 +float(defense)) * random.uniform(0.7, 1.5)))
                                if dannissimi <= 0:
                                    dannissimi = 5
                                
                                player["hp"] -= dannissimi
                                nos = player["hp"]

                                text += f"Lo spaventapasseri ti colpisce alle spalle per {dannissimi} danni!({nos})\n"
                            
                            else:
                                text += frasi["preso"][difesa]%(dannissimi,nos)
                                
                        except:
                            text += frasi["preso"][difesa]
                        
                        if difesa == "Muraglione extra":
                            bonus["def"] += 5 * (nemico[difesa]["lv"] + (len(nemico)/4))
                            if difesa == "Muraglione extra" and 0.1 > num:
                                text += "__Il taglio ha fatto una brutta infezione...__\n"
                                player["def"] -= 50
                        elif difesa == "Spaventapasseri ornamentale" and 0.1 > num and setting["Spaventapasseri ornamentale"] != "Animato":
                            text += "Sembra che lo spaventapasseri non sia così inutile, sta facendo cose?\n\nODDIO MA COSA SONO TUTTI QUI CORVI!"
                            break
                        elif difesa == "Stazione laser di sicurezza" and 0.1 > num:
                            bonus["def"] += 10 * nemico[difesa]["lv"]
                        elif difesa == "Cane da guardia" and 0.3 > num and setting["Cane da guardia"] != "Orso":
                            text += f"{nome} non è abbastanza veloce ed il cane lo riinsegue,subendo così altri {dannissimi} danni!\n"
                            player["hp"] -= dannissimi
                            num = random.random()
                            dannissimi = round(dannissimi//2)
                            for g in range(4):
                                if difesa == "Cane da guardia" and 0.5 > num and setting["Cane da guardia"] == "Cane rapido":
                                    text += f"{nome} non è ancora abbastanza veloce ed il cane lo riinsegue,subendo così altri {dannissimi} danni!\n"
                                    player["hp"] -= dannissimi
                                else:
                                    break

                        elif difesa == "Cannoncino" and setting["Cannoncino"] != "Danneggiante":
                            bonus["agi"] += 5
                            if 0.1 > num:
                                text += f"**Sbaglio o questo colpo ha svegliato un drago nelle circostanze?**\n"
                                bonus["agi"] += 20
                        
                        elif difesa == "Spuntone malefico":
                            bonus["def"] += 2 * nemico[difesa]["lv"]
                        
                        elif difesa == "Sedimento del cucciolo" and 0.1 > num:
                            text += f"**Il drago ancora spaventato richiama la mamma, che altro che sparare fuoco, schiaccia {nome}!**\n"
                            player["hp"] = random.randint(-2, 10)
                        
                        elif difesa == "Centrale di cura centralizzata":
                            if set == "Assassino delle ombre" and num <= (proc_val(set, "assalto", "centrale", "proc_post") / 100):
                                if setting["Centrale di cura centralizzata"] == "Sparsa":
                                    text += (
                                        f"La centrale di cura danneggia tutte le strutture!\n"
                                    )
                                    for dife in nemico:
                                        if dife == "inguerra":
                                            pass
                                        else:
                                            player["fatto"] += 3 * int(nemico[difesa]["lv"])
                                            if nemico[dife]["hp"] > 50:
                                                nemico[dife]["hp"] += -3 * int(nemico[difesa]["lv"])
                                else:
                                    news = random.choice(list(nemico))
                                    text += (
                                            f"La centrale di cura danneggia {news}!\n"
                                        )
                                    for dife in nemico:
                                            if dife == "inguerra":
                                                pass
                                            else:
                                                nemico[news]["hp"] += -3 * int(nemico[difesa]["lv"])
                            else:
                                if setting["Centrale di cura centralizzata"] == "Sparsa":
                                    text += "Cure a non finire sgorgano per l'intero villaggio!\n"
                                    for dife in nemico:
                                        if dife == "inguerra":
                                            pass
                                        else:
                                            
                                            player["fatto"] += 3 * int(nemico[difesa]["lv"])
                                            if nemico[dife]["hp"] > 50:
                                                nemico[dife]["hp"] += 3 * int(nemico[difesa]["lv"])        
                                else:
                                    news = random.choice(list(nemico))
                                    text += (
                                            f"La centrale di cura cura {news}!\n"
                                        )
                                    for dife in nemico:
                                            if dife == "inguerra":
                                                pass
                                            else:
                                                nemico[news]["hp"] += 3 * int(nemico[difesa]["lv"])
                    
                    if set != None:
                        if set == "Sopravvissuto" and proc_ok(num, set, "assalto", "sopravvive"):
                            text += "Sopravvissuto ancora!\n"
                            player["atk"] += dannissimi / proc_val(set, "assalto", "sopravvive", "atk_divisore")
                        elif set == "Sanguinolento" and proc_ok(num, set, "assalto", "sangue"):
                            player["atk"] += dannissimi / proc_val(set, "assalto", "sangue", "divisore_atk")
                            player["def"] += dannissimi / proc_val(set, "assalto", "sangue", "divisore_def")
                            text += f"**{nome} si potenzia con il sangue sul campo di battaglia!**\n"

                        elif set == "Orrido" and proc_ok(num, set, "assalto", "sgignolo"):
                            nemico[difesa]["hp"] -= proc_val(set, "assalto", "sgignolo", "danno")
                            text += f"**{nome} non riesce a tenere sgignolo, infligge 33 danni alla difesa!**\n"
                            player["fatto"] += proc_val(set, "assalto", "sgignolo", "danno")
                    
                    
                if player["hp"] <= 0:
                    text += f"\n{nome} cade a terra, un granchio gigante di soccorso lo raccoglie al volo e fugge in mare velocissimo!\n"                        
                    break   
                
                if difesa == target:
                        num = random.random()
                        
                        
                        if set == "Bug Abuser" and proc_ok(num, set, "assalto", "target"):
                            num = random.random()
                            if num < (proc_val(set, "assalto", "target", "s1") / 100):
                                text += f"__A me orripilante creatura!__\n"
                                dps += proc_val(set, "assalto", "target", "dps1")
                            elif num < (proc_val(set, "assalto", "target", "s2") / 100):
                                text += f"__{nome} grazie al suo cannoncino copisce fortissimo il Cannoncino!__\n"
                                dps += proc_val(set, "assalto", "target", "dps2")
                            elif num < (proc_val(set, "assalto", "target", "s3") / 100):
                                text += f"__La maledizione di {nome} si presenta!__\n"
                                cura = round((player["hp"] * proc_val(set, "assalto", "target", "percento_hp")) / 100)
                                dps += cura
                            elif num < (proc_val(set, "assalto", "target", "s4") / 100):
                                text += "__La spada beta si attiva!__\n"
                                dps += proc_val(set, "assalto", "target", "dps4")
                            else:
                                text += f"__{nome} becca inoltre in pieno il draghetto!__\n"
                                dps += proc_val(set, "assalto", "target", "dps5")

                        elif set == "Betatester" and proc_ok(num, set, "assalto", "spada_beta"):
                            text += "__La spada beta si attiva!__\n"
                            dps += proc_val(set, "assalto", "spada_beta", "dps")

                        elif set == "Maledetto" and proc_ok(num, set, "assalto", "maledizione"):
                            text += f"__La maledizione di {nome} si presenta!__\n"
                            cura = round((player["hp"] * proc_val(set, "assalto", "maledizione", "percento_hp")) / 100)
                            dps += cura

                        elif (set == "Crociato" and target == "Muraglione extra" and proc_ok(num, set, "assalto", "muraglione")):
                            text += f"__{nome} grazie al potere della luce incendia questo blocco!__\n"
                            dps += dps + dps + dps + dps

                        elif (set == "Primo alla bandiera" and target == "Cannoncino" and proc_ok(num, set, "assalto", "cannoncino")):
                            text += f"__{nome} grazie al suo cannoncino copisce fortissimo il Cannoncino!__\n"
                            dps += proc_val(set, "assalto", "cannoncino", "dps")

                        elif (
                            set == "Ice and fire"
                            and target == "Sedimento del cucciolo"
                            and proc_ok(num, set, "assalto", "drago_scaccia_drago")
                        ):
                            text += f"__Drago scaccia drago!__\n"
                            dps += proc_val(set, "assalto", "drago_scaccia_drago", "dps")

                        elif (
                            set == "Cacciatore"
                            and target == "Sedimento del cucciolo"
                            and proc_ok(num, set, "assalto", "draghetto")
                        ):
                            text += f"__{nome} becca inoltre in pieno il draghetto!__\n"
                            dps += proc_val(set, "assalto", "draghetto", "dps")

                        elif (
                            set == "Spacca Mostri"
                            and target == "Clone"
                            and proc_ok(num, set, "assalto", "clone")
                        ):
                            text += f"__A me orripilante creatura!__\n"
                            dps += proc_val(set, "assalto", "clone", "dps")
                        if difesan < 0:
                            dps -= difesan
                            difesan = 0
                        dannissimi = round(float(dps) * (100 / (float(1 + difesan)) * random.uniform(0.7, 1.3)))

                        if set == "Cavaliere d'argento":
                            dannissimi += proc_val(set, "assalto", "danno_fisso", "danno")

                        elif set == "Orrido":
                            dannissimi = proc_val(set, "assalto", "sgignolo", "danno")
                        player["fatto"] += dannissimi
                        
                        if dannissimi <= 0:
                            dannissimi *= -1
                        num = random.random()
                        if setting["Bersaglio enorme"] == "Movibile" and num >= 0.3 and target == "Bersaglio enorme":
                            dannissimi = 0
                            text += "**Il bersaglio si sposta all'ultimo!**\n"
                        
                        if setting["Bersaglio enorme"] == "Movibile" and target == "Bersaglio enorme":
                            dannissimi *= 4
                        
                        try:
                            nemico[difesa]["hp"] -= dannissimi
                            nos = nemico[difesa]["hp"]

                            text += f"\n**{nome} arriva al bersaglio, il {difesa}, infliggendo {dannissimi} ({nos}) danni alla struttura!**\n"
                        
                        except Exception as e:
                            print(f"{e}, Assalto nel danno")
                        if nemico[difesa]["hp"] <= 0:
                            nemico.pop(difesa)
                            text += "**E' andata!!**\n"
                        if set == "Fire lord":
                            cfg = proc_cfg(set, "assalto", "catena")
                            for x in range(cfg["tentativi"]):
                                num = random.random()
                                if num < (cfg["stop_proc"] / 100):
                                    break
                                else:
                                    try:
                                        news = random.choice(list(nemico))
                                        if nemico[news]["hp"] < cfg["hp_min"]:
                                            break
                                        nemico[news]["hp"] -= cfg["danno"]

                                        nos = nemico[difesa]["hp"]
                                        text += f"\n**{nome} impugna il suo maglio fiammeggiante e infligge {cfg['danno']} danni anche a {news}, che nulla blocchi la sua furia!**\n"
                                        if nemico[news]["hp"] <= 0:
                                            nemico.pop(news)
                                            text += "**E' andata!!**\n"
                                        
                                        player["fatto"] += cfg["danno"]
                                    except:
                                        break

                        elif set == "Shogun moderno" and proc_ok(num, set, "assalto", "doppio_colpo"):
                            if difesan < 0:
                                dps -= difesan
                                difesan = 0
                            dannissimi = round(
                                float(dps)
                                * (100 / (proc_val(set, "assalto", "doppio_colpo", "denominatore") + float(1 + difesan)) * random.uniform(proc_val(set, "assalto", "doppio_colpo", "random_min"), proc_val(set, "assalto", "doppio_colpo", "random_max")))
                            )
                            nemico[difesa]["hp"] -= dannissimi
                            nos = nemico[difesa]["hp"]
                            text += f"\n**DOPPIO COLPO!\nInfligge {dannissimi} ({nos}) danni alla struttura!**\n"
                            player["fatto"] += dannissimi
                        
                        elif set == "Pazzoide glamour" and proc_ok(num, set, "assalto", "cura_target"):
                            player["hp"] += dannissimi
                            text += "Pazzesko!\n"

                        elif set == "Combattente 2D" and proc_ok(num, set, "assalto", "raggio_lunare"):
                            if difesan < 0:
                                dps -= difesan
                                difesan = 0
                            dannissimi = round(
                                float(dps)
                                * (100 / (proc_val(set, "assalto", "raggio_lunare", "denominatore") + float(1 + difesan)) * random.uniform(proc_val(set, "assalto", "raggio_lunare", "random_min"), proc_val(set, "assalto", "raggio_lunare", "random_max")))
                            )
                            nemico[difesa]["hp"] -= dannissimi
                            nos = nemico[difesa]["hp"]
                            text += f"\n**Un raggio lunare colpisce {difesa}, infliggendo {dannissimi} ({nos}) danni alla struttura!**\n"
                            player["fatto"] += dannissimi
                        
                        if anello == "Carica mobile" and anello_ok(num, anello, "assalto", "esplosione"):
                            dannissimi = random.randint(
                                anello_val(anello, "assalto", "esplosione", "danno_min"),
                                anello_val(anello, "assalto", "esplosione", "danno_max"),
                            )
                            try:
                                nemico[difesa]["hp"] -= dannissimi
                            except:
                                pass
                            nos = nemico[difesa]["hp"]
                            text += f"\n**BOOOOM({dannissimi})!**\n"
                            player["fatto"] += dannissimi
                
                if set == "Cultista pazzo" and proc_ok(num, set, "assalto", "ultimo_colpo"):
                        num = random.random()
                        news = random.choice(list(nemico))
                        if nemico[news]["hp"] > proc_val(set, "assalto", "ultimo_colpo", "hp_min"):
                            danno_follia = proc_val(set, "assalto", "ultimo_colpo", "danno")
                            nemico[news]["hp"] -= danno_follia
                            text += f"\n__{nome} prima di terminare del tutto, con un colpo di follia, infligge {danno_follia} danni a {news}!__\n"
                            
                        player["fatto"] += proc_val(set, "assalto", "ultimo_colpo", "danno")
    num = random.random()
    if set == "Mariachi" and player["hp"] <= 0 and proc_ok(num, set, "assalto", "resurrezione"):
        text += f"\n**Questa disfatta non basta per far desistere {nome}, che anzi si rialza pronto a combattere!\n"
        player["hp"] = proc_val(set, "assalto", "resurrezione", "hp")

    elif necron and player["hp"] <= 0:
        text += "\n**Il nucleo necron sprigiona un aura oscura che riporta in vita il malcapitato, per ora...**"
        player["hp"] = 1000

    elif (set == "Guardiano del passaggio" and player["hp"] <= 0 and proc_ok(num, set, "assalto", "resurrezione")):
        text += f"\n**{nome} ritorna dalla morte, pronto a combattere ancora!\n"
        player["hp"] = proc_val(set, "assalto", "resurrezione", "hp")

    elif set == "Fiamma pura" and player["hp"] <= 0 and proc_ok(num, set, "assalto", "esplosione_morte"):
        text += f"\n{nome} esplode in un esplosione di fuoco dannegiando tutte le strutture!"
        for dife in nemico:
            if dife == "inguerra":
                pass
            else:
                if nemico[dife]["hp"] > proc_val(set, "assalto", "esplosione_morte", "hp_min_struttura"):
                    nemico[dife]["hp"] -= proc_val(set, "assalto", "esplosione_morte", "danno_struttura")
            player["fatto"] += proc_val(set, "assalto", "esplosione_morte", "danno_struttura")

    return text               
              

async def dungeon_boss(app, message,player,scelta,nop,username,evento,last_dungeon,inabilitati,tuttov):
    if ("Affronta" in scelta and "Boss" in player[username]["dungeon"]["mostri"]):
        other_time = last_dungeon.get(username,0)
        now = time.time() 
        modificatore = 0
        if evento["mod"] == "stop_dg":
            modificatore -= 5               
        if evento["mod"] == "più_dg":
            modificatore += 5
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



async def dungeon_mostro(app, message,player,scelta,nop,username,evento,last_dungeon,nemici,inabilitati,trader):
    if scelta in nemici:
        other_time = last_dungeon.get(username,0)
        now = time.time() 
        modificatore = 0
        if evento["mod"] == "stop_dg":
            modificatore -= 5                
        if evento["mod"] == "più_dg":
            modificatore += 5
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



async def arena(client, app, message, player, scelta, armi, protezioni, armieprot, Approcci, classi, trader, username):
    arenaitem = arenamod[trader["stagione"].lower()]
    megaset = ['Neo blaster', 'Spada a protoni', 'Z-Saber', 'Chip terra', 'Chip fuoco', 'Chip elettro', 'Chip lunare']
    scheda = player[username]["arena"]
    
    if scelta == "...":
        if username == trader["arena"]:
            await message.answer("No, tutto ok")
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

        if trader["arena"] != None and trader["arena"] != username:
            nome1 = username
            nome2 = trader["arena"]
            trader["arena"] = None
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
            trader["arena"] = username
            for appz in ["..."]:
                bottoni.append(
                        [InlineKeyboardButton(f"{appz}", callback_data=f"arena_{appz}")]
                    )
            reply_markup = InlineKeyboardMarkup(bottoni)
            await message.message.edit("Attendiamo un avversario!",reply_markup=reply_markup)

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


def turno(main, oppo,cond=None):
    text = str()
    nome1 = main["Nome"]
    nome2 = oppo["Nome"]

    anello = main["anello"]
    anellon = oppo["anello"]

    # Leggiadra neutralizza i gadget di entrambi per il solo turno corrente.
    # Non modifica l'equipaggiamento salvato nelle schede.
    leggiadra_presente = (
        "Leggiadra" in main.get("incantamenti", [])
        or "Leggiadra" in oppo.get("incantamenti", [])
    )
    if leggiadra_presente and incantesimo_ok(random.random(), "Leggiadra", "turno", "neutralizza_gadget"):
        if incantesimo_val("Leggiadra", "turno", "neutralizza_gadget", "blocca_anello_attaccante", True):
            anello = None
        if incantesimo_val("Leggiadra", "turno", "neutralizza_gadget", "blocca_anello_difensore", True):
            anellon = None
        text += "🎈 **Leggiadra neutralizza i gadget di entrambi!**\n"

    dps = main["atk"]
    difesan = oppo["def"]

    agi = main["agi"]
    agin = oppo["agi"]

    if anello == "Anello perfezionista" or anellon == "Anello perfezionista":
            random.seed(PROC_ANELLI["Anello perfezionista"]["generale"]["seed"])
    set = main.get("set",None)
    setN = oppo.get("set",None)

    # I set con blocco_set disattivano le abilità di entrambi prima di qualsiasi proc.
    blocca_set = (
        (set is not None and proc_val(set, "turno", "blocco_set", "blocca_set_avversario", False))
        or (setN is not None and proc_val(setN, "turno", "blocco_set", "blocca_set_avversario", False))
    )
    if blocca_set:
        set = "MusicoSciamano"
        setN = "MusicoSciamano"
    
    inte = main.get("int",0)
    bonus = (inte * 0.02) + 0.75   
    
    inten = oppo.get("int",0)
    bonusn = (inten * 0.02) + 0.75   

    dogebonus = 0

    if set != None:
        num = random.random()
        if set == 'Cecchino modulare':
            main["powa"] = main.get("powa", 0) + PROC_CLASSI[set]["turno"]["powa_per_turno"]

            cfg = proc_cfg(set, "turno", "colpo_caricato")
            if main["powa"] >= cfg["powa_min"] and proc_ok(num, set, "turno", "colpo_caricato"):
                text += "Colpo caricato!\n"
                dps += cfg["dps"]

            cfg = proc_cfg(set, "turno", "colpo_preciso")
            if main["powa"] >= cfg["powa_min"] and proc_ok(num, set, "turno", "colpo_preciso"):
                text += "Colpo preciso!\n"
                agi += cfg["agi"]

            cfg = proc_cfg(set, "turno", "colpo_possente")
            if main["powa"] >= cfg["powa_min"] and proc_ok(num, set, "turno", "colpo_possente"):
                text += "Colpo possente!\n"
                dps += cfg["dps"]

            cfg = proc_cfg(set, "turno", "cura_rapida")
            if main["powa"] >= cfg["powa_min"] and proc_ok(num, set, "turno", "cura_rapida"):
                text += "Cura rapida!\n"
                main["hp"] += cfg["cura"]

            cfg = proc_cfg(set, "turno", "colpo_perforante")
            if main["powa"] >= cfg["powa_min"] and proc_ok(num, set, "turno", "colpo_perforante"):
                text += "Colpo perforante!\n"
                difesan = cfg["difesa_target"]
        elif set == "Inferno risvegliato":
            main["atk"] += proc_val(set, "turno", "inferno", "atk_main")
            oppo["atk"] += proc_val(set, "turno", "inferno", "atk_target")
        elif set == "MusicoSciamano":
            setN = "MusicoSciamano"
        elif set == "Uomo di un tempo":
            main["hp"] += proc_val(set, "turno", "vitalita", "hp")
        elif set == "Juggernaut":
            agin *= 0.3
        elif set == "Corvo":
            dogebonus += proc_val(set, "turno", "pressione_evasiva", "dogebonus")
        elif set == "Scudiero del boschetto" and main["fatto"] <= proc_val("Scudiero del boschetto", "turno", "recupero", "fatto_max"):
            main["hp"] += proc_val("Scudiero del boschetto", "turno", "recupero", "hp")
            main["atk"] += proc_val("Scudiero del boschetto", "turno", "recupero", "atk")
            main["def"] += proc_val("Scudiero del boschetto", "turno", "recupero", "def")
            main["agi"] += proc_val("Scudiero del boschetto", "turno", "recupero", "agi")
        elif set == "Uomo di classe" and proc_ok(num, set, "turno", "spumeggiante_attacco"):
            if setN == "Ombra silenziosa" and proc_ok(num, setN, "turno", "silenzio_spumeggiante"):
                text += "(Silenziato)\n"
            else:
                text += "**Spumeggiante!**\n"
                dps = oppo["atk"]
        elif set == "Chierico" and proc_ok(num, set, "turno", "cura") and main["hp"] <= proc_val(set, "turno", "cura", "hp_max"):
            cura = round((main["hp"] * proc_val(set, "turno", "cura", "cura_percento_hp")) / 100) + proc_val(set, "turno", "cura", "cura_base")
            main["hp"] += cura
            text += f"__Cura automatica di {nome1}, {cura} hp presi ✝️__\n"
        elif set == "Vigilante" and proc_ok(num, set, "turno", "cambio_proiettili_attacco"):
            old = main["atk"]
            main["atk"] = main["def"] + proc_val(set, "turno", "cambio_proiettili_attacco", "bonus_difesa")
            main["def"] = old
            text += f"__{nome1} cambia proiettili__\n"
        elif set == "Maestro delle tartarughe" and proc_ok(num, set, "turno", "insegnamenti"):
            difesan -= proc_val(set, "turno", "insegnamenti", "riduzione_difesa_target")
            text += f"__{nome1} ricorda gli insegnamenti del vecchio saggio!__\n"
        elif set == "Druido della selva" and proc_ok(num, set, "turno", "inselvatichisce"):
            if setN == "Ombra silenziosa" and proc_ok(num, setN, "turno", "silenzio_druido"):
                    text += "(Silenziato)\n"
            else:
                    main["atk"] += proc_val(set, "turno", "inselvatichisce", "atk")
                    main["def"] += proc_val(set, "turno", "inselvatichisce", "def")
                    main["agi"] += proc_val(set, "turno", "inselvatichisce", "agi")
                    text += f"__{nome1} si inselvatichisce!__\n"
        elif set == "Incantatore di controparte" and proc_ok(num, set, "turno", "potere_cosmico"):
            if nome2 == "Franco est" or nome2 == "Fantasma del rimorso":
                pass
            else:
                oppo["anello"] = random.choice(list(anellic))
                text += f"__Mistici poteri cosmici partono da {nome1}!__\n"
        elif set == "PiroIncantatore" and proc_ok(num, set, "turno", "golem_fuoco"):
            agi += proc_val(set, "turno", "golem_fuoco", "agi")
            text += f"**{nome1} evoca un golem di fuoco di supporto!**\n"
            dps += round(main["def"] / proc_val(set, "turno", "golem_fuoco", "dps_da_def_divisore"))
        elif set == "Arciere di prima linea" and proc_ok(num, set, "turno", "sfinimento"):
            text += "__Il nemico è sfinito dai colpi subiti!__\n"
            oppo["def"] += proc_val(set, "turno", "sfinimento", "def_target")
            if difesan <= 0:
                difesan = 1
        elif set == "Forma elettro" and proc_ok(num, set, "turno", "chip"):
            text += "__Chip elettro, attivazione!__\n "
            agi += proc_val(set, "turno", "chip", "agi")
            dps += proc_val(set, "turno", "chip", "dps")
        elif set == "Bug Abuser" and proc_ok(num, set, "turno", "bug"):
            if proc_ok(random.random(), set, "turno", "golem_fuoco"):
                agi += proc_val(set, "turno", "golem_fuoco", "agi")
                text += f"**{nome1} evoca un golem di fuoco di supporto!**\n"
                dps += round(main["def"] / proc_val(set, "turno", "golem_fuoco", "dps_da_def_divisore"))
            elif proc_ok(random.random(), set, "turno", "druido"):
                main["atk"] += proc_val(set, "turno", "druido", "atk")
                main["def"] += proc_val(set, "turno", "druido", "def")
                main["agi"] += proc_val(set, "turno", "druido", "agi")
                text += f"__{nome1} si inselvatichisce!__\n"
            elif proc_ok(random.random(), set, "turno", "tartaruga"):
                difesan -= proc_val(set, "turno", "tartaruga", "riduzione_difesa")
                text += f"__{nome1} ricorda gli insegnamenti del vecchio saggio!__\n"
            elif proc_ok(random.random(), set, "turno", "vigilante"):
                old = main["atk"]
                main["atk"] = main["def"]
                main["def"] = old
                text += f"__{nome1} cambia proiettili__\n"
            elif proc_ok(random.random(), set, "turno", "chip_fuoco"):
                text += "__Chip fuoco, attivazione!__\n "
                dps += proc_val(set, "turno", "chip_fuoco", "dps")
        elif set == "Ghoul" and proc_ok(num, set, "turno", "pressione"):
            main["agi"] = oppo["agi"]
            oppo["atk"] += proc_val(set, "turno", "pressione", "atk_target")
            oppo["def"] += proc_val(set, "turno", "pressione", "def_target")
            text += f"__{nome2} si sente sotto pressione, non capisce...__\n"
        elif set == "Forma fuoco" and proc_ok(num, set, "turno", "chip"):
            text += "__Chip fuoco, attivazione!__\n "
            dps += proc_val(set, "turno", "chip", "dps")
        elif set == "Portatore di morte" and proc_ok(num, set, "turno", "crescita"):
            if setN == "Ombra silenziosa" and proc_ok(num, setN, "turno", "silenzio_crescita"):
                    text += "(Silenziato)\n"
            else:
                main["atk"] += proc_val(set, "turno", "crescita", "atk")
                main["def"] += proc_val(set, "turno", "crescita", "def")
                main["agi"] += proc_val(set, "turno", "crescita", "agi")
                text += f"__{nome1} cresce!__\n"      
        elif set == "Contrabbandiere" and "carica" in oppo:
            if proc_ok(num, set, "turno", "detonazione") or main["hp"] <= proc_val(set, "turno", "detonazione", "hp_trigger") or oppo["carica"] > proc_val(set, "turno", "detonazione", "cariche_trigger"):
                if oppo["carica"] > 0:
                    danno = oppo["carica"] * proc_val(set, "turno", "detonazione", "danno_per_carica")
                    oppo["hp"] -= danno
                    oppo["carica"] = 0
                    text += f"\n**Le cariche pazzate sopra {nome2} esplodono!** ({danno} hp persi)\n"
        elif set in ["Terrore delle ombre","Oracolo del buio","Ufficiale dell'oltretomba","Sciamano della verità","Dannato", "Dipper"]:
            if "marchio" in oppo:
                
                cfg = proc_cfg(set, "turno", "marchio")
                if num < (cfg.get("proc_aggiungi", 0) / 100):
                    oppo["marchio"] += 1
                    text += "🧿"
                elif set == "Terrore delle ombre" and num < (cfg.get("proc_effetto", 0) / 100):
                    text += f"I marchi di {nome2} potenziano {nome1}\n"
                    main["atk"] += oppo["marchio"] * cfg["atk_per_marchio"]
                    main["def"] += oppo["marchio"] * cfg["def_per_marchio"]
                    main["agi"] += oppo["marchio"] * cfg["agi_per_marchio"]
                    
                elif set == "Oracolo del buio" and num < (cfg.get("proc_effetto", 0) / 100):
                    text += f"La fine è vicina {nome2}\n"
                    oppo["atk"] += oppo["marchio"] * cfg["atk_per_marchio"]
                    oppo["def"] += oppo["marchio"] * cfg["def_per_marchio"]
                    oppo["agi"] += oppo["marchio"] * cfg["agi_per_marchio"]
                elif set == "Sciamano della verità" and num < (cfg.get("proc_effetto", 0) / 100):
                    text += f"I marchi di {nome2} nutrono {nome1}\n"
                    main["hp"] += oppo["marchio"] * cfg["cura_per_marchio"]
                
                elif set == "Dannato" and num < (cfg.get("proc_effetto", 0) / 100):
                    text += f"{nome2} brucia sotto i marchi\n"
                    oppo["hp"] -= oppo["marchio"] * cfg["danno_per_marchio"]
                    
                elif set == "Dipper" and num < (cfg.get("proc_effetto", 0) / 100) and oppo["marchio"] >= cfg["marchi_min"]:
                    text += f"{nome2} è troppo marchiato, {nome1} riesce a sfruttare tutti i marchi\n"
                    oppo["hp"] = round(oppo["hp"] / cfg["divisore_hp"])
                    main["hp"] = round(main["hp"] / cfg["divisore_hp"])
                else:
                    pass
            else:
                oppo["marchio"] = 1
        elif set == "Cacciatore di bestie" and proc_ok(num, set, "turno", "previsione_attacco"):
            text += f"__{nome1} prevede l'azione del suo avversario!__\n"
            agi += proc_val(set, "turno", "previsione_attacco", "agi")
        elif set == "Ice and fire" and proc_ok(num, set, "turno", "calore"):
            text += f"__{nome1} scalda l'ambiente circostante!__\n"
            main["atk"] += proc_val(set, "turno", "calore", "atk")
        elif set == "Cacciatore di uomini" and proc_ok(num, set, "turno", "trappola"):
            text += f"__{nome2} cade in una trappola per orsi, non è un buon momento per lui__\n"
            oppo["agi"] += proc_val(set, "turno", "trappola", "agi_target")
    
    if anello != None:
        num = random.random()
        if anello == "Un frammento del potere" and anello_ok(num, anello, "turno", "attacco"):
            anello = anello_val(anello, "turno", "attacco", "trasforma_in")
            text += f"**POTERE ILLIMITAAAAATO**\n"
        elif anello == "Aura pessima":
            difesan *= anello_val(anello, "turno", "aura", "moltiplicatore_difesa_target")
        elif (
            (
                (anello == "Effige della tribe" or anello in anello_val("Effige della tribe", "turno", "cura_spettrale", "equivalenti", []))
                and anello_ok(num, "Effige della tribe", "turno", "cura_spettrale")
                and main["hp"] <= anello_val("Effige della tribe", "turno", "cura_spettrale", "hp_max")
            )
            or (
                main["Nome"] in anello_val("Effige della tribe", "turno", "cura_spettrale", "speciali", {})
                and num < (anello_val("Effige della tribe", "turno", "cura_spettrale", "speciali")[main["Nome"]]["proc"] / 100)
                and main["hp"] <= anello_val("Effige della tribe", "turno", "cura_spettrale", "speciali")[main["Nome"]]["hp_max"]
            )
        ):
            cura = round(round((main["hp"] * anello_val("Effige della tribe", "turno", "cura_spettrale", "cura_percento_hp")) / 100) * bonus )
            main["hp"] += cura
            text += f"__Antichi fantasmi aiutano {nome1} a rimettersi di {cura} punti vita ⚜️__\n"
        elif anello == "Fanghiglia della palude" and main["hp"] >= anello_val(anello, "turno", "fango", "hp_min") and anello_ok(num, anello, "turno", "fango"):
            if setN == "Ombra silenziosa" and proc_ok(num, setN, "turno", "silenzio_fanghiglia"):

                        text += "(Silenziato)\n"
            else:
                        main["atk"] += round(anello_val(anello, "turno", "fango", "atk") * bonus) 
                        main["def"] += round(anello_val(anello, "turno", "fango", "def") * bonus) 

                        main["hp"] += anello_val(anello, "turno", "fango", "hp")

                        text += f"**{nome1} viene ricoperto di fango e diventa mostruoso!**\n"
        elif anello == "Elsa vitale" and anello_ok(num, anello, "turno", "crescita"):
            if setN == "Ombra silenziosa" and proc_ok(num, setN, "turno", "silenzio_elsa"):

                        text += "(Silenziato)\n"
            else:
                vita = main["hp"]
                dis = round(round((vita / anello_val(anello, "turno", "crescita", "hp_divisore"))) * bonus)
                dps += dis
                agi += dis / anello_val(anello, "turno", "crescita", "agi_divisore")
                text += f"**{nome1} diventa ancora più grosso!**\n"
        
        elif anello == "Veleno del folle" or set == "Cultista pazzo":            
            if set == "Cultista pazzo":
                cfg_cultista = proc_cfg(set, "turno", "veleno_folle")
                proc_positivo = proc_ok(num, set, "turno", "veleno_folle")
                bonus_dps = cfg_cultista["bonus_dps"]
                malus_dps = cfg_cultista["malus_dps"]
            else:
                cfg_veleno = anello_cfg("Veleno del folle", "turno", "veleno")
                proc_positivo = anello_ok(num, "Veleno del folle", "turno", "veleno")
                bonus_dps = cfg_veleno["bonus_dps"]
                malus_dps = cfg_veleno["malus_dps"]

            if proc_positivo:
                dps += round(bonus_dps * bonus)
                text += f"**OgGi {nome1} eSpLoDe dI ViTa!**\n"
            else:
                dps -= round(malus_dps * bonus)
                text += f"**OgGi {nome1} sI SeNtE UnO ScHiFo aSsUrDo!**\n"
        
        elif anello == "Guanto del falco" and anello_ok(num, anello, "turno", "falcon_punch"):
            text += "**Falcon punch!**\n"
            difesan = anello_val(anello, "turno", "falcon_punch", "difesa_base") - inte     
        elif (anello == "Campanellina concentrante" or main["Nome"] in anello_val("Campanellina concentrante", "turno", "concentrazione", "nomi_equivalenti", [])) and anello_ok(num, "Campanellina concentrante", "turno", "concentrazione"):
            text += "🎯 "
            agi += anello_val("Campanellina concentrante", "turno", "concentrazione", "agi")
        elif  anello == "Roccia viva" and anello_ok(num, anello, "turno", "golem"):
            text += f"**{nome1} col potere dell'anello genera un golem di sabbia...**\n"
            dps =round((main["def"] + anello_val(anello, "turno", "golem", "bonus_def")) * bonus)
        elif  anello == "Vincastro" and anello_ok(num, anello, "turno", "attacco"):
            if setN == "Ombra silenziosa" and proc_ok(num, setN, "turno", "silenzio_vincastro"):

                        text += "(Silenziato)\n"
            else:
                difesan = anello_val(anello, "turno", "attacco", "difesa_base") - inte
                text += f"**{nome2} grazie ad un potere mistico inizia a beeeeeelare...**\n"
        elif anello == "Proteina brullicanti" and anello_ok(num, anello, "turno", "massa"):
            text += f"**{nome1} raddoppia la sua massa pronto a colpire l'avversario!**\n"
            dps += dps * anello_val(anello, "turno", "massa", "moltiplicatore_extra_dps")
        elif (anellon == "Corna da toro" or oppo["Nome"] in anello_val("Corna da toro", "turno", "terrore", "nomi_equivalenti", [])) and anello_ok(num, "Corna da toro", "turno", "terrore"):
            vitan = oppo["hp"]
            rid = round(vitan / anello_val("Corna da toro", "turno", "terrore", "hp_divisore"))
            if set == "Ombra silenziosa" and proc_ok(num, set, "turno", "silenzio_corna"):
                text += "(Silenziato)\n"
            else:
                dps -= round(rid * bonusn)
                agi -= rid / anello_val("Corna da toro", "turno", "terrore", "agi_divisore")
                text += f"__{nome1} è terrorizzato da {nome2}!__\n"
        elif anello == "Corteccia naturale" and anello_ok(num, anello, "turno", "crescita"):
            main["atk"] += anello_val(anello, "turno", "crescita", "atk_base") + inte
            main["def"] += anello_val(anello, "turno", "crescita", "def_base") + inte
            main["agi"] += anello_val(anello, "turno", "crescita", "agi")
            text += f"__{nome1} cresce!__\n"
        elif anello == "Muschio Selvaggio" and anello_ok(num, anello, "turno", "selvaggio") and not any(
            main[stat] > limite for stat, limite in anello_val(anello, "turno", "selvaggio", "limiti_stat").items()
        ):
            boost(main, Approcci)
            text += f"**{nome1} diventa selvaggio!**\n"
        elif anello == "Pozione di furia" and anello_ok(num, anello, "turno", "furia"):
            text += f"**L'attacco di {nome1} sale in maniera esponenziale!**\n"
            main["atk"] += (anello_val(anello, "turno", "furia", "atk_base") + inte)
        elif anello == "Cinta del comandante" and anello_ok(num, anello, "turno", "comando"):
            text += f"__L'attacco di {nome2} cala!__\n"
            oppo["atk"] -= (anello_val(anello, "turno", "comando", "atk_target_base") + inte)
        elif anellon == "Vincastro" and anello_ok(num, anellon, "turno", "difesa"):
            text += f"__{nome1} grazie ad un potere mistico inizia a beeeeeelare...__\n"
            dps = anello_val(anellon, "turno", "difesa", "dps")
        elif (anellon == "Fantasmino luminoso" or nome2 in anello_val("Fantasmino luminoso", "turno", "debuff", "nomi_equivalenti", [])) and anello_ok(num, "Fantasmino luminoso", "turno", "debuff"):
            main["agi"] += anello_val("Fantasmino luminoso", "turno", "debuff", "agi")
            main["def"] += anello_val("Fantasmino luminoso", "turno", "debuff", "def_base") - inten
            main["atk"] += anello_val("Fantasmino luminoso", "turno", "debuff", "atk_base") - inten
            text += f"__{nome1} si sente stanco ed inconcludente...__\n"
        elif anellon == "Ali di luminite" and anello_ok(num, anellon, "turno", "volo"):
            if set == "Ombra silenziosa" and proc_ok(num, set, "turno", "silenzio_ali"):
                    text += "(Silenziato)\n"
            else:

                    agin += anello_val(anellon, "turno", "volo", "agi_difesa")
                    text += f"__{nome2} grazie al potere dell'anello riesce a spiccare il volo!__\n"



    if setN != None:
        num = random.random()
        if setN == "MusicoSciamano":
            set = "MusicoSciamano"
        elif setN == "Cacciatore della feccia" and oppo["fatto"] <= proc_val(setN, "turno", "difesa_sotto_soglia", "fatto_max"):
            agin += proc_val(setN, "turno", "difesa_sotto_soglia", "agi_difesa")
            difesan += proc_val(setN, "turno", "difesa_sotto_soglia", "def_difesa")
        elif setN == "Elfo silvano":
            dogebonus += proc_val(setN, "turno", "evasione", "dogebonus")
        elif setN == "Uomo di classe" and proc_ok(num, setN, "turno", "spumeggiante_difesa"):
            text += "**Spumeggiante!**\n"
            difesan = main["def"]
        elif setN == "Contrabbandiere" and proc_ok(num, setN, "turno", "piazza_carica"):
            text += "**Carica piazzzata!**\n"
            try:
                main["carica"] += proc_val(setN, "turno", "piazza_carica", "cariche")
            except:
                main["carica"] = proc_val(setN, "turno", "piazza_carica", "cariche")
        elif setN == "Portatore di morte" and proc_ok(num, setN, "turno", "debuff_difesa"):
            if set == "Ombra silenziosa" and proc_ok(num, set, "turno", "silenzio_portatore"):
                text += "(Silenziato)\n"   
            else:
                main["agi"] += proc_val(setN, "turno", "debuff_difesa", "agi")
                main["def"] += proc_val(setN, "turno", "debuff_difesa", "def")
                main["atk"] += proc_val(setN, "turno", "debuff_difesa", "atk")
                text += f"__{nome1} si sente stanco ed inconcludente...__\n"
        elif setN == "Forma terra" and proc_ok(num, setN, "turno", "chip_difesa"):
            text += "__Chip terra, attivazione!__\n"
            dps += proc_val(setN, "turno", "chip_difesa", "dps")
        elif setN == "Forma lunare" and proc_ok(num, setN, "turno", "chip_difesa"):
            text += "__Chip lunare, attivazione!__\n"
            main["agi"] += proc_val(setN, "turno", "chip_difesa", "agi_nemico")
            oppo["agi"] += proc_val(setN, "turno", "chip_difesa", "agi_propria")
        elif setN == "Regina golgari" and proc_ok(num, setN, "turno", "pietrifica"):
            text += f"{nome2} pietrifica un poco {nome1}\n"
            main["def"] += proc_val(setN, "turno", "pietrifica", "def_main")
            main["atk"] += proc_val(setN, "turno", "pietrifica", "atk_main")
            main["agi"] += proc_val(setN, "turno", "pietrifica", "agi_main")
        elif setN == "Vigilante" and proc_ok(num, setN, "turno", "cambio_proiettili_difesa"):
            old = main["atk"]
            main["atk"] = main["def"]
            main["def"] = old
            text += f"__{nome1} cambia proiettili__\n"
        elif setN == "Cacciatore di bestie" and proc_ok(num, setN, "turno", "previsione_difesa"):
            text += f"__{nome2} prevede l'azione del suo avversario!__\n"
            agin += proc_val(setN, "turno", "previsione_difesa", "agi")
        elif setN == "Ice and fire" and proc_ok(num, setN, "turno", "gelo"):
            text += f"__{nome2} congela l'ambiente circostante!__\n"
            oppo["def"] += proc_val(setN, "turno", "gelo", "def")
        
    if anellon != None:
        num = random.random()
        if anellon == "Un frammento del potere" and anello_ok(num, anellon, "turno", "difesa"):
            anello = anello_val(anellon, "turno", "difesa", "trasforma_in")
            text += f"**POTERE ILLIMITAAAAATO**\n"
        elif anellon == "Amuleto del protettore" and anello_ok(num, anellon, "turno", "protezione"):
            text += f"**{nome2} raddoppia la sua massa pronto a difendere!**\n"
            difesan += round(difesan * bonusn * anello_val(anellon, "turno", "protezione", "moltiplicatore_bonus"))
        elif anellon == "Guanto titanico" and anello_ok(num, anellon, "turno", "difesa"):
            text += "**Ottima difesa!**\n"
            dps = anello_val(anellon, "turno", "difesa", "dps_base") - inten
        elif anellon == "Stemma della rocca" and anello_ok(num, anellon, "turno", "rocca"):
            text += f"__La difesa di {nome2} aumenta!__\n"
            oppo["def"] += (anello_val(anellon, "turno", "rocca", "def_base") + inten)
    
    if main["incantamenti"] != []:
        num = random.random()
        if 'Urlo di drago' in main["incantamenti"] and incantesimo_ok(num, "Urlo di drago", "turno", "terrore"):
            text += "ROAAR!\n"
            oppo["terrore"] = True      
            num = random.random()  
        if "Mimico" in main["incantamenti"] and incantesimo_val("Mimico", "turno", "copia", "attivo", True):
            main["incantamenti"] = oppo["incantamenti"]
            text += f"\n**{nome1} copia gli incantamenti di {nome2}!**\n"
            num = random.random()
        if 'Legaccio' in main["incantamenti"] and incantesimo_ok(num, "Legaccio", "turno", "lega"):
            oppo["agi"] = oppo["agi"] * incantesimo_val("Legaccio", "turno", "lega", "agi_target_mul")
            text += f"🎋"
            num = random.random()
        if "Affilatezza" in main["incantamenti"] and incantesimo_ok(num, "Affilatezza", "turno", "affila"):
            text += "⚔\n"
            main["atk"] = main["atk"] * incantesimo_val("Affilatezza", "turno", "affila", "atk_mul")
            num = random.random()
        if "Legione" in main["incantamenti"] and "Legione" in oppo["incantamenti"]:
            dps = dps * incantesimo_val("Legione", "turno", "duello_legione", "dps_mul")
        
        if "Ingrossamento" in main["incantamenti"] and incantesimo_ok(num, "Ingrossamento", "turno", "crescita"):
                main["atk"] += random.randint(incantesimo_val("Ingrossamento", "turno", "crescita", "atk_min"), incantesimo_val("Ingrossamento", "turno", "crescita", "atk_max"))
                main["agi"] += random.randint(incantesimo_val("Ingrossamento", "turno", "crescita", "agi_min"), incantesimo_val("Ingrossamento", "turno", "crescita", "agi_max"))
                text += f"**L'arma di {nome1} diventa enorme**\n"  
                num = random.random()
                          
        if "Icore" in main["incantamenti"] and incantesimo_ok(num, "Icore", "turno", "penetrazione"):
            difesan = difesan * incantesimo_val("Icore", "turno", "penetrazione", "difesa_target_mul")
            text += "🟡"

    if oppo["incantamenti"] != []:
        num = random.random()
        if "Predominio" in oppo["incantamenti"] and main["hp"] <= oppo["hp"]:
            dps = dps * incantesimo_val("Predominio", "turno", "difesa", "dps_attaccante_mul")
            agi += incantesimo_val("Predominio", "turno", "difesa", "agi_attaccante")  
               
        if "Duraturo" in oppo["incantamenti"] and incantesimo_ok(num, "Duraturo", "turno", "difesa"):
            difesan = difesan * incantesimo_val("Duraturo", "turno", "difesa", "difesa_mul")
            text += "🛡"
            num = random.random()
        if "Multiplo" in oppo["incantamenti"] and incantesimo_ok(num, "Multiplo", "turno", "difesa"):
            agin += incantesimo_val("Multiplo", "turno", "difesa", "agi")
            text += f"💪"
    
    if setN == "Esperto di animali" and oppo["Ap"] == "Fantamsa del ritorno" and proc_ok(num, setN, "turno", "fantasma_ritorno"):
            text += f"Il Fantamsa del ritorno spaventa {nome1}"
            dps *= proc_val(setN, "turno", "fantasma_ritorno", "dps_mul")
    if set == "Esperto di animali" and main["Ap"] == "Dragone delle stelle" and proc_ok(num, set, "turno", "dragone_stelle"):
            text += f"Il Dragone delle stelle colpisce con {nome1}"
            dps *= proc_val(set, "turno", "dragone_stelle", "dps_mul")
    
    possibile = possibiles(agin, agi)
    possibile += dogebonus


    if possibile > random.randint(0, 100):
        text += f"{nome2} schiva il colpo di {nome1}\n"
        oppo["schivato"] = True
        if anello == "Coda demoniaca":
            oppo["lastD"] = anello_val(anello, "turno", "schivata", "lastD_reset")
        mod = 0
        danno = 0
    
    else:
        oppo["schivato"] = False
        num = random.random()
        mod = random.uniform(0.8, 1.2)
        if main["schivato"] == True:
            mod *= 1.3
            if anellon == "Testuggine del vecchio saggio":
                mod *= anello_val(anellon, "turno", "atterraggio", "moltiplicatore_mod")
            if set == "Ricercatore del pericolo" and proc_ok(num, set, "turno", "contrattacco_schivata"):
                mod += proc_val(set, "turno", "contrattacco_schivata", "mod")
                text += "🩸 "
                num = random.random()
            if setN == "Guerriero 3D":
                mod += proc_val(setN, "turno", "atterraggio", "mod_delta")
                text += "💧 "
            if anello == "Fascette luminose" and anello_ok(num, anello, "turno", "atterraggio"):
                mod += anello_val(anello, "turno", "atterraggio", "mod")
                text += "✨ "               
                
            text += "Riatterrando dalla schivata infligge danno extra!\n"
        
        if (
            (anello == "Compasso" and anello_ok(num, anello, "turno", "bilanciamento"))
            or (anellon == "Bilanciere" and anello_ok(num, anellon, "turno", "bilanciamento"))
            or (anello == "Bilanciere" and anello_ok(num, anello, "turno", "bilanciamento"))
        ):
            text += "⚖️ "
            ring_bilanciamento = anello if anello in ("Compasso", "Bilanciere") else anellon
            mod = anello_val(ring_bilanciamento, "turno", "bilanciamento", "mod")

    if set != None:
        num = random.random()
        if set == "Cavaliere d'argento" and mod <= proc_val(set, "turno", "recupero_colpo", "mod_massimo"):
            mod += proc_val(set, "turno", "recupero_colpo", "mod_bonus")
        elif set == "Spacca Mostri":
            dps += oppo["hp"] / proc_val(set, "turno", "mostro_enorme", "hp_divisore")
        elif set == "IppoFan" and proc_ok(num, set, "turno", "copia_attacco"):
            dps = oppo["atk"]
            text += f"__{nome1} copia l'attacco nemico per attaccare!__\n" 
        elif set == "Maledetto" and proc_ok(num, set, "turno", "maledizione"):
            cura = round((proc_val(set, "turno", "maledizione", "hp_riferimento") - main["hp"]))
            if cura <= 0:
                cura = proc_val(set, "turno", "maledizione", "danno_min")
            dps += cura
            text += f"**La maledizione di {nome1} si riperquote sull'avversario!**\n"

        elif set == "Campione del sole":
                if "mol" in main:
                    main["mol"] += 1
                else:
                    main["mol"] = 1
                
                cfg = proc_cfg(set, "turno", "colpo_caricato")
                if (main["hp"] <= cfg["hp_trigger"] and main["mol"] >= cfg["mol_min_hp"]) or (main["mol"] > cfg["mol_min_fallback"] and num > (1 - cfg["proc_fallback"] / 100)):
                    
                    dps = dps * (main["mol"] * cfg["moltiplicatore"])
                    
                    main["mol"] = 0
                    
                    text += "**Colpo caricato!**\n"
    
    if setN != None:
        num = random.random()
        if setN == "Proiettile":
            mod += proc_val(setN, "turno", "difesa", "mod_delta")
        elif setN == "Macellaio":
            difesan += oppo["hp"] // proc_val(setN, "turno", "difesa_sangue", "hp_divisore")
        elif setN == "Segna ombre" and proc_ok(num, setN, "turno", "mimica_difesa"):
            difesan = main["def"]
            text += f"__{nome2} mimica la difesa avversaria!__\n"
        elif setN == "Drago" and proc_ok(num, setN, "turno", "scaglie"):
                    mod -= proc_val(setN, "turno", "scaglie", "riduzione_mod")
                    text += "__Danni ridotti dalle scaglie!__\n"
                    if num < (proc_val(setN, "turno", "scaglie", "proc_rottura_arma") / 100):
                        text += "__L'arma dell'avversario si rovina!__\n"
                        main["atk"] += proc_val(setN, "turno", "scaglie", "atk_target")
        
        elif setN == "Anima oscura" and proc_ok(num, setN, "turno", "parry"):
                    text += f"**{nome2} effettua un parry a {nome1}!**\n"
                    mod = 0
                    oppo["atk"] = oppo["atk"] * proc_val(setN, "turno", "parry", "moltiplicatore_atk")
        elif setN == "Abitante" and proc_ok(num, setN, "turno", "radice"):
                    text += f"**{nome2} pianta al volo la radice vitale, che crescendo blocca {nome1}!**\n"
                    mod = 0
                    oppo["def"] = oppo["def"] * proc_val(setN, "turno", "radice", "moltiplicatore_def")
        elif setN == 'Gangster' and proc_ok(num, setN, "turno", "lega"):
            text += f"{nome1} rimane legato a testa in giù!\n\n"
            main["bloccato"] = True



    if mod <= 0:
        mod = 0
    if difesan < 0:
        dps -= difesan
        difesan = 0
    danno = random.uniform(
                dps * (100 / ((100 + difesan * 1.5)+1)), dps * (100 / ((100 + difesan)+1))
            )

    if danno <= 20:
        danno = 20
    
    if main["incantamenti"] != []:
        if 'Primo impatto' in main["incantamenti"]:
                main["incantamenti"].remove('Primo impatto')
                danno = round(danno * incantesimo_val("Primo impatto", "turno", "primo_colpo", "danno_mul"))
                text += "💥\n"
                try:
                    main["incantamenti"].remove('Primo impatto')
                except:
                    pass
            
        if 'Critico' in main["incantamenti"] and incantesimo_ok(num, "Critico", "turno", "critico"):
                text += "\n**Critico!**\n"
                danno = round(danno * incantesimo_val("Critico", "turno", "critico", "danno_mul"))

        if "Velenoso" in main["incantamenti"] and incantesimo_ok(num, "Velenoso", "turno", "veleno"):
            try:
                oppo["veleno"] += incantesimo_val("Velenoso", "turno", "veleno", "stack")
            except:
                oppo["veleno"] = incantesimo_val("Velenoso", "turno", "veleno", "stack")
            text += "🟢**Colpo velenoso!**\n"

    if setN != None:
        num = random.random()
        if setN == "Marines" and proc_ok(num, setN, "turno", "armatura"):
            text += (
                        f"__La spessa armatura di {nome2} riduce il danno subito!__\n"
                    )
            danno = round(danno - ((danno * proc_val(setN, "turno", "armatura", "riduzione_danno_percento")) / 100))
            if danno <= 0:
                danno = 1   
        elif setN == "Illusionista" and proc_ok(num, setN, "turno", "copie_difesa"):
            num = random.random()
            text += f"__{nome2} evoca delle copie di se stesso!__\n"
            if num < (proc_val(setN, "turno", "copie_difesa", "proc_originale") / 100):
                text += f"{nome1} colpisce però l'originale!\n"
            else:
                text += f"**{nome1} sbaglia bersaglio!**\n"
                danno = 0
                mod = 0
    
    if set != None:
        num = random.random()
        if set == "Betatester" and proc_ok(num, set, "turno", "spada_beta"):
            danno += proc_val(set, "turno", "spada_beta", "danno")
            text += f"**La Spada della beta si illumina di potere!**\n"

    if anellon != None:
        num = random.random()
        if anellon == "Pegno di amicizia":
            danno = danno * anello_val(anellon, "turno", "difesa", "moltiplicatore_danno")
            if anello_val(anellon, "turno", "difesa", "sottrai_int"):
                danno -= inten
        elif anellon == "Tasto B" and anello_ok(num, anellon, "turno", "roll"):
            text += f"__Roll...__\n"
            mod = anello_val(anellon, "turno", "roll", "mod") 
        elif anellon == "Tasto X" and anello_ok(num, anellon, "turno", "obliteratore"):
            text += f"**{nome2} rilascia un obliteratore che blocca in parte {nome1}!**\n"
            mod = mod / anello_val(anellon, "turno", "obliteratore", "divisore_mod")
            bonus_tasto_x = anello_val(anellon, "turno", "obliteratore", "bonus_stat_base") + inten
            oppo["atk"] += bonus_tasto_x
            oppo["def"] += bonus_tasto_x
        elif anellon == "Scudiero fidato" and anello_ok(num, anellon, "turno", "blocco"):
            text += f"**L'anello di {nome2} blocca il danno!**\n"
            danno = anello_val(anellon, "turno", "blocco", "danno")
        elif anellon == "Aureola" and anello_ok(num, anellon, "turno", "salvezza"):
            text += f"__Una luce dall'alto salva {nome2} da diversi danni!__\n"
            danno = round(danno * anello_val(anellon, "turno", "salvezza", "moltiplicatore_danno")) - inten
            if danno <= 0:
                danno = anello_val(anellon, "turno", "salvezza", "danno_min")
        elif anellon == "Coda demoniaca" and "lastD" in main:
            percento = (main["lastD"] * bonus) / anello_val(anellon, "turno", "dolore", "divisore_chance")

            if nome2 == anello_val(anellon, "turno", "dolore", "nome_speciale"):
                        percento += anello_val(anellon, "turno", "dolore", "bonus_speciale")

            if percento > num:
                        danno = anello_val(anellon, "turno", "dolore", "danno")
                        mod = anello_val(anellon, "turno", "dolore", "mod")
                        text += f"__A causa del dolore {nome1} non riesce a colpire e si blocca a metà__\n"
        elif (anellon == "Ricordo straziante" and anello_ok(num, anellon, "turno", "intangibile")) or nome2 in anello_val("Ricordo straziante", "turno", "intangibile", "nomi_equivalenti", []):
            danno = anello_val("Ricordo straziante", "turno", "intangibile", "danno")
            mod = anello_val("Ricordo straziante", "turno", "intangibile", "mod")
            text += f"__{nome2} non è colpibile!__\n"
            oppo["schivato"] = True


    if anello != None:
        num = random.random()
        if anello == "Spuntoni" and anello_ok(num, anello, "turno", "danno_extra"):
            text += "__Danni extra da spuntoni!__\n"
            mod += anello_val(anello, "turno", "danno_extra", "mod")
    
    
    if "Minimista" in main["incantamenti"] and mod <= 0:
        mod = incantesimo_val("Minimista", "turno", "danno_minimo", "mod_min")
        text += "+"
        if danno <= 0:
            danno = incantesimo_val("Minimista", "turno", "danno_minimo", "danno_base_min")
            text += "+"
    
    
    dannov = round(danno * mod)
    main["fatto"] += dannov
    if setN == 'Spadaccino Musashi':
                danno = danno * proc_val(setN, "turno", "riduzione_danno", "danno_mul")
    if anello == "Coda demoniaca":
        oppo["lastD"] = dannov
    
    if "terrore"in main:
                text += f"{nome1} è terrorizzato!\n"
                main.pop("terrore")
    elif "bloccato" in main:
                text += f"{nome1} è bloccato, le corde lo danneggiano!\n"
                main["hp"] -= 10
                main.pop("bloccato")
                danno = 0
                mod = 0
                dannov = 0
    elif main["set"] == 'Avventuriero delle praterie' and proc_ok(1 - num, main["set"], "turno", "respira"):
                text += f"Respira {nome1}, sta andando bene!\n"
                main["atk"] += proc_val(main["set"], "turno", "respira", "atk")
                main["def"] += proc_val(main["set"], "turno", "respira", "def")
                main["agi"] += proc_val(main["set"], "turno", "respira", "agi")
                danno = 0
                mod = 0
                dannov = 0
    else:
        if mod == 0 or danno == 0 or dannov == 0:
            pass
        else:
            num = random.random()
            if setN == "Paladino" and oppo["Scudo"] >= 0:

                    oppo["Scudo"] -= round(float(danno) * (mod + proc_val(setN, "turno", "scudo", "mod_bonus")))
                    vita = oppo["Scudo"]
                    text += f"{nome1} infligge {dannov} danno allo scudo di {nome2} ({vita} scudo)!\n"
                    if oppo["Scudo"] <= 0:
                        text += "**Lo scudo si è rotto!**\n"
            else:
                    oppo["hp"] -= round(float(danno) * mod)
                    vita = oppo["hp"]
                    dannov = round(danno * mod)
                    text += f"{nome1} infligge {dannov} danni a {nome2} ({vita})!\n"

            if set == "Shogun moderno":

                    if proc_ok(num, set, "turno", "doppio_colpo"):
                        text += "**Doppio colpo**\n"
                        if setN == "Paladino" and oppo["Scudo"] >= 0:

                            oppo["Scudo"] -= round(float(danno) * random.uniform(proc_val(set, "turno", "doppio_colpo", "moltiplicatore_min"), proc_val(set, "turno", "doppio_colpo", "moltiplicatore_max")))
                            vita = oppo["Scudo"]
                            text += f"{nome1} infligge {dannov} danno allo scudo di {nome2} ({vita} scudo)!\n"
                            if oppo["Scudo"] <= 0:
                                text += "**Lo scudo si è rotto!**\n"
                        else:
                            new_m = random.uniform(proc_val(set, "turno", "doppio_colpo", "moltiplicatore_min"), proc_val(set, "turno", "doppio_colpo", "moltiplicatore_max"))
                            oppo["hp"] -= round(float(danno) * new_m)
                            vita = oppo["hp"]
                            dannov = round(danno * new_m)
                            text += f"{nome1} infligge {dannov} danni a {nome2} ({vita})!\n"

            if set == "Manipolatore di morte" and proc_ok(num, set, "turno", "scheletri"):
                    text += f"\n**{nome1} evoca una marea di scheletri ad attaccare!**\n"
                    scheletri = cura = round((proc_val(set, "turno", "scheletri", "hp_riferimento") - main["hp"]) / proc_val(set, "turno", "scheletri", "hp_per_scheletro"))
                    new_m = mod
                    for x in range(scheletri):

                        if setN == "Paladino" and oppo["Scudo"] >= 0:

                            new_m = random.uniform(proc_val(set, "turno", "scheletri", "mod_min"), proc_val(set, "turno", "scheletri", "mod_max"))
                            oppo["Scudo"] -= round(float(danno) * new_m)

                            vita = oppo["Scudo"]
                            text += f"Uno scheletrino infligge {dannov} danno allo scudo di {nome2} ({vita} scudo)!\n"
                            if oppo["Scudo"] <= 0:
                                text += "**Lo scudo si è rotto!**\n"
                            danno += proc_val(set, "turno", "scheletri", "crescita_danno_scudo")
                        else:
                            new_m = random.uniform(proc_val(set, "turno", "scheletri", "mod_min"), proc_val(set, "turno", "scheletri", "mod_max"))
                            oppo["hp"] -= round(float(danno) * new_m)

                            vita = oppo["hp"]
                            dannov = round(danno * new_m)
                            text += f"Uno scheletrino infligge {dannov} danni a {nome2} ({vita})!\n"
                            danno += proc_val(set, "turno", "scheletri", "crescita_danno_hp")

                    danno = round(float(danno) * new_m)
    
    num = random.random()
    if set == "Mago mentale" and proc_ok(num, set, "turno", "showtime"):
                text += "**ShowTime!**\n\n"
                for x in range(random.randint(proc_val(set, "turno", "showtime", "colpi_min"), proc_val(set, "turno", "showtime", "colpi_max"))):
                    new_m = random.uniform(proc_val(set, "turno", "showtime", "mod_min"), proc_val(set, "turno", "showtime", "mod_max"))
                    oppo["hp"] -= round(float(danno) * new_m)
                    if num < (proc_val(set, "turno", "showtime", "autodanno_proc") / 100):
                        meg = random.choice(
                            [
                                "Forse sbaglio",
                                "Non ce la farò mai",
                                "E' destino perdere",
                            ]
                        )
                        text += f"__{meg}__\n"
                        main["hp"] -= round((danno * new_m))
                    vita = oppo["hp"]
                    dannov = round(danno * new_m)
                    frase = random.choice(
                        [
                            f"Non credo valga la pena neanche combatterti ({vita})!\n",
                            f"Meglio arrendersi ({vita})!\n",
                            f"Forse il peggiore qui sei tu? ({vita})!\n",
                            f"Hai la minima idea di chi sono? ({vita})!\n",
                            f"Forse il problema qui sei tu? ({vita})!\n",
                            f"Che ne dici di arrenderti? ({vita})!\n",
                            f"Mai visto tattica peggiore? ({vita})!\n",
                        ]
                    )
                    text += f"**{frase}**"
                    danno += proc_val(set, "turno", "showtime", "crescita_danno")
    
    if set != None:
        num = random.random()
        if set == 'Guardiano della bestie':
                main["powe"] = main.get("powe", 0) + PROC_CLASSI[set]["turno"]["powe_per_turno"]

                cfg = proc_cfg(set, "turno", "volpe")
                if main["powe"] >= cfg["powe_min"] and proc_ok(num, set, "turno", "volpe"):
                    text += "Una volpa difende la zona!\n"
                    main["def"] += cfg["def"]

                cfg = proc_cfg(set, "turno", "lupo")
                if main["powe"] >= cfg["powe_min"] and proc_ok(num, set, "turno", "lupo"):
                    text += "Una lupo si prepara a mordere!\n"
                    main["atk"] += cfg["atk"]

                cfg = proc_cfg(set, "turno", "ratti")
                if main["powe"] >= cfg["powe_min"] and proc_ok(num, set, "turno", "ratti"):
                    text += "I ratti si avvicinano!\n"
                    main["agi"] += cfg["agi"]

                cfg = proc_cfg(set, "turno", "orsi")
                if main["powe"] >= cfg["powe_min"] and proc_ok(num, set, "turno", "orsi"):
                    text += "Gli orsi si agitano!\n"
                    main["atk"] += cfg["atk"]

                cfg = proc_cfg(set, "turno", "serpenti")
                if main["powe"] >= cfg["powe_min"] and proc_ok(num, set, "turno", "serpenti"):
                    text += "I serpenti iniziano a sbucare!\n"
                    oppo["agi"] += cfg["agi_target"]

                cfg = proc_cfg(set, "turno", "presenza_lunare")
                if main["powe"] >= cfg["powe_min"] and proc_ok(num, set, "turno", "presenza_lunare"):
                    text += "La presenza lunare ti osserva!\n"
                    main["def"] = main["def"] * cfg["def_mul"]
        elif set == "Fiamma pura" and proc_ok(num, set, "turno", "arena_brucia"):
            text += "L'arena brucia!\n"
            main["hp"] -= proc_val(set, "turno", "arena_brucia", "danno_main")
            oppo["hp"] -= proc_val(set, "turno", "arena_brucia", "danno_oppo")
        
        elif set == "Crociato" and proc_ok(num, set, "turno", "punizione_schivata"):
                if "schiva il colpo" in text:
                    danni = round(dps / proc_val(set, "turno", "punizione_schivata", "divisore_dps") * random.uniform(proc_val(set, "turno", "punizione_schivata", "random_min"), proc_val(set, "turno", "punizione_schivata", "random_max")))
                    if danni <= proc_val(set, "turno", "punizione_schivata", "danno_min"):
                        danni = proc_val(set, "turno", "punizione_schivata", "danno_min")
                    oppo["hp"] -= danni
                    text += f"**Lo spirito della luce punisce {nome2}, obbligandolo a subire {danni} danni!**"
        
        elif set == "Assassino delle ombre" or setN == "Assassino delle ombre":
            danno = 0
            dannov = 0
        
        elif set == "Medico improvvisato" and proc_ok(num, set, "turno", "cura_schivata"):
                if "schiva il colpo" in text:
                    danni = round(dps / proc_val(set, "turno", "cura_schivata", "divisore_dps") * random.uniform(proc_val(set, "turno", "cura_schivata", "random_min"), proc_val(set, "turno", "cura_schivata", "random_max")))

                    main["hp"] += danni
                    text += f"__Dato il mancato colpo il totem di {nome1} lo cura di {danni} hp!__\n"
        
        elif set == "Vampiro" and proc_ok(num, set, "turno", "morso"):
                if "schiva il colpo" not in text:
                    hp = round(((float(danno) + oppo["hp"]) * mod) / proc_val(set, "turno", "morso", "divisore"))
                    if hp >= proc_val(set, "turno", "morso", "cap_trigger"):
                        hp = proc_val(set, "turno", "morso", "cura_cap")
                    main["hp"] += hp
                    text += f"__{nome1} morde l'avversario durante il colpo per recuperare {hp} hp!!__\n"
                    
        elif set == "Guaritore da campo" and proc_ok(num, set, "turno", "rinsana"):
                if "schiva il colpo" not in text:
                    hp = round((float(danno) * mod) / proc_val(set, "turno", "rinsana", "divisore"))
                    main["hp"] += hp
                    text += f"__{nome1} rinsana di {hp} punti vita__\n"

                
        
        elif set == "Cacciatore" and proc_ok(num, set, "turno", "junior"):
                danni = round(float(dps) * (100 / (proc_val(set, "turno", "junior", "denominatore") + float(1 + difesan)) * proc_val(set, "turno", "junior", "moltiplicatore")))

                text += f"**{nome2} viene morso da Junior, subendo {danni} danni!**\n"
                oppo["hp"] -= danni
        
        elif set == "Orrido" and proc_ok(num, set, "turno", "sgignolo"):
                danni = round(float(dps) * (100 / (proc_val(set, "turno", "sgignolo", "denominatore") + float(1 + difesan)) * proc_val(set, "turno", "sgignolo", "moltiplicatore")))

                text += f"**{nome1} non riesce a tener fermo Sgignolo, infliggendo a {nome2} {danni} danni!**\n"
                oppo["hp"] -= danni
        
        elif set == "Pazzoide glamour" and proc_ok(num, set, "turno", "pazzia"):
            if setN == "Ombra silenziosa" and proc_ok(num, setN, "turno", "silenzio_pazzoide"):
                    text += "(Silenziato)\n"
            else:
                    if "schiva il colpo" not in text:
                        hp = round((float(danno) * mod))
                        main["hp"] += hp
                        testo = random.choice(
                            [
                                "__HAHAHAH__\n",
                                "__ADOOOROH__\n",
                                "__ANCORA__\n",
                                "__DI PIU'__\n",
                            ]
                        )
                        text += testo
                    
        
        elif set == "Primo alla bandiera":

            if proc_ok(num, set, "turno", "colpito"):
                if "schiva il colpo" not in text:
               
                    hp = round((float(danno) * mod) / proc_val(set, "turno", "colpito", "divisore_bonus"))
                    main["hp"] += round(danno / proc_val(set, "turno", "colpito", "cura_divisore"))
                    main["atk"] += hp
                    main["def"] += hp

                    text += f"__HAHAHAHA COLPITO!!__\n"
                
        
        elif set == "Difensore delle mareggiate" and proc_ok(num, set, "turno", "fauna"):
                num = random.random()
                cfg = proc_cfg(set, "turno", "fauna")
                if num < (cfg["soglia_sogliola"] / 100):
                    dannissimi = round(
                        float(dps)
                        * (100 / (50 + float(1 + difesan)) * random.uniform(cfg["sogliola_min"], cfg["sogliola_max"]))
                    )
                    oppo["hp"] -= dannissimi
                    text += f"**Una sogliola colpisce {nome2} infliggendo {dannissimi} danni!**\n"
                elif num < (cfg["soglia_scorpione"] / 100):
                    dannissimi = round(
                        float(dps)
                        * (100 / (50 + float(1 + difesan)) * random.uniform(cfg["scorpione_min"], cfg["scorpione_max"]))
                    )
                    oppo["hp"] -= dannissimi
                    text += f"**Un pesce scorpione colpisce {nome2} infliggendo {dannissimi} danni!**\n"
                elif num < (cfg["soglia_spada"] / 100):
                    dannissimi = round(
                        float(dps)
                        * (100 / (50 + float(1 + difesan)) * random.uniform(cfg["spada_min"], cfg["spada_max"]))
                    )
                    oppo["hp"] -= dannissimi
                    text += f"**Un pesce spada colpisce {nome2} infliggendo {dannissimi} danni!**\n"
                else:
                    dannissimi = round(
                        float(dps)
                        * (100 / (50 + float(1 + difesan)) * random.uniform(cfg["balena_min"], cfg["balena_max"]))
                    )
                    oppo["hp"] -= dannissimi
                    text += f"**Una balena tenta di colpire {nome2}, mandando comunque a segno parte del colpo con cui infligge {dannissimi} danni!**\n"
        elif set == "Cercatore di reliquie" and proc_ok(num, set, "turno", "reliquia"):
                num = random.random()
                cfg = proc_cfg(set, "turno", "reliquia")
                if num < (cfg["soglia1"] / 100):

                    main["agi"] += cfg["agi"]
                    text += f"**Una bellissimo Tereitoscopio a terra!**\n"
                elif num < (cfg["soglia2"] / 100):

                    main["hp"] += cfg["hp"]
                    text += f"**Un incredibile nucleo rapido di cura a terra!**\n"
                elif num < (cfg["soglia3"] / 100):

                    main["def"] += cfg["def"]
                    text += f"**Un pazzesco lamillo versak a terra!**\n"
                else:

                    main["atk"] += cfg["atk"]
                    text += f"**Una possente ancora dimensionale a terra!**\n"
        elif set == "Fire lord" and proc_ok(num, set, "turno", "muori_insetto"):

                
                text += f"**MUORI INSETTO!**"
                if "Smateriabile" in oppo["incantamenti"] and incantesimo_val("Smateriabile", "interazioni", "fire_lord", "blocca", False):
                    text += "🚫"
                else:
                    oppo["hp"] -= proc_val(set, "turno", "muori_insetto", "danno")
        elif set == "Combattente 2D" and proc_ok(num, set, "turno", "evocazione"):
                num = random.random()
                cfg = proc_cfg(set, "turno", "evocazione")
                if num < (cfg["soglia_occhio"] / 100):
                    text += (
                        f"__Un occhietto di cthulhu si unisce a {nome1} nella lotta__"
                    )
                    main["atk"] += cfg["atk"]
                    main["def"] += cfg["def"]
                    main["agi"] += cfg["agi"]
                elif num < (cfg["soglia_zombie"] / 100):
                    oppo["hp"] -= cfg["danno_zombie"]
                    text += f"**Uno zombie attacca {nome2} infliggendo {cfg['danno_zombie']} danni!**"
                elif num < (cfg["soglia_raggio"] / 100):
                    dannissimi = round(
                        float(dps)
                        * (100 / (50 + float(1 + difesan)) * random.uniform(cfg["raggio_min"], cfg["raggio_max"]))
                    )
                    oppo["hp"] -= dannissimi
                    text += f"**Un raggio del distruttore di mondi colpisce {nome2} infliggendo {dannissimi} danni!**"
                else:
                    pass
        elif set == "Accolito" and main["fatto"] >= proc_val(set, "turno", "potere", "danno_fatto_min"):
                text += "**ECCOLO ECCOLO LUI E' QUI, LUI MI DA POTEEERE**\n"
                main["atk"] += proc_val(set, "turno", "potere", "atk")
                main["def"] += proc_val(set, "turno", "potere", "def")
                main["hp"] += proc_val(set, "turno", "potere", "hp")
                main["agi"] += proc_val(set, "turno", "potere", "agi")
        elif set == "Esperto di animali" and main["Ap"] == "Ratto delle tombe" and oppo["hp"] <= proc_val(set, "turno", "ratto_tombe", "hp_target_max"):
                oppo["hp"] = 0
                text += "Il Ratto delle tombe finisce il lavoro"
        elif set == "Esperto di animali" and main["Ap"] == "Balena territoriale" and proc_ok(num, set, "turno", "balena_territoriale"):
            text += f"La Balena territoriale aumenta la difesa di {nome1}"
            main["def"] += proc_val(set, "turno", "balena_territoriale", "def")
        elif set == "Esperto di animali" and main["Ap"] == "Silvantropo" and proc_ok(num, set, "turno", "silvantropo"):
            text += f"Il Silvantropo cura {nome1}"
            main["hp"] += proc_val(set, "turno", "silvantropo", "cura")
    
    if setN != None:
        num = random.random()
        if setN == "Sanguinolento" and proc_ok(num, setN, "turno", "sangue_difesa"):
            if "schiva il colpo" not in text:
                if set == "Ombra silenziosa" and proc_ok(num, set, "turno", "silenzio_sanguinolento"):

                    text += "(Silenziato)\n"
                else:

                    hp = round((float(danno) + 2) / proc_val(setN, "turno", "sangue_difesa", "divisore")) + 1
                    oppo["atk"] += hp
                    oppo["def"] += hp
                    text += (
                        f"__{nome2} unisce il proprio sangue a quello della spada!__\n"
                    )
    
        elif setN == "Accolito" and proc_ok(num, setN, "turno", "difesa_cura"):
            if "schiva il colpo" not in text:
                    hp = round((float(danno) + proc_val(setN, "turno", "difesa_cura", "base")) / proc_val(setN, "turno", "difesa_cura", "divisore"))
                    oppo["hp"] += hp
                    text += f"__{nome2} non può morire per cause così futili, si cura di {hp} hp!__\n"

            

        elif setN == "Ufficiale dell'oltretomba" and proc_ok(num, setN, "turno", "demoni_difesa"):
                if "schiva il colpo" not in text:

                    danno2 = round(dannov * random.uniform(proc_val(setN, "turno", "demoni_difesa", "random_min"), proc_val(setN, "turno", "demoni_difesa", "random_max")) * bonusn)

                    text += f"**A causa del danno inflitto {nome2} schiera demoni a colpire {nome1} anticipatamente, infliggendo {danno2} danni!**\n"
                    main["hp"] -= danno2

        elif setN == "Cercatore" and proc_ok(num, setN, "turno", "demoni_difesa"):
                if "schiva il colpo" not in text:

                    danno2 = round(dannov * random.uniform(proc_val(setN, "turno", "demoni_difesa", "random_min"), proc_val(setN, "turno", "demoni_difesa", "random_max")))

                    text += f"**{nome2} viene difeso da oscuri demoni, che infliggono {danno2} a {nome1} danni!**\n"
                    main["hp"] -= danno2

        elif setN == "Cavaliere delle spine" and proc_ok(num, setN, "turno", "spine_difesa"):
                 if "schiva il colpo" not in text:

                    danno2 = round(dannov * random.uniform(proc_val(setN, "turno", "spine_difesa", "random_min"), proc_val(setN, "turno", "spine_difesa", "random_max")))

                    text += f"**{nome1} subisce {danno2} danni da spine!**\n"
                    main["hp"] -= danno2

                
        elif setN == "Mariachi" and proc_ok(num, setN, "turno", "resurrezione_difesa") and oppo["hp"] <= 0:
                    oppo["hp"] = proc_val(setN, "turno", "resurrezione_difesa", "hp")
                    oppo["atk"] += proc_val(setN, "turno", "resurrezione_difesa", "atk")
                    oppo["def"] += proc_val(setN, "turno", "resurrezione_difesa", "def")
                    text += f"**El Dios de la Muerte, fiero di {nome2}, decide di far continuare la sua avventura, almeno un altro pochettino!**\n"

        elif setN == "Esperto di animali" and oppo["Ap"] == "OrsoDruido" and proc_ok(num, setN, "turno", "orsodruido"):
                try:

                    danno2 = round(dannov * random.uniform(proc_val(setN, "turno", "orsodruido", "random_min"), proc_val(setN, "turno", "orsodruido", "random_max")))

                    text += f"**{nome1} viene attaccato dall'oOrsoDruido, subendo {danno2} danni!**\n"
                    main["hp"] -= danno2
                except:
                    pass
    




    if anellon != None:
            num = random.random()
            
            if anellon == "Scarica di adrenalina" and anello_ok(num, anellon, "turno", "adrenalina"):
                try:
                    if set == "Ombra silenziosa" and proc_ok(num, set, "turno", "silenzio_adrenalina"):

                        text += "(Silenziato)\n"
                    else:
                        if "schiva il colpo" not in text:
                            hp = round((float(danno) + anello_val(anellon, "turno", "adrenalina", "offset_danno")) / anello_val(anellon, "turno", "adrenalina", "divisore")) + anello_val(anellon, "turno", "adrenalina", "bonus_finale")
                            oppo["atk"] += hp

                            text += f"__{nome2} sente l'adrenalina salire!__\n"
                except:
                    pass
            
            elif (anellon == "Lapsus vitale" or oppo["Nome"] in anello_val("Lapsus vitale", "turno", "cura_danno", "nomi_equivalenti", [])) and anello_ok(num, "Lapsus vitale", "turno", "cura_danno"):
                if "schiva il colpo" not in text:
                    hp = round(round((float(dannov) + anello_val("Lapsus vitale", "turno", "cura_danno", "offset_danno")) / anello_val("Lapsus vitale", "turno", "cura_danno", "divisore")) * bonusn)
                    oppo["hp"] += hp
                    text += f"__{nome2} adora subire danni, si cura di {hp} hp!__\n"
                
            
            elif anellon == "Vasetto all'orlo" and anello_ok(num, anellon, "turno", "contrattacco"):
                if "schiva il colpo" not in text:

                    danno2 = round(dannov * random.uniform(
                        anello_val(anellon, "turno", "contrattacco", "random_min"),
                        anello_val(anellon, "turno", "contrattacco", "random_max"),
                    ) * bonusn)

                    text += f"**Preso dalla rabbia {nome2} colpisce {nome1} anticipatamente, infliggendo {danno2} danni!**\n"
                    main["hp"] -= danno2

                
            elif oppo["hp"] <= 0 and ((anellon == "Chiavi dell'aldilà" and anello_ok(num, anellon, "turno", "resurrezione")) or (setN == "Guardiano del passaggio" and proc_ok(num, setN, "turno", "resurrezione"))):
                hp_base = (
                    proc_val(setN, "turno", "resurrezione", "hp_base", anello_val("Chiavi dell'aldilà", "turno", "resurrezione", "hp_base"))
                    if setN == "Guardiano del passaggio"
                    else anello_val(anellon, "turno", "resurrezione", "hp_base")
                )
                oppo["hp"] = (hp_base * bonusn)
                text += f"**La morte non vuole {nome2}, impedendogli di arrivare a lei!**\n"
            

    if anello != None:
            num = random.random()
            
            if (anello == "Benedizione sanguinolenta" or main["Nome"] in anello_val("Benedizione sanguinolenta", "turno", "cura_danno", "nomi_equivalenti", [])) and anello_ok(num, "Benedizione sanguinolenta", "turno", "cura_danno"):
                if "schiva il colpo" not in text:
                    hp = round(((float(danno) * mod) / anello_val("Benedizione sanguinolenta", "turno", "cura_danno", "divisore")) * bonus)
                    main["hp"] += hp
                    text += f"__{nome1} apprezza il danno inflitto e si cura di {hp} con esso!!__\n"
                
            elif anello == "Anello dell'occulto" and anello_ok(num, anello, "turno", "trascinamento"):
                if setN == "Ombra silenziosa" and proc_ok(num, setN, "turno", "silenzio_occulto"):
                        danni = 0
                        text += "(Silenziato)\n"
                else:
                    
                    if "schiva il colpo" in text:
                        
                        danni = round(dps / anello_val(anello, "turno", "trascinamento", "dps_divisore") * random.uniform(
                            anello_val(anello, "turno", "trascinamento", "random_min"),
                            anello_val(anello, "turno", "trascinamento", "random_max"),
                        )) + inte
                        oppo["hp"] -= danni
                        text += f"**{nome2} viene trascinato da un potere oscuro a terra ed obbligato a subire {danni} danni!**\n"
            
            elif anellon == "Anello di totano" and anello_ok(num, anellon, "turno", "cura"):
                if "schiva il colpo" not in text:
                    hp = round(anello_val(anellon, "turno", "cura", "cura_colpito") * mod)
                    oppo["hp"] += hp
                else:
                    mod = random.uniform(
                        anello_val(anellon, "turno", "cura", "random_min"),
                        anello_val(anellon, "turno", "cura", "random_max"),
                    ) * anello_val(anellon, "turno", "cura", "moltiplicatore_mod_schivato")
                    hp = round(anello_val(anellon, "turno", "cura", "cura_schivato") * mod)
                    oppo["hp"] += hp
                text += f"__{nome2} mangia un pezzetto di anello di totano, moooolto buono ({hp} recuperati)!__\n"
            
            elif anello == "Cuffia da boia" and oppo["hp"] <= (anello_val(anello, "turno", "esecuzione", "hp_target_base") * bonus ):
                oppo["hp"] = anello_val(anello, "turno", "esecuzione", "hp_finale")
                text += "🪓"
            
            elif (anello == "Cuore delle sabbie" and anello_ok(num, anello, "turno", "insabbiato")) or nome1 in anello_val("Cuore delle sabbie", "turno", "insabbiato", "nomi_equivalenti", []):
                text += "**La tempesta di sabbia avanza**\n"
                try:
                    oppo["boost"]["sfida"]["Insabbiato"]["lv"] += anello_val("Cuore delle sabbie", "turno", "insabbiato", "lv_incremento")
                except:

                    oppo["boost"]["sfida"]["Insabbiato"] = {
                        "lv": anello_val("Cuore delle sabbie", "turno", "insabbiato", "lv"),
                        "dur": anello_val("Cuore delle sabbie", "turno", "insabbiato", "dur"),
                    }
            elif anello == "Chiavi" and anello_ok(num, anello, "turno", "batmobile"):
                danno_chiavi = anello_val(anello, "turno", "batmobile", "danno")
                text += f"**{nome2} viene investito dalla batmobile, subendo così {danno_chiavi} danni!**\n"
                oppo["hp"] -= danno_chiavi
    
    if oppo["incantamenti"] != []:
        if "Iridescente" in oppo["incantamenti"] and incantesimo_ok(num, "Iridescente", "turno", "cura"):
            text += f"✨ {nome2} recupera energia iridescente!\n"
            oppo["hp"] += incantesimo_val("Iridescente", "turno", "cura", "cura")
        
        if "Speranza" in oppo["incantamenti"] and oppo["hp"] <= incantesimo_val("Speranza", "turno", "salvezza", "hp_max") and oppo["hp"] >= incantesimo_val("Speranza", "turno", "salvezza", "hp_min"):
                oppo["hp"] = incantesimo_val("Speranza", "turno", "salvezza", "hp_porta_a")
                text += "🕊"
        
        if "Smateriabile" in oppo["incantamenti"] and incantesimo_ok(num, "Smateriabile", "turno", "annulla_colpo"):
                try:
                    danno = 0
                    mod = 0
                    text += "🚫"
                except:
                    
                    pass
    if main["incantamenti"] != []:
        if "Tocco fantasma" in main["incantamenti"] and incantesimo_ok(num, "Tocco fantasma", "turno", "colpo_schivato"):
                if "schiva il colpo" in text:
                    danni = round(dps * random.uniform(incantesimo_val("Tocco fantasma", "turno", "colpo_schivato", "dps_percento_min"), incantesimo_val("Tocco fantasma", "turno", "colpo_schivato", "dps_percento_max")) / 100)
                    if danni <= incantesimo_val("Tocco fantasma", "turno", "colpo_schivato", "danno_min"):
                        danni = incantesimo_val("Tocco fantasma", "turno", "colpo_schivato", "danno_min")
                    oppo["hp"] -= danni
                    text += f"L'arma fantasma di {nome1} colpisce lo stesso, infliggendo {danni} danni!"
        
        
               
    if "veleno" in oppo:
        oppo["hp"] -= oppo["veleno"] * incantesimo_val("Velenoso", "turno", "veleno", "danno_per_stack")
    
    if "Insabbiato" in oppo["boost"]["sfida"]:
        sabbia = round(4 * oppo["boost"]["sfida"]["Insabbiato"]["lv"])
        if nome1 == "Leviatano delle sabbie":
                    sabbia = round(sabbia / 3)
                    text += f"La tempesta di sabbia infligge {sabbia} danni a {nome2}!\n"
                    if "Smateriabile" in oppo["incantamenti"] and incantesimo_ok(num, "Smateriabile", "turno", "tempesta_sabbia"):
                        text += "🚫"

                    else:
                        
                        oppo["hp"] -= sabbia
        else:
                    if 0.5 > num:
                        sabbia = round(sabbia / 2)
                        text += f"La tempesta di sabbia infligge {sabbia} danni a {nome2}!\n"
                        if "Smateriabile" in oppo["incantamenti"] and incantesimo_ok(num, "Smateriabile", "turno", "tempesta_sabbia"):
                            text += "🚫"

                        else:
                            oppo["hp"] -= sabbia
                    elif 0.05 > num:
                        pass
                    elif 0.2 > num:
                        text += f"La tempesta di sabbia rovina l'armatura di {nome2}!\n"
                    else:
                        oppo["agi"] -= (sabbia/6)
                        text += f"La tempesta di sabbia acceca {nome2}!\n"
    text += "\n"
    return text


async def dungeon_stanze(app, message,player,scelta,nop,username,evento,last_dungeon,globali,inabilitati,scelte,tutto,tuttov,megaman,zombie,gungeon,magic,protezioni,armi,trader):
    if scelta not in nemici:
        other_time = last_dungeon.get(username,0)
        now = time.time() 
        modificatore = 0
        if evento["mod"] == "stop_dg":
            modificatore += dungeon_global("generale", "mod_stop_dg", -5)
        if evento["mod"] == "più_dg":
            modificatore += dungeon_global("generale", "mod_piu_dg", 5)
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


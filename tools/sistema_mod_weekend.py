from pathlib import Path
import ast
import re

ROOT = Path(__file__).resolve().parents[1]


def leggi(nome):
    return (ROOT / nome).read_text(encoding="utf-8")


def scrivi(nome, testo):
    (ROOT / nome).write_text(testo, encoding="utf-8")


def sostituisci(testo, vecchio, nuovo, nome, minimo=1, massimo=None):
    n = testo.count(vecchio)
    if n < minimo or (massimo is not None and n > massimo):
        raise RuntimeError(f"{nome}: occorrenze inattese {n}, attese {minimo}..{massimo}")
    return testo.replace(vecchio, nuovo)


# -----------------------------------------------------------------------------
# bilanciamento.py: database unico dei modificatori weekend
# -----------------------------------------------------------------------------
bil = leggi("bilanciamento.py")
if "WEEKEND_MOD_CONFIG =" not in bil:
    marker = "# ============================================================\n# DATABASE HARDCODATO DUNGEON"
    blocco = '''# ============================================================
# MODIFICATORI WEEKEND
# ============================================================
# Chiavi macchina stabili; nome/descrizione sono ciò che vede il giocatore.
# Il pool mantiene circa un terzo di weekend senza modificatore.
WEEKEND_MOD_CONFIG = {
    "punti_extra": {
        "nome": "Punti extra",
        "descrizione": "Le sfide PvP assegnano 5 punti extra al vincitore.",
        "punti_extra": 5,
    },
    "calma": {
        "nome": "Calma",
        "descrizione": "Hai 55 secondi per rispondere a una sfida invece di 35.",
        "tempo_sfida": 55,
    },
    "sfide assurde": {
        "nome": "Sfide assurde",
        "descrizione": "Hai 28 secondi per rispondere a una sfida invece di 35.",
        "tempo_sfida": 28,
    },
    "stop_dg": {
        "nome": "Dungeon scialli",
        "descrizione": "Le azioni del dungeon richiedono 5 secondi in più.",
        "mod_dungeon": -5,
    },
    "più_dg": {
        "nome": "Più dungeon",
        "descrizione": "Le azioni del dungeon richiedono 5 secondi in meno.",
        "mod_dungeon": 5,
    },
    "flexville": {
        "nome": "Flexville",
        "descrizione": "Il tempo base per riprendersi dalla morte passa da 900 a 450 secondi.",
        "recupero_secondi": 450,
    },
    "ricchezze_sparse": {
        "nome": "Ricchezze sparse",
        "descrizione": "Quando una sfida PvP droppa un oggetto, ne ricevi 2 copie.",
        "quantita_drop_pvp": 2,
    },
    "senza_frontiere": {
        "nome": "Senza frontiere",
        "descrizione": "Spostarsi tra le zone richiede soltanto 5 secondi.",
        "tempo_movimento": 5,
    },
    "dungeon_brutti_sporti_cattivi": {
        "nome": "Dungeon brutti, sporti e cattivi",
        "descrizione": "I premi positivi del dungeon sono x2, ma le statistiche dei nemici e dei boss del dungeon sono x3.",
        "moltiplicatore_premi_dungeon": 2,
        "moltiplicatore_stat_dungeon": 3,
    },
    "piovono_incantesimi": {
        "nome": "Piovono incantesimi",
        "descrizione": "Ogni giocatore riceve 3 copie di un libro casuale all'inizio dell'evento e di nuovo a mezzanotte.",
        "quantita_libri": 3,
        "ripeti_mezzanotte": True,
    },
    "grazie_partecipato": {
        "nome": "Grazie di aver partecipato",
        "descrizione": "Ogni giocatore riceve 20 usabili comuni casuali.",
        "quantita_usabili": 20,
    },
}

WEEKEND_MOD_POOL = [
    "punti_extra",
    "calma",
    "sfide assurde",
    "stop_dg",
    "più_dg",
    "flexville",
    "ricchezze_sparse",
    "senza_frontiere",
    "dungeon_brutti_sporti_cattivi",
    "piovono_incantesimi",
    "grazie_partecipato",
    None, None, None, None, None, None,
]


'''
    if marker not in bil:
        raise RuntimeError("bilanciamento.py: marker dungeon non trovato")
    bil = bil.replace(marker, blocco + marker, 1)
scrivi("bilanciamento.py", bil)


# -----------------------------------------------------------------------------
# nft.py: helper comuni + dungeon + movimento
# -----------------------------------------------------------------------------
nft = leggi("nft.py")
old_import = "from bilanciamento import PROC_CLASSI, PROC_ANELLI, NUCLEI_CONFIG, DUNGEON_CONFIG, INCANTESIMI_CONFIG, EFFETTI_CONFIG"
new_import = "from bilanciamento import PROC_CLASSI, PROC_ANELLI, NUCLEI_CONFIG, DUNGEON_CONFIG, INCANTESIMI_CONFIG, EFFETTI_CONFIG, WEEKEND_MOD_CONFIG, WEEKEND_MOD_POOL"
if old_import in nft:
    nft = nft.replace(old_import, new_import, 1)
elif new_import not in nft:
    raise RuntimeError("nft.py: import bilanciamento inatteso")

if "def weekend_mod_cfg(" not in nft:
    anchor = '''def anello_val(anello, contesto, nome, chiave, default=None):
    """Legge un valore di tuning dell'anello."""
    return anello_cfg(anello, contesto, nome).get(chiave, default)
'''
    helpers = '''def anello_val(anello, contesto, nome, chiave, default=None):
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
'''
    if anchor not in nft:
        raise RuntimeError("nft.py: anchor anello_val non trovato")
    nft = nft.replace(anchor, helpers, 1)

# Movimento: 5 secondi netti, senza ulteriori sconti di setta.
old_move = '''        ccc = 3600
        if player[username]["setta"]["benedizione"] == "Verme delle sabbie":
            a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
            ccc *= 1 - (a/100)
'''
new_move = '''        ccc = 3600
        if _WEEKEND_MOD_ATTIVO == "senza_frontiere":
            ccc = weekend_mod_val(_WEEKEND_MOD_ATTIVO, "tempo_movimento", 5)
        elif player[username]["setta"]["benedizione"] == "Verme delle sabbie":
            a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
            ccc *= 1 - (a/100)
'''
if old_move in nft:
    nft = nft.replace(old_move, new_move, 1)
elif new_move not in nft:
    raise RuntimeError("nft.py: blocco movimento non trovato")

nft = nft.replace(
    'text=f"Devi aspettare un\'ora per muoverti, diciamo che circa ti manca {tempo} ore!",',
    'text=f"Devi aspettare ancora {tempo} per muoverti!",'
)

# I vecchi stop/più dungeon diventano data-driven in tutte e tre le funzioni.
pattern_mod_dg = re.compile(
    r'modificatore = 0\n\s*if evento\["mod"\] == "stop_dg":\n\s*modificatore (?:-= 5|\+= dungeon_global\("generale", "mod_stop_dg", -5\))\s*\n\s*if evento\["mod"\] == "più_dg":\n\s*modificatore (?:\+= 5|\+= dungeon_global\("generale", "mod_piu_dg", 5\))\s*\n'
)
nft, n_mod_dg = pattern_mod_dg.subn('modificatore = weekend_mod_val(evento.get("mod"), "mod_dungeon", 0)\n', nft)
if n_mod_dg != 3 and 'weekend_mod_val(evento.get("mod"), "mod_dungeon", 0)' not in nft:
    raise RuntimeError(f"nft.py: sostituzione mod dungeon inattesa ({n_mod_dg})")

# Snapshot premi in tutte le modalità del dungeon.
for firma in [
    'async def dungeon_boss(app, message,player,scelta,nop,username,evento,last_dungeon,inabilitati,tuttov):\n',
    'async def dungeon_mostro(app, message,player,scelta,nop,username,evento,last_dungeon,nemici,inabilitati,trader):\n',
    'async def dungeon_stanze(app, message,player,scelta,nop,username,evento,last_dungeon,globali,inabilitati,scelte,tutto,tuttov,megaman,zombie,gungeon,magic,protezioni,armi,trader):\n',
]:
    if firma in nft and firma + '    _snapshot_premi_weekend' not in nft:
        nft = nft.replace(firma, firma + '    _snapshot_premi_weekend = _snapshot_premi_dungeon(player[username])\n', 1)

# Il boss può dare premio anche al supporto: snapshot separato.
boss_snapshot_anchor = 'async def dungeon_boss(app, message,player,scelta,nop,username,evento,last_dungeon,inabilitati,tuttov):\n    _snapshot_premi_weekend = _snapshot_premi_dungeon(player[username])\n'
if boss_snapshot_anchor in nft and '_snapshot_supporter_weekend' not in nft:
    nft = nft.replace(boss_snapshot_anchor, boss_snapshot_anchor + '''    _supporter_nome_weekend = None
    _snapshot_supporter_weekend = None
    try:
        _supporter_nome_weekend = player[username].get("supporto", {}).get("Nome")
        if _supporter_nome_weekend and _supporter_nome_weekend != username and _supporter_nome_weekend in player:
            _snapshot_supporter_weekend = _snapshot_premi_dungeon(player[_supporter_nome_weekend])
    except Exception:
        pass
''', 1)

# x3 dopo lo scaling normale: il moltiplicatore riguarda le statistiche finali del nemico.
monster_anchor = '''                )
            user1["incantamenti"] = get_ench(player[username])
            user2["incantamenti"] = []
'''
monster_new = '''                )
            _applica_stat_dungeon_evento(user2, evento)
            user1["incantamenti"] = get_ench(player[username])
            user2["incantamenti"] = []
'''
if monster_anchor in nft and monster_new not in nft:
    nft = nft.replace(monster_anchor, monster_new, 1)

boss_anchor = '''                    )
                )

            if "supporto" in player[username]:
'''
boss_new = '''                    )
                )

            _applica_stat_dungeon_evento(user2, evento)

            if "supporto" in player[username]:
'''
if boss_anchor in nft and boss_new not in nft:
    nft = nft.replace(boss_anchor, boss_new, 1)

# Duplica i delta positivi al termine delle tre funzioni.
if '_duplica_premi_dungeon_da_snapshot(player[username], _snapshot_premi_weekend, evento)\n\n\nasync def dungeon_mostro' not in nft:
    nft = re.sub(
        r'\n(?=async def dungeon_mostro\()',
        '\n    _duplica_premi_dungeon_da_snapshot(player[username], _snapshot_premi_weekend, evento)\n'
        '    if _snapshot_supporter_weekend is not None and _supporter_nome_weekend in player:\n'
        '        _duplica_premi_dungeon_da_snapshot(player[_supporter_nome_weekend], _snapshot_supporter_weekend, evento)\n\n',
        nft,
        count=1,
    )
if '_duplica_premi_dungeon_da_snapshot(player[username], _snapshot_premi_weekend, evento)\n\n\nasync def arena' not in nft:
    nft = re.sub(
        r'\n(?=async def arena\()',
        '\n    _duplica_premi_dungeon_da_snapshot(player[username], _snapshot_premi_weekend, evento)\n\n',
        nft,
        count=1,
    )
if nft.rstrip().endswith('await message.answer(f"Mancano {manca} secondi!")'):
    nft = nft.rstrip() + '\n    _duplica_premi_dungeon_da_snapshot(player[username], _snapshot_premi_weekend, evento)\n'

scrivi("nft.py", nft)


# -----------------------------------------------------------------------------
# __init__.py: selezione, effetti immediati, PvP, mezzanotte
# -----------------------------------------------------------------------------
ini = leggi("__init__.py")

# Sincronizza il mod caricato da backup con nft.py (serve a Senza frontiere).
if 'nft.set_weekend_mod(evento.get("mod"))' not in ini:
    anchor = 'strader = {"sfide":{}}\n'
    sync = '''try:
    nft.set_weekend_mod(evento.get("mod"))
except Exception:
    nft.set_weekend_mod(None)

strader = {"sfide":{}}
'''
    if anchor not in ini:
        raise RuntimeError("__init__.py: anchor strader non trovato")
    ini = ini.replace(anchor, sync, 1)

# Helper evento inseriti una volta, prima del comando manuale.
if 'def _regala_pioggia_incantesimi():' not in ini:
    anchor = '@app.on_message(filters.command("iniziaevento") & filters.private & filters.user(autorizzati)\n)\n'
    helpers = '''def _mod_weekend_corrente():
    if isinstance(evento, dict):
        return evento.get("mod")
    return None


def _tempo_sfida_weekend():
    return int(nft.weekend_mod_val(_mod_weekend_corrente(), "tempo_sfida", 35))


def _regala_pioggia_incantesimi():
    quantita = int(nft.weekend_mod_val("piovono_incantesimi", "quantita_libri", 3))
    for nome_giocatore in list(player):
        libro = random.choice(list(liste.libri))
        nft.gestione_zaino(player[nome_giocatore]["zaino"], "add", libro, quantita)
        try:
            app.send_message(
                nome_giocatore,
                f"🌧️ **Piovono incantesimi!**\\nDal cielo ti cadono {quantita} copie di **{libro}**!",
            )
        except Exception:
            pass


def _regala_grazie_partecipato():
    quantita = int(nft.weekend_mod_val("grazie_partecipato", "quantita_usabili", 20))
    for nome_giocatore in list(player):
        ricevuti = {}
        for _ in range(quantita):
            usabile = random.choice(liste.usabilitutti)
            nft.gestione_zaino(player[nome_giocatore]["zaino"], "add", usabile, 1)
            ricevuti[usabile] = ricevuti.get(usabile, 0) + 1
        riepilogo = ", ".join(f"{q}x {oggetto}" for oggetto, q in ricevuti.items())
        try:
            app.send_message(
                nome_giocatore,
                f"🎁 **Grazie di aver partecipato!**\\nRicevi {quantita} usabili comuni casuali:\\n{riepilogo}",
            )
        except Exception:
            pass


def _attiva_mod_weekend(mod):
    nft.set_weekend_mod(mod)
    if mod == "piovono_incantesimi":
        _regala_pioggia_incantesimi()
    elif mod == "grazie_partecipato":
        _regala_grazie_partecipato()


''' + anchor
    if anchor not in ini:
        raise RuntimeError("__init__.py: comando iniziaevento non trovato")
    ini = ini.replace(anchor, helpers, 1)

# Due estrazioni: manuale e sabato mattina.
old_pool = 'random.choice(["punti_extra", "calma", "sfide assurde", "stop_dg","più_dg","flexville",None,None,None])'
if old_pool in ini:
    ini = ini.replace(old_pool, 'random.choice(nft.WEEKEND_MOD_POOL)')
if ini.count('random.choice(nft.WEEKEND_MOD_POOL)') < 2:
    raise RuntimeError("__init__.py: non risultano entrambe le estrazioni weekend")

# Attiva globalmente il mod e gli eventuali regali immediati dopo la scelta.
activation_old = '    evento["mod"] = mod\n    evento["evento"] = scelto\n\n    with open("./backup/evento.json", "w") as outfile:'
activation_new = '    evento["mod"] = mod\n    evento["evento"] = scelto\n    _attiva_mod_weekend(mod)\n\n    with open("./backup/evento.json", "w") as outfile:'
if activation_old in ini:
    ini = ini.replace(activation_old, activation_new)
if ini.count('_attiva_mod_weekend(mod)') < 3:  # definizione + 2 chiamate
    raise RuntimeError("__init__.py: attivazione immediata non inserita in entrambe le partenze")

# Descrizioni dei nuovi modificatori nelle due notifiche di inizio.
flex_line = '        if mod == "flexville":\n            testo+= " Tempi morti dimezzati, muori meno per vivere meglio!"\n'
new_desc = flex_line + '''        if mod in ("ricchezze_sparse", "senza_frontiere", "dungeon_brutti_sporti_cattivi", "piovono_incantesimi", "grazie_partecipato"):
            testo += " " + nft.weekend_mod_descrizione(mod)
'''
if flex_line in ini and 'mod in ("ricchezze_sparse"' not in ini:
    ini = ini.replace(flex_line, new_desc)

# Punti extra: il vecchio codice incrementava furto dopo aver copiato punti, quindi non aveva effetto.
old_points = '                            if evento["mod"] == "punti_extra":\n                                furto += 5\n'
new_points = '                            if evento["mod"] == "punti_extra":\n                                punti += nft.weekend_mod_val("punti_extra", "punti_extra", 5)\n'
if old_points in ini:
    ini = ini.replace(old_points, new_points)
if 'furto += 5' in ini:
    raise RuntimeError("__init__.py: bug punti_extra ancora presente")

# Flexville: corregge tutti i vecchi no-op `minimo - 450`.
ini = ini.replace(
    'if evento["mod"] == "flexville":\n                minimo - 450',
    'if evento["mod"] == "flexville":\n                minimo = nft.weekend_mod_val("flexville", "recupero_secondi", 450)'
)
ini = ini.replace(
    'if evento["mod"] == "flexville":\n                        minimo - 450',
    'if evento["mod"] == "flexville":\n                        minimo = nft.weekend_mod_val("flexville", "recupero_secondi", 450)'
)
if 'minimo - 450' in ini:
    raise RuntimeError("__init__.py: bug flexville ancora presente")

# Calma/Sfide assurde su ogni percorso che usa il timer PvP, senza doppia applicazione.
ini = ini.replace('tempo = 35', 'tempo = _tempo_sfida_weekend()')
old_adjust = '''                if evento["mod"] ==  "calma":
                        tempo += 20
                if evento["mod"] ==  "sfide assurde":
                        tempo -= 7
'''
ini = ini.replace(old_adjust, '')

# Ricchezze sparse: quantità doppia dello stesso drop, non probabilità doppia.
start = ini.index('def premio_exp(a, b, text):')
end = ini.index('\nimport asyncio', start)
premio = ini[start:end]
if 'quantita_drop_pvp' not in premio:
    premio = premio.replace(
        '    possibilia = 0.2\n    possibilib = 0.1\n',
        '    possibilia = 0.2\n    possibilib = 0.1\n    quantita_drop = int(nft.weekend_mod_val(_mod_weekend_corrente(), "quantita_drop_pvp", 1))\n',
        1,
    )
    premio = premio.replace('a["zaino"][contentino] += 1', 'a["zaino"][contentino] += quantita_drop')
    premio = premio.replace('a["zaino"][contentino] = 1', 'a["zaino"][contentino] = quantita_drop')
    premio = premio.replace('b["zaino"][contentino] += 1', 'b["zaino"][contentino] += quantita_drop')
    premio = premio.replace('b["zaino"][contentino] = 1', 'b["zaino"][contentino] = quantita_drop')
    premio = premio.replace(
        'f"Hai vinto {contentino} grazie alla tua bravura in questa sfida!"',
        'f"Hai vinto {quantita_drop}x {contentino} grazie alla tua bravura in questa sfida!"'
    )
    premio = premio.replace(
        'f"Di consolazione ottieni {contentino}!"',
        'f"Di consolazione ottieni {quantita_drop}x {contentino}!"'
    )
    ini = ini[:start] + premio + ini[end:]

# A mezzanotte Piovono incantesimi riparte finché il mod è attivo.
midnight_old = 'def mezzanotte():\n    \n    trader["primo"] = None'
midnight_new = 'def mezzanotte():\n    if _mod_weekend_corrente() == "piovono_incantesimi":\n        _regala_pioggia_incantesimi()\n    \n    trader["primo"] = None'
if midnight_old in ini and midnight_new not in ini:
    ini = ini.replace(midnight_old, midnight_new, 1)
if midnight_new not in ini:
    raise RuntimeError("__init__.py: hook mezzanotte non trovato")

# Alla fine del weekend pulisce anche lo stato runtime usato dal movimento.
fine_old = 'def fine_weew():\n    \n    evento["evento"] = None\n    evento["mod"] = None'
fine_new = 'def fine_weew():\n    \n    evento["evento"] = None\n    evento["mod"] = None\n    nft.set_weekend_mod(None)'
if fine_old in ini and fine_new not in ini:
    ini = ini.replace(fine_old, fine_new, 1)
if fine_new not in ini:
    raise RuntimeError("__init__.py: fine weekend non aggiornato")

scrivi("__init__.py", ini)


# -----------------------------------------------------------------------------
# Validazioni locali del patcher
# -----------------------------------------------------------------------------
for nome in ("bilanciamento.py", "nft.py", "liste.py"):
    ast.parse(leggi(nome), filename=nome)

bil = leggi("bilanciamento.py")
nft = leggi("nft.py")
ini = leggi("__init__.py")

for chiave in (
    "ricchezze_sparse", "senza_frontiere", "dungeon_brutti_sporti_cattivi",
    "piovono_incantesimi", "grazie_partecipato",
):
    assert chiave in bil
    assert chiave in ini

assert '"quantita_drop_pvp": 2' in bil
assert '"tempo_movimento": 5' in bil
assert '"moltiplicatore_premi_dungeon": 2' in bil
assert '"moltiplicatore_stat_dungeon": 3' in bil
assert '"quantita_libri": 3' in bil
assert '"quantita_usabili": 20' in bil
assert nft.count('_applica_stat_dungeon_evento(user2, evento)') >= 2
assert nft.count('_duplica_premi_dungeon_da_snapshot(') >= 4
assert 'ccc = weekend_mod_val(_WEEKEND_MOD_ATTIVO, "tempo_movimento", 5)' in nft
assert 'minimo - 450' not in ini
assert 'furto += 5' not in ini
assert ini.count('random.choice(nft.WEEKEND_MOD_POOL)') >= 2
assert ini.count('_tempo_sfida_weekend()') >= 2
assert '_regala_pioggia_incantesimi()' in ini
assert 'quantita_drop = int(nft.weekend_mod_val' in ini
print("Patch modificatori weekend applicata e validata")

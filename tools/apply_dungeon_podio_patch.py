# -*- coding: utf-8 -*-
"""Patch temporanea: applica Podio/imboscate ai file runtime storici."""
from pathlib import Path


def replace_once(text, old, new, label):
    matches = text.count(old)
    if matches != 1:
        raise RuntimeError(f"{label}: atteso 1 match, trovati {matches}")
    return text.replace(old, new, 1)


# nft.py: helper + Podio + imboscata.
p = Path("nft.py")
s = p.read_text(encoding="utf-8")
s = replace_once(
    s,
    "from frasi_incantesimi import FRASI_INCANTESIMI_TECNICHE\n",
    "from frasi_incantesimi import FRASI_INCANTESIMI_TECNICHE\n"
    "from dungeon_extra import (\n"
    "    podio_probabilita_pct,\n"
    "    podio_livello_premio,\n"
    "    podio_penalita_gloria,\n"
    "    podio_applica_penalita,\n"
    "    scegli_nemici_imboscata,\n"
    ")\n",
    "import dungeon_extra",
)

action_anchor = (
    '                text = f"Scegli {scelta}\\n"\n'
    '                if scelta == "Vedere" and "Faro" in player[username]["dungeon"]["mostri"]:\n'
)
action_insert = '''                text = f"Scegli {scelta}\\n"

                if (
                    scelta in ["1° posto", "2° posto", "3° posto"]
                    and "Podio" in player[username]["dungeon"]["mostri"]
                ):
                    stanza = "Podio"
                    posizione = {"1° posto": 1, "2° posto": 2, "3° posto": 3}[scelta]
                    obiettivi_totali = len(descri)
                    obiettivi_completati = len(player[username].get("obbiettivi", []))
                    probabilita_podio = podio_probabilita_pct(
                        obiettivi_completati, obiettivi_totali, posizione
                    )
                    livello_premio = podio_livello_premio(
                        posizione,
                        dungeon_global("generale", "podio_livello_base", 4),
                    )
                    if random.random() < (probabilita_podio / 100):
                        premi_livellabili = [x for x in tutto if "LV0" in str(x)]
                        if premi_livellabili:
                            contentino = random.choice(premi_livellabili).replace(
                                "LV0", f"LV{livello_premio}"
                            )
                            gestione_zaino(player[username]["zaino"], "add", contentino, 1)
                            text += (
                                f"Sali sul {posizione}° gradino e stavolta il Podio ti premia!\\n"
                                f"Probabilità: {probabilita_podio:.3f}% · Ottieni **{contentino}**."
                            )
                        else:
                            text += "Il Podio vorrebbe premiarti, ma non trova oggetti livellabili nel pool."
                    else:
                        penalita = podio_penalita_gloria(
                            posizione,
                            base=dungeon_global("generale", "podio_gloria_base", 6),
                            moltiplicatore=dungeon_global("generale", "podio_gloria_moltiplicatore", 2),
                        )
                        nuova_gloria, gloria_persa = podio_applica_penalita(
                            player[username].get("gloria", 0), penalita
                        )
                        player[username]["gloria"] = nuova_gloria
                        text += (
                            f"Sali sul {posizione}° gradino, ma non vinci nulla.\\n"
                            f"Probabilità: {probabilita_podio:.3f}% · Perdi **{gloria_persa} Gloria**."
                        )

                if scelta == "Vedere" and "Faro" in player[username]["dungeon"]["mostri"]:
'''
s = replace_once(s, action_anchor, action_insert, "azione Podio")

room_anchor = (
    '                fines = False\n'
    '                text = f"Esplorando il dungeon raggiungi {scelta}!\\n"\n'
    '                if scelta == "Faro":\n'
)
room_insert = '''                fines = False
                text = f"Esplorando il dungeon raggiungi {scelta}!\\n"

                imboscata_cfg = DUNGEON_CONFIG.get("generale", {}).get("imboscata", {})
                if random.random() < (float(imboscata_cfg.get("proc", 0.5)) / 100):
                    locali_imboscata = casa_nemici.get(player[username]["location"], [])
                    nemici_imboscata = scegli_nemici_imboscata(
                        list(nemici),
                        locali_imboscata,
                        imboscata_cfg.get("nemici", 2),
                    )
                    if nemici_imboscata:
                        for nemico_imboscata in reversed(nemici_imboscata):
                            player[username]["dungeon"]["mostri"].insert(0, nemico_imboscata)
                        await app.send_message(
                            username,
                            "Mentre giravi per il dungeon un gruppo di loschi figuri si avvicina, è un imboscata!",
                        )

                if scelta == "Faro":
'''
s = replace_once(s, room_anchor, room_insert, "imboscata stanza")

podio_room_anchor = '                if scelta == "Cucina":\n'
podio_room_insert = '''                if scelta == "Podio":
                    obiettivi_totali = len(descri)
                    obiettivi_completati = len(player[username].get("obbiettivi", []))
                    text += (
                        "Tre gradini illuminati emergono dal pavimento: 1°, 2° e 3° posto.\\n"
                        f"Hai {obiettivi_completati}/{obiettivi_totali} obiettivi completati.\\n"
                    )
                    for posizione_podio in (1, 2, 3):
                        chance_podio = podio_probabilita_pct(
                            obiettivi_completati, obiettivi_totali, posizione_podio
                        )
                        lv_podio = podio_livello_premio(
                            posizione_podio,
                            dungeon_global("generale", "podio_livello_base", 4),
                        )
                        perdita_podio = podio_penalita_gloria(
                            posizione_podio,
                            base=dungeon_global("generale", "podio_gloria_base", 6),
                            moltiplicatore=dungeon_global("generale", "podio_gloria_moltiplicatore", 2),
                        )
                        text += (
                            f"{posizione_podio}°: {chance_podio:.3f}% → oggetto LV{lv_podio}; "
                            f"se fallisci perdi fino a {perdita_podio} Gloria.\\n"
                        )
                    bottoni = []
                    for appz in ["1° posto", "2° posto", "3° posto"]:
                        bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])
                    reply_markup = InlineKeyboardMarkup(bottoni)
                    await app.send_message(
                        chat_id=username,
                        text=text,
                        reply_markup=reply_markup,
                    )

                if scelta == "Cucina":
'''
s = replace_once(s, podio_room_anchor, podio_room_insert, "stanza Podio")
p.write_text(s, encoding="utf-8")


# liste.py: una copia della stanza + le tre scelte.
p = Path("liste.py")
s = p.read_text(encoding="utf-8")
marker = "\n# --- PODIO DUNGEON / IMBOSCATE ---\n"
if marker not in s:
    s += marker
    s += 'if "Podio" not in stanze:\n'
    s += '    stanze.append("Podio")\n'
    s += 'for _scelta_podio in ("1° posto", "2° posto", "3° posto"):\n'
    s += '    if _scelta_podio not in scelte:\n'
    s += '        scelte.append(_scelta_podio)\n'
    s += 'del _scelta_podio\n'
p.write_text(s, encoding="utf-8")


# bilanciamento.py: tuning centralizzato.
p = Path("bilanciamento.py")
s = p.read_text(encoding="utf-8")
marker = "\n# --- PODIO DUNGEON / IMBOSCATE ---\n"
if marker not in s:
    s += marker
    s += 'DUNGEON_CONFIG.setdefault("generale", {}).update({\n'
    s += '    "podio_livello_base": 4,\n'
    s += '    "podio_gloria_base": 6,\n'
    s += '    "podio_gloria_moltiplicatore": 2,\n'
    s += '    "imboscata": {"proc": 0.5, "nemici": 2},\n'
    s += '})\n'
    s += 'DUNGEON_CONFIG.setdefault("stanze", {})["Podio"] = {\n'
    s += '    "1° posto": {"posizione": 1},\n'
    s += '    "2° posto": {"posizione": 2},\n'
    s += '    "3° posto": {"posizione": 3},\n'
    s += '}\n'
p.write_text(s, encoding="utf-8")

print("Patch runtime Podio/imboscate applicata")

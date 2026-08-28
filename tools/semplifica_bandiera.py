from pathlib import Path

path = Path("__init__.py")
text = path.read_text(encoding="utf-8")

start_marker = '@app.on_message(filters.command(["disegna", "disegna@NFTchallengebot"])'
start = text.index(start_marker)
next_handler = text.index("\n\n@app.on_message", start + len(start_marker))

new_block = r'''BANDIERA_EDITOR_HEADER = "🧵 MODIFICA BANDIERA"


def _bandiera_testo_editabile(griglia):
    """Rende la bandiera copiabile senza spezzare le emoji composte."""
    return "\n".join(" ".join(str(cella) for cella in riga) for riga in griglia)


def _leggi_bandiera_risposta(testo, schema):
    """Legge una griglia con celle separate da spazi e conserva la forma esistente."""
    righe_testo = [riga.strip() for riga in testo.splitlines() if riga.strip()]
    if len(righe_testo) != len(schema):
        return None

    nuova = []
    for indice, riga_testo in enumerate(righe_testo):
        celle = riga_testo.split()
        if len(celle) != len(schema[indice]):
            return None
        nuova.append(celle)
    return nuova


@app.on_message(filters.command(["disegna", "disegna@NFTchallengebot"]) & ~filters.user(bannati) & ~filters.chat(non_qui))
async def disegna(client, message):
    username = message.from_user.username
    if player[username]["team"] is None or player[username]["team"] == "nessuno":
        await app.send_message(message.chat.id, "Non hai un team!")
        return

    team = player[username]["team"]
    if clan[team]["Sarto"] != username:
        await app.send_message(message.chat.id, "Non sei il sarto del clan!")
        return

    if "Bandiera" not in clan[team] or not clan[team]["Bandiera"]:
        await app.send_message(message.chat.id, "Questo clan non ha ancora una griglia Bandiera valida.")
        return

    # Modalità semplice: il bot rimanda la bandiera e il Sarto risponde con la nuova griglia.
    if len(message.command) == 1:
        griglia = clan[team]["Bandiera"]
        dimensioni = " x ".join([str(len(griglia)), str(len(griglia[0]))]) if griglia else "?"
        testo = (
            f"{BANDIERA_EDITOR_HEADER}\n"
            f"Dimensioni: {dimensioni}\n\n"
            "Rispondi A QUESTO MESSAGGIO con la nuova bandiera completa.\n"
            "Mantieni uno spazio tra ogni casella e lo stesso numero di righe/colonne.\n"
            "La risposta sovrascriverà completamente la bandiera attuale.\n\n"
            f"{_bandiera_testo_editabile(griglia)}"
        )
        await app.send_message(message.chat.id, testo)
        return

    # Mantiene anche il vecchio editor rapido di una singola casella.
    try:
        x = int(message.command[1]) - 1
        y = int(message.command[2]) - 1
        emoji = message.command[3].strip()
        if not emoji:
            raise ValueError("emoji vuota")
        if x < 0 or y < 0:
            raise IndexError("coordinate negative")
        clan[team]["Bandiera"][x][y] = emoji
        await app.send_message(
            message.chat.id,
            "Fatto!\n" + _bandiera_testo_editabile(clan[team]["Bandiera"]),
        )
    except Exception:
        await app.send_message(
            message.chat.id,
            "Formato non valido. Usa /disegna per l'editor completo, oppure /disegna riga colonna emoji.",
        )


@app.on_message(filters.reply & filters.text & ~filters.user(bannati) & ~filters.chat(non_qui))
async def sovrascrivi_bandiera_da_risposta(client, message):
    risposta = message.reply_to_message
    if risposta is None or not getattr(risposta, "text", None):
        return
    if not risposta.text.startswith(BANDIERA_EDITOR_HEADER):
        return

    username = message.from_user.username
    if username not in player or player[username]["team"] is None or player[username]["team"] == "nessuno":
        await app.send_message(message.chat.id, "Non hai un team!")
        return

    team = player[username]["team"]
    if clan[team]["Sarto"] != username:
        await app.send_message(message.chat.id, "Solo il Sarto può sovrascrivere la bandiera.")
        return

    vecchia = clan[team].get("Bandiera")
    if not vecchia:
        await app.send_message(message.chat.id, "Non trovo la griglia della bandiera del clan.")
        return

    nuova = _leggi_bandiera_risposta(message.text, vecchia)
    if nuova is None:
        forma = " x ".join([str(len(vecchia)), str(len(vecchia[0]))]) if vecchia else "?"
        await app.send_message(
            message.chat.id,
            f"La griglia non ha la forma corretta ({forma}). Lascia uno spazio tra ogni casella e riprova rispondendo allo stesso messaggio.",
        )
        return

    clan[team]["Bandiera"] = nuova
    await app.send_message(
        message.chat.id,
        "🧵 Bandiera sovrascritta!\n\n" + _bandiera_testo_editabile(nuova),
    )
'''

text = text[:start] + new_block + text[next_handler:]
path.write_text(text, encoding="utf-8")

# Controlli statici mirati (il file storico contiene altre aree non compilabili isolate).
updated = path.read_text(encoding="utf-8")
checks = [
    'BANDIERA_EDITOR_HEADER = "🧵 MODIFICA BANDIERA"',
    'async def sovrascrivi_bandiera_da_risposta',
    'clan[team]["Bandiera"] = nuova',
    'emoji = message.command[3].strip()',
    '_bandiera_testo_editabile',
    '_leggi_bandiera_risposta',
]
for check in checks:
    assert check in updated, check
assert 'emoji = message.command[3][0]' not in updated
print("Editor bandiera aggiornato e validato")

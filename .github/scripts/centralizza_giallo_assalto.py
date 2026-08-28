from pathlib import Path

NFT = Path("nft.py")
INIT = Path("__init__.py")

nft = NFT.read_text(encoding="utf-8")
init = INIT.read_text(encoding="utf-8")

# 1) Centralizza logica last/Giallo in nft.py.
marker = '''def effetto_cfg(effetto, contesto, nome):
'''
if marker not in nft:
    raise SystemExit("Marker effetto_cfg non trovato")

helper = '''def calcola_omini_assalto(giocatore, username, last_clan):
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
        messaggio_giallo = "Venite a me ~~Minions~~ giallini, è ora di distruggere questo posto!\\n"

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


'''
if "def calcola_omini_assalto(" not in nft:
    nft = nft.replace(marker, helper + marker, 1)

# 2) Sostituisce il blocco duplicato in nft.riassalto con la funzione comune.
start_marker = '                                    # Gli "omini" del clan sono le entry recenti di last.\n'
end_marker = '                                    serv = matx\n'
start = nft.find(start_marker)
end = nft.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit("Blocco Giallo inline in nft.riassalto non trovato")
replacement = '''                                    matx, omini_reali, giallini_attivi, messaggio_giallo = calcola_omini_assalto(
                                        giocatore, username, clan[user["team"]]["last"]
                                    )

'''
nft = nft[:start] + replacement + nft[end:]
NFT.write_text(nft, encoding="utf-8")

# 3) Il percorso /assalto principale deve caricare gli incantesimi.
old_copy = '''                                        giocatore = copy.deepcopy(player[username]["scheda"])
                                        if "pet" in player[username]:
'''
new_copy = '''                                        giocatore = copy.deepcopy(player[username]["scheda"])
                                        giocatore["incantamenti"] = nft.get_ench(player[username])
                                        if "pet" in player[username]:
'''
if old_copy not in init:
    raise SystemExit("Copia giocatore in __init__.py non trovata")
init = init.replace(old_copy, new_copy, 1)

# 4) Usa lo stesso conteggio Giallo condiviso anche nel comando /assalto.
old_count = '''                                        matx = 0
                                        for pl in clan[user["team"]]["last"]:
                                            elapsed = time.time() - clan[user["team"]]["last"][pl]
                                            if elapsed < 301 and username != pl:
                                                matx += 1
                                                
                                        serv = matx
'''
new_count = '''                                        matx, omini_reali, giallini_attivi, messaggio_giallo = nft.calcola_omini_assalto(
                                            giocatore, username, clan[user["team"]]["last"]
                                        )
                                        serv = matx
'''
if old_count not in init:
    raise SystemExit("Conteggio omini storico in __init__.py non trovato")
init = init.replace(old_count, new_count, 1)

old_output = '''                                        output = nft.assedio(player,
                                            giocatore,
                                            nemico,
                                            target[0],
                                            user["team"],
                                            ordine,
                                            clan,
                                            trader["meteo"][player[username]["location"]],
                                            clan[clan[user["team"]]["inguerra"]]["setting"]
                                            
                                        )
                                        output += f"\\n{matx} persone assaltano con te!"
'''
new_output = '''                                        output = messaggio_giallo + nft.assedio(player,
                                            giocatore,
                                            nemico,
                                            target[0],
                                            user["team"],
                                            ordine,
                                            clan,
                                            trader["meteo"][player[username]["location"]],
                                            clan[clan[user["team"]]["inguerra"]]["setting"]
                                            
                                        )
                                        output += f"\\n{omini_reali} persone assaltano con te!"
                                        if giallini_attivi:
                                            output += f" (+{giallini_attivi} giallini attivi)"
'''
if old_output not in init:
    raise SystemExit("Output assalto storico in __init__.py non trovato")
init = init.replace(old_output, new_output, 1)

INIT.write_text(init, encoding="utf-8")
print("Conteggio Giallo centralizzato su nft.riassalto e /assalto")

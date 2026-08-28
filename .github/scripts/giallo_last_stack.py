from pathlib import Path

NFT = Path("nft.py")
FRASI = Path("frasi_incantesimi.py")

nft = NFT.read_text(encoding="utf-8")

old = '''                                    matx = 0
                                    for pl in clan[user["team"]]["last"]:
                                        elapsed = time.time() - clan[user["team"]]["last"][pl]
                                        if elapsed < 301 and username != pl:
                                            matx += 1
                                            
                                    matx_effettivo = matx
                                    messaggio_giallo = ""
                                    if "Giallo" in giocatore.get("incantamenti", []) and incantesimo_ok(random.random(), "Giallo", "assalto", "aiutanti"):
                                        matx_effettivo += incantesimo_val("Giallo", "assalto", "aiutanti", "aiutanti_extra")
                                        messaggio_giallo = "Venite a me ~~Minions~~ giallini, è ora di distruggere questo posto!\\n"

                                    serv = matx_effettivo
                                    if matx_effettivo < proc_val("Eroe caduto", "assalto", "supporto_clan", "compagni_soglia") and giocatore["set"] == 'Eroe caduto':
                                        serv += proc_val("Eroe caduto", "assalto", "supporto_clan", "serv_bonus_nft")
                                        
                                    if giocatore["set"] == 'Eroe della rivolta':
                                        serv = serv * proc_val("Eroe della rivolta", "assalto", "supporto_clan", "serv_mul")
                                    if player[username]["setta"]["benedizione"] == 'Orso polare' and matx_effettivo > 2:
                                        
                                        a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"] /100))
                                        serv += (a/4)
                                    if player[username]["setta"]["benedizione"] == 'Kaimano' and matx_effettivo <= 2:
                                        a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"] /100))
                                        serv += (a/4)
'''

# Il file storico non ha spazi attorno a /100: normalizziamo solo per il match.
old = old.replace('["%"] /100', '["%"])/100').replace('["%"])/100)', '["%"])/100)')

# Usa un blocco più robusto delimitato da marker reali.
start_marker = '                                    matx = 0\n                                    for pl in clan[user["team"]]["last"]:'
end_marker = '                                    bostabile = ["def", "atk", "agi"]\n'
start = nft.find(start_marker)
end = nft.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit("Blocco riassalto/Giallo non trovato")

new = '''                                    # Gli "omini" del clan sono le entry recenti di last.
                                    # Giallo inserisce vere entry fittizie nello stesso dizionario:
                                    # ogni proc crea 10 chiavi nuove, quindi gli stack sono naturali.
                                    last_clan = clan[user["team"]]["last"]
                                    ora_omini = time.time()
                                    prefisso_giallo = "__giallo__"

                                    # Le entry finte scadute non servono più: puliamo solo quelle,
                                    # senza cambiare il comportamento storico delle entry reali.
                                    for pl, timestamp in list(last_clan.items()):
                                        if str(pl).startswith(prefisso_giallo) and (ora_omini - timestamp) >= 301:
                                            last_clan.pop(pl, None)

                                    messaggio_giallo = ""
                                    if "Giallo" in giocatore.get("incantamenti", []) and incantesimo_ok(random.random(), "Giallo", "assalto", "aiutanti"):
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

                                    serv = matx
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
'''.replace('["%"] /100', '["%"])/100').replace('["%"])/100)', '["%"])/100)')

# Corregge la forma della moltiplicazione generata sopra in modo esplicito.
new = new.replace('trader["sette"][player[username]["setta"]["loc"]]["%"])/100)', 'trader["sette"][player[username]["setta"]["loc"]]["%"] /100)')

nft = nft[:start] + new + nft[end:]

old_output = '''                                    output += f"\\n{matx} persone assaltano con te!"
                                    if matx_effettivo != matx:
                                        output += f" ({matx_effettivo} considerate nei calcoli grazie a Giallo)"
'''
new_output = '''                                    output += f"\\n{omini_reali} persone assaltano con te!"
                                    if giallini_attivi:
                                        output += f" (+{giallini_attivi} giallini attivi)"
'''
if old_output not in nft:
    raise SystemExit("Blocco output Giallo non trovato")
nft = nft.replace(old_output, new_output, 1)

if "matx_effettivo" in nft:
    raise SystemExit("matx_effettivo è ancora presente")

NFT.write_text(nft, encoding="utf-8")

frasi = FRASI.read_text(encoding="utf-8")
old_frase = '    "Giallo": "All\'inizio dell\'assalto, prima di tutti i bonus che dipendono dal numero di compagni, hai il {assalto.aiutanti.proc:pct} di aggiungere {assalto.aiutanti.aiutanti_extra} aiutanti virtuali al conteggio. Non sono giocatori reali: valgono solo per quei calcoli.",'
new_frase = '    "Giallo": "All\'inizio del tuo assalto hai il {assalto.aiutanti.proc:pct} di chiamare {assalto.aiutanti.aiutanti_extra} giallini. Ognuno viene registrato tra gli assaltatori recenti del clan con l\'ora dell\'attivazione: per 301 secondi conta come un compagno in tutti gli assalti del clan. Ogni nuova attivazione aggiunge un altro gruppo e gli stack scadono indipendentemente.",'
if old_frase not in frasi:
    raise SystemExit("Frase Giallo precedente non trovata")
frasi = frasi.replace(old_frase, new_frase, 1)
FRASI.write_text(frasi, encoding="utf-8")

print("Giallo convertito a stack condivisi tramite clan[last]")

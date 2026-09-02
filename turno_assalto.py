# -*- coding: utf-8 -*-
"""Logica di turno e assalto estratta da nft.py.

Il file viene eseguito nel namespace di ``nft.py`` per preservare esattamente
la catena storica di wrapper e tutte le dipendenze globali senza introdurre
import circolari. Non contiene avvio del bot, handler Telegram, arena o stanze
dungeon: qui vivono soltanto le implementazioni di ``turno``/``assedio`` e i
relativi helper/ondate.
"""

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
    nuc = clan[team].get("nucleo")
    numero_membri_clan = len(clan[team].get("membri", []))
    if nuc is not None:
        text += f"\nIl nucleo {nuc} sprigiona la sua forza!\n\n"
        cfg_nucleo = NUCLEI_CONFIG.get(nuc, {}).get("assalto", {})
        if not cfg_nucleo:
            print(nuc)
        for stat_nucleo, valore_per_membro in cfg_nucleo.get("stat_per_membro", {}).items():
            player[stat_nucleo] += numero_membri_clan * valore_per_membro
        if "cura_per_struttura" in cfg_nucleo:
            bacon = True
        cfg_necron = cfg_nucleo.get("resurrezione")
        if cfg_necron and num < (cfg_necron.get("proc", 0) / 100):
            necron = True

    # HP massimi dell'assalto: includono omini/set già applicati dal chiamante e il nucleo.
    hp_massimi_assalto = player["hp"]

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
            cfg_tridente = proc_cfg(set, "assalto", "tridente")
            danno_tridente = cfg_tridente["danno"]
            if target in nemico and nemico[target]["hp"] > cfg_tridente["hp_min"]:
                try:
                    indice_target = order.index(target)
                except ValueError:
                    indice_target = -1

                bersagli_tridente = order[indice_target:] if indice_target >= 0 else [target]
                for struttura_tridente in bersagli_tridente:
                    if danno_tridente <= 0:
                        break
                    if struttura_tridente not in nemico or struttura_tridente == "inguerra":
                        continue
                    nemico[struttura_tridente]["hp"] -= danno_tridente
                    player["fatto"] += danno_tridente
                    text += f"{nome} lancia il tridente fortissimo e colpisce {struttura_tridente} per {danno_tridente} danni!\n"
                    danno_tridente -= cfg_tridente["decremento"]
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

    # Incantesimi offensivi d'assalto.
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

    if "Bersaglio enorme" in list(nemico) and struttura_ok(num, "Bersaglio enorme", "generale", "distrazione_proc"):
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

    if clan[team].get("membri"):
        for pl in clan[team]['membri']:
            scheda_membro = playerg[pl]["scheda"]
            aniel = scheda_membro["anello"]

            if anello == "Polimerizzazione" and pl != nome and aniel == "Polimerizzazione":
                cfg_poly = anello_cfg("Polimerizzazione", "assalto", "polimerizzazione")
                bonus_poly = {}
                for stat_poly in cfg_poly["stats"]:
                    valore_poly = scheda_membro.get(stat_poly, 0) * cfg_poly["percento_stat"] / 100
                    player[stat_poly] += valore_poly
                    bonus_poly[stat_poly] = valore_poly
                text += (
                    f"La polimerizzazione di {pl} eccheggia, dandoti "
                    f"{_numero_placeholder_tecnico(bonus_poly['atk'])} atk "
                    f"{_numero_placeholder_tecnico(bonus_poly['def'])} def e "
                    f"{_numero_placeholder_tecnico(bonus_poly['agi'])} agilità!\n"
                )

            if (
                "Unione dello spirito" in player.get("incantamenti", [])
                and pl != nome
                and "Unione dello spirito" in get_ench(playerg[pl])
            ):
                cfg_unione = incantesimo_cfg("Unione dello spirito", "assalto", "unione")
                bonus_unione = {}
                for stat_unione in cfg_unione["stats"]:
                    valore_unione = scheda_membro.get(stat_unione, 0) * cfg_unione["percento_stat"] / 100
                    player[stat_unione] += valore_unione
                    bonus_unione[stat_unione] = valore_unione
                text += (
                    f"L'unione dello spirito di {pl} risuona, dandoti "
                    f"{_numero_placeholder_tecnico(bonus_unione['atk'])} atk "
                    f"{_numero_placeholder_tecnico(bonus_unione['def'])} def e "
                    f"{_numero_placeholder_tecnico(bonus_unione['agi'])} agilità!\n"
                )

            if aniel in PROC_ANELLI and "aura" in PROC_ANELLI[aniel].get("assalto", {}):
                cfg_anello = anello_cfg(aniel, "assalto", "aura")
                stat_anello = cfg_anello["stat"]
                stat_proprietario = scheda_membro.get(stat_anello, 0)
                valore_anello = max(
                    cfg_anello["minimo"],
                    stat_proprietario * cfg_anello["percento_stat"] / 100,
                )
                moltiplicatore = 1
                if set == "Portatore di morte":
                    moltiplicatore = proc_val(set, "assalto", "bonus_gadget", "moltiplicatore", 2)
                bonus_aura = valore_anello * moltiplicatore
                player[stat_anello] += bonus_aura
                bonus_testo = _numero_placeholder_tecnico(bonus_aura)
                text += f"L'anello di {pl} ti dona {bonus_testo} {stat_anello.upper()}!\n"

            if scheda_membro["set"] == "Re dei pirati" and pl != nome:
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
        player["atk"] += struttura_val("Fabbro incantaspade", "generale", "bonus_atk_per_livello") * clan[team]["villaggio"]["Fabbro incantaspade"]["lv"]
        player["def"] += struttura_val("Fabbro incantaspade", "generale", "bonus_def_per_livello") * clan[team]["villaggio"]["Fabbro incantaspade"]["lv"]
        if set == "Arciere di prima linea" and proc_ok(num, set, "assalto", "fabbro"):
            player["atk"] += proc_val(set, "assalto", "fabbro", "atk_per_livello") * clan[team]["villaggio"]["Fabbro incantaspade"]["lv"]
            player["def"] += proc_val(set, "assalto", "fabbro", "def_per_livello") * clan[team]["villaggio"]["Fabbro incantaspade"]["lv"]
            text += "Fabbro potenziato dal set "
        text += "⚔️"
    text += "\n"
    try:
        indice_target_ordine = order.index(target)
    except ValueError:
        indice_target_ordine = len(order)
    for difesa in order:

        if difesa in nemico:
            # Mente centrale: alieno per struttura attraversata.
            if set == "Mente centrale" and proc_ok(random.random(), set, "assalto", "alieno"):
                danno_alieno = round(player["atk"] / proc_val(set, "assalto", "alieno", "divisore_atk"))
                nemico[difesa]["hp"] -= danno_alieno
                player["fatto"] += danno_alieno
                text += f"👽 Un alieno della mente centrale colpisce {difesa} per {danno_alieno} danni!\n"
            text += "\n"
            if bacon:
                player["hp"] += NUCLEI_CONFIG["Nucleo di bacon instabile"]["assalto"]["cura_per_struttura"]
            if nemico[difesa]["hp"] <= 0:
                nemico.pop(difesa)
            else:
                defense = player["def"]
                dps = player["atk"]
                # Amletico: sacrificio vita per il singolo colpo d'assalto.
                if set == "Amletico" and proc_ok(random.random(), set, "assalto", "sacrificio"):
                    costo_amletico = max(1, round(max(0, player["hp"]) * proc_val(set, "assalto", "sacrificio", "percento_hp") / 100))
                    player["hp"] -= costo_amletico
                    dps += costo_amletico
                    text += f"🎭 {nome} sacrifica {costo_amletico} HP e li trasforma in attacco!\n"
                agi = player["agi"]
                attaccon = (starmi[difesa]["atk"] + starmi[difesa]["atk"] * (nemico[difesa]["lv"] / struttura_val("generale", "scaling", "divisore_livello")) + bonus["atk"])
                difesan = (starmi[difesa]["def"] + starmi[difesa]["def"] * (nemico[difesa]["lv"] / struttura_val("generale", "scaling", "divisore_livello")) + bonus["def"])
                agin = (starmi[difesa]["agi"] + starmi[difesa]["agi"] * (nemico[difesa]["lv"] / struttura_val("generale", "scaling", "divisore_livello")) + bonus["agi"])

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
                    attaccon += struttura_val("generale", "ultima_struttura", "atk_delta")
                    agin += struttura_val("generale", "ultima_struttura", "agi_delta")
                    difesan += struttura_val("generale", "ultima_struttura", "def_delta")
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
                                agin += struttura_val("Clone", "modalita", "Difensivo", "agi_delta")
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
                    agin += struttura_val("Sedimento del cucciolo", "modalita", "Affamato", "agi_delta")
                    text += "__Si sente un gorgoglio...__\n"
                    attaccon = attaccon // struttura_val("Sedimento del cucciolo", "modalita", "Affamato", "atk_divisore")

                elif setting["Spuntone malefico"] == "Sotterraneo" and difesa == "Spuntone malefico":
                    text += "Stranamente lo spuntone non è qui!\n"
                    agin += struttura_val("Spuntone malefico", "modalita", "Sotterraneo", "agi_delta")

                elif setting["Stazione laser di sicurezza"] == "Difesa laser" and difesa == "Stazione laser di sicurezza":
                    old = attaccon
                    attaccon = difesan * struttura_val("Stazione laser di sicurezza", "modalita", "Difesa laser", "atk_da_def_mul")
                    difesan = old // struttura_val("Stazione laser di sicurezza", "modalita", "Difesa laser", "def_da_atk_divisore")
                    text += "La difesa laser si alza sotto la stazione!\n"

                elif setting["Stazione laser di sicurezza"] == "Suicidio laser" and difesa == "Stazione laser di sicurezza":
                    nemico[difesa]["hp"] -= struttura_val("Stazione laser di sicurezza", "modalita", "Suicidio laser", "autodanno")
                    attaccon = round(attaccon * struttura_val("Stazione laser di sicurezza", "modalita", "Suicidio laser", "atk_mul"))
                    agin += struttura_val("Stazione laser di sicurezza", "modalita", "Suicidio laser", "agi_delta")

                    text += "La torre laser si sovraccarica!\n"

                colpito = round(agi - (agin / struttura_val("generale", "tiro", "agi_difensore_divisore")) + struttura_val("generale", "tiro", "bonus"))

                if colpito > random.randint(0, struttura_val("generale", "tiro", "random_max")):
                    if setting["Sedimento del cucciolo"] == "Affamato" and difesa == "Sedimento del cucciolo":
                        text += "Il cucciolo di drago sta mangiando altro..\n"
                    elif setting["Spuntone malefico"] == "Sotterraneo" and difesa == "Spuntone malefico":
                        text += "No, nessuno spuntone!\n"
                    elif setting["Chiesa"] == "Orribile" and difesa == "Chiesa":
                        if struttura_ok(num, "Chiesa", "modalita", "Orribile", "creatura_proc"):
                                    num = random.random()
                                    bonus["atk"] += struttura_val("Chiesa", "modalita", "Orribile", "bonus_atk")
                                    bonus["def"] += struttura_val("Chiesa", "modalita", "Orribile", "bonus_def")
                                    bonus["agi"] += struttura_val("Chiesa", "modalita", "Orribile", "bonus_agi")
                                    text += f"Una creatura orribile esce dalla chiesa, pronta seminare il chaos!\n"
                        else:
                            text += "Un antica creatura riposa nella chiesa\n"
                    else:
                        text += frasi["miss"][difesa]
                    if difesa == "Muraglione extra":
                        bonus["def"] += struttura_val("Muraglione extra", "generale", "bonus_def_per_livello") * (nemico[difesa]["lv"] + (len(nemico) / struttura_val("Muraglione extra", "generale", "bonus_def_strutture_divisore")))
                    elif difesa == "Spuntone malefico":
                        text += "\n**Si apre al volo una botola sotto i tuoi piedi!**\n"
                        for x in range(nemico[difesa]["lv"]):
                            num = random.random()
                            if setting["Spuntone malefico"] == "Sotterraneo":
                                num += struttura_val("Spuntone malefico", "modalita", "Sotterraneo", "roll_bonus_pct") / 100
                            if (struttura_val("Spuntone malefico", "generale", "stop_proc") / 100) > num:
                                break
                            else:
                                if defense < 0:
                                    attaccon -= defense
                                    defense = 0
                                dannissimi = struttura_danno(attaccon, defense, "spuntone")
                                player["hp"] -= dannissimi
                                if set == "Oscurato" and difesa in nemico and isinstance(nemico.get(difesa), dict):
                                    riflesso_oscuro = round(max(0, dannissimi) * proc_val("Oscurato", "assalto", "riflesso", "percento") / 100)
                                    if riflesso_oscuro > 0:
                                        nemico[difesa]["hp"] -= riflesso_oscuro
                                        player["fatto"] = player.get("fatto", 0) + riflesso_oscuro
                                        text += f"🌑 Il dolore torna indietro: {riflesso_oscuro} danni riflessi a {difesa}!\n"
                                nos = player["hp"]
                                text += f"Cade così sul {x+1}° spuntone! ({nos})\n"
                            if set == "Cavaliere delle spine" and proc_ok(num, set, "assalto", "spuntone_schivato"):
                                text += f"\n{nome} prende spuntoni extra per la sua armatura e prosegue!\n"
                                player["def"] += proc_val(set, "assalto", "spuntone_schivato", "def")
                                player["atk"] += proc_val(set, "assalto", "spuntone_schivato", "atk")
                                player["hp"] += dannissimi
                    elif difesa == "Clone":
                        text += f"{nomeclone} non riesce a farti nulla, ma direziona le difese verso di te!\n"
                        bonus["atk"] += struttura_val("Clone", "generale", "bonus_atk_difese_su_mancato_colpo")
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
                                            player["fatto"] += struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])
                                            if nemico[dife]["hp"] > struttura_val("Centrale di cura centralizzata", "generale", "hp_minimo_modifica"):
                                                nemico[dife]["hp"] += -struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])
                                else:
                                    text += (
                                        f"La centrale cura tutte le difese!\n"
                                    )
                                    for dife in nemico:
                                        if dife == "inguerra":
                                            pass
                                        else:
                                            nemico[dife]["hp"] += struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])
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
                                            player["fatto"] += struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])
                                            if nemico[news]["hp"] > struttura_val("Centrale di cura centralizzata", "generale", "hp_minimo_modifica"):
                                                nemico[news]["hp"] += -struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])
                                else:
                                    text += (
                                        f"La centrale cura {news}!\n"
                                    )
                                    for dife in nemico:
                                        if dife == "inguerra":
                                            pass
                                        else:
                                            nemico[news]["hp"] += struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])

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

                                        player["fatto"] += struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])
                                        if nemico[dife]["hp"] > struttura_val("Centrale di cura centralizzata", "generale", "hp_minimo_modifica"):
                                            nemico[dife]["hp"] += -struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])
                            else:

                                news = random.choice(list(nemico))
                                text += (
                                        f"La centrale di cura danneggia {news}!\n"
                                    )
                                for dife in nemico:
                                        if dife == "inguerra":
                                            pass
                                        else:
                                            player["fatto"] += struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])
                                            if nemico[news]["hp"] > struttura_val("Centrale di cura centralizzata", "generale", "hp_minimo_modifica"):
                                                nemico[news]["hp"] += -struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])
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
                                defense *= struttura_val("Muraglione extra", "generale", "def_attaccante_mul")

                            if defense < 0:
                                attaccon -= defense
                                defense = 0

                            dannissimi = struttura_danno(attaccon, defense, "difesa")

                            if setting["Accampamento"] == "Trappole demoralizzanti" and difesa == "Accampamento":
                                dannissimi = dannissimi // struttura_val("Accampamento", "modalita", "Trappole demoralizzanti", "danno_divisore")

                            elif setting["Cane da guardia"] == "Cane rapido" and difesa == "Cane da guardia":
                                dannissimi = round(dannissimi // struttura_val("Cane da guardia", "modalita", "Cane rapido", "danno_divisore"))
                            elif setting["Cane da guardia"] == "Orso" and difesa == "Cane da guardia":
                                dannissimi = round(dannissimi * struttura_val("Cane da guardia", "modalita", "Orso", "danno_mul"))

                            elif setting["Cannoncino"] == "Danneggiante" and difesa == "Cannoncino":
                                dannissimi = dannissimi * struttura_val("Cannoncino", "modalita", "Danneggiante", "danno_mul")
                                text += "BOOM!\n"


                            elif setting["Muraglione extra"] == "Infiammato" and difesa == "Muraglione extra":
                                dannissimi += struttura_val("Muraglione extra", "modalita", "Infiammato", "danno_bonus")
                                nemico[difesa]["hp"] -= struttura_val("Muraglione extra", "modalita", "Infiammato", "autodanno")

                            if dannissimi <= 0:
                                dannissimi = struttura_val("generale", "danno_minimo")

                            if setting["Fabbro incantaspade"] == "Curativo" and difesa == "Fabbro incantaspade":
                                dannissimi = 0
                            elif setting["Chiesa"] == "Orribile" and difesa == "Chiesa":
                                dannissimi = 0
                                text += "La chiesa pare contenere un antico male...\n"

                            player["hp"] -= dannissimi
                            if set == "Oscurato" and difesa in nemico and isinstance(nemico.get(difesa), dict):
                                riflesso_oscuro = round(max(0, dannissimi) * proc_val("Oscurato", "assalto", "riflesso", "percento") / 100)
                                if riflesso_oscuro > 0:
                                    nemico[difesa]["hp"] -= riflesso_oscuro
                                    player["fatto"] = player.get("fatto", 0) + riflesso_oscuro
                                    text += f"🌑 Il dolore torna indietro: {riflesso_oscuro} danni riflessi a {difesa}!\n"
                            nos = player["hp"]

                        else:
                            nos = 0
                            dannissimi = 0
                        try:
                            if setting["Accampamento"] == "Trappole demoralizzanti" and difesa == "Accampamento":
                                bonus["atk"] += struttura_val("Accampamento", "modalita", "Trappole demoralizzanti", "bonus_atk_difese")
                                text += f"Delle trappole escono a iosa dalle tende, infliggendo {dannissimi} danni ({nos})\n"
                            elif setting["Chiesa"] == "Orribile" and difesa == "Chiesa":
                                if struttura_ok(num, "Chiesa", "modalita", "Orribile", "creatura_proc"):
                                    num = random.random()
                                    bonus["atk"] += struttura_val("Chiesa", "modalita", "Orribile", "bonus_atk")
                                    bonus["def"] += struttura_val("Chiesa", "modalita", "Orribile", "bonus_def")
                                    bonus["agi"] += struttura_val("Chiesa", "modalita", "Orribile", "bonus_agi")
                                    text += f"Una creatura orribile esce dalla chiesa, pronta seminare il chaos!\n"

                            elif setting["Fabbro incantaspade"] == "Curativo" and difesa == "Fabbro incantaspade":
                                news = random.choice(list(nemico))
                                dannissimi = struttura_danno(attaccon, defense, "difesa")
                                nemico[news]["hp"] += dannissimi
                                nos = nemico[news]["hp"]
                                text += f"Il fabbro ripara un poco {news} per {dannissimi} hp, ne ha ora {nos}\n"

                            elif setting["Spaventapasseri ornamentale"] == "Animato" and difesa == "Spaventapasseri ornamentale":

                                dannissimi = struttura_danno(attaccon, defense, "difesa")
                                if dannissimi <= 0:
                                    dannissimi = struttura_val("generale", "danno_minimo")

                                player["hp"] -= dannissimi
                                if set == "Oscurato" and difesa in nemico and isinstance(nemico.get(difesa), dict):
                                    riflesso_oscuro = round(max(0, dannissimi) * proc_val("Oscurato", "assalto", "riflesso", "percento") / 100)
                                    if riflesso_oscuro > 0:
                                        nemico[difesa]["hp"] -= riflesso_oscuro
                                        player["fatto"] = player.get("fatto", 0) + riflesso_oscuro
                                        text += f"🌑 Il dolore torna indietro: {riflesso_oscuro} danni riflessi a {difesa}!\n"
                                nos = player["hp"]

                                text += f"Lo spaventapasseri ti colpisce alle spalle per {dannissimi} danni!({nos})\n"

                            else:
                                text += frasi["preso"][difesa]%(dannissimi,nos)

                        except:
                            text += frasi["preso"][difesa]

                        if difesa == "Muraglione extra":
                            bonus["def"] += struttura_val("Muraglione extra", "generale", "bonus_def_per_livello") * (nemico[difesa]["lv"] + (len(nemico) / struttura_val("Muraglione extra", "generale", "bonus_def_strutture_divisore")))
                            if difesa == "Muraglione extra" and struttura_ok(num, "Muraglione extra", "generale", "infezione_proc"):
                                text += "__Il taglio ha fatto una brutta infezione...__\n"
                                player["def"] += struttura_val("Muraglione extra", "generale", "infezione_def_delta")
                        elif difesa == "Spaventapasseri ornamentale" and struttura_ok(num, "Spaventapasseri ornamentale", "modalita", "Magico", "corvi_proc") and setting["Spaventapasseri ornamentale"] != "Animato":
                            text += "Sembra che lo spaventapasseri non sia così inutile, sta facendo cose?\n\nODDIO MA COSA SONO TUTTI QUI CORVI!"
                            break
                        elif difesa == "Stazione laser di sicurezza" and struttura_ok(num, "Stazione laser di sicurezza", "generale", "bonus_def_proc"):
                            bonus["def"] += struttura_val("Stazione laser di sicurezza", "generale", "bonus_def_per_livello") * nemico[difesa]["lv"]
                        elif difesa == "Cane da guardia" and struttura_ok(num, "Cane da guardia", "generale", "rincorsa_proc") and setting["Cane da guardia"] != "Orso":
                            text += f"{nome} non è abbastanza veloce ed il cane lo riinsegue,subendo così altri {dannissimi} danni!\n"
                            player["hp"] -= dannissimi
                            if set == "Oscurato" and difesa in nemico and isinstance(nemico.get(difesa), dict):
                                riflesso_oscuro = round(max(0, dannissimi) * proc_val("Oscurato", "assalto", "riflesso", "percento") / 100)
                                if riflesso_oscuro > 0:
                                    nemico[difesa]["hp"] -= riflesso_oscuro
                                    player["fatto"] = player.get("fatto", 0) + riflesso_oscuro
                                    text += f"🌑 Il dolore torna indietro: {riflesso_oscuro} danni riflessi a {difesa}!\n"
                            num = random.random()
                            dannissimi = round(dannissimi // struttura_val("Cane da guardia", "generale", "rincorsa_danno_divisore"))
                            for g in range(struttura_val("Cane da guardia", "modalita", "Cane rapido", "rincorse_extra_max")):
                                if difesa == "Cane da guardia" and struttura_ok(num, "Cane da guardia", "modalita", "Cane rapido", "rincorsa_extra_proc") and setting["Cane da guardia"] == "Cane rapido":
                                    text += f"{nome} non è ancora abbastanza veloce ed il cane lo riinsegue,subendo così altri {dannissimi} danni!\n"
                                    player["hp"] -= dannissimi
                                    if set == "Oscurato" and difesa in nemico and isinstance(nemico.get(difesa), dict):
                                        riflesso_oscuro = round(max(0, dannissimi) * proc_val("Oscurato", "assalto", "riflesso", "percento") / 100)
                                        if riflesso_oscuro > 0:
                                            nemico[difesa]["hp"] -= riflesso_oscuro
                                            player["fatto"] = player.get("fatto", 0) + riflesso_oscuro
                                            text += f"🌑 Il dolore torna indietro: {riflesso_oscuro} danni riflessi a {difesa}!\n"
                                else:
                                    break

                        elif difesa == "Cannoncino" and setting["Cannoncino"] != "Danneggiante":
                            bonus["agi"] += struttura_val("Cannoncino", "generale", "bonus_agi_difese")
                            if struttura_ok(num, "Cannoncino", "generale", "drago_proc"):
                                text += f"**Sbaglio o questo colpo ha svegliato un drago nelle circostanze?**\n"
                                bonus["agi"] += struttura_val("Cannoncino", "generale", "drago_bonus_agi")

                        elif difesa == "Spuntone malefico":
                            bonus["def"] += struttura_val("Spuntone malefico", "generale", "bonus_def_per_livello") * nemico[difesa]["lv"]

                        elif difesa == "Sedimento del cucciolo" and struttura_ok(num, "Sedimento del cucciolo", "generale", "mamma_proc"):
                            text += f"**Il drago ancora spaventato richiama la mamma, che altro che sparare fuoco, schiaccia {nome}!**\n"
                            player["hp"] = random.randint(struttura_val("Sedimento del cucciolo", "generale", "mamma_hp_min"), struttura_val("Sedimento del cucciolo", "generale", "mamma_hp_max"))

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
                                            player["fatto"] += struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])
                                            if nemico[dife]["hp"] > struttura_val("Centrale di cura centralizzata", "generale", "hp_minimo_modifica"):
                                                nemico[dife]["hp"] += -struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])
                                else:
                                    news = random.choice(list(nemico))
                                    text += (
                                            f"La centrale di cura danneggia {news}!\n"
                                        )
                                    for dife in nemico:
                                            if dife == "inguerra":
                                                pass
                                            else:
                                                nemico[news]["hp"] += -struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])
                            else:
                                if setting["Centrale di cura centralizzata"] == "Sparsa":
                                    text += "Cure a non finire sgorgano per l'intero villaggio!\n"
                                    for dife in nemico:
                                        if dife == "inguerra":
                                            pass
                                        else:

                                            player["fatto"] += struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])
                                            if nemico[dife]["hp"] > struttura_val("Centrale di cura centralizzata", "generale", "hp_minimo_modifica"):
                                                nemico[dife]["hp"] += struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])
                                else:
                                    news = random.choice(list(nemico))
                                    text += (
                                            f"La centrale di cura cura {news}!\n"
                                        )
                                    for dife in nemico:
                                            if dife == "inguerra":
                                                pass
                                            else:
                                                nemico[news]["hp"] += struttura_val("Centrale di cura centralizzata", "generale", "valore_per_livello") * int(nemico[difesa]["lv"])

                    if set != None:
                        if set == "Sopravvissuto" and proc_ok(num, set, "assalto", "sopravvive"):
                            text += "Sopravvissuto ancora!\n"
                            player["atk"] += dannissimi / proc_val(set, "assalto", "sopravvive", "atk_divisore")
                        elif set == "Sanguinolento" and proc_ok(num, set, "assalto", "sangue"):
                            player["atk"] += dannissimi / proc_val(set, "assalto", "sangue", "divisore_atk")
                            player["def"] += dannissimi / proc_val(set, "assalto", "sangue", "divisore_def")
                            text += f"**{nome} si potenzia con il sangue sul campo di battaglia!**\n"

                        elif (
                            set == "Orrido"
                            and order.index(difesa) < indice_target_ordine
                            and proc_ok(num, set, "assalto", "sgignolo")
                        ):
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
                            dps += dps * proc_val(set, "assalto", "muraglione", "moltiplicatore_extra")

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
                        dannissimi = struttura_danno(dps, difesan, "attaccante")

                        if set == "Cavaliere d'argento":
                            cfg_argento = proc_cfg(set, "assalto", "danno_fisso")
                            danno_argento = round(max(
                                hp_massimi_assalto / cfg_argento["hp_massimi_divisore"],
                                cfg_argento["danno_minimo"],
                            ))
                            dannissimi += danno_argento

                        elif set == "Orrido":
                            dannissimi = proc_val(set, "assalto", "sgignolo", "danno")
                        player["fatto"] += dannissimi

                        if dannissimi <= 0:
                            dannissimi *= -1
                        num = random.random()
                        if setting["Bersaglio enorme"] == "Movibile" and not struttura_ok(num, "Bersaglio enorme", "modalita", "Movibile", "colpito_proc") and target == "Bersaglio enorme":
                            dannissimi = 0
                            text += "**Il bersaglio si sposta all'ultimo!**\n"

                        if setting["Bersaglio enorme"] == "Movibile" and target == "Bersaglio enorme":
                            dannissimi *= struttura_val("Bersaglio enorme", "modalita", "Movibile", "danno_mul")

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
    # Armadillibilità è un trigger di morte e si risolve prima delle resurrezioni.
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
        text += f"\n**Questa disfatta non basta per far desistere {nome}, che anzi si rialza pronto a combattere!\n"
        player["hp"] = proc_val(set, "assalto", "resurrezione", "hp")

    elif necron and player["hp"] <= 0:
        text += "\n**Il nucleo necron sprigiona un aura oscura che riporta in vita il malcapitato, per ora...**"
        player["hp"] = NUCLEI_CONFIG["Nucleo Necron instabile"]["assalto"]["resurrezione"]["hp"]

    elif (set == "Guardiano del passaggio" and player["hp"] <= 0 and proc_ok(num, set, "assalto", "resurrezione")):
        text += f"\n**{nome} ritorna dalla morte, pronto a combattere ancora!\n"
        player["hp"] = proc_val(set, "assalto", "resurrezione", "hp")

    elif set == "Fiamma pura" and player["hp"] <= 0 and proc_ok(num, set, "assalto", "esplosione_morte"):
        text += f"\n{nome} esplode in un esplosione di fuoco dannegiando tutte le strutture!"
        cfg_fiamma = proc_cfg(set, "assalto", "esplosione_morte")
        danno_fiamma = round(max(
            hp_massimi_assalto / cfg_fiamma["hp_massimi_divisore"],
            cfg_fiamma["danno_minimo"],
        ))
        for dife in list(nemico):
            if dife == "inguerra":
                continue
            if nemico[dife]["hp"] > danno_fiamma:
                nemico[dife]["hp"] -= danno_fiamma
                player["fatto"] += danno_fiamma

    return text


def turno(main, oppo,cond=None):
    text = str()
    nome1 = main["Nome"]
    nome2 = oppo["Nome"]

    text += _applica_valvola_inizio_sfida(main)
    text += _applica_valvola_inizio_sfida(oppo)

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

    text += _effetti_anelli_inizio_turno(main, oppo, anello, anellon)
    if main["hp"] <= 0 or oppo["hp"] <= 0:
        return text

    dps = main["atk"]
    difesan = oppo["def"]

    agi = main["agi"]
    agin = oppo["agi"]

    if anello == "Anello perfezionista" or anellon == "Anello perfezionista":
            random.seed(PROC_ANELLI["Anello perfezionista"]["generale"]["seed"])
    set = main.get("set",None)
    setN = oppo.get("set",None)

    # Incantesimi che devono risolversi prima di qualsiasi abilità di set.
    # Cangiante assegna il set alla sola copia di combattimento.
    if "Cangiante" in main.get("incantamenti", []) and incantesimo_ok(random.random(), "Cangiante", "turno", "attacco"):
        set = random.choice(set_cangiante_disponibili())
        main["set"] = set
        if set == "Paladino":
            main.setdefault("Scudo", 0)
        text += f"Per {nome1} è ora di comportarsi come {set}!\n"

    if "Cangiante" in oppo.get("incantamenti", []) and incantesimo_ok(random.random(), "Cangiante", "turno", "difesa"):
        setN = random.choice(set_cangiante_disponibili())
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


    if _tiro_schivata_seconda_ondata(possibile, oppo):
        text += f"{nome2} schiva il colpo di {nome1}\n"
        oppo["schivato"] = True
        if anellon == "Dance Dance Revolution":
            incremento_combo = anello_val(anellon, "turno", "combo", "incremento")
            oppo["_ddr_combo"] = oppo.get("_ddr_combo", 0) + incremento_combo
            text += f"CCCompo a {oppo['_ddr_combo']}!\n"
        if anello == "WuWuWuuurm" and anello_ok(random.random(), anello, "turno", "presa_schivata"):
            cfg_wurm = anello_cfg(anello, "turno", "presa_schivata")
            atk_wurm = cfg_wurm["atk_base"] + (main.get("int", 0) if cfg_wurm.get("aggiungi_int", True) else 0)
            def_wurm = max(0, difesan)
            danni_wurm = random.uniform(
                atk_wurm * (100 / ((100 + def_wurm * 1.5) + 1)),
                atk_wurm * (100 / ((100 + def_wurm) + 1)),
            )
            danni_wurm = round(max(cfg_wurm["danno_min"], danni_wurm))
            oppo["hp"] -= danni_wurm
            text += f"Il wurm prende al volo {nome2}, mordendolo per {danni_wurm} danni!\n"
        if anello == "Coda demoniaca":
            oppo["lastD"] = anello_val(anello, "turno", "schivata", "lastD_reset")
        mod = 0
        danno = 0

    else:
        oppo["schivato"] = False
        if anellon == "Dance Dance Revolution" and oppo.get("_ddr_combo", 0) > 0:
            oppo["_ddr_combo"] = 0
            text += "CCCompo persa!\n"
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
    formula_gdr = anello == "GDR semplificato" or anellon == "GDR semplificato"
    if formula_gdr:
        danno = max(anello_val("GDR semplificato", "turno", "formula", "danno_min", 0), dps - difesan)
        if mod > 0:
            mod = 1
    else:
        danno = random.uniform(
                    dps * (100 / ((100 + difesan * 1.5)+1)), dps * (100 / ((100 + difesan)+1))
                )
        if danno <= 20:
            danno = 20

    if anello == "Dance Dance Revolution" and mod > 0:
        combo_ddr = main.get("_ddr_combo", 0)
        if combo_ddr > 0:
            bonus_combo = anello_val(anello, "turno", "combo", "bonus_danno_per_combo_pct")
            danno *= 1 + ((combo_ddr * bonus_combo) / 100)

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


    formula_tag = "F" if formula_gdr else ""
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
    elif set == 'Avventuriero delle praterie' and proc_ok(1 - num, set, "turno", "respira"):
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
                    text += f"{nome1} infligge {dannov}{formula_tag} danno allo scudo di {nome2} ({vita} scudo)!\n"
                    if oppo["Scudo"] <= 0:
                        text += "**Lo scudo si è rotto!**\n"
            else:
                    oppo["hp"] -= round(float(danno) * mod)
                    vita = oppo["hp"]
                    dannov = round(danno * mod)
                    text += f"{nome1} infligge {dannov}{formula_tag} danni a {nome2} ({vita})!\n"

            if set == "Shogun moderno":

                    if proc_ok(num, set, "turno", "doppio_colpo"):
                        text += "**Doppio colpo**\n"
                        if setN == "Paladino" and oppo["Scudo"] >= 0:

                            oppo["Scudo"] -= round(float(danno) * random.uniform(proc_val(set, "turno", "doppio_colpo", "moltiplicatore_min"), proc_val(set, "turno", "doppio_colpo", "moltiplicatore_max")))
                            vita = oppo["Scudo"]
                            text += f"{nome1} infligge {dannov}{formula_tag} danno allo scudo di {nome2} ({vita} scudo)!\n"
                            if oppo["Scudo"] <= 0:
                                text += "**Lo scudo si è rotto!**\n"
                        else:
                            new_m = random.uniform(proc_val(set, "turno", "doppio_colpo", "moltiplicatore_min"), proc_val(set, "turno", "doppio_colpo", "moltiplicatore_max"))
                            oppo["hp"] -= round(float(danno) * new_m)
                            vita = oppo["hp"]
                            dannov = round(danno * new_m)
                            text += f"{nome1} infligge {dannov}{formula_tag} danni a {nome2} ({vita})!\n"

            if set == "Manipolatore di morte" and proc_ok(num, set, "turno", "scheletri"):
                    text += f"\n**{nome1} evoca una marea di scheletri ad attaccare!**\n"
                    scheletri = cura = round((proc_val(set, "turno", "scheletri", "hp_riferimento") - main["hp"]) / proc_val(set, "turno", "scheletri", "hp_per_scheletro"))
                    new_m = mod
                    for x in range(scheletri):

                        if setN == "Paladino" and oppo["Scudo"] >= 0:

                            new_m = random.uniform(proc_val(set, "turno", "scheletri", "mod_min"), proc_val(set, "turno", "scheletri", "mod_max"))
                            oppo["Scudo"] -= round(float(danno) * new_m)

                            vita = oppo["Scudo"]
                            text += f"Uno scheletrino infligge {dannov}{formula_tag} danno allo scudo di {nome2} ({vita} scudo)!\n"
                            if oppo["Scudo"] <= 0:
                                text += "**Lo scudo si è rotto!**\n"
                            danno += proc_val(set, "turno", "scheletri", "crescita_danno_scudo")
                        else:
                            new_m = random.uniform(proc_val(set, "turno", "scheletri", "mod_min"), proc_val(set, "turno", "scheletri", "mod_max"))
                            oppo["hp"] -= round(float(danno) * new_m)

                            vita = oppo["hp"]
                            dannov = round(danno * new_m)
                            text += f"Uno scheletrino infligge {dannov}{formula_tag} danni a {nome2} ({vita})!\n"
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


_turno_eroi_base = turno
_assedio_eroi_base = assedio

def _nomi_pve_conosciuti():
    nomi = set()
    for raccolta in (Boss, nemici, Nautici):
        try:
            valori = raccolta.values()
        except Exception:
            continue
        for dati in valori:
            if isinstance(dati, dict) and dati.get("Nome"):
                nomi.add(dati["Nome"])
    return nomi

def _e_sfida_pvp(main, oppo, cond):
    # I flussi PvP principali passano sempre un cond (anche stringa vuota).
    # Il fallback sui nomi copre le amichevoli storiche che chiamano turno() senza cond.
    pve = _nomi_pve_conosciuti()
    if main.get("Nome") in pve or oppo.get("Nome") in pve:
        return False
    return True

def _prepara_set_pvp(personaggio):
    text = ""
    nome_set = personaggio.get("set")

    if nome_set == "Guerriero Temporale":
        cfg = proc_cfg(nome_set, "sfida", "ciclo_temporale")
        if not personaggio.get("_temporale_inizializzato"):
            personaggio["hp"] = cfg["hp"]
            personaggio["_temporale_resurrezioni"] = 0
            personaggio["_temporale_inizializzato"] = True
            text += f"⏳ {personaggio['Nome']} entra nel ciclo temporale con {cfg['hp']} HP!\\n"
        elif personaggio["hp"] > cfg["hp"]:
            personaggio["hp"] = cfg["hp"]

    if nome_set == "Dannato primordiale" and not personaggio.get("_dannato_conversione"):
        difesa = personaggio.get("def", 0)
        personaggio["atk"] += difesa
        personaggio["def"] = 0
        personaggio["_dannato_conversione"] = True
        text += f"😈 {personaggio['Nome']} converte {difesa} DEF in ATK!\\n"

    if nome_set == "Monarca della tempesta di fuoco" and not personaggio.get("_monarca_inizializzato"):
        innati = proc_val(nome_set, "sfida", "incantamenti", "nomi", [])
        incantamenti = personaggio.setdefault("incantamenti", [])
        for incantesimo in innati:
            if incantesimo not in incantamenti:
                incantamenti.append(incantesimo)
        personaggio["_monarca_inizializzato"] = True

    return text

def _resurrezione_temporale(personaggio):
    if personaggio.get("set") != "Guerriero Temporale" or personaggio.get("hp", 0) > 0:
        return ""
    cfg = proc_cfg("Guerriero Temporale", "sfida", "ciclo_temporale")
    usate = personaggio.get("_temporale_resurrezioni", 0)
    if usate >= cfg["resurrezioni"]:
        return ""
    usate += 1
    personaggio["_temporale_resurrezioni"] = usate
    personaggio["hp"] = cfg["hp"]
    return f"⏳ {personaggio['Nome']} riavvolge il tempo e rivive! ({usate}/{cfg['resurrezioni']})\\n"

def _oggetto_accumulatore():
    oggetti = proc_val("Accumulatore di meraviglie", "sfida", "evocazione", "oggetti", {})
    nomi = list(oggetti)
    pesi = [1 / max(1, oggetti[nome]) for nome in nomi]
    scelto = random.choices(nomi, weights=pesi, k=1)[0]
    return scelto, oggetti[scelto]

def _danno_normale_macellatore(main, oppo):
    dps = max(0, float(main.get("atk", 0)))
    difesa = max(0, float(oppo.get("def", 0)))
    minimo = dps * (100 / ((100 + difesa * 1.5) + 1))
    massimo = dps * (100 / ((100 + difesa) + 1))
    danno = random.uniform(minimo, massimo)
    return max(20, danno)

def turno(main, oppo, cond=None):
    if not _e_sfida_pvp(main, oppo, cond):
        return _turno_eroi_base(main, oppo, cond)

    prefisso = _prepara_set_pvp(main) + _prepara_set_pvp(oppo)

    # Il Guerriero Temporale non può mai conservare cure oltre il proprio tetto di 100 HP.
    for combattente in (main, oppo):
        if combattente.get("set") == "Guerriero Temporale":
            combattente["hp"] = min(combattente["hp"], proc_val("Guerriero Temporale", "sfida", "ciclo_temporale", "hp"))

    # Anima della festa recupera un seguace a ogni proprio turno.
    if main.get("set") == "Anima della festa":
        cfg = proc_cfg("Anima della festa", "sfida", "seguaci")
        if "_anima_festa_base" not in main:
            main["_anima_festa_base"] = {stat: main.get(stat, 0) for stat in ("hp", "atk", "def", "agi")}
        main["_anima_festa_seguaci"] = main.get("_anima_festa_seguaci", 0) + cfg["seguaci_per_turno"]
        for stat in ("hp", "atk", "def", "agi"):
            main[stat] += main["_anima_festa_base"][stat] * cfg["percento_stat_per_seguace"] / 100
        prefisso += f"🎉 {main['Nome']} recupera un seguace! ({main['_anima_festa_seguaci']} seguaci)\\n"

    # Mecha sciamano: costo fisso e nuovo passaggio sul moltiplicatore dell'approccio.
    if main.get("set") == "Mecha sciamano":
        costo = proc_val("Mecha sciamano", "sfida", "riuso_approccio", "danno_hp")
        main["hp"] -= costo
        try:
            boost(main, Approcci)
        except Exception:
            pass
        prefisso += f"🤖 {main['Nome']} perde {costo} HP e riusa {main.get('Ap', 'Base')}!\\n"

    # Amletico: il bonus ATK vale solo per questo attacco.
    bonus_amletico = 0
    if main.get("set") == "Amletico" and proc_ok(random.random(), "Amletico", "sfida", "sacrificio"):
        pct = proc_val("Amletico", "sfida", "sacrificio", "percento_hp")
        bonus_amletico = max(1, round(max(0, main["hp"]) * pct / 100))
        main["hp"] -= bonus_amletico
        main["atk"] += bonus_amletico
        prefisso += f"🎭 {main['Nome']} sacrifica {bonus_amletico} HP e li aggiunge al proprio ATK!\\n"

    # Accumulatore: ogni possessore tira indipendentemente nel turno in cui attacca/difende.
    oggetto_attacco = None
    oggetto_difesa = None
    if main.get("set") == "Accumulatore di meraviglie" and proc_ok(random.random(), "Accumulatore di meraviglie", "sfida", "evocazione"):
        oggetto_attacco = _oggetto_accumulatore()
    if oppo.get("set") == "Accumulatore di meraviglie" and proc_ok(random.random(), "Accumulatore di meraviglie", "sfida", "evocazione"):
        oggetto_difesa = _oggetto_accumulatore()

    hp_oppo_prima = oppo.get("hp", 0)
    testo = _turno_eroi_base(main, oppo, cond)

    if bonus_amletico:
        main["atk"] -= bonus_amletico

    danno_corrente = max(0, hp_oppo_prima - oppo.get("hp", 0))
    if oggetto_attacco is not None:
        nome_oggetto, valore = oggetto_attacco
        if danno_corrente > 0:
            oppo["hp"] -= valore
            main["fatto"] = main.get("fatto", 0) + valore
            testo += f"🧳 Il tuo colpo è potenziato da {nome_oggetto}: +{valore} danni!\\n"
        else:
            testo += f"🧳 {nome_oggetto} esce dalla valigia, ma il colpo non arriva a segno.\\n"

    if oggetto_difesa is not None:
        nome_oggetto, valore = oggetto_difesa
        danno_totale = max(0, hp_oppo_prima - oppo.get("hp", 0))
        ridotto = min(valore, danno_totale)
        if ridotto > 0:
            oppo["hp"] += ridotto
            main["fatto"] = max(0, main.get("fatto", 0) - ridotto)
            testo += f"🧳 Il colpo nemico è ridotto grazie all'uso di {nome_oggetto}: -{ridotto} danni!\\n"
        else:
            testo += f"🧳 {nome_oggetto} viene evocato, ma non c'è danno da ridurre.\\n"

    # Macellatore punisce una schivata appena risolta.
    if main.get("set") == "Macellatore" and oppo.get("schivato") is True and proc_ok(random.random(), "Macellatore", "sfida", "presa_schivata"):
        mol = proc_val("Macellatore", "sfida", "presa_schivata", "moltiplicatore_danno")
        danno = round(_danno_normale_macellatore(main, oppo) * mol)
        oppo["hp"] -= danno
        main["fatto"] = main.get("fatto", 0) + danno
        testo += f"🪝 {main['Nome']} riacciuffa {oppo['Nome']} dopo la schivata e infligge {danno} danni!\\n"

    # Uditore del profondo scatta ogni volta che si entra esattamente a 1 HP.
    trigger = []
    for proprietario, bersaglio in ((main, oppo), (oppo, main)):
        if proprietario.get("hp") != 1:
            proprietario["_uditore_a_uno"] = False
        if proprietario.get("set") == "Uditore del profondo" and proprietario.get("hp") == 1 and not proprietario.get("_uditore_a_uno"):
            proprietario["_uditore_a_uno"] = True
            trigger.append((proprietario, bersaglio))
    for proprietario, bersaglio in trigger:
        danno = proc_val("Uditore del profondo", "sfida", "richiamo", "danno")
        bersaglio["hp"] -= danno
        proprietario["fatto"] = proprietario.get("fatto", 0) + danno
        testo += f"🌊 Il profondo risponde a {proprietario['Nome']}: {danno} danni a {bersaglio['Nome']}!\\n"

    # Le resurrezioni temporali si risolvono prima che il loop esterno controlli is_dead().
    testo += _resurrezione_temporale(main)
    testo += _resurrezione_temporale(oppo)
    for combattente in (main, oppo):
        if combattente.get("set") == "Guerriero Temporale" and combattente.get("hp", 0) > 0:
            combattente["hp"] = min(combattente["hp"], proc_val("Guerriero Temporale", "sfida", "ciclo_temporale", "hp"))

    return prefisso + testo

def assedio(playerg, player, nemico, target, team, order, clan, meteo=None, setting=dict()):
    nome_set = player.get("set")
    prefisso = ""

    if nome_set == "Dannato primordiale" and not player.get("_dannato_conversione"):
        difesa = player.get("def", 0)
        player["atk"] += difesa
        player["def"] = 0
        player["_dannato_conversione"] = True
        prefisso += f"😈 {player['Nome']} converte {difesa} DEF in ATK prima dell'assalto!\\n"

    if nome_set == "Evocatore delle maree":
        incantesimo = proc_val(nome_set, "assalto", "onda", "incantesimo")
        incantamenti = player.setdefault("incantamenti", [])
        if incantesimo not in incantamenti:
            incantamenti.append(incantesimo)

    testo = _assedio_eroi_base(playerg, player, nemico, target, team, order, clan, meteo, setting)

    if nome_set == "Uditore del profondo" and player.get("hp") == proc_val(nome_set, "assalto", "richiamo", "hp_trigger"):
        bersaglio = target if target in nemico else next((x for x in order if x in nemico), None)
        if bersaglio is not None and isinstance(nemico.get(bersaglio), dict):
            danno = proc_val(nome_set, "assalto", "richiamo", "danno")
            nemico[bersaglio]["hp"] -= danno
            player["fatto"] = player.get("fatto", 0) + danno
            testo += f"🌊 Il profondo risponde: {danno} danni a {bersaglio}!\\n"
            if nemico[bersaglio].get("hp", 0) <= 0:
                nemico.pop(bersaglio, None)

    if nome_set == "Evocatore delle maree" and player.get("hp", 0) <= 0:
        pct = proc_val(nome_set, "assalto", "tsunami", "percento_atk")
        danno = round(player.get("atk", 0) * pct / 100)
        colpite = 0
        for struttura, dati in list(nemico.items()):
            if struttura == "inguerra" or not isinstance(dati, dict) or dati.get("hp", 0) <= 0:
                continue
            dati["hp"] -= danno
            colpite += 1
            if dati["hp"] <= 0:
                nemico.pop(struttura, None)
        if colpite:
            player["fatto"] = player.get("fatto", 0) + (danno * colpite)
            testo += f"🌊 Cadendo, {player['Nome']} genera uno tsunami: {danno} danni a ciascuna delle {colpite} strutture rimaste!\\n"

    return prefisso + testo


# --- SECONDA ONDATA SET: RUNTIME ---
_turno_seconda_ondata_base = turno
_assedio_seconda_ondata_base = assedio

def _tiro_schivata_seconda_ondata(possibile, difensore):
    successo = possibile > random.randint(0, 100)
    if successo and difensore.get("set") == "Anima persa":
        hp = proc_val("Anima persa", "sfida", "schivata_negata", "hp")
        difensore["hp"] += hp
        difensore["_anima_persa_hp"] = difensore.get("_anima_persa_hp", 0) + hp
        return False
    return successo

def _inizializza_seconda_ondata_sfida(p):
    if p.get("set") == "Esca vivente" and not p.get("_esca_vivente_inizializzata"):
        p["def"] = proc_val("Esca vivente", "sfida", "esca", "def")
        p["_esca_vivente_inizializzata"] = True
        return f"🪱 {p['Nome']} si offre come esca e rinuncia completamente alla difesa!\n"
    return ""

def turno(main, oppo, cond=None):
    if not _e_sfida_pvp(main, oppo, cond):
        return _turno_seconda_ondata_base(main, oppo, cond)
    prefisso = _inizializza_seconda_ondata_sfida(main) + _inizializza_seconda_ondata_sfida(oppo)
    if main.get("set") == "Giustiziere a V":
        main["_giustiziere_turni"] = main.get("_giustiziere_turni", 0) + 1
        if main["_giustiziere_turni"] >= proc_val("Giustiziere a V", "sfida", "giudizio", "turno_min") and not main.get("_giustiziere_agilita_attiva"):
            main["agi"] *= proc_val("Giustiziere a V", "sfida", "giudizio", "agi_mul")
            main["_giustiziere_agilita_attiva"] = True
            prefisso += f"⚖️ {main['Nome']} entra nella fase del giudizio: agilità raddoppiata!\n"
    if main.get("set") == "Pescatore alternativo" and proc_ok(random.random(), "Pescatore alternativo", "sfida", "azzardo"):
        main["atk"] *= proc_val("Pescatore alternativo", "sfida", "azzardo", "atk_mul")
        main["def"] *= proc_val("Pescatore alternativo", "sfida", "azzardo", "def_mul")
        prefisso += f"🎣 {main['Nome']} rischia tutto: attacco raddoppiato e difesa dimezzata!\n"
    hp_prima = {id(main): main.get("hp", 0), id(oppo): oppo.get("hp", 0)}
    fatto_prima = main.get("fatto", 0)
    anima_prima = oppo.get("_anima_persa_hp", 0)
    testo = _turno_seconda_ondata_base(main, oppo, cond)
    anima_dopo = oppo.get("_anima_persa_hp", 0)
    if anima_dopo > anima_prima:
        testo += f"👻 {oppo['Nome']} avrebbe schivato, ma l'Anima persa gli concede {anima_dopo-anima_prima} HP e il colpo continua!\n"
    for combattente in (main, oppo):
        if combattente.get("set") == "Controllore del cielo":
            guadagno = combattente.get("hp", 0) - hp_prima[id(combattente)]
            if guadagno > 0:
                atk_gain = guadagno / proc_val("Controllore del cielo", "sfida", "cura_in_potere", "atk_divisore")
                def_gain = guadagno / proc_val("Controllore del cielo", "sfida", "cura_in_potere", "def_divisore")
                combattente["atk"] += atk_gain
                combattente["def"] += def_gain
                testo += f"🪽 {combattente['Nome']} converte {guadagno:g} HP in +{atk_gain:g} ATK e +{def_gain:g} DEF!\n"
    if main.get("set") == "Eterna sventura" and main.get("fatto", 0) > fatto_prima and not oppo.get("schivato", False) and proc_ok(random.random(), "Eterna sventura", "sfida", "sventura"):
        for stat, key in (("atk", "atk_target"), ("def", "def_target"), ("agi", "agi_target")):
            oppo[stat] += proc_val("Eterna sventura", "sfida", "sventura", key)
        testo += f"☠️ La sventura di {main['Nome']} corrode {oppo['Nome']}: -10 ATK, -10 DEF e -10 AGI!\n"
    return prefisso + testo

def assedio(playerg, player, nemico, target, team, order, clan, meteo=None, setting=dict()):
    prefisso = ""
    nome_set = player.get("set")
    if nome_set == "Esca vivente":
        player["def"] = proc_val("Esca vivente", "assalto", "esca", "def")
        prefisso += "🪱 Ti presenti come esca vivente: difesa azzerata!\n"
    if nome_set == "Disabilitatore provetto" and target == "Muraglione extra":
        player["atk"] *= proc_val("Disabilitatore provetto", "assalto", "muraglione", "atk_mul")
        prefisso += "🔧 Smonti il Muraglione extra pezzo per pezzo: attacco ×4!\n"
    if nome_set == "Giustiziere a V" and target == "Accampamento":
        player["atk"] *= proc_val("Giustiziere a V", "assalto", "accampamento", "atk_mul")
        prefisso += "⚖️ L'Accampamento è sotto giudizio: attacco ×6!\n"
    return prefisso + _assedio_seconda_ondata_base(playerg, player, nemico, target, team, order, clan, meteo, setting)


# --- TERZA ONDATA SET: NOVE SET ---
_turno_terza_ondata_base = turno
_assedio_terza_ondata_base = assedio

def _danno_normale_terza(attaccante, difensore):
    dps = max(0, float(attaccante.get("atk", 0)))
    difesa = max(0, float(difensore.get("def", 0)))
    minimo = dps * (100 / ((100 + difesa * 1.5) + 1))
    massimo = dps * (100 / ((100 + difesa) + 1))
    return max(20, random.uniform(minimo, massimo))


def _mangia_vermi_terza(personaggio, contesto):
    if personaggio.get("set") != "Duellista vermico":
        return ""
    marker = f"_duellista_vermico_{contesto}"
    if personaggio.get(marker):
        return ""
    cfg = proc_cfg("Duellista vermico", contesto, "vermi")
    mangiati = 1 if cfg.get("primo_garantito", True) else 0
    while proc_ok(random.random(), "Duellista vermico", contesto, "vermi"):
        mangiati += 1
    if mangiati:
        personaggio["atk"] += cfg["atk"] * mangiati
        personaggio["def"] += cfg["def"] * mangiati
        personaggio["hp"] += cfg["hp"] * mangiati
    personaggio[marker] = True
    return f"🪱 {personaggio['Nome']} mangia {mangiati} verme/i: +{cfg['atk']*mangiati} ATK, +{cfg['def']*mangiati} DEF, +{cfg['hp']*mangiati} HP!\n"


def _inizializza_terza_combattimento(proprietario, avversario):
    testo = ""
    nome_set = proprietario.get("set")
    if nome_set == "Monarca oscuro" and not proprietario.get("_monarca_oscuro_inizializzato"):
        pct = proc_val(nome_set, "combattimento", "inizio", "hp_target_percento")
        prima = avversario.get("hp", 0)
        avversario["hp"] = round(prima * pct / 100)
        proprietario["_monarca_oscuro_inizializzato"] = True
        testo += f"🌑 {avversario['Nome']} entra nell'ombra del Monarca con solo il {pct}% degli HP!\n"
    if nome_set == "Re dei gadget" and not proprietario.get("_re_gadget_inizializzato"):
        bonus_int = proc_val(nome_set, "combattimento", "intelletto", "int")
        proprietario["int"] = proprietario.get("int", 0) + bonus_int
        proprietario["_re_gadget_inizializzato"] = True
        testo += f"🧰 {proprietario['Nome']} apre la collezione di gadget: +{bonus_int} INT!\n"
    if nome_set == "Il comico" and not proprietario.get("_comico_clap_combattimento"):
        proprietario["_comico_clap_combattimento"] = True
        testo += "👏 **CLAP!**\n"
    testo += _mangia_vermi_terza(proprietario, "combattimento")
    return testo


def _proc_comico_terza(proprietario, avversario):
    if proprietario.get("set") != "Il comico":
        return ""
    if not proc_ok(random.random(), "Il comico", "combattimento", "confusione"):
        return ""
    possibile = possibiles(avversario.get("agi", 0), avversario.get("agi", 0))
    if possibile > random.randint(0, 100):
        return ""
    danno = round(_danno_normale_terza(avversario, avversario))
    avversario["hp"] -= danno
    proprietario["fatto"] = proprietario.get("fatto", 0) + danno
    return f"🤡 {avversario['Nome']} è così confuso da colpirsi da solo! ({danno} danni)\n"


def _danno_su_bersaglio_terza(hp_prima, scudo_prima, bersaglio):
    danno_hp = max(0, hp_prima - bersaglio.get("hp", hp_prima))
    danno_scudo = 0
    if scudo_prima is not None:
        danno_scudo = max(0, scudo_prima - bersaglio.get("Scudo", scudo_prima))
    return danno_hp + danno_scudo


def _aggiungi_extra_terza(attaccante, bersaglio, danno_base, percento, etichetta):
    if danno_base <= 0:
        return ""
    extra = round(danno_base * percento / 100)
    if extra <= 0:
        return ""
    if "Scudo" in bersaglio and bersaglio.get("Scudo", -1) >= 0 and bersaglio.get("hp", 0) > 0:
        bersaglio["Scudo"] -= extra
    else:
        bersaglio["hp"] -= extra
    attaccante["fatto"] = attaccante.get("fatto", 0) + extra
    return f"{etichetta} +{extra} danni!\n"


def turno(main, oppo, cond=None):
    prefisso = _inizializza_terza_combattimento(main, oppo) + _inizializza_terza_combattimento(oppo, main)
    hp_turno_main = main.get("hp", 0)
    hp_turno_oppo = oppo.get("hp", 0)

    prefisso += _proc_comico_terza(main, oppo)
    prefisso += _proc_comico_terza(oppo, main)

    hp_prima = oppo.get("hp", 0)
    scudo_prima = oppo.get("Scudo") if "Scudo" in oppo else None
    testo = _turno_terza_ondata_base(main, oppo, cond)
    danno_base = _danno_su_bersaglio_terza(hp_prima, scudo_prima, oppo)

    if main.get("set") == "Demone delle lame" and danno_base > 0:
        pct = proc_val("Demone delle lame", "combattimento", "danno_extra", "percento")
        testo += _aggiungi_extra_terza(main, oppo, danno_base, pct, "🔪 Le lame trovano un secondo varco:")
    elif main.get("set") == "Cacciatore d'esce" and danno_base > 0 and proc_ok(random.random(), "Cacciatore d'esce", "combattimento", "secondo_colpo"):
        pct = proc_val("Cacciatore d'esce", "combattimento", "secondo_colpo", "percento_danno")
        testo += _aggiungi_extra_terza(main, oppo, danno_base, pct, "🎯 L'esca richiama un secondo colpo:")

    danno_subito_main = max(0, hp_turno_main - main.get("hp", 0))
    danno_subito_oppo = max(0, hp_turno_oppo - oppo.get("hp", 0))
    if main.get("set") == "Oscurato" and danno_subito_main > 0:
        pct = proc_val("Oscurato", "combattimento", "riflesso", "percento")
        riflesso = round(danno_subito_main * pct / 100)
        if riflesso > 0:
            oppo["hp"] -= riflesso
            main["fatto"] = main.get("fatto", 0) + riflesso
            testo += f"🌑 {main['Nome']} riflette {riflesso} danni a {oppo['Nome']}!\n"
    if oppo.get("set") == "Oscurato" and danno_subito_oppo > 0:
        pct = proc_val("Oscurato", "combattimento", "riflesso", "percento")
        riflesso = round(danno_subito_oppo * pct / 100)
        if riflesso > 0:
            main["hp"] -= riflesso
            oppo["fatto"] = oppo.get("fatto", 0) + riflesso
            testo += f"🌑 {oppo['Nome']} riflette {riflesso} danni a {main['Nome']}!\n"

    return prefisso + testo


def _last_recenti_terza(clan, team, nome, finestra):
    ora = time.time()
    recenti = 0
    try:
        last = clan[team].get("last", {})
    except Exception:
        return 0
    for giocatore, timestamp in last.items():
        try:
            if giocatore != nome and ora - float(timestamp) < finestra:
                recenti += 1
        except Exception:
            continue
    return recenti


def assedio(playerg, player, nemico, target, team, order, clan, meteo=None, setting=dict()):
    prefisso = ""
    nome_set = player.get("set")
    prefisso += _mangia_vermi_terza(player, "assalto")
    if nome_set == "Il comico":
        prefisso += "👏 **CLAP!**\n"

    danno_monarca = 0
    if nome_set == "Monarca oscuro" and target in nemico and isinstance(nemico.get(target), dict):
        cfg = proc_cfg(nome_set, "assalto", "last")
        quanti = _last_recenti_terza(clan, team, player.get("Nome"), cfg["finestra_secondi"])
        danno_monarca = cfg["danno_per_last"] * quanti
        if danno_monarca > 0:
            nemico[target]["hp"] -= danno_monarca
            prefisso += f"🌑 Le ombre di {quanti} assaltatori recenti colpiscono {target} per {danno_monarca} danni!\n"

    hp_target_prima = None
    if target in nemico and isinstance(nemico.get(target), dict):
        hp_target_prima = nemico[target].get("hp", 0)

    testo = _assedio_terza_ondata_base(playerg, player, nemico, target, team, order, clan, meteo, setting)
    if danno_monarca > 0:
        player["fatto"] = player.get("fatto", 0) + danno_monarca

    if hp_target_prima is not None and target in nemico and isinstance(nemico.get(target), dict):
        danno_base = max(0, hp_target_prima - nemico[target].get("hp", hp_target_prima))
        extra = 0
        etichetta = ""
        if nome_set == "Demone delle lame" and danno_base > 0:
            pct = proc_val(nome_set, "assalto", "danno_extra", "percento")
            extra = round(danno_base * pct / 100)
            etichetta = "🔪 Le lame approfondiscono il colpo"
        elif nome_set == "Cacciatore d'esce" and danno_base > 0 and proc_ok(random.random(), nome_set, "assalto", "secondo_colpo"):
            pct = proc_val(nome_set, "assalto", "secondo_colpo", "percento_danno")
            extra = round(danno_base * pct / 100)
            etichetta = "🎯 L'esca richiama un secondo colpo"
        if extra > 0:
            nemico[target]["hp"] -= extra
            player["fatto"] = player.get("fatto", 0) + extra
            testo += f"{etichetta}: +{extra} danni a {target}!\n"
            if nemico[target].get("hp", 0) <= 0:
                nemico.pop(target, None)
                testo += "**E' andata!!**\n"

    return prefisso + testo


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

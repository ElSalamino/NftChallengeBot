# coding=utf-8
import copy,html,json,random,sys,time,asyncio,gc, importlib
from io import BytesIO, StringIO
from apscheduler.schedulers.background import BackgroundScheduler
from pyrogram import Client, ContinuePropagation, filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types import ReplyKeyboardMarkup,ReplyKeyboardRemove
from pyrogram.errors import FloodWait
nft = importlib.import_module("nft")
liste = importlib.import_module("liste")


me = "ElSalamino"

last_sms = dict()
liste.bloccati += list(liste.decoro)

newpesci = list()
for x in liste.pesci:
    newpesci.append("Pesce " + x)
allneed = newpesci + liste.ingredienti

notifiche = ["exp", "compatte", "oggetti", "privacy","amichevoli"]
if 1 == 1:
    pozioni = dict()
    with open("./backup/pozioni.json") as json_file:
        pozioni = json.load(json_file)
    
    sicurezza = dict()
    with open("./backup/sicurezza.json") as json_file:
        sicurezza = json.load(json_file)

    clan = dict()
    with open("./backup/clan.json") as json_file:
        clan = json.load(json_file)

    trader = dict()
    with open("./backup/trader.json") as json_file:
        trader = json.load(json_file)

    player = dict()
    with open("./backup/player.json") as json_file:
        player = json.load(json_file)
    inabilitati = dict()
    with open("./backup/inabilitati.json") as json_file:
        inabilitati = json.load(json_file)
    

    evento = list()
    with open("./backup/evento.json") as json_file:
        evento = json.load(json_file)

strader = {"sfide":{}}
sched = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 12})


app = Client(
    "nft",
    api_id=,
    api_hash="",
    bot_token="",
    workers= 32
)

if 1 == 1:
    app.start()
    try:
        app.delete_messages(-1001549963117,int(trader["killer"]))
    except:
        pass
    app.stop()

cestino = Client(
    "cestino",
    api_id=,
    api_hash="",
    bot_token="",
    workers= 32
)


# eventi attuali


armieprot = list()
for armature in liste.protezioni:
    nome = f"{armature} LV0"
    armieprot.append(nome)
for armature in liste.armi:
    nome = f"{armature} LV0"
    armieprot.append(nome)

    

tempesta = ["Centro temporale LV0","Benda maledetta LV0","Armatura di carne LV0","Anima dispersa LV0","Origine della tempesta LV0","Corona maledetta LV0","Il ciondolo della creazione LV0","Zanna del aliena LV0"]
zombie = ["Un armatura in filo spinato LV0","Un pompa del nonno LV0","Due gemelle luccicanti LV0","Una katana ben affilata LV0","Un fucile a pallettoni LV0","Una bandana da tipo tosto LV0","Delle placche metalliche LV0","Un visore laser LV0","Un manganello LV0",]
megaman = ["Neo blaster LV0","Spada a protoni LV0","Z-Saber LV0","Chip terra LV0","Chip fuoco LV0","Chip elettro LV0","Chip lunare LV0",]
megaset = ['Neo blaster', 'Spada a protoni', 'Z-Saber', 'Chip terra', 'Chip fuoco', 'Chip elettro', 'Chip lunare']
gungeon = ["Mantello rosso LV0","Tasto X","Tasto B","Blasfemia LV0","Armatura di cormorant LV0","Guanti di cormorant LV0","Pistola del west LV0","Blaster a turbina LV0","Cacciavite multiuso LV0","Junior secondo LV0",]
magic = ["Lama Mentale LV0","Fuoco purificatore LV0","Spada del dio della fucina LV0","Velo di catena LV0","Bussola taumaturgica LV0",]
premi_pescatore = ["Canna rossa LV0","Canna blu LV0","Canna magenta LV0","Cappellino da pescatore LV0","Armatura di esche LV0","Secchiello di vermi LV0","Giubbina con lenze LV0"]
item_pescatore = ["Canna rossa","Canna blu","Canna magenta","Cappellino da pescatore","Armatura di esche","Secchiello di vermi","Giubbina con lenze"]


emojiz = {"Velo di catena": "💫","Spada del dio della fucina": "💫","Fuoco purificatore": "💫","Bussola taumaturgica": "💫","Lama Mentale": "💫","Un armatura in filo spinato": "🧟","Un pompa del nonno": "🧟","Due gemelle luccicanti": "🧟","Una katana ben affilata": "🧟","Un fucile a pallettoni": "🧟","Una bandana da tipo tosto": "🧟","Delle placche metalliche": "🧟","Un visore laser": "🧟","Un manganello": "🧟","Mantello rosso": "🔫","Tasto X": "🔫","Tasto B": "🔫","Blasfemia": "🔫","Armatura di cormorant": "🔫","Guanti di cormorant": "🔫","Pistola del west": "🔫","Blaster a turbina": "🔫","Cacciavite multiuso": "🔫","Junior secondo": "🔫","Neo blaster": "🤖","Spada a protoni": "🤖","Z-Saber": "🤖","Chip terra": "🤖","Chip fuoco": "🤖","Chip elettro": "🤖","Chip lunare": "🤖","Assetto mecha":"⛈","Centro temporale":"⛈","Benda maledetta":"⛈","Armatura di carne":"⛈","Anima dispersa":"⛈","Origine della tempesta":"⛈","Corona maledetta":"⛈","Il ciondolo della creazione":"⛈","Zanna del aliena":"⛈"}

item_boss = ['Ricordo straziante',"Un terzo occhio","Pessime idee","Marchio del dannato","Aura pessima", 'Una falce spaventosa', 'Un mantello nero cenere', 'Una bibbia inversa', 'Un piccolo uccellino scheletrico', 'Amuleto del protettore', 'Guanto titanico', 'Cinta del comandante', 'Un frammento del potere', 'Un generatore incartato', 'Una tempesta in barattolo', 'Catenaccio demoniaco', 'Dente infernale', "Chiavi dell'aldilà", 'Tentacolo viscido', 'Coda-mazza', 'Cuore delle sabbie', 'Spada di sangue di demone', 'Un copricapo rossastro', 'Coda demoniaca', 'Fiamma bluastra', 'Forcone fiammeggiante', 'Una spilla rossa', 'Vanga da cimitero', 'Sacco da cadaveri', "Anello dell'occulto", 'Corvo amichevole', 'Ali piumate', 'Artiglio del mostro', 'Unto e lercio', 'Fanghiglia della palude', 'Laniccio del pantano', 'Ninfea stagnia', 'Un teschio antico', 'Uncino rituale', 'Copricapo maori', 'Effige della tribe', 'Totem spirituale', 'Stecca tori']

protezioni = nft.merge_two_dicts(liste.protezioni, liste.protezioniextra)
armi = nft.merge_two_dicts(liste.armi,liste.armiextra)
possi = list(armi) + list(protezioni)

prot = dict()
for armature in protezioni:

    for x in range(12):
        if x == 10:
            x = "X"
        if x == 11:
            x = "MAX"
        nome = f"{armature} LV{x}"
        stati = dict()
        for stats in protezioni[armature]:
            if stats == "type":
                pass
            else:
                if x == "X":
                    x = 10
                if x == "MAX":
                    x = 15
                stati[stats] = round(
                    int(protezioni[armature][stats]) + (int(protezioni[armature][stats]) * x / 10)
                )
        try:
            stati["type"] = protezioni[armature]["type"]
        except:
            stati["type"] = "Arena"
        prot[nome] = stati

for armature in protezioni:
    
    for x in range(10):
        x = x * -1
        nome = f"{armature} LV{x}"
        stati = dict()
        for stats in protezioni[armature]:
            if stats == "type":
                pass
            else:
                if x == "X":
                    x = 10
                if x == "MAX":
                    x = 15
                stati[stats] = round(
                    int(protezioni[armature][stats]) + (int(protezioni[armature][stats]) * x / 10)
                )
        try:
            stati["type"] = protezioni[armature]["type"]
        except:
            stati["type"] = "Arena"
        prot[nome] = stati

protezioni = prot

protezioni["armatura sakuretsu LV0"] = {"hp": 0,"atk": 0,"def": 0,"agi": 0,"type": "🛡",}

prot = dict()
for armature in armi:
    for x in range(12):
        if x == 10:
            x = "X"
        if x == 11:
            x = "MAX"
        nome = f"{armature} LV{x}"
        stati = dict()
        for stats in armi[armature]:
            if stats == "type":
                pass
            else:
                if x == "X":
                    x = 10
                if x == "MAX":
                    x = 15
                stati[stats] = round(
                    int(armi[armature][stats]) + (int(armi[armature][stats]) * x / 10)
                )
        try:
            stati["type"] = armi[armature]["type"]
        except:
            stati["type"] = "Arena"
        
        prot[nome] = stati
        
for armature in armi:
    for x in range(10):
        x = x * -1
        nome = f"{armature} LV{x}"
        stati = dict()
        for stats in armi[armature]:
            if stats == "type":
                pass
            else:
                if x == "X":
                    x = 10
                stati[stats] = round(
                    int(armi[armature][stats]) + (int(armi[armature][stats]) * x / 10)
                )
        try:
            stati["type"] = armi[armature]["type"]
        except:
            stati["type"] = "Arena"
        prot[nome] = stati

armi = prot


globali = {"Cancello": False, "Mucche": True}


tutto = list(liste.anellic) + liste.usabilitutti + armieprot + liste.usabilitutti + armieprot
tuttov = list(liste.anellic) + liste.usabilitutti + armieprot
tuttot = list(liste.anellic) + list(liste.anellic) + armieprot
text = ""

for z in player:
    player[z]["preso"] = False

async def auto_check(username):
    if username in inabilitati:
        if inabilitati[username] == "Una copia dell'arte della guerra autografata":
            pass
        else:
            minimo = 900
            if evento["mod"] == "flexville":
                minimo - 450
            if player[username]["team"] != "nessuno":
                if "Chiesa" in clan[player[username]["team"]]["villaggio"]:
                    minimo -= 5 * int(clan[player[username]["team"]]["villaggio"]["Chiesa"]["lv"])
            if player[username]["setta"]["benedizione"] == 'Non morto':
                a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
                minimo -= a
            
            oldtime = inabilitati[username]
            direi = time.time() - oldtime
            
            if direi > minimo:
                inabilitati.pop(username)
                try:
                    await app.send_message(username, "Ok ti dovresti essere ripreso")
                except:
                    pass



nop = []

def premio_exp(a, b, text):
    possibilia = 0.2
    possibilib = 0.1
    #
    
    if "set" in a["scheda"]:
        if a["scheda"]["set"] == "Pilota":
            possibilia += 0.1
    if "set" in a["scheda"]:
        if a["scheda"]["set"] == "Sopravvissuto":
            possibilia += 0.25
    if "set" in b["scheda"]:
        if b["scheda"]["set"] == "Sopravvissuto":
            possibilia += 0.25

    if "set" in b["scheda"]:
        if b["scheda"]["set"] == "Pilota":
            possibilib += 0.1
    if "l-streak" in b:
        possibilib += b["l-streak"] / 20
    
    if "Fortunello" in a["scheda"]["boost"]["sfida"]:
        possibilia += 0.05 * a["scheda"]["boost"]["sfida"]["Fortunello"]["lv"]
        
    if "Fortunello" in b["scheda"]["boost"]["sfida"]:
        possibilib += 0.05 * a["scheda"]["boost"]["sfida"]["Fortunello"]["lv"]
    
    if player[a["scheda"]["Nome"]]["setta"]["benedizione"] == "Guardia reale":
        ga = round(trader["sette"][player[a["scheda"]["Nome"]]["setta"]["loc"]]["power"] * (trader["sette"][player[a["scheda"]["Nome"]]["setta"]["loc"]]["%"]/100))
        possibilia += (ga/100)
    
    if player[b["scheda"]["Nome"]]["setta"]["benedizione"] == "Guardia reale":
        gb = round(trader["sette"][player[b["scheda"]["Nome"]]["setta"]["loc"]]["power"] * (trader["sette"][player[b["scheda"]["Nome"]]["setta"]["loc"]]["%"]/100))
        possibilib += (gb/100)
    
    if a["scheda"]["Nome"] in nop:
        possibilia = -10000
    if b["scheda"]["Nome"] in nop:
        possibilib = -10000
    
    if possibilia > random.random() and a["location"] != "Hub":
        item_trovabili = liste.pool[a["location"]]
        vertutto = item_trovabili
        if evento["evento"] == "mega":
            vertutto = item_trovabili + megaman 
        if evento["evento"] == "zombie":
            vertutto = item_trovabili + zombie 
        if evento["evento"] == "gungeon":
            vertutto = item_trovabili + gungeon 
        if evento["evento"] == "magic":
            vertutto = item_trovabili + magic 

        contentino = random.choice(vertutto)
        if (
            a["scheda"]["anello"] == "Un generatore incartato"
            and 0.06 > random.random()
        ):
            contentino = "Un oggetto incartato"
        try:
            a["zaino"][contentino] += 1
        except:
            a["zaino"][contentino] = 1
        
        if a["notifiche"]["oggetti"] == "no":
            pass
        else:
            try:
                app.send_message(
                    a["scheda"]["Nome"],
                    f"Hai vinto {contentino} grazie alla tua bravura in questa sfida!",
                )
            except:
                pass

    if 0.4 > random.random():
        nm = 1
        if player[b["scheda"]["Nome"]]["setta"]["benedizione"] == 'Corvo':
            gb = round(trader["sette"][player[b["scheda"]["Nome"]]["setta"]["loc"]]["power"] * (trader["sette"][player[b["scheda"]["Nome"]]["setta"]["loc"]]["%"]/100))
            if gb >= random.randint(0,100):
                nm += 1
        
        b["exp"]["expattuale"] += nm
        if b["notifiche"]["exp"] == "no":
            pass
        else:
            try:
                app.send_message(b["scheda"]["Nome"], f"Inoltre guadagni {nm} exp!")
            except:
                pass

        if b["exp"]["expattuale"] > b["exp"]["nextlv"]:
            b["livello"] += 1

            b["exp"]["expattuale"] = 1
            b["exp"]["nextlv"] += 10
            b["gloria"] += b["livello"] * 10
            
            numerino = round(b["livello"] / 10)
            if numerino > 0:

                try:
                    b["zaino"]["Un oggetto incartato"] += round(b["livello"] / 10)
                except:
                    b["zaino"]["Un oggetto incartato"] = round(b["livello"] / 10)
            try:
                b["zaino"]["Una licenza per animali domestici"] += 1
            except:
                b["zaino"]["Una licenza per animali domestici"] = 1

            if b["livello"] == 2:
                try:
                    app.send_message(
                        b["scheda"]["Nome"], f"Ecco a te una licenza per animali!"
                    )
                except:
                    pass

            gg = b["livello"] * 10
            try:
                app.send_message(
                    b["scheda"]["Nome"],
                    f"Sei salito di livello!\nOttieni {gg} gloria e {numerino} oggetti incartati!",
                )
            except:
                pass
            
            

    if possibilib > random.random() and b["location"] != "Hub":
        item_trovabili = liste.pool[b["location"]]
        vertutto = item_trovabili
        if evento["evento"] == "mega":
            vertutto = item_trovabili + megaman + megaman
        if evento["evento"] == "zombie":
            vertutto = item_trovabili + zombie + zombie
        if evento["evento"] == "gungeon":
            vertutto = item_trovabili + gungeon + gungeon
        if evento["evento"] == "magic":
            vertutto = item_trovabili + magic + magic + magic

        contentino = random.choice(vertutto)
        if (
            b["scheda"]["anello"] == "Un generatore incartato"
            and 0.06 > random.random()
        ):
            contentino = "Un oggetto incartato"

        if "l-streak" in b:
            b["l-streak"] = 0

        try:
            b["zaino"][contentino] += 1
        except:
            b["zaino"][contentino] = 1
        if b["notifiche"]["oggetti"] == "no":
            pass
        else:

            try:
                app.send_message(
                    b["scheda"]["Nome"], f"Di consolazione ottieni {contentino}!"
                )
            except:
                pass

    if 0.8 > random.random():
        nm = 2
        if player[a["scheda"]["Nome"]]["setta"]["benedizione"] == 'Corvo':
            ga = round(trader["sette"][player[a["scheda"]["Nome"]]["setta"]["loc"]]["power"] * (trader["sette"][player[a["scheda"]["Nome"]]["setta"]["loc"]]["%"]/100))
            if ga >= random.randint(0,100):
                nm += 1
    
        a["exp"]["expattuale"] += nm

        if a["notifiche"]["exp"] == "no":
            pass
        else:
            try:
                app.send_message(a["scheda"]["Nome"], f"Inoltre guadagni {nm} exp!")
            except:
                pass

        if a["exp"]["expattuale"] > a["exp"]["nextlv"]:
            a["livello"] += 1

            a["exp"]["expattuale"] = 1
            a["exp"]["nextlv"] += 10

            try:
                a["gloria"] += a["livello"] * 10
            except:
                a["gloria"] = a["livello"] * 10
            
            numerino = round(a["livello"] / 10)
            if numerino > 0:

                try:
                    a["zaino"]["Un oggetto incartato"] += round(a["livello"] / 10)
                except:
                    a["zaino"]["Un oggetto incartato"] = round(a["livello"] / 10)

            gg = a["livello"] * 10
            try:
                a["zaino"]["Una licenza per animali domestici"] += 1
            except:
                a["zaino"]["Una licenza per animali domestici"] = 1

            if a["livello"] == 2:
                try:
                    app.send_message(
                        a["scheda"]["Nome"], f"Ecco a te una licenza per animali!"
                    )
                except:
                    pass
            try:
                app.send_message(
                    a["scheda"]["Nome"],
                    f"Sei salito di livello!\nOttieni {gg} gloria e {numerino} oggetti incartati!",
                )
            except:
                pass
            
            
import asyncio


non_qui = [-438830562, -1001476172565]

bannatim = {'Verity_Ice_Ocean':"Multi di Sun_landae", 'Sun_Landar':"Utilizzo di multi","Giecklosquartatoree":"Automatismo, 35 secondi puliti intersfida!","TheRealDioBrando":"Preciso al millisecodno, 35 secondi a sfida per ben 12 ore consecutive.\n2 volte!"}
bannati = ['Verity_Ice_Ocean', 'Sun_Landar',"Giecklosquartatoree"]

@app.on_message(filters.command(["start"]) & filters.private & ~filters.user(bannati))
async def start(client, message):
    username = message.from_user.username
    id = message.from_user.id

    if username == None:
        await app.send_message(message.chat.id,"Necessiti di un username per giocare!")

    elif username in list(player):
        await app.send_photo(message.chat.id, "AgACAgQAAxkBAAEWlM1hXIl8xLH3Ikyw8Ej5mBQU0eWangACPbcxG_Ef6VIEjy5Z1I_m7pRVBTVdAAMBAAMCAANtAANdMwACHgQ", caption="Sei già iscritto!\nNon sai cosa fare?\nhttps://telegra.ph/Una-piccola-guida-per-NFT-10-14 \nSe non lo hai già fatto fai /ruota!")
        
        if len(message.command) > 1:
            codice = message.command[1]
            print(codice)
            if codice in trader["qr"]:
                if username in trader["qr"][codice]:
                    await message.reply("Già ricevuto!")
                else:
                    if codice == "FreeRolex":
                        await message.reply("Ecco a te il tuo unico rolex!")
                        try:
                            player[username]["zaino"]["Un rolex oro LV1"] += 1
                        except:
                            player[username]["zaino"]["Un rolex oro LV1"] = 1
    
                    trader["qr"][codice].append(username)
                    
    else:
        sus = False
        for g in player:
            if id == player[g]["id"]:
                await app.send_message(message.chat.id,"Tu non mi sei nuovo, rimetti il tuo username!"
                              )
                sus = True
                break
        if sus == False:
            player[username] = {
                "livello": 1,
                "exp": {"expattuale": 0, "nextlv": 15},
                "punti": 1000,
                "team": "nessuno",
                "bestiario": dict(),
                "zaino": dict(),
                "w": 0,
                "l": 0,
                "topP": 0,
                "totali": 0,
                "da": "Lapsus vitale",
                "vuole": "Vasetto all'orlo",
                "oggi": 0,
                'richiesta_pescatore':None,
                "cap":0,
                "conosciuto": "no",
                "incantamenti":{},
                "preso": False,
                "gloria":0,
                "pozioni": dict(),
                "varie": {"pat":0,"pesca":0,"trade":0,"cambi":0,"pescatore":0},
                "obbiettivi": list(),
                "setvisti": list(),
                "prima": False,
                "streak": 0,
                "location":"Labirintico inizio",
                "last":0,
                "ruota":True,
                "aigettoni":{"pesca":0,"sfide":0,"assalti":0,"commerci":0},
                "guerrieggiato":0,
                "l-streak": 0,
                "notifiche": {
                    "exp": "si",
                    "oggetti": "si",
                    "compatte": "no",
                    "privacy": "no",
                    "amichevoli":"si"
                },
                "id":message.from_user.id,
                "setta":{"benedizione":None,"libero":True},
                "classe": "Nullatenente",
                "inviti": {"numero": 0, "link": nft.id_generator(), "dachi": None},
                "arenagratis":True,
                "Approcci":dict(),
                "scheda": {
                    "Nome": username,
                    "hp": 1000,
                    "def": 100,
                    "atk": 100,
                    "agi": 20,
                    "int":0,
                    "Ap": "Base",
                    "schivato": False,
                    "anello": None,
                    "protezione": None,
                    "arma": None,
                    "boost": {"sfida": dict(), "assalto": dict()},
                    "set": None,
                },
            }

            
            await app.send_message(message.chat.id,
                "Iscritto con successo!\nEcco una rapida ed indolore guida!\nhttps://telegra.ph/Una-piccola-guida-per-NFT-10-14\nGruppo ufficioso: https://t.me/joinchat/RREYf8lUUsM4NDA0\nO parti fortissimo facendo /sfida!\nAttenzione: Ti consiglio di silenziare il bot dato che è moooooolto rumoroso!\n\nUsa pure /ruota per cose gratis"
            )

            trader["battaglieri"].append(username)
            if len(message.command) > 1:
                codice = message.command[1]
                for a in player:
                    if player[a]["inviti"]["link"] == codice:
                        player[a]["inviti"]["numero"] += 1
                        app.send_message(message.chat.id,f"Registrat* col link di {a}")
                        player[username]["inviti"]["dachi"] = a
                        try:
                            player[username]["zaino"]["Un oggetto incartato"] += 1

                        except:
                            player[username]["zaino"]["Un oggetto incartato"] = 1

                        await app.send_message(
                            a, f"{username} si è registrato col tuo link d'invito!"
                        )
    

@app.on_message()
async def logger(client, message):
    if trader["primo"] == None and message.chat.id == -1001549963117:

        if "primo" in message.text.lower():

            if 0.7 > random.random():
                username = message.from_user.username
                trader["primo"] = username
                await app.send_message(message.chat.id,"Sei il re primo di oggi!\n+1 gloria!")
                player[username]["gloria"] += 1
                
                if "Primo" not in player[username]["obbiettivi"]:
                    player[username]["obbiettivi"].append("Primo")
                    try:
                        await app.send_message(
                            username, "Obbiettivo completato!\n**Primo**, Primo!"
                        )
                    except:
                        pass

    if message.from_user.username != None and message.text != None:
        if message.text:
            username = message.from_user.username
            other_time = last_sms.get(username,1)
            
            now = time.time()
            
            elapsed = now - other_time
            g = time.ctime(now)
            if elapsed > 0.15:
                    if "/" in message.text:
                        dist = int(elapsed)
                        print(f"{username} - {message.text} [{g}]({dist})")
                    last_sms[username] = now
                    
                    
                        
                    await auto_check(username)
                    
                    
                    if ("/sfida" in message.text or "Sfida ⚔️" in message.text) and elapsed < 640 and username not in bannati:
                        try:
                            dist = int(time.time() - sicurezza[username]["ultima"])
                        except:
                            pass
                        if dist <= 640:
                            try:
                                sicurezza[username]["tempi"].append(dist)
                                sicurezza[username]["ultima"] = time.time()
                                
                            except:
                                print(f"Nuovo {username}")
                                sicurezza[username] = {"tempi":[dist],"ultima":time.time()}
                        else:
                            try:
                                
                                sicurezza[username]["ultima"] = time.time()
                                
                            except:
                                print(f"Nuovo {username}")
                                sicurezza[username] = {"tempi":[],"ultima":time.time()}
                    
                    if message.text in ['Pesca 🎣', 'Domande ❔', 'Top 🔝', 'Obbiettivi 🎖', 'Notifiche 🛎', 'Invita 📮', 'Switch 🪖', 'menu', 'Sfida ⚔️', 'Arena ☠️', 'Dungeon 🏃‍♂️', 'Assalto 📯', 'Clan 🔱', 'Boss 👹', 'Muoviti 🚩', 'Setta ©️', 'Trafficante \U0001f977', 'Negozio 🛒', 'Pescatore 🎣', 'Me 👤', 'Altro 🧩', 'Info 🗞', 'Chiudi🚫']:
                        dist = int(elapsed)
                        print(f"{username} - {message.text} [{g}]({dist})")
                    
                    
                    raise ContinuePropagation
autorizzati = ["ElSalamino", "Isideasy"]
mediotourizzati = ["ElSalamino", "Isideasy","CosoSenpai" ,"Adularia" ,"Zipizz" ,"LeRoiJaune" ]


@app.on_message(filters.command("savexit") & filters.private & filters.user(mediotourizzati))
def savexit(client, message):
    u = app.send_sticker(-1001549963117,"CAACAgIAAxkBAAEVHzZhVdq8hUuLtmE_jxTUf2HEd93TaAACQgEAAs0bMAgEAoCtK287vh4E")
    trader["killer"] = u.message_id
    with open("./backup/pozioni.json", "w") as outfile:
        json.dump(pozioni, outfile)
    with open("./backup/player.json", "w") as outfile:
        json.dump(player, outfile)
    with open("./backup/sicurezza.json", "w") as outfile:
        json.dump(sicurezza, outfile)
    with open("./backup/sicurezza2.json", "w") as outfile:
        json.dump(sicurezza, outfile)
    
    with open("./backup/inabilitati.json", "w") as outfile:
        json.dump(inabilitati, outfile)
    with open("./backup/clan.json", "w") as outfile:
        json.dump(clan, outfile)
    with open("./backup/pozioni2.json", "w") as outfile:
        json.dump(pozioni, outfile)
    with open("./backup/player2.json", "w") as outfile:
        json.dump(player, outfile)
    
    with open("./backup/inabilitati2.json", "w") as outfile:
        json.dump(inabilitati, outfile)
    with open("./backup/clan2.json", "w") as outfile:
        json.dump(clan, outfile)
    with open("./backup/evento.json", "w") as outfile:
        json.dump(evento, outfile)
    with open("./backup/evento2.json", "w") as outfile:
        json.dump(evento, outfile)
    with open("./backup/trader.json", "w") as outfile:
        json.dump(trader, outfile)
    with open("./backup/trader2.json", "w") as outfile:
        json.dump(trader, outfile)
    
    exit()

@app.on_message(filters.command("save") & filters.private & filters.user(mediotourizzati))
def save(client, message):
    with open("./backup/pozioni.json", "w") as outfile:
        json.dump(pozioni, outfile)
    with open("./backup/player.json", "w") as outfile:
        json.dump(player, outfile)
    with open("./backup/sicurezza.json", "w") as outfile:
        json.dump(sicurezza, outfile)
    with open("./backup/sicurezza2.json", "w") as outfile:
        json.dump(sicurezza, outfile)
    
    with open("./backup/inabilitati.json", "w") as outfile:
        json.dump(inabilitati, outfile)
    with open("./backup/clan.json", "w") as outfile:
        json.dump(clan, outfile)
    with open("./backup/pozioni2.json", "w") as outfile:
        json.dump(pozioni, outfile)
    with open("./backup/player2.json", "w") as outfile:
        json.dump(player, outfile)
    
    with open("./backup/inabilitati2.json", "w") as outfile:
        json.dump(inabilitati, outfile)
    with open("./backup/clan2.json", "w") as outfile:
        json.dump(clan, outfile)
    with open("./backup/evento.json", "w") as outfile:
        json.dump(evento, outfile)
    with open("./backup/evento2.json", "w") as outfile:
        json.dump(evento, outfile)
    with open("./backup/trader.json", "w") as outfile:
        json.dump(trader, outfile)
    with open("./backup/trader2.json", "w") as outfile:
        json.dump(trader, outfile)
    app.send_message(message.chat.id,"Fatto!")

@app.on_message(filters.command("exit") & filters.user(autorizzati))
def executer(app, message):
    
    exit()
    

@app.on_message(~filters.user(bannati) &  filters.private & (filters.command(["menu"])|filters.regex(r"^menu"))) 
async def tastiera(clinet,message):
    cagata = random.choice(
        [
            "I dungeon non sono così impossibili",
            "Se non sai cosa fare puoi tentare /pesca, è un orribile passatempo!",
            "Sei in dubbio su cosa fare? Cerca supporto nei gruppi ufficiali!",
            "Ogni martedì e giocedì ci saranno le guerre tra clan!",
            "I boss cambiano ogni giorno, attento a non farteli fuggire!",
            "Ogni tanto il /trafficante cambia offerte!",
            "Ci vogliono circa 50 minuti tra un offerta del /trafficante ed un altra, mezz'ora più o mezz'ora meno!",
            "Attento a non cliccare troppo forte tutte le cose!",
            "Una volta scelto l'approccio quello resterà per sempre, o fino al prossimo cambio!",
            "Api!",
            "Ogni giorno il primo che dice primo nel parchetto ha un buon 70% di vincere 1 gloria!",
            "Perdi tante sfide? Cambia set!",
            "Ogni gadget è unico!",
            "Valuta ttentamente i tuoi scambi!",
            "Serve un clan? Si, a tutti serve un clan!",
            "Ogni tanto ricorda di fare /negozio, coccolati un poco",
            "Il latte in sacchetto è il top del latte!",
            "Ricorda di avere un animaletto, lui farebbe tutto per te!",
            "/wikiboss è una buona fonte di idee per i boss, ma non basta",
            "Set speciali fanno danno a strutture apposite!",
            "/forgiabili è troppo vago? Mettici dopo un numero!",
            "Non faresti mai /rimuovi hp",
            "Setta una setta per avere bonus onesti",
            "Attento a non perderti",
            "Nutri le mucche e mungi le mucche, non essere troppo avaro",
            "Dona su /dona, aiuterà me a comprarmi del cibo",
            "Si, acquila",
            "/rimuovi accetta argomenti, 1,2,arma e protezione",
        ]
    )
    text = f"Benvenuto {message.from_user.username}\n🕐 {time.ctime(time.time())}\n"
    ora = time.time()
    if ora - last_boss.get(message.from_user.username,0) >= 35:
        text += "👹 Boss disponibili!\n"
    
    if ora - last_dungeon.get(message.from_user.username,0) >= 35:
        text += "🏃‍♂️ Puoi esplorare il dungeon!\n"
    
    try:
        if clan[player[message.from_user.username]["team"]]["inguerra"] != None:
            text += f'🔥 In guerra con {clan[player[message.from_user.username]["team"]]["inguerra"]}\n'
        else:
            text += "🔱 Siete in pace al momento!\n" 
    except:
        text += "🔱 Non hai nessun team!"
    if evento["evento"] != None:
        text += f"🎉{evento['evento']}!\n"
    
    if message.from_user.username in inabilitati:
        text += "⚰️ Al momento sei memento morto...\n"
    
    if ora - player[message.from_user.username]["last"] >= 3600:
        text += "🚩 Ci si può spostare\n"
    
    mete = trader["meteo"][player[message.from_user.username]["location"]]
    text += f"Al momento il meteo è {mete}\n"
    text += f"\n__{cagata}__"
    await app.send_message(
        message.from_user.username,  # Edit this
        text,
        reply_markup=ReplyKeyboardMarkup(
            [["Sfida ⚔️"],["Arena ☠️","Dungeon 🏃‍♂️","Assalto 📯"],["Clan 🔱","Boss 👹"],["Muoviti 🚩","Setta ©️"],["Trafficante 🥷","Negozio 🛒","Pescatore 🎣"],["Me 👤","Altro 🧩","Info 🗞"],["Chiudi🚫"]],
            resize_keyboard=True  # Make the keyboard smaller
        )
        
    )  

@app.on_message(~filters.user(bannati) & filters.regex(r"^Altro 🧩") & filters.private & ~filters.edited)
async def tastiera(clinet,message):
    cagata = random.choice(
        [
            "I dungeon non sono così impossibili",
            "Se non sai cosa fare puoi tentare /pesca, è un orribile passatempo!",
            "Sei in dubbio su cosa fare? Cerca supporto nei gruppi ufficiali!",
            "Ogni martedì e giocedì ci saranno le guerre tra clan!",
            "I boss cambiano ogni giorno, attento a non farteli fuggire!",
            "Ogni tanto il /trafficante cambia offerte!",
            "Ci vogliono circa 50 minuti tra un offerta del /trafficante ed un altra, mezz'ora più o mezz'ora meno!",
            "Attento a non cliccare troppo forte tutte le cose!",
            "Una volta scelto l'approccio quello resterà per sempre, o fino al prossimo cambio!",
            "Api!",
            "Ogni giorno il primo che dice primo nel parchetto ha un buon 70% di vincere 1 gloria!",
            "Perdi tante sfide? Cambia set!",
            "Ogni anello è unico!",
            "Valuta ttentamente i tuoi scambi!",
            "Serve un clan? Si, a tutti serve un clan!",
            "Ogni tanto ricorda di fare /negozio, coccolati un poco",
            "Il latte in sacchetto è il top del latte!",
            "Ricorda di avere un animaletto, lui farebbe tutto per te!",
            "/wikiboss è una buona fonte di idee per i boss, ma non basta",
            "Set speciali fanno danno a strutture apposite!",
            "/forgiabili è troppo vago? Mettici dopo un numero!",
            "Non faresti mai /rimuovi hp",
            "Setta una setta per avere bonus onesti",
            "Attento a non perderti",
            "Nutri le mucche e mungi le mucche, non essere troppo avaro",
            "Dona su /dona, aiuterà me a comprarmi del cibo",
            "Si, acquila",
            "/rimuovi accetta argomenti, 1,2,arma e protezione",
        ]
    )
    text = f"Benvenuto {message.from_user.username}\n🕐 {time.ctime(time.time())}\n"
    ora = time.time()
    if ora - last_boss.get(message.from_user.username,0) >= 35:
        text += "👹 Boss disponibili!\n"
    
    if ora - last_dungeon.get(message.from_user.username,0) >= 35:
        text += "🏃‍♂️ Puoi esplorare il dungeon!\n"
    
    try:
        if clan[player[message.from_user.username]["team"]]["inguerra"] != None:
            text += f'🔥 In guerra con {clan[player[message.from_user.username]["team"]]["inguerra"]}\n'
        else:
            text += "🔱 Siete in pace al momento!\n" 
    except:
        text += "🔱 Non hai nessun team!"
    if evento["evento"] != None:
        text += f"🎉{evento['evento']}!\n"
    
    if message.from_user.username in inabilitati:
        text += "⚰️ Al momento sei memento morto...\n"
    
    if ora - player[message.from_user.username]["last"] >= 3600:
        text += "🚩 Ci si può spostare\n"
    
    mete = trader["meteo"][player[message.from_user.username]["location"]]
    text += f"Al momento il meteo è {mete}\n"
    text += f"\n__{cagata}__"
    await app.send_message(
        message.from_user.username,  # Edit this
        text,
        reply_markup=ReplyKeyboardMarkup(
            [["Pesca 🎣"],["Domande ❔"],["Top 🔝","Obbiettivi 🎖","Notifiche 🛎"],["Invita 📮","Switch 🪖"],["menu"]],
            resize_keyboard=True  # Make the keyboard smaller
        )
        
    )  
@app.on_message(~filters.user(bannati) & filters.regex(r"^Chiudi🚫") & filters.private & ~filters.edited)
async def tastiera(clinet,message):
    await message.reply_text(
    "Tastiera chiusa",  
    reply_markup=ReplyKeyboardRemove()
)
@app.on_message(filters.user(bannati))
async def welcome(client, message):
    
    mmm = bannatim[message.from_user.username]
    await message.reply(f"Sei stato bannato, riprova più tardi!\nMessaggio allegato al ban:\n {mmm}")
    
       



@app.on_message(filters.command("metaupdate") & filters.user(mediotourizzati))
async def meta(client, message):
    distinti = dict()
    for tipo in player:
        if "set" in player[tipo]["scheda"]:
            if player[tipo]["scheda"]["set"] in distinti:
                distinti[player[tipo]["scheda"]["set"]] +=1
            else:
                distinti[player[tipo]["scheda"]["set"]] =1
    g = "Meta update (SET):\n"
    for c in distinti:
        g += f"{c} - {distinti[c]}\n"
    await message.reply(g)


@app.on_message(filters.command("sicurezza") & filters.user(mediotourizzati))
async def meta(client, message):
    distinti = dict()
    usern = message.command[1]
    print(usern)
    usern = nft.search(list(sicurezza),usern)[0]
    print(usern)
    if usern != None:
        g = f"Analisi sicurezza per {usern}...\n\n"
        minima = min(sicurezza[usern]["tempi"])
        maxima = max(sicurezza[usern]["tempi"])
        media = 0
        possi = dict()
        for x in sicurezza[usern]["tempi"]:
            media += int(x)
            try:
                possi[x] += 1
            except:
                possi[x] = 1
            
        media = round(media/ len(sicurezza[usern]["tempi"]))
        try:
            my_keys = sorted(possi, key=possi.get, reverse=True)[:3]
            best = ""
            for y in my_keys:
                best += f"{y} secondi - {possi[y]} volte\n"
        except:
            best = "No best time"
        g+= f"""
Tempo minimo; {minima}
Tempo massimo; {maxima}

Media di {media} secondi

{best}
"""
        await message.reply(g)
    

@app.on_message(filters.command("globale") & filters.private & filters.user(autorizzati))
async def globale(client, message):
    testo = message.text.replace("/globale", "")
    for a in list(player):
        try:
            h = await app.send_message(a, testo)
            await h.pin(both_sides=True)
            await asyncio.sleep(0.2)
        except:
            await asyncio.sleep(0.1)
    await message.reply("Fatto")
        


lotteria = {"Attiva": False, "Iscritti": list(), "Altro": {}, "Iscrizioni": False}


@app.on_message(filters.command("rotteria") & filters.user(autorizzati) & ~filters.user(bannati))
async def jlotteria(client, message):
    global lotteria
    if lotteria["Attiva"] == False:
        lotteria["Iscrizioni"] = True
        lotteria["Attiva"] = True
        username = message.from_user.username
        
        await app.send_message(message.chat.id,"ROOOOOOOOOOTTERIA!\nIscriviti con /iscrivi per orrbili premi!")
    else:
        scritti = lotteria["Iscritti"]
        await app.send_message(message.chat.id,f"La rotteria è aperta con ben {len(scritti)} mele iscritte!")


@app.on_message(filters.command("estrazione") & filters.user(autorizzati) & ~filters.user(bannati))
async def estrazione(client, message):
    global lotteria
    username = message.from_user.username
    lotteria["Iscrizioni"] = False
    vincitore = random.choice(lotteria["Iscritti"])
    cosa = random.choice(tutto)

    if len(message.command) == 1:
        pass
    else:
        cosa = cosa.replace("0", message.command[1])

    if cosa in player[vincitore]["zaino"]:
        player[vincitore]["zaino"][cosa] += 1
    else:
        player[vincitore]["zaino"][cosa] = 1

    lotteria["Iscritti"].remove(vincitore)

    await app.send_message(
        -1001549963117,
        f"Dal magico coso delle rotterie viene estratto @{vincitore}!\nChe solo per oggi si porta a casa {cosa}!",
    )

        
    
@app.on_message(filters.command("finale") & filters.user(autorizzati) & ~filters.user(bannati))
async def fine(client, message):
    global lotteria
    username = message.from_user.username
    lotteria["Iscrizioni"] = False
    vincitore = random.choice(lotteria["Iscritti"])
    cosa = random.choice(tutto)

    if len(message.command) == 1:
        pass
    else:
        cosa = cosa.replace("0", message.command[1])

    if cosa in player[vincitore]["zaino"]:
        player[vincitore]["zaino"][cosa] += 1
    else:
        player[vincitore]["zaino"][cosa] = 1

    lotteria["Iscritti"].remove(vincitore)
    lotteria["Attiva"] = False
    lotteria["Iscritti"] = list()

    await app.send_message(
        -1001549963117,
        f"E come tutte le cose belle anche questa rotteria deve finire...\nMa non prima che @{vincitore} vinca!\nChe solo per oggi si porta a casa {cosa}!\n",
    )


@app.on_message(filters.command(["ricognizione"]) & ~filters.user(bannati))
async def fine(client, message):
    
    username = message.from_user.username
    print(list(player[message.from_user.username].get("spedizione",[False])))
    if list(player[message.from_user.username].get("spedizione",[False])) == [True] or list(player[message.from_user.username].get("spedizione",[False])) == ["true"]:
        try:
            delay = round((time.time() - player[message.from_user.username]["spedizione"][True]["inizio"])//60)
        except:
            delay = round((time.time() - player[message.from_user.username]["spedizione"]["true"]["inizio"])//60)
        
        if delay >= 15:
            try:
                win = player[message.from_user.username]["spedizione"][True]["value"]
                player[message.from_user.username]["spedizione"] = [False]
            except:
                win = player[message.from_user.username]["spedizione"]["true"]["value"]
                player[message.from_user.username]["spedizione"] = [False]
            win += round(delay/15)
            testo = f"Hai finito la ricognizione, sei stato fuori {delay} minuti e vinto {win} oggetti!\n"
            
            vertutto = tutto
            vincite = {}
            if evento["evento"] == "mega":
                                        vertutto = tuttov + megaman + megaman
            if evento["evento"] == "zombie":
                                        vertutto = tuttov + zombie + zombie
            if evento["evento"] == "gungeon":
                                        vertutto = tuttov + gungeon + gungeon
            if evento["evento"] == "magic":
                                        vertutto = tuttov + magic + magic + magic
            for gwefqw in range(win):
                vinto = random.choice(vertutto)
                try:
                    vincite[vinto] += 1
                except:
                    vincite[vinto] = 1
                
            for gwefqw in vincite:
                testo += f"{gwefqw} x {vincite[gwefqw]}\n"
                try:
                    player[message.from_user.username]["zaino"][gwefqw] += vincite[gwefqw]
                except:
                    player[message.from_user.username]["zaino"][gwefqw] = vincite[gwefqw]
            
            if len(testo) > 4096:
                testo = testo[:4095]
            #incartato
            await message.reply(testo)
        else:
            await message.reply(f"Sei stato troppo poco fuori, aspetta ancora un attimo({delay}/15)!")
    else:
        
        player[message.from_user.username]["spedizione"] = {True:{"inizio":time.time(),"value":0,"ultimoevento":time.time() }}
        await message.reply("Ti incammini per una ricognizione, nessuno sa esattamente cosa ti aspetta, ma lo scoprirai!")

@app.on_message(filters.private & ~ filters.user(bannati))
def check_spe(client,message):
    
    if list(player[message.from_user.username].get("spedizione",[False])) == [True] or list(player[message.from_user.username].get("spedizione",[False])) == ["true"] and message.from_user.username != 'NftChallengeBot':
        message.reply("Sei in giro, non puoi!")
    else:
        raise ContinuePropagation





@app.on_message(filters.command(["iscrivi", "iscrivi@NFTchallengebot"]) & ~filters.user(bannati))
async def fine(client, message):
    global lotteria
    username = message.from_user.username
    if username in player:

        if lotteria["Attiva"] == True:
            if lotteria["Iscrizioni"] == True:
                if username not in lotteria["Iscritti"]:
                    if message.chat.id == -1001549963117:

                        lotteria["Iscritti"].append(username)
                        await app.send_message(message.chat.id,"Iscritto!")
                    else:
                        await app.send_message(message.chat.id,"Non puoi iscriverti qui!")
                else:
                    await app.send_message(message.chat.id,"Sei già dentro!")
            else:
                await app.send_message(message.chat.id,"Non puoi ora!")
        else:
            await app.send_message(message.chat.id,"La lotteria non è aperta!")
    else:
        await app.send_message(message.chat.id,"Avvia il bot!")



@app.on_message(filters.command("resetboss") & filters.private & filters.user(autorizzati))
def reset(client, message):
    
    for a in player:

        player[a]["boss"] = dict()

        try:
            app.send_message(a, f"I boss paiono essersi calmati!")
        except:
            pass


@app.on_message(filters.command("ban") & filters.user(autorizzati)
)
def reset(client, message):
    if len(message.command) == 1:
        app.kick_chat_member(message.chat.id,message.reply_to_message.from_user.id)
        app.send_message(message.chat.id,f"{message.reply_to_message.from_user.username} bannato per seeeempre!")
    else:
        app.kick_chat_member(message.chat.id,message.reply_to_message.from_user.id, int(time.time() + int(message.command[1])))
        app.send_message(message.chat.id,f"{message.reply_to_message.from_user.username} bannato per un pochino di secondi, tipo {message.command[1]}!")

@app.on_message(filters.command("kick") & filters.user(autorizzati)
)
def reset(client, message):
    app.kick_chat_member(message.chat.id,message.reply_to_message.from_user.id, int(time.time() + 30))
    app.send_message(message.chat.id,f"{message.reply_to_message.from_user.username} cacciato via dal gruppo!")

@app.on_message(filters.command("sban") & filters.user(autorizzati)
)
def reset(client, message):
    if not message.reply_to_message:
        
        app.send_message(message.chat.id,f"No ecco, devi fare /sban in risposta alla persona!")
    else:
        try:
            app.unban_chat_member(message.chat.id, message.reply_to_message.from_user.username)
        
            app.send_message(message.chat.id,f"{message.reply_to_message.from_user.username} sbannato!")
        except:
            pass




@app.on_message(filters.command("iniziaevento") & filters.private & filters.user(autorizzati)
)
def reset(client, message):
    
    if len(trader["vorrei"]) == 0:
        scelto = random.choice(["gungeon", "zombie", "mega", "magic"])
    else:
        scelto = trader["vorrei"][0]
        trader["vorrei"] = list()
    mod = random.choice(["punti_extra", "calma", "sfide assurde", "stop_dg","più_dg","flexville",None,None,None])
    evento["mod"] = mod
    evento["evento"] = scelto

    with open("./backup/evento.json", "w") as outfile:
        json.dump(evento, outfile)

    if scelto == "gungeon":
        testo = "Le porte del gungeon 🔫 si aprono alla clientela, venite a soffrire con noi🐕!\nNuovi oggetti unici e set disponibili!"
    if scelto == "zombie":
        testo = "Una piccola epidemia zombie 🧟 coglie alla spovvista l'intero pianeta di NFT 🌎!\nNuovi oggetti e set unici si rivelano a noi!"
    if scelto == "mega":
        testo = "La cyber arena 🏟️ ha inizio, trovere tutto il necessario nelle sfide 💾!\nNuovi oggetti e set unici si rivelano a noi, decisamente particolari!"
    if scelto == "magic":
        testo = "Antichi poteri ed antiche magie si liberano per le terre di NFT!\nSei pronto ad impugnare questi arcani poteri?!\nDimostralo in sfida!"
    if mod != None:
        testo += "\n\nMod attuale:"
        if mod == "punti_extra":
            testo+= " Punti extra nelle sfide!"
        if mod == "calma":
            testo+= " Weekend di pausa, le sfide ci mettono un pò di più a partire!"
        if mod == "sfide assurde":
            testo+= " Sfide assurde abilitate, pronti a sfidare h24?!?!"
        if mod == "stop_dg":
            testo+= " I dungeon sono più scialli per questo weekend, prendetevi una pausa!"
        if mod == "più_dg":
            testo+= " Corri corri che il dungeon non aspetta nessuno, preparati ad una corsa assurda!"
        if mod == "flexville":
            testo+= " Tempi morti dimezzati, muori meno per vivere meglio!"
    
    try:
        app.send_message(-1001549963117, testo)
    except:
        pass
    



@app.on_message(filters.command("fineevnto") & filters.private & filters.user(autorizzati)
)
def reset(client, message):
    
    evento["evento"] = None
    evento["mod"] = None
    with open("./backup/evento.json", "w") as outfile:
        json.dump(evento, outfile)
    


@sched.scheduled_job("cron", day_of_week="sat", hour=8)
def inizio_weew():
    
    if len(trader["vorrei"]) == 0:
        scelto = random.choice(["gungeon", "zombie", "mega", "magic"])
    else:
        scelto = trader["vorrei"][0]
        trader["vorrei"] = list()
    mod = random.choice(["punti_extra", "calma", "sfide assurde", "stop_dg","più_dg","flexville",None,None,None])
    evento["mod"] = mod
    evento["evento"] = scelto

    with open("./backup/evento.json", "w") as outfile:
        json.dump(evento, outfile)

    if scelto == "gungeon":
        testo = "Le porte del gungeon 🔫 si aprono alla clientela, venite a soffrire con noi🐕!\nNuovi oggetti unici e set disponibili!"
    if scelto == "zombie":
        testo = "Una piccola epidemia zombie 🧟 coglie alla spovvista l'intero pianeta di NFT 🌎!\nNuovi oggetti e set unici si rivelano a noi!"
    if scelto == "mega":
        testo = "La cyber arena 🏟️ ha inizio, trovere tutto il necessario nelle sfide 💾!\nNuovi oggetti e set unici si rivelano a noi, decisamente particolari!"
    if scelto == "magic":
        testo = "Antichi poteri ed antiche magie si liberano per le terre di NFT!\nSei pronto ad impugnare questi arcani poteri?!\nDimostralo in sfida!"
    if mod != None:
        testo += "\n\nMod attuale:"
        if mod == "punti_extra":
            testo+= " Punti extra nelle sfide!"
        if mod == "calma":
            testo+= " Weekend di pausa, le sfide ci mettono un pò di più a partire!"
        if mod == "sfide assurde":
            testo+= " Sfide assurde abilitate, pronti a sfidare h24?!?!"
        if mod == "stop_dg":
            testo+= " I dungeon sono più scialli per questo weekend, prendetevi una pausa!"
        if mod == "più_dg":
            testo+= " Corri corri che il dungeon non aspetta nessuno, preparati ad una corsa assurda!"
        if mod == "flexville":
            testo+= " Tempi morti dimezzati, muori meno per vivere meglio!"
        
    try:
        app.send_message(-1001549963117, testo)
    except:
        pass
    

@sched.scheduled_job("cron", day_of_week="sun", hour=23)
def fine_weew():
    
    evento["evento"] = None
    evento["mod"] = None
    with open("./backup/evento.json", "w") as outfile:
        json.dump(evento, outfile)
    for a in player:
        player[a]["guerrieggiato"] = 0
        
    for g in clan:
        clan[g]["cariche"] = 2


def metereologia(attuale):
    if attuale in ["Normale","Nuvolo","Arieggiato"]:
        futuro = random.choice(["Pioggia","Soleggiato","Normale","Arieggiato","Caldo torrido"])
    elif attuale in ["Pioggia","Tempesta"]:
        futuro = random.choice(["Pioggia","Tempesta","Normale","Nuvoloso","Arieggiato", 'Arcobaleno'])
    elif attuale in ["Soleggiato","Caldo torrido",'Caldo infernale']:
        futuro = random.choice(["Caldo torrido",'Caldo infernale',"Soleggiato", 'Nuvoloso', 'Normale'])
    elif attuale in ["Arcobaleno"]:
        futuro =random.choice(["Caldo torrido","Pioggia","Normale"])
    else:
        futuro = "Normale"
    return futuro

switch = True

@sched.scheduled_job("interval", minutes=4, )
def auto_incarico():
    
    for cla in clan:
        nft.incarichiamo(cla,clan,player,app)

    #{True:{"inizio":time.time(),"value":0,"ultimoevento":time.time() }}
    for pla in player:
        if list(player[pla].get("spedizione",[False])) == [True] or list(player[pla].get("spedizione",[False])) == ["true"]:
            try:
                delayinit = round((time.time() - player[pla]["spedizione"][True]["inizio"])//60)
                delaylast = round((time.time() - player[pla]["spedizione"][True]["ultimoevento"])//60)
            except:
                delayinit = round((time.time() - player[pla]["spedizione"]["true"]["inizio"])//60)
                delaylast = round((time.time() - player[pla]["spedizione"]["true"]["ultimoevento"])//60)
            if delayinit >= 480:
                testo = f"Sei stato fuori ben {delayinit} minuti, devi tornare,hai trovato {win} oggetti!\n"
                try:
                    win = player[pla]["spedizione"][True]["value"]
                except:
                    win = player[pla]["spedizione"]["true"]["value"]
                player[pla]["spedizione"] = [False]
                vertutto = tutto
                vincite = {}
                if evento["evento"] == "mega":
                                            vertutto = tuttov + megaman + megaman
                if evento["evento"] == "zombie":
                                            vertutto = tuttov + zombie + zombie
                if evento["evento"] == "gungeon":
                                            vertutto = tuttov + gungeon + gungeon
                if evento["evento"] == "magic":
                                            vertutto = tuttov + magic + magic + magic
                for gwefqw in range(win):
                    vinto = random.choice(vertutto)
                    try:
                        vincite[vinto] += 1
                    except:
                        vincite[vinto] = 1
                
                for gwefqw in vincite:
                    testo += f"{gwefqw} x {vincite[gwefqw]}\n"
                    try:
                        player[pla]["zaino"][gwefqw] += vincite[gwefqw]
                    except:
                        player[pla]["zaino"][gwefqw] = vincite[gwefqw]
                if len(testo) > 4096:
                    testo = testo[:4096]
                app.send_message(pla,testo)
                
            elif delaylast >= 4 and 0.95 > random.random():
                cosa = random.choice(["+","+",".","-","-","+","+",".","-","-","*"])
                if cosa == "+":
                    app.send_message(pla,"Evento positivo!")
                    player[pla]["spedizione"][True]["value"] += 1
                    
                elif cosa == "-":
                    app.send_message(pla,"Evento negativo!")
                    player[pla]["spedizione"][True]["value"] -= 1
                    if player[pla]["spedizione"][True]["value"] <= 0:
                        player[pla]["spedizione"][True]["value"] = 0
                        
                elif cosa == ".":
                    app.send_message(pla,"Evento neutro!")
                    
                elif cosa == "*":
                    app.send_message(pla,"Evento speciale!")
                    player[pla]["spedizione"][True]["value"] += 2
                    
                
                player[pla]["spedizione"][True]["ultimoevento"] = time.time() - 2


@app.on_message(filters.command(["clan", "clan@NFTchallengebot", "cl"]) | filters.regex(r"^Clan 🔱") )
async def party(client, message):
    try:
        username = message.from_user.username
        for x in clan:
            if username in clan[x]["membri"]:
                player[username]["team"] = x
        if len(message.command) == 1:
            user = player[username]
            team = user["team"]
            if team != "nessuno":
                    try:

                        massimo = 5 + round(
                            clan[team]["villaggio"]["Accampamento"]["lv"] // 2
                        )
                    except:
                        massimo = 5
                    adesso = len(clan[team]["membri"])

                    testo = f"Villaggio del party {team}!\nEroi ({adesso}/{massimo}):\n"
                    for cittadino in clan[user["team"]]["membri"]:
                        try:
                            if clan[user["team"]]["inguerra"] == None:
                                potenza = player[cittadino]["punti"]
                            else:
                                try:
                                    potenza = clan[user["team"]]["danno"][cittadino]
                                except:
                                    potenza = "Non ha ancora attaccato!"
                            testo += f"-**{cittadino}** - {potenza}"
                            if cittadino in trader["battaglieri"]:
                                testo += " ⚔️"
                            if cittadino == clan[user["team"]]["Architetto"]:
                                testo += " 📐"
                            if cittadino == clan[user["team"]]["Gestore"]:
                                testo += " 🗝️"
                            if cittadino == clan[user["team"]]["Sarto"]:
                                testo += " 🧵"
                            if cittadino == clan[user["team"]]["Sacrificio"]:
                                testo += " 🩸"
                            if cittadino in inabilitati:
                                testo += " ⚰️"

                            testo += " " + liste.moji_posto[player[cittadino]["location"]]
                        except:
                            testo += f"-{cittadino} - non trovato!"
                        testo += "\n"
                    testo += "\nDifese:\n"
                    for difesa in clan[user["team"]]["order"]:

                        if difesa in clan[user["team"]]["villaggio"]:
                            finder = clan[user["team"]]["villaggio"][difesa]
                            hp = finder["hp"]

                            lv = finder["lv"]
                            testo += f"-{difesa} LV{lv} ({hp}❤️)\n"

                    potere = clan[user["team"]]["potere"]
                    inguerra = clan[user["team"]]["inguerra"]
                    potrebbero = str(clan[user["team"]]["cariche"])
                    if potrebbero != 0 and inguerra == None:
                        potrebbero += "\nInizia subito una guerra con /guerra!"
                    ini = str(time.ctime(clan[user["team"]]["inizio"]))[3:]
                    testo += f"Altre statistiche:\n -{potere} potere \n-Guerre possibili questa settimana: {potrebbero}\n-In guerra con {inguerra}\n-Inizio ultima guerra: {ini}\nUsa /clan help per tutti i comandi! \nPuoi migliorare o comprare strutture usando /clan Negozio!"
                    if "nucleo" in clan[user["team"]]:
                        nucleo = clan[user["team"]]["nucleo"]
                        testo += f"\n{nucleo} attivato!"
                    bottoni = [InlineKeyboardButton(text="Dettagli", callback_data="villo_dettagli")]
                    reply_markup = InlineKeyboardMarkup([bottoni])
                    await app.send_message(message.chat.id,testo,reply_markup=reply_markup)
            else:
                await message.reply("Non hai un clan!\nUsa /clan help per tutti i comandi!")

        else:
            username = message.from_user.username
            user = player[username]
            arg = message.command[1]

            if "Crea" in arg or "crea" in arg:
                if user["team"] == "nessuno":

                    if len(message.command) > 2:
                        nome = message.command[2:]
                        defi = nft.listToString(nome)

                        if defi not in list(clan):

                            if len(defi) > 25:
                                await app.send_message(message.chat.id,"Questo nome è decisamente troppo lungo!")
                            else:
                                user["team"] = defi
                                clan[defi] = {
                                    "punti": 0,
                                    "danni": dict(),
                                    "Creatore": username,
                                    "membri": [username],
                                    "Sacrificio": None,
                                    "villaggio": {
                                        "Spuntone malefico": {"hp": 5000, "lv": 1}
                                    },
                                    "cariche":2,
                                    "order": liste.order,
                                    "potere": 250,
                                    "inguerra": None,
                                    "Sarto": None,
                                    "Architetto": None,
                                    "Gestore": None,
                                    "last":{},
                                    "ultimoavversario":None,
                                    "inizio" : 0,
                                    "setting" : {'Bersaglio enorme': 'Classico', 'Muraglione extra': 'Possente', 'Spaventapasseri ornamentale': 'Magico', 'Clone': 'Aggressivo', 'Chiesa': 'Credente', 'Accampamento': 'Trappole danneggianti', 'Cane da guardia': 'Cane possente', 'Stazione laser di sicurezza': 'Mitragliatrice laser', 'Spuntone malefico': 'Palese', 'Cannoncino': 'Rumoroso', 'Sedimento del cucciolo': 'Assonnato', 'Centrale di cura centralizzata': 'Sparsa', 'Fabbro incantaspade': 'Malevolo'},
                                    "Bandiera": [
                                        [
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                        ],
                                        [
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                        ],
                                        [
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                        ],
                                        [
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                        ],
                                        [
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                        ],
                                        [
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                            "⬛️",
                                        ],
                                    ],
                                }

                                await app.send_message(message.chat.id,f"Hai creato il clan {defi}!")
                        else:
                            await app.send_message(message.chat.id,"Clan già esistente!")
                    else:
                        await app.send_message(message.chat.id,"/clan Crea Nome del clan!")
                else:
                    await app.send_message(message.chat.id,"Lascia prima il tuo attuale clan!")

            elif "Negozio" in arg or "negozio" in arg:

                if user["team"] != "nessuno":

                    if 1 == 1:

                        if len(message.command) == 2:
                            potere = clan[user["team"]]["potere"]
                            testo = f"Ecco a te un negozio dei potenziamenti possibili per il clan!\nHai al momeno {potere} potere!\n"
                            for struttura in liste.strutture:
                                if struttura in clan[user["team"]]["villaggio"]:
                                    lv = clan[user["team"]]["villaggio"][struttura]["lv"]
                                    prezzo = 25 * (lv + 1)
                                    if struttura == "Accampamento":
                                        prezzo += 50
                                    testo += f"🔝 `{struttura}` - {prezzo} potere\n"
                                else:
                                    testo += f"🆕 `{struttura}` - 25 potere\n"
                            testo += "Compra utilizzando /clan Negozio Struttura"
                            await app.send_message(message.chat.id,testo)

                        else:
                            if (
                                clan[user["team"]]["Creatore"] == username
                                or clan[user["team"]]["Architetto"] == username
                            ):
                                if len(message.command) > 2:
                                    nome = nft.listToString(message.command[2:])
                                    nome = nft.search(list(liste.starmi), nome)[0]
                                    
                                    if nome in liste.strutture:
                                        if nome in clan[user["team"]]["villaggio"]:
                                            lv = clan[user["team"]]["villaggio"][nome]["lv"]
                                            prezzo = 25 * (lv + 1)
                                            if nome == "Accampamento":
                                                prezzo += 50
                                            if clan[user["team"]]["potere"] >= prezzo:
                                                if nome == "Accampamento" and lv >= 6:
                                                    await app.send_message(message.chat.id,
                                                        "Al momento l'accampamento è al massimo!"
                                                    )
                                                else:

                                                    clan[user["team"]]["potere"] -= prezzo
                                                    clan[user["team"]]["villaggio"][nome]["lv"] += 1
                                                    if clan[user["team"]]["villaggio"][nome]["lv"] < 11:
                                                        clan[user["team"]]["villaggio"][nome][
                                                            "hp"
                                                        ] += liste.hps[nome]
                                                    lv += 1
                                                    await app.send_message(message.chat.id,
                                                        f"{nome} è salito al LV {lv}"
                                                    )

                                            else:
                                                await app.send_message(message.chat.id,
                                                    "Non avete abbastanza gloria!"
                                                )
                                        else:
                                            prezzo = 25
                                            if clan[user["team"]]["potere"] >= prezzo:
                                                clan[user["team"]]["potere"] -= prezzo
                                                clan[user["team"]]["villaggio"][nome] = {
                                                    "hp": liste.starmi[nome]["hp"],
                                                    "lv": 1,
                                                }
                                                await app.send_message(message.chat.id,
                                                    f"{nome} è stato aggiunto al villaggio!"
                                                )

                                            else:
                                                await app.send_message(message.chat.id,
                                                    "Non avete abbastanza gloria!"
                                                )
                                    else:

                                        await app.send_message(message.chat.id,
                                            "Non ho capito cosa intendi comprare!"
                                        )

                            else:
                                await app.send_message(message.chat.id,"Non hai poteri!")
                else:
                    await app.send_message(message.chat.id,"Non sei in un clan!")
            
            elif "assalto" in arg or "Assalto" in arg:
                try:
                    if user["team"] != "nessuno":
                        if clan[user["team"]]["inguerra"] == None:

                            if clan[user["team"]]['Sacrificio'] == username:
                                target = [None]
                                giocatore = copy.deepcopy(player[username]["scheda"])
                                nft.classe(giocatore,giocatore["set"], liste.bonus)
                                output = nft.assedio(player,
                                                     giocatore,
                                                     copy.deepcopy(clan[user["team"]]["villaggio"]),
                                                     target[0],
                                                     user["team"],
                                                     clan[user["team"]]["order"],
                                                     clan,
                                                     trader["meteo"][player[username]["location"]],
                                                     clan[user["team"]]["setting"])
                                
                                await message.reply(output)
               
                except Exception as err:
                    e = f"{type(err).__name__}: {err}"
                    await message.reply(e)
                                                        
            elif "Nomina" in arg or "nomina" in arg:
                if user["team"] != "nessuno":
                    if clan[user["team"]]["inguerra"] == None:

                        if clan[user["team"]]["Creatore"] == username:
                            if len(message.command) > 2:
                                nome = str(message.command[2]).replace("@", "")
                                nome = nft.search(clan[user["team"]]["membri"], nome)[0]
                                if (
                                    nome in list(player)
                                    or nome == "rimuovi"
                                    or nome == "Rimuovi"
                                ):
                                    if (
                                        nome in clan[user["team"]]["membri"]
                                        or nome == "rimuovi"
                                        or nome == "Rimuovi"
                                    ):
                                        ruolo = str(message.command[3])
                                        ruolo = nft.search([ "Architetto","Gestore","Creatore","Sarto","Sacrificio",], ruolo)[0]
                                        if ruolo in [
                                            "Architetto",
                                            "Gestore",
                                            "Creatore",
                                            "Sarto",
                                            "Sacrificio",
                                        ]:
                                            if nome == "rimuovi" or nome == "Rimuovi":
                                                nome = None
                                            if nome == None and ruolo == "Creatore":
                                                await app.send_message(message.chat.id,
                                                    "non puoi rimuovere il creatore!"
                                                )
                                            else:

                                                clan[user["team"]][ruolo] = nome
                                                await app.send_message(message.chat.id,"Fatto!")
                                        else:
                                            await app.send_message(message.chat.id,"Questo ruolo non esiste!")
                                    else:
                                        await app.send_message(message.chat.id,"Questo utente non è con voi!")
                                else:
                                    await app.send_message(message.chat.id,"L'utente non esiste!")

                            else:
                                bottoni = list()
                                for tipo in ["Architetto","Gestore","Creatore","Sarto","Sacrificio",]:
                                    bottoni.append(
                                            [InlineKeyboardButton(tipo, callback_data=f"nomina?{tipo}")]
                                        )
                                
                                reply_markup = InlineKeyboardMarkup(bottoni)
                                
                                await app.send_message(message.chat.id,"Che ruolo vuoi gestire?",reply_markup=reply_markup)
                        else:
                            await app.send_message(message.chat.id,"Non hai poteri!")
                    else:
                        await app.send_message(message.chat.id,"Non puoi farlo in guerra!")
                else:
                    await app.send_message(message.chat.id,"Non sei in un clan!")

            elif "Nucleo" in arg or "nucleo" in arg:
                if user["team"] != "nessuno":
                    if (clan[user["team"]]["Creatore"] == username or clan[user["team"]]["Architetto"] == username):
                        possibile = list()
                        for g in player[username]["zaino"]:
                            if g in liste.nuclei:
                                possibile.append(g)
                        bottoni = list()
                        for appz in possibile:
                                bottoni.append(
                                    [InlineKeyboardButton(appz, callback_data=f"nucleo_{appz}")]
                                )

                        reply_markup = InlineKeyboardMarkup(bottoni)
                        text = "Che nucleo scegli?"
                        try:
                            await app.send_message(message.chat.id,text, reply_markup=reply_markup)
                        except:
                            await message.reply("Non hai liste.nuclei!")
                            
            elif "Ordina" in arg or "ordina" in arg:
                if user["team"] != "nessuno":
                    if 1 == 1:

                        if (
                            clan[user["team"]]["Creatore"] == username
                            or clan[user["team"]]["Architetto"] == username
                        ):
                            text = "Ordine strutture:\n🏃‍♂️\n"
                            for stru in clan[user["team"]]["order"]:
                                text += f"-{stru}\n"
                            text += "🚩"
                            bottoni = list()
                            for appz in clan[user["team"]]["order"]:
                                bottoni.append(
                                    [InlineKeyboardButton(appz, callback_data=f"ordine_{appz}")]
                                )

                            reply_markup = InlineKeyboardMarkup(bottoni)

                            await app.send_message(message.chat.id,text, reply_markup=reply_markup)

                        else:
                            await app.send_message(message.chat.id,"Non hai poteri!")
                    else:
                        await app.send_message(message.chat.id,"Non puoi farlo in guerra!")
                else:
                    await app.send_message(message.chat.id,"Non sei in un clan!")

            elif "Invita" in arg or "invita" in arg:
                if user["team"] != "nessuno":
                    if clan[user["team"]]["inguerra"] == None:

                        if (
                            clan[user["team"]]["Creatore"] == username
                            or clan[user["team"]]["Gestore"] == username
                        ):
                            if len(message.command) > 2:
                                nome = str(message.command[2]).replace("@", "")
                                if nome in list(player):

                                    if player[nome]["team"] == "nessuno":
                                        if player[nome]["team"] != player[username]["team"]:

                                            invitante = player[username]["team"]
                                            finder = user["team"]
                                            try:

                                                massimo = 5 + round(
                                                    clan[finder]["villaggio"][
                                                        "Accampamento"
                                                    ]["lv"]
                                                    // 2
                                                )
                                            except:
                                                massimo = 5

                                            if len(clan[invitante]["membri"]) < massimo:
                                                await app.send_message(message.chat.id,"L'utente è stato preso!")
                                                player[nome]["team"] = invitante
                                                clan[invitante]["membri"].append(nome)
                                                try:

                                                    await app.send_message(
                                                        nome,
                                                        f"Sei ora nel clan {invitante}!",
                                                    )
                                                except:
                                                    pass
                                            else:
                                                await app.send_message(message.chat.id,"Questo clan è pieno!")

                                    else:
                                        await app.send_message(message.chat.id,"Questo utente ha già un clan!")
                                else:
                                    await app.send_message(message.chat.id,"L'utente non esiste!")

                            else:
                                await app.send_message(message.chat.id,"/clan Invita username!")
                        else:
                            await app.send_message(message.chat.id,"Non hai poteri!")
                    else:
                        await app.send_message(message.chat.id,"Non puoi farlo in guerra!")
                else:
                    await app.send_message(message.chat.id,"Non sei in un clan!")

            elif arg == "Lascia" or arg == "lascia":
                if user["team"] != "nessuno":
                    if clan[user["team"]]["inguerra"] == None:
                        if clan[user["team"]]["Creatore"] != username:
                            await app.send_message(
                                clan[user["team"]]["Creatore"],
                                f"{username} ha lasciato il clan!",
                            )
                            clan[user["team"]]["membri"].remove(username)
                            user["team"] = "nessuno"

                            await app.send_message(message.chat.id,
                                "Hai lasciato il tuo clan, non scoraggiarti!\nNe esistono di migliori!"
                            )
                        else:
                            await app.send_message(message.chat.id,"Non puoi lasciare il tuo team!")
                    else:
                        await app.send_message(message.chat.id,"Devi prima finire la guerra")
                else:
                    await app.send_message(message.chat.id,"Non hai un clan!")

            elif "Caccia" in arg or "caccia" in arg:
                if user["team"] != "nessuno":
                    if clan[user["team"]]["inguerra"] == None:
                        if len(message.command) > 2:
                            if (
                                clan[user["team"]]["Creatore"] == username
                                or clan[user["team"]]["Gestore"] == username
                            ):
                                nome = str(message.command[2]).replace("@", "")
                                if (
                                    nome in clan[user["team"]]["membri"]
                                    and nome != clan[user["team"]]["Creatore"]
                                ):

                                    clan[user["team"]]["membri"].remove(nome)
                                    await app.send_message(message.chat.id,"Cacciato con successo!")
                                    try:

                                        await app.send_message(
                                            nome, "Sei stato cacciato dal clan!"
                                        )
                                    except:
                                        pass
                                    player[nome]["team"] = "nessuno"
                                else:
                                    await app.send_message(message.chat.id,"Questo utente non è in team!")
                            else:
                                await app.send_message(message.chat.id,"Solo il capo può farlo!")
                        else:
                            await app.send_message(message.chat.id,"/clan Caccia utente")
                    else:
                        await app.send_message(message.chat.id,"Non puoi cacciare gente durante la guerra!")
                else:
                    await app.send_message(message.chat.id,"Non hai un clan!")

            elif arg == "Difesa" or arg == "difesa":
                if user["team"] != "nessuno":
                    team = user["team"]
                    if 1 == 1:
                        testo = "Ecco i tuoi villaggi in guerra:\n"
                        for teaz in clan:
                            if clan[teaz]["inguerra"] == team:
                                testo += f"**{teaz}**:\n"
                                for difesa in clan[teaz]["nemico"]:
                                    finder = clan[teaz]["nemico"][difesa]
                                    hp = finder["hp"]

                                    lv = finder["lv"]
                                    testo += f"-{difesa} LV{lv} ({hp}❤️)\n"
                                "\n\n"
                        await app.send_message(message.chat.id,testo)
                    else:
                        await app.send_message(message.chat.id,"Non ci sono guerre!")
                else:
                    await app.send_message(message.chat.id,"Non hai un team!")

            
            elif arg == "Help" or arg == "help":
                if 1 == 1:
                    await app.send_message(message.chat.id,
                """Argomenti validi:
    -`Crea` - Crea un clan!
    -`Invita` - Invita altri membri nel clan (Solo per il comandante)
    -`Caccia` - Caccia altri membri dal clan (Solo per il comandante) 
    -`Nomina` - Scegli chi vuoi siano `Sarto`,`Architetto`, `Sacrificio` e `Gestore` o addirittura `Creatore` del clan!
    -`Lascia` - Vai via dal clan   
    -`Help` - Questo menù
    -`Ordina` - Organizza il tuo villaggio
    -`Difesa` - Scruta il villaggio nelle guerre altrui
    -`nucleo` - Gestisci il nucleo del villaggio
    -`Elimina` - Elimina il clan, senza conferme o simili (Solo per il comandante)  
    __ Il sarto ha accesso a /disegna per il design della bandiera__
    /clan Argomento desiderato           
    """
            )
                
                else:
                    await app.send_message(message.chat.id,"Non hai un clan!")

            elif arg == "Elimina" or arg == "elimina":
                if user["team"] != "nessuno":
                    if clan[user["team"]]["Creatore"] == username:
                        if clan[user["team"]]["inguerra"] == None:

                            team = user["team"]

                            for m in clan[user["team"]]["membri"]:

                                player[m]["team"] = "nessuno"
                                try:

                                    await app.send_message(
                                        m, "Il tuo clan ha smesso di esistere!"
                                    )
                                except:
                                    pass

                            clan.pop(team)
                        else:
                            await app.send_message(message.chat.id,"Devi finire la guerra!")

                    else:
                        await app.send_message(message.chat.id,"Solo il capo può farlo!")
    except:
        user = player[username]
        team = user["team"]
        if team != "nessuno":
                    try:

                        massimo = 5 + round(
                            clan[team]["villaggio"]["Accampamento"]["lv"] // 2
                        )
                    except:
                        massimo = 5
                    adesso = len(clan[team]["membri"])

                    testo = f"Villaggio del party {team}!\nEroi ({adesso}/{massimo}):\n"
                    for cittadino in clan[user["team"]]["membri"]:
                        try:
                            if clan[user["team"]]["inguerra"] == None:
                                potenza = player[cittadino]["punti"]
                            else:
                                try:
                                    potenza = clan[user["team"]]["danno"][cittadino]
                                except:
                                    potenza = "Non ha ancora attaccato!"
                            testo += f"-**{cittadino}** - {potenza}"
                            if cittadino in trader["battaglieri"]:
                                testo += " ⚔️"
                            if cittadino == clan[user["team"]]["Architetto"]:
                                testo += " 📐"
                            if cittadino == clan[user["team"]]["Gestore"]:
                                testo += " 🗝️"
                            if cittadino == clan[user["team"]]["Sarto"]:
                                testo += " 🧵"
                            if cittadino == clan[user["team"]]["Sacrificio"]:
                                testo += " 🩸"
                            if cittadino in inabilitati:
                                testo += " ⚰️"

                            testo += " " + liste.moji_posto[player[cittadino]["location"]]
                        except:
                            testo += f"-{cittadino} - non trovato!"
                        testo += "\n"
                    testo += "\nDifese:\n"
                    for difesa in clan[user["team"]]["order"]:

                        if difesa in clan[user["team"]]["villaggio"]:
                            finder = clan[user["team"]]["villaggio"][difesa]
                            hp = finder["hp"]

                            lv = finder["lv"]
                            testo += f"-{difesa} LV{lv} ({hp}❤️)\n"

                    potere = clan[user["team"]]["potere"]
                    inguerra = clan[user["team"]]["inguerra"]
                    potrebbero = str(clan[user["team"]]["cariche"])
                    if potrebbero != 0 and inguerra == None:
                        potrebbero += "\nInizia subito una guerra con /guerra!"
                    ini = str(time.ctime(clan[user["team"]]["inizio"]))[3:]
                    testo += f"Altre statistiche:\n -{potere} potere \n-Guerre possibili questa settimana: {potrebbero}\n-In guerra con {inguerra}\n-Inizio ultima guerra: {ini}\nUsa /clan help per tutti i comandi! \nPuoi migliorare o comprare strutture usando /clan Negozio!"
                    if "nucleo" in clan[user["team"]]:
                        nucleo = clan[user["team"]]["nucleo"]
                        testo += f"\n{nucleo} attivato!"
                    
                    bottoni = [InlineKeyboardButton(text="Dettagli", callback_data="villo_dettagli")]
                    reply_markup = InlineKeyboardMarkup([bottoni])
                    await app.send_message(message.chat.id,testo,reply_markup=reply_markup)
        else:
                await message.reply("Non hai un clan!")

@sched.scheduled_job("interval", minutes=20)
def auto_backup():
    global switch
    global last_assalto
    global last_gift
    global last_pat
    global last_dungeon
    last_dungeon = dict()
    last_assalto = dict()
    last_gift = dict()
    last_pat = dict()
    with open("./backup/pozioni.json", "w") as outfile:
        json.dump(pozioni, outfile)
    
    with open("./backup/evento.json", "w") as outfile:
        json.dump(evento, outfile)

    with open("./backup/player.json", "w") as outfile:
        json.dump(player, outfile)
    with open("./backup/sicurezza.json", "w") as outfile:
        json.dump(sicurezza, outfile)
    
    with open("./backup/inabilitati.json", "w") as outfile:
        json.dump(inabilitati, outfile)
    with open("./backup/clan.json", "w") as outfile:
        json.dump(clan, outfile)
    txt = ""
       
    
    for x in player:
        player[x]["conosciuto"] = "no"
        auto_check(x)
    
    if switch == False:
        for c in liste.location:
            trader["meteo"][c] = metereologia(trader["meteo"][c])
        switch = True
    else:
        switch = False
    
    
            
        
        
    
    with open("./backup/trader.json", "w") as outfile:
        json.dump(trader, outfile)
    
    for cl in clan:
        if "nemico" in clan[cl]:
            elapsed = time.time() - clan[cl]["inizio"]
            if len(clan[cl]["nemico"]) == 0 or elapsed >= 86400:
                mod = 0.0
                if "comparo" not in clan[cl]:
                    clan[cl]["comparo"] = list(clan[clan[cl]["inguerra"]]["villaggio"])
                to_c = clan[cl]["comparo"]
                difficioltà = 0                                       
                for struttura in liste.order:
                    if struttura in to_c and struttura not in clan[cl]["nemico"]:
                        try:
                            difficioltà += int(
                                                    clan[clan[cl]["inguerra"]]["villaggio"][struttura]["lv"]
                                                )
                            mod += 0.04
                        except:
                            pass
                                                

                if len(clan[cl]["nemico"]) == 0:
                    mod += 0.3
                    pos = round((int(elapsed)/60)/60)
                    bonus = (12 - pos) * 0.02
                    mod += bonus
                else:
                    try:
                        app.send_message(clan[clan[cl]["inguerra"]]["Creatore"],f"Il clan nemico si allontana dal vostro villaggio sconfitto...\n100 punti e potere a voi!",)
                    except:
                        pass
                    clan[clan[cl]["inguerra"]]['potere'] += 100
                    clan[clan[cl]["inguerra"]]['punti'] += 100
                    
                    mod = mod / 4

                mod += difficioltà / 85
                if mod < 0:
                    mod = 0.1
                
                clan[cl]["inguerra"] = None
                clan[cl].pop("nemico")
                clan[cl].pop("comparo")

                premio = round(mod * 250)
                numero = round(premio / 10)
                try:
                    app.send_message(clan[cl]["Creatore"],
                                     f"La guerra è per ora terminata in {pos} ore contro un villaggio LV {difficioltà}!!\n\nVi viene aggiunta {premio} potenza al clan!\nOgni membro ottiene {premio} gloria e {numero} oggetti incartati!",
                                            )
                except:
                    pass
                try:
                        app.send_message(clan[clan[cl]["inguerra"]]["Creatore"],f"Recap:\nTempo impiegato ad abbattervi il villaggio {pos} ore.\nLV villaggio {difficioltà}",)
                except:
                        pass
                
                clan[cl]["potere"] += premio
                try:
                    clan[cl]["punti"] += premio
                except:
                    clan[cl]["punti"] = premio
                for mem in clan[cl]["membri"]:
                    player[mem]["guerrieggiato"] += 1
                    try:
                        try:
                            player[mem]["gloria"] += round(premio * 1.25)
                        except:
                            player[mem]["gloria"] = round(premio * 1.25)
                        try:
                            player[mem]["zaino"]["Un oggetto incartato"] += numero
                        except:
                            player[mem]["zaino"]["Un oggetto incartato"] = numero
                    except:
                        pass
                    try:
                        player[mem]["exp"]["expattuale"] += round(clan[cl]["danni"][mem]/1000)
                    except:
                        pass
                try:
                    clan[cl].pop("nucleo")
                except:
                    pass
    
    tot = 0
    for g in trader["sette"]:
        tot += int(trader["sette"][g]["iscritti"])

    for g in trader["sette"]:
        trader["sette"][g]["%"] = 100 - round((100 * int(trader["sette"][g]["iscritti"]))/tot)
      
    gc.collect()


@sched.scheduled_job("cron", hour=00)
def mezzanotte():
    
    trader["primo"] = None
    trader["bossoggi"] = nft.take_boss(liste.Boss, 3)
    for pozione in pozioni:
        pozioni[pozione] = nft.take_boss(allneed, 4)
    incolla = dict()
    for g in list(liste.descri):
        incolla[g] = 0
    
    for p in player:
        if player[p]["prima"] == False:
            player[p]["streak"] = 0
            if "Perditore" not in player[p]["obbiettivi"]:
                    player[p]["obbiettivi"].append("Perditore")
                    try:
                        app.send_message(
                            p, "Obbiettivo completato!\n**Perditore**, hai perso una streak!"
                        )
                    except:
                        pass
        else:
            player[p]["prima"] = False
        player[p]["arenagratis"] = True
        player[p]["oggi"] = 0
        player[p]["scheda"]["int"] = nft.intel(player[p]["zaino"],liste.decoro)
        player[p]["setta"]["libero"] = True
        for hhf in player[p]['obbiettivi']:
            try:
                incolla[hhf] += 1
            except:
                incolla[hhf] = 1
    trader["obquanti"] = incolla
    trader["stagione"] = random.choice(list(liste.arenamod))
    
@sched.scheduled_job("cron", hour="00,6,12,18")
def pescatore_cambio():
    for coso in player:
        vuole = random.choice(liste.pesci)
        player[coso]["richiesta_pescatore"] = vuole


@sched.scheduled_job("cron", hour="8,16,00")
def trafficante_cambio():
    for coso in player:
        for g in range(10):
            vuole = random.choice(tuttot + tuttot)
            da = random.choice(tutto)
            if vuole in liste.usabili or da == vuole:
                    pass
            else:
                    player[coso]["vuole"] = vuole
                    player[coso]["da"] = da
                    break

        
@sched.scheduled_job("cron", day_of_week="mon,fri", hour=00)
def rest_auto_top():
    
    premi = [
        "Uno scudo d'oro LV0",
        "Un pugnale d'oro LV0",
        "Una balestra d'oro LV0",
        "Spada d'oro fortissima LV0",
        "Elmo d'oro fortissimo LV0",
        "Anello d'oro fortissimo",
        "Un rolex oro LV0"
    ]
    #
    v = "Ecco a voi la top di mezza settimana!\n"
    d = dict()
    for tipo in player:
        if player[tipo]["punti"] == 1000 and tipo not in trader["battaglieri"]:
            pass
        else:
            d[tipo] = player[tipo]["punti"]

    sort_orders = sorted(d.items(), key=lambda x: x[1], reverse=True)
    addd = dict()
    for i in sort_orders:
        addd[i[0]] = i[1]

    x = 1
    for tipo in addd:
        v += f"{x}° {tipo} - {addd[tipo]} punti!"
        if x == 1 and "neeerrrd" not in player[tipo]["obbiettivi"]:
                    player[tipo]["obbiettivi"].append("neeerrrd")
                    try:
                        app.send_message(
                            tipo, "Obbiettivo completato!\n**neeerrrd**, perdi 100 ore di sonno ed arriva primo in tooop!"
                        )
                    except:
                        pass
        x += 1
        
        if x > 3 and 0.5 > random.random():
            premio = random.choice(premi)
            try:
                player[tipo]["zaino"][premio] += 1
            except:
                player[tipo]["zaino"][premio] = 1
            v += " ORO!"
            
            if "Luzzica" not in player[tipo]["obbiettivi"]:
                    player[tipo]["obbiettivi"].append("Luzzica")
                    try:
                        app.send_message(
                            tipo, "Obbiettivo completato!\n**Luzzica**, vinci un item oro!"
                        )
                    except:
                        pass
        v += "\n"
        if x > 15:
            break

    v += "\nChe scontri epici, vi lascio a voi i vostri premi!\nTroverete la gloria direttamente nelle vostre tasche ed i punti resettati a 1000!\nI migliori troveranno cose interessanti nel loro zainetto!\n"
    for a in player:

        punti = player[a]["punti"]
        player[a]["punti"] = 1000
        rest = (punti - 100) * (int(player[a]["livello"])/10)
        day = player[a]['streak']
        if rest > 0 and day > 4:

            gloria = round(rest / 10)
            try:

                app.send_message(
                    a,
                    f"Grazie alle sfide da te effettuate, le tua bravura e cose simili ottieni {gloria} gloria!",
                )
            except:

                pass
            try:
                player[a]["gloria"] += gloria
            except:
                player[a]["gloria"] = gloria
            
    app.send_message(-1001549963117, v)

@sched.scheduled_job("cron", day_of_week="Thu", hour=12)
def Auto_inizio_giovedì():
    if 1 == 2:
        eve = random.choice(["Randomedì!"])
        trader["Giovedì"] = eve
        text = f"Siniori e siniore ecco a voi un evento del giovedì!\n{eve}"
        app.send_message(-1001549963117, text)
    
@sched.scheduled_job("cron", day_of_week="fri", hour=12)
def Auto_fine_giovedi():
    trader["Giovedì"] = None   


@app.on_message(filters.command("ex") & filters.user(autorizzati))
def executer(app, message):
    
    if len(message.command) - 1:
        code = " ".join(message.text.split(" ")[1:])
        sys.stdout = result = StringIO()
        e = ""

        try:
            exec(code)
        except Exception as err:
            e = f"{type(err).__name__}: {err}"

        sys.stdout = sys.__stdout__

        resultvalue = result.getvalue()

        output = [
            f"**Code**:\n<code>{html.escape(code).strip()}</code>",
            f"**Result:**\n<code>{html.escape(resultvalue).strip()}</code>"
            if len(resultvalue) < 2000
            else "**Result:**",
            f"**Errors**:\n<code>{html.escape(e).strip()}</code>" if e else "",
        ]

        try:
            app.send_message(message.chat.id,"\n".join([elem for elem in output if elem]))

            if len(resultvalue) >= 2000:
                _tmp = BytesIO()
                _tmp.write(resultvalue.encode())
                _tmp.name = "exec.txt"

                app.send_document(message.chat.id, _tmp, thumb="MyUserbot/thumb.jpg")
        except:
            pass

    else:
        app.send_message(message.chat.id,"pong")

last_assalto = dict()


@app.on_message(filters.command(["bestiario", "bestiario@NFTchallengebot"]) & ~filters.user(bannati))
async def bestiarioc(client, message):
    username = message.from_user.username
    if len(player[username]["bestiario"]) > 0:

        zaino = player[username]["bestiario"]
        numero = len(player[username]["bestiario"])
        text = f"Al momento hai visto ben {numero} animali:"
        for figura in sorted(zaino):
            qt = zaino[figura]
            text += f"\n -🐟Pesce {figura} - {qt} Kg record"

        chunk = 4096

        for t in (text[i : i + chunk] for i in range(0, len(text), chunk)):
            await app.send_message(message.chat.id,t)
    else:
        await app.send_message(message.chat.id,"Meglio evitare, inizia a pescare!")

@app.on_message(filters.command(["donazioni", "donazioni@NFTchallengebot","donazione","dona"]) & ~filters.user(bannati) & ~filters.chat(non_qui))
def donazioni(c,message):
    message.reply("Siamo chiari fin da subito, il server si tiene su e si riesce a mantenere autonomamente, quindi l'unico modo per uccidere questo giochino è far scelrare (Di nuovo) ElSalamino.\n\nDetto ciò se vuoi donare per il foraggiamento del server e acquisto di nuove lucine per un pc fisso potete usare il link in fondo al messaggio.\n\nNon otterrete nulla, anche perchè le API di paypall sono lunghe e complicate, quindi dovrei fare tutto a mano e sono pigro, se proprio volete e mi venite a chiedere post pagamento vi posso lasciare un trofeo apposito che mi inventerò alla prima donazione.\n\n[Link](https://paypal.me/ElSalamino?locale.x=it_IT)")
    


tipi = {
    1: "Labirintico",
    2: "Segreto",
    3: "Canonico",
    4: "Centralizzato",
    5: "Regale",
    6: "Complicato",
    7: "Aulico",
    8: "Escherico",
    9: "Colossale",
}

last_arena = dict()
spiegazionearena = {"scelta variagate":"Più scelte per una caduta con stile","nulla per tutto":"Ad ogni nulla equipaggia un set",'normale': 'Classica arena...\\nDraft, set, magie e cose così', 'la classe è acqua': 'Set casuali ogni scelta casuale!', 'scontro magico': 'Magie a profusione, sarai degno di questa sfida?', 'scelta speciale': 'Solo item evento!', 'boss fight': 'Solo boss item!', 'alto livello': 'Combattimenti lv 5+, vietati i minori', 'rissa in arena': 'Colpi disonesti di sgabelli e tavoli!\\nAttento a cosa potrebbe arrivare, gli item normali non ci sono!', 'lotta tra nani': 'Armi giocattolo per combattenti giocattolo, divertitevi nani!', 'vecchi tempi': 'Tutto come una volta, solo vecchi item e set vecchi!\\nMolti set sono prenerf', 'anelli perfetti': 'Anelli del perfezionista a profusione, gli altri anche ma meno', 'sumo': 'Combattimenti nudi!', 'oro puro': 'Solo armi oro e flex!'}
@app.on_message( ~filters.user(bannati) & filters.private & (filters.regex(r"^Arena ☠️")| filters.command(["arena", "ar"])))
async def arenaff(client, message):
    username = message.from_user.username
    if 1 == 1:
        if "arena" in player[username]:
            try:
                await client.send_message(
                    chat_id=message.chat.id,
                    text="Usa questo messaggio qui per tornare all'arena",
                    reply_to_message_id=player[username]["arena"]["pin"]
                )
            except Exception as h:
                player[username].pop("arena")
                try:
                    await client.delete(
                    chat_id=message.chat.id,
                    reply_to_message_id=player[username]["arena"]["pin"]
                )
                except:
                    pass
                await message.reply(f"L'arena è stata chiusa per attività sospette\n{h}")
        else:
            bottoni = list()
            for appz in [f"Entra","Poi"]:
                bottoni.append([InlineKeyboardButton(appz, callback_data=f"arena_{appz}")])

            try:
                quanti = player[username]["zaino"]["Gettone arena"]
            except:
                quanti = 0
            if player[username]["arenagratis"] == True:
                prez = 0
            else:
                prez = 1
            reply_markup = InlineKeyboardMarkup(bottoni)
            stagio = trader["stagione"]
            bio = spiegazionearena[stagio]
            g = await message.reply(f"Sei sicuro di voler entrare nell'arena?\n\nStagione attuale:\n{stagio.title()}\n{bio}\n\nCosta {prez} gettone arena per entrare!({quanti} posseduti)",reply_markup=reply_markup)
            player[username]["arena"] = {
                        "Nome": username,
                        "hp": 1000,
                        "def": 100,
                        "atk": 100,
                        "agi": 20,
                        "int":0,
                        "Ap": "Base",
                        "schivato": False,
                        "anello": None,
                        "protezione": None,
                        "arma": None,
                        "boost": {"sfida": dict(), "assalto": dict()},
                        "set": None,
                        "draw":4,
                        "pin":g.message_id,
                        "W":0,
                        "L":0,
                        "incantamenti":[]
                    }
            await g.pin(both_sides = True)
            
@app.on_message( ~filters.user(bannati) & filters.private & (filters.regex(r"^Dungeon 🏃‍♂️")|filters.command(["dungeon", "dg"])))
async def dungeon(client, message):
    username = message.from_user.username
    if player[username]["location"] != "Hub":
        if "dungeon" in player[username]:
            numero = player[username]["dungeon"]["piano"]
            if numero > player[username]["topP"]:
                player[username]["topP"] = numero
            nemicii = len(player[username]["dungeon"]["mostri"])
            if nemicii == 0:
                player[username]["dungeon"] = nft.genera_dungeon(player,username)

            numero = player[username]["dungeon"]["piano"]
            cap = player[username]["dungeon"]["visibility"]
            tipo = tipi[cap]

            if player[username]["dungeon"]["danno"] < -500:
                player[username]["dungeon"]["danno"] = -500
            dann = player[username]["dungeon"]["danno"]
            testo = f"Entri nel dungeon, sei al piano {numero}, un piano {tipo}!\nHai ancora {nemicii} stanze sul piano, quale affronti prima?\n(Danno subito {dann})"
            bottoni = list()
            x = 0

            for appz in player[username]["dungeon"]["mostri"]:
                x += 1
                bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])
                if x == cap:
                    break
            reply_markup = InlineKeyboardMarkup(bottoni)

            await app.send_message(message.chat.id,testo, reply_markup=reply_markup)
        else:

            
            player[username]["dungeon"] = nft.genera_dungeon(player,username,"n")
            testo = f"Entri nel dungeon, sei al piano 0!\nHai ancora diverse stanze sul piano, quale affronti prima?"
            bottoni = list()
            x = 0
            for appz in player[username]["dungeon"]["mostri"]:
                x += 1
                bottoni.append([InlineKeyboardButton(appz, callback_data=f"dungi_{appz}")])
                if x == 6:
                    break

            reply_markup = InlineKeyboardMarkup(bottoni)
            await app.send_sticker(username,"CAACAgIAAxkBAAEcXvthe-42HzuvtszESUUn4eyKyXqbqgACQgADQbVWDA3cFm2mjQABmB4E")
            await app.send_message(message.chat.id,testo, reply_markup=reply_markup)
    else:
        await message.reply("Non ci sono dungeon qui!")


@app.on_message(filters.command(["ruota"]) & filters.private & ~filters.user(bannati))
async def ruota(client, message):
    username = message.from_user.username
    if player[username]["ruota"]:
        player[username]["ruota"] = False
        while True:
            scelto = random.choice(list(liste.classi))
            if len(liste.classi[scelto]) == 2:
                break
        text = f"Dato che sei nuovo e ti serve un aiutini ti rechi alla ruota della fortuna!\nLa spingi fortissimo e giiiiira,giiiira e giiiiira...\nSi ferma su {scelto}!\nNel tuo zaino compaiono i seguenti elementi:\n"
        for item in liste.classi[scelto]:
            try:
                player[username]["zaino"][item + " LV0"] += 1
            except:
                player[username]["zaino"][item + " LV0"] = 1
            text += item + " LV0\n"
            
        text += "\nIndossali per ottenere un set unico!"
        await message.reply(text)
    


@app.on_message(filters.command(["adunata", "adunata@NFTchallengebot"]) & ~filters.chat(non_qui))
async def party(client, message):
    username = message.from_user.username
    if player[username]["team"] != "nessuno":
        text = f"{username} chiama tutti all'attenti:\n"
        
        for x in clan[player[username]["team"]]["membri"]:
            if x != username:
                text += f"@{x}\n"

        await app.send_message(message.chat.id,text)


@app.on_message(filters.command("guerra"))
def inizio_guerra(c,message):
    username = message.from_user.username
    user = player[username]
    if user["team"] != "nessuno":
        if clan[user["team"]]["Creatore"] == username or username == "ElSalamino":
                if clan[user["team"]]["inguerra"] == None:
                    text = "Ecco dei possibili bersagli per questa guerra!"     
                    d = dict()
                    for tipo in clan:    
                        try:

                            d[tipo] = clan[tipo]["punti"] + 1
                        except:
                            d[tipo] = 0
                    
                    d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}  
                    pos = list()
                    attuale = list(d).index(user["team"])
                    
                    if attuale <= 2:
                        if attuale == 0:
                            pos.append(list(d)[attuale+1])
                            pos.append(list(d)[attuale+2])
                            pos.append(list(d)[attuale+3])
                        if attuale == 1:
                            pos.append(list(d)[attuale-1])
                            pos.append(list(d)[attuale+1])
                            pos.append(list(d)[attuale+2])
                        if attuale == 2:
                            pos.append(list(d)[attuale-1])
                            pos.append(list(d)[attuale-2])
                            pos.append(list(d)[attuale+1])
                        
                    else:
                        pos.append(list(d)[attuale-1])
                        pos.append(list(d)[attuale-2])
                        pos.append(list(d)[attuale-3])
                    
                    pos.append(trader["ricerca"])
                    
                    bottoni = list()
                    for appz in pos:
                        bottoni.append(
                            [InlineKeyboardButton(appz, callback_data=f"guerro_{appz}")]
                            )

                    reply_markup = InlineKeyboardMarkup(bottoni)
                    
                    if "setting" in clan[user["team"]]:
                        pass
                    else:
                        clan[user["team"]]["setting"] = dict()
                    try:
                        app.send_message(username,text, reply_markup=reply_markup)
                    except Exception as e:
                        print(e)
                        message.reply("Avvia il bot in privato!")
                    
                else:
                    app.send_message(message.chat.id,"Devi finire la guerra!")
        else:
            app.send_message(message.chat.id,"Solo il capo può farlo!")


@app.on_message( filters.private & ~filters.user(bannati) & (filters.regex(r"^Trafficante 🥷")| filters.command(["trafficante", "traffic"])))
async def trader_c(client, message):
    username = message.from_user.username
    richiesto = player[username]["vuole"]
    dato = player[username]["da"]
    if dato in liste.anelli:
        qt = 2
    else:
        qt = 1
    text = f"Salve {username}, cosa può interessarti dalla mia umile bancarella?\nSono un uomo di mondo, che non fa altro che offrire i suoi servizi alla communità...\nChe ne dici di un offerta?\nTi posso offrire **{qt} {dato}** per solamente 2 **{richiesto}**!\nCosa vuoi fare?"
    bottoni = [
        [
            InlineKeyboardButton(text="Accetta", callback_data="Traffi_Accetta"),
            InlineKeyboardButton(text="Passo.", callback_data="Traffi_Passo."),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(bottoni)
    await app.send_message(message.chat.id,text, reply_markup=reply_markup)


@app.on_message((filters.regex(r"^Obbiettivi 🎖")|filters.command(["obbiettivi"])) & filters.private & ~filters.user(bannati))
async def obbiettivi(client, message):
    username = message.from_user.username
    text = f"🌟Obbiettivi completati di {username}🌟\n"
    for boo in player[username]["obbiettivi"]:
        try:
            desc = liste.descri[boo]
        except:
            desc = "descrizione da fare"
        try:
            quin = trader["obquanti"][boo]
        except:
            quin = 0
        
        text += f"{boo} - {desc} ({quin} persone oltre te lo hanno)\n"

    await app.send_message(message.chat.id,text)


@app.on_message(filters.command(["saku"]) & filters.private & ~filters.user(bannati))
async def saku(client, message):
    username = message.from_user.username
    if (
        "armatura sakuretsu LV0" not in player[username]["zaino"]
        and evento["saku"] <= 120
    ):
        evento["saku"] += 1
        numero = evento["saku"]
        player[username]["zaino"]["armatura sakuretsu LV0"] = 1
        await app.send_message(message.chat.id,
            f"Arrivi al santuario del fato, sulla cima del monte dello spirito, nel continente del nord, sul pianteta di NFT.\nDato il tuo lungo viaggio vieni ricompensato con un **armatura sakuretsu LV0**, la {numero}° generata dal mistico fabbro del santuario."
        )
    else:
        pass


@app.on_message(filters.command(["suggerisci"]) & filters.private & ~filters.user(bannati))
def suggerisci(client, message):
    if message.reply_to_message:
        if message.from_user.username not in ["Veenquellovero","TheFBIsus"]:
            testo = message.reply_to_message.text
            for x in ["Culo","Cazzo","Tette","Figa","@","Sesso","Sesso oscuro","Schifo","LootBot","Dio"]:
                testo.lower().replace(x.lower(),"")
            if "#" in testo:
                idx = str(len(trader["Suggerimenti"]) + 1 * 2)
                trader["Suggerimenti"][idx] = {"Karma":0,"Votanti":dict(),"Proprietario":message.from_user.username}
                bottoni = list()
                    
                bottoni.append([InlineKeyboardButton("1", callback_data=f"suggerisci*1_{idx}"),InlineKeyboardButton("2", callback_data=f"suggerisci*2_{idx}")])
                bottoni.append([InlineKeyboardButton("3", callback_data=f"suggerisci*3_{idx}"),InlineKeyboardButton("4", callback_data=f"suggerisci*4_{idx}")])
                bottoni.append([InlineKeyboardButton("5", callback_data=f"suggerisci*5_{idx}"),])
                bottoni.append([InlineKeyboardButton("Chiudi", callback_data=f"suggerisci*Chiudi_{idx}")])
                    
                reply_markup = InlineKeyboardMarkup(bottoni)
                testo = f"Suggerimento id {idx}\n\n{testo}\nKarma | 0"
                message.reply(f"Fatto, sei il fiero proprietario del suggerimento {idx}")
                app.send_message(-1001542640246,testo, reply_markup=reply_markup)
                
            else:
                message.reply("Usa degli # per segnare le tematiche del tuo suggerimento!")
        else:
            message.reply("A causa di qualcosa che hai fatto non puoi suggerire!")
    else:
        message.reply("Rispondi al testo del suggerimento, ricordati di usare gli # per segnalare le tematiche")
    
@app.on_message( filters.private & ~filters.user(nop) & (filters.regex(r"^Boss 👹")|filters.command(["boss"])))
async def boss(client, message):
    username = message.from_user.username
    if "boss" in player[username]:
        pass
    else:
        player[username]["boss"] = dict()

    txt = "I boss sono acerrimi nemici di noi sfigatelli di NFT!\nE' importante prepararsi bene prima di scegliere che boss si vuole affrontare!\nInformati con /wikiboss!\nIn caso di vittoria ricchi ed unici premi!\nViceversa ore ed ore di sofferenza!\n"
    txt += "\nOggi ci sono i seguenti boss:\n"
    for b in trader["bossoggi"]:
        if b in player[username]["boss"]:
            lv = player[username]["boss"][b]
            txt += f"{b} - lv {lv}\n"
        else:

            txt += f"{b} - Nuovo!\n"

    bottoni = list()
    for appz in trader["bossoggi"]:
        bottoni.append([InlineKeyboardButton(appz, callback_data=f"bossveri_{appz}")])

    reply_markup = InlineKeyboardMarkup(bottoni)

    await app.send_message(message.chat.id,txt, reply_markup=reply_markup)

@app.on_message( filters.private & ~filters.user(bannati) & (filters.regex(r"^Muoviti 🚩")|filters.command(["muoviti"])))
async def muoviti(client, message):
    username = message.from_user.username
    loc = player[username]["location"]
    txt = f"""{username}, è ora di muoversi, sei stato a {loc} troppo tempo!
Questo posto non offre molte possibilità ma almeno 3 sono facilmente individuabili!
Dove si va?"""        

    bottoni = list()
    if player[username]["location"] != "Hub":
        for appz in liste.move[player[username]["location"]]:
            bottoni.append([InlineKeyboardButton(appz, callback_data=f"sposto_{appz}")])
    else:
        for appz in nft.take_boss(liste.location,9):
            bottoni.append([InlineKeyboardButton(appz, callback_data=f"sposto_{appz}")])
    reply_markup = InlineKeyboardMarkup(bottoni)

    await app.send_message(message.chat.id,txt, reply_markup=reply_markup)

@app.on_message( filters.private & ~filters.user(bannati) & (filters.regex(r"^Setta ©️")| filters.command(["setta"])))
async def setta(client, message):
    username = message.from_user.username
    loc = player[username]["location"]
    txt = f"""{username}, sei arrivato alla setta del territorio di {loc}"""        

    bottoni = list()
    if player[username]["livello"] >= 10:
        if player[username]["setta"]["libero"]:
            if player[username]["location"] != "Hub":
                for appz in ["Accetto","Non accetto"]:
                    bottoni.append([InlineKeyboardButton(appz, callback_data=f"setta_{appz}")])
                reply_markup = InlineKeyboardMarkup(bottoni)

                if player[username]["setta"]["benedizione"] != None:
                    txt += "\nSei al momento in un altra setta, possedendo questo bonus!\n"
                    
                    a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
                    txt += trader["sette"][player[username]["setta"]["loc"]]["Bonus"].format(a)
                
                settia = trader["sette"][loc]["Nome"]
                txt += f"\nTi vuoi affiliare alla setta del {settia}?"
                await app.send_message(message.chat.id,txt, reply_markup=reply_markup)
        
            else:
                await message.reply("Qui non esiste nessuna setta, prova a muoverti con /muoviti")
        
        else:
            if player[username]["setta"]["benedizione"] != None:
                a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
                txt = trader["sette"][player[username]["setta"]["loc"]]["Bonus"].format(a)
            await message.reply(f"Sei passato ad un altra setta poco fà!\nBonus attuale:\n{txt}")
    else:
        await message.reply("Sei di livello troppo basso, devi almeno essere di lv 10 per entrare in una setta")

def split(l, n):
    """
    Split a list into n chunks.
    """
    return [l[i:i+n] for i in range(0, len(l), n)]
        
@app.on_message((filters.regex(r"^Notifiche 🛎")|filters.command(["notifiche"])) & filters.private & ~filters.user(bannati))
async def notifiches(client, message):
    username = message.from_user.username
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
    await app.send_message(message.chat.id,text=testo, reply_markup=reply_markup)


@app.on_message(filters.regex(r"^Invita 📮")|filters.command(["invita", "invita@NFTchallengebot"]) & ~filters.user(bannati)
)
async def invita(client, message):
    username = message.from_user.username

    inviti = player[username]["inviti"]
    az = inviti["link"]
    link = f"t.me/NftChallengeBot?start={az}"
    numero = inviti["numero"]
    await app.send_message(message.chat.id,
        f"Ecco a te il tuo link d'invito al bot:\n{link}\nHai inviato già {numero} persone!"
    )


@app.on_message(filters.command(["bandiera", "bandiera@NFTchallengebot"]) & ~filters.user(bannati) & ~filters.chat(non_qui)
)
async def bandiera(client, message):
    username = message.from_user.username
    if player[username]["team"] != None and player[username]["team"] != "nessuno":
        team = player[username]["team"]
        if "Bandiera" in clan[team]:
            testo = (
                "Sventoli con felicità la bandiera del tuo clan davanti a tutti!\n\n\n"
            )
            for riga in clan[team]["Bandiera"]:
                testo += nft.listToString(riga) + "\n"

            await app.send_message(message.chat.id,testo)
        else:
            await app.send_message(message.chat.id,"Nessuno ha mai disegnato la vostra bandiera!")
    else:
        await app.send_message(message.chat.id,"Non hai un team!")


@app.on_message(filters.command(["disegna", "disegna@NFTchallengebot"]) & ~filters.user(bannati) & ~filters.chat(non_qui)
)
async def disegna(client, message):
    username = message.from_user.username
    if player[username]["team"] != None and player[username]["team"] != "nessuno":
        team = player[username]["team"]
        if clan[team]["Sarto"] == username:
            if len(message.command) == 1:
                await app.send_message(message.chat.id,"Usa /disegna x y emoji per sostituire una casella!")
            try:
                x = int(message.command[1]) - 1
                y = int(message.command[2]) - 1
                emoji = message.command[3][0]
                
                clan[team]["Bandiera"][x][y] = emoji
                await app.send_message(message.chat.id,"Fatto")
            except:
                await app.send_message(message.chat.id,"Mmmm, non credo vada bene così...")
        else:
            await app.send_message(message.chat.id,"Non sei il sarto del clan!")
    else:
        await app.send_message(message.chat.id,"Non sei in un clan!")


@app.on_message(filters.command(["gloria", "gloria@NFTchallengebot"]) & ~filters.user(bannati)
)
async def gloria(client, message):
    username = message.from_user.username
    if "gloria" in player[username] and not player[username]["gloria"] <= 0:
        inviti = player[username]["gloria"]
        await app.send_message(message.chat.id,
            f"{username} possiedi ben {inviti} gloria, devi esserne molto orglorioso!"
        )

    else:
        await app.send_message(message.chat.id,
            f"{username} non possiedi gloria,non devi esserne molto orglorioso!"
        )

@app.on_message(filters.command(["mappa", "mappa@NFTchallengebot"]) & ~filters.user(bannati)
)
async def gloria(client, message):
    username = message.from_user.username
    
    await app.send_photo(message.chat.id,
            "AgACAgQAAxkDAAEcAgxhenCPXuCfmKevrJJKyWv8ZBnpQgACOrwxG7u50VMG6VQVL7lViaX8pC9dAAMBAAMCAAN5AANdVwUAAR4E"
        )



@app.on_message(filters.command(["nomina", "nomina@NFTchallengebot"]) & ~filters.user(bannati) & ~filters.chat(non_qui)
)
async def nomina(client, message):
    username = message.from_user.username
    if "pet" in player[username]:
        if len(message.command) == 1:
            await app.send_message(message.chat.id,"/nomina nome del pet!")
        else:
            nome = nft.listToString(message.command[1:]).replace("<", "")

            if len(nome) <= 25:

                player[username]["NomePet"] = nome

                await app.send_message(message.chat.id,f"Il tuo pet ora si chiama {nome}")
            else:
                await app.send_message(message.chat.id,"Pare lunghetto...")
    else:
        await app.send_message(message.chat.id,"Non hai un pet!")


@app.on_message(filters.command(["aiuta", "aiuta@NFTchallengebot"]) & ~filters.user(bannati) & ~filters.chat(non_qui))
async def aiutaa(client, message):
    username = message.from_user.username
    if "Boss" in player[username]["dungeon"]:
        chi = player[username]["dungeon"]["Boss"]
        text = f"{username} necessita di una mano per il prossimo boss nel dungeon, {chi}!"
        bottoni = [InlineKeyboardButton(text="Aiuto", callback_data="Aiuto")]
        reply_markup = InlineKeyboardMarkup([bottoni])
        await app.send_message(message.chat.id,text=text, reply_markup=reply_markup)


@app.on_message(filters.command(["spedizione", "spedizione@NFTchallengebot"]) & ~filters.user(bannati) & ~filters.private)
async def aiutaa(client, message):
    username = message.from_user.username
    clon = clan[player[username]["team"]]
    if "incarico" in clon:
        await message.reply("Non puoi lasciare vuoto il villaggio, aspetta il ritorno dei tuoi amici!")
    else:
        ps = player[username]["team"]
        clon["pronti"] = [username]
        text = f"{username} cerca validi compagni per ricercare il nucleo bianco!\nChi è pronto?\n"
        for h in clon["pronti"]:
            text += f"-{h}\n"
        text += "A 4 si parte subitissimo!"
        bottoni = [InlineKeyboardButton(text="Io", callback_data=f"spedizione_{ps}")]
        reply_markup = InlineKeyboardMarkup([bottoni])
        await app.send_message(message.chat.id,text=text, reply_markup=reply_markup)

@app.on_message(filters.command(["rapporto", "rapporto@NFTchallengebot"])  & ~filters.user(bannati) & ~filters.private)
async def aiutaa(client, message):
    username = message.from_user.username
    clon = clan[player[username]["team"]]
    if "incarico" in clon:
        gh = "Qui pare mancare:\n"
        for g in clon["incarico"]["partecipanti"]:
            if g not in clon["incarico"]["mancano"]:
                gh += f"@{g}!\n"
        if gh == "Qui pare mancare:\n":
            gh += "Stocazzo!"
        await message.reply(gh)
    

last_gift = dict()
regali = dict()



@app.on_message(filters.command(["rissa", "rissa@NFTchallengebot"]) & ~filters.user(bannati) & filters.user(mediotourizzati))
def rissac(client, message):
    username = message.from_user.username
    bottoni = [InlineKeyboardButton(text="Io!", callback_data=f"rissa_Io!"),InlineKeyboardButton(text="Inizia!", callback_data=f"rissa_Inizia!")]
    
    reply_markup = InlineKeyboardMarkup([bottoni])
    txt = f"{username} inizia una rissa!\n"
    app.send_message(message.chat.id,txt, reply_markup=reply_markup)
    
    
@app.on_message(filters.command(["regala", "regala@NFTchallengebot"]) & ~filters.user(bannati) & ~filters.private)
async def regala(client, message):
    username = message.from_user.username
    if message.chat.id == -1001549963117:
        try:
            other_time = last_gift[username]
        except:
            other_time = 1

        now = time.time()

        elapsed = now - other_time

        if elapsed > 40:

            user = player[username]
            zaino = user["zaino"]
            if len(message.command) > 1:

                list_oggetto = nft.listToString(message.command[1:])
                if list_oggetto in tutto:
                    risultati = [list_oggetto]
                else:
                    risultati = nft.search(zaino, list_oggetto)

                if len(list(risultati)) > 1:
                    await app.send_message(message.chat.id,"Sii più preciso!")
                elif len(list(risultati)) == 0:
                    await app.send_message(message.chat.id,
                        "Non ci sono oggetti così chiamati nel tuo zaino!"
                    )
                elif len(list(risultati)) == 1:
                    to_give = risultati[0]
                    if to_give not in liste.bloccati:
                        last_gift[username] = time.time()
                        player[username]["zaino"][to_give] -= 1
                        if player[username]["zaino"][to_give] <= 0:
                            player[username]["zaino"].pop(to_give)

                        idx = str(len(regali) + 1 * 2)
                        bottoni = [InlineKeyboardButton(text="Mio", callback_data=f"reg_{idx}")]
                        regali[idx] = {"dachi": username, "cosa": to_give}
                        reply_markup = InlineKeyboardMarkup([bottoni])
                        txt = f"{username} lancia in aria {to_give}!\nChi lo prenderà?"
                        await app.send_message(message.chat.id,txt, reply_markup=reply_markup)
                        if "Bello e bravo" not in player[username]["obbiettivi"]:
                            player[username]["obbiettivi"].append("Bello e bravo")
                            try:
                                await app.send_message(
                                    username,
                                    "Obbiettivo completato!\n**Bello e bravo**, sei decisamente un ottima persona!",
                                )
                            except:
                                pass

            else:
                await app.send_message(message.chat.id,"/regala oggetto")

        else:
            pass
    else:
        pass


last_pat = dict()

@app.on_message(filters.command(["meteo", "meteo@NFTchallengebot"]) & ~filters.user(bannati) & ~filters.chat(non_qui))
async def meteo(client, message):
    username = message.from_user.username
    loca = player[username]["location"]
    mete = trader["meteo"][loca]
    await app.send_message(message.chat.id,f"Ti trovi a {loca}, e qui il meteo pare {mete}!")    

@app.on_message(filters.command(["pat", "pat@NFTchallengebot"]) & ~filters.user(bannati) & ~filters.chat(non_qui))
async def pat(client, message):
    username = message.from_user.username
    if "pet" in player[username]:
        if "ricerca" not in player[username] or player[username]["ricerca"] == None:
            if message.chat.id == -1001476172565:
                pass
            else:

                pet = player[username]["pet"]
                other_time = last_pat.get(username,1)

                now = time.time()

                elapsed = now - other_time

                if elapsed > 10:
                    if "NomePet" in player[username]:
                        nome = player[username]["NomePet"] + ", "
                    else:
                        nome = ""
                    last_pat[username] = now
                    await app.send_message(message.chat.id,
                        f"Fai pat pat a {nome}{pet.lower()}, lui si che è un bravo animaletto!\n__Il tuo animaletto si sente più amato__"
                    )
                    try:
                        player[username]["varie"]["pat"] += 1
                    except:
                        player[username]["varie"]["pat"] = 1

                    if player[username]["varie"]["pat"] == 666:
                        tipo = random.choice(["leddissima", "velocissima"])
                        player[username]["zaino"][f"Una ventolina {tipo}"] = 1
                        await app.send_message(message.chat.id,
                            "Wow!\nGrazie a te il server è forse 1° più caldo!"
                        )
                else:
                    await app.send_message(message.chat.id,"Piano piano!\nSennò lo rompi!")
        else:
            tipo = random.choice(list(player))
            await app.send_message(message.chat.id,
                f"Vorresti fare pat pat al tuo animaletto, ma non c'è più...\nSe vuoi puoi pattare {tipo} al suo posto!"
            )

    else:
        await app.send_message(message.chat.id,f"Non hai un animaletto da coccolare")


@app.on_message(filters.command(["forgia", "forgia@NFTchallengebot"]) & ~filters.user(bannati) & ~filters.chat(non_qui))
async def forgia(client, message):
    username = message.from_user.username

    if len(message.command) == 1:
        await app.send_message(message.chat.id,
            "La forgia è un luogo mistico, pieno di fiamme e cose così.\nQui dentro puoi offrire al grande fabbro con sicuramente un nome 2 armi o protezioni UGUALI per farle salir di livello!\nL'azione non richiede attese ma costa 10 gloria * lv item.\nPer iniziare a forgiare devi essere almeno lv1, inoltre non devi indossare il pezzo che desideri riforgiare.\n\nInizia quando vuoi con /forgia nomeoggetto"
        )
    else:
        user = player[username]
        zaino = user["zaino"]
        list_oggetto = nft.listToString(message.command[1:])
        if ":" in message.text:
            
            try:
                qt = int(list_oggetto.split(":")[1])
            except:
                
                qt = 1
            list_oggetto = list_oggetto.split(":")[0]
            
            
            if qt <= 0:
                qt = 1
            need = 2 * qt
        else:
            need = 2
        if list_oggetto in zaino:
            risultati = [list_oggetto]
        else:

            risultati = nft.search(zaino, list_oggetto)
        if 1 == 1:

            if len(list(risultati)) > 1:
                await app.send_message(message.chat.id,"Sii più preciso!")
            elif len(list(risultati)) == 0:
                await app.send_message(message.chat.id,"Non ci sono oggetti così chiamati nel tuo zaino!")
            elif len(list(risultati)) == 1:
                item = risultati[0]
                if (item == player[username]["scheda"]["arma"] or item == player[username]["scheda"]["protezione"]):
                    need += 1
                if (item in armi or item in protezioni and item != "armatura sakuretsu LV0"):
                    listina = item.split("LV")

                    lv = listina[1]
                    if lv == "X":
                        lv = 10
                    prezzo = int(int(lv) * 10)
                    if ":" in message.text:
                        prezzo = int(int(lv) * 10) * qt
                        
                    if prezzo <= player[username]["gloria"]:
                        if lv == 10:
                            lv = "X"
                        if lv != "X":
                            coso = listina[0]
                            if player[username]["zaino"][item] >= need:
                                if (item == player[username]["scheda"]["arma"] or item == player[username]["scheda"]["protezione"]):
                                    need -= 1
                                nft.gestione_zaino(zaino,"rem",item,need)
                                lv = int(lv) + 1
                                player[username]["gloria"] -= prezzo
                                if lv == 10:
                                    lv = "X"
                                new_it = f"{coso}LV{lv}"
                                nft.gestione_zaino(zaino,"add",new_it,round(need//2))
                                await app.send_message(message.chat.id,
                                    f"Il fabbro che ha sicuramente un nome prende {need} {coso} e dopo diverse martellate lo potenzia!\nOra ha il 10% aggiuntivo di tutte le stats!\nTi è costato {prezzo} Gloria!"
                                )
                                if (
                                    "Come non bruciarsi"
                                    not in player[username]["obbiettivi"]
                                    and lv == 2
                                ):
                                    player[username]["obbiettivi"].append(
                                        "Come non bruciarsi"
                                    )
                                    await app.send_message(message.chat.id,
                                        "Obbiettivo completato!\n**Come non bruciarsi**, sei bravo a forgiare!"
                                    )
                                if (
                                    "Forgiatore seriale"
                                    not in player[username]["obbiettivi"]
                                    and lv == 5
                                ):
                                    player[username]["obbiettivi"].append(
                                        "Forgiatore seriale"
                                    )
                                    await app.send_message(message.chat.id,
                                        "Obbiettivo completato!\n**Forgiatore seriale**, sei migliorato a forgiare!"
                                    )
                                if (
                                    "El forgiator" not in player[username]["obbiettivi"]
                                    and lv == 9
                                ):
                                    player[username]["obbiettivi"].append("El forgiator")
                                    await app.send_message(message.chat.id,
                                        "Obbiettivo completato!\n**El forgiator**, che mostro del forging!"
                                    )
                            else:
                                txt = f"Ti servono {need} copie di questo item"
                                if (item == player[username]["scheda"]["arma"] or item == player[username]["scheda"]["protezione"]):
                                    txt += f"\nSe te lo togliessi ne servirebbero solo {need-1}"
                                await app.send_message(message.chat.id,txt)
                        
                        else:
                            await app.send_message(message.chat.id,"Quest'ogetto è inforgiabile!")
                    else:
                        await app.send_message(message.chat.id,f"Non hai abbastanza gloria, te ne serve {prezzo}!")
                else:
                    await app.send_message(message.chat.id,"Questo oggetto non è forgiabile")





@app.on_message(filters.command(["mostra", "mostra@NFTchallengebot", "m"]) & ~filters.user(bannati)
)
async def mostra(client, message):
    username = message.from_user.username

    if len(message.command) == 1:
        await app.send_message(message.chat.id,"/mosta oggetto")
    else:
        if 1 == 1:

            user = player[username]
            zaino = user["zaino"]
            list_oggetto = nft.listToString(message.command[1:])
            if list_oggetto in tutto:
                risultati = [list_oggetto]
            else:
                risultati = nft.search(zaino, list_oggetto)

            if len(list(risultati)) > 1:
                await app.send_message(message.chat.id,"Sii più preciso!")
            elif len(list(risultati)) == 0:
                await app.send_message(message.chat.id,"Non ci sono oggetti così chiamati nel tuo zaino!")
            elif len(list(risultati)) == 1:
                qt = zaino[risultati[0]]
                if risultati[0] in armi or risultati[0] in protezioni:
                    try:
                        arma = risultati[0]
                        v = armi[arma]["hp"]
                        a = armi[arma]["atk"]
                        d = armi[arma]["def"]
                        ag = armi[arma]["agi"]
                        cosa = "Arma"
                    except:
                        arma = risultati[0]
                        v = protezioni[arma]["hp"]
                        a = protezioni[arma]["atk"]
                        d = protezioni[arma]["def"]
                        ag = protezioni[arma]["agi"]
                        cosa = "Protezione"
                    t = f"""{risultati[0]}
Vitalità : {v}
Attacco: {a}
Difesa: {d}
Agilità: {ag}
Questa pare essere un __{cosa}__
Ne possiedi {qt} copie.
                    """
                    
                    t+= "\nQuest'oggetto ha il seguente incantamento addosso:\n"
                    try:
                        t += str(player[username]["incantamenti"][risultati[0][:-4]])
                    except:
                        t += "Nessuno"
                if risultati[0] in liste.anelli:
                    aa = liste.anelli[risultati[0]]
                    t = f"{risultati[0]}\n__{aa}__\nNe possiedi {qt} copie."
                if risultati[0] in liste.usabili:
                    aa = liste.usabili[risultati[0]]
                    t = f"{risultati[0]}\n__{aa}__\nNe possiedi {qt} copie."
                if risultati[0] in liste.decoro:
                    aa = liste.decoro[risultati[0]]
                    t = f"{risultati[0]}\n__{aa}__\nNe possiedi {qt} copie."
                if risultati[0] in liste.libri:
                    aa = liste.libri[risultati[0]]["descrizione"]
                    bb = liste.libri[risultati[0]]["ef"]
                    t = f"{risultati[0]}\nQuesto libro contiene: **{bb}**\n__{aa}__\nNe possiedi {qt} copie."
                
            else:
                t = "Nessun risultato"

            try:

                if risultati[0][:-4] in liste.eventi:
                    eventoz =liste. eventi[risultati[0][:-4]]
                    t += f"\n**{eventoz}**"
                if risultati[0] in liste.eventi:
                    eventoz =liste. eventi[risultati[0]]
                    t += f"\n**{eventoz}**"
            except:
                pass
            
            try:

                await app.send_message(message.chat.id,t)
            except:
                pass


def gentop(d, v, tipo):
    if tipo in ["perdenti"]:
        rr = False
    else:
        rr = True
    sort_orders = sorted(d.items(), key=lambda x: x[1], reverse=rr)
    addd = dict()
    for i in sort_orders:
        addd[i[0]] = i[1]
    x = 1
    for tipo in addd:
        if x > 51 or addd[tipo] == 0:
            break
        v += f"{x}° {tipo} - {addd[tipo]} punti!\n"
        x += 1
    return v

@app.on_message(filters.regex(r"^Top 🔝")|filters.command(["top", "top@NFTchallengebot"]) & ~filters.user(bannati) & ~filters.chat(non_qui)
)
async def top(client, message):
    try:
        if len(message.command) == 1:
            v = "Top picchiatori!\n"
            d = dict()
            for tipo in player:
                if (player[tipo]["punti"] == 1000 and tipo not in trader["battaglieri"]):
                    pass
                else:

                    d[tipo] = player[tipo]["punti"]

            await app.send_message(message.chat.id,gentop(d, v, tipo))

        else:
            ricerca = message.command[1]
            tipo = ricerca
            if ricerca == "perdenti":
                v = "Top dei migliori a perdere!\n"
                d = dict()
                for tipo in player:

                    d[tipo] = player[tipo]["punti"]

                await app.send_message(message.chat.id,gentop(d, v, tipo))

            elif ricerca == "livello":
                v = "Top livelli!\n"
                d = dict()
                for tipo in player:

                    d[tipo] = player[tipo]["livello"]
                await app.send_message(message.chat.id,gentop(d, v, tipo))

            elif ricerca == "grado":
                v = "Top grado!\n"
                d = dict()
                for tipo in player:
                    try:
                        d[tipo] = player[tipo]["grado"]
                    except:
                        d[tipo] = 0
                await app.send_message(message.chat.id,gentop(d, v, tipo))
            
            elif ricerca == "domande":
                v = "Top domande!\n"
                d = dict()
                for tipo in player:
                    try:
                        d[tipo] = player[tipo]["domande"]
                    except:
                        d[tipo] = 0
                await app.send_message(message.chat.id,gentop(d, v, tipo))

            
            elif ricerca == "inviti":
                v = "Top invitati!\n"
                d = dict()
                for tipo in player:

                    d[tipo] = player[tipo]["inviti"]["numero"]

                await app.send_message(message.chat.id,gentop(d, v, tipo))

            elif ricerca == "zaino":
                v = "Top zaino differenti!\n"
                d = dict()
                for tipo in player:

                    d[tipo] = len(player[tipo]["zaino"])

                await app.send_message(message.chat.id,gentop(d, v, tipo))

            elif ricerca == "gloria":
                v = "Top gloria!\n"
                d = dict()
                for tipo in player:
                    try:

                        d[tipo] = player[tipo]["gloria"]
                    except:
                        d[tipo] = 0

                await app.send_message(message.chat.id,gentop(d, v, tipo))

            elif ricerca == "win":

                v = "Top vinte!\n"
                d = dict()
                for tipo in player:
                    try:

                        d[tipo] = player[tipo]["w"]
                    except:
                        d[tipo] = 0

                await app.send_message(message.chat.id,gentop(d, v, tipo))

            elif ricerca == "lose":

                v = "Top perse!\n"
                d = dict()
                for tipo in player:
                    try:

                        d[tipo] = player[tipo]["l"]
                    except:
                        d[tipo] = 0

                await app.send_message(message.chat.id,gentop(d, v, tipo))

            elif ricerca == "boss":

                v = "Top vittorie vs Boss!\n"
                d = dict()
                for tipo in player:
                    value = 0
                    if "boss" in player[tipo]:

                        for bossin in player[tipo]["boss"]:
                            value += player[tipo]["boss"][bossin]

                    d[tipo] = value

                await app.send_message(message.chat.id,gentop(d, v, tipo))

            elif ricerca == "clan":

                v = "Top clan!\n"
                d = dict()
                for tipo in clan:

                    try:

                        d[tipo] = clan[tipo]["punti"] + 1
                    except:
                        d[tipo] = 0

                await app.send_message(message.chat.id,gentop(d, v, tipo))

            elif ricerca == "oggi":

                v = "Top sfide oggi!\n"
                d = dict()
                for tipo in player:

                    try:

                        d[tipo] = player[tipo]["oggi"]
                    except:
                        d[tipo] = 0

                await app.send_message(message.chat.id,gentop(d, v, tipo))

            elif ricerca == "sfide":

                v = "Top sfide fatte!\n"
                d = dict()
                for tipo in player:

                    try:

                        d[tipo] = player[tipo]["totali"]
                    except:
                        d[tipo] = 0

                await app.send_message(message.chat.id,gentop(d, v, tipo))

            elif ricerca == "set":

                v = "Top set visti!\n"
                d = dict()
                for tipo in player:

                    try:

                        d[tipo] = len(player[tipo]["setvisti"])
                    except:
                        d[tipo] = 0

                await app.send_message(message.chat.id,gentop(d, v, tipo))

            elif ricerca == "obbiettivi":

                v = "Top obbiettivi!\n"
                d = dict()
                for tipo in player:

                    try:

                        d[tipo] = len(player[tipo]["obbiettivi"])
                    except:
                        d[tipo] = 0

                await app.send_message(message.chat.id,gentop(d, v, tipo))

            else:
                await app.send_message(message.chat.id,
                    "/top accetta solo `livello`,`zaino`,`oggi`,`sfide`,`win`,`lose`,`boss`,`clan`,`inviti`, `perdenti`,`set`,`obbiettivi` o `gloria`"
                )
    except:
        v = "Top picchiatori!\n"
        d = dict()
        for tipo in player:
                if player[tipo]["punti"] == 1000 and tipo not in trader["battaglieri"]:
                    pass
                else:

                    d[tipo] = player[tipo]["punti"]

        await app.send_message(message.chat.id,gentop(d, v, tipo))


@app.on_message(filters.command(["dai", "dai@NFTchallengebot"]) & ~filters.user(bannati))
async def dai(client, message):
    username = message.from_user.username

    if len(message.command) == 1:
        await app.send_message(message.chat.id,"/dai (quantità) nome_oggetto [username]")

    else:
        
        tipo = "None"
        if message.reply_to_message == None:
            tipo = "pvt"
            target = message.command[-1].replace("@", "")
            target = nft.findo(target, list(player))
        else:
            tipo = "pubblico"
            target = message.reply_to_message.from_user.username

        user = player[username]

        if target == username or target == "NFTlittlebot":
            await app.send_message(message.chat.id,f"Scegli un altra persona!")
        else:
            if target in list(player):
                
                if message.command[1].isdigit():
                    if tipo == "pubblico":
                        list_oggetto = nft.listToString(message.command[2:])
                    if tipo == "pvt":
                        list_oggetto = nft.listToString(message.command[2:-1])
                    qt = int(message.command[1])
                    
                else:
                    if tipo == "pubblico":
                        list_oggetto = nft.listToString(message.command[1:])
                    if tipo == "pvt":
                        list_oggetto = nft.listToString(message.command[1:-1])
                    qt = 1
                    
                
                zaino = player[username]["zaino"]
                risultati = nft.search(zaino, list_oggetto)
                if len(risultati) > 1:
                    await app.send_message(message.chat.id,"Sii più preciso!")
                elif len(risultati) == 0:
                    await app.send_message(message.chat.id,
                        "Non ci sono oggetti così chiamati nel tuo zaino!"
                    )
                elif len(risultati) == 1:
                    scheda = user["scheda"]
                    arma = scheda["arma"]
                    prot = scheda["protezione"]
                    anello = scheda["anello"]
                    if ((risultati[0] in liste.bloccati or risultati[0] in liste.decoro or risultati[0] in list(trader["erranti"]) or "MAX" in risultati[0])  and username not in autorizzati) and risultati[0] not in liste.nuclei:
                        await app.send_message(message.chat.id,"Questi item non sono scambiabili!")
                    elif (
                        risultati[0] in [arma, prot, anello]
                        and zaino[risultati[0]] == 1
                    ):
                        await app.send_message(message.chat.id,"Devi prima posarlo!")
                    else:
                        
                        t = 0
                        if int(qt) > 0:
                            for x in range(int(qt)):
                                if risultati[0] in zaino:
                                    nft.gestione_zaino(zaino,"rem",risultati[0],1)
                                    ricevente = player[target]["zaino"]
                                    nft.gestione_zaino(ricevente,"add",risultati[0],1)
                                    t += 1
                                else:
                                    await app.send_message(message.chat.id,"Dati tutti!")
                                    break

                            await app.send_message(message.chat.id,
                                f"{username} dà {t} {risultati[0]} a {target}!"
                            )
                            try:
                                await app.send_message(
                                    target, f"{username} ti dà {t} {risultati[0]}!"
                                )
                            except:
                                pass
                            try:
                                await cestino.send_message(
                                    -1001522938963,
                                    f"{username} dà {t} {risultati[0]} a {target}!",
                                )
                            except:
                                pass

            else:
                await app.send_message(message.chat.id,"Questo utente non gioca!")


duelli = {}
from pykeyboard import InlineKeyboard

@app.on_message( ~filters.user(bannati) & filters.command(["duello"]))
async def duello(client, message):
    if message.reply_to_message == None:
                    to = message.command[1].replace("@", "")
                    for x in list(player):
                        if to.lower() == x.lower():
                            username = x
                            break
    else:
                    username = message.reply_to_message.from_user.username
    
    dgx = player[username].get("duello", None)
    dgp= player[message.from_user.username].get("duello", None)
    
   
    if (dgx == None or dgx not in duelli):
        if (dgp == None or dgp not in duelli):
            keyboardAttacco = InlineKeyboard()
            keyboardAttacco.row(InlineKeyboardButton('Attacca', 'pvp_attacco'))
            re = time.time()
            player[username]["duello"] = f"{re}_p"
            player[message.from_user.username]["duello"] = f"{re}_p"
            

            keyboardDifesa = InlineKeyboard()
            keyboardDifesa.row(InlineKeyboardButton('Stordisci', 'pvp_tempo'))
            h = await app.send_message(message.from_user.username,f"Inizia il duello contro {username}",reply_markup=keyboardAttacco)
            k = await app.send_message(username,f"Inizia il duello contro {message.from_user.username}",reply_markup=keyboardDifesa)
            duelli[f"{re}_p"] = {"a":message.from_user.username,"b":username,"adanno":0,"bdanno":0,"tempo":time.time(),"amess":h.message_id,"bmess":k.message_id,
                                "afatto":0,"bfatto":0,
                                "abonus":{'def': 0, 'atk': 0, 'agi': 0},
                                "bbonus":{'def': 0, 'atk': 0, 'agi': 0},
                                "aaltro":{},"baltro":{}}
            
            await message.reply("Ok,andato")
        else:
          await message.reply("Sei tu in un duello!")  
    else:
        await message.reply("Lo sfidato è in un duello!")
    
    
@app.on_message( ~filters.user(bannati) & filters.regex(r"^Me 👤")| filters.command(["me", "me@NFTchallengebot"]))
async def me(client, message):
    try:
        if len(message.command) == 1 and message.reply_to_message == None:

            username = message.from_user.username
            zaino = len(player[username]["zaino"])
            scheda = player[username]["scheda"]
            punti = player[username]["punti"]
            w = player[username]["w"]
            l = player[username]["l"]
            a = scheda["atk"]
            aa = scheda["def"]
            aaa = scheda["agi"]
            aaaa = scheda["hp"]
            arma = scheda["arma"]
            prot = scheda["protezione"]
            anello = scheda["anello"]
            team = player[username]["team"]
            lv = player[username]["livello"]
            expd = player[username]["exp"]
            now = expd["expattuale"]
            next = expd["nextlv"]
            lv = player[username]["livello"]
            expd = player[username]["exp"]
            niw = expd["expattuale"]
            next = expd["nextlv"]
            topP = player[username]["topP"]
            classe = player[username]["scheda"]["set"]
            da = player[username]["inviti"]["dachi"]
            quanti = player[username]["inviti"]["numero"]
            straknumero = player[username]["streak"]
            oggi = player[username]["oggi"]
            totali = player[username]["totali"]
            visti = len(player[username]["setvisti"])
            location = player[username]["location"]
            moje = liste.moji_posto[location]
            try:
                grado = player[username]["grado"]
            except:
                grado = 0
            if "NomePet" in player[username]:
                nome = player[username]["NomePet"] + ","
            else:
                nome = ""
            if username in inabilitati:
                now = time.time()
                other_time = inabilitati[username]
                if other_time == "Una copia dell'arte della guerra autografata":
                    stato = "Stordito dall'arte della guerra"
                else:
                    minimo = 900
                    if evento["mod"] == "flexville":
                        minimo - 450
                    if player[username]["team"] != "nessuno":
                        if "Chiesa" in clan[player[username]["team"]]["villaggio"]:
                            minimo -= 5 * int(clan[player[username]["team"]]["villaggio"]["Chiesa"]["lv"])
                    if player[username]["setta"]["benedizione"] == 'Non morto':
                        a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
                        minimo -= a   
                    oldtime = inabilitati[username]
                    
                    direi = time.time() - oldtime 
                    
                    ty_res = time.gmtime(minimo - direi)
                    tempo = time.strftime("%H:%M:%S", ty_res)
                    stato = f"Manca ancora {tempo} minuti prima che si riprenda!"
            else:
                stato = ""
            if da == None:
                da = "nessuno!"
            try:
                pet = player[username]["pet"]
                pet = f"Insieme a {nome} {pet.lower()}"
            except:
                pet = ""
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
            ass = scheda["int"]
            fs_w = 1
            scheda = player[username]["scheda"]
            if lv > 1:
                try:
                    arma = scheda["arma"]
                    protezione = scheda["protezione"]
                    listina = arma.split(" LV")
                    coso = listina[0]
                    listina2 = protezione.split(" LV")
                    ricercato = listina2[0]
                    if coso in item_pescatore:
                        fs_w += 1
                    if ricercato in item_pescatore:
                        fs_w += 1
                    if scheda["set"] == "Pescatore":
                        fs_w += 1
                    if scheda["set"] == "Pescatore di balene":
                        fs_w += 2
                    
                except:
                    pass
                if trader["meteo"][player[username]["location"]] == "Pioggia":
                    fs_w += 1
                if trader["meteo"][player[username]["location"]] == "Tempesta":
                    fs_w += 2
                if trader["meteo"][player[username]["location"]] == "Caldo torrido":
                    fs_w -= 1
                if trader["meteo"][player[username]["location"]] == "Caldo infernale":
                    fs_w -= 2
            
            f = nft.get_ench(player[username])
            if f != []:
                enchi = "Incantamenti:\n    "
                for xqwe in f:
                    enchi += f"{xqwe} "
                enchi += "\n"
            else:
                enchi = ""
            if lv == 0:
                mj = "📖"
            if lv > 0:
                mj = "👤"
            if lv > 5:
                mj = "🎈"
            if lv > 8:
                mj = "🧠"
            if lv > 10:
                mj = "⭐️"
            if lv > 15:
                mj = "✨"
            if lv > 25:
                mj = "☀️"

            if username in trader["preferenziale"]:
                spezio = "🍥 " + str(trader["preferenziale"].count(username))
            else:
                spezio = ""
            text = f"""{username}
    {mj}{lv} lv.({niw}/{next})
    ⚔️ Punti battaglia: {punti} {spezio}
    🎖 {classe}
    👥 {team}
    🛡 {topP} ({grado})
    🌍 {location} {moje}
    {pet}


    ❤️ Vitalità: {aaaa}
    🪓 Attacco: {a}
    🥋 Difesa: {aa}
    🌪️ Agilità: {aaa}
    🧠 Intelligenza : {ass}

    Arma: {arma}
    {armaa}/{armad}/{armag}
    Protezione: {prot}
    {armaas}/{armads}/{armags}
    Anello: {anello}
    {enchi}
    ({w} w/{l} l)
    Sfide totali: {totali} ({oggi})
    Set usati : {visti}
    Invitato da {da}
    Invitati: {quanti}
    Potere di pesca: {fs_w}
    __Sfida da ben {straknumero} giorni!__
    {stato}"""

            try:
                await app.send_message(message.chat.id,text)
            except:
                pass

        else:

            try:
                if message.reply_to_message == None:
                    to = message.command[1].replace("@", "")
                    for x in list(player):
                        if to.lower() == x.lower():
                            username = x
                            break
                else:
                    username = message.reply_to_message.from_user.username

                scheda = player[username]["scheda"]
                punti = player[username]["punti"]
                w = player[username]["w"]
                l = player[username]["l"]
                a = scheda["atk"]
                topP = player[username]["topP"]
                aa = scheda["def"]
                aaa = scheda["agi"]
                aaaa = scheda["hp"]
                arma = scheda["arma"]
                prot = scheda["protezione"]
                anello = scheda["anello"]
                team = player[username]["team"]
                lv = player[username]["livello"]
                expd = player[username]["exp"]
                now = expd["expattuale"]
                next = expd["nextlv"]
                lv = player[username]["livello"]
                expd = player[username]["exp"]
                now = expd["expattuale"]
                next = expd["nextlv"]
                if (
                    player[message.from_user.username]["notifiche"]["privacy"] == "no"
                    and player[username]["notifiche"]["privacy"] == "no"
                ):
                    dati = True
                else:
                    dati = False
                if player[message.from_user.username]["team"] == player[username]["team"]:
                    dati = True
                
                classe = player[username]["scheda"]["set"]

                if dati == True or message.from_user.username == "ElSalamino":
                    
                    scheda = f"""Arma: `{arma}`
    Protezione: `{prot}`
    Anello: `{anello}`
    """
                else:
                    scheda = "__Uno dei 2 giocatori ha scelto di nascondere la scheda!__\n"

                da = player[username]["inviti"]["dachi"]
                straknumero = player[username]["streak"]
                oggi = player[username]["oggi"]
                try:
                    grado = player[username]["grado"]
                except:
                    grado = 0
                totali = player[username]["totali"]
                if "NomePet" in player[username]:
                    nome = player[username]["NomePet"] + ","
                else:
                    nome = ""
                try:
                    pet = player[username]["pet"]
                    pet = f"Insieme a {nome} {pet}"
                except:
                    pet = ""
                if da == None:
                    da = "nessuno!"
                quanti = player[username]["inviti"]["numero"]
                if lv == 0:
                    mj = "📖"
                if lv > 0:
                    mj = "👤"
                if lv > 5:
                    mj = "🎈"
                if lv > 8:
                    mj = "🧠"
                if lv > 10:
                    mj = "⭐️"
                if lv > 15:
                    mj = "✨"
                if lv > 25:
                    mj = "☀️"
                if username in bannati:
                    mj = "🚷"
                location = player[username]["location"]
                if username in trader["preferenziale"]:
                    spezio = "🍥 " + str(trader["preferenziale"].count(username))
                else:
                    spezio = ""
                text = f"""{username}
    {mj}{lv} lv.({now}/{next})
    ⚔️ Punti battaglia: {punti} {spezio}
    🎖 {classe}
    👥 {team}
    🛡 {topP} ({grado})
    🌍 {location}
    {pet}

    ❤️ Vitalità: {aaaa}
    🪓 Attacco: {a}
    🥋 Difesa: {aa}
    🌪️ Agilità: {aaa}

    {scheda}
    ({w} w/{l} l)
    Sfide totali: {totali} ({oggi})
    Invitato da {da}
    __Sfida da ben {straknumero} giorni!__
    Invitati {quanti}"""

                chunk = 4096
                for t in (text[i : i + chunk] for i in range(0, len(text), chunk)):
                    await app.send_message(message.chat.id,t)
            except Exception as err:
                print(err)
                await app.send_message(message.chat.id,"Utente non trovato!")
    except:
        if 1 == 1:
            username = message.from_user.username
            zaino = len(player[username]["zaino"])
            scheda = player[username]["scheda"]
            punti = player[username]["punti"]
            w = player[username]["w"]
            l = player[username]["l"]
            a = scheda["atk"]
            aa = scheda["def"]
            aaa = scheda["agi"]
            aaaa = scheda["hp"]
            arma = scheda["arma"]
            prot = scheda["protezione"]
            anello = scheda["anello"]
            team = player[username]["team"]
            lv = player[username]["livello"]
            expd = player[username]["exp"]
            now = expd["expattuale"]
            next = expd["nextlv"]
            lv = player[username]["livello"]
            expd = player[username]["exp"]
            niw = expd["expattuale"]
            next = expd["nextlv"]
            topP = player[username]["topP"]
            classe = player[username]["scheda"]["set"]
            da = player[username]["inviti"]["dachi"]
            quanti = player[username]["inviti"]["numero"]
            straknumero = player[username]["streak"]
            oggi = player[username]["oggi"]
            totali = player[username]["totali"]
            visti = len(player[username]["setvisti"])
            location = player[username]["location"]
            moje = liste.moji_posto[location]
            try:
                grado = player[username]["grado"]
            except:
                grado = 0
            if "NomePet" in player[username]:
                nome = player[username]["NomePet"] + ","
            else:
                nome = ""
            if username in inabilitati:
                now = time.time()
                other_time = inabilitati[username]
                if other_time == "Una copia dell'arte della guerra autografata":
                    stato = "Stordito dall'arte della guerra"
                else:
                    minimo = 900
                    if evento["mod"] == "flexville":
                        minimo - 450
                    if player[username]["team"] != "nessuno":
                        if "Chiesa" in clan[player[username]["team"]]["villaggio"]:
                            minimo -= 5 * int(clan[player[username]["team"]]["villaggio"]["Chiesa"]["lv"])
                    if player[username]["setta"]["benedizione"] == 'Non morto':
                        a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
                        minimo -= a   
                    oldtime = inabilitati[username]
                    
                    direi = time.time() - oldtime 
                    
                    ty_res = time.gmtime(minimo - direi)
                    tempo = time.strftime("%H:%M:%S", ty_res)
                    stato = f"Manca ancora {tempo} minuti prima che si riprenda!"
            else:
                stato = ""
            if da == None:
                da = "nessuno!"
            try:
                pet = player[username]["pet"]
                pet = f"Insieme a {nome} {pet.lower()}"
            except:
                pet = ""
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
            ass = scheda["int"]
            fs_w = 1
            scheda = player[username]["scheda"]
            if lv > 1:
                try:
                    arma = scheda["arma"]
                    protezione = scheda["protezione"]
                    listina = arma.split(" LV")
                    coso = listina[0]
                    listina2 = protezione.split(" LV")
                    ricercato = listina2[0]
                    if coso in item_pescatore:
                        fs_w += 1
                    if ricercato in item_pescatore:
                        fs_w += 1
                    if scheda["set"] == "Pescatore":
                        fs_w += 1
                    if scheda["set"] == "Pescatore di balene":
                        fs_w += 2
                    
                except:
                    pass
                if trader["meteo"][player[username]["location"]] == "Pioggia":
                    fs_w += 1
                if trader["meteo"][player[username]["location"]] == "Tempesta":
                    fs_w += 2
                if trader["meteo"][player[username]["location"]] == "Caldo torrido":
                    fs_w -= 1
                if trader["meteo"][player[username]["location"]] == "Caldo infernale":
                    fs_w -= 2
            
            f = nft.get_ench(player[username])
            if username in trader["preferenziale"]:
                spezio = "🍥 " + str(trader["preferenziale"].count(username))
            else:
                spezio = ""
            if f != []:
                enchi = "Incantamenti:\n"
                for xqwe in f:
                    enchi += f"{xqwe} "
                enchi += "\n"
            else:
                enchi = ""
            if lv == 0:
                mj = "📖"
            if lv > 0:
                mj = "👤"
            if lv > 5:
                mj = "🎈"
            if lv > 8:
                mj = "🧠"
            if lv > 10:
                mj = "⭐️"
            if lv > 15:
                mj = "✨"
            if lv > 25:
                mj = "☀️"

            text = f"""{username}
    {mj}{lv} lv.({niw}/{next})
    ⚔️ Punti battaglia: {punti} {spezio}
    🎖 {classe}
    👥 {team}
    🛡 {topP} ({grado})
    🌍 {location} {moje}
    {pet}


    ❤️ Vitalità: {aaaa}
    🪓 Attacco: {a}
    🥋 Difesa: {aa}
    🌪️ Agilità: {aaa}
    🧠 Intelligenza : {ass}

    Arma: {arma}
    {armaa}/{armad}/{armag}
    Protezione: {prot}
    {armaas}/{armads}/{armags}
    Anello: {anello}
    {enchi}
    ({w} w/{l} l)
    Sfide totali: {totali} ({oggi})
    Set usati : {visti}
    Invitato da {da}
    Invitati: {quanti}
    Potere di pesca: {fs_w}
    __Sfida da ben {straknumero} giorni!__
    {stato}"""

            try:
                await app.send_message(message.chat.id,text)
            except:
                pass

pescaTORI = list()
@sched.scheduled_job("interval",seconds=10)
def sfide_brain():
    to = list()
    try:
        for sfida in strader["sfide"]:
            now = time.time()
            sfidha = strader["sfide"][sfida]
                
            elapsed = now - sfidha["ora"]
            if elapsed >= sfidha["tempo"]:
            
                username = sfidha["a"]
                to.append(sfida)
                nome1 = username
                player[username]["preso"] = False
                nome2 = sfidha["b"]
                sfidante = sfidha["b"]
                g = sfidha["a_mess"]
                sesso = sfidha["b_mess"]
                user1 = copy.deepcopy(player[username]["scheda"])
                user2 = copy.deepcopy(player[sfidante]["scheda"])
                if  player[username]["setta"]["benedizione"] == "Troll del labirinto":
                    a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
                    try:
                        user1["int"] += a
                    except:
                        user1["int"] = a
                
                if  player[sfidante]["setta"]["benedizione"] == "Troll del labirinto":
                    a = round(trader["sette"][player[sfidante]["setta"]["loc"]]["power"] * (trader["sette"][player[sfidante]["setta"]["loc"]]["%"]/100))
                    try:
                        user2["int"] += a
                    except:
                        user2["int"] = a
                if "Approcci" not in player[username]:
                            player[username]["Approcci"] = dict()
                if "Approcci" not in player[sfidante]:
                            player[sfidante]["Approcci"] = dict()
                        
                if sfidante in player[username]["Approcci"]:
                    user1["Ap"] = player[username]["Approcci"][sfidante]
                            
                    if user1["Ap"] in liste.Approccini[player[username]["scheda"]["set"]] or user1["Ap"] == "Base":
                                pass
                    else:
                        user1["Ap"] = "Base"
                    try:
                        player[username]["Approcci"].pop(sfidante)
                    except:
                        pass
                if username in player[sfidante]["Approcci"]:
                    user2["Ap"] = player[sfidante]["Approcci"][username]
                    if user2["Ap"] in liste.Approccini[player[sfidante]["scheda"]["set"]] or user2["Ap"] == "Base":
                                pass
                    else:
                                user2["Ap"] = "Base"
                    try:
                                player[sfidante]["Approcci"].pop(username)
                    except:
                                pass
                if sfidante in list(inabilitati):
                    player[username]["preso"] = False
                    try:
                        sesso.edit("Vorrei farti sfidare ma aimè sei morto!")
                    except:
                        pass
                    try:
                        g.edit("Probabilmente è successo qualcosa al tuo avversario...")
                    except:
                        
                                pass
                elif username in list(inabilitati):
                    player[username]["preso"] = False
                    try:
                        g.edit("Vorrei farti sfidare ma aimè sei morto!")
                    except:
                        pass
                    try:
                        sesso.edit(
                                    "Probabilmente è successo qualcosa al tuo avversario..."
                                )
                    except:
                        pass
                else:
                    liste.approccio1 = user1["Ap"]
                    liste.approccio2 = user2["Ap"]
                    eventzo =  trader["Giovedì"]
                    text = f"Sfida tra {nome1} e {nome2}!\n{nome1} sceglie: {liste.approccio1}, mentre {nome2} su {liste.approccio2}!\n\n"
                   
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
                                user1["Scudo"] = 800

                    if user2["set"] == "Paladino":
                                user2["Scudo"] = 800
                    if user1["set"] == "Serial killer":
                                user2["hp"] = round(user2["hp"] * 0.75)
                    if user2["set"] == "Serial killer":
                                user1["hp"] = round(user1["hp"] * 0.75)
                    
                    nft.boost(user1,liste.Approcci)
                    nft.boost(user2,liste.Approcci)

                    user1["incantamenti"] = nft.get_ench(player[username])
                    user2["incantamenti"] = nft.get_ench(player[sfidante])  

                    user1["fatto"] = 0
                    user2["fatto"] = 0
                    nft.classe(user1, user1["set"],liste.bonus)
                    nft.classe(user2, user2["set"],liste.bonus)
                    if user1["anello"] == "Pegno di amicizia":
                                text += f"\nPartendo dal presupposto che {nome1} è un grande amico di {nome2}...\n"
                    if user2["anello"] == "Pegno di amicizia":
                                text += f"\nConsiderando che {nome2} è un grande amico di {nome1}...\n"
                    if user1["anello"] == "Fascette luminose":
                                text += f"\nEntra sul ring {nome1}!\n\n"
                    if user2["anello"] == "Fascette luminose":
                                text += f"\nE si presenta a noi {nome2}!\n\n"
                    if 0.2 > random.random() and "pet" in player[username]:
                                if "NomePet" in player[username]:
                                    nome = player[username]["NomePet"] + ", "
                                else:
                                    nome = ""
                                pet = player[username]["pet"]
                                text += f"\n{nome}{pet} fa il tifo per {nome1}!\n\n"
                                user1["hp"] += 1

                    if 0.2 > random.random() and "pet" in player[sfidante]:
                                if "NomePet" in player[sfidante]:
                                    nome = player[sfidante]["NomePet"] + ", "
                                else:
                                    nome = ""
                                pet = player[sfidante]["pet"]
                                text += f"\n{nome}{pet} fa il tifo per {nome2}!\n\n"
                                user2["hp"] += 1
                    rip = 0
                    while True:
                        rip += 1
                        text += nft.turno(user2, user1,eventzo)
                        if nft.is_dead(user1):
                                    b = player[username]
                                    a = player[sfidante]
                                    premio_exp(
                                        player[sfidante], player[username], text
                                    )
                                    break
                        if nft.is_dead(user2):
                                    a = player[username]
                                    b = player[sfidante]
                                    premio_exp(
                                        player[username], player[sfidante], text
                                    )
                                    break
                        text += nft.turno(user1, user2,eventzo)
                        if nft.is_dead(user2):
                                    a = player[username]
                                    b = player[sfidante]
                                    premio_exp(
                                        player[username], player[sfidante], text
                                    )
                                    break
                        if nft.is_dead(user1):
                                    b = player[username]
                                    a = player[sfidante]
                                    premio_exp(
                                        player[sfidante], player[username], text
                                    )
                                    break
                        if rip == 150:
                                    text += f"\nLa battaglia ha stremato {nome1}, che cade a terra sfinito!\n"
                                    b = player[username]
                                    a = player[sfidante]
                                    premio_exp(
                                        player[sfidante], player[username], text
                                    )
                                    break
                    if b["scheda"]["Nome"] == user1["Nome"]:
        
                                nomeperdente = user1["Nome"]
                                proccioperd = user1["Ap"]
                                vitarima = user2["hp"]
                                liste.approcciovin = user2["Ap"]
                                nomevincitore = user2["Nome"]
                                vitapp = user1["hp"]

                    else:
                                nomeperdente = user2["Nome"]
                                proccioperd = user2["Ap"]
                                vitapp = user2["hp"]
                                vitarima = user1["hp"]
                                nomevincitore = user1["Nome"]
                                liste.approcciovin = user1["Ap"]
                    if 1 == 1:
                        
                        if "Precisino" not in a["obbiettivi"] and vitapp == 0:
                                a["obbiettivi"].append("Precisino")

                                try:
                                    app.send_message(
                                        a["scheda"]["Nome"],
                                        "Obbiettivo completato!\n**Precisino**, il tuo avversario è morto giusto giusto!",
                                    )
                                except:
                                    pass

                        if "Tutta fortuna" not in a["obbiettivi"] and vitarima == 1:
                                a["obbiettivi"].append("Tutta fortuna")
                                try:
                                    app.send_message(
                                        a["scheda"]["Nome"],
                                        "Obbiettivo completato!\n**Tutta fortuna**, dillo che è stato grazie al tipo del famiglio!",
                                    )
                                except:
                                    pass

                        if "Titanico" not in a["obbiettivi"] and vitarima >= 4000:
                                a["obbiettivi"].append("Titanico")
                                try:
                                    app.send_message(
                                        a["scheda"]["Nome"],
                                        "Obbiettivo completato!\n**Titanico**, sei stato il giocatore con più hp di sicuro!",
                                    )
                                except:
                                    pass
                        
                        if 1 == 1:
                            
                            puntia = b["punti"]

                            puntib = a["punti"]

                            mod = ((puntib - puntia) / 22) * -1
                            furto = round(8 * (mod / 8))
                            if furto == 0:
                                furto = 12
                            if furto < 8:
                                furto = 8
                            
                            if player[a["scheda"]["Nome"]]["setta"]["benedizione"] == "Alligatore":
                                
                                aff = round(trader["sette"][player[a["scheda"]["Nome"]]["setta"]["loc"]]["power"] * (trader["sette"][player[a["scheda"]["Nome"]]["setta"]["loc"]]["%"]/100))
                                furto += aff
                            
                            punti = furto
                            if evento["mod"] == "punti_extra":
                                furto += 5
                            
                            if "set" in a["scheda"]:
                                if a["scheda"]["anello"] == "Anello d'oro fortissimo":
                                    punti += 2
                                if a["scheda"]["set"] == "Pilota":
                                    punti += 2
                            if "set" in b["scheda"]:
                                if b["scheda"]["anello"] == "Anello d'oro fortissimo":
                                    punti -= 2
                                if b["scheda"]["set"] == "Lupo di mare":
                                    punti -= 2

                            b["punti"] -= punti
                            if b["punti"] < 0:
                                b["punti"] = 0
                                punti = 0
                            a["punti"] += punti
                            a["w"] += 1

                            b["l"] += 1
                            try:
                                b["l-streak"] += 1
                            except:
                                b["l-streak"] = 1

                            if ("Caduta con stile" not in b["obbiettivi"] and b["l-streak"] == 15):
                                b["obbiettivi"].append("Caduta con stile")
                                try:
                                    app.send_message(
                                        b["scheda"]["Nome"],
                                        "Obbiettivo completato!\n**Caduta con stile**, sei bravissimo a vincere, talmente tanto da sapere come perderle tutte!",
                                    )
                                except:
                                    pass
                            if ("Caduta con stile" not in a["obbiettivi"] and a["l-streak"] == 15):
                                a["obbiettivi"].append("Caduta con stile")

                                try:
                                    app.send_message(
                                        a["scheda"]["Nome"],
                                        "Obbiettivo completato!\n**Caduta con stile**, sei bravissimo a vincere, talmente tanto da sapere come perderle tutte!",
                                    )
                                except:
                                    pass

                            if (
                                "Danneggiatore" not in player[user1["Nome"]]["obbiettivi"]
                                and user1["fatto"] >= 5555
                            ):
                                player[user1["Nome"]]["obbiettivi"].append("Danneggiatore")
                                try:
                                    app.send_message(
                                        user2["Nome"],
                                        "Obbiettivo completato!\n**Danneggiatore**, sei il miglior danneggiatore dell'isolato!",
                                    )
                                except:
                                    pass

                            if (
                                "Danneggiatore" not in player[user2["Nome"]]["obbiettivi"]
                                and user2["fatto"] >= 5555
                            ):
                                player[user2["Nome"]]["obbiettivi"].append("Danneggiatore")
                                try:
                                    app.send_message(
                                        user2["Nome"],
                                        "Obbiettivo completato!\n**Danneggiatore**, sei il miglior danneggiatore dell'isolato!",
                                    )
                                except:
                                    pass

                            if (
                                "Schiappetta" not in player[user1["Nome"]]["obbiettivi"]
                                and user1["fatto"] <= 100
                            ):
                                player[user1["Nome"]]["obbiettivi"].append("Schiappetta")
                                try:
                                    app.send_message(
                                        user1["Nome"],
                                        "Obbiettivo completato!\n**Schiappetta**, non hai fatto molto ma è stata una sfida onesta!",
                                    )
                                except:
                                    pass

                            if (
                                "Schiappetta" not in player[user2["Nome"]]["obbiettivi"]
                                and user2["fatto"] <= 100
                            ):
                                player[user2["Nome"]]["obbiettivi"].append("Schiappetta")
                                try:
                                    app.send_message(
                                        user2["Nome"],
                                        "Obbiettivo completato!\n**Schiappetta**, non hai fatto molto ma è stata una sfida onesta!",
                                    )
                                except:
                                    pass

                            a["l-streak"] = 0

                            nome1 = a["scheda"]["Nome"]
                            nome2 = b["scheda"]["Nome"]
                            
                            text += f"\nIl vincitore è quindi {nomevincitore}, che batte {nomeperdente}.\nAvviene inoltre un furto di ben {punti} punti!"
                            nuovo = f"Vince {nome1}({liste.approcciovin})  in {rip} turni, battendo così {nome2} ({proccioperd}), dato che resta con {vitarima} hp.\nAvviene un furto di {punti} punti!"

                            player[username]["preso"] = False

                            nft.controllo_effetti_sfida(username,player)
                            nft.controllo_effetti_sfida(sfidante,player)
                            player[username]["oggi"] += 1
                            player[username]["totali"] += 1
                            player[sfidante]["oggi"] += 1
                            player[sfidante]["totali"] += 1

                            if (
                                "Iperattivo" not in player[username]["obbiettivi"]
                                and player[username]["oggi"] == 2500
                            ):
                                player[username]["obbiettivi"].append("Iperattivo")
                                app.send_message(username,
                                    "Obbiettivo completato!\n**Iperattivo**, non sarebbe ora di fare una pausa?"
                                )
                            if (
                                "Iperattivo" not in player[sfidante]["obbiettivi"]
                                and player[sfidante]["oggi"] == 2500
                            ):
                                player[sfidante]["obbiettivi"].append("Iperattivo")
                                try:

                                    app.send_message(
                                        sfidante,
                                        "Obbiettivo completato!\n**Iperattivo**, non sarebbe ora di fare una pausa?",
                                    )
                                except:
                                    pass

                            if (
                                "Prima sfida" not in player[username]["obbiettivi"]
                                and player[username]["totali"] >= 1
                            ):
                                player[username]["obbiettivi"].append("Prima sfida")
                                try:
                                    app.send_message(username,
                                    "Obbiettivo completato!\n**Prima sfida**, bravissimo continua così!"
                                )
                                except:
                                    pass
                            if (
                                "Prima sfida" not in player[sfidante]["obbiettivi"]
                                and player[sfidante]["totali"] >= 1
                            ):
                                player[sfidante]["obbiettivi"].append("Prima sfida")
                                try:

                                    app.send_message(
                                        sfidante,
                                        "Obbiettivo completato!\n**Prima sfida**, bravissimo continua così!",
                                    )
                                except:
                                    pass

                            if (
                                "Sfidante tosto" not in player[username]["obbiettivi"]
                                and player[username]["totali"] >= 4500
                            ):
                                player[username]["obbiettivi"].append("Sfidante tosto")
                                app.send_message(username,
                                    "Obbiettivo completato!\n**Sfidante tosto**, sei un ottimo sfidante, ma quanto puoi andare avanti?"
                                )
                            if (
                                "Sfidante tosto" not in player[sfidante]["obbiettivi"]
                                and player[sfidante]["totali"] >= 4500
                            ):
                                player[sfidante]["obbiettivi"].append("Sfidante tosto")
                                try:

                                    app.send_message(
                                        sfidante,
                                        "Obbiettivo completato!\n**Sfidante tosto**, sei un ottimo sfidante, ma quanto puoi andare avanti?",
                                    )
                                except:
                                    pass
                            if (
                                "Campione di sfida" not in player[username]["obbiettivi"]
                                and player[username]["totali"] >= 8000
                            ):
                                player[username]["obbiettivi"].append("Campione di sfida")
                                app.send_message(username,
                                    "Obbiettivo completato!\n**Campione di sfida**, ormai sei un esperto, continua così!"
                                )
                            if (
                                "Campione di sfida" not in player[sfidante]["obbiettivi"]
                                and player[sfidante]["totali"] >= 8000
                            ):
                                player[sfidante]["obbiettivi"].append("Campione di sfida")
                                try:
                                    app.send_message(
                                        sfidante,
                                        "Obbiettivo completato!\n**Campione di sfida**, ormai sei un esperto, continua così!",
                                    )
                                except:
                                    pass

                            if (
                                "SUPER SFIDANTE" not in player[username]["obbiettivi"]
                                and player[username]["totali"] >= 12500
                            ):
                                player[username]["obbiettivi"].append("SUPER SFIDANTE")
                                app.send_message(username,
                                    "Obbiettivo completato!\n**SUPER SFIDANTE**, wooooooooooooooooooooooooooooooooooooooooooooooo"
                                )
                            if (
                                "SUPER SFIDANTE" not in player[sfidante]["obbiettivi"]
                                and player[sfidante]["totali"] >= 12500
                            ):
                                player[sfidante]["obbiettivi"].append("SUPER SFIDANTE")
                                try:
                                    app.send_message(
                                        sfidante,
                                        "Obbiettivo completato!\n**SUPER SFIDANTE**, wooooooooooooooooooooooooooooooooooooooooooooooo",
                                    )
                                except:
                                    pass


                            if player[username]["notifiche"]["compatte"] == "no":
                                try:
                                    g.edit(text)
                                except:
                                    g.delete()

                                    chunk = nft.separatore(text)
                                    for t in chunk:
                                        try:
                                            app.send_message(username,t)
                                        except:
                                            pass
                            else:
                                try:
                                    g.edit(nuovo)
                                except:
                                    pass

                            try:
                                if player[sfidante]["notifiche"]["compatte"] == "no":
                                    try:
                                        sesso.edit(text)
                                    except:
                                        sesso.delete()
                                        chunk = nft.separatore(text)
                                        for t in chunk:
                                            app.send_message(sfidante, t)
                                else:
                                    sesso.edit(nuovo)
                            except:
                                pass
                            player[username]["aigettoni"]["sfide"] += 1
                            if player[username]["aigettoni"]["sfide"] >= 100:
                                try:
                                    player[username]["zaino"]["Gettone arena"] += 1
                                except:
                                    player[username]["zaino"]["Gettone arena"] = 1
                                    
                                player[username]["aigettoni"]["sfide"] = 0
                                app.send_message(username,"Vinci inoltre un gettone arena!")
                            player[sfidante]["aigettoni"]["sfide"] += 1
                            if player[sfidante]["aigettoni"]["sfide"] >= 100:
                                try:
                                    player[sfidante]["zaino"]["Gettone arena"] += 1
                                except:
                                    player[sfidante]["zaino"]["Gettone arena"] = 1
                                    
                                player[sfidante]["aigettoni"]["sfide"] = 0
                                app.send_message(sfidante,"Vinci inoltre un gettone arena!")
    except RuntimeError:
        pass   
    
    for t in to:
        try:
            strader["sfide"].pop(t)                  
        except:
            pass                  



@app.on_message(filters.command(["usa"]) & ~filters.user(bannati) & ~filters.chat(non_qui)
)
async def usa(client, message):
    username = message.from_user.username
    if len(message.command) == 1:
        text = "/usa nomeoggetto\nPer usi multipli: /usa cosa : quanto\nPer erranti: /usa cosa , chi\n\nPuoi usare @a per usare tutto o @r per usarne a caso da 1 a 10\n\n"
        for figura in player[username]["zaino"]:
            if figura in liste.usabili:
                qt = player[username]["zaino"][figura]
                text += f"\n - `{figura}` x {qt} 👝"
                text += nft.correggiemoji(figura, emojiz,item_boss,item_pescatore)
        await app.send_message(message.chat.id,
            text
        )
    else:

        
        zaino = player[username]["zaino"]
        tipo = None
        argomento = nft.listToString(message.command[1:])

        if "," in argomento:
            tipo = "errante"
        elif ":" in argomento:
            tipo = "multiplo"
        else:
            tipo = "liste.classico"

        if tipo == None:
            await app.send_message(message.chat.id,"Errore!\nContatta @ElSalamino dando come codice errore 709!")
        else:

            if tipo == "errante":
                argomento = argomento.replace(","," ")
                chi = argomento.split(" ")[-1].replace(" ", "").replace("@","")
                cosa = nft.listToString(argomento.split(" ")[0:-1])
                chi = nft.findo(chi, list(player))
                
            if tipo == "multiplo":
                argomento = argomento.replace(":"," ")
                quanto = argomento.split(" ")[-1]
                cosa = nft.listToString(argomento.split(" ")[0:-1])
                
                
                if int(quanto) < 1:
                    quanto = 1
            if tipo == "liste.classico":
                cosa = argomento

            if cosa in zaino:
                risultati = [cosa]
            else:
                risultati = nft.search(zaino, cosa)
            if len(risultati) == 0:
                risultati = nft.search(player[username]["pozioni"], cosa)
            if len(list(risultati)) > 1:
                await app.send_message(message.chat.id,"Sii più preciso!")
            elif len(list(risultati)) == 0:
                await app.send_message(message.chat.id,"Non ci sono oggetti così chiamati nel tuo zaino!")
            elif len(list(risultati)) == 1:
                if risultati[0] in liste.usabili or risultati[0] in pozioni:
                    ricercato = risultati[0]

                    if tipo == "liste.classico" or tipo == "multiplo":
                        if ricercato == "Un idoletto":
                            if player[username]["team"] != "nessuno":
                                rep = 1
                                if tipo == "multiplo":
                                    rep = int(quanto)
                                    if rep >= 10:
                                        rep = 10

                                for x in range(rep):

                                    if ricercato in zaino:
                                        nft.gestione_zaino(zaino,"rem",ricercato,1)
                                        clan[player[username]["team"]]["potere"] += 4
                                        clan[player[username]["team"]]["punti"] += 4
                                    else:
                                        x -= 1
                                        await app.send_message(message.chat.id,"Sono finiti prima!")
                                        break
                                await app.send_message(message.chat.id,
                                    f"Vendi l'idoletto e guadagni {rep*4} potere per il clan!"
                                )
                            else:
                                await app.send_message(message.chat.id,"Ti serve un clan per usare questa cosa!")
                        if ricercato == "Dell'acqua fresca":
        
                            rep = 1
                            if tipo == "multiplo":
                                rep = int(quanto)
                                
                            await app.send_message(message.chat.id,"Dissetante e fresca.")
                            for x in range(rep):

                                if ricercato in zaino:

                                    nft.gestione_zaino(zaino,"rem",ricercato,1)
                                    
                                    player[username]["last"] -= 320

                                else:

                                    await app.send_message(message.chat.id,"Non ne hai!")
                                    break
                        elif ricercato == "BATH WATER":
        
                            rep = 1
                            if tipo == "multiplo":
                                rep = int(quanto)
                                
                            await app.send_message(message.chat.id,"Dissetante e fwesca (*^ω^)")
                            for x in range(rep):
    
                                if ricercato in zaino:

                                    nft.gestione_zaino(zaino,"rem",ricercato,1)
                                    
                                    player[username]["last"] -= 420
                                    if username in last_dungeon:
                                        last_dungeon[username] -= 50
                                    if username in last_boss:
                                        last_boss[username] -= 50
                                    if username in last_assalto:
                                        last_assalto[username] -= 50
                                    if username in inabilitati:
                                        inabilitati[username] -= 240
                                    
                                else:

                                    await app.send_message(message.chat.id,"Nywon nye hai più ┬─┬ ノ( ゜-゜ノ)")
                                    break
                            
                        
                        elif ricercato == "Dell'ambrosia":
    
                            rep = 1
                            if tipo == "multiplo":
                                rep = int(quanto)
                                
                            await app.send_message(message.chat.id,"Un potere devastante scorre nelle tue vene.")
                            for x in range(rep):

                                if ricercato in zaino:

                                    nft.gestione_zaino(zaino,"rem",ricercato,1)
                                    try:

                                        player[username]["scheda"]["boost"]["assalto"][
                                            "Divino"
                                        ]["dur"] += 6
                                    except:

                                        player[username]["scheda"]["boost"]["assalto"][
                                            "Divino"
                                        ] = {"lv": 1, "dur": 6}

                                else:

                                    await app.send_message(message.chat.id,"Non ne hai!")
                                    break
                        elif ricercato == "Un eco-locatore":
                            if "last-eco" in player[username]:
                                last = player[username]["last-eco"]
                            else:
                                last = 0
                            now = time.time()

                            elapsed = now - last
                            if elapsed > 3651:
                                for x in list(liste.location):
                                    if trader["meteo"][x] == "Pioggia" or trader["meteo"][x] == "Tempesta":
                                        locan = x
                                        break
                                    else:
                                        locan = random.choice(list(liste.location))
                                player[username]["location"] = locan
                                player[username]["last-eco"] = time.time()
                                await app.send_message(message.chat.id,f"Segnale trovato!\nL'eco si illumina e magicamente partite per {locan}!")
                                if player[username]["zaino"]["Un eco-locatore"] > 1:
                                    quanti = player[username]["zaino"]["Un eco-locatore"] - 1
                                    try:
                                        player[username]["zaino"]["Dell'ambrosia"] += quanti
                                    except:
                                        player[username]["zaino"]["Dell'ambrosia"] = quanti     
                                    player[username]["zaino"]["Un eco-locatore"] = 1
                                    message.reply("I tuoi eco extra sono stati convertiti in ambrosia!")
                            else:
                                await app.send_message(message.chat.id,"L'eco non ha trovato nulla!")
                            
                            
                        elif ricercato == "La spezia":
                            if username not in trader["preferenziale"]:
                                rep = 1
                                if tipo == "multiplo":
                                    rep = int(quanto)
                                    if rep >= 10:
                                        rep = 10

                                for x in range(rep):

                                    if ricercato in zaino:

                                        nft.gestione_zaino(zaino,"rem",ricercato,1)
                                        trader["preferenziale"].append(username)
                                        trader["preferenziale"].append(username)
                                        trader["preferenziale"].append(username)
                                        trader["preferenziale"].append(username)
                                        try:

                                            player[username]["scheda"]["boost"]["sfida"][
                                                "Speziato"
                                            ]["dur"] += 4
                                        except:

                                            player[username]["scheda"]["boost"]["sfida"][
                                                "Speziato"
                                            ] = {"lv": 1, "dur": 4}

                                        random.shuffle(trader["preferenziale"])

                                    else:
                                        x -= 1
                                        await app.send_message(message.chat.id,"Sono finiti prima!")
                                        break
                                await app.send_message(message.chat.id,f"La spezia attirerà {rep*4} persone!")
                            else:
                                ff = str(trader["preferenziale"].count(username))
                                await app.send_message(message.chat.id,f"Hai ancora una spezia attiva! ({ff} cariche)")

                        elif ricercato == "Un hp extra":
                            rep = 1
                            if tipo == "multiplo":
                                rep = int(quanto)
                                
                            nowcap = player[username]["cap"]
                            try:
                                cap = round(((player[username]["livello"]/2) + (player[username]["topP"]*2) + (player[username]["totali"]/1000) + (len(player[username]["obbiettivi"])/2) + (len(player[username]["bestiario"])/5)+ (player[username]["grado"]/700)) * 20) 
                            except:
                                cap = round(((player[username]["livello"]/2) + (player[username]["totali"]/1000) + (len(player[username]["obbiettivi"])/2) + (len(player[username]["bestiario"])/5)) * 20)
                            
                            if (nowcap + (liste.valore[ricercato] * rep)) > cap:
                                await app.send_message(message.chat.id,"Non sei abbastanza esperto per usare così tanti punti!")
                            else:
                                for x in range(rep):

                                    if ricercato in zaino:

                                        nft.gestione_zaino(zaino,"rem",ricercato,1)
                                        player[username]["scheda"]["hp"] += 1

                                    else:
                                        x -= 1
                                        await app.send_message(message.chat.id,"Sono finiti prima!")
                                        break
                                
                                
                                player[username]["cap"] += liste.valore[ricercato] * (x + 1 )
                                ora = player[username]["cap"]
                                await app.send_message(message.chat.id,f"+{rep}up\n({ora}\{cap})")
                            
                        elif ricercato == "Un punto attacco":
                            rep = 1
                            if tipo == "multiplo":
                                rep = int(quanto)
                            nowcap = player[username]["cap"]
                            try:
                                cap = round(((player[username]["livello"]/2) + (player[username]["topP"]*2) + (player[username]["totali"]/1000) + (len(player[username]["obbiettivi"])/2) + (len(player[username]["bestiario"])/5)+ (player[username]["grado"]/700)) * 20)
                            except:
                                cap = round(((player[username]["livello"]/2) + (player[username]["totali"]/1000) + (len(player[username]["obbiettivi"])/2) + (len(player[username]["bestiario"])/5)) * 20)
                            
                            if (nowcap + (liste.valore[ricercato] * rep)) > cap:
                                await app.send_message(message.chat.id,"Non sei abbastanza esperto per usare così tanti punti!")
                            else:
                                for x in range(rep):

                                    if ricercato in zaino:

                                        nft.gestione_zaino(zaino,"rem",ricercato,1)
                                        player[username]["scheda"]["atk"] += 1

                                    else:
                                        x -= 1
                                        await app.send_message(message.chat.id,"Sono finiti prima!")
                                        break
                                player[username]["cap"] += liste.valore[ricercato] * (x + 1 )
                                ora = player[username]["cap"]
                                await app.send_message(message.chat.id,f"{rep} danno extra approvato\n({ora}\{cap})")

                        elif ricercato == "Un punto difesa":
                            rep = 1
                            if tipo == "multiplo":
                                rep = int(quanto)
                            nowcap = player[username]["cap"]
                            try:
                                cap = round(((player[username]["livello"]/2) + (player[username]["topP"]*2) + (player[username]["totali"]/1000) + (len(player[username]["obbiettivi"])/2) + (len(player[username]["bestiario"])/5)+ (player[username]["grado"]/700)) * 20)
                            except:
                                cap = round(((player[username]["livello"]/2) + (player[username]["totali"]/1000) + (len(player[username]["obbiettivi"])/2) + (len(player[username]["bestiario"])/5)) * 20)
                            
                            if (nowcap + (liste.valore[ricercato] * rep)) > cap:
                                await app.send_message(message.chat.id,"Non sei abbastanza esperto per usare così tanti punti!")
                            else:
                                for x in range(rep):

                                    if ricercato in zaino:

                                        nft.gestione_zaino(zaino,"rem",ricercato,1)
                                        player[username]["scheda"]["def"] += 1

                                    else:
                                        x -= 1
                                        await app.send_message(message.chat.id,"Sono finiti prima!")
                                        break
                                    
                                player[username]["cap"] += liste.valore[ricercato] * (x + 1 )
                                ora = player[username]["cap"]
                                await app.send_message(message.chat.id,f"Ecco a te {rep} scudino extra\n({ora}\{cap})")

                        elif ricercato == "Un punto agilità":
                            rep = 1
                            if tipo == "multiplo":
                                rep = int(quanto)
                            nowcap = player[username]["cap"]
                            try:
                                cap = round(((player[username]["livello"]/2) + (player[username]["topP"]*2) + (player[username]["totali"]/1000) + (len(player[username]["obbiettivi"])/2) + (len(player[username]["bestiario"])/5)+ (player[username]["grado"]/700)) * 20)
                            except:
                                cap = round(((player[username]["livello"]/2) + (player[username]["totali"]/1000) + (len(player[username]["obbiettivi"])/2) + (len(player[username]["bestiario"])/5)) * 20)
                            
                            if (nowcap + (liste.valore[ricercato] * rep)) > cap:
                                await app.send_message(message.chat.id,"Non sei abbastanza esperto per usare così tanti punti!")
                            else:
                                for x in range(rep):

                                    if ricercato in zaino:

                                        nft.gestione_zaino(zaino,"rem",ricercato,1)
                                        player[username]["scheda"]["agi"] += 1

                                    else:
                                        x -= 1
                                        await app.send_message(message.chat.id,"Sono finiti prima!")
                                        break
                                player[username]["cap"] += liste.valore[ricercato] * (x + 1 )
                                ora = player[username]["cap"]
                                await app.send_message(message.chat.id,f"Aumentata l'abilità di salto dello {rep * 0.42069}%\n({ora}\{cap})")
                                

                        elif ricercato == "Una licenza per animali domestici":
                            rep = 1
                            if tipo == "multiplo":
                                rep = 1
                            for x in range(rep):

                                if ricercato in zaino:

                                    nft.gestione_zaino(zaino,"rem",ricercato,1)
                                    pet = random.choice(liste.animaletti)
                                    await app.send_message(message.chat.id,
                                        f"Un aereoscafo dal cielo lancia una cassa, che cadendo a terra rimbalza una quindicina di volte.\nDa dentro esce un bellissimo {pet}, che figo!"
                                    )
                                    player[username]["pet"] = pet
                                    
                                    try:
                                        player[username]["varie"]["cambi"] += 1
                                    except:
                                        player[username]["varie"]["cambi"] = 1
                                else:
                                    x -= 1
                                    await app.send_message(message.chat.id,"Sono finiti prima!")
                                    break
                        
                        
                        elif ricercato == "Un biglietto polivalente":
                            rep = 1
                            for x in range(rep):

                                if ricercato in zaino:
                                    nft.gestione_zaino(zaino,"rem",ricercato,1)
                                    player[username]["location"] = "Hub"
                                    await app.send_message(message.chat.id,"Uno spaziocottero atterra e ti carica al volo!\nVolate altissimi nello spazio fino a raggiungere l'hub!\nDa qui ci si può lanciare ovunque!")
                                else:

                                    await app.send_message(message.chat.id,"Sono finiti prima!")
                                    break
                        elif ricercato == "Del latte in sacchetto":
                            rep = 1
                            if tipo == "multiplo":
                                rep = int(quanto)
                            for x in range(rep):

                                if ricercato in zaino:
                                    if username in inabilitati:
                                        if (
                                            inabilitati[username]
                                            != "Una copia dell'arte della guerra autografata"
                                        ):
                                            nft.gestione_zaino(zaino,"rem",ricercato,1)
                                            await app.send_message(message.chat.id,
                                                "Bevi tutto il latte e ti senti subito meglio, che comodo!"
                                            )
                                            inabilitati.pop(username)
                                        else:
                                            await app.send_message(message.chat.id,"Non puoi riprenderti così!")
                                            break
                                    else:
                                        await app.send_message(message.chat.id,"Sei già in forza")
                                        break
                                else:

                                    await app.send_message(message.chat.id,"Sono finiti prima!")
                                    break

                        elif ricercato in [
                            "Un fune di fuga",
                            "Uno stimpak",
                            "Candela blu",
                            "Ultimo barlore",
                        ]:
                            if "dungeon" in player[username]:
                                rep = 1

                                if ricercato == "Un fune di fuga":
                                    player[username].pop("dungeon")
                                    await app.send_message(message.chat.id,
                                        "Giri su te stesso velocissimo e finisci fuori dal dungeon vomitando!"
                                    )
                                    if (
                                        "A ri vederci"
                                        not in player[username]["obbiettivi"]
                                    ):
                                        player[username]["obbiettivi"].append(
                                            "A ri vederci"
                                        )
                                        await app.send_message(message.chat.id,
                                            "Obbiettivo completato!\n**A ri vederci**, ci ri vederemo signor. dungeun!"
                                        )

                                if ricercato == "Uno stimpak":
                                    player[username]["dungeon"]["danno"] -= 200
                                    await app.send_message(message.chat.id,"Ti curi di 200 hp, ottimo ottimo!")
                                    if "Tossico" not in player[username]["obbiettivi"]:
                                        player[username]["obbiettivi"].append("Tossico")
                                        await app.send_message(message.chat.id,
                                            "Obbiettivo completato!\n**Tossico**, ti sei ignettato cose strane in un braccio!"
                                        )
                                if ricercato == "Candela blu":
                                    player[username]["dungeon"]["mostri"].append("Boss")
                                    await app.send_message(message.chat.id,
                                        "Delle oscure presenze si aggirano per il dungeon...\nEsso cresce a vista d'occhio!"
                                    )
                                    if (
                                        "Te la sei cercata"
                                        not in player[username]["obbiettivi"]
                                    ):
                                        player[username]["obbiettivi"].append(
                                            "Te la sei cercata"
                                        )
                                        await app.send_message(message.chat.id,
                                            "Obbiettivo completato!\n**Te la sei cercata**, tirati contro un boss!"
                                        )
                                if ricercato == "Ultimo barlore":
                                    player[username]["dungeon"]["mostri"].append(
                                        random.choice(liste.stanze)
                                    )
                                    await app.send_message(message.chat.id,
                                        "Alzi al cielo l'ultimo barlore!\nEsso si incendia e con un lampo di luce ti illumina la via!"
                                    )
                                    if (
                                        "Ultima a morire"
                                        not in player[username]["obbiettivi"]
                                    ):
                                        player[username]["obbiettivi"].append(
                                            "Ultima a morire"
                                        )
                                        await app.send_message(message.chat.id,
                                            "Obbiettivo completato!\n**Ultima a morire**, spera in bene, andrà bene dai!"
                                        )
                                nft.gestione_zaino(zaino,"rem",ricercato,1)

                            else:
                                await app.send_message(message.chat.id,"A quanto pare non sei in un dungeon!")
                        elif ricercato == "Un oggetto incartato":
                            rep = 1
                            if tipo == "multiplo":
                                vincite = dict()
                                if len(quanto) <= 8:
                                    
                                    if int(quanto) >= 100000:
                                        rep = 100000
                                    else:
                                        rep = int(quanto)
                                else:
                                    rep = 100000
                                
                            if rep <= zaino[ricercato]:
                                for x in range(rep):

                                
                                    vertutto = tutto
                                    if evento["evento"] == "mega":
                                        vertutto = tuttov + megaman + megaman
                                    if evento["evento"] == "zombie":
                                        vertutto = tuttov + zombie + zombie
                                    if evento["evento"] == "gungeon":
                                        vertutto = tuttov + gungeon + gungeon
                                    if evento["evento"] == "magic":
                                        vertutto = tuttov + magic + magic + magic

                                    
                                    if rep == 1:
                                        nft.gestione_zaino(zaino,"rem",ricercato,1)
                                        contentino = random.choice(vertutto)
                                        if 0.001 > random.random():
                                            contentino = "Nulla assoluto"
                                        try:
                                            player[username]["zaino"][contentino] += 1
                                        except:
                                            player[username]["zaino"][contentino] = 1
                                        try:
                                            await app.send_message(
                                                username,
                                                f"Apri l'oggetto con molto stupore e scopri essere; {contentino}, speravi in una bici ma vabbè su!",
                                            )
                                        except:
                                            pass
                                    else:
                                        contentino = random.choice(vertutto)
                                        
                                        try:
                                            vincite[contentino] += 1
                                        except:
                                            vincite[contentino] = 1
                                    
                                        
                                        


                            else:
                                await app.send_message(message.chat.id,"Non ne hai abbastanza!")
                                rep = 0
                            
                            if rep > 1:
                                nft.gestione_zaino(zaino,"rem",ricercato,rep)
                                for x in sorted(vincite):
                                    
                                    try:
                                        player[username]["zaino"][x] += vincite[x]
                                    except:
                                        player[username]["zaino"][x] = vincite[x]
                                    try:
                                        vinto += f"{x} x {vincite[x]}\n"
                                    except:
                                        vinto = f"Hai vinto le seguenti cose:\n{x} x {vincite[x]}\n"
                                
                                vinto += "\nE basta"
                                messaggini = nft.separatore(vinto)
                                for mess in messaggini:
                                    try:

                                        await app.send_message(username, mess)
                                        time.sleep(0.1)
                                    except:
                                        pass
                                vincite = dict()
                                vinto = ""
                                

                    if tipo == "errante":
                        elapsed = time.time() - trader["attese"][ricercato]

                        if elapsed < 1800:
                            ty_res = time.gmtime(1800 - elapsed)

                            tempo = time.strftime("%H:%M:%S", ty_res)
                            if ricercato == "Una mail di spam con anche qualche pene":
                                await app.send_message(message.chat.id,
                                    f"Forse mancano ancora più maiuscole a caso...\nLo sbagliatore automatico dovrebbe finire in {tempo} minuti!"
                                )
                            if ricercato == "Il controller del super raggio mortale a neutroni mega pericolosissimo":
                                await app.send_message(message.chat.id,
                                    f"Non riesco a trovare il segnale\nSpero di trovarlo tra {tempo} minuti!"
                                )
                            if (
                                ricercato
                                == "Una copia dell'arte della guerra autografata"
                            ):
                                await app.send_message(message.chat.id,
                                    f"Serve leggere di più!\nIl capitolo finirà tra {tempo} pagine!"
                                )
                            if ricercato == "un castoro cattivissimo":
                                await app.send_message(message.chat.id,
                                    f"Il castoro cattivissimo si sta ancora scaldando!\nFinirà il suo riscaldamento tra {tempo} minuti!"
                                )
                            if ricercato == "Un megafono megaenorme":
                                await app.send_message(message.chat.id,
                                    f"Batteria scarica!\nRicarica stimanta:{tempo} minuti!"
                                )

                        else:
                            if chi not in list(player):
                                await app.send_message(message.chat.id,"Quell'utente non esiste!")
                            else:
                                if ricercato == "Il controller del super raggio mortale a neutroni mega pericolosissimo":
                                    trader["attese"][
                                        "Il controller del super raggio mortale a neutroni mega pericolosissimo"
                                    ] = time.time()
                                    
                                    zaino.pop("Il controller del super raggio mortale a neutroni mega pericolosissimo")
                                    
                                    
                                    acui = random.choice(list(player))
                                    trader["erranti"]["Il controller del super raggio mortale a neutroni mega pericolosissimo"] = acui
                                    
                                    pool = player[acui]["zaino"]
                                    pool["Il controller del super raggio mortale a neutroni mega pericolosissimo"] = 1
                                    
                                    posto =  random.choice(liste.location)
                                    for g in range(9):
                                        if posto != "Hub":
                                            break
                                        else:
                                            posto =  random.choice(liste.location)
                                    player[chi]["location"] = posto
                                    
                                    try:

                                        await app.send_message(
                                            chi,
                                            f"Eri totalmente intento a pescare quando un raggio mega mortale ti cade a 2cm di distanza, l'impatto è fortissimo ma non ti ferisce!\nAl tuo risveglio noti di non essere esattamente dove ti trovavi prima...",
                                        )

                                    except:
                                        pass
                                    try:
                                        await app.send_message(
                                            acui,
                                            f"Porca vacca, un controller col nome corto e semplice ti è caduto in testa!",
                                        )
                                    except:
                                        pass
                                    try:
                                        await app.send_message(
                                            username,
                                            f"Indirizzi il laser su {chi} e spari fortissimo!\nL'impatto del laser non distrugge il terreno perfettamente renderizzato ma spazza via il poveretto!\nL'onda d'urto è però così forte da far andare lontanissimo il controller!",
                                        )
                                    except:
                                        pass
                                    
                                if (
                                    ricercato
                                    == "Una mail di spam con anche qualche pene"
                                ):
                                    trader["attese"][
                                        "Una mail di spam con anche qualche pene"
                                    ] = time.time()

                                    zaino.pop("Una mail di spam con anche qualche pene")
                                    acui = random.choice(list(player))
                                    trader["erranti"][
                                        "Una mail di spam con anche qualche pene"
                                    ] = acui
                                    pool = player[acui]["zaino"]
                                    pool["Una mail di spam con anche qualche pene"] = 1

                                    player[chi]["punti"] -= 100
                                    player[username]["punti"] += 100

                                    try:

                                        await app.send_message(
                                            chi,
                                            f"Cliccando a caso /sfida ti si apre un link altamente non voluto.\nCercando di uscire spendi 100 tuoi punti sfida in vibratori e cose simili.\nForse non l'hai fatto totalmente per sbaglio.",
                                        )

                                    except:
                                        pass
                                    try:
                                        await app.send_message(
                                            acui,
                                            f"Ricevi una mail truffa, ovviamente sei troppo furbo per cascarci, ma un inoltro è sicuramente una buona idea!",
                                        )
                                    except:
                                        pass
                                    try:
                                        await app.send_message(
                                            username,
                                            f"E taaac, 100 punti sfida gratis!\n\n\nHey aspetta un attimo, ci sta anche l'indirizzo di {acui} tra i destinatari...",
                                        )
                                    except:
                                        pass

                                if ricercato == "Un megafono megaenorme":
                                    trader["attese"]["Un megafono megaenorme"] = time.time()
                                    zaino.pop("Un megafono megaenorme")
                                    acui = random.choice(list(player))
                                    trader["erranti"]["Un megafono megaenorme"] = acui
                                    pool = player[acui]["zaino"]
                                    pool["Un megafono megaenorme"] = 1
                                    username = chi
                                    user = player[username]
                                    scheda = user["scheda"]
                                    arma = scheda["arma"]
                                    prot = scheda["protezione"]
                                    nft.unequiP1(scheda, prot, protezioni)
                                    nft.unequiA(scheda, arma, armi)
                                    scheda["Ap"] = "Base"
                                    
                                    scheda["set"] = None
                                    scheda["anello"] = None
                                    try:

                                        await app.send_message(
                                            chi,
                                            f"HEY HEY HEY HEY HEY\n HEY HEY HEY HEY HEY HEY HEY HEY\nHEY HEY\nHEY HEY\nHEY HEY\nHEY HEY\nHEY HEY\n",
                                        )

                                    except:
                                        pass
                                    try:

                                        await app.send_message(
                                            acui,
                                            f"Hey, ci sta un megafono megaenorme qui perterra!",
                                        )
                                    except:
                                        pass

                                    try:
                                        await app.send_message(message.chat.id,
                                            f"E anche oggi si infastidisce qualcuno, passi a {acui} il megafono e te ne vai!"
                                        )
                                    except:
                                        pass

                                if (
                                    ricercato
                                    == "Una copia dell'arte della guerra autografata"
                                ):
                                    trader["attese"][
                                        "Una copia dell'arte della guerra autografata"
                                    ] = time.time()

                                    zaino.pop(
                                        "Una copia dell'arte della guerra autografata"
                                    )
                                    acui = random.choice(list(player))
                                    trader["erranti"][
                                        "Una copia dell'arte della guerra autografata"
                                    ] = acui
                                    pool = player[acui]["zaino"]
                                    pool[
                                        "Una copia dell'arte della guerra autografata"
                                    ] = 1

                                    inabilitati[
                                        chi
                                    ] = "Una copia dell'arte della guerra autografata"

                                    try:

                                        await app.send_message(
                                            chi,
                                            f"Eri totalmente intento a farti i fatti tuoi quando BONK!\nVieni colpito fortissimo da un libro di un certo spessore, ci vorrà un attimo a riprendersi...",
                                        )
                                    except:
                                        pass
                                    try:
                                        await app.send_message(
                                            acui,
                                            f"In una libreria ci sta in sconto una copia dell'arte della guerra, perchè non comprarla!",
                                        )
                                    except:
                                        pass
                                    try:
                                        await app.send_message(
                                            username,
                                            f"Prendi la copia del libro, e dopo averlo letto per diverso tempo, colpisci fortissimo in testa {chi}!\nLa copia si rompe all'impatto, ma vabbè è solo una ristampa",
                                        )
                                    except:
                                        pass

                                if ricercato == "un castoro cattivissimo":
                                    cpool = player[chi]["zaino"]
                                    if len(list(cpool)) > 4:
                                        mas = 0
                                        while True:
                                            preso = random.choice(list(cpool))
                                            if (
                                                preso in liste.anelli
                                                or "1" in preso
                                                or "2" in preso
                                                or "3" in preso
                                                or "0" in preso
                                                or mas == 20 
                                            ) and preso not in liste.decoro:
                                                break
                                            mas += 1
                                        nft.gestione_zaino(cpool,"rem",preso,1)
                                        nft.gestione_zaino(zaino,"add",preso,1)
                                        cpool["un castoro cattivissimo"] = 1

                                        zaino.pop("un castoro cattivissimo")
                                        try:

                                            await app.send_message(
                                                chi,
                                                f"Dai su, a cosa ti serve un {preso} quando puoi avere un bellissimo castoro?",
                                            )
                                        except:
                                            pass
                                        try:

                                            await app.send_message(
                                                username,
                                                f"Mandi il tuo castoro cattivissimo dritto verso {chi}, lo vedi tornare con {preso}!\nPeccato che un aquila rubi il castoro cattivissimo esattamente prima di poterlo riprendere in mano!",
                                            )
                                        except:
                                            pass
                                        trader["attese"]["un castoro cattivissimo"] = time.time()
                                        trader["erranti"][
                                            "un castoro cattivissimo"
                                        ] = chi
                                    else:
                                        await app.send_message(message.chat.id,
                                            "Quel giocatore non ha nulla di interessante..."
                                        )

                else:
                    await app.send_message(message.chat.id,"Questo item non è usabile!")


@app.on_message(filters.command(["forgiabili", "forgiabili@NFTchallengebot"]) & ~filters.user(bannati) & ~filters.chat(non_qui)
)
async def forgiabili(client, message):
    if len(message.command) == 1:
        minimo = "0"
    else:
        minimo = message.command[1]

    username = message.from_user.username
    zaino = player[username]["zaino"]
    text = f"Potresti forgiare:"
    for figura in zaino:
        qt = zaino[figura]
        if figura in list(armi) and qt > 1:
            if figura[-1] >= minimo:
                tipo = armi[figura]["type"]
                text += f"\n - `{figura}` x {qt} {tipo}"
        elif figura in protezioni and qt > 1:
            if figura[-1] >= minimo:
                tipo = protezioni[figura]["type"]
                text += f"\n - `{figura}` x {qt} {tipo}"

    chunk = nft.separatore(text)
    for t in chunk:
        try:
            await app.send_message(message.chat.id,t)
        except:
            pass


@app.on_message(filters.command(["zaino", "zaino@NFTchallengebot", "z"]) & ~filters.user(bannati)
)
async def zainoC(client, message):
    if len(message.command) == 1:

        username = message.from_user.username
        zaino = player[username]["zaino"]
        numero = len(player[username]["zaino"])
        text = f"Al momento possiedi ben {numero} item:"
        for figura in sorted(list(zaino)):
            qt = zaino[figura]
            if figura in list(armi):

                tipo = armi[figura]["type"]
            elif figura in protezioni:

                tipo = protezioni[figura]["type"]
            elif figura in liste.decoro:
                tipo = "✨"
            elif figura in liste.usabili:
                tipo = "👝"
            elif figura in liste.libri:
                tipo = "📓"
            else:
                tipo = "⚙️"
            
            text += f"\n - `{figura}` x {qt} {tipo}"
            text += nft.correggiemoji(figura, emojiz,item_boss,item_pescatore)
            
        text += "\nPuoi vedere categorie simili con /zaino armi, protezioni, anelli, decoro o usabili!"
        chunk = nft.separatore(text)
        for t in chunk:
            try:
                await app.send_message(message.chat.id,t)
            except:
                pass
    else:
        categoria = nft.listToString(message.command[1:])
        username = message.from_user.username
        zaino = player[username]["zaino"]
        numero = len(player[username]["zaino"])
        text = f"Ecco a te un elenco più specifico:"
        if categoria in ["evento","armi","protezioni","pesca","boss","usabili","decoro","gadget","libri"]:
            for figura in sorted(list(zaino)):
                qt = zaino[figura]
                if categoria == "evento":
                    if figura[:-4] in emojiz or figura in emojiz:
                        text += f"\n - `{figura}` x {qt} "
                        text += nft.correggiemoji(figura, emojiz,item_boss,item_pescatore)
                elif categoria == "armi":
                    if figura in armi:
                        text += f"\n - `{figura}` x {qt} 🗡"
                        text += nft.correggiemoji(figura, emojiz,item_boss,item_pescatore)
                elif categoria == "protezioni":
                    if figura in protezioni:
                        text += f"\n - `{figura}` x {qt} 🛡"
                        text += nft.correggiemoji(figura, emojiz,item_boss,item_pescatore)
                elif categoria == "pesca":
                    if figura[:-4] in item_pescatore:
                        text += f"\n - `{figura}` x {qt} "
                        if figura in armi:
                            text += "🗡"
                        if figura in protezioni:
                            text += "🛡"
                        if figura in liste.decoro:
                            text += "✨"
                        if figura in liste.anelli:
                            text += "⚙️"
                        
                        text += nft.correggiemoji(figura, emojiz,item_boss,item_pescatore)
                elif categoria == "boss":
                    if figura[:-4] in item_boss or figura in item_boss:
                        text += f"\n - `{figura}` x {qt} "
                        if figura in armi:
                            text += "🗡"
                        if figura in protezioni:
                            text += "🛡"
                        if figura in liste.decoro:
                            text += "✨"
                        if figura in liste.anelli:
                            text += "⚙️"
                        
                        text += nft.correggiemoji(figura, emojiz,item_boss,item_pescatore)
                elif categoria == "usabili":
                    if figura in liste.usabili:
                        text += f"\n - `{figura}` x {qt} 👝"
                        text += nft.correggiemoji(figura, emojiz,item_boss,item_pescatore)
                elif categoria == "decoro":
                    if figura in liste.decoro:
                        text += f"\n - `{figura}` x {qt} ✨"
                        text += nft.correggiemoji(figura, emojiz,item_boss,item_pescatore)
                elif categoria == "gadget":
                    if figura in liste.anelli:
                        text += f"\n - `{figura}` x {qt} ⚙️"
                        text += nft.correggiemoji(figura, emojiz,item_boss,item_pescatore)
                elif categoria == "libri":
                    if figura in liste.libri:
                        text += f"\n - `{figura}` x {qt} 📓"
                        text += nft.correggiemoji(figura, emojiz,item_boss,item_pescatore)
        else:
            if 1 == 1:

                if "," in categoria:
                    if len(categoria.split(",")) < 5:
                        for sear in categoria.split(","):
                            possibili = nft.search(zaino, sear)
                            for asd in sorted(list(possibili)):

                                qt = zaino[asd]
                                if asd in armi:
                                    tipo = "🗡"
                                if asd in protezioni:
                                    tipo = "🛡"
                                if asd in liste.usabili:

                                    tipo = "👝"
                                if asd in liste.anelli:
                                    tipo = "⚙️"
                                if asd in liste.libri:
                                    tipo = "📓"
                                if asd in liste.decoro:
                                    tipo = "✨"

                                text += f"\n - `{asd}` x {qt} {tipo}"
                                text += nft.correggiemoji(asd, emojiz,item_boss,item_pescatore)
                else:
                    possibili = nft.search(zaino, categoria)
                    for asd in sorted(list(possibili)):

                        qt = zaino[asd]
                        if asd in armi:
                            tipo = "🗡"
                        if asd in protezioni:
                            tipo = "🛡"
                        if asd in liste.usabili:

                            tipo = "👝"
                        if asd in liste.anelli:
                            tipo = "⚙️"
                        if asd in liste.libri:
                            tipo = "📓"
                        if asd in liste.decoro:
                            tipo = "✨"

                        text += f"\n - `{asd}` x {qt} {tipo}"
                        text += nft.correggiemoji(asd, emojiz,item_boss,item_pescatore)
        chunk = nft.separatore(text)
        for t in chunk:
            await app.send_message(message.chat.id,t)

domande = {}
@app.on_message((filters.regex(r"^Domande ❔")|filters.command(["domande"])) & filters.private & ~filters.user(bannati))
async def domandee(client, message):
    username = message.from_user.username
    if 1 == 1:
        f = nft.domandami(3,5,20)
        
        txt = f["text"]
        domande[username] = f
        
        bottoni = list()
        for appz in f["Risposte"]:
            bottoni.append([InlineKeyboardButton(appz, callback_data=f"dmando_{appz}")])

        reply_markup = InlineKeyboardMarkup(bottoni)

        await app.send_message(message.chat.id,txt, reply_markup=reply_markup)


@app.on_message( filters.private & ~filters.user(bannati) & (filters.regex(r"^Negozio 🛒")| filters.command(["negozio"])))
async def negozio(client, message):
    try:
        username = message.from_user.username
        if len(message.command) == 1:
            txt = "Benvenuto al negozio!\nQui potrai spendere la tua gloria per ottenere potenziamenti e simili!\nIl negozio è in beta, non odiarci\n"
            for cose in liste.shop:
                prezzo = liste.shop[cose]
                txt += f"{cose} - {prezzo} gloria 🏆\n"
            bottoni = list()
            for appz in liste.shop:
                bottoni.append([InlineKeyboardButton(appz, callback_data=f"negozio_{appz}")])

            reply_markup = InlineKeyboardMarkup(bottoni)

            await app.send_message(message.chat.id,txt, reply_markup=reply_markup)
        else:
            try:
                vuole = nft.listToString(message.command[1:])
                qt = vuole.split(" ")[-1]
                chiede =nft.listToString(vuole.split(" ")[0:-1])
                if chiede in list(liste.shop):
                    chiaro = [chiede]
                else:
                    chiaro = nft.search(list(liste.shop), chiede)
                if int(qt) > 0:
                    if len(chiaro) == 1:
                        ricerca = chiaro[0]
                        prezzo = liste.shop[ricerca] * int(qt)
                        if "gloria" in player[username]:
                            if player[username]["gloria"] >= prezzo:
                                nft.gestione_zaino(player[username]["zaino"],"add",ricerca,int(qt))
                                player[username]["gloria"] -= prezzo
                                await app.send_message(message.chat.id,f"Hai comprato {ricerca} a {prezzo} gloria!")
                                    
                            else:
                                await app.send_message(message.chat.id,"Non puoi permettertelo!") 
                        else:
                            await app.send_message(message.chat.id,"Non puoi permettertelo!")
                    else:
                        await app.send_message(message.chat.id,"Specifica di più!")
                else:
                    await app.send_message(message.chat.id,"Un quantità positiva perfavore!")
            except:
                await app.send_message(message.chat.id,"Usa /negozio cosa numero perfavore")
    except:
        txt = "Benvenuto al negozio!\nQui potrai spendere la tua gloria per ottenere potenziamenti e simili!\nIl negozio è in beta, non odiarci\n"
        for cose in liste.shop:
                prezzo = liste.shop[cose]
                txt += f"{cose} - {prezzo} gloria 🏆\n"
        bottoni = list()
        for appz in liste.shop:
                bottoni.append([InlineKeyboardButton(appz, callback_data=f"negozio_{appz}")])

        reply_markup = InlineKeyboardMarkup(bottoni)

        await app.send_message(message.chat.id,txt, reply_markup=reply_markup)


@app.on_message( ~filters.user(bannati) & filters.regex(r"^Info 🗞")|filters.command(["info"]))
async def eenfo(client, message):
    iscritti = len(player)
    trovabili = len(tuttov)
    strutturs = len(liste.strutture)
    set = len(liste.classi)
    animali = len(liste.animaletti)
    clans = len(clan)
    attivi = 0
    pescis = len(liste.pesci)
    diffe = len(liste.ingredienti)
    bossdif = len(liste.Boss)
    animalati = 0
    ora = 0
    setmuniti = 0
    cagata = random.choice(
        [
            "I dungeon non sono così impossibili",
            "Se non sai cosa fare puoi tentare /pesca, è un orribile passatempo!",
            "Sei in dubbio su cosa fare? Cerca supporto nei gruppi ufficiali!",
            "Ogni martedì e giocedì ci saranno le guerre tra clan!",
            "I boss cambiano ogni giorno, attento a non farteli fuggire!",
            "Ogni tanto il /trafficante cambia offerte!",
            "Ci vogliono circa 50 minuti tra un offerta del /trafficante ed un altra, mezz'ora più o mezz'ora meno!",
            "Attento a non cliccare troppo forte tutte le cose!",
            "Una volta scelto l'approccio quello resterà per sempre, o fino al prossimo cambio!",
            "Api!",
            "Ogni giorno il primo che dice primo nel parchetto ha un buon 70% di vincere 1 gloria!",
            "Perdi tante sfide? Cambia set!",
            "Ogni anello è unico!",
            "Valuta ttentamente i tuoi scambi!",
            "Serve un clan? Si, a tutti serve un clan!",
            "Ogni tanto ricorda di fare /negozio, coccolati un poco",
            "Il latte in sacchetto è il top del latte!",
            "Ricorda di avere un animaletto, lui farebbe tutto per te!",
            "/wikiboss è una buona fonte di idee per i boss, ma non basta",
            "Set speciali fanno danno a strutture apposite!",
            "/forgiabili è troppo vago? Mettici dopo un numero!",
            "Non faresti mai /rimuovi hp",
            "Setta una setta per avere bonus onesti",
            "Attento a non perderti",
            "Nutri le mucche e mungi le mucche, non essere troppo avaro",
            "Dona su /dona, aiuterà me a comprarmi del cibo",
            "Si, acquila",
            "/rimuovi accetta argomenti, 1,2,arma e protezione",
        ]
    )
    oggi = ""
    in_s = 0
    for v in trader["bossoggi"]:
        oggi += v + ", "
    for p in last_sms:
        if time.time() - last_sms[p] < 3600:
            ora += 1
    for ass in player:
        if player[ass]["preso"] == True:
            in_s += 1
        if "pet" in player[ass]:
            animalati += 1
        if player[ass]["prima"] == True:
            attivi += 1
        if "set" in player[ass]["scheda"]:
            if player[ass]["scheda"]["set"] != None:
                setmuniti += 1

    await app.send_message(message.chat.id,
        f"""**Menù info del bot:**
Iscritti: {iscritti}
Clan: {clans}
Oggetti trovabili in sfida: {trovabili}                  
Strutture inventate nel villaggio: {strutturs}                  
Animaletti possibili: {animali}                  
Persone con un animaletto: {animalati}
Set disponibili: {set} (__{setmuniti} set muniti__)
Pesci differenti: {pescis}
Boss differenti: {bossdif} ({oggi})
Draghi: 1
Cose rotte: __foooorse__

__Attivi oggi: {attivi}__
__Dei quali attivi nell'ultima ora: {ora}__
__Stanno sfidando: {in_s}__

Abbiamo un gruppo [ot](https://t.me/joinchat/RREYf8lUUsM4NDA0)
Gruppo di [mercato](https://t.me/joinchat/xDEsinMpBXk0MWRk)
Posto in cui si pobblicano i [suggerimenti](https://t.me/joinchat/6BDcD_z-w7A3ODU0)
Segnala i bug ad @ElSalamino

__{cagata}__"""
    )


@app.on_message(filters.command(["incanta", "incanta@NFTchallengebot", "inca"]) & ~filters.user(bannati) & ~filters.chat(non_qui)
)
async def incanta(client, message):
    username = message.from_user.username
    try:
        if len(message.command) == 1:
            hhgh = "/incanta oggetto , libro\nAl momento hai i seguenti equip:\n"
            for x in player[username]["incantamenti"]:
                cosa = player[username]["incantamenti"][x]
                hhgh += f"{x} -> {cosa}\n"
            chunk = nft.separatore(hhgh)
            for t in chunk:
                await app.send_message(message.chat.id,t)

        elif len(message.command) <= 3:
            await app.send_message(message.chat.id,"/incanta oggetto , libro")
        else:
            zaino = player[username]["zaino"]
            list_oggetto = nft.listToString(message.command[1:])
            oggetto = list_oggetto.split(",")[0]
            libro = list_oggetto.split(",")[1]
            
            if oggetto in possi:
                risultati = [oggetto]
            else:
                risultati = nft.search(possi, oggetto)
            
            if len(list(risultati)) > 1:
                await app.send_message(message.chat.id,"Sii più preciso sull'arma!")
            elif len(list(risultati)) == 0:
                await app.send_message(message.chat.id,"Non ci sono oggetti così chiamati!")
            elif len(list(risultati)) == 1:
                ogg = risultati[0]
                if libro in zaino:
                    risultati = [oggetto]
                else:
                    risultati = nft.search(zaino, libro)
                if len(list(risultati)) > 1:
                    await app.send_message(message.chat.id,"Sii più preciso sul libro!")
                elif len(list(risultati)) == 0:
                    await app.send_message(message.chat.id,"Non ci sono libri così chiamati nel tuo zaino!")
                elif len(list(risultati)) == 1:
                    ench = risultati[0]
                    nft.gestione_zaino(zaino,"rem",ench,1)
                    ench = liste.libri[ench]["ef"]
                    player[username]["incantamenti"][ogg] = ench
                    await app.send_message(message.chat.id,f"Da ora {ogg} sarà incantato con {ench}!")
    except:
        await app.send_message(message.chat.id,"/incanta oggetto , libro")
                       
@app.on_message(filters.command(["equipaggia", "equipaggia@NFTchallengebot", "equip","e"]) & ~filters.user(bannati) & ~filters.chat(non_qui)
)
async def equip(client, message):
    username = message.from_user.username

    if len(message.command) == 1:
        await app.send_message(message.chat.id,"/equipaggia oggetto")
    else:
        user = player[username]
        zaino = user["zaino"]
        list_oggetto = nft.listToString(message.command[1:])

        if list_oggetto in tutto:
            risultati = [list_oggetto]
        else:
            risultati = nft.search(zaino, list_oggetto)

        if len(list(risultati)) <= 15 and len(list(risultati)) > 1:
            serve = dict()
            for g in risultati:        
                if "LV" in g:
                    serve[g.split("LV")[1]] = g.split("LV")[0]
            try:
                risultati = [serve[sorted(serve)[-1]] + "LV" + sorted(serve)[-1]]
            except:
                pass
                                
        
        if len(list(risultati)) > 1:
            await app.send_message(message.chat.id,"Sii più preciso!")
        elif len(list(risultati)) == 0:
            await app.send_message(message.chat.id,"Non ci sono oggetti così chiamati nel tuo zaino!")
        elif len(list(risultati)) == 1:
            scheda = user["scheda"]
            t = "Non è equipaggiabile questa cosa!"
            
            if "LV" in risultati[0]:
                li = risultati[0].split(" LV")[1]
                if li == "X":
                    li = 10
                if li == "MAX":
                    li = 15
                pos = round((player[username]["livello"] + (player[username]["topP"]/2) + (len(player[username]["incantamenti"])/2))/5 )
                if int(li) <= pos:
                    if risultati[0] in armi:
                        t = ""
                        if scheda["arma"] != None:
                            
                            scheda["set"] = None
                            arma = scheda["arma"]
                            nft.unequiA(scheda, arma, armi)
                            t += "Arma rimossa\n"
                            scheda["Ap"] = "Base"
                        t += nft.equiA(scheda, risultati[0], armi)
                        
                    if risultati[0] in protezioni:
                        t = ""
                        if scheda["protezione"] != None:
                            
                            scheda["set"] = None
                            prot = scheda["protezione"]
                            nft.unequiP1(scheda, prot, protezioni)
                            t += "Protezione rimossa\n"
                            scheda["Ap"] = "Base"
                        t += nft.equiP1(scheda, risultati[0], protezioni)
                    

                        
                    arma = scheda["arma"]
                    protezione = scheda["protezione"]
                    
                    if (protezione != None and arma != None and t != "Hai già una arma addosso!" and t != "Hai già una protezione addosso!" and t != "Non è equipaggiabile questa cosa!"):
                        
                        t += "\n"
                        
                        listina = arma.split(" LV")
                        coso = listina[0]
                        listina2 = protezione.split(" LV")
                        ricercato = listina2[0]
                        to_c = [coso, ricercato]
                        if nft.is_in(to_c,item_pescatore):
                            scheda["set"] = "Pescatore"
                            t += "Set del Pescatore equipaggiato!\nStats extra e pesca migliorata!"
                            
                            if "Pescatore" in player[username]["setvisti"]:
                                pass
                            else:
                                player[username]["setvisti"].append("Pescatore")
                                t += "\nNuovo!"
                        if nft.is_in(to_c,megaset):
                            if ricercato == 'Chip terra':
                                scheda["set"] = "Forma terra"
                            if ricercato == 'Chip fuoco':
                                scheda["set"] = "Forma fuoco"
                            if ricercato == 'Chip lunare':
                                scheda["set"] = "Forma lunare"
                            if ricercato == 'Chip elettro':
                                scheda["set"] = "Forma elettro"
                            t += "Set mega equipaggiato!\nAbilità chip attivate!"
                            
                            if scheda["set"] in player[username]["setvisti"]:
                                pass
                            else:
                                player[username]["setvisti"].append(scheda["set"])
                                t += "\nNuovo!"
                        else:
                            for tipi in liste.classi:
                                need = liste.classi[tipi]
                                if to_c == need: 
                                    if 1 == 2:
                                        t+= "QUESTO SET ESISTE GIA', CHE SCHIFO\n"   
                                    else:         
                                                    
                                        scheda["set"] = tipi
                                        t += liste.frasi_set[tipi]
                            if scheda["set"] in player[username]["setvisti"] or scheda["set"] == None:
                                pass
                            else:
                                player[username]["setvisti"].append(scheda["set"])
                                t += "\nNuovo!"
                else:
                    
                    t += "\nLivello troppo basso!"              
                                
                


            if risultati[0] in liste.anelli:
                scheda["anello"] = risultati[0]
                t = f"{risultati[0]} equipaggiato!"


            await app.send_message(message.chat.id,t)
            if scheda["set"] != None:
                if "Collezionista" not in player[username]["obbiettivi"] and len(
                    player[username]["setvisti"]
                ) >= len(liste.classi):
                    player[username]["obbiettivi"].append("Collezionista")
                    await app.send_message(
                        username,
                        "Obbiettivo completato!\n**Collezionista**, hai visto tutti i set! __Per ora__",
                    )

                if (
                    "A metà strada" not in player[username]["obbiettivi"]
                    and len(player[username]["setvisti"]) >= len(liste.classi) / 2
                ):
                    player[username]["obbiettivi"].append("A metà strada")
                    await app.send_message(
                        username,
                        "Obbiettivo completato!\n**A metà strada**, sei al provare il 50% dei set esistenti! __Per ora__",
                    )

                if (
                    "Un decimo della collezione" not in player[username]["obbiettivi"]
                    and len(player[username]["setvisti"]) >= len(liste.classi) / 10
                ):
                    player[username]["obbiettivi"].append("Un decimo della collezione")
                    await app.send_message(
                        username,
                        "Obbiettivo completato!\n**Un decimo della collezione**, sei al provare il 10% dei set esistenti! __Per ora__",
                    )

                if (
                    "Prima scoperta" not in player[username]["obbiettivi"]
                    and len(player[username]["setvisti"]) >= 1
                ):
                    player[username]["obbiettivi"].append("Prima scoperta")
                    await app.send_message(
                        username,
                        "Obbiettivo completato!\n**Prima scoperta**, hai scoperto il tuo primo set, complimenti! __Per ora__",
                    )


@app.on_message(filters.command(["wikiboss", "wikiboss@NFTchallengebot", "wiki"]) & ~filters.user(bannati)
)
async def wiki(client, message):

    BossAbi = {"Comandante della bastiglia" : "Un esperto in difesa, un esperto in tutto ciò che serve per non morire.",
        "Franco est": "Difficile ma potrebbe valerne la pena",
        "Fantasma del rimorso": "Un fantasma intangibile, che vuoi che sia?",
        "IL FOLLE": "COSE SUCCEDONO MA E' UNO SCONTRO NORMALE E FOOOLLE",
        "Leviatano delle sabbie": "Un leviatano in grado di controllare la sabbia, fate attenzione a non prolungare troppo lo scontro",
        "Cerbero": "Un agglomerato di odio e morte, spesso serve ucciderlo diverse volte prima di morire",
        "Demone spezza-ossa": "Presta attenzione a lui, un colpo solo potrebbe esserti fatale!",
        "Carl": "Non è molto spaventoso più che tutto è molto sfuggevole",
        "Orrore della palude": "Un tuttuno con la palude, difficile da abbattere senza i giusti mezzi!",
        "IppoSciamano": "Piccolo ed indifeso, piccolo e pieno di antichi fantasmi del passato",
        "Pensatore corrotto":"Blocca le tue difese, inprigiona la tua anima e ti lascia marcire"
    }
    text = "Ecco una wiki dei boss conosciuti:\n"
    for b in trader["bossoggi"]:

        abi = BossAbi[b]
        stat = liste.Boss[b]
        vita = stat["hp"]
        at = stat["atk"]
        dif = stat["def"]
        agi = stat["agi"]

        text += f"{b}, un terribile boss!\n❤️Vita: {vita}\n🪓Attacco: {at}\n🥋Difesa: {dif}\n🌪️Agilità: {agi}\n⭐️Abilità: {abi}\n\n"
    text += "Perdere contro un boss ti inabiliterà per molto tempo, fai attenzione!"
    await app.send_message(message.chat.id,text)


posA = ["arma", "spada", "1", "a","armi","attacco"]
posB = ["protezione", "scudo", "prot", "2", "p","pr"]


@app.on_message(filters.command(["personal", "personal@NFTchallengebot"]) & ~filters.user(bannati)
)
async def personal(client, message):
    username = message.from_user.username
    text = "Ecco un resoconto di statistiche che non so dove mettere:\nLivelli dei boss battuti:\n\n"

    try:
        totale = 0
        for b in sorted(list(player[username]["boss"])):
            lv = player[username]["boss"][b]
            totale += int(lv)
            text += f"{b} al livello {lv}\n"
        text += f"Totale: {totale} boss\n"
    except:
        text += "Nessun boss fatto!\n"    
    try:

        pat = player[username]["varie"]["pat"]
        cambi = player[username]["varie"]["cambi"]
        pesci = player[username]["varie"]["pesca"]
        pesca = player[username]["varie"]["pescatore"]
        trading = player[username]["varie"]["trade"]
        text += f"\nStatistiche animaletti:\nPat fatti: {pat}\nCambi fatti: {cambi}\n---------\nTrade fatti:{trading}\nPesci presi:{pesci}\nMissioni di pesca: {pesca}\n\n"
    except:
        pass
    
    nowcap = player[username]["cap"]
    try:
        cap = round(((player[username]["livello"]/2) + (player[username]["topP"]*2) + (player[username]["totali"]/1000) + (len(player[username]["obbiettivi"])/2) + (len(player[username]["bestiario"])/5) + (player[username]["grado"]/700)) * 20)
    except:
        cap = round(((player[username]["livello"]/2) + (player[username]["totali"]/1000) + (len(player[username]["obbiettivi"])/2) + (len(player[username]["bestiario"])/5)) * 20)
    
    pos = round((player[username]["livello"] + (player[username]["topP"]/2) + (len(player[username]["incantamenti"])/2))/5 )
    text  += f"Cap: {nowcap} punti su {cap} usabili\nLivello massimo equip: LV{pos}" 
    await app.send_message(message.chat.id,text)


@app.on_message(filters.command(["rimuovi", "rimuovi@NFTchallengebot", "r"]) & ~filters.user(bannati) & ~filters.chat(non_qui)
)
async def rimuovi(client, message):
    username = message.from_user.username
    user = player[username]
    scheda = user["scheda"]
    arma = scheda["arma"]
    prot = scheda["protezione"]
    scheda["Ap"] = "Base"
    
    scheda["set"] = None

    if len(message.command) == 1:
        nft.unequiP1(scheda, prot, protezioni)
        nft.unequiA(scheda, arma, armi)
        
        scheda["anello"] = None
        await app.send_message(message.chat.id,"Ora sei nudo!")
    else:
        if message.command[1].lower() in posA:
            
            nft.unequiA(scheda, arma, armi)
            await app.send_message(message.chat.id,"Arma riposta!")

        if message.command[1].lower() in posB:
            nft.unequiP1(scheda, prot, protezioni)
            await app.send_message(message.chat.id,"Protezione riposta!")


@app.on_message(filters.regex(r"^Switch 🪖")|filters.command(["switch", "switch@NFTchallengebot"]))
async def switch(client, message):
    togliere = list()
    username = message.from_user.username
    if username in trader["battaglieri"]:
        trader["battaglieri"].remove(username)
        await app.send_message(message.chat.id,"Sfide chiuse!")
    else:
        trader["battaglieri"].append(username)
        await app.send_message(message.chat.id,"Sfide aperte!")


@app.on_message(filters.command(["sfida", "sfida@NFTchallengebot"]) & filters.group & ~filters.user(bannati) & ~filters.chat(non_qui)
)
async def amichevole(client, message):
    username = message.from_user.username
    if message.reply_to_message != None:
        if username in list(inabilitati):

            await app.send_message(message.chat.id,"Non sei in grado di combattere!")
        else:
            sfidante = message.reply_to_message.from_user.username
            if username in trader["battaglieri"] and player[username]["notifiche"]["amichevoli"] == "si" and player[sfidante]["notifiche"]["amichevoli"] == "si":
                if player[username]["preso"] == True:

                    await app.send_message(message.chat.id,"Hai altre sfide in corso!")

                else:
                    
                    if username == sfidante or sfidante in list(inabilitati):
                        await app.send_message(message.chat.id,
                            "Probabilmente è successo qualcosa al tuo avversario..."
                        )
                    elif username != sfidante or sfidante not in list(inabilitati):
                        player[username]["preso"] = True

                        tempo = 35
                        nome1 = username
                        nome2 = sfidante
                        txt = f"Stai sfidando {sfidante}!\nHai {tempo} secondi per scegliere l'approccio!"
                        bottoni = list()
                        for appz in ["Base"] + liste.Approccini[player[nome1]["scheda"]["set"]]:
                            bottoni.append([InlineKeyboardButton(appz, callback_data=f"approzzi*{appz}_{sfidante}")])

                        reply_markup = InlineKeyboardMarkup(bottoni)

                        g = await app.send_message(nome1,txt, reply_markup=reply_markup)

                        txt = f"Sei stato sfidato da {username}!\nHai {tempo} secondi per scegliere l'approccio!"
                        bottoni = list()
                        for appz in ["Base"] + liste.Approccini[player[nome2]["scheda"]["set"]]:
                            bottoni.append([InlineKeyboardButton(appz, callback_data=f"approzzi*{appz}_{username}")])
                        reply_markup = InlineKeyboardMarkup(bottoni)
                        
                        if "Approcci" not in player[username]:
                            player[username]["Approcci"] = dict()
                        if "Approcci" not in player[sfidante]:
                            player[sfidante]["Approcci"] = dict()
                        
                        

                        try:

                            sesso = await app.send_message(
                                sfidante, txt, reply_markup=reply_markup
                            )
                        except:
                            pass

                        of = await app.send_message(message.chat.id,"Parte la sfida amichevole!")

                        await asyncio.sleep(10)
                        if username in player[sfidante]["Approcci"] and sfidante in player[username]["Approcci"]:
                            pass
                        else:
                            await asyncio.sleep(25)

                        user1 = copy.deepcopy(player[username]["scheda"])
                        if sfidante in player[username]["Approcci"]:
                            user1["Ap"] = player[username]["Approcci"][sfidante]
                            
                            if user1["Ap"] in liste.Approccini[player[username]["scheda"]["set"]] or user1["Ap"] == "Base":
                                pass
                            else:
                                user1["Ap"] = "Base"
                            try:
                                player[username]["Approcci"].pop(sfidante)
                            except:
                                pass
                        user2 = copy.deepcopy(player[sfidante]["scheda"])
                        if username in player[sfidante]["Approcci"]:
                            user2["Ap"] = player[sfidante]["Approcci"][username]
                            if user2["Ap"] in liste.Approccini[player[sfidante]["scheda"]["set"]] or user2["Ap"] == "Base":
                                pass
                            else:
                                user2["Ap"] = "Base"
                            try:
                                player[sfidante]["liste.Approcci"].pop(username)
                            except:
                                pass
                            
                        user1["incantamenti"] = nft.get_ench(player[username])
                        user2["incantamenti"] = nft.get_ench(player[sfidante])
                        
                        liste.approccio1 = user1["Ap"]
                        liste.approccio2 = user2["Ap"]
                        user1["fatto"] = 0
                        user2["fatto"] = 0
                        nft.classe(user1, user1["set"],liste.bonus)
                        nft.classe(user2, user2["set"],liste.bonus)
                        
                        
                        if user1["set"] == "Paladino":
                            user1["Scudo"] = 800
                        if user2["set"] == "Paladino":
                            user2["Scudo"] = 800
                        if user1["set"] == "Serial killer":
                            user2["hp"] = round(user2["hp"] * 0.75)
                        if user2["set"] == "Serial killer":
                            user1["hp"] = round(user1["hp"] * 0.75)

                        text = f"Sfida tra {nome1} e {nome2}!\n{nome1} sceglie: {liste.approccio1}, mentre {nome2} su {liste.approccio2}!\n\n"
                        if user1["anello"] == "Pegno di amicizia":
                            text += f"\nPartendo dal presupposto che {nome1} è un grande amico di {nome2}...\n"

                        if user2["anello"] == "Pegno di amicizia":
                            text += f"\nConsiderando che {nome2} è un grande amico di {nome1}...\n"

                        if user1["anello"] == "Fascette luminose":
                            text += f"\nEntra sul ring {nome1}!\n\n"
                        if user2["anello"] == "Pegno di amicizia":
                            text += f"\nE si presenta a noi {nome2}!\n\n"

                        if 0.2 > random.random() and "pet" in player[username]:
                            pet = player[username]["pet"]
                            text += f"\n{pet} fa il tifo per {nome1}!\n\n"
                            user1["hp"] += 1

                        if 0.2 > random.random() and "pet" in player[sfidante]:
                            pet = player[sfidante]["pet"]
                            text += f"\n{pet} fa il tifo per {nome2}!\n\n"
                            user2["hp"] += 1

                        
                        rip = 0
                        while True:
                            rip += 1

                            text += nft.turno(user2, user1)
                            if nft.is_dead(user1):
                                b = player[username]
                                a = player[sfidante]

                                break
                            if nft.is_dead(user2):
                                a = player[username]
                                b = player[sfidante]

                                break
                            text += nft.turno(user1, user2)
                            if nft.is_dead(user2):
                                a = player[username]
                                b = player[sfidante]

                                break
                            if nft.is_dead(user1):
                                b = player[username]
                                a = player[sfidante]

                                break

                            if rip == 150:
                                text += f"\nLa battaglia ha stremato {nome1}, che cade a terra sfinito!\n"
                                b = player[username]
                                a = player[sfidante]

                                break

                        nft.controllo_effetti_sfida(username,player)
                        nft.controllo_effetti_sfida(sfidante,player)

                        nome1 = a["scheda"]["Nome"]
                        nome2 = b["scheda"]["Nome"]

                        
                        if b["scheda"]["Nome"] == user1["Nome"]:

                            nomeperdente = user1["Nome"]
                            proccioperd = user1["Ap"]
                            vitarima = user2["hp"]
                            liste.approcciovin = user2["Ap"]
                            nomevincitore = user2["Nome"]
                            vitarima = user2["hp"]

                        else:
                            nomeperdente = user2["Nome"]
                            proccioperd = user2["Ap"]
                            vitarima = user1["hp"]
                            nomevincitore = user1["Nome"]
                            liste.approcciovin = user1["Ap"]

                        text += f"\nIl vincitore è quindi {nome1}, che batte {nome2}, dato che resta con {vitarima} hp."

                        nuovo = f"Vince {nome1}({liste.approcciovin})  in {rip} turni, battendo così {nome2} ({proccioperd}), dato che resta con {vitarima} hp."
                        player[username]["preso"] = False

                        try:
                            await g.edit(text)
                        except:
                            await g.delete()

                            chunk = nft.separatore(text)
                            for t in chunk:
                                await app.send_message(username, t)

                        try:

                            try:
                                await sesso.edit(text)
                            except:
                                await sesso.delete()
                                chunk = nft.separatore(text)
                                for t in chunk:
                                    await app.send_message(sfidante, t)

                        except:
                            pass
                        try:

                            try:
                                await of.edit(nuovo)
                            except:
                                await of.delete()
                                chunk = nft.separatore(nuovo)
                                for t in chunk:
                                    await app.send_message(message.chat.id,t)

                        except:
                            pass
            else:
                await message.reply("Sfide blocate!")
    else:
        await app.send_message(message.chat.id,"Rispondi al tuo bersaglio!")

@app.on_message(filters.command(["meka", "meka@NFTchallengebot"]) & filters.group & ~filters.user(bannati) & ~filters.chat(non_qui)
)
async def amichevole(client, message):
    username = message.from_user.username
    if message.reply_to_message != None:
        if username in list(inabilitati):

            await app.send_message(message.chat.id,"Non sei in grado di combattere!")
        else:
            sfidante = message.reply_to_message.from_user.username
            if username in trader["battaglieri"] and player[username]["notifiche"]["amichevoli"] == "si" and player[sfidante]["notifiche"]["amichevoli"] == "si":
                if player[username]["preso"] == True:

                    await app.send_message(message.chat.id,"Hai altre sfide in corso!")

                else:
                    
                    if username == sfidante or sfidante in list(inabilitati):
                        await app.send_message(message.chat.id,
                            "Probabilmente è successo qualcosa al tuo avversario..."
                        )
                    elif username != sfidante or sfidante not in list(inabilitati):
                        player[username]["preso"] = True

                        tempo = 35
                        nome1 = username
                        nome2 = sfidante
                        txt = f"Stai sfidando {sfidante}!\nHai {tempo} secondi per scegliere l'approccio!"
                        bottoni = list()
                        for appz in ["Base"] + liste.Approccini[player[nome1]["scheda"]["set"]]:
                            bottoni.append([InlineKeyboardButton(appz, callback_data=f"approzzi*{appz}_{sfidante}")])

                        reply_markup = InlineKeyboardMarkup(bottoni)

                        g = await app.send_message(nome1,txt, reply_markup=reply_markup)

                        txt = f"Sei stato sfidato da {username}!\nHai {tempo} secondi per scegliere l'approccio!"
                        bottoni = list()
                        for appz in ["Base"] + liste.Approccini[player[nome2]["scheda"]["set"]]:
                            bottoni.append([InlineKeyboardButton(appz, callback_data=f"approzzi*{appz}_{username}")])
                        reply_markup = InlineKeyboardMarkup(bottoni)
                        
                        if "Approcci" not in player[username]:
                            player[username]["Approcci"] = dict()
                        if "Approcci" not in player[sfidante]:
                            player[sfidante]["Approcci"] = dict()
                        
                        

                        try:

                            sesso = await app.send_message(
                                sfidante, txt, reply_markup=reply_markup
                            )
                        except:
                            pass

                        of = await app.send_message(message.chat.id,"Parte la sfida amichevole!")

                        await asyncio.sleep(5)
                        
                        user1 = copy.deepcopy(player[username]["scheda"])
                        if sfidante in player[username]["Approcci"]:
                            user1["Ap"] = player[username]["Approcci"][sfidante]
                            
                            if user1["Ap"] in liste.Approccini[player[username]["scheda"]["set"]] or user1["Ap"] == "Base":
                                pass
                            else:
                                user1["Ap"] = "Base"
                            try:
                                player[username]["Approcci"].pop(sfidante)
                            except:
                                pass
                        user2 = copy.deepcopy(player[sfidante]["scheda"])
                        if username in player[sfidante]["Approcci"]:
                            user2["Ap"] = player[sfidante]["Approcci"][username]
                            if user2["Ap"] in liste.Approccini[player[sfidante]["scheda"]["set"]] or user2["Ap"] == "Base":
                                pass
                            else:
                                user2["Ap"] = "Base"
                            try:
                                player[sfidante]["liste.Approcci"].pop(username)
                            except:
                                pass
                        
                        for k in ["hp","atk","def","int"]:
                            try:
                                user1[k] *= 1000
                                user2[k] *= 1000
                            except:
                                pass
                        user1["incantamenti"] = nft.get_ench(player[username])
                        user2["incantamenti"] = nft.get_ench(player[sfidante])
                        
                        liste.approccio1 = user1["Ap"]
                        liste.approccio2 = user2["Ap"]
                        user1["fatto"] = 0
                        user2["fatto"] = 0
                        nft.classe(user1, user1["set"],liste.bonus)
                        nft.classe(user2, user2["set"],liste.bonus)
                        
                        
                        if user1["set"] == "Paladino":
                            user1["Scudo"] = 800
                        if user2["set"] == "Paladino":
                            user2["Scudo"] = 800
                        if user1["set"] == "Serial killer":
                            user2["hp"] = round(user2["hp"] * 0.75)
                        if user2["set"] == "Serial killer":
                            user1["hp"] = round(user1["hp"] * 0.75)

                        text = f"Sfida MEKA tra {nome1} e {nome2}!\n"
                        if user1["anello"] == "Pegno di amicizia":
                            text += f"\nPartendo dal presupposto che {nome1} è un grande amico di {nome2}...\n"

                        if user2["anello"] == "Pegno di amicizia":
                            text += f"\nConsiderando che {nome2} è un grande amico di {nome1}...\n"

                        if user1["anello"] == "Fascette luminose":
                            text += f"\nEntra sul ring {nome1}!\n\n"
                        if user2["anello"] == "Pegno di amicizia":
                            text += f"\nE si presenta a noi {nome2}!\n\n"

                        if 0.2 > random.random() and "pet" in player[username]:
                            pet = player[username]["pet"]
                            text += f"\n{pet} fa il tifo per {nome1}!\n\n"
                            user1["hp"] += 1

                        if 0.2 > random.random() and "pet" in player[sfidante]:
                            pet = player[sfidante]["pet"]
                            text += f"\n{pet} fa il tifo per {nome2}!\n\n"
                            user2["hp"] += 1

                        
                        rip = 0
                        while True:
                            rip += 1

                            text += nft.turno(user2, user1)
                            if nft.is_dead(user1):
                                b = player[username]
                                a = player[sfidante]

                                break
                            if nft.is_dead(user2):
                                a = player[username]
                                b = player[sfidante]

                                break
                            text += nft.turno(user1, user2)
                            if nft.is_dead(user2):
                                a = player[username]
                                b = player[sfidante]

                                break
                            if nft.is_dead(user1):
                                b = player[username]
                                a = player[sfidante]

                                break

                            if rip == 150:
                                text += f"\nLa battaglia ha stremato {nome1}, che cade a terra sfinito!\n"
                                b = player[username]
                                a = player[sfidante]

                                break

                        nft.controllo_effetti_sfida(username,player)
                        nft.controllo_effetti_sfida(sfidante,player)

                        nome1 = a["scheda"]["Nome"]
                        nome2 = b["scheda"]["Nome"]

                        
                        if b["scheda"]["Nome"] == user1["Nome"]:

                            nomeperdente = user1["Nome"]
                            proccioperd = user1["Ap"]
                            vitarima = user2["hp"]
                            liste.approcciovin = user2["Ap"]
                            nomevincitore = user2["Nome"]
                            vitarima = user2["hp"]

                        else:
                            nomeperdente = user2["Nome"]
                            proccioperd = user2["Ap"]
                            vitarima = user1["hp"]
                            nomevincitore = user1["Nome"]
                            liste.approcciovin = user1["Ap"]

                        text += f"\nIl vincitore è quindi {nome1}, che batte {nome2}, dato che resta con {vitarima} hp."

                        nuovo = f"Vince {nome1}({liste.approcciovin})  in {rip} turni, battendo così {nome2} ({proccioperd}), dato che resta con {vitarima} hp."
                        player[username]["preso"] = False

                        try:
                            await g.edit(text)
                        except:
                            await g.delete()

                            chunk = nft.separatore(text)
                            for t in chunk:
                                await app.send_message(username, t)

                        try:

                            try:
                                await sesso.edit(text)
                            except:
                                await sesso.delete()
                                chunk = nft.separatore(text)
                                for t in chunk:
                                    await app.send_message(sfidante, t)

                        except:
                            pass
                        try:

                            try:
                                await of.edit(nuovo)
                            except:
                                await of.delete()
                                chunk = nft.separatore(nuovo)
                                for t in chunk:
                                    await app.send_message(message.chat.id,t)

                        except:
                            pass
            else:
                await message.reply("Sfide blocate!")
    else:
        await app.send_message(message.chat.id,"Rispondi al tuo bersaglio!")

@app.on_message( filters.private & ~filters.user(bannati) & (filters.regex(r"^Sfida ⚔️")| filters.command(["sfida"])))
async def sfida(client, message):
    for x in copy.deepcopy(inabilitati):
        await auto_check(x)
    
    username = message.from_user.username
    if username in list(inabilitati):
        await app.send_message(message.chat.id,"Non sei in grado di combattere!")
    elif player[username]["preso"] == True:
        await app.send_message(message.chat.id,"Sei in attesa che l'avversario scelga cosa fare....")
    elif username not in trader["battaglieri"]:
        await app.send_message(message.chat.id,"Hai le sfide chiuse!")
    else:
        for g in trader["attese"]:
            if (time.time() - trader["attese"][g]) >= 3600:
                trader["attese"][g] = time.time()
                try:
                    player[trader["erranti"][g]]["zaino"].pop(g)
                except:
                    pass
                
                chi = random.choice(list(player))
                print(f'{chi} riceve {g} da {trader["erranti"][g]}')
                trader["erranti"][g] = chi
                player[chi]["zaino"][g] = 1
                try:
                    await app.send_message(chi,f"Pare qualcuno abbia scordato un {g}!")
                except:
                    pass
            elif g == "Una copia dell'arte della guerra autografata" and (time.time() - trader["attese"][g]) >= 600:
                for k in inabilitati:
                    if inabilitati[k] == "Una copia dell'arte della guerra autografata":
                        inabilitati.pop(k)
                        try:
                            await app.send_message(k,f"Ti riprendi solo ora dalla botta!")
                        except:
                            pass
        
        player[username]["preso"] = True
        d = dict()
        x = 0
        prefe = False
        sfidante = None
        if len(trader["preferenziale"]) > 0:
            if username != trader["preferenziale"][0]:
                sfidante = trader["preferenziale"][0]
                trader["preferenziale"].pop(0)
        if sfidante == None:
            for tipo in player:
                if tipo not in trader["battaglieri"] or tipo in inabilitati:
                            pass
                else:
                    x += 1
                    d[tipo] = player[tipo]["oggi"] + player[tipo]["livello"]  + (player[tipo]["punti"]/3)
                    sort_orders = sorted(d.items(), key=lambda x: x[1], reverse=True)

            sfidante = nft.match(sort_orders, message.from_user.username)
        
        if sfidante in list(inabilitati):
                await app.send_message(message.chat.id,"Il tuo avversario è morto!")
                player[username]["preso"] = False
        else:
                
                if player[username]["prima"] == False:
                        player[username]["prima"] = True
                        player[username]["streak"] += 1
                        sfide = player[username]["streak"]
                        contentino = random.choice(tutto)
                        if 0.5 > random.random():
                            contentino = contentino.replace("LV0", "LV1")

                        elif 0.25 > random.random():
                            contentino = contentino.replace("LV0", "LV2")

                        else:
                            pass
                        nft.gestione_zaino(player[username]["zaino"],"add",contentino,1)
                        await app.send_message(message.chat.id,
                            f"Complimenti, sei a {sfide} giorni di sfide!\nIn regalo {contentino}!"
                        )
                tempo = 35
                if evento["mod"] ==  "calma":
                        tempo += 20
                if evento["mod"] ==  "sfide assurde":
                        tempo -= 7
                nome1 = username
                nome2 = sfidante
                if nome1 == nome2:
                    await app.send_message(message.chat.id,"Nessuno in vista!")
                    player[username]["preso"] = False
                else:
                    
                    
                    txt = f"Stai sfidando {sfidante}!\nHai {tempo} secondi per scegliere l'approccio!"
                    bottoni = list()
                    for appz in ["Base"] + liste.Approccini[player[nome1]["scheda"]["set"]]:
                            bottoni.append([InlineKeyboardButton(appz, callback_data=f"approzzi*{appz}_{sfidante}")])

                    reply_markup = InlineKeyboardMarkup(bottoni)

                    g = await app.send_message(nome1,txt, reply_markup=reply_markup)

                    txt = f"Sei stato sfidato da {username}!\nHai {tempo} secondi per scegliere l'approccio!"
                    bottoni = list()
                    for appz in ["Base"] + liste.Approccini[player[nome2]["scheda"]["set"]]:
                            bottoni.append([InlineKeyboardButton(appz, callback_data=f"approzzi*{appz}_{username}")])
                    reply_markup = InlineKeyboardMarkup(bottoni)
                        
                    if "liste.Approcci" not in player[username]:
                            player[username]["liste.Approcci"] = dict()
                    if "liste.Approcci" not in player[sfidante]:
                            player[sfidante]["liste.Approcci"] = dict()
                        
                    try:
                        sesso = await app.send_message(
                            sfidante, txt, reply_markup=reply_markup
                        )
                    except:
                        sesso = None
                    strader["sfide"][str(username) + str(time.time())] = {"a":username,"b":sfidante,"a_mess":g,"b_mess":sesso,"ora":time.time(),"tempo":tempo}



@app.on_message(filters.regex(r"^Pesca 🎣")|filters.command(["pesca", f"pesca@NFTchallengebot"]))
async def pesca(client, message):
    username = message.from_user.username
    if message.chat.type == "private" and player[username]["location"] != "Hub":
        if username not in pescaTORI:
            if username not in inabilitati:
                pescaTORI.append(username)
                attesa = random.randint(1, 2)
                await app.send_message(message.chat.id,
                    "Lanci la canna da pesca in acqua e aspetti un pesce!"
                )
                await asyncio.sleep(attesa)
                unix_time = time.time()
                reply_markup = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Pesca!", callback_data=("pescax " + str(unix_time))
                            )
                        ]
                    ]
                )

                await app.send_message(message.chat.id,
                    "Un pesce tira la lenza, presto!", reply_markup=reply_markup
                )
            else:
                await app.send_message(message.chat.id,"Sei troppo morto per pescare!")
        else:
            pass
    else:
        await app.send_message(message.chat.id,
            "Questo luogo è troppo affollato, i pesci scapperebbero."
        )




@app.on_callback_query(filters.regex("^pescax"))
async def pesca_callback(client, message):
    username = message.from_user.username
    if username in pescaTORI:
        pescaTORI.remove(username)
        orario_attuale = time.time()
        info = message.data
        orario = info.split()[1]
        orario_concesso = float(orario) + 3
        if orario_attuale < orario_concesso:
            PesoKg = random.randint(0, 55)
            PesoG = random.randint(0, 97)
            fs_w = 1
            scheda = player[username]["scheda"]
            try:
                arma = scheda["arma"]
                protezione = scheda["protezione"]
                listina = arma.split(" LV")
                coso = listina[0]
                listina2 = protezione.split(" LV")
                ricercato = listina2[0]
                if coso in item_pescatore:
                    fs_w += 1
                if ricercato in item_pescatore:
                    fs_w += 1
                if scheda["set"] == "Pescatore":
                    fs_w += 1
                if scheda["set"] == "Pescatore di balene":
                    fs_w += 2
                
                
            except:
                pass
            if trader["meteo"][player[username]["location"]] == "Pioggia":
                fs_w += 1
            if trader["meteo"][player[username]["location"]] == "Tempesta":
                fs_w += 2
            if trader["meteo"][player[username]["location"]] == "Caldo torrido":
                fs_w -= 1
            if trader["meteo"][player[username]["location"]] == "Caldo infernale":
                fs_w -= 2
            
            fs_w += random.randint(0,2)
            if fs_w <= 0:
                fs_w = 1
            if (fs_w == 6 and 0.03 > random.random()) or (fs_w == 7 and 0.05 > random.random()) or (fs_w >= 8 and 0.2 > random.random()):
                bossina = random.choice(["Kraken Nautico","Balena territoriale","Granchio da rave"])
                nome1 = username
                nome2 = bossina
                if 1 == 1:
                    if 1 == 1:
                        await message.message.delete()
                        try:
                            forza = player[username]["boss"][bossina]

                        except:
                            forza = 0
                        user1 = copy.deepcopy(player[username]["scheda"])
                        user1["incantamenti"] = nft.get_ench(player[username])
                        user2 = copy.deepcopy(liste.Nautici[bossina])
                        if user1["set"] == "Paladino":
                            user1["Scudo"] = 1000
                        if user1["set"] == "Serial killer":
                            user2["hp"] = round(user2["hp"] * 0.75)

                        nft.controllo_effetti_sfida(username,player)
                        bostabile = ["hp", "def", "atk", "agi"]
                        user1["fatto"] = 0
                        user2["fatto"] = 0
                        nft.classe(user1, user1["set"],liste.bonus)
                        for stat in bostabile:

                            user2[stat] = round(
                                user2[stat] + (user2[stat] * (forza / 35))
                            )
                        

                        liste.approccio1 = user1["Ap"]
                        liste.approccio2 = user2["Ap"]
                        user1["incantamenti"] = nft.get_ench(player[username])
                        user2["incantamenti"] = []
                        text = f"Sfida tra {nome1} e {nome2} lv {forza}, uno dei terribili boss!!\n{nome1} sceglie: {liste.approccio1}, mentre {nome2} su {liste.approccio2}!\n\n"
                        if player[username]["setta"]["benedizione"] == "Tartagura":
                            a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))                       
                            for stat in bostabile:
    
                                user1[stat] = round(
                                    user1[stat] + (user1[stat] * (a / 100))
                                )
                            text += "La setta ti potenzia!\n"
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

                                text += nft.turno(user2, user1)
                                if nft.is_dead(user1):
                                    b = "player"
                                    a = "Boss"

                                    break
                                elif nft.is_dead(user2):
                                    a = "player"
                                    b = "Boss"

                                    break
                                text += nft.turno(user1, user2)
                                if nft.is_dead(user2):
                                    a = "player"
                                    b = "Boss"

                                    break
                                elif nft.is_dead(user1):
                                    b = "player"
                                    a = "Boss"

                                    break

                            
                            if a == "Boss":

                                text += f"\nIl Boss lancia a terra {nome1} e scappa in mare, ci metterà un po a riprendersi!"
                                inabilitati[nome1] = time.time()

                                if (
                                    "Pesca grande ma poco fumo o arrosto"
                                    not in player[username]["obbiettivi"]
                                ):
                                    player[username]["obbiettivi"].append(
                                        "Pesca grande ma poco fumo o arrosto"
                                    )
                                    try:
                                        await app.send_message(
                                            username,
                                            "Obbiettivo completato!\n**Pesca grande ma poco fumo o arrosto**, hai perso da un boss marino, ma sai come si dice, meglio il pesce al fumo che l'arrosto oggi!",
                                        )
                                    except:
                                        pass

                            if a == "player":
                                if bossina == "Kraken Nautico":
                                    listina = [
                                        "Un dente di kraken LV0",
                                        "Uncino enorme LV0",
                                        "Delle squame viscide LV0"
                                    ]
                                if bossina == "Balena territoriale":
                                    listina = [
                                        "Dell'ambrosia", "Un eco-locatore"
                                    ]
                                if bossina == "Granchio da rave":
                                    listina = [
                                        "Corona del rave LV0",
                                        "Staffa da rave LV0",
                                        "Chela animata LV0"
                                    ]
                                
                                item = random.choice(listina).replace(
                                    "0",
                                    random.choice(
                                        [
                                            
                                            "0",
                                            "1",
                                            "1",
                                            "1",
                                            "2",
                                            "3",
                                        ]
                                    ),
                                )

                                nft.gestione_zaino(player[username]["zaino"],"add",item,1)

                                try:
                                    player[username]["gloria"] += round(
                                        10 + (10 * forza / 15)
                                    )
                                except:
                                    player[username]["gloria"] = round(
                                        10 + (10 * forza / 15)
                                    )

                                try:
                                    player[username]["boss"][bossina] += 1

                                except:
                                    player[username]["boss"][bossina] = 1

                                text += f"{nome1} batte il boss!\nAppena cade a terra coglie al volo la possibiltà e ruba {item} e gloria!"

                            messaggini = nft.separatore(text)
                            for mess in messaggini:
                                try:

                                    await app.send_message(username, mess)
                                except:
                                    pass
            else:
                pesce = liste.pesciame[player[username]["location"]][random.randint(0,min(fs_w,len(liste.pesciame[player[username]["location"]])-1))]
                testo = f"Hai preso uno splendido pesce {pesce}!\nPesa ben {PesoKg}.{PesoG}Kg!\nPoi lo liberi di nuovo perchè qui si vuole bene agli animali."
                if "Micro Pescatore" not in player[username]["obbiettivi"] and PesoKg <= 2:
                    player[username]["obbiettivi"].append("Micro Pescatore")
                    try:
                        await app.send_message(
                            username,
                            "Obbiettivo completato!\n**Micro Pescatore**, hai pescato un pesce minuscolo!",
                        )
                    except:
                        pass
                if "Macro Pescatore" not in player[username]["obbiettivi"] and PesoKg >= 52:
                    player[username]["obbiettivi"].append("Macro Pescatore")
                    try:
                        await app.send_message(
                            username,
                            "Obbiettivo completato!\n**Macro Pescatore**, hai pescato un pesce ENORME!",
                        )
                    except:
                        pass

                if "sacca" in player[username] and username in autorizzati:
                    try:

                        player[username]["sacca"][f"Pesce {pesce}"] += 1
                    except:
                        player[username]["sacca"][f"Pesce {pesce}"] = 1
                        
                if pesce in player[username]["bestiario"]:
                    if float(f"{PesoKg}.{PesoG}") > float(player[username]["bestiario"][pesce]):
                        testo += "\nNuovo record!"
                        player[username]["bestiario"][pesce] = f"{PesoKg}.{PesoG}"
                else:
                    testo += "\nNuovo pesce!"
                    player[username]["bestiario"][pesce] = f"{PesoKg}.{PesoG}"

            
                await app.edit_message_text(
                    chat_id=message.message.chat.id,
                    message_id=message.message.message_id,
                    text=testo,
                )
                if pesce == player[username]["richiesta_pescatore"]:
                    player[username]["richiesta_pescatore"] = None
                    premio = random.choice(premi_pescatore)
                    texto = f"Eccolo, lui è il pesce voluto dal pescatore!\nDato il tuo impegno vieni ricompensato con {premio}!"
                    nft.gestione_zaino(player[username]["zaino"],"add",premio,1)
                    try:
                        player[username]["varie"]["pescatore"] += 1
                    except:
                        player[username]["varie"]["pescatore"] = 1
                    player[username]["aigettoni"]["pesca"] += 1
                    if player[username]["aigettoni"]["pesca"] >= 3:
                        try:
                            player[username]["zaino"]["Gettone arena"] += 1
                        except:
                            player[username]["zaino"]["Gettone arena"] = 1
                            
                        player[username]["aigettoni"]["pesca"] = 0
                        texto += "\nE un gettone arena!"
                    
                    await app.send_message(username,texto)
                    
                try:
                    player[username]["varie"]["pesca"] += 1
                except:
                    player[username]["varie"]["pesca"] = 1
                
        else:
            try:
                await app.edit_message_text(
                    chat_id=message.message.chat.id,
                    message_id=message.message.message_id,
                    text="Il pesce è fuggito, peccato",
                )
            except:
                pass
    else:
        try:
            await app.edit_message_text(
                    chat_id=message.message.chat.id,
                    message_id=message.message.message_id,
                    text="Il pesce è fuggito, peccato",
                )
        except:
            pass


@app.on_message(filters.private & (filters.regex(r"^Assalto 📯")|filters.command("assalto")))
async def assalto(client, message):
    try:
        
        if player[message.from_user.username]["team"] != None:
            username = message.from_user.username
            user = player[username]
            if len(message.command) == 1:
                
                if clan[user["team"]]["inguerra"] != None:
                    chi = clan[user["team"]]["inguerra"]
                    testo = f"Sei attualmente in guerra con {chi}!\n"
                    for difesa in clan[user["team"]]["nemico"]:
                        finder = clan[user["team"]]["nemico"][difesa]
                        hp = finder["hp"]

                        lv = finder["lv"]
                        testo += f"-`{difesa}` LV{lv} ({hp}❤️)\n"

                    testo += f"Assaltalo tramite /assalto Nomestruttura"
                    await app.send_message(message.chat.id,testo)
                else:
                    await app.send_message(message.chat.id,"Siete in pace al momento!")
            else:

                other_time = last_assalto.get(username,1)
                elapsed = time.time() - other_time
                if username in nop:
                    elapsed -= 60
                if player[username]["setta"]["benedizione"] == 'Gufo':
                    a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
                    elapsed += a
                
                if elapsed > random.randint(25, 50):
                    if clan[user["team"]]["inguerra"] != None:
                        user = player[username]
                        arg = message.command[1:]
                        g = True
                        if "incarico" in clan[user["team"]]:
                            if username in clan[user["team"]]["incarico"]["partecipanti"]:
                                g = False
                        target = nft.listToString(arg)
                        if target in clan[user["team"]]["nemico"]:
                            target = [target]
                        else:
                            target = nft.search(clan[user["team"]]["nemico"], target)
                            
                        if len(target) == 1 and g:
                            if target[0] in clan[user["team"]]["nemico"]:
                                if username not in inabilitati:
                                    last_assalto[username] = time.time()
                                    if 1 == 1:

                                        nemico = clan[user["team"]]["nemico"]
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
                                        if matx < 2 and giocatore["set"] == 'Eroe caduto':
                                            serv += 2
                                            
                                        if giocatore["set"] == 'Eroe della rivolta':
                                            serv = serv * 1.2
                                        
                                        if player[username]["setta"]["benedizione"] == 'Orso polare' and  matx > 2:
                                            
                                            a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
                                            serv += (a/4)
                                        if player[username]["setta"]["benedizione"] == 'Kaimano' and  matx <= 2:
                                            a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
                                            serv += (a/4)
                                        
                                        bostabile = ["def", "atk", "agi"]
                                        for stat in bostabile:
        
                                            giocatore[stat] = round(giocatore[stat] + (giocatore[stat] * (serv / 12)))
                                            
                                        for struttura in nemico:
                                            if struttura not in clan[clan[user["team"]]["inguerra"]]["setting"]:
                                                clan[clan[user["team"]]["inguerra"]]["setting"][struttura] = liste.spec[x][0]
        
                                        nft.classe(giocatore,giocatore["set"], liste.bonus)
                                        
                                        output = nft.assedio(player,
                                            giocatore,
                                            nemico,
                                            target[0],
                                            user["team"],
                                            ordine,
                                            clan,
                                            trader["meteo"][player[username]["location"]],
                                            clan[clan[user["team"]]["inguerra"]]["setting"]
                                            
                                        )
                                        output += f"\n{matx} persone assaltano con te!"
                                        player[username]["aigettoni"]["assalti"] += 1
                                        if player[username]["aigettoni"]["assalti"] >= 80:
                                            try:
                                                player[username]["zaino"]["Gettone arena"] += 1
                                            except:
                                                player[username]["zaino"]["Gettone arena"] = 1
                                                
                                            player[username]["aigettoni"]["assalti"] = 0
                                            output += "\nA terra trovi un gettone arena!"
                                        
                                        nft.controllo_effetti_assalto(username,player)
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
                                            await app.send_message(message.chat.id,output)
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
                                            
                                            for appz in [target[0]]:
                                                bottoni.append([InlineKeyboardButton("Ancora!", callback_data=f"ancora_{appz}")])
                                            reply_markup = InlineKeyboardMarkup(bottoni)
                                            await app.send_message(message.chat.id,output,reply_markup=reply_markup)
                                            
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
                                            if (
                                                "Fra, fatti una vita" not in player[username]["obbiettivi"]
                                                and clan[user["team"]]["danno"][username]
                                                >= 100000
                                            ):
                                                player[username]["obbiettivi"].append("Fra, fatti una vita")
                                                try:
                                                    await app.send_message(
                                                        username,
                                                        "Obbiettivo completato!\n**Fra, fatti una vita**, sei stato fortissimo in assalto, ma chiedi aiuto a qualcuno",
                                                    )
                                                except:
                                                    pass
                                            

                                else:
                                    await app.send_message(message.chat.id,"Devi ancora rimetterti!")
                            else:
                                await app.send_message(message.chat.id,"Bersaglio non disponibile!")
                        else:
                            await app.send_message(message.chat.id,"Bersaglio non disponibile!")
                    else:
                        await app.send_message(message.chat.id,"Siete in pace!")
                else:
                    await app.send_message(message.chat.id,"Un attimo!")
        else:
            await app.send_message(message.chat.id,f"Non è ora di usare questo comando, fai altro!")
    except :
        
        if player[message.from_user.username]["team"] != None:
            username = message.from_user.username
            user = player[username]
            if user["team"] != "nessuno":
                if clan[user["team"]]["inguerra"] != None:
                    chi = clan[user["team"]]["inguerra"]
                    testo = f"Sei attualmente in guerra con {chi}!\n"
                    for difesa in clan[user["team"]]["nemico"]:
                        finder = clan[user["team"]]["nemico"][difesa]
                        hp = finder["hp"]

                        lv = finder["lv"]
                        testo += f"-`{difesa}` LV{lv} ({hp}❤️)\n"

                    testo += f"Assaltalo tramite /assalto Nomestruttura"
                    await app.send_message(message.chat.id,testo)
                else:
                    await app.send_message(message.chat.id,"Siete in pace al momento!")
            else:
                await app.send_message(message.chat.id,"Non hai un clan!")


traders = ["Accetta", "Passo."]
last_boss = dict()
last_dungeon = dict()

@app.on_message(filters.private & ~filters.user(bannati) & (filters.regex(r"^Pescatore 🎣")|filters.command(["pescatore"]))
)
async def pescatore(client, message):
    username = message.from_user.username
    if "richiesta_pescatore" in player[username]:
        chiede = player[username]["richiesta_pescatore"]
        if chiede != None:
            text = f"Hey {username}, sono io, il pescatore!\nAvrei bisogno di te per un lavoretto,ci stai?\nMi servirebbe un {chiede}, guarda che pago bene!"
        else:
            text = "Scusa ma per ora sto apposto così!"
    else:
        text = "Non mi fido ancora di te..."
    await app.send_message(message.chat.id,text)

@app.on_callback_query()
async def logger(client, message):
    username = message.from_user.username
    scelta = message.data
    other_time = last_sms.get(username,1)
            
    now = time.time()
            
    elapsed = now - other_time
    g = time.ctime(now)
    if elapsed > 0.15:
        dist = int(elapsed)
        print(f"{username} - {scelta} [{g}]({dist})")
        last_sms[username] = now
        raise ContinuePropagation
    else:
        await message.answer("Con calma...")

@app.on_callback_query(~ filters.user(bannati))
def check_spe(client,message):
    if list(player[message.from_user.username].get("spedizione",[False])) == [True] or list(player[message.from_user.username].get("spedizione",[False])) == ["true"]:
        message.message.edit("Sei in giro, non puoi!")
    else:
        raise ContinuePropagation



@app.on_callback_query(filters.regex("dungi_") )
async def dungeon_hub(client, message):
    username = message.from_user.username
    scelta = message.data
    scelta = scelta.replace("dungi_","")
    for x in copy.deepcopy(inabilitati):
        await auto_check(x)
    
    if "dungeon" in player[username]:
        if username in list(inabilitati):
            await message.message.edit(text="Non sei in grado di entrare nel dungeon!")
        else:
            if scelta in liste.nemici:
                await nft.dungeon_mostro(app, message,player,scelta,nop,username,evento,last_dungeon,liste.nemici,inabilitati,trader)
            elif scelta in liste.scelte or scelta in liste.stanze:
                await nft.dungeon_stanze(app, message,player,scelta,nop,username,evento,last_dungeon,globali,inabilitati,liste.scelte,tutto,tuttov,megaman,zombie,gungeon,magic,protezioni,armi,trader)
            elif "Affronta" in scelta:

                await nft.dungeon_boss(app, message,player,scelta,nop,username,evento,last_dungeon,inabilitati,tuttov)
            
    
@app.on_callback_query(~filters.user(bannati) & filters.regex("arena"))
async def arena_hub(client, message):
    username = message.from_user.username
    scelta = message.data
    
    if "arena" in player[username]:
            other_time = last_arena.get(username,1)
            elapsed = time.time() - other_time
            if elapsed > 0.5:
                if scelta.split("_")[1] == "Entra" and ("Gettone arena" in player[username]["zaino"] or player[username]["arenagratis"] == True):
                    if player[username]["arenagratis"] != True:
                        player[username]["arena"]["arenagratis"] = False
                        player[username]["zaino"]["Gettone arena"] -= 1
                        if player[username]["zaino"]["Gettone arena"] == 0:
                            player[username]["zaino"].pop("Gettone arena")
                    else:
                        player[username]["arena"]["arenagratis"] = True
                        player[username]["arenagratis"] = False
                        
                    await nft.arena(client,app, message,player,scelta.split("_")[1], armi, protezioni,armieprot,liste.Approcci,liste.classi,trader,username)
                    last_arena[username] = time.time()
                else:
                    if scelta.split("_")[1] == "Poi":
                        player[username].pop("arena")
                        await message.message.edit("Esci dall'arena, sarà per un altra volta")
                    elif scelta.split("_")[1] != "Entra":
                        await nft.arena(client,app, message,player,scelta.split("_")[1], armi, protezioni,armieprot,liste.Approcci,liste.classi,trader,username)
                        last_arena[username] = time.time()
                    else:
                        player[username].pop("arena")
                        await message.message.edit("Non possiedi gettoni arena e/o non hai una corsa gratis oggi!")
            else:
                try:
                    await message.answer("Spe")
                except:
                    pass
    else:
        await message.message.delete()
  

@app.on_callback_query(~filters.user(bannati) & filters.regex("^ancora"))
async def rissona(clinet,message):
    scelta = message.data.split("_")[1]
    await nft.riassalto(scelta,message.from_user.username,message,trader,clan,app,player,last_assalto,inabilitati)

@app.on_callback_query(~filters.user(bannati) & filters.regex("^negozio"))
async def rissona(clinet,message):
    scelta = message.data.split("_")[1]
    await nft.shoping(scelta,player,message.from_user.username,app,message)
      
@app.on_callback_query(~filters.user(bannati) & filters.regex("rissa_"))
async def rissona(clinet,message):
    scelta = message.data.split("_")[1]
    await nft.gestione_risse(message,app,trader,mediotourizzati,player,scelta,message.from_user.username)

@app.on_callback_query(~filters.user(bannati) & filters.regex("spedizione_"))
async def rissona(clinet,message):
    await nft.make_party_inline(message.data,player,message.from_user.username,clan,message,app)

@app.on_callback_query(~filters.user(bannati) & filters.regex("inca_"))
async def rissona(clinet,message):
    scelta = message.data.split("_")[1]
    await nft.incarico(scelta,player,message.from_user.username,clan,message,app)

@app.on_callback_query(~filters.user(bannati) & filters.regex("suggerisci*"))
async def rissona(clinet,message):
    scelta = message.data.split("*")[1]
    await nft.suggerimenti_inline(scelta,message.from_user.username,message,trader,app)

@app.on_callback_query(~filters.user(bannati) & filters.regex("sposto_"))
async def rissona(clinet,message):
    scelta = message.data.split("_")[1]
    await nft.muoveeere(scelta,liste.location,player,message,app, message.from_user.username,trader)

@app.on_callback_query(~filters.user(bannati) & filters.regex("Traffi_"))
async def rissona(clinet,message):
    scelta = message.data.split("_")[1]
    await nft.commerciante_inline(scelta,player,message.from_user.username,app,message)

@app.on_callback_query(~filters.user(bannati) & filters.regex("Aiuto"))
async def rissona(clinet,message):
    chi = message.message.text.split(" ")[0]
    player[chi]["supporto"] = copy.deepcopy(player[message.from_user.username]["scheda"])
    esito = f"{message.from_user.username} si propone volontario!"
    await app.edit_message_text(
            chat_id=message.message.chat.id,
            message_id=message.message.message_id,
            text=esito,
        )
    await message.answer("GOOO")

@app.on_callback_query(~filters.user(bannati) & filters.regex("reg_"))
async def rissona(clinet,message):
    scelta = message.data.split("_")[1]
    await nft.regale(regali,scelta,message.from_user.username,player,app,message)


@app.on_callback_query(~filters.user(bannati) & filters.regex("ordine_"))
async def rissona(clinet,message):
    scelta = message.data.split("_")[1]
    await nft.riordino(scelta,clan,message.from_user.username,app,message,player)
    
@app.on_callback_query(~filters.user(bannati) & filters.regex("nucleo_"))
async def rissona(clinet,message):
    scelta = message.data.split("_")[1]
    await nft.nucealte(scelta,player,message.from_user.username,message,clan)

@app.on_callback_query(~filters.user(bannati) & filters.regex("bossveri_"))
async def rissona(clinet,message):
    scelta = message.data.split("_")[1]
    await nft.bossata(scelta,player,message.from_user.username,app,message,last_boss,inabilitati,armi,trader)

@app.on_callback_query(~filters.user(bannati) & filters.regex("notifiche_"))
async def rissona(clinet,message):
    scelta = message.data.split("_")[1]
    await nft.cambio_not(scelta,player,message.from_user.username,app,message)


@app.on_callback_query(~filters.user(bannati) & filters.regex("approzzi*"))
async def rissona(clinet,message):
    scelta = message.data.split("*")[1]
    await nft.cambio_approccio(scelta,player,message.from_user.username,app,message)
    
    
@app.on_callback_query(~filters.user(bannati) & filters.regex("nomina?"))
async def rissona(clinet,message):
    scelta = message.data.split("?")
    
    if len(scelta) == 2:
        clang = clan[player[message.from_user.username]["team"]]
        bottoni = list()
        for g in clang["membri"]:
            bottoni.append(
                [InlineKeyboardButton(g, callback_data=f"nomina?{scelta[1]}?{g}")]
                )
        reply_markup = InlineKeyboardMarkup(bottoni)
        text = f"Chi vuoi rendere {scelta[0]}?"
        await message.message.edit( text, reply_markup=reply_markup)
    else:
        clan[player[message.from_user.username]["team"]][scelta[1]] = scelta[2]
        text = f"Da ora {scelta[1]} è {scelta[2]}."
        await message.message.edit( text)

@app.on_callback_query(~filters.user(bannati) & filters.regex("guerro_"))
async def guerria(clinet,message):
    scelta = message.data.split("_")[1]
    username = message.from_user.username
    user = player[username]
    if user["team"] != "nessuno":
        if clan[user["team"]]["Creatore"] == username:
            if clan[user["team"]]["inguerra"] == None:
                if 1 == 1:
                    ggh = list()
                    for g in clan[user["team"]]["membri"]:
                        ggh.append(player[g]["guerrieggiato"])
                    if clan[user["team"]]["cariche"] > 0 and all(i < 2 for i in ggh):
                        clan[user["team"]]["cariche"] -= 1
                        clan[user["team"]]["inizio"] = time.time()
                        cl = user["team"]
                        oppo = scelta
                        print(cl,oppo)
                        clan[cl]["danno"] = dict()
                        clan[cl]["inguerra"] = oppo
                        clan[cl]["nemico"] = copy.deepcopy(clan[oppo]["villaggio"])
                        clan[cl]["comparo"] = list(clan[oppo]["villaggio"])
                        clan[cl]["orderN"] = list(clan[oppo]["order"])

                        if "setting" in clan[scelta]:
                                pass
                        else:
                            clan[scelta]["setting"] = dict()
                        
                        for x in list(liste.order):    
                            if x not in clan[scelta]["setting"]:                        
                                o = clan[scelta]["setting"].get(x,liste.spec[x][0])
                                clan[scelta]["setting"][x] = o
                        
                        if "Clone" in clan[oppo]["villaggio"]:
                            try:
                                clan[cl]["nemico"]["Clone"]["atk"] = player[clan[oppo]["Sacrificio"]][
                                    "scheda"
                                ]["atk"]
                                clan[cl]["nemico"]["Clone"]["def"] = player[clan[oppo]["Sacrificio"]][
                                    "scheda"
                                ]["def"]
                                clan[cl]["nemico"]["Clone"]["agi"] = player[clan[oppo]["Sacrificio"]][
                                    "scheda"
                                ]["agi"]
                            except:
                                pass

                        try:
                            await app.send_message(
                                clan[oppo]["Creatore"], f"Il vostro villaggio è in assalto da {cl}!"
                            )
                        except:
                            pass
                        bandiera = ""
                        if "Bandiera" in clan[oppo]:
                            for riga in clan[oppo]["Bandiera"]:
                                bandiera += nft.listToString(riga) + "\n"
                        
                        for x in list(liste.order):
                            o = clan[oppo]["setting"].get(x,liste.spec[x][0])
                            clan[oppo]["setting"][x] = o
                        
                        for membro in clan[cl]["membri"]:
                            try:

                                await app.send_message(
                                    membro,
                                    f"All'orizzonte si erge la bandiera di {oppo}\n{bandiera}\nVEDETE BENE DI FARLA CADERE!\nSarete così ricompensati con la gloria ed il potere!",
                                )
                            except:
                                pass
                            
                        
                        trader["ricerca"] = cl
                    else:
                        await message.message.edit("Uno o più utenti del tuo clan sono stanchi!")                 
            else:
                await message.message.edit("Devi finire la guerra!")
        else:
            await message.message.edit("Solo il capo può farlo!")
    else:
        await message.message.edit("Ti manca un clan")


@app.on_callback_query(~filters.user(bannati) & filters.regex("pvp_"))
async def duello_i(clinet,message):
    scelta = message.data.split("_")[1]
    username = message.from_user.username
    
    if "duello" in player[username]:
        if player[username]["duello"] in duelli:
            keyboardAttacco = InlineKeyboard()
            keyboardAttacco.row(InlineKeyboardButton('Attacca', 'pvp_attacco'))
            
            
            

            keyboardDifesa = InlineKeyboard()
            keyboardDifesa.row(InlineKeyboardButton('Stordisci', 'pvp_tempo'))
            
            duellox = duelli[player[username]["duello"]]
            text = message.message.text.html
            text += "\n\n"
            if scelta == "attacco":
                if username == duellox["a"]:
                    sfidante = duellox["b"]
                    user1 = copy.deepcopy(player[username]["scheda"])
                    user2 = copy.deepcopy(player[sfidante]["scheda"])
                    user1["incantamenti"] = nft.get_ench(player[username])
                    user2["incantamenti"] = nft.get_ench(player[sfidante]) 
                    if "Impatto" in duellox:
                        if "Primo impatto" in user1["incantamenti"]:
                            user1["incantamenti"].remove("Primo impatto")
                        if "Primo impatto" in user2["incantamenti"]:
                            user2["incantamenti"].remove("Primo impatto")
                    else:
                        duellox["Impatto"] = True
                    
                    user1["fatto"] = duellox["afatto"]
                    user2["fatto"] = duellox["bfatto"]
                    nft.classe(user1, user1["set"],liste.bonus)
                    nft.classe(user2, user2["set"],liste.bonus)
                    
                    basi = {"a":{},"b":{}}
                    
                    for h in ["def", "atk", "agi"]:
                            basi["a"][h] = user1[h]
                            user1[h] += duellox["abonus"][h]             

                            basi["b"][h] = user2[h]
                            user2[h] += duellox["bbonus"][h]
                    
                    for h in duellox["aaltro"]:
                        user1[h] = duellox["aaltro"][h]
                    
                    for h in duellox["baltro"]:
                        user2[h] = duellox["baltro"][h]
                    
                    
                    
                    inizioa = user1["hp"]
                    iniziob = user2["hp"]
                    user1["hp"] -= duellox["adanno"]
                    
                    user2["hp"] -= duellox["bdanno"]
                    
                    eventzo = ""
                    
                    text += nft.turno(user1, user2,eventzo)
                    
                    duellox["baltro"] = dict()
                    duellox["aaltro"] = dict()
                    for j in user1:
                        if j not in ['Nome', 'hp', 'def', 'atk', 'agi', 'int', 'Ap', 'schivato', 'anello', 'protezione', 'arma', 'boost', 'set',"fatto","incantamenti"]:
                            duellox["aaltro"][j] = user1[j]
                   
                    for j in user2:
                        if j not in ['Nome', 'hp', 'def', 'atk', 'agi', 'int', 'Ap', 'schivato', 'anello', 'protezione', 'arma', 'boost', 'set',"fatto","incantamenti"]:
                            duellox["baltro"][j] = user2[j]
                    
                    for h in ["def", "atk", "agi"]:
                        duellox["abonus"][h] = user1[h] -basi["a"][h]           
                    
                        duellox["bbonus"][h] =  user2[h] - basi["b"][h]
                    
                    
                
                    duellox["afatto"] = user1["fatto"]
                    duellox["bfatto"] = user2["fatto"]
                    duellox["adanno"] = user1["hp"] - inizioa
                    duellox["bdanno"] = user2["hp"] - iniziob
                    
                if username == duellox["b"]:
                    sfidante = duellox["a"]
                    
                    user1 = copy.deepcopy(player[username]["scheda"])
                    user2 = copy.deepcopy(player[sfidante]["scheda"])
                    user1["incantamenti"] = nft.get_ench(player[username])
                    user2["incantamenti"] = nft.get_ench(player[sfidante]) 
                    user1["fatto"] = duellox["bfatto"]
                    user2["fatto"] = duellox["afatto"]
                    nft.classe(user1, user1["set"],liste.bonus)
                    nft.classe(user2, user2["set"],liste.bonus)
                    iniziob = user1["hp"]
                    inizioa = user2["hp"]
                    if "Impatto" in duellox:
                        if "Primo impatto" in user1["incantamenti"]:
                            user1["incantamenti"].remove("Primo impatto")
                        if "Primo impatto" in user2["incantamenti"]:
                            user2["incantamenti"].remove("Primo impatto")
                    else:
                        duellox["Impatto"] = True
                    basi = {"a":{},"b":{}}
                    
                    for h in ["def", "atk", "agi"]:
                            basi["b"][h] = user1[h]
                            user1[h] += duellox["bbonus"][h]
                    
                    for h in ["def", "atk", "agi"]:
                            basi["a"][h] = user2[h]
                            user2[h] += duellox["abonus"][h]
                            
                    for h in duellox["baltro"]:
                        user1[h] = duellox["baltro"][h]
                    
                    for h in duellox["aaltro"]:
                        user2[h] = duellox["aaltro"][h]
                    
                    
                    user1["hp"] -= duellox["bdanno"]
                    
                    user2["hp"] -= duellox["adanno"]
                    
                    eventzo = ""
                    
                    text += nft.turno(user1, user2,eventzo)
                    duellox["baltro"] = dict()
                    duellox["aaltro"] = dict()
                    for j in user2:
                        if j not in ['Nome', 'hp', 'def', 'atk', 'agi', 'int', 'Ap', 'schivato', 'anello', 'protezione', 'arma', 'boost', 'set',"fatto","incantamenti"]:
                            duellox["aaltro"][j] = user2[j]
                    
                    for j in user1:
                        if j not in ['Nome', 'hp', 'def', 'atk', 'agi', 'int', 'Ap', 'schivato', 'anello', 'protezione', 'arma', 'boost', 'set',"fatto","incantamenti"]:
                            duellox["baltro"][j] = user1[j]
                    
                    for h in ["def", "atk", "agi"]:
                        duellox["bbonus"][h] = user1[h] - basi["b"][h]
                    
                    for h in ["def", "atk", "agi"]:
                        duellox["abonus"][h] =  user2[h] - basi["a"][h]
                    
                    
                    duellox["bfatto"] = user1["fatto"]
                    duellox["afatto"] = user2["fatto"]
                    duellox["adanno"] = user2["hp"] - inizioa
                    duellox["bdanno"] = user1["hp"] - iniziob
                
                if len(text) >= 1000:
                    text = text[600:]
                    if len(text) >= 3200:
                        text = text[1000:]
                    
                
                if username == duellox["b"]:
                        if duellox["bdanno"] <= player[duellox["b"]]["scheda"]["hp"]:
                            await app.edit_message_text(duellox["b"],duellox["bmess"],text,reply_markup=keyboardDifesa)
                            await app.edit_message_text(duellox["a"],duellox["amess"],text,reply_markup=keyboardAttacco)
                        else:
                            text += f'E vince così {duellox["a"]}!'
                            await app.edit_message_text(duellox["b"],duellox["bmess"],text)
                            await app.edit_message_text(duellox["a"],duellox["amess"],text)
                            duelli.pop(player[username]["duello"])
                else:
                    if duellox["adanno"] <= player[duellox["a"]]["scheda"]["hp"]:
                        await app.edit_message_text(duellox["a"],duellox["amess"],text,reply_markup=keyboardDifesa)
                        await app.edit_message_text(duellox["b"],duellox["bmess"],text,reply_markup=keyboardAttacco)
                    else:
                        text += f'E vince così {duellox["b"]}!'
                        await app.edit_message_text(duellox["a"],duellox["amess"],text)
                        await app.edit_message_text(duellox["b"],duellox["bmess"],text)
                        duelli.pop(player[username]["duello"])
                duellox["tempo"] = time.time()
            
            elif scelta == "tempo":
                if time.time() - duellox["tempo"] >= 60:
                    if username == duellox["b"]:
                        await app.edit_message_text(duellox["a"],duellox["amess"],text,reply_markup=keyboardDifesa)
                        await app.edit_message_text(duellox["b"],duellox["bmess"],text,reply_markup=keyboardAttacco)
                    else:
                        await app.edit_message_text(duellox["b"],duellox["bmess"],text,reply_markup=keyboardDifesa)
                        await app.edit_message_text(duellox["a"],duellox["amess"],text,reply_markup=keyboardAttacco)
                    duellox["tempo"] = time.time()
                else:
                    await message.answer("Spe...")
        else:
            await message.message.delete()
    else:
        await message.message.delete()

@app.on_callback_query(~filters.user(bannati) & filters.regex("setta_"))
async def rissona(clinet,message):
    scelta = message.data.split("_")[1]
    username = message.from_user.username
    if scelta == "Non accetto":
        await message.message.edit("Chiaro, sarà per un altra volta...")
    else:
        loc = player[username]["location"]
        a = round(trader["sette"][loc]["power"] * (trader["sette"][loc]["%"]/100))
        if player[username]["setta"]["benedizione"] != None:
            trader["sette"][player[username]["setta"]["loc"]]["iscritti"] -= 1
        trader["sette"][loc]["iscritti"] += 1
        txt = trader["sette"][loc]["Bonus"].format(a)
        nome = trader["sette"][loc]["Nome"]
        player[username]["setta"] = {"loc":loc,"benedizione":nome,"libero":False}
        await message.message.edit(f"Ti sei affiliato alla setta del {nome}!\n{txt}")

@app.on_callback_query(~filters.user(bannati) & filters.regex("dmando_"))
async def rissona(clinet,message):
    scelta = message.data.split("_")[1]
    if message.from_user.username in domande:
        if float(scelta) == domande[message.from_user.username]["corretta"]:
            test = "Corretto!\n"
            try:
                player[message.from_user.username]["domande"] += 1
            except:
                player[message.from_user.username]["domande"] = 1
        else:
            test = f"Sbagliato, era {domande[message.from_user.username]['corretta']}\n"
        
        f = nft.domandami(3,5,20)        
        test += f["text"]
        domande[message.from_user.username] = f
        bottoni = list()
        for appz in f["Risposte"]:
            bottoni.append([InlineKeyboardButton(appz, callback_data=f"dmando_{appz}")])

        reply_markup = InlineKeyboardMarkup(bottoni)
        
        await message.message.edit(test,reply_markup=reply_markup)
    else:
        await message.message.delete()

@app.on_callback_query(~filters.user(bannati) & filters.regex("villo_"))
async def villaggio(clinet,message):
    scelta = message.data.split("_")[1]
    username = message.from_user.username
    user = player[username]
    team = user["team"]
    
    if team != "nessuno":
        if scelta == "dettagli":
            text = "Schermata di dettagli tecnici:\n"
            bottoni = list()
            
            for g in clan[team]["villaggio"]:
                text += f"**{g}**\n"
                
                if clan[team]["villaggio"][g]["lv"] >= 5:
                    if "setting" in clan[team]:
                        pass
                    else:
                        clan[team]["setting"] = dict()
                    status = clan[team]["setting"].get(g,liste.spec[g][0])
                    clan[team]["setting"][g] = status
                    cagat = liste.frasispec[status]
                    text += f"{status}:\n{cagat}\n\n"
                    bottoni.append([InlineKeyboardButton(g, callback_data=f"villo_{g}_{status}")])
                else:
                    text += "Serve portare la struttura al lv 5 per le specializzazioni!\n\n"
            bottoni.append([InlineKeyboardButton("Indietro", callback_data=f"villo_indietro")])
            reply_markup = InlineKeyboardMarkup(bottoni)
            if clan[user["team"]]['Architetto'] == username:
                
                text += "Quale struttura vuoi modificare?"
                await message.message.edit(text,reply_markup =reply_markup)
            else:
                reply_markup2 = [[InlineKeyboardButton("Indietro", callback_data=f"villo_indietro")]]
                reply_markup2 = InlineKeyboardMarkup(reply_markup2)
                await message.message.edit(text,reply_markup =reply_markup2)
                
        elif scelta == "indietro":
            user = player[username]
            team = user["team"]
            if team != "nessuno":
                    try:

                        massimo = 5 + round(
                            clan[team]["villaggio"]["Accampamento"]["lv"] // 2
                        )
                    except:
                        massimo = 5
                    adesso = len(clan[team]["membri"])

                    testo = f"Villaggio del party {team}!\nEroi ({adesso}/{massimo}):\n"
                    for cittadino in clan[user["team"]]["membri"]:
                        try:
                            if clan[user["team"]]["inguerra"] == None:
                                potenza = player[cittadino]["punti"]
                            else:
                                try:
                                    potenza = clan[user["team"]]["danno"][cittadino]
                                except:
                                    potenza = "Non ha ancora attaccato!"
                            testo += f"-**{cittadino}** - {potenza}"
                            if cittadino in trader["battaglieri"]:
                                testo += " ⚔️"
                            if cittadino == clan[user["team"]]["Architetto"]:
                                testo += " 📐"
                            if cittadino == clan[user["team"]]["Gestore"]:
                                testo += " 🗝️"
                            if cittadino == clan[user["team"]]["Sarto"]:
                                testo += " 🧵"
                            if cittadino == clan[user["team"]]["Sacrificio"]:
                                testo += " 🩸"
                            if cittadino in inabilitati:
                                testo += " ⚰️"

                            testo += " " + liste.moji_posto[player[cittadino]["location"]]
                        except:
                            testo += f"-{cittadino} - non trovato!"
                        testo += "\n"
                    testo += "\nDifese:\n"
                    for difesa in clan[user["team"]]["order"]:

                        if difesa in clan[user["team"]]["villaggio"]:
                            finder = clan[user["team"]]["villaggio"][difesa]
                            hp = finder["hp"]

                            lv = finder["lv"]
                            testo += f"-{difesa} LV{lv} ({hp}❤️)\n"

                    potere = clan[user["team"]]["potere"]
                    inguerra = clan[user["team"]]["inguerra"]
                    potrebbero = str(clan[user["team"]]["cariche"])
                    if potrebbero != 0 and inguerra == None:
                        potrebbero += "\nInizia subito una guerra con /guerra!"
                    ini = str(time.ctime(clan[user["team"]]["inizio"]))[3:]
                    testo += f"Altre statistiche:\n -{potere} potere \n-Guerre possibili questa settimana: {potrebbero}\n-In guerra con {inguerra}\n-Inizio ultima guerra: {ini}\nUsa /clan help per tutti i comandi! \nPuoi migliorare o comprare strutture usando /clan Negozio!"
                    if "nucleo" in clan[user["team"]]:
                        nucleo = clan[user["team"]]["nucleo"]
                        testo += f"\n{nucleo} attivato!"
                    
                    bottoni = [InlineKeyboardButton(text="Dettagli", callback_data="villo_dettagli")]
                    reply_markup = InlineKeyboardMarkup([bottoni])
                    await message.message.edit(testo,reply_markup=reply_markup)
        
        elif scelta in clan[team]["villaggio"]:
            if clan[team]["villaggio"][scelta]["lv"] >= 5:
                fase = message.data.split("_")[2]
                fase = liste.spec[scelta].index(fase)
                nes =fase + 1
                try:
                    fase = liste.spec[scelta][nes]
                except:
                    fase = liste.spec[scelta][0]
                    nes = 0
                clan[team]["setting"][scelta] = fase
                cagata = liste.frasispec[fase]
                await message.message.edit(f"{scelta} cambia abilità in {fase}\n{cagata}")
            else:
                await message.message.edit("Serve portare la struttura al lv 5 per le specializzazioni!")
        else:
            await message.message.edit("Non questa struttura in clan")
    else:
        await message.message.edit("Non hai un clan")



gc.collect()
sched.start()
app.start()
cestino.start()
idle()

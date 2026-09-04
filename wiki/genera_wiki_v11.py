#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wiki v11: guida leggibile e completa per tutte le stanze dungeon."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import genera_wiki_v10 as v10

ROOT = v10.ROOT
v9 = v10.v9
v8 = v10.v8
v7 = v10.v7
v6 = v10.v6
v5 = v10.v5
v4 = v10.v4
v3 = v10.v3
v2 = v10.v2
bilanciamento = v10.bilanciamento
liste = v10.liste
_prefixed_flatten = v10._prefixed_flatten
_structure_technical = v10._structure_technical


def A(nome, stat="", chance="", successo="", fallimento="", note=""):
    return {"name": nome, "stat": stat, "chance": chance, "success": successo, "failure": fallimento, "note": note}


ROOM_GUIDES = {
    "Arena": {"category":"Prova di statistiche","icon":"⚔️","summary":"Sfida un avversario scegliendo quale statistica mettere alla prova.","actions":[A("Disco acuminato","AGI","AGI / 4000","Ottieni un oggetto casuale dal pool dungeon.","Nessun premio."),A("Disco ricurvo","ATK","ATK / 4000","Ottieni un oggetto casuale dal pool dungeon.","Nessun premio."),A("Disco bilanciato","DEF","DEF / 4000","Ottieni un oggetto casuale dal pool dungeon.","Nessun premio.")],"rewards":["Oggetto casuale dungeon"],"risks":["Nessun premio se fallisci"]},
    "Armeria": {"category":"Premio legato al set","icon":"🛡️","summary":"Può materializzare un componente LV0 del set che indossi.","actions":[A("Evento automatico","Set equipaggiato","70% se il set è compatibile","Un componente casuale del tuo set a LV0.","30% nessun evento; nessun premio anche se non hai un set compatibile.","Le Forme Mega e il Pescatore non compatibile con l'Armeria vengono esclusi.")],"rewards":["Componente del proprio set LV0"],"risks":[]},
    "Bar": {"category":"Azzardo","icon":"🍹","summary":"La locanda di Bob può aiutarti, intrappolarti o allungare parecchio il dungeon.","actions":[A("Bevi","—","40%","Salti una stanza del percorso.","60% vieni inabilitato.","Il ramo che randomizzerebbe il danno è attualmente irraggiungibile perché usa lo stesso tiro dopo la soglia del 40%."),A("Passa","—","100%","Te ne vai senza conseguenze.","—"),A("Gira per la locanda","—","50% acqua · 30% latte · 10% loop · 10% crew","50%: 5 Acqua fresca; 30%: 2 Latte in sacchetto; 10%: aggiunge 2 Bar.","10%: aggiunge 3 nemici casuali.","Il boss extra previsto nel ramo crew è attualmente irraggiungibile con lo stesso tiro casuale.")],"rewards":["5× Dell'acqua fresca","2× Del latte in sacchetto"],"risks":["Inabilitazione","Stanze extra","Nemici extra"]},
    "Boss": {"category":"Combattimento","icon":"👑","summary":"Portone del boss: prepara uno scontro con un nemico boss del dungeon.","actions":[A("Apri la porta","Combattimento","—","Affronti il boss memorizzato per quella stanza.","Rischi la sconfitta in combattimento.","In gruppo puoi usare /aiuta prima dello scontro per chiedere supporto.")],"rewards":["Drop del boss"],"risks":["Scontro boss"]},
    "Cancello": {"category":"Evento globale","icon":"🚪","summary":"Un cancello condiviso alterna stato chiuso/aperto fra le visite dei giocatori.","actions":[A("Evento automatico","—","Dipende dallo stato globale","Se è aperto ottieni un oggetto casuale dai pool evento portato a LV2; poi il cancello si chiude.","Se è chiuso non ottieni nulla e il cancello viene aperto per la visita successiva.","Lo stato è globale, quindi può essere cambiato anche da un altro giocatore.")],"rewards":["Oggetto evento casuale LV2"],"risks":["Possibile stanza senza premio"]},
    "Crepaccio": {"category":"Percorso","icon":"🕳️","summary":"Puoi alterare la lunghezza del piano toccando la crepa.","actions":[A("Tocchi la crepa","—","50% / 50%","50% aggiunge una stanza casuale.","50% rimuove un'altra stanza dal percorso."),A("Ti allontani","—","100%","Nessun cambiamento.","—")],"rewards":[],"risks":["Il piano può allungarsi"]},
    "Cucina": {"category":"Azzardo / materiali","icon":"🌶️","summary":"Più spezie provi a rubare, maggiore è il bottino e maggiore è il rischio.","actions":[A("Ne prendo una","—","90%","1 Spezia.","Fallisci; nel ramo di fallimento può scattare l'inabilitazione."),A("Ne prendo 5","—","70%","5 Spezie.","Fallimento con rischio maggiore."),A("Ne prendo 10","—","50%","10 Spezie.","Fallimento con rischio maggiore."),A("Prendo il tavolo intero","—","20%","15 Spezie.","Fallimento molto rischioso.","È la scelta estrema della stanza.")],"rewards":["La spezia"],"risks":["Inabilitazione in caso di fallimento"]},
    "Cunicolo": {"category":"Evento raro","icon":"🪨","summary":"Passaggio automatico con possibilità di scaglione giallo e crollo del piano.","actions":[A("Evento automatico","—","1% scaglione · 2% crollo","All'1% ottieni Uno scaglione giallo.","Al 2% il crollo sposta il piano di -1.","I controlli usano lo stesso tiro: quando esce lo scaglione rientri anche nel crollo.")],"rewards":["Uno scaglione giallo"],"risks":["Crollo del cunicolo"]},
    "Fabbro": {"category":"Scambio / endgame","icon":"🔥","summary":"Scambia alcuni collezionabili per Gloria e può forgiare equipaggiamento LVMAX.","actions":[A("Avvicinati","Inventario","98% di attivazione","Può comprare Spilla rossa, Teschio antico, Uccellino scheletrico o Tempesta in barattolo in cambio di Gloria.","Se non possiedi materiale utile non ricavi nulla."),A("Allontanati","—","100%","Te ne vai.","—"),A("Approcciala","Equipaggiamento","Requisiti fissi","Con i 4 scaglioni e un equip LVX, trasforma un LVX in LVMAX.","Senza tutti i requisiti non forgia nulla.")],"rewards":["Gloria","Upgrade LVX → LVMAX"],"risks":["Consumo di oggetti/scaglioni quando applicabile"]},
    "Fattoria": {"category":"Evento globale","icon":"🐄","summary":"Nutrire le mucche prepara il premio; mungerle senza averle nutrite è pericoloso.","actions":[A("Nutri le mucche","—","100%","Attiva globalmente lo stato Mucche nutrite.","—"),A("Mungi le mucche","—","Dipende dallo stato globale","Se sono state nutrite ottieni 2 Latte in sacchetto e lo stato si resetta.","Se non sono nutrite vieni inabilitato.","Lo stato Mucche è condiviso fra i giocatori.")],"rewards":["2× Del latte in sacchetto"],"risks":["Inabilitazione se mungi al momento sbagliato"]},
    "Fonte magica": {"category":"Cura","icon":"💧","summary":"Una fonte automatica che può ridurre il danno accumulato nel dungeon.","actions":[A("Evento automatico","—","54%","Riduce il danno dungeon di 200.","46% non succede nulla.")],"rewards":["Cura 200 danno dungeon"],"risks":[]},
    "Locanda spettrale": {"category":"Azzardo","icon":"👻","summary":"Puoi riposare, ignorarla o tentare di svegliarti da ciò che forse è un sogno.","actions":[A("Entraci","—","Evento casuale","Può ridurre il danno dungeon di 300.","Può farti cadere e aggiungere 100 danno.","La stanza usa i suoi tiri di pericolo/risveglio per decidere l'esito."),A("Ignorala","—","100%","Nessun effetto.","—"),A("Svegliati","—","Evento raro","Può ottenere Uno scaglione blu.","Altrimenti nessun premio.")],"rewards":["Uno scaglione blu","Riposo: -300 danno"],"risks":["Caduta: +100 danno"]},
    "Luci ed ombre": {"category":"Inventario / approccio","icon":"☯️","summary":"La luce duplica un oggetto; gli approcci oscuri rischiano invece di perderlo.","actions":[A("Evento automatico","Approccio","Approcci oscuri: 20% punizione","Normalmente aggiunge una copia dell'oggetto scelto dal tuo inventario.","Con approccio oscuro, nel 20% dei casi rimuove una copia invece di aggiungerla.","Gli approcci non oscuri ricevono sempre la copia.")],"rewards":["Copia di un oggetto del proprio inventario"],"risks":["20% perdita oggetto con approccio oscuro"]},
    "Parco": {"category":"Prova di statistiche","icon":"🐻","summary":"Un branco di OrsoDruidi ti segue: puoi fuggire, affrontarlo o provare a parlarci.","actions":[A("Fuggi","AGI","AGI / 200","Se riesci ottieni un oggetto casuale; con il tiro attuale può diventare LV1.","Se fallisci rischi di perdere il dungeon / essere inabilitato."),A("Fermali","DEF","DEF / 1300","Se riesci ottieni un oggetto casuale; con il tiro attuale può diventare LV1.","Se fallisci perdi il dungeon e vieni inabilitato."),A("Parlaci","—","60% inabilitazione","—","Il dungeon viene interrotto; al 60% vieni anche inabilitato.","Il codice prevede Uno scaglione verde in un ramo rarissimo. Il premio LV2 di Fuggi/Fermali è oggi irraggiungibile perché la soglia LV1 viene controllata prima con lo stesso tiro.")],"rewards":["Oggetto casuale","Uno scaglione verde (raro)"],"risks":["Perdita del dungeon","Inabilitazione"]},
    "Piedistallo": {"category":"Azzardo / usabili","icon":"🎁","summary":"Rischia contro il masso per portarti via due copie di un usabile casuale.","actions":[A("Subito","—","50%","Ottieni 2 copie di un usabile casuale.","Vieni schiacciato e inabilitato."),A("Nah","—","100%","Te ne vai senza rischi.","—")],"rewards":["2× usabile casuale"],"risks":["Inabilitazione"]},
    "Pilastri": {"category":"Azzardo","icon":"⚡","summary":"I sette pilastri impostano brutalmente il danno del dungeon a uno dei due estremi.","actions":[A("Ti ci avvicini","—","50% / 50%","50% imposta il danno dungeon a -300.","50% imposta il danno dungeon a 999.","Sono valori impostati, non +/− relativi."),A("Fuggi!","—","100%","Nessun effetto.","—")],"rewards":["Danno dungeon impostato a -300"],"risks":["Danno dungeon impostato a 999"]},
    "Sabbie mobili": {"category":"Evento / pet","icon":"🏜️","summary":"Le sabbie possono inghiottirti; un valore PAT elevato può permettere al pet di salvarti.","actions":[A("Evento automatico","PAT","80% caduta","Con PAT > 666, nei casi compatibili il pet può salvarti; nel ramo più raro puoi ottenere Uno scaglione nero.","Se il salvataggio non avviene subisci la conseguenza delle sabbie.","La stanza usa lo stesso tiro per caduta, salvataggio e scaglione: i sotto-eventi non sono tiri indipendenti.")],"rewards":["Uno scaglione nero (rarissimo)"],"risks":["Conseguenza delle sabbie mobili"]},
    "Segreta abbandonata": {"category":"Loot","icon":"🗝️","summary":"Perquisisci un cadavere: a volte c'è ancora qualcosa di utile.","actions":[A("Evento automatico","—","40%","Ottieni 1 oggetto casuale fra Fune di fuga, Stimpak, Candela blu e Ultimo barlore.","60% nessun loot.")],"rewards":["Un fune di fuga","Uno stimpak","Candela blu","Ultimo barlore"],"risks":[]},
    "Stagno": {"category":"Pesca dungeon","icon":"🎣","summary":"Una piccola parentesi di pesca dentro il dungeon.","actions":[A("Peschiamo!","—","Prova della stanza","Puoi ottenere la cattura prevista dalla stanza.","Puoi ritrovarti con la Scarpa vecchia.","Il pool speciale della stanza include Carpa dentata e Scarpa vecchia."),A("Non è il caso","—","100%","Te ne vai.","—")],"rewards":["Carpa dentata","Scarpa vecchia"],"risks":[]},
    "Distributore": {"category":"Gloria / premio","icon":"🍬","summary":"Spendi una piccola quantità di Gloria per una caramella casuale.","actions":[A("Metti monetina","Gloria","Costa 1 Gloria","Ricevi una caramella determinata dal tiro della stanza.","Senza Gloria non puoi pagare."),A("Anche no","—","100%","Nessun effetto.","—")],"rewards":["Caramelle del distributore"],"risks":["-1 Gloria"]},
    "Bisca": {"category":"Azzardo / Gloria","icon":"🃏","summary":"Scommessa secca da 150 Gloria su due carte.","actions":[A("Scommetti","Gloria","Carte casuali 0–15","Se la tua carta è più alta vinci la scommessa prevista.","Se perdi, i 150 Gloria sono del banco."),A("N'altra volta","—","100%","Nessun effetto.","—")],"rewards":["Gloria dalla scommessa"],"risks":["150 Gloria"]},
    "Lupo solitario": {"category":"Evento automatico","icon":"🐺","summary":"Nel comportamento attuale il lupo, paradossalmente, non riesce mai ad attaccare.","actions":[A("Evento automatico","—","40% cura · 60% nulla","40%: nessun lupo e riduci il danno dungeon di 50.","60%: non succede nulla.","Il ramo +70 danno è attualmente irraggiungibile: usa la stessa soglia 40% in un elif dopo il primo controllo.")],"rewards":["-50 danno dungeon"],"risks":[]},
    "Stanza del sonno": {"category":"Azzardo","icon":"🛏️","summary":"Puoi continuare a dormire e lasciare che la stanza modifichi il danno, oppure scappare.","actions":[A("Continua a dormire","—","Evento casuale","Il danno viene modificato secondo gli scaglioni della stanza.","Gli esiti peggiori aumentano il danno.","La stanza usa moltiplicatori configurati in base al tiro."),A("Corri via","—","100%","Interrompi il sonno e lasci la stanza.","—")],"rewards":["Possibile riduzione/variazione del danno"],"risks":["Possibile aumento del danno"]},
    "Tempio azteco": {"category":"Prova di progressione","icon":"🗿","summary":"Tre modi diversi di controbilanciare l'idolo, ognuno basato su una misura della tua progressione.","actions":[A("Un mattone ancestrale","Specie nel bestiario","bestiario / 45","Ottieni Un idoletto.","Nessun premio."),A("Una piuma azteca","Livello giocatore","livello / 150","Ottieni Un idoletto.","Nessun premio."),A("Un cappello da esploratore","Grado","grado / 5000","Ottieni Un idoletto.","Nessun premio.")],"rewards":["Un idoletto"],"risks":[]},
    "Biblioteca": {"category":"Loot / libri","icon":"📚","summary":"Nel 30% dei casi trovi un libro casuale; nel restante 70% la vecchia biblioteca è vuota.","actions":[A("Evento automatico","—","30% libro · 70% vuota","Ottieni 1 libro casuale dal pool dei libri.","70% non trovi nulla.")],"rewards":["Libro casuale"],"risks":[]},
    "Stanza": {"category":"Percorso / danno","icon":"⬆️","summary":"Tre bottoni: puoi alterare piano e danno oppure uscire senza toccare nulla.","actions":[A("Sali","—","90% effetto · 10% niente","90%: -450 danno dungeon e piano -1.","10% il bottone non fa nulla."),A("Scendi","—","90% effetto · 10% niente","Se il danno è ≤500 viene impostato a 500 e il piano sale di +1.","Se il danno è già >500, aggiunge altri 500 senza aumentare il piano."),A("Non cliccare","—","100%","Esci senza modifiche.","—")],"rewards":["Possibile -450 danno"],"risks":["Possibile danno impostato/aumentato a 500"]},
    "Chiesa": {"category":"Set / libri","icon":"⛪","summary":"La preghiera premia alcuni set graditi con un libro; gli altri rischiano di essere cacciati a botte.","actions":[A("Prega","Set equipaggiato","Set gradito: premio certo","Se il tuo set è fra quelli graditi ricevi 1 libro casuale.","Con un set non gradito: 40% vieni fermato senza danni, 60% vieni cacciato e aggiungi 123 danno dungeon.","La soglia usa dungeon_over(60): il ramo senza danno è quindi il 40%, mentre il 60% restante subisce 123 danno."),A("Ritirati","—","100%","Te ne vai senza conseguenze.","—")],"rewards":["Libro casuale con set gradito"],"risks":["+123 danno con set non gradito"]},
    "MetaMusicoteca": {"category":"Drop rarissimo","icon":"🎵","summary":"Evento automatico con una piccolissima possibilità di trovare Crack musica.","actions":[A("Evento automatico","—","1%","Ottieni Crack musica.","99% nessun drop.")],"rewards":["Crack musica"],"risks":[]},
    "Spada conficcata": {"category":"Evento speciale","icon":"🗡️","summary":"Nei giorni 17 o 21 puoi liberarti della build attuale e ricevere Dono stellare LV4, una protezione unica fuori da qualsiasi set.","actions":[A("Estrai la spada","Data","Solo nei giorni 17 o 21","Azzera approccio/set/anello, disequipaggia arma e protezione, riporta la scheda alle stat base, restituisce gli extra permanenti come punti nello zaino e assegna Dono stellare LV4.","Negli altri giorni non ottieni il premio.","Dono stellare è una protezione standalone: a LV0 possiede, per ciascuna raw stat HP/ATK/DEF/AGI, il doppio del massimo raw presente fra tutti gli altri equipaggiamenti. Non appartiene ad alcun set."),A("Non ora","—","100%","Lasci la spada dov'è.","—")],"rewards":["Dono stellare LV4"],"risks":["La build corrente viene completamente liberata e le statistiche permanenti tornano alla base, con gli extra restituiti come oggetti-punto"]},
    "Faro": {"category":"Set / percorso","icon":"🔦","summary":"Puoi farti vedere da un nemico locale per ricevere un suo componente, oppure attirare boss.","actions":[A("Vedere","Nemici della location","100% se il set è materializzabile","Sceglie un nemico della tua location e ti dà un componente casuale del suo set a LV2.","Se il set non ha componenti materializzabili non ricevi l'oggetto.","Supporta anche le Forme Mega tramite arma Mega + Chip della forma."),A("Essere visto","—","100%","—","Aggiunge 2 incontri Boss al percorso.")],"rewards":["Componente set locale LV2"],"risks":["+2 Boss"]},
    "Podio": {"category":"Obiettivi / premio","icon":"🏆","summary":"Trasforma il numero di obiettivi completati in probabilità di vincere equipaggiamento di livello alto.","actions":[A("1° posto","Obiettivi","min(obiettivi / (totale / 1), 1)","Oggetto casuale LV3.","Perdi fino a 10 Gloria."),A("2° posto","Obiettivi","min(obiettivi / (totale / 2), 1)","Oggetto casuale LV2.","Perdi fino a 8 Gloria."),A("3° posto","Obiettivi","min(obiettivi / (totale / 3), 1)","Oggetto casuale LV1.","Perdi fino a 6 Gloria.","Con tutti gli obiettivi, tutti e tre i gradini arrivano al 100%.")],"rewards":["LV3 / LV2 / LV1"],"risks":["10 / 8 / 6 Gloria"]},
}


def build_data():
    data = v10.build_data()
    rooms = data.get("dungeon", {}).get("rooms", [])
    mancanti = []
    for room in rooms:
        guide = ROOM_GUIDES.get(room["name"])
        if guide is None:
            mancanti.append(room["name"])
            continue
        room["guide"] = guide
    if mancanti:
        raise RuntimeError(f"Stanze senza guida v11: {mancanti}")
    data["dungeon_room_guide"] = {
        "title": "Guida alle stanze",
        "description": "Ogni stanza spiegata in termini di gioco: cosa può succedere, cosa conviene scegliere, quali statistiche contano e cosa puoi ottenere o perdere.",
        "count": len(rooms),
    }
    data["meta"]["wiki_version"] = 11
    return data


EXTRA_JS = r'''
function roomRewardLink(name){
  const clean=String(name||'').replace(/^\d+×\s*/, '').replace(/\s+\(.*\)$/,'');
  const item=find(D.items,clean);
  return item?link('item',clean):esc(name);
}
function roomGuideCard(r){
  const g=r.guide||{};
  const stats=(g.actions||[]).map(a=>a.stat).filter(x=>x&&x!=='—');
  const unique=[...new Set(stats)];
  return `<button class="entity-card" onclick="go('room',${JSON.stringify(r.name)})"><div class="entity-title"><span>${esc(g.icon||'🚪')}</span><b>${esc(r.name)}</b></div><div class="muted">${esc(g.category||'Stanza')} · ${r.pct}%</div><p>${esc(g.summary||r.intro||'')}</p>${unique.length?`<div class="chips">${unique.map(x=>`<span class="chip">${esc(x)}</span>`).join('')}</div>`:''}</button>`;
}
const _wikiV11DungeonHome=dungeonHome;
dungeonHome=function(){
  const base=_wikiV11DungeonHome();
  const rooms=D.dungeon.rooms;
  const legend=`<div class="card"><h3>Come leggere le stanze</h3><p>La <b>probabilità di comparsa</b> deriva dal peso con cui la stanza entra nel generatore del piano. Le percentuali nelle scelte descrivono invece il tiro che avviene dopo essere entrati.</p><p>Quando una prova usa una statistica, la scheda mostra direttamente la formula. I casi in cui il runtime ha rami irraggiungibili o usa lo stesso tiro più volte sono indicati esplicitamente.</p></div>`;
  return base+sectionTitle('Guida alle stanze')+legend+`<div class="entity-grid">${rooms.map(roomGuideCard).join('')}</div>`;
};

roomDetail=function(name){
  const r=find(D.dungeon.rooms,name);if(!r)return missing(name);
  const g=r.guide||{};
  const actions=(g.actions||[]).map(a=>`<div class="card"><h3>${esc(a.name)}</h3>${a.stat&&a.stat!=='—'?`<p><b>Conta:</b> ${esc(a.stat)}</p>`:''}${a.chance?`<p><b>Probabilità / check:</b> ${esc(a.chance)}</p>`:''}${a.success?`<p><b>Se va bene:</b> ${esc(a.success)}</p>`:''}${a.failure&&a.failure!=='—'?`<p><b>Se va male:</b> ${esc(a.failure)}</p>`:''}${a.note?`<div class="effect human"><b>Comportamento attuale:</b> ${esc(a.note)}</div>`:''}</div>`).join('');
  const rewards=(g.rewards||[]).length?sectionTitle('Premi')+`<div class="chips">${g.rewards.map(x=>`<span class="chip">${roomRewardLink(x)}</span>`).join('')}</div>`:'';
  const risks=(g.risks||[]).length?sectionTitle('Rischi')+`<div class="chips">${g.risks.map(x=>`<span class="chip">${esc(x)}</span>`).join('')}</div>`:'';
  const raw=r.config&&Object.keys(r.config).length?`<details class="card"><summary><b>Parametri tecnici</b></summary><pre>${esc(JSON.stringify(r.config,null,2))}</pre></details>`:'';
  return head(r.name,g.summary||r.intro||'Stanza dungeon','Dungeon')+`<div class="detail"><div><div class="card"><div class="kicker">${esc(g.category||'Stanza')}</div><h2>In breve</h2><p>${esc(g.summary||r.intro||'')}</p><p><b>Probabilità di comparsa:</b> ${r.pct}% · <b>Peso:</b> ${r.weight}</p>${r.intro?`<p class="muted"><b>Scena:</b> ${esc(r.intro)}</p>`:''}</div>${sectionTitle('Come funziona')}<div class="entity-grid">${actions}</div>${rewards}${risks}${raw}</div><aside class="sidebox">${img('rooms',r.name,g.icon||'🚪')}<div class="mini"><b>${esc(g.category||'Stanza')}</b><br>${r.pct}% di comparsa</div></aside></div>`;
};
'''


def build_html():
    html = v10.HTML
    return v3._must_replace(html, "function render(){", EXTRA_JS + "\nfunction render(){", "Wiki v11 guida stanze")


HTML = build_html()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="_site")
    args = parser.parse_args()
    out = Path(args.output)
    if not out.is_absolute(): out = ROOT / out
    out.mkdir(parents=True, exist_ok=True)
    data = build_data()
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (out / "index.html").write_text(HTML.replace("__DATA__", payload), encoding="utf-8")
    (out / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    assets = ROOT / "wiki" / "assets"
    if assets.exists(): shutil.copytree(assets, out / "assets", dirs_exist_ok=True)
    print("Wiki v11 generata:", out)
    print(json.dumps(data["meta"]["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__": main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wiki v9: obiettivi, cataloghi separati, provenienza collezionabili e boss marini."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import genera_wiki_v8 as v8

ROOT = v8.ROOT
v7 = v8.v7
v6 = v8.v6
v5 = v8.v5
v4 = v8.v4
v3 = v8.v3
v2 = v8.v2
bilanciamento = v8.bilanciamento
liste = v8.liste
_prefixed_flatten = v8._prefixed_flatten
_structure_technical = v8._structure_technical


OBIETTIVI_COME_SI_OTTENGONO = {
    "Primo": "Diventa il primo giocatore del giorno a ottenere il titolo Primo.",
    "El forgiator": "Completa una forgia quando l'equipaggiamento si trova a LV9.",
    "Lo vincitor": "Raggiungi 10 vittorie nella stessa Arena.",
    "Stessa storia": "Raggiungi 3 sconfitte nella stessa Arena.",
    "Ottima kill": "Demolisci almeno una struttura durante un assalto.",
    "Quasi tuto perfetto": "Durante un assalto arriva al punto in cui hai subito troppo danno per continuare prima di completare l'assedio.",
    "Set all'improvviso": "In Arena ottieni una configurazione che contiene un set.",
    "DPS": "Totalizza almeno 30.000 danni registrati in un assalto.",
    "Ultima kill": "Distruggi l'ultima struttura rimasta nel villaggio nemico durante un assalto.",
    "Aiuto dungeon": "Aiuta un altro giocatore a sconfiggere un boss del dungeon al piano 8 o superiore.",
    "Bello e bravo": "Lancia/regala un oggetto agli altri giocatori con il sistema dei regali.",
    "Come non bruciarsi": "Completa una forgia quando l'equipaggiamento si trova a LV2.",
    "Milano tutta la vita": "Incontra l'evento della nebbia/Milano durante un dungeon.",
    "MEGA aiutino": "Aiuta un altro giocatore a sconfiggere un boss del dungeon al piano 18 o superiore.",
    "Forgiatore seriale": "Completa una forgia quando l'equipaggiamento si trova a LV5.",
    "Luzzica": "Ottieni un oggetto Oro come premio della Settimanale.",
    "neeerrrd": "Arriva al 1° posto nella classifica punti quando viene calcolata la graduatoria.",
    "Fra, fatti una vita": "Totalizza almeno 100.000 danni registrati in un assalto.",
    "Pesca grande ma poco fumo o arrosto": "Perdi una lotta marina contro uno dei boss nautici.",
    "Super smash sbros sbrau": "Vinci una rissa.",
    "Perditore": "Perdi una streak.",
    "A ri vederci": "Usa Una fune di fuga mentre sei in un dungeon.",
    "Tossico": "Usa Uno stimpak mentre sei in un dungeon.",
    "Te la sei cercata": "Usa Candela blu nel dungeon, aggiungendo un incontro Boss al percorso.",
    "Ultima a morire": "Usa Ultimo barlore nel dungeon, aggiungendo una stanza casuale al percorso.",
    "Fuga col sacco": "Riesci nell'evento Cucina del dungeon scegliendo una delle opzioni che fanno prendere 10 o più spezie.",
    "Collezionista": "Registra in setvisti tutti i set attualmente esistenti, equipaggiandoli/scoprendoli almeno una volta.",
    "A metà strada": "Registra in setvisti almeno il 50% dei set esistenti.",
    "Un decimo della collezione": "Registra in setvisti almeno il 10% dei set esistenti.",
    "Prima scoperta": "Scopri/equipaggia il tuo primo set.",
    "Precisino": "Concludi una sfida portando gli HP dell'avversario esattamente a 0.",
    "Tutta fortuna": "Vinci una sfida restando esattamente a 1 HP.",
    "Titanico": "Termina una sfida con almeno 4.000 HP rimanenti.",
    "Caduta con stile": "Raggiungi una serie di 15 sconfitte consecutive.",
    "Danneggiatore": "Infliggi almeno 5.555 danni in una singola sfida.",
    "Schiappetta": "Infliggi al massimo 100 danni in una singola sfida.",
    "Iperattivo": "Completa 2.500 sfide nello stesso giorno.",
    "Prima sfida": "Completa almeno 1 sfida.",
    "Sfidante tosto": "Raggiungi 4.500 sfide totali.",
    "Campione di sfida": "Raggiungi 8.000 sfide totali.",
    "SUPER SFIDANTE": "Raggiungi 12.500 sfide totali.",
    "Micro Pescatore": "Pesca un pesce con PesoKg <= 2: nel formato attuale significa un peso inferiore a 3 kg.",
    "Macro Pescatore": "Pesca un pesce con PesoKg >= 52.",
    "Dito lesto": "Sii il primo a premere il pulsante e prendere un regalo lanciato nel gruppo.",
    "Prima compera": "Effettua un acquisto nel negozio.",
    "Andrà meglio la prossima volta": "Perdi contro un boss.",
    "Non è andata meglio": "Perdi nuovamente contro un boss dopo avere già ottenuto Andrà meglio la prossima volta.",
    "Boss buster": "Sconfiggi il tuo primo boss.",
    "Boss slayer": "Sconfiggi un boss al livello personale 5 o superiore.",
    "Capo del boss": "Sconfiggi un boss al livello personale 15 o superiore.",
    "Maestro dei boss": "Sconfiggi un boss al livello personale 45 o superiore.",
    "Voglioso di perdere": "Prova ad affrontare un boss mentre il relativo cooldown non è ancora terminato.",
}


def _base(name):
    return v2.base_item(name)


def _achievement_data():
    rows = []
    for name, description in getattr(liste, "descri", {}).items():
        rows.append({
            "name": name,
            "description": str(description or "").strip(),
            "how": OBIETTIVI_COME_SI_OTTENGONO.get(
                name,
                str(description or "Condizione non documentata nel runtime corrente.").strip(),
            ),
            "cap_bonus": 10,
        })
    return sorted(rows, key=lambda x: x["name"].lower())


def _arena_sources(name):
    out = []
    for season, pool in getattr(liste, "arenamod", {}).items():
        if any(_base(item) == name for item in pool):
            out.append(str(season))
    return sorted(set(out), key=str.lower)


def _weekly_gold_names():
    try:
        import settimanale
        return {_base(x) for x in getattr(settimanale, "PREMI_ORO_SETTIMANALE", [])}
    except Exception:
        return set()


def _marine_boss_data(fishing):
    drops = {
        row["name"]: list(row.get("drops", []))
        for row in fishing.get("marine_encounters", {}).get("bosses", [])
    }
    rows = []
    for name, cfg in getattr(liste, "Nautici", {}).items():
        rows.append({
            "name": name,
            "stats": {
                "hp": cfg.get("hp", 0),
                "atk": cfg.get("atk", 0),
                "def": cfg.get("def", 0),
                "agi": cfg.get("agi", 0),
            },
            "set": cfg.get("set"),
            "ring": cfg.get("anello"),
            "approach": cfg.get("Ap"),
            "drops": drops.get(name, []),
        })
    return sorted(rows, key=lambda x: x["name"].lower())


def build_data():
    data = v8.build_data()
    shop = getattr(liste, "shop", {})
    weekly_gold = _weekly_gold_names()

    for row in data.get("items", []):
        name = row.get("name")
        types = set(row.get("types", []))
        row["is_collectible"] = "Decorativo / lore" in types
        row["is_usable"] = "Usabile" in types
        row["shop_price"] = shop.get(name) if name in shop else None
        row["arena_sources"] = _arena_sources(name)
        row["weekly_gold"] = name in weekly_gold

    achievements = _achievement_data()
    data["achievements"] = achievements
    data["achievement_system"] = {
        "cap_bonus_each": 10,
        "description": (
            "Gli obiettivi sono traguardi permanenti del profilo. Ogni obiettivo completato "
            "aumenta di 10 punti il Cap massimo utilizzabile per i punti statistica permanenti. "
            "Il numero di obiettivi completati viene inoltre usato dalla classifica /top obbiettivi."
        ),
    }
    data["marine_bosses"] = _marine_boss_data(data.get("fishing", {}))

    counts = data.setdefault("meta", {}).setdefault("counts", {})
    counts["achievements"] = len(achievements)
    counts["collectibles"] = sum(1 for x in data.get("items", []) if x.get("is_collectible"))
    counts["usables"] = sum(1 for x in data.get("items", []) if x.get("is_usable"))
    counts["marine_bosses"] = len(data["marine_bosses"])
    data["meta"]["wiki_version"] = 9
    return data


EXTRA_JS = r"""
const _wikiV9ListPage=listPage;
listPage=function(title,sub,arr,type,extra=x=>'',icon='•'){
  if(type==='item'&&title==='Oggetti'){
    arr=arr.filter(x=>!x.is_collectible&&!x.is_usable);
  }
  return _wikiV9ListPage(title,sub,arr,type,extra,icon);
};

function collectiblesPage(){
  const rows=D.items.filter(x=>x.is_collectible);
  return _wikiV9ListPage(
    'Collezionabili',
    'Oggetti decorativi e di collezione, separati dal catalogo generale. Apri una voce per vedere anche come si ottiene quando il runtime espone una provenienza.',
    rows,'item',
    x=>{
      const src=[];
      if(x.boss_drops?.length)src.push('Boss');
      if(x.location_drops?.length)src.push('Location');
      if(x.events?.length)src.push('Eventi');
      if(x.shop_price!=null)src.push('Negozio');
      if(x.arena_sources?.length)src.push('Arena');
      if(x.weekly_gold)src.push('Settimanale');
      return src.length?`Provenienza: ${src.join(' · ')}`:'Provenienza automatica non individuata';
    },
    '🏺'
  );
}

function usablesPage(){
  const rows=D.items.filter(x=>x.is_usable);
  return _wikiV9ListPage(
    'Usabili',
    'Consumabili e oggetti attivabili, separati dagli altri oggetti. Apri una voce per leggere l’effetto tecnico reale.',
    rows,'item',
    x=>x.description||x.types.join(' · '),
    '🧪'
  );
}

function collectibleAcquisition(i){
  const rows=[];
  (i.boss_drops||[]).forEach(x=>rows.push(`<div class="rowlink" onclick="location.hash='boss/${enc(x.boss)}'"><span>Boss: ${esc(x.boss)}</span><span class="prob">${x.pct}%</span></div>`));
  (i.location_drops||[]).forEach(x=>rows.push(`<div class="rowlink" onclick="location.hash='location/${enc(x.location)}'"><span>Location: ${esc(x.location)}</span><span class="prob">${x.pct}%</span></div>`));
  (i.events||[]).forEach(x=>rows.push(`<div class="rowlink" onclick="location.hash='event/${enc(x)}'"><span>Evento: ${esc(x)}</span><span>→</span></div>`));
  if(i.shop_price!=null)rows.push(`<div class="rowlink"><span>Negozio</span><span>${esc(i.shop_price)}</span></div>`);
  (i.arena_sources||[]).forEach(x=>rows.push(`<div class="rowlink"><span>Arena · ${esc(x)}</span><span>pool</span></div>`));
  if(i.weekly_gold)rows.push(`<div class="rowlink"><span>Settimanale</span><span>premio Oro</span></div>`);
  if(!rows.length)return '';
  return `${sectionTitle('Come si ottiene')}<div class="card">${rows.join('')}</div>`;
}

const _wikiV9ItemDetail=itemDetail;
itemDetail=function(name){
  const i=find(D.items,name);
  const base=_wikiV9ItemDetail(name);
  if(!i||!i.is_collectible)return base;
  return base+collectibleAcquisition(i);
};

function achievementsPage(){
  const s=D.achievement_system;
  const cards=D.achievements.map(a=>`<div class="card clickcard" data-search="${esc((a.name+' '+a.how+' '+a.description).toLowerCase())}" onclick="location.hash='achievement/${enc(a.name)}'"><h3>🎖 ${esc(a.name)}</h3><div class="muted">${esc(a.how)}</div></div>`).join('');
  return head('Obiettivi','Tutti i traguardi del profilo: cosa servono e come si sbloccano.','Obiettivi')
    +sectionTitle('A cosa servono')
    +`<div class="card"><p>${esc(s.description)}</p><p><b>Bonus per ogni obiettivo:</b> +${s.cap_bonus_each} Cap massimo.</p></div>`
    +sectionTitle(`Tutti gli obiettivi (${D.achievements.length})`)
    +`<div class="entity-grid">${cards}</div>`;
}

function achievementDetail(name){
  const a=find(D.achievements,name);
  if(!a)return missing(name);
  return head(a.name,'Condizione di sblocco e utilità dell’obiettivo.','Obiettivi')
    +`<div class="detail"><div>${sectionTitle('Come si ottiene')}<div class="effect human">${esc(a.how)}</div>`
    +`${sectionTitle('Descrizione originale')}<div class="card"><p>${esc(a.description||'—')}</p></div>`
    +`${sectionTitle('A cosa serve')}<div class="card"><p>Una volta completato resta nel profilo, vale <b>+${a.cap_bonus} Cap massimo</b> e aumenta di 1 il conteggio usato da <code>/top obbiettivi</code>.</p></div>`
    +`</div><aside class="sidebox">${img('achievements',a.name,'🎖️')}</aside></div>`;
}

function marineBossDetail(name){
  const b=find(D.marine_bosses,name);
  if(!b)return missing(name);
  const drops=(b.drops||[]).length?chipLinks('item',b.drops):'<div class="empty">Nessun drop configurato.</div>';
  return head(b.name,'Boss delle lotte marine: statistiche base e drop.','Pesca')
    +`<div class="detail"><div>${sectionTitle('Statistiche base')}${stats(b.stats)}`
    +`${sectionTitle('Drop')}${drops}`
    +`${sectionTitle('Configurazione')}<div class="card"><p><b>Set:</b> ${b.set?link('set',b.set):'—'}</p><p><b>Anello:</b> ${b.ring?link('ring',b.ring):'—'}</p><p><b>Approccio:</b> ${esc(b.approach||'—')}</p></div>`
    +`</div><aside class="sidebox">${img('bosses',b.name,'🌊')}</aside></div>`;
}
"""


def build_html():
    html = v8.HTML
    html = v3._must_replace(
        html,
        "${categoryCard('items','Oggetti','Oggetti senza LV, livelli, set e provenienza.','⚔️')}",
        "${categoryCard('items','Oggetti','Equipaggiamenti e altri oggetti, esclusi Usabili e Collezionabili.','⚔️')}${categoryCard('usables','Usabili','Consumabili e oggetti attivabili.','🧪')}${categoryCard('collectibles','Collezionabili','Oggetti decorativi, lore e relativa provenienza.','🏺')}${categoryCard('achievements','Obiettivi','Traguardi, utilità e condizioni di sblocco.','🎖️')}",
        "home cataloghi e obiettivi",
    )
    html = v3._must_replace(
        html,
        "else if(type==='location')html=locationDetail(name);else if(type==='fishing')html=fishingPage();else if(type==='items')",
        "else if(type==='location')html=locationDetail(name);else if(type==='fishing')html=fishingPage();else if(type==='marineboss')html=marineBossDetail(name);else if(type==='collectibles')html=collectiblesPage();else if(type==='usables')html=usablesPage();else if(type==='achievements')html=achievementsPage();else if(type==='achievement')html=achievementDetail(name);else if(type==='items')",
        "router v9",
    )
    html = v3._must_replace(
        html,
        '<div class=\\"card\\"><h3>${esc(b.name)}</h3><div class=\\"muted\\">Possibili premi</div>${chipLinks(\'item\',b.drops)}</div>',
        '<div class=\\"card clickcard\\" onclick=\\"location.hash=\\\'marineboss/${enc(b.name)}\\\'\\"><h3>${link(\'marineboss\',b.name)}</h3><div class=\\"muted\\">Apri statistiche e drop</div>${chipLinks(\'item\',b.drops)}</div>',
        "boss marini cliccabili",
    )
    html = v3._must_replace(
        html,
        "function render(){",
        EXTRA_JS + "\nfunction render(){",
        "funzioni v9",
    )
    return html


HTML = build_html()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="_site")
    args = parser.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        out = ROOT / out
    out.mkdir(parents=True, exist_ok=True)

    data = build_data()
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (out / "index.html").write_text(HTML.replace("__DATA__", payload), encoding="utf-8")
    (out / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    assets = ROOT / "wiki" / "assets"
    if assets.exists():
        shutil.copytree(assets, out / "assets", dirs_exist_ok=True)

    print("Wiki v9 generata:", out)
    print(json.dumps(data["meta"]["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

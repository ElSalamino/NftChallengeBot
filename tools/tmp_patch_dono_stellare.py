# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path, old, new, label):
    p = ROOT / path
    s = p.read_text(encoding='utf-8')
    if s.count(old) != 1:
        raise RuntimeError(f'{label}: atteso 1 match, trovati {s.count(old)}')
    p.write_text(s.replace(old, new, 1), encoding='utf-8')


# 1) liste.py: Dono stellare = protezione standalone, 2x il massimo di ogni raw stat
# fra tutti gli equipaggiamenti già esistenti. Viene calcolato prima di inserirlo,
# quindi non può auto-influenzare il proprio massimo.
replace_once(
    'liste.py',
    '''protezioniextra = {\n    "Cappellino da pescatore": {"hp": 0, "atk": 100, "def": 100, "agi": 0, "type": "🛡"},''',
    '''protezioniextra = {\n    "Cappellino da pescatore": {"hp": 0, "atk": 100, "def": 100, "agi": 0, "type": "🛡"},''',
    'ancora protezioniextra',
)

p = ROOT / 'liste.py'
s = p.read_text(encoding='utf-8')
anchor = '\n\nclassi = {'
if s.count(anchor) != 1:
    raise RuntimeError(f'ancora classi: {s.count(anchor)}')
insert = r'''

# Dono stellare: protezione unica e fuori dai set.
# Per ogni statistica prende il valore raw massimo fra TUTTI gli equipaggiamenti
# già definiti (armi/protezioni, normali ed extra) e lo raddoppia.
def _dono_stellare_stat_massima(stat):
    valori = []
    for gruppo in (armi, armiextra, protezioni, protezioniextra):
        for dati in gruppo.values():
            try:
                valori.append(int(dati.get(stat, 0)))
            except (TypeError, ValueError):
                pass
    return max(valori) if valori else 0


DONO_STELLARE_RAW_MASSIMI = {
    stat: _dono_stellare_stat_massima(stat)
    for stat in ("hp", "atk", "def", "agi")
}

protezioniextra["Dono stellare"] = {
    "hp": DONO_STELLARE_RAW_MASSIMI["hp"] * 2,
    "atk": DONO_STELLARE_RAW_MASSIMI["atk"] * 2,
    "def": DONO_STELLARE_RAW_MASSIMI["def"] * 2,
    "agi": DONO_STELLARE_RAW_MASSIMI["agi"] * 2,
    "type": "🛡",
}
'''
s = s.replace(anchor, insert + anchor, 1)
p.write_text(s, encoding='utf-8')

# 2) Runtime: nei giorni validi, dopo aver liberato/refundato la build,
# assegna davvero il Dono stellare LV4 promesso dalla stanza.
replace_once(
    'nft.py',
    '''                            if dif != 0:\n                                try:\n                                                player[username]["zaino"][pt[x]] += dif\n                                except:\n                                                player[username]["zaino"][pt[x]] = dif\n                    else:\n                        text += "\\nCosa?\\nCome non è il momento?!\\nERA IL MIO MOMENTO\\nNOOOOOOOOOOOOOOOOOOO"''',
    '''                            if dif != 0:\n                                try:\n                                                player[username]["zaino"][pt[x]] += dif\n                                except:\n                                                player[username]["zaino"][pt[x]] = dif\n\n                        premio_stellare = "Dono stellare LV4"\n                        try:\n                            player[username]["zaino"][premio_stellare] += 1\n                        except:\n                            player[username]["zaino"][premio_stellare] = 1\n                        text += f"\\nDalla spada si libera un bagliore: ottieni **{premio_stellare}**!"\n                    else:\n                        text += "\\nCosa?\\nCome non è il momento?!\\nERA IL MIO MOMENTO\\nNOOOOOOOOOOOOOOOOOOO"''',
    'premio runtime Spada conficcata',
)

# 3) Wiki v11: chiarisce cosa sia il Dono e che il reset della build è parte del prezzo.
p = ROOT / 'wiki/genera_wiki_v11.py'
s = p.read_text(encoding='utf-8')
old = '''    "Spada conficcata": {"category":"Evento speciale","icon":"🗡️","summary":"Una spada speciale legata anche al giorno/data può diventare Dono stellare.","actions":[A("Estrai la spada","Data / tiro","Giorni 17 o 21 + logica evento","Nel caso favorevole ottieni Dono stellare LV4.","Altrimenti la spada non viene estratta.","La stanza usa una soglia del 10% e controlli specifici sui giorni 17 e 21."),A("Non ora","—","100%","Lasci la spada dov'è.","—")],"rewards":["Dono stellare LV4"],"risks":[]},'''
new = '''    "Spada conficcata": {"category":"Evento speciale","icon":"🗡️","summary":"Nei giorni 17 o 21 puoi liberarti della build attuale e ricevere Dono stellare LV4, una protezione unica fuori da qualsiasi set.","actions":[A("Estrai la spada","Data","Solo nei giorni 17 o 21","Azzera approccio/set/anello, disequipaggia arma e protezione, riporta la scheda alle stat base, restituisce gli extra permanenti come punti nello zaino e assegna Dono stellare LV4.","Negli altri giorni non ottieni il premio.","Dono stellare è una protezione standalone: a LV0 possiede, per ciascuna raw stat HP/ATK/DEF/AGI, il doppio del massimo raw presente fra tutti gli altri equipaggiamenti. Non appartiene ad alcun set."),A("Non ora","—","100%","Lasci la spada dov'è.","—")],"rewards":["Dono stellare LV4"],"risks":["La build corrente viene completamente liberata e le statistiche permanenti tornano alla base, con gli extra restituiti come oggetti-punto"]},'''
if s.count(old) != 1:
    raise RuntimeError(f'blocco Spada wiki: {s.count(old)}')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')

print('Patch Dono stellare applicata')

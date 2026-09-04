# -*- coding: utf-8 -*-
from pathlib import Path
p=Path('wiki/genera_wiki_v11.py')
s=p.read_text(encoding='utf-8')
repls={
'''    "Biblioteca": {"category":"Evento raro","icon":"📚","summary":"Una biblioteca che nella maggior parte dei casi non offre nulla.","actions":[A("Evento automatico","—","70% vuota","Nel ramo non vuoto può produrre l'evento/libro previsto dalla stanza.","70% la biblioteca è vuota.")],"rewards":["Evento libro della Biblioteca"],"risks":[]},''':
'''    "Biblioteca": {"category":"Loot / libri","icon":"📚","summary":"Nel 30% dei casi trovi un libro casuale; nel restante 70% la vecchia biblioteca è vuota.","actions":[A("Evento automatico","—","30% libro · 70% vuota","Ottieni 1 libro casuale dal pool dei libri.","70% non trovi nulla.")],"rewards":["Libro casuale"],"risks":[]},''',
'''    "Chiesa": {"category":"Scelta narrativa","icon":"⛪","summary":"La chiesa offre la scelta fra pregare e ritirarsi.","actions":[A("Prega","—","Evento della stanza","Applica l'esito previsto dalla preghiera.","Può non produrre un vantaggio."),A("Ritirati","—","100%","Abbandoni la stanza.","—")],"rewards":[],"risks":[]},''':
'''    "Chiesa": {"category":"Set / libri","icon":"⛪","summary":"La preghiera premia alcuni set graditi con un libro; gli altri rischiano di essere cacciati a botte.","actions":[A("Prega","Set equipaggiato","Set gradito: premio certo","Se il tuo set è fra quelli graditi ricevi 1 libro casuale.","Con un set non gradito: 40% vieni fermato senza danni, 60% vieni cacciato e aggiungi 123 danno dungeon.","La soglia usa dungeon_over(60): il ramo senza danno è quindi il 40%, mentre il 60% restante subisce 123 danno."),A("Ritirati","—","100%","Te ne vai senza conseguenze.","—")],"rewards":["Libro casuale con set gradito"],"risks":["+123 danno con set non gradito"]},''',
}
for old,new in repls.items():
    if old not in s:
        raise RuntimeError('Blocco v11 da rifinire non trovato')
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

# -*- coding: utf-8 -*-
from pathlib import Path
p=Path('.github/workflows/wiki-pages.yml')
s=p.read_text(encoding='utf-8')

def one(old,new,label):
    global s
    if s.count(old)!=1:
        raise RuntimeError(f'{label}: match {s.count(old)}')
    s=s.replace(old,new,1)

one('wiki/genera_wiki_v10.py wiki/run_wiki.py','wiki/genera_wiki_v10.py wiki/genera_wiki_v11.py wiki/run_wiki.py','compile v11')
one("assert data['meta']['wiki_version'] == 10","assert data['meta']['wiki_version'] == 11",'wiki version')
one('print(f"Wiki v10: {len(data[\'achievements\'])} obiettivi; Podio e imboscate documentati")', '''rooms = data['dungeon']['rooms']
          assert len(rooms) == 31
          assert data['dungeon_room_guide']['count'] == 31
          assert all(r.get('guide') for r in rooms)
          assert all(r['guide'].get('summary') and r['guide'].get('category') for r in rooms)
          by_room = {r['name']: r for r in rooms}
          assert len(by_room['Arena']['guide']['actions']) == 3
          assert 'AGI' in {a['stat'] for a in by_room['Arena']['guide']['actions']}
          assert '54%' in by_room['Fonte magica']['guide']['actions'][0]['chance']
          assert 'LV2' in by_room['Faro']['guide']['actions'][0]['success']
          assert 'irraggiungibile' in by_room['Lupo solitario']['guide']['actions'][0]['note']
          assert '30%' in by_room['Biblioteca']['guide']['summary']
          assert '123' in by_room['Chiesa']['guide']['actions'][0]['failure']

          print(f"Wiki v11: {len(data['achievements'])} obiettivi; {len(rooms)} stanze tutte documentate")''','assert stanze v11')
anchor='''          grep -q "Mostri aggiunti" _site/index.html

          ! grep -q "generale.distrazione_proc=" _site/index.html'''
replacement='''          grep -q "Mostri aggiunti" _site/index.html

          # Wiki v11: guida completa e leggibile delle 31 stanze.
          grep -q "Guida alle stanze" _site/index.html
          grep -q "Come leggere le stanze" _site/index.html
          grep -q "Probabilità di comparsa" _site/index.html
          grep -q "Comportamento attuale" _site/index.html
          grep -q "Prova di statistiche" _site/index.html
          grep -q "Upgrade LVX" _site/index.html
          grep -q "30% dei casi trovi un libro" _site/index.html
          grep -q "123 danno dungeon" _site/index.html

          ! grep -q "generale.distrazione_proc=" _site/index.html'''
one(anchor,replacement,'grep v11')
p.write_text(s,encoding='utf-8')

# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'wiki'))

import genera_wiki_v10 as wiki
import bilanciamento

# Stesso bootstrap usato da wiki/run_wiki.py: evita la vecchia chiave None nei set.
wiki.v3.v2.set_names = wiki.v3._valid_set_names

data = wiki.build_data()
rooms = []
for room in data['dungeon']['rooms']:
    name = room['name']
    rooms.append({
        'name': name,
        'intro': room.get('intro'),
        'weight': room.get('weight'),
        'pct': room.get('pct'),
        'actions': room.get('actions', []),
        'config': bilanciamento.DUNGEON_CONFIG.get('stanze', {}).get(name, {}),
    })
print('ROOM_DUMP_BEGIN')
print(json.dumps(rooms, ensure_ascii=False, indent=2, sort_keys=True))
print('ROOM_DUMP_END')

# Contesto runtime delle stanze meno autoesplicative.
source = (ROOT / 'nft.py').read_text(encoding='utf-8').splitlines()
ambigue = [
    'Armeria', 'Bar', 'Boss', 'Cunicolo', 'Fabbro', 'Fattoria',
    'Locanda spettrale', 'Luci ed ombre', 'Sabbie mobili', 'Stagno',
    'Distributore', 'Bisca', 'Lupo solitario', 'Stanza del sonno',
    'Biblioteca', 'Chiesa', 'MetaMusicoteca', 'Spada conficcata',
]
print('RUNTIME_CONTEXT_BEGIN')
for stanza in ambigue:
    print(f'===== {stanza} =====')
    hits = [i for i, line in enumerate(source) if stanza in line]
    emitted = set()
    for i in hits:
        start = max(0, i - 5)
        end = min(len(source), i + 28)
        key = (start, end)
        if key in emitted:
            continue
        emitted.add(key)
        for j in range(start, end):
            print(f'{j+1:05d}: {source[j]}')
        print('---')
print('RUNTIME_CONTEXT_END')

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

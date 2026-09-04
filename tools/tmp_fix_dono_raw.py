# -*- coding: utf-8 -*-
from pathlib import Path
import re

p = Path('liste.py')
s = p.read_text(encoding='utf-8')

pattern = re.compile(
    r'# Dono stellare: protezione unica e fuori dai set\..*?(?=from set_raw_balance import \()',
    re.S,
)

replacement = '''# Dono stellare: protezione unica e fuori dai set.\n# Prende UN SOLO equipaggiamento: quello con il raw score base più alto secondo\n# gli stessi pesi usati dalla Wiki (HP x1, ATK x4, DEF x4, AGI x20).\n# La distribuzione completa di quell'oggetto viene poi raddoppiata.\nfrom set_raw_balance import SET_RAW_WEIGHTS as _DONO_RAW_WEIGHTS\n\n\ndef _dono_stellare_raw_score(dati):\n    totale = 0.0\n    for stat, peso in _DONO_RAW_WEIGHTS.items():\n        try:\n            valore = float((dati or {}).get(stat, 0) or 0)\n        except (TypeError, ValueError):\n            valore = 0.0\n        totale += valore * float(peso)\n    return totale\n\n\ndef _dono_stellare_oggetto_migliore():\n    migliore_nome = None\n    migliore_dati = None\n    migliore_score = None\n    for gruppo in (armi, armiextra, protezioni, protezioniextra):\n        for nome, dati in gruppo.items():\n            if str(nome).split(" LV", 1)[0] == "Dono stellare":\n                continue\n            score = _dono_stellare_raw_score(dati)\n            if migliore_score is None or score > migliore_score:\n                migliore_nome = str(nome).split(" LV", 1)[0]\n                migliore_dati = dati\n                migliore_score = score\n    return migliore_nome, migliore_dati or {}, migliore_score or 0\n\n\nDONO_STELLARE_BASE_OGGETTO, _DONO_STELLARE_BASE_STATS, DONO_STELLARE_BASE_SCORE = _dono_stellare_oggetto_migliore()\n\nprotezioniextra["Dono stellare"] = {\n    stat: int(round(float(_DONO_STELLARE_BASE_STATS.get(stat, 0) or 0) * 2))\n    for stat in ("hp", "atk", "def", "agi")\n}\nprotezioniextra["Dono stellare"]["type"] = "🛡"\nDONO_STELLARE_RAW_SCORE = _dono_stellare_raw_score(protezioniextra["Dono stellare"])\n\n'''

s2, count = pattern.subn(replacement, s, count=1)
if count != 1:
    raise SystemExit(f'Blocco Dono stellare non trovato in modo univoco: {count}')

p.write_text(s2, encoding='utf-8')
print('Dono stellare corretto: usa il singolo equipaggiamento col raw score massimo')

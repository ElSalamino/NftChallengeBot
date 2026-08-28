from pathlib import Path

p = Path('bilanciamento.py')
s = p.read_text(encoding='utf-8')

replacements = {
    # Hard counter statistici: circa x100 rispetto ai vecchi numeri.
    "'assalto': {'terrore_clone': {'proc': 100, 'atk_clone': -30, 'def_clone': -50}}":
        "'assalto': {'terrore_clone': {'proc': 100, 'atk_clone': -3000, 'def_clone': -5000}}",
    "'assalto': {'fabbro': {'proc': 100, 'atk': 30, 'def': 20}}":
        "'assalto': {'fabbro': {'proc': 100, 'atk': 3000, 'def': 2000}}",
    "'assalto': {'cucciolo': {'proc': 100, 'atk': 50}}":
        "'assalto': {'cucciolo': {'proc': 100, 'atk': 5000}}",
    "'assalto': {'cucciolo_drago': {'proc': 100, 'atk': 33}}":
        "'assalto': {'cucciolo_drago': {'proc': 100, 'atk': 3300}}",
    "'assalto': {'accampamento': {'proc': 100, 'atk': 20}}":
        "'assalto': {'accampamento': {'proc': 100, 'atk': 2000}}",
    "'assalto': {'spaventapasseri': {'atk': 30, 'def': 20}}":
        "'assalto': {'spaventapasseri': {'atk': 3000, 'def': 2000}}",
    "'assalto': {'centrale': {'proc': 100, 'atk': 150}}":
        "'assalto': {'centrale': {'proc': 100, 'atk': 15000}}",
    "'assalto': {'spuntone_schivato': {'proc': 100, 'def': 22, 'atk': 22},\n                                       'spuntone_colpito': {'proc': 100, 'def': 33}}":
        "'assalto': {'spuntone_schivato': {'proc': 100, 'def': 2200, 'atk': 2200},\n                                       'spuntone_colpito': {'proc': 100, 'def': 3300}}",
    "'assalto': {'cannoncino': {'proc': 100, 'def': 70}}":
        "'assalto': {'cannoncino': {'proc': 100, 'def': 7000}}",

    # Hard counter DPS diretti: abbastanza alti da far sentire davvero il matchup.
    "'assalto': {'draghetto': {'proc': 100, 'dps': 1000}}":
        "'assalto': {'draghetto': {'proc': 100, 'dps': 10000}}",
    "'assalto': {'clone': {'proc': 100, 'dps': 1000}}":
        "'assalto': {'clone': {'proc': 100, 'dps': 10000}}",
    "'assalto': {'cannoncino': {'proc': 100, 'dps': 1400}}":
        "'assalto': {'cannoncino': {'proc': 100, 'dps': 14000}}",
    "'assalto': {'drago_scaccia_drago': {'proc': 100, 'dps': 700}}":
        "'assalto': {'drago_scaccia_drago': {'proc': 100, 'dps': 7000}}",
}

for old, new in replacements.items():
    if old not in s:
        raise SystemExit(f'Pattern non trovato: {old}')
    s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
print('Hard counter assalto potenziati')

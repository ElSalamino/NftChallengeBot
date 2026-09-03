from pathlib import Path
import re


# nft.py — premi oro Settimanale centralizzati + LV0..LV4
path = Path("nft.py")
text = path.read_text(encoding="utf-8")

import_marker = (
    "from bilanciamento import PROC_CLASSI, PROC_ANELLI, NUCLEI_CONFIG, DUNGEON_CONFIG, "
    "INCANTESIMI_CONFIG, EFFETTI_CONFIG, WEEKEND_MOD_CONFIG, WEEKEND_MOD_POOL, STRUTTURE_CONFIG\n"
)
new_import = (
    import_marker
    + "from settimanale import PREMI_ORO_SETTIMANALE, SOGLIE_PREMI_ORO_SETTIMANALE, estrai_premio_oro_settimanale\n"
)
assert text.count(import_marker) == 1, "Import bilanciamento nft.py non riconosciuto"
text = text.replace(import_marker, new_import, 1)

pool_pattern = re.compile(
    r'(?ms)^(?P<indent>[ \t]+)premi = \[\s*'
    r'"Uno scudo d\'oro LV0",\s*'
    r'"Un pugnale d\'oro LV0",\s*'
    r'"Una balestra d\'oro LV0",\s*'
    r'"Spada d\'oro fortissima LV0",\s*'
    r'"Elmo d\'oro fortissimo LV0",\s*'
    r'"Anello d\'oro fortissimo",\s*'
    r'"Un rolex oro LV0"\s*\]\s*'
    r'(?P=indent)if punti > 8\.4:'
)
matches = list(pool_pattern.finditer(text))
assert len(matches) == 1, f"Pool oro settimanale trovato {len(matches)} volte"
indent = matches[0].group("indent")
text = pool_pattern.sub(
    f'{indent}premi = PREMI_ORO_SETTIMANALE\n'
    f'{indent}if punti > SOGLIE_PREMI_ORO_SETTIMANALE[0]:',
    text,
    count=1,
)

assert text.count("if punti > 8.8:") == 1
assert text.count("if punti > 9.6:") == 1
text = text.replace("if punti > 8.8:", "if punti > SOGLIE_PREMI_ORO_SETTIMANALE[1]:", 1)
text = text.replace("if punti > 9.6:", "if punti > SOGLIE_PREMI_ORO_SETTIMANALE[2]:", 1)

old_draw = "mio = random.choice(premi)"
draw_count = text.count(old_draw)
assert draw_count == 3, f"Attese 3 estrazioni premio oro, trovate {draw_count}"
text = text.replace(old_draw, "mio = estrai_premio_oro_settimanale(premi)")
path.write_text(text, encoding="utf-8")


# turno_assalto.py — la Coda usa l'INT del proprietario.
# anellon = anello del difensore, bonusn = bonus INT del difensore.
path = Path("turno_assalto.py")
text = path.read_text(encoding="utf-8")
old = (
    'percento = (main["lastD"] * bonus) / '
    'anello_val(anellon, "turno", "dolore", "divisore_chance")'
)
new = (
    'percento = (main["lastD"] * bonusn) / '
    'anello_val(anellon, "turno", "dolore", "divisore_chance")'
)
count = text.count(old)
assert count >= 1, "Formula Coda demoniaca non trovata"
text = text.replace(old, new)
path.write_text(text, encoding="utf-8")
print(f"Coda demoniaca corretta in {count} implementazioni")


# frasi_anelli.py — descrizione allineata alla logica reale.
path = Path("frasi_anelli.py")
text = path.read_text(encoding="utf-8")
old_phrase = (
    '    "Coda demoniaca": "Quando schivi prepari il terreno per far soffrire il nemico. '
    'Più danno c\'è in gioco, più cresce la possibilità di bloccarlo completamente; '
    'il calcolo usa {turno.dolore.divisore_chance} danni come riferimento e '
    'Demone spezza-ossa aggiunge {turno.dolore.bonus_speciale} al bonus.",'
)
new_phrase = (
    '    "Coda demoniaca": "Quando colpisci, la Coda demoniaca lascia al nemico il ricordo del dolore. '
    'Al suo turno, più danni gli hai inflitto e più è probabile che il dolore lo paralizzi, annullando completamente il suo attacco. '
    'La probabilità cresce anche con la tua INT; Demone spezza-ossa ottiene inoltre un bonus fisso del '
    '{turno.dolore.bonus_speciale:pct_mul}.",'
)
assert text.count(old_phrase) == 1, "Frase Coda demoniaca non riconosciuta"
text = text.replace(old_phrase, new_phrase, 1)
path.write_text(text, encoding="utf-8")

# -*- coding: utf-8 -*-
import json
import re
import string

from bilanciamento import PROC_CLASSI

PATH = "frasi_set.py"

AGGIORNAMENTI = {
    "Cercatore di reliquie": "Hai il {turno.reliquia.proc:pct} di trovare una reliquia durante la sfida: può regalarti {turno.reliquia.agi:signed} agilità, {turno.reliquia.hp:signed} HP, {turno.reliquia.def:signed} difesa oppure {turno.reliquia.atk:signed} attacco. ASSALTO — HARD COUNTER del Cannoncino: se scegli il Cannoncino come bersaglio, al {assalto.cannoncino.proc:pct} guadagni {assalto.cannoncino.def:signed} DEF per l'assalto.",
    "Ghoul": "Hai il {turno.pressione.proc:pct} di mettere pressione al nemico e togliergli {turno.pressione.atk_target:abs} ATK e {turno.pressione.def_target:abs} DEF. ASSALTO — HARD COUNTER del Clone: quando lo incontri, al {assalto.terrore_clone.proc:pct} gli togli {assalto.terrore_clone.atk_clone:abs} ATK e {assalto.terrore_clone.def_clone:abs} DEF per quello scontro contro la struttura.",
    "Contrabbandiere": "Hai il {turno.piazza_carica.proc:pct} di piazzare una carica sul nemico; quando esplode, ogni carica vale {turno.detonazione.danno_per_carica} danni. ASSALTO — HARD COUNTER della Stazione laser di sicurezza: quando la incontri, al {assalto.laser.proc:pct} neutralizzi completamente il suo attacco.",
    "IppoFan": "In sfida hai il {turno.copia_attacco.proc:pct} di sfruttare l'attacco avversario. ASSALTO — HARD COUNTER del Cannoncino: quando lo incontri, al {assalto.cannoncino.proc:pct} lo confondi e neutralizzi completamente il suo attacco.",
    "Campione del sole": "Più aspetti, più il colpo diventa pericoloso: sotto {turno.colpo_caricato.hp_trigger} HP puoi scaricarlo già dopo {turno.colpo_caricato.mol_min_hp} cariche, altrimenti ne servono almeno {turno.colpo_caricato.mol_min_fallback}. ASSALTO — HARD COUNTER del Fabbro incantaspade: quando lo incontri, al {assalto.fabbro.proc:pct} eviti il suo attacco e guadagni {assalto.fabbro.atk:signed} ATK e {assalto.fabbro.def:signed} DEF, che restano per il resto dell'assalto.",
    "Anima oscura": "In sfida hai il {turno.parry.proc:pct} di parare completamente il colpo e potenziare il tuo attacco. ASSALTO — HARD COUNTER del Fabbro incantaspade: quando lo incontri, al {assalto.fabbro.proc:pct} neutralizzi completamente il suo attacco.",
    "Drago": "Le scaglie hanno il {turno.scaglie.proc:pct} di ridurre il colpo subito e possono anche danneggiare l'arma nemica. ASSALTO — HARD COUNTER del Sedimento del cucciolo: quando lo incontri, al {assalto.cucciolo.proc:pct} neutralizzi il suo attacco e guadagni {assalto.cucciolo.atk:signed} ATK, che resta per il resto dell'assalto.",
    "PiroIncantatore": "In sfida hai il {turno.golem_fuoco.proc:pct} di evocare il golem di fuoco. ASSALTO — HARD COUNTER del Sedimento del cucciolo: quando lo incontri, al {assalto.cucciolo_drago.proc:pct} neutralizzi il suo attacco e guadagni {assalto.cucciolo_drago.atk:signed} ATK, che resta per il resto dell'assalto.",
    "Guerriero 3D": "In sfida il tuo stile altera anche l'atterraggio dei colpi. ASSALTO — HARD COUNTER del Sedimento del cucciolo: quando lo incontri, al {assalto.cucciolo.proc:pct} neutralizzi completamente il suo attacco.",
    "Cercatore": "Quando difendi hai il {turno.demoni_difesa.proc:pct} di richiamare i demoni in tuo aiuto. ASSALTO — HARD COUNTER dell'Accampamento: quando lo incontri, al {assalto.accampamento.proc:pct} neutralizzi il suo attacco e guadagni {assalto.accampamento.atk:signed} ATK, che resta per il resto dell'assalto.",
    "Juggernaut": "In sfida la tua massa porta l'agilità difensiva del nemico a {turno.peso.agi_difesa_mul:x} del normale. ASSALTO — HARD COUNTER del Cane da guardia: quando lo incontri, al {assalto.cane.proc:pct} la tua armatura neutralizza completamente il suo attacco.",
    "Scudiero del boschetto": "Finché non hai inflitto più di {turno.recupero.fatto_max} danni continui a crescere: {turno.recupero.hp:signed} HP, {turno.recupero.atk:signed} ATK, {turno.recupero.def:signed} DEF e {turno.recupero.agi:signed} AGI. ASSALTO — HARD COUNTER dello Spaventapasseri ornamentale: quando lo incontri lo neutralizzi e guadagni {assalto.spaventapasseri.atk:signed} ATK e {assalto.spaventapasseri.def:signed} DEF, che restano per il resto dell'assalto.",
    "Regina golgari": "Hai il {turno.pietrifica.proc:pct} di pietrificare il nemico in sfida. ASSALTO — HARD COUNTER del Clone: quando lo incontri, al {assalto.clone.proc:pct} lo pietrifichi e neutralizzi completamente il suo attacco.",
    "Ombra silenziosa": "In sfida puoi silenziare numerose abilità avversarie. ASSALTO — HARD COUNTER della Centrale di cura centralizzata: quando la incontri, al {assalto.centrale.proc:pct} la silenzi prima del suo impulso e guadagni {assalto.centrale.atk:signed} ATK, che resta per il resto dell'assalto.",
    "Assassino delle ombre": "ASSALTO — COUNTER della Centrale di cura centralizzata: quando la Centrale prova a curare, hai un primo controllo al {assalto.centrale.proc:pct} e un secondo al {assalto.centrale.proc_post:pct} per trasformare la sua cura in danno alle strutture. Il valore è {assalto.centrale.danno_per_livello} danni per livello della Centrale; nel primo effetto le strutture sotto la soglia di {assalto.centrale.hp_min} HP vengono preservate.",
    "Cavaliere delle spine": "Quando difendi hai il {turno.spine_difesa.proc:pct} di rimandare indietro parte del colpo. ASSALTO — HARD COUNTER dello Spuntone malefico: se lo eviti, al {assalto.spuntone_schivato.proc:pct} guadagni {assalto.spuntone_schivato.atk:signed} ATK e {assalto.spuntone_schivato.def:signed} DEF; se ti colpisce, al {assalto.spuntone_colpito.proc:pct} guadagni {assalto.spuntone_colpito.def:signed} DEF. I bonus restano per il resto dell'assalto.",
    "Crociato": "Se il nemico schiva, hai il {turno.punizione_schivata.proc:pct} di punirlo comunque. ASSALTO — HARD COUNTER del Muraglione extra: se scegli il Muraglione come bersaglio, al {assalto.muraglione.proc:pct} aggiungi altre {assalto.muraglione.moltiplicatore_extra} volte il DPS originale al colpo, oltre al colpo normale.",
    "Cacciatore": "In sfida puoi sfruttare il tuo compagno Junior. ASSALTO — HARD COUNTER del Sedimento del cucciolo: se lo scegli come bersaglio, al {assalto.draghetto.proc:pct} aggiungi {assalto.draghetto.dps:signed} DPS al colpo.",
    "Spacca Mostri": "Più vita ha il nemico, più male gli fai: in sfida aggiungi al colpo un quarto dei suoi HP. ASSALTO — HARD COUNTER del Clone: se lo scegli come bersaglio, al {assalto.clone.proc:pct} aggiungi {assalto.clone.dps:signed} DPS al colpo.",
    "Primo alla bandiera": "Quando vieni colpito hai il {turno.colpito.proc:pct} di trasformare parte del colpo in cura. ASSALTO — HARD COUNTER del Cannoncino: se lo scegli come bersaglio, al {assalto.cannoncino.proc:pct} aggiungi {assalto.cannoncino.dps:signed} DPS al colpo.",
    "Ice and fire": "Hai il {turno.calore.proc:pct} di scaldarti e guadagnare {turno.calore.atk:signed} ATK oppure il {turno.gelo.proc:pct} di congelare tutto e guadagnare {turno.gelo.def:signed} DEF. ASSALTO — HARD COUNTER del Sedimento del cucciolo: se lo scegli come bersaglio, al {assalto.drago_scaccia_drago.proc:pct} aggiungi {assalto.drago_scaccia_drago.dps:signed} DPS al colpo.",
    "Serial killer": "Il tuo avversario inizia la sfida con solo il {generale.inizio.hp_target_percento:pct} dei suoi HP. ASSALTO — se il Bersaglio enorme riesce a deviare il tuo assalto su di sé, guadagni {assalto.bersaglio_enorme.agi:signed} AGI per affrontarlo.",
    "Vigilante": "In sfida hai il {turno.cambio_proiettili_attacco.proc:pct} di cambiare munizioni in attacco e il {turno.cambio_proiettili_difesa.proc:pct} in difesa. ASSALTO — HARD COUNTER del Bersaglio enorme: se prova a deviare il tuo assalto, Vigilante impedisce la deviazione e mantieni il bersaglio scelto.",
}


def valida_placeholder(nome, template):
    for _, campo, formato, conversione in string.Formatter().parse(template):
        if campo is None:
            continue
        if conversione:
            raise ValueError(f"Conversione non supportata in {nome}: {conversione}")
        if campo.startswith("bonus."):
            continue
        valore = PROC_CLASSI[nome]
        for parte in campo.split("."):
            if not isinstance(valore, dict) or parte not in valore:
                raise KeyError(f"Placeholder non valido: {nome}.{campo}")
            valore = valore[parte]


for nome, frase in AGGIORNAMENTI.items():
    valida_placeholder(nome, frase)

with open(PATH, encoding="utf-8") as f:
    righe = f.readlines()

modificati = set()
for i, riga in enumerate(righe):
    m = re.match(r'^\s{4}"([^"]+)":\s*"', riga)
    if not m:
        continue
    nome = m.group(1)
    if nome in AGGIORNAMENTI:
        righe[i] = f"    {json.dumps(nome, ensure_ascii=False)}: {json.dumps(AGGIORNAMENTI[nome], ensure_ascii=False)},\n"
        modificati.add(nome)

mancanti = set(AGGIORNAMENTI) - modificati
if mancanti:
    raise RuntimeError(f"Frasi non trovate: {sorted(mancanti)}")

with open(PATH, "w", encoding="utf-8") as f:
    f.writelines(righe)

print(f"Aggiornate {len(modificati)} frasi hard counter")

# -*- coding: utf-8 -*-
"""Frasi leggibili degli incantesimi, con valori presi da INCANTESIMI_CONFIG."""

FRASI_INCANTESIMI_TECNICHE = {
    "Icore": "Quando attacchi hai il {turno.penetrazione.proc:pct} di portare la difesa usata dal nemico al {turno.penetrazione.difesa_target_mul:pct_mul} per quel colpo.",
    "Ingrossamento": "A ogni attacco hai il {turno.crescita.proc:pct} di far crescere l'arma: guadagni tra {turno.crescita.atk_min} e {turno.crescita.atk_max} ATK, ma perdi tra {turno.crescita.agi_max:abs} e {turno.crescita.agi_min:abs} AGI.",
    "Predominio": "Se chi ti attacca ha meno o gli stessi HP di te, riduci il suo potenziale offensivo del {turno.difesa.dps_attaccante_mul:rid_pct}; nello stesso calcolo però gli concedi {turno.difesa.agi_attaccante:signed} AGI, rendendolo più difficile da schivare.",
    "Duraturo": "Quando difendi hai il {turno.difesa.proc:pct} di far valere la tua DEF al {turno.difesa.difesa_mul:pct_mul} per quel colpo.",
    "Smateriabile": "Quando difendi hai il {turno.annulla_colpo.proc:pct} di annullare completamente un colpo normale; contro la tempesta di sabbia la possibilità sale al {turno.tempesta_sabbia.proc:pct}. Inoltre blocca sempre Muori insetto di Fire lord quando quel colpo speciale riesce ad attivarsi.",
    "Tocco fantasma": "Se il nemico schiva, hai il {turno.colpo_schivato.proc:pct} di colpirlo comunque per un danno tra il {turno.colpo_schivato.dps_percento_min:pct} e il {turno.colpo_schivato.dps_percento_max:pct} del tuo DPS, con un minimo di {turno.colpo_schivato.danno_min} danni.",
    "Leggiadra": "Se almeno uno dei due combattenti possiede Leggiadra, a ogni turno c’è il {turno.neutralizza_gadget.proc:pct} di neutralizzare contemporaneamente il gadget dell’attaccante e quello del difensore per quel turno. Gli anelli restano equipaggiati: vengono solo ignorati durante quel calcolo.",
    "Speranza": "Quando difendi e resti tra {turno.salvezza.hp_min} e {turno.salvezza.hp_max} HP, torni subito a {turno.salvezza.hp_porta_a} HP prima di risolvere il colpo in arrivo.",
    "Velenoso": "Ogni tuo colpo ha il {turno.veleno.proc:pct} di aggiungere {turno.veleno.stack} carica di veleno. Ogni carica infligge {turno.veleno.danno_per_stack} danni ogni volta che quel bersaglio torna a subire un tuo turno.",
    "Iridescente": "Quando vieni attaccato hai il {turno.cura.proc:pct} di recuperare {turno.cura.cura} HP.",
    "Minimista": "Se un colpo verrebbe annullato, riporta il modificatore a {turno.danno_minimo.mod_min:pct_mul}; se anche il danno base è a zero lo porta a {turno.danno_minimo.danno_base_min}, così il colpo può ancora lasciare il segno.",
    "Mimico": "Quando entra in gioco, sostituisce i tuoi incantesimi con quelli dell'avversario per il resto di quella copia dello scontro.",
    "Affilatezza": "A ogni attacco hai il {turno.affila.proc:pct} di portare il tuo ATK al {turno.affila.atk_mul:pct_mul} del valore attuale. L'aumento resta nello scontro e può attivarsi più volte.",
    "Legione": "Se anche l'avversario possiede Legione, il DPS del tuo colpo viene moltiplicato per {turno.duello_legione.dps_mul:x}.",
    "Critico": "Ogni colpo ha il {turno.critico.proc:pct} di diventare critico e portare il danno al {turno.critico.danno_mul:pct_mul} del valore normale.",
    "Primo impatto": "Il primo colpo dello scontro porta il danno al {turno.primo_colpo.danno_mul:pct_mul}; poi Primo impatto si consuma per quello scontro.",
    "Multiplo": "Quando difendi hai il {turno.difesa.proc:pct} di ottenere {turno.difesa.agi:signed} AGI solo nel calcolo della schivata di quel colpo.",
    "Legaccio": "A ogni attacco hai il {turno.lega.proc:pct} di portare l'AGI attuale del nemico al {turno.lega.agi_target_mul:pct_mul}. La riduzione resta nello scontro e può accumularsi.",
    "Urlo di drago": "A ogni attacco hai il {turno.terrore.proc:pct} di terrorizzare il nemico: al suo prossimo turno non infligge il colpo e poi il terrore svanisce.",
    "Evocabilità": "Se vieni evocato come supporto contro un boss del dungeon, chi ti ha chiamato riceve {dungeon.supporto.atk:signed} ATK, {dungeon.supporto.def:signed} DEF e {dungeon.supporto.agi:signed} AGI.",
}

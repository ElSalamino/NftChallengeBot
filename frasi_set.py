# -*- coding: utf-8 -*-
"""Frasi leggibili dei set.

I numeri non sono duplicati qui: ogni placeholder legge il valore corrente da
PROC_CLASSI oppure, con il prefisso ``bonus.``, dai bonus base del set.
In questo modo il testo resta umano ma segue sempre il bilanciamento reale.

Formati disponibili nel renderer di nft.py:
- ``:pct`` aggiunge il simbolo %;
- ``:x`` mostra un moltiplicatore;
- ``:signed`` mostra il segno sui bonus positivi;
- ``:abs`` usa il valore assoluto;
- ``:bool`` mostra sì/no;
- ``:rid_pct`` trasforma un moltiplicatore nella riduzione percentuale.
"""

FRASI_SET_TECNICHE = {
    "Esperto di animali": "Scegli la creatura giusta e lascia che combatta con te. Il Dragone delle stelle ha il {turno.dragone_stelle.proc:pct} di portare il tuo danno a {turno.dragone_stelle.dps_mul:x}, la Balena territoriale ha il {turno.balena_territoriale.proc:pct} di darti {turno.balena_territoriale.def:signed} difesa e il Silvantropo ha il {turno.silvantropo.proc:pct} di curarti di {turno.silvantropo.cura} HP.",
    "Pescatore": "Oltre a darti {bonus.atk:signed} attacco e {bonus.def:signed} difesa, migliora di {pesca.rarita.bonus_rarita:signed} la rarità della pesca.",
    "Re del raaave": "Il meteo diventa la tua pista da ballo: con Arcobaleno guadagni {assalto.meteo.arcobaleno_atk:signed} attacco, mentre Caldo torrido e Caldo infernale possono cambiare attacco e agilità di {assalto.meteo.caldo_torrido_atk:signed} e {assalto.meteo.caldo_infernale_agi:signed}.",
    "Piccolo kraken": "Il suo vero vantaggio sta negli approcci migliorati: non aggiunge altri effetti casuali durante la sfida.",
    "Pescatore di balene": "Parti più robusto con {bonus.hp:signed} HP, {bonus.atk:signed} attacco e {bonus.def:signed} difesa, e aumenti di {pesca.rarita.bonus_rarita:signed} la rarità della pesca.",
    "Campione del sole": "Più aspetti, più il colpo diventa pericoloso: sotto {turno.colpo_caricato.hp_trigger} HP puoi scaricarlo già dopo {turno.colpo_caricato.mol_min_hp} cariche, altrimenti ne servono almeno {turno.colpo_caricato.mol_min_fallback}. ASSALTO — HARD COUNTER del Fabbro incantaspade: quando lo incontri, al {assalto.fabbro.proc:pct} eviti il suo attacco e guadagni {assalto.fabbro.atk:signed} ATK e {assalto.fabbro.def:signed} DEF, che restano per il resto dell'assalto.",
    "Cercatore di reliquie": "Hai il {turno.reliquia.proc:pct} di trovare una reliquia durante la sfida: può regalarti {turno.reliquia.agi:signed} agilità, {turno.reliquia.hp:signed} HP, {turno.reliquia.def:signed} difesa oppure {turno.reliquia.atk:signed} attacco. ASSALTO — HARD COUNTER del Cannoncino: se scegli il Cannoncino come bersaglio, al {assalto.cannoncino.proc:pct} guadagni {assalto.cannoncino.def:signed} DEF per l'assalto.",
    "Regina golgari": "Hai il {turno.pietrifica.proc:pct} di pietrificare il nemico in sfida. ASSALTO — HARD COUNTER del Clone: quando lo incontri, al {assalto.clone.proc:pct} lo pietrifichi e neutralizzi completamente il suo attacco.",
    "Manipolatore di morte": "Hai il {turno.scheletri.proc:pct} di richiamare scheletri quando ti manca vita: ne arriva uno ogni {turno.scheletri.hp_per_scheletro} HP mancanti rispetto a {turno.scheletri.hp_riferimento}. In assalto la loro distrazione ha il {assalto.distrazione.proc:pct} di darti {assalto.distrazione.agi:signed} agilità.",
    "Inferno risvegliato": "Il fuoco non fa preferenze: in sfida aumenta il tuo attacco di {turno.inferno.atk_main} e anche quello del nemico di {turno.inferno.atk_target}. In assalto guadagni altri {assalto.inferno.atk_player:signed} punti attacco.",
    "Fiamma pura": "Hai il {turno.arena_brucia.proc:pct} di incendiare entrambi e togliere {turno.arena_brucia.danno_main} HP a testa. Se muori durante un assalto, hai il {assalto.esplosione_morte.proc:pct} di esplodere: ogni struttura con abbastanza vita subisce il maggiore tra {assalto.esplosione_morte.danno_minimo} danni e un centesimo dei tuoi HP massimi.",
    "Mago mentale": "Hai il {turno.showtime.proc:pct} di prendere il controllo dello scontro e scatenare da {turno.showtime.colpi_min} a {turno.showtime.colpi_max} colpi. Attenzione: c'è anche il {turno.showtime.autodanno_proc:pct} che il potere ti si ritorca contro.",
    "Illusionista": "Quando difendi hai il {turno.copie_difesa.proc:pct} di creare copie di te stesso; chi ti attacca ha solo il {turno.copie_difesa.proc_originale:pct} di trovare l'originale. In assalto le copie hanno il {assalto.copie.proc:pct} di togliere {assalto.copie.agi_difesa:abs} agilità alla difesa nemica.",
    "Assassino delle ombre": "ASSALTO — COUNTER della Centrale di cura centralizzata: quando la Centrale prova a curare, hai un primo controllo al {assalto.centrale.proc:pct} e un secondo al {assalto.centrale.proc_post:pct} per trasformare la sua cura in danno alle strutture. Il valore è {assalto.centrale.danno_per_livello} danni per livello della Centrale; nel primo effetto le strutture sotto la soglia di {assalto.centrale.hp_min} HP vengono preservate.",
    "Cercatore": "Quando difendi hai il {turno.demoni_difesa.proc:pct} di richiamare i demoni in tuo aiuto. ASSALTO — HARD COUNTER dell'Accampamento: quando lo incontri, al {assalto.accampamento.proc:pct} neutralizzi il suo attacco e guadagni {assalto.accampamento.atk:signed} ATK, che resta per il resto dell'assalto.",
    "Scudiero del boschetto": "Finché non hai inflitto più di {turno.recupero.fatto_max} danni continui a crescere: {turno.recupero.hp:signed} HP, {turno.recupero.atk:signed} ATK, {turno.recupero.def:signed} DEF e {turno.recupero.agi:signed} AGI. ASSALTO — HARD COUNTER dello Spaventapasseri ornamentale: quando lo incontri lo neutralizzi e guadagni {assalto.spaventapasseri.atk:signed} ATK e {assalto.spaventapasseri.def:signed} DEF, che restano per il resto dell'assalto.",
    "Contrabbandiere": "Hai il {turno.piazza_carica.proc:pct} di piazzare una carica sul nemico; quando esplode, ogni carica vale {turno.detonazione.danno_per_carica} danni. ASSALTO — HARD COUNTER della Stazione laser di sicurezza: quando la incontri, al {assalto.laser.proc:pct} neutralizzi completamente il suo attacco.",
    "Bug Abuser": "Hai il {turno.bug.proc:pct} di rompere le regole e pescare un effetto da altri set: Golem, Druido, Tartaruga, Vigilante o Chip fuoco. Il Chip, per esempio, può aggiungere {turno.chip_fuoco.dps:signed} danni, mentre il Golem può darti {turno.golem_fuoco.agi:signed} agilità.",
    "Serial killer": "Il tuo avversario inizia la sfida con solo il {generale.inizio.hp_target_percento:pct} dei suoi HP. ASSALTO — se il Bersaglio enorme riesce a deviare il tuo assalto su di sé, guadagni {assalto.bersaglio_enorme.agi:signed} AGI per affrontarlo.",
    "Fire lord": "Hai il {turno.muori_insetto.proc:pct} di bruciare il nemico per {turno.muori_insetto.danno} danni. In assalto puoi concatenare fino a {assalto.catena.tentativi} colpi da {assalto.catena.danno} danni ciascuno.",
    "Forma terra": "Quando difendi, il Chip terra ha il {turno.chip_difesa.proc:pct} di ridurre di {turno.chip_difesa.dps:abs} i danni del colpo nemico.",
    "Forma fuoco": "Il Chip fuoco ha il {turno.chip.proc:pct} di accendersi e aggiungere {turno.chip.dps:signed} danni al tuo colpo.",
    "Forma lunare": "Quando difendi, il Chip lunare ha il {turno.chip_difesa.proc:pct} di aumentare la tua agilità di {turno.chip_difesa.agi_propria} e ridurre quella del nemico di {turno.chip_difesa.agi_nemico:abs}.",
    "Forma elettro": "Il Chip elettro ha il {turno.chip.proc:pct} di renderti quasi imprendibile, portando il bonus agilità a {turno.chip.agi} e aggiungendo {turno.chip.dps:signed} danni.",
    "Operatore di classe": "Niente trucchi: il set ti dà direttamente {bonus.atk:signed} attacco e {bonus.def:signed} difesa.",
    "Shogun moderno": "Hai il {turno.doppio_colpo.proc:pct} di sferrare un secondo colpo, con forza tra {turno.doppio_colpo.moltiplicatore_min:x} e {turno.doppio_colpo.moltiplicatore_max:x} del normale. Anche in assalto il doppio colpo ha il {assalto.doppio_colpo.proc:pct} di attivarsi.",
    "Vigilante": "In sfida hai il {turno.cambio_proiettili_attacco.proc:pct} di cambiare munizioni in attacco e il {turno.cambio_proiettili_difesa.proc:pct} in difesa. ASSALTO — HARD COUNTER del Bersaglio enorme: se prova a deviare il tuo assalto, Vigilante impedisce la deviazione e mantieni il bersaglio scelto.",
    "Uomo di un tempo": "La vecchia scuola non molla: recuperi {turno.vitalita.hp} HP ogni turno in sfida e {assalto.vitalita.hp} HP durante l'assalto.",
    "Pazzoide glamour": "In sfida la pazzia si scatena nel {turno.pazzia.proc:pct} dei casi. In assalto hai il {assalto.cura_target.proc:pct} di ottenere la tua cura speciale.",
    "Combattente diretto": "Poche parole, molti numeri: parti con {bonus.hp:signed} HP, {bonus.atk:signed} attacco, {bonus.def:signed} difesa e {bonus.agi:signed} agilità.",
    "Lupo di mare": "Nei duelli fai il pirata fino in fondo: sottrai {ricompense.duello.punti_malus:abs} punti al risultato del tuo avversario.",
    "Cacciatore della feccia": "Finché il nemico non ha fatto più di {turno.difesa_sotto_soglia.fatto_max} danni, difendi con {turno.difesa_sotto_soglia.agi_difesa:signed} agilità e {turno.difesa_sotto_soglia.def_difesa:signed} difesa in più. In assalto hai il {assalto.massa_nemici.proc:pct} di crescere con il numero dei nemici.",
    "Sopravvissuto": "Hai il {assalto.sopravvive.proc:pct} di resistere meglio durante l'assalto e, quando vinci, aumenti del {ricompense.exp.bonus_probabilita_pct:pct} la possibilità di ottenere esperienza extra.",
    "Paladino": "Lo scudo ti segue ovunque: vale {boss.scudo.hp_scudo} HP contro i boss, {dungeon.scudo.hp_scudo} nei dungeon e {arena.scudo.hp_scudo} in arena. Finché regge, assorbe parte del colpo al posto tuo.",
    "Accolito": "Dopo aver inflitto almeno {turno.potere.danno_fatto_min} danni, il sacrificio ti premia con {turno.potere.atk:signed} attacco, {turno.potere.def:signed} difesa e {turno.potere.agi:signed} agilità. Quando difendi hai anche il {turno.difesa_cura.proc:pct} di curarti.",
    "Spacca Mostri": "Più vita ha il nemico, più male gli fai: in sfida aggiungi al colpo un quarto dei suoi HP. ASSALTO — HARD COUNTER del Clone: se lo scegli come bersaglio, al {assalto.clone.proc:pct} aggiungi {assalto.clone.dps:signed} DPS al colpo.",
    "Cavaliere del passaggio": "Sei fatto per tenere la posizione: il set ti dà {bonus.atk:signed} attacco e soprattutto {bonus.def:signed} difesa.",
    "Primo alla bandiera": "Quando vieni colpito hai il {turno.colpito.proc:pct} di trasformare parte del colpo in cura. ASSALTO — HARD COUNTER del Cannoncino: se lo scegli come bersaglio, al {assalto.cannoncino.proc:pct} aggiungi {assalto.cannoncino.dps:signed} DPS al colpo.",
    "Ice and fire": "Hai il {turno.calore.proc:pct} di scaldarti e guadagnare {turno.calore.atk:signed} ATK oppure il {turno.gelo.proc:pct} di congelare tutto e guadagnare {turno.gelo.def:signed} DEF. ASSALTO — HARD COUNTER del Sedimento del cucciolo: se lo scegli come bersaglio, al {assalto.drago_scaccia_drago.proc:pct} aggiungi {assalto.drago_scaccia_drago.dps:signed} DPS al colpo.",
    "MusicoSciamano": "La tua musica spegne le abilità dei set: durante la sfida né tu né il tuo avversario potete attivare gli effetti del set.",
    "Arciere di prima linea": "Hai il {turno.sfinimento.proc:pct} di sfinire il nemico e togliergli {turno.sfinimento.def_target:abs} difesa. In assalto il Fabbro ha il {assalto.fabbro.proc:pct} di darti {assalto.fabbro.atk_per_livello} attacco e {assalto.fabbro.def_per_livello} difesa per livello.",
    "Ghoul": "Hai il {turno.pressione.proc:pct} di mettere pressione al nemico e togliergli {turno.pressione.atk_target:abs} ATK e {turno.pressione.def_target:abs} DEF. ASSALTO — HARD COUNTER del Clone: quando lo incontri, al {assalto.terrore_clone.proc:pct} gli togli {assalto.terrore_clone.atk_clone:abs} ATK e {assalto.terrore_clone.def_clone:abs} DEF per quello scontro contro la struttura.",
    "Difensore delle mareggiate": "Hai il {turno.fauna.proc:pct} di ricevere aiuto da una creatura marina, dalla piccola sogliola fino alla balena. In assalto la fauna ha il {assalto.fauna.proc:pct} di regalarti {assalto.fauna.atk:signed} attacco.",
    "Taglialegna schivo": "Taglia e sparisci: il set ti dà {bonus.def:signed} difesa e {bonus.agi:signed} agilità.",
    "Cultista oscuro": "Nessun compromesso: il rituale ti concede direttamente {bonus.atk:signed} attacco.",
    "Dolce mietitore": "Sotto il mantello c'è molta più resistenza di quanto sembri: guadagni {bonus.def:signed} difesa.",
    "Sanguinolento": "Quando difendi hai il {turno.sangue_difesa.proc:pct} di trasformare il sangue perso in potere. In assalto l'effetto ha il {assalto.sangue.proc:pct} e usa una parte del tuo attacco e della tua difesa.",
    "Portatore di morte": "Hai il {turno.crescita.proc:pct} di crescere e guadagnare {turno.crescita.atk:signed} attacco, {turno.crescita.def:signed} difesa e {turno.crescita.agi:signed} agilità. Quando difendi puoi invece indebolire il nemico nel {turno.debuff_difesa.proc:pct} dei casi.",
    "Orrido": "Sghignolo decide quanto essere utile: in sfida compare nel {turno.sgignolo.proc:pct} dei casi. In assalto ha il {assalto.sgignolo.proc:pct} di infliggere {assalto.sgignolo.danno} danni.",
    "Guardiano del passaggio": "La morte non ti ferma facilmente: in sfida hai il {turno.resurrezione.proc:pct} di tornare con {turno.resurrezione.hp_base} HP, mentre in assalto hai il {assalto.resurrezione.proc:pct} di rialzarti con {assalto.resurrezione.hp} HP.",
    "Pyromante": "Tutto brucia meglio con più potere: il set ti dà direttamente {bonus.atk:signed} attacco.",
    "Uomo di classe": "Quando parte Spumeggiante copi la statistica dell'avversario per quel calcolo: in attacco hai il {turno.spumeggiante_attacco.proc:pct} di usare il suo attacco al posto del tuo, mentre in difesa hai il {turno.spumeggiante_difesa.proc:pct} di usare la sua difesa al posto della tua. In assalto hai il {assalto.spumeggiante.proc:pct} di usare attacco e difesa della struttura nemica, riducendone anche l'agilità di {assalto.spumeggiante.agi_difesa:abs}.",
    "Incantatore di controparte": "Hai l'{turno.potere_cosmico.proc:pct} di lanciare un potere cosmico e trasformare l'anello del tuo avversario in qualcosa di completamente diverso.",
    "Proiettile": "Sei molto più duro da fermare: quando difendi riduci di {turno.difesa.mod_delta:abs} il modificatore del colpo nemico; in assalto guadagni {assalto.difesa.def:signed} difesa.",
    "Cacciatore": "In sfida puoi sfruttare il tuo compagno Junior. ASSALTO — HARD COUNTER del Sedimento del cucciolo: se lo scegli come bersaglio, al {assalto.draghetto.proc:pct} aggiungi {assalto.draghetto.dps:signed} DPS al colpo.",
    "Pilota": "A fine partita sai sempre come portare a casa qualcosa in più: aumenti del {ricompense.exp.bonus_probabilita_pct:pct} la possibilità di esperienza extra e guadagni {ricompense.duello.punti_bonus:signed} punti nei duelli.",
    "Marines": "La tua armatura ha il {turno.armatura.proc:pct} di assorbire il colpo e ridurre i danni del {turno.armatura.riduzione_danno_percento:pct}.",
    "Armaliere": "Sai esattamente dove mettere il metallo: guadagni {bonus.atk:signed} attacco e {bonus.def:signed} difesa.",
    "Controllore del'entrata": "Nessuno passa senza essere visto: guadagni {bonus.hp:signed} HP e {bonus.agi:signed} agilità.",
    "Mariachi": "La musica può letteralmente rimetterti in piedi: quando difendi hai il {turno.resurrezione_difesa.proc:pct} di tornare con {turno.resurrezione_difesa.hp} HP e {turno.resurrezione_difesa.atk:signed} attacco. In assalto la resurrezione ha il {assalto.resurrezione.proc:pct}.",
    "Abitante": "Hai il {turno.radice.proc:pct} di piantare una radice che blocca il colpo e aumenta la tua difesa. In assalto gli alberelli hanno il {assalto.alberelli.proc:pct} di togliere {assalto.alberelli.bonus_atk_nemici:abs} attacco ai nemici.",
    "Cavaliere d'argento": "Se il tuo colpo esce troppo debole, recuperi fino a {turno.recupero_colpo.mod_bonus:signed} sul modificatore. In assalto, quando il colpo va a segno, aggiungi danno diretto pari al maggiore tra {assalto.danno_fisso.danno_minimo} e un centesimo dei tuoi HP massimi.",
    "Medico improvvisato": "Quando schivi hai il {turno.cura_schivata.proc:pct} di trasformare parte del colpo evitato in cura. In assalto hai il {assalto.cura.proc:pct} di recuperare {assalto.cura.cura} HP.",
    "Cavaliere delle spine": "Quando difendi hai il {turno.spine_difesa.proc:pct} di rimandare indietro parte del colpo. ASSALTO — HARD COUNTER dello Spuntone malefico: se lo eviti, al {assalto.spuntone_schivato.proc:pct} guadagni {assalto.spuntone_schivato.atk:signed} ATK e {assalto.spuntone_schivato.def:signed} DEF; se ti colpisce, al {assalto.spuntone_colpito.proc:pct} guadagni {assalto.spuntone_colpito.def:signed} DEF. I bonus restano per il resto dell'assalto.",
    "Selvaggio": "Non hai bisogno di magie: il vantaggio del set arriva dagli approcci, che diventano molto più aggressivi.",
    "Maestro delle tartarughe": "Hai il {turno.insegnamenti.proc:pct} di ricordare gli insegnamenti del vecchio saggio e togliere {turno.insegnamenti.riduzione_difesa_target} difesa al nemico. In assalto il carapace ha il {assalto.carapace.proc:pct} di darti {assalto.carapace.def:signed} difesa.",
    "Combattente 2D": "Hai il {turno.evocazione.proc:pct} di evocare un alleato casuale durante la sfida. In assalto il Raggio lunare ha il {assalto.raggio_lunare.proc:pct} di colpire con una potenza casuale.",
    "Guerriero 3D": "In sfida il tuo stile altera anche l'atterraggio dei colpi. ASSALTO — HARD COUNTER del Sedimento del cucciolo: quando lo incontri, al {assalto.cucciolo.proc:pct} neutralizzi completamente il suo attacco.",
    "Guaritore da campo": "Hai il {turno.rinsana.proc:pct} di recuperare vita mentre combatti. In assalto hai inoltre il {assalto.cura.proc:pct} di curarti di {assalto.cura.cura} HP.",
    "Combattente della taverna": "Birra, salsiccia e statistiche: guadagni {bonus.atk:signed} attacco e {bonus.def:signed} difesa.",
    "Ricercatore del pericolo": "Quando schivi hai il {turno.contrattacco_schivata.proc:pct} di rendere il contrattacco più pesante. In assalto l'adrenalina ha il {assalto.adrenalina.proc:pct} di darti {assalto.adrenalina.atk:signed} attacco.",
    "Ultima speranza": "Quando tutto va male, almeno le statistiche restano: guadagni {bonus.hp:signed} HP, {bonus.atk:signed} attacco e {bonus.def:signed} difesa. In assalto hai il {assalto.paura.proc:pct} di togliere {assalto.paura.bonus_def_nemico:abs} difesa al nemico.",
    "Elfo silvano": "La schivata diventa il tuo terreno di gioco: aumenti il bonus schivata di {turno.evasione.dogebonus}. In assalto hai il {assalto.evasione.proc:pct} di dimezzare il bonus agilità della difesa nemica.",
    "Juggernaut": "In sfida la tua massa porta l'agilità difensiva del nemico a {turno.peso.agi_difesa_mul:x} del normale. ASSALTO — HARD COUNTER del Cane da guardia: quando lo incontri, al {assalto.cane.proc:pct} la tua armatura neutralizza completamente il suo attacco.",
    "Ombra silenziosa": "In sfida puoi silenziare numerose abilità avversarie. ASSALTO — HARD COUNTER della Centrale di cura centralizzata: quando la incontri, al {assalto.centrale.proc:pct} la silenzi prima del suo impulso e guadagni {assalto.centrale.atk:signed} ATK, che resta per il resto dell'assalto.",
    "Crociato": "Se il nemico schiva, hai il {turno.punizione_schivata.proc:pct} di punirlo comunque. ASSALTO — HARD COUNTER del Muraglione extra: se scegli il Muraglione come bersaglio, al {assalto.muraglione.proc:pct} aggiungi altre {assalto.muraglione.moltiplicatore_extra} volte il DPS originale al colpo, oltre al colpo normale.",
    "Drago": "Le scaglie hanno il {turno.scaglie.proc:pct} di ridurre il colpo subito e possono anche danneggiare l'arma nemica. ASSALTO — HARD COUNTER del Sedimento del cucciolo: quando lo incontri, al {assalto.cucciolo.proc:pct} neutralizzi il suo attacco e guadagni {assalto.cucciolo.atk:signed} ATK, che resta per il resto dell'assalto.",
    "Maledetto": "Più sei vicino alla fine, più la maledizione diventa cattiva: hai il {turno.maledizione.proc:pct} di trasformare la vita mancante in danno. In assalto hai il {assalto.maledizione.proc:pct} di colpire per l'{assalto.maledizione.percento_hp:pct} degli HP.",
    "Medievalista": "Armatura solida e passo leggero: guadagni {bonus.def:signed} difesa e {bonus.agi:signed} agilità.",
    "Anima oscura": "In sfida hai il {turno.parry.proc:pct} di parare completamente il colpo e potenziare il tuo attacco. ASSALTO — HARD COUNTER del Fabbro incantaspade: quando lo incontri, al {assalto.fabbro.proc:pct} neutralizzi completamente il suo attacco.",
    "Macellaio": "La tua stessa vita diventa armatura: in sfida aggiungi alla difesa un decimo dei tuoi HP; in assalto ne usi un ventesimo.",
    "Chierico": "Hai il {turno.cura.proc:pct} di curarti automaticamente finché resti sotto {turno.cura.hp_max} HP. In assalto hai il {assalto.cura.proc:pct} di recuperare {assalto.cura.cura} HP.",
    "Betatester": "La Spada della beta ha il {turno.spada_beta.proc:pct} di illuminarsi e aggiungere {turno.spada_beta.danno} danni. In assalto ha ancora il {assalto.spada_beta.proc:pct} di scatenare {assalto.spada_beta.dps} danni.",
    "Cacciatore di bestie": "Il tuo istinto ti fa leggere l'avversario: in attacco hai il {turno.previsione_attacco.proc:pct} di ottenere un enorme vantaggio di agilità, in difesa il {turno.previsione_difesa.proc:pct}. In assalto la previsione ha il {assalto.previsione.proc:pct} di darti {assalto.previsione.agi:signed} agilità.",
    "Cacciatore di uomini": "Hai il {turno.trappola.proc:pct} di far finire il nemico in una trappola e ridurgli l'agilità di {turno.trappola.agi_target:abs}.",
    "Cultista pazzo": "Ogni turno il veleno decide se amarti o odiarti: hai il {turno.veleno_folle.proc:pct} di guadagnare {turno.veleno_folle.bonus_dps:signed} danni, altrimenti ne perdi {turno.veleno_folle.malus_dps}. In assalto l'ultimo colpo ha il {assalto.ultimo_colpo.proc:pct} di fare {assalto.ultimo_colpo.danno} danni.",
    "Druido della selva": "Hai il {turno.inselvatichisce.proc:pct} di crescere durante la sfida, guadagnando {turno.inselvatichisce.atk:signed} attacco, {turno.inselvatichisce.def:signed} difesa e {turno.inselvatichisce.agi:signed} agilità. In assalto la natura ti aiuta nel {assalto.natura.proc:pct} dei casi.",
    "Spaccatesta": "Il nome dice già abbastanza: parti con {bonus.atk:signed} attacco e {bonus.def:signed} difesa.",
    "Piarata": "Un po' di tutto, come un vero pirata: {bonus.atk:signed} attacco, {bonus.def:signed} difesa e {bonus.agi:signed} agilità.",
    "Vampiro": "Hai il {turno.morso.proc:pct} di mordere il nemico e recuperare vita, fino a {turno.morso.cura_cap} HP di cura. In assalto il pipistrello ha il {assalto.pipistrello.proc:pct} di darti {assalto.pipistrello.agi:signed} agilità.",
    "Teppistello duro": "Non sarà elegante, ma funziona: guadagni direttamente {bonus.def:signed} difesa.",
    "Segna ombre": "Hai il {turno.mimica_difesa.proc:pct} di copiare la difesa dell'avversario e usarla contro di lui.",
    "PiroIncantatore": "In sfida hai il {turno.golem_fuoco.proc:pct} di evocare il golem di fuoco. ASSALTO — HARD COUNTER del Sedimento del cucciolo: quando lo incontri, al {assalto.cucciolo_drago.proc:pct} neutralizzi il suo attacco e guadagni {assalto.cucciolo_drago.atk:signed} ATK, che resta per il resto dell'assalto.",
    "IppoFan": "In sfida hai il {turno.copia_attacco.proc:pct} di sfruttare l'attacco avversario. ASSALTO — HARD COUNTER del Cannoncino: quando lo incontri, al {assalto.cannoncino.proc:pct} lo confondi e neutralizzi completamente il suo attacco.",
    "Corvo": "Sei più difficile da seguire: il set modifica il bonus schivata di {turno.pressione_evasiva.dogebonus:signed} e ti dà anche {bonus.agi:signed} agilità.",
    "Apprendista delle paludi": "La palude ti rende decisamente più difficile da buttare giù: guadagni {bonus.hp:signed} HP.",
    "Eroe della rivolta": "Quando assalti insieme al clan, moltiplichi il tuo contributo per {assalto.supporto_clan.serv_mul:x}: più siete organizzati, più pesi nello scontro.",
    "Guardiano della bestie": "Ogni turno accumuli {turno.powe_per_turno} POWE e sblocchi aiuti sempre più forti: Volpe a {turno.volpe.powe_min}, Lupo a {turno.lupo.powe_min}, Ratti a {turno.ratti.powe_min}, Orsi a {turno.orsi.powe_min}, Serpenti a {turno.serpenti.powe_min} e Presenza lunare a {turno.presenza_lunare.powe_min}. Ogni creatura ha la sua possibilità di attivarsi.",
    "Incubo dei cieli": "Scendi dall'alto già pronto a fare male: guadagni {bonus.atk:signed} attacco e {bonus.def:signed} difesa.",
    "Cecchino modulare": "Ogni turno carichi {turno.powa_per_turno} POWA. A {turno.colpo_caricato.powa_min} POWA hai il {turno.colpo_caricato.proc:pct} di fare {turno.colpo_caricato.dps:signed} danni extra; a {turno.colpo_preciso.powa_min} puoi guadagnare {turno.colpo_preciso.agi:signed} agilità, a {turno.colpo_possente.powa_min} altri {turno.colpo_possente.dps:signed} danni, a {turno.cura_rapida.powa_min} curarti di {turno.cura_rapida.cura} HP e a {turno.colpo_perforante.powa_min} portare la difesa nemica a {turno.colpo_perforante.difesa_target}.",
    "Spadaccino Musashi": "La tua armatura riduce i danni subiti del {turno.riduzione_danno.danno_mul:rid_pct}. In assalto la difesa diventa {assalto.difesa.def_mul:x} quella normale.",
    "Eroe caduto": "Quando siete meno di {assalto.supporto_clan.compagni_soglia} nell'assalto, combatti meglio da solo e aumenti il tuo peso nello scontro di {assalto.supporto_clan.serv_bonus_nft:signed} o {assalto.supporto_clan.serv_bonus_bot:signed}, a seconda del percorso usato.",
    "Lanciatore olimpico": "In assalto hai il {assalto.tridente.proc:pct} di iniziare una raffica se la struttura scelta ha più di {assalto.tridente.hp_min} HP: il primo tridente infligge {assalto.tridente.danno} danni e poi colpisce le strutture successive perdendo {assalto.tridente.decremento} danni a ogni passaggio, fino a 0 o alla fine delle strutture.",
    "Gangster": "Hai il {turno.lega.proc:pct} di appendere il nemico a testa in giù e bloccarlo.",
    "Avventuriero delle praterie": "Hai il {turno.respira.proc:pct} di fermarti, respirare e tornare più forte con {turno.respira.atk:signed} attacco, {turno.respira.def:signed} difesa e {turno.respira.agi:signed} agilità.",
    "Difensore del popolo": "Se un compagno sta per cadere nel dungeon, puoi salvarlo lasciandolo ad almeno {dungeon.salvataggio_supporto.hp_salvato_min} HP e recuperando per lui metà della vita disponibile.",
    "Terrore delle ombre": "Hai il {turno.marchio.proc_aggiungi:pct} di marchiare il nemico. Quando i marchi sprigionano il loro potere, ognuno può regalarti {turno.marchio.atk_per_marchio:signed} attacco, {turno.marchio.def_per_marchio:signed} difesa e {turno.marchio.agi_per_marchio:signed} agilità.",
    "Oracolo del buio": "Hai il {turno.marchio.proc_aggiungi:pct} di marchiare il nemico. Quando i marchi si attivano, ogni marchio gli toglie {turno.marchio.atk_per_marchio:abs} attacco, {turno.marchio.def_per_marchio:abs} difesa e {turno.marchio.agi_per_marchio:abs} agilità.",
    "Ufficiale dell'oltretomba": "Hai il {turno.marchio.proc_aggiungi:pct} di marchiare il nemico e il {turno.demoni_difesa.proc:pct} di lasciare che siano i demoni a occuparsi del resto.",
    "Sciamano della verità": "Hai il {turno.marchio.proc_aggiungi:pct} di marchiare il nemico; quando il potere dei marchi si attiva, ogni marchio ti cura di {turno.marchio.cura_per_marchio} HP.",
    "Dannato": "Hai il {turno.marchio.proc_aggiungi:pct} di marchiare il nemico; quando i marchi bruciano, ognuno infligge {turno.marchio.danno_per_marchio} danni.",
    "Dipper": "Hai il {turno.marchio.proc_aggiungi:pct} di marchiare il nemico. Quando raggiunge almeno {turno.marchio.marchi_min} marchi, puoi far implodere lo scontro e dividere gli HP di entrambi per {turno.marchio.divisore_hp}.",
    "Re dei pirati": "Durante gli assalti dei tuoi compagni puoi cannonare da fuori: il colpo fa almeno {assalto.supporto_ciurma.danno_min} danni e cresce con il tuo attacco.",
    "Thunderlord": "In assalto hai l'{assalto.tuono.proc:pct} di scatenare {assalto.tuono.colpi} fulmini da {assalto.tuono.danno} danni ciascuno sulla struttura nemica.",
}

# --- SET EROI DELLA TEMPESTA: FRASI TECNICHE ---
FRASI_SET_TECNICHE.update({
    "Guerriero Temporale": "Sfida: HP fissati a {sfida.ciclo_temporale.hp}; fino a {sfida.ciclo_temporale.resurrezioni} resurrezioni, ciascuna di nuovo a 100 HP. Assalto: nessun effetto.",
    "Dannato primordiale": "Sfida/Assalto: converte il 100% della DEF posseduta in ATK e porta la DEF a 0.",
    "Macellatore": "Sfida: quando l'avversario schiva, {sfida.presa_schivata.proc:pct} di riacciuffarlo e infliggere {sfida.presa_schivata.moltiplicatore_danno:x} il danno normale. Assalto: nessun effetto.",
    "Mente centrale": "Assalto: per ogni struttura attraversata, {assalto.alieno.proc:pct} che un alieno infligga ATK/{assalto.alieno.divisore_atk}. Sfida: nessun effetto.",
    "Amletico": "Bonus base: +50 HP. Sfida/Assalto: {sfida.sacrificio.proc:pct} per sacrificare il {sfida.sacrificio.percento_hp:pct} degli HP correnti e aggiungerlo all'ATK del colpo.",
    "Accumulatore di meraviglie": "Sfida: ogni turno {sfida.evocazione.proc:pct} di evocare un oggetto. Il valore dell'oggetto aumenta il danno del proprio colpo o riduce quello nemico; gli oggetti di valore alto sono più rari.",
    "Anima della festa": "Sfida: +1 seguace per turno e +{sfida.seguaci.percento_stat_per_seguace:pct} HP/ATK/DEF/AGI per ogni seguace. Assalto: il contributo degli aiutanti recenti è moltiplicato per {assalto.last.moltiplicatore:x}.",
    "Zanno": "Bonus base permanente del set: +300 ATK.",
    "Uditore del profondo": "Sfida/Assalto: entrando esattamente a {sfida.richiamo.hp_trigger} HP infligge {sfida.richiamo.danno} danni al bersaglio.",
    "Monarca della tempesta di fuoco": "Sfida: possiede sempre Iridescente, Minimista, Primo impatto e Icore come incantamenti innati. Assalto: nessun effetto.",
    "Evocatore delle maree": "Assalto: attiva sempre Onde dell'abisso; alla morte infligge a tutte le strutture il {assalto.tsunami.percento_atk:pct} del proprio ATK. Sfida: nessun effetto.",
    "Mecha sciamano": "Sfida: perde {sfida.riuso_approccio.danno_hp} HP a ogni proprio turno e riapplica il moltiplicatore dell'approccio. Assalto: nessun effetto.",
})


# --- SECONDA ONDATA SET: FRASI TECNICHE ---
FRASI_SET_TECNICHE.update({
    "Anima persa": "Sfida: non può schivare. Ogni tiro che sarebbe stato una schivata concede {sfida.schivata_negata.hp} HP e il colpo prosegue normalmente.",
    "Disabilitatore provetto": "ASSALTO — HARD COUNTER del Muraglione extra: se lo scegli come bersaglio, il tuo ATK viene moltiplicato per {assalto.muraglione.atk_mul:x} per quell'assalto.",
    "Controllore del cielo": "Sfida: a fine di ogni turno, se hai guadagnato HP durante quel turno, guadagni ATK pari agli HP recuperati/{sfida.cura_in_potere.atk_divisore} e DEF pari agli HP recuperati/{sfida.cura_in_potere.def_divisore}.",
    "Eterna sventura": "Sfida: quando un tuo colpo va a segno hai il {sfida.sventura.proc:pct} di togliere {sfida.sventura.atk_target:abs} ATK, {sfida.sventura.def_target:abs} DEF e {sfida.sventura.agi_target:abs} AGI all'avversario.",
    "Pescatore alternativo": "Sfida: a ogni tuo turno hai il {sfida.azzardo.proc:pct} di moltiplicare permanentemente per {sfida.azzardo.atk_mul:x} l'ATK e per {sfida.azzardo.def_mul:x} la DEF. I proc successivi si accumulano fino a fine sfida.",
    "Esca vivente": "Sfida: all'inizio la DEF viene impostata a {sfida.esca.def}. Assalto: anche la DEF dell'assaltatore viene impostata a {assalto.esca.def}.",
    "Giustiziere a V": "Sfida: dal proprio turno {sfida.giudizio.turno_min} in poi l'AGI è moltiplicata una volta per {sfida.giudizio.agi_mul:x} e resta così fino a fine sfida. ASSALTO — HARD COUNTER dell'Accampamento: se lo bersagli, ATK ×{assalto.accampamento.atk_mul}.",
})


# --- TERZA ONDATA SET: NOVE SET ---
FRASI_SET_TECNICHE.update({
    "Monarca oscuro": "COMBATTIMENTO (vale anche in dungeon e boss): l'avversario inizia al {combattimento.inizio.hp_target_percento:pct} dei suoi HP. ASSALTO: all'inizio infliggi {assalto.last.danno_per_last} danni per ogni entry last attiva negli ultimi {assalto.last.finestra_secondi} secondi alla struttura scelta.",
    "Oscurato": "COMBATTIMENTO (vale anche in dungeon e boss): ogni danno subito ne riflette il {combattimento.riflesso.percento:pct} all'avversario. ASSALTO: ogni colpo delle difese subito riflette il {assalto.riflesso.percento:pct} alla struttura che lo ha inflitto.",
    "Demone delle lame": "COMBATTIMENTO (vale anche in dungeon e boss): ogni colpo andato a segno infligge il {combattimento.danno_extra.percento:pct} di danno extra. ASSALTO: il colpo alla struttura bersaglio infligge il {assalto.danno_extra.percento:pct} di danno extra.",
    "Re dei gadget": "COMBATTIMENTO (vale anche in dungeon e boss): all'inizio ottieni {combattimento.intelletto.int:signed} INT fino alla fine dello scontro.",
    "Il comico": "COMBATTIMENTO (vale anche in dungeon e boss): all'inizio compare un sonoro CLAP! A ogni turno l'avversario ha il {combattimento.confusione.proc:pct} di provare a colpirsi da solo; se non schiva, subisce il proprio colpo. ASSALTO: compare CLAP!, senza altri effetti.",
    "Survival medievale": "Bonus base sempre attivo in qualunque modalità: {bonus.hp:signed} HP.",
    "Duellista vermico": "COMBATTIMENTO e ASSALTO: il primo verme è garantito; poi hai il {combattimento.vermi.proc:pct} di mangiarne un altro, ripetendo finché fallisci. Ogni verme dà {combattimento.vermi.atk:signed} ATK, {combattimento.vermi.def:signed} DEF e {combattimento.vermi.hp:signed} HP.",
    "Cacciatore d'esce": "COMBATTIMENTO (vale anche in dungeon e boss): ogni colpo andato a segno ha il {combattimento.secondo_colpo.proc:pct} di generare un secondo colpo pari al {combattimento.secondo_colpo.percento_danno:pct} del primo. ASSALTO: stessa logica con {assalto.secondo_colpo.proc:pct} di probabilità e {assalto.secondo_colpo.percento_danno:pct} della forza del primo colpo.",
    "Duro a morire": "Bonus base sempre attivo in qualunque modalità: {bonus.def:signed} DEF.",
})


# --- QUARTA ONDATA SET: SEI SET ---
FRASI_SET_TECNICHE.update({
    "Primo alla torre": "COMBATTIMENTO (vale anche in dungeon e boss): il primo colpo che va a segno infligge il danno totale ×{combattimento.primo_colpo.moltiplicatore_danno}. ASSALTO — HARD COUNTER del Clone: se lo bersagli, ATK ×{assalto.clone.atk_mul}.",
    "Pazzo temporale": "COMBATTIMENTO (vale anche in dungeon e boss): a inizio scontro compare Snap! e hai il {combattimento.seed.proc:pct} di fissare il seed a {combattimento.seed.seed} per tutta la sequenza casuale dello scontro. ASSALTO: stessa logica con il {assalto.seed.proc:pct}.",
    "Evocatore del vero potere": "COMBATTIMENTO (vale anche in dungeon e boss): prima di ogni tuo attacco compare un canto; hai il {combattimento.canto.proc:pct} di sostituire il tuo anello per il resto dello scontro con {combattimento.canto.anello}.",
    "GunSlingher": "COMBATTIMENTO (vale anche in dungeon e boss): a inizio scontro spari da {combattimento.raffica.colpi_min} a {combattimento.raffica.colpi_max} colpi prima della normale azione, ciascuno da {combattimento.raffica.danno_per_colpo} danni. ASSALTO: se esiste un Clone gli spari da {assalto.raffica_clone.colpi_min} a {assalto.raffica_clone.colpi_max} colpi da {assalto.raffica_clone.danno_per_colpo} danni prima che reagisca.",
    "Arcidemone": "COMBATTIMENTO (vale anche in dungeon e boss): quando l'avversario recupera HP durante un turno, guadagni {combattimento.cura_nemica.atk:signed} ATK per il resto dello scontro.",
    "Big Game Hunter": "COMBATTIMENTO (vale anche in dungeon e boss): all'inizio dello scontro imposti la tua AGI uguale all'AGI corrente dell'avversario.",
})


# --- QUINTA ONDATA SET: TREDICI SET ---
FRASI_SET_TECNICHE.update({
    "Nucleo dell'uragano": "COMBATTIMENTO (anche dungeon/boss): ogni volta che un anello avversario procca, il vento infligge al proprietario dell'anello danni puliti pari al {combattimento.proc_anello_avversario.percento_atk_proprio:pct} del tuo ATK. ASSALTO: non subisci danni dallo {assalto.immunita.struttura}.",
    "Tormento di fuoco": "COMBATTIMENTO (anche dungeon/boss): ogni volta che un anello avversario procca, il proprietario dell'anello subisce danni puliti pari al {combattimento.proc_anello_avversario.percento_atk_avversario:pct} del proprio ATK. ASSALTO: non subisci danni dal {assalto.immunita.struttura}.",
    "Girarrosto": "COMBATTIMENTO (anche dungeon/boss): la prima volta che scendi sotto il {combattimento.salvezza.hp_soglia_percento:pct} degli HP iniziali torni al {combattimento.salvezza.hp_ripristino_percento:pct}. ASSALTO: stessa salvezza, una volta per assalto.",
    "Venere di ferro": "COMBATTIMENTO (anche dungeon/boss): ogni perdita di HP viene ridotta del {combattimento.riduzione_danno.percento:pct}. ASSALTO: la riduzione sale al {assalto.riduzione_danno.percento:pct}.",
    "Rosso D'ossidina": "COMBATTIMENTO (anche dungeon/boss): dopo ogni colpo riuscito riapplichi il tuo approccio e il log mostra in cosa stai diventando più estremo. ASSALTO: non subisci danni dal {assalto.immunita.struttura}.",
    "Oltraggioso": "COMBATTIMENTO (anche dungeon/boss): finché partecipi allo scontro, ogni singola perdita di HP o Scudo di entrambi i combattenti è limitata a un massimo di {combattimento.cap_danno.massimo} danni. ASSALTO: non subisci danni dalla {assalto.immunita.struttura}.",
    "Festante oscuro": "COMBATTIMENTO (anche dungeon/boss): i fantasmi assorbono al posto tuo ogni perdita di HP; all'inizio di ogni tuo turno subisci il {combattimento.fantasmi.percento_ritorno:pct} del danno ancora accumulato nei fantasmi e quel valore viene rimosso dal loro accumulo. ASSALTO: non subisci danni dal {assalto.immunita.struttura}.",
    "Legionaro di Evelin": "COMBATTIMENTO (anche dungeon/boss): nei tuoi turni {combattimento.danno_turno.parita}, se il colpo non viene schivato e va a segno, infliggi altri {combattimento.danno_turno.danno} danni puliti. ASSALTO: non subisci danni dall'{assalto.immunita.struttura}.",
    "Neo Genesi": "COMBATTIMENTO (anche dungeon/boss): nei tuoi turni {combattimento.danno_turno.parita}, se il colpo non viene schivato e va a segno, infliggi altri {combattimento.danno_turno.danno} danni puliti. ASSALTO: non subisci danni dallo {assalto.immunita.struttura}.",
    "Intermezzo": "COMBATTIMENTO (anche dungeon/boss): ogni schivata concede una carica. Da {combattimento.cariche_schivata.soglia_1} cariche aggiungi {combattimento.cariche_schivata.bonus_1} danni; da {combattimento.cariche_schivata.soglia_2} aggiungi anche altri {combattimento.cariche_schivata.bonus_2}; da {combattimento.cariche_schivata.soglia_3} il danno risultante viene inoltre moltiplicato ×{combattimento.cariche_schivata.moltiplicatore}. ASSALTO: non subisci danni dal {assalto.immunita.struttura}.",
    "Obscurio": "COMBATTIMENTO (anche dungeon/boss): l'avversario non può aumentare i propri HP tramite cure finché è vivo; le resurrezioni da 0 HP o meno restano possibili. ASSALTO: non subisci danni dalla {assalto.immunita.struttura}.",
    "Primo al comando": "COMBATTIMENTO (anche dungeon/boss): ogni proc di qualsiasi anello nello scontro ti cura di {combattimento.proc_anello.cura} HP. ASSALTO: non subisci danni dal {assalto.immunita.struttura}.",
    "Luce persa": "COMBATTIMENTO (anche dungeon/boss): a inizio scontro calcoli AGI ×{combattimento.conversione.agi_mul}; il {combattimento.conversione.quota_atk:pct_mul} va in ATK e il {combattimento.conversione.quota_def:pct_mul} in DEF, poi AGI diventa 0. ASSALTO: stessa conversione prima dell'assalto.",
})

# --- COMPLETEZZA AUTOMATICA FRASI SET: INIZIO ---
# Blocco statico generato confrontando FRASI_SET_TECNICHE con tutte le foglie di PROC_CLASSI.
# Serve a rendere visibile ogni parametro di tuning nella scheda tecnica dell'NFT.
FRASI_SET_TECNICHE.update({'Cecchino modulare': 'Ogni turno carichi {turno.powa_per_turno} POWA. A {turno.colpo_caricato.powa_min} POWA hai il {turno.colpo_caricato.proc:pct} di fare '
                      '{turno.colpo_caricato.dps:signed} danni extra; a {turno.colpo_preciso.powa_min} puoi guadagnare {turno.colpo_preciso.agi:signed} '
                      'agilità, a {turno.colpo_possente.powa_min} altri {turno.colpo_possente.dps:signed} danni, a {turno.cura_rapida.powa_min} curarti di '
                      '{turno.cura_rapida.cura} HP e a {turno.colpo_perforante.powa_min} portare la difesa nemica a {turno.colpo_perforante.difesa_target}. '
                      'PARAMETRI COMPLETI — turno.colpo_preciso.proc={turno.colpo_preciso.proc}; turno.colpo_possente.proc={turno.colpo_possente.proc}; '
                      'turno.cura_rapida.proc={turno.cura_rapida.proc}; turno.colpo_perforante.proc={turno.colpo_perforante.proc}.',
 'Chierico': 'Hai il {turno.cura.proc:pct} di curarti automaticamente finché resti sotto {turno.cura.hp_max} HP. In assalto hai il {assalto.cura.proc:pct} di '
             'recuperare {assalto.cura.cura} HP. PARAMETRI COMPLETI — turno.cura.cura_percento_hp={turno.cura.cura_percento_hp}; '
             'turno.cura.cura_base={turno.cura.cura_base}.',
 'Vigilante': 'In sfida hai il {turno.cambio_proiettili_attacco.proc:pct} di cambiare munizioni in attacco e il {turno.cambio_proiettili_difesa.proc:pct} in '
              'difesa. ASSALTO — HARD COUNTER del Bersaglio enorme: se prova a deviare il tuo assalto, Vigilante impedisce la deviazione e mantieni il '
              'bersaglio scelto. PARAMETRI COMPLETI — turno.cambio_proiettili_attacco.bonus_difesa={turno.cambio_proiettili_attacco.bonus_difesa}.',
 'Druido della selva': 'Hai il {turno.inselvatichisce.proc:pct} di crescere durante la sfida, guadagnando {turno.inselvatichisce.atk:signed} attacco, '
                       '{turno.inselvatichisce.def:signed} difesa e {turno.inselvatichisce.agi:signed} agilità. In assalto la natura ti aiuta nel '
                       '{assalto.natura.proc:pct} dei casi. PARAMETRI COMPLETI — assalto.natura.atk={assalto.natura.atk}; '
                       'assalto.natura.def={assalto.natura.def}; assalto.natura.agi={assalto.natura.agi}.',
 'PiroIncantatore': 'In sfida hai il {turno.golem_fuoco.proc:pct} di evocare il golem di fuoco. ASSALTO — HARD COUNTER del Sedimento del cucciolo: quando lo '
                    'incontri, al {assalto.cucciolo_drago.proc:pct} neutralizzi il suo attacco e guadagni {assalto.cucciolo_drago.atk:signed} ATK, che resta '
                    "per il resto dell'assalto. PARAMETRI COMPLETI — turno.golem_fuoco.agi={turno.golem_fuoco.agi}; "
                    'turno.golem_fuoco.dps_da_def_divisore={turno.golem_fuoco.dps_da_def_divisore}.',
 'Arciere di prima linea': 'Hai il {turno.sfinimento.proc:pct} di sfinire il nemico e togliergli {turno.sfinimento.def_target:abs} difesa. In assalto il '
                           'Fabbro ha il {assalto.fabbro.proc:pct} di darti {assalto.fabbro.atk_per_livello} attacco e {assalto.fabbro.def_per_livello} difesa '
                           'per livello. PARAMETRI COMPLETI — turno.sfinimento.def_min={turno.sfinimento.def_min}.',
 'Portatore di morte': 'Hai il {turno.crescita.proc:pct} di crescere e guadagnare {turno.crescita.atk:signed} attacco, {turno.crescita.def:signed} difesa e '
                       '{turno.crescita.agi:signed} agilità. Quando difendi puoi invece indebolire il nemico nel {turno.debuff_difesa.proc:pct} dei casi. '
                       'PARAMETRI COMPLETI — turno.debuff_difesa.atk={turno.debuff_difesa.atk}; turno.debuff_difesa.def={turno.debuff_difesa.def}; '
                       'turno.debuff_difesa.agi={turno.debuff_difesa.agi}; assalto.bonus_gadget.moltiplicatore={assalto.bonus_gadget.moltiplicatore}.',
 'Contrabbandiere': 'Hai il {turno.piazza_carica.proc:pct} di piazzare una carica sul nemico; quando esplode, ogni carica vale '
                    '{turno.detonazione.danno_per_carica} danni. ASSALTO — HARD COUNTER della Stazione laser di sicurezza: quando la incontri, al '
                    '{assalto.laser.proc:pct} neutralizzi completamente il suo attacco. PARAMETRI COMPLETI — turno.detonazione.proc={turno.detonazione.proc}; '
                    'turno.detonazione.hp_trigger={turno.detonazione.hp_trigger}; turno.detonazione.cariche_trigger={turno.detonazione.cariche_trigger}; '
                    'turno.piazza_carica.cariche={turno.piazza_carica.cariche}.',
 'Terrore delle ombre': 'Hai il {turno.marchio.proc_aggiungi:pct} di marchiare il nemico. Quando i marchi sprigionano il loro potere, ognuno può regalarti '
                        '{turno.marchio.atk_per_marchio:signed} attacco, {turno.marchio.def_per_marchio:signed} difesa e '
                        '{turno.marchio.agi_per_marchio:signed} agilità. PARAMETRI COMPLETI — turno.marchio.proc_effetto={turno.marchio.proc_effetto}.',
 'Oracolo del buio': 'Hai il {turno.marchio.proc_aggiungi:pct} di marchiare il nemico. Quando i marchi si attivano, ogni marchio gli toglie '
                     '{turno.marchio.atk_per_marchio:abs} attacco, {turno.marchio.def_per_marchio:abs} difesa e {turno.marchio.agi_per_marchio:abs} agilità. '
                     'PARAMETRI COMPLETI — turno.marchio.proc_effetto={turno.marchio.proc_effetto}.',
 'Sciamano della verità': 'Hai il {turno.marchio.proc_aggiungi:pct} di marchiare il nemico; quando il potere dei marchi si attiva, ogni marchio ti cura di '
                          '{turno.marchio.cura_per_marchio} HP. PARAMETRI COMPLETI — turno.marchio.proc_effetto={turno.marchio.proc_effetto}.',
 'Dannato': 'Hai il {turno.marchio.proc_aggiungi:pct} di marchiare il nemico; quando i marchi bruciano, ognuno infligge {turno.marchio.danno_per_marchio} '
            'danni. PARAMETRI COMPLETI — turno.marchio.proc_effetto={turno.marchio.proc_effetto}.',
 'Dipper': 'Hai il {turno.marchio.proc_aggiungi:pct} di marchiare il nemico. Quando raggiunge almeno {turno.marchio.marchi_min} marchi, puoi far implodere lo '
           'scontro e dividere gli HP di entrambi per {turno.marchio.divisore_hp}. PARAMETRI COMPLETI — '
           'turno.marchio.proc_effetto={turno.marchio.proc_effetto}.',
 'Cacciatore di bestie': "Il tuo istinto ti fa leggere l'avversario: in attacco hai il {turno.previsione_attacco.proc:pct} di ottenere un enorme vantaggio di "
                         'agilità, in difesa il {turno.previsione_difesa.proc:pct}. In assalto la previsione ha il {assalto.previsione.proc:pct} di darti '
                         '{assalto.previsione.agi:signed} agilità. PARAMETRI COMPLETI — turno.previsione_attacco.agi={turno.previsione_attacco.agi}; '
                         'turno.previsione_difesa.agi={turno.previsione_difesa.agi}.',
 'Ricercatore del pericolo': "Quando schivi hai il {turno.contrattacco_schivata.proc:pct} di rendere il contrattacco più pesante. In assalto l'adrenalina ha "
                             'il {assalto.adrenalina.proc:pct} di darti {assalto.adrenalina.atk:signed} attacco. PARAMETRI COMPLETI — '
                             'turno.contrattacco_schivata.mod={turno.contrattacco_schivata.mod}.',
 'Maledetto': 'Più sei vicino alla fine, più la maledizione diventa cattiva: hai il {turno.maledizione.proc:pct} di trasformare la vita mancante in danno. In '
              "assalto hai il {assalto.maledizione.proc:pct} di colpire per l'{assalto.maledizione.percento_hp:pct} degli HP. PARAMETRI COMPLETI — "
              'turno.maledizione.hp_riferimento={turno.maledizione.hp_riferimento}; turno.maledizione.danno_min={turno.maledizione.danno_min}.',
 'Campione del sole': 'Più aspetti, più il colpo diventa pericoloso: sotto {turno.colpo_caricato.hp_trigger} HP puoi scaricarlo già dopo '
                      '{turno.colpo_caricato.mol_min_hp} cariche, altrimenti ne servono almeno {turno.colpo_caricato.mol_min_fallback}. ASSALTO — HARD COUNTER '
                      'del Fabbro incantaspade: quando lo incontri, al {assalto.fabbro.proc:pct} eviti il suo attacco e guadagni {assalto.fabbro.atk:signed} '
                      "ATK e {assalto.fabbro.def:signed} DEF, che restano per il resto dell'assalto. PARAMETRI COMPLETI — "
                      'turno.colpo_caricato.proc_fallback={turno.colpo_caricato.proc_fallback}; '
                      'turno.colpo_caricato.moltiplicatore={turno.colpo_caricato.moltiplicatore}.',
 'Drago': "Le scaglie hanno il {turno.scaglie.proc:pct} di ridurre il colpo subito e possono anche danneggiare l'arma nemica. ASSALTO — HARD COUNTER del "
          'Sedimento del cucciolo: quando lo incontri, al {assalto.cucciolo.proc:pct} neutralizzi il suo attacco e guadagni {assalto.cucciolo.atk:signed} ATK, '
          "che resta per il resto dell'assalto. PARAMETRI COMPLETI — turno.scaglie.riduzione_mod={turno.scaglie.riduzione_mod}; "
          'turno.scaglie.proc_rottura_arma={turno.scaglie.proc_rottura_arma}; turno.scaglie.atk_target={turno.scaglie.atk_target}.',
 'Anima oscura': 'In sfida hai il {turno.parry.proc:pct} di parare completamente il colpo e potenziare il tuo attacco. ASSALTO — HARD COUNTER del Fabbro '
                 'incantaspade: quando lo incontri, al {assalto.fabbro.proc:pct} neutralizzi completamente il suo attacco. PARAMETRI COMPLETI — '
                 'turno.parry.moltiplicatore_atk={turno.parry.moltiplicatore_atk}.',
 'Abitante': 'Hai il {turno.radice.proc:pct} di piantare una radice che blocca il colpo e aumenta la tua difesa. In assalto gli alberelli hanno il '
             '{assalto.alberelli.proc:pct} di togliere {assalto.alberelli.bonus_atk_nemici:abs} attacco ai nemici. PARAMETRI COMPLETI — '
             'turno.radice.moltiplicatore_def={turno.radice.moltiplicatore_def}.',
 'Marines': 'La tua armatura ha il {turno.armatura.proc:pct} di assorbire il colpo e ridurre i danni del {turno.armatura.riduzione_danno_percento:pct}. '
            'PARAMETRI COMPLETI — turno.armatura.danno_min={turno.armatura.danno_min}.',
 'Shogun moderno': 'Hai il {turno.doppio_colpo.proc:pct} di sferrare un secondo colpo, con forza tra {turno.doppio_colpo.moltiplicatore_min:x} e '
                   '{turno.doppio_colpo.moltiplicatore_max:x} del normale. Anche in assalto il doppio colpo ha il {assalto.doppio_colpo.proc:pct} di '
                   'attivarsi. PARAMETRI COMPLETI — assalto.doppio_colpo.denominatore={assalto.doppio_colpo.denominatore}; '
                   'assalto.doppio_colpo.random_min={assalto.doppio_colpo.random_min}; assalto.doppio_colpo.random_max={assalto.doppio_colpo.random_max}.',
 'Manipolatore di morte': 'Hai il {turno.scheletri.proc:pct} di richiamare scheletri quando ti manca vita: ne arriva uno ogni '
                          '{turno.scheletri.hp_per_scheletro} HP mancanti rispetto a {turno.scheletri.hp_riferimento}. In assalto la loro distrazione ha il '
                          '{assalto.distrazione.proc:pct} di darti {assalto.distrazione.agi:signed} agilità. PARAMETRI COMPLETI — '
                          'turno.scheletri.mod_min={turno.scheletri.mod_min}; turno.scheletri.mod_max={turno.scheletri.mod_max}; '
                          'turno.scheletri.crescita_danno_scudo={turno.scheletri.crescita_danno_scudo}; '
                          'turno.scheletri.crescita_danno_hp={turno.scheletri.crescita_danno_hp}.',
 'Mago mentale': 'Hai il {turno.showtime.proc:pct} di prendere il controllo dello scontro e scatenare da {turno.showtime.colpi_min} a '
                 "{turno.showtime.colpi_max} colpi. Attenzione: c'è anche il {turno.showtime.autodanno_proc:pct} che il potere ti si ritorca contro. PARAMETRI "
                 'COMPLETI — turno.showtime.mod_min={turno.showtime.mod_min}; turno.showtime.mod_max={turno.showtime.mod_max}; '
                 'turno.showtime.crescita_danno={turno.showtime.crescita_danno}.',
 'Guardiano della bestie': 'Ogni turno accumuli {turno.powe_per_turno} POWE e sblocchi aiuti sempre più forti: Volpe a {turno.volpe.powe_min}, Lupo a '
                           '{turno.lupo.powe_min}, Ratti a {turno.ratti.powe_min}, Orsi a {turno.orsi.powe_min}, Serpenti a {turno.serpenti.powe_min} e '
                           'Presenza lunare a {turno.presenza_lunare.powe_min}. Ogni creatura ha la sua possibilità di attivarsi. PARAMETRI COMPLETI — '
                           'turno.volpe.proc={turno.volpe.proc}; turno.volpe.def={turno.volpe.def}; turno.lupo.proc={turno.lupo.proc}; '
                           'turno.lupo.atk={turno.lupo.atk}; turno.ratti.proc={turno.ratti.proc}; turno.ratti.agi={turno.ratti.agi}; '
                           'turno.orsi.proc={turno.orsi.proc}; turno.orsi.atk={turno.orsi.atk}; turno.serpenti.proc={turno.serpenti.proc}; '
                           'turno.serpenti.agi_target={turno.serpenti.agi_target}; turno.presenza_lunare.proc={turno.presenza_lunare.proc}; '
                           'turno.presenza_lunare.def_mul={turno.presenza_lunare.def_mul}.',
 'Fiamma pura': 'Hai il {turno.arena_brucia.proc:pct} di incendiare entrambi e togliere {turno.arena_brucia.danno_main} HP a testa. Se muori durante un '
                'assalto, hai il {assalto.esplosione_morte.proc:pct} di esplodere: ogni struttura con abbastanza vita subisce il maggiore tra '
                '{assalto.esplosione_morte.danno_minimo} danni e un centesimo dei tuoi HP massimi. PARAMETRI COMPLETI — '
                'turno.arena_brucia.danno_oppo={turno.arena_brucia.danno_oppo}; '
                'assalto.esplosione_morte.hp_massimi_divisore={assalto.esplosione_morte.hp_massimi_divisore}.',
 'Crociato': 'Se il nemico schiva, hai il {turno.punizione_schivata.proc:pct} di punirlo comunque. ASSALTO — HARD COUNTER del Muraglione extra: se scegli il '
             'Muraglione come bersaglio, al {assalto.muraglione.proc:pct} aggiungi altre {assalto.muraglione.moltiplicatore_extra} volte il DPS originale al '
             'colpo, oltre al colpo normale. PARAMETRI COMPLETI — turno.punizione_schivata.divisore_dps={turno.punizione_schivata.divisore_dps}; '
             'turno.punizione_schivata.random_min={turno.punizione_schivata.random_min}; '
             'turno.punizione_schivata.random_max={turno.punizione_schivata.random_max}; '
             'turno.punizione_schivata.danno_min={turno.punizione_schivata.danno_min}.',
 'Medico improvvisato': 'Quando schivi hai il {turno.cura_schivata.proc:pct} di trasformare parte del colpo evitato in cura. In assalto hai il '
                        '{assalto.cura.proc:pct} di recuperare {assalto.cura.cura} HP. PARAMETRI COMPLETI — '
                        'turno.cura_schivata.divisore_dps={turno.cura_schivata.divisore_dps}; turno.cura_schivata.random_min={turno.cura_schivata.random_min}; '
                        'turno.cura_schivata.random_max={turno.cura_schivata.random_max}.',
 'Vampiro': 'Hai il {turno.morso.proc:pct} di mordere il nemico e recuperare vita, fino a {turno.morso.cura_cap} HP di cura. In assalto il pipistrello ha il '
            '{assalto.pipistrello.proc:pct} di darti {assalto.pipistrello.agi:signed} agilità. PARAMETRI COMPLETI — '
            'turno.morso.divisore={turno.morso.divisore}; turno.morso.cap_trigger={turno.morso.cap_trigger}.',
 'Guaritore da campo': 'Hai il {turno.rinsana.proc:pct} di recuperare vita mentre combatti. In assalto hai inoltre il {assalto.cura.proc:pct} di curarti di '
                       '{assalto.cura.cura} HP. PARAMETRI COMPLETI — turno.rinsana.divisore={turno.rinsana.divisore}.',
 'Cacciatore': 'In sfida puoi sfruttare il tuo compagno Junior. ASSALTO — HARD COUNTER del Sedimento del cucciolo: se lo scegli come bersaglio, al '
               '{assalto.draghetto.proc:pct} aggiungi {assalto.draghetto.dps:signed} DPS al colpo. PARAMETRI COMPLETI — turno.junior.proc={turno.junior.proc}; '
               'turno.junior.denominatore={turno.junior.denominatore}; turno.junior.moltiplicatore={turno.junior.moltiplicatore}.',
 'Orrido': 'Sghignolo decide quanto essere utile: in sfida compare nel {turno.sgignolo.proc:pct} dei casi. In assalto ha il {assalto.sgignolo.proc:pct} di '
           'infliggere {assalto.sgignolo.danno} danni. PARAMETRI COMPLETI — turno.sgignolo.denominatore={turno.sgignolo.denominatore}; '
           'turno.sgignolo.moltiplicatore={turno.sgignolo.moltiplicatore}; assalto.danno_target={assalto.danno_target}.',
 'Primo alla bandiera': 'Quando vieni colpito hai il {turno.colpito.proc:pct} di trasformare parte del colpo in cura. ASSALTO — HARD COUNTER del Cannoncino: '
                        'se lo scegli come bersaglio, al {assalto.cannoncino.proc:pct} aggiungi {assalto.cannoncino.dps:signed} DPS al colpo. PARAMETRI '
                        'COMPLETI — turno.colpito.divisore_bonus={turno.colpito.divisore_bonus}; turno.colpito.cura_divisore={turno.colpito.cura_divisore}.',
 'Difensore delle mareggiate': 'Hai il {turno.fauna.proc:pct} di ricevere aiuto da una creatura marina, dalla piccola sogliola fino alla balena. In assalto la '
                               'fauna ha il {assalto.fauna.proc:pct} di regalarti {assalto.fauna.atk:signed} attacco. PARAMETRI COMPLETI — '
                               'turno.fauna.soglia_sogliola={turno.fauna.soglia_sogliola}; turno.fauna.sogliola_min={turno.fauna.sogliola_min}; '
                               'turno.fauna.sogliola_max={turno.fauna.sogliola_max}; turno.fauna.soglia_scorpione={turno.fauna.soglia_scorpione}; '
                               'turno.fauna.scorpione_min={turno.fauna.scorpione_min}; turno.fauna.scorpione_max={turno.fauna.scorpione_max}; '
                               'turno.fauna.soglia_spada={turno.fauna.soglia_spada}; turno.fauna.spada_min={turno.fauna.spada_min}; '
                               'turno.fauna.spada_max={turno.fauna.spada_max}; turno.fauna.balena_min={turno.fauna.balena_min}; '
                               'turno.fauna.balena_max={turno.fauna.balena_max}.',
 'Cercatore di reliquie': 'Hai il {turno.reliquia.proc:pct} di trovare una reliquia durante la sfida: può regalarti {turno.reliquia.agi:signed} agilità, '
                          '{turno.reliquia.hp:signed} HP, {turno.reliquia.def:signed} difesa oppure {turno.reliquia.atk:signed} attacco. ASSALTO — HARD '
                          'COUNTER del Cannoncino: se scegli il Cannoncino come bersaglio, al {assalto.cannoncino.proc:pct} guadagni '
                          "{assalto.cannoncino.def:signed} DEF per l'assalto. PARAMETRI COMPLETI — turno.reliquia.soglia1={turno.reliquia.soglia1}; "
                          'turno.reliquia.soglia2={turno.reliquia.soglia2}; turno.reliquia.soglia3={turno.reliquia.soglia3}.',
 'Fire lord': 'Hai il {turno.muori_insetto.proc:pct} di bruciare il nemico per {turno.muori_insetto.danno} danni. In assalto puoi concatenare fino a '
              '{assalto.catena.tentativi} colpi da {assalto.catena.danno} danni ciascuno. PARAMETRI COMPLETI — '
              'assalto.catena.stop_proc={assalto.catena.stop_proc}; assalto.catena.hp_min={assalto.catena.hp_min}.',
 'Combattente 2D': 'Hai il {turno.evocazione.proc:pct} di evocare un alleato casuale durante la sfida. In assalto il Raggio lunare ha il '
                   '{assalto.raggio_lunare.proc:pct} di colpire con una potenza casuale. PARAMETRI COMPLETI — '
                   'turno.evocazione.soglia_occhio={turno.evocazione.soglia_occhio}; turno.evocazione.soglia_zombie={turno.evocazione.soglia_zombie}; '
                   'turno.evocazione.soglia_raggio={turno.evocazione.soglia_raggio}; turno.evocazione.atk={turno.evocazione.atk}; '
                   'turno.evocazione.def={turno.evocazione.def}; turno.evocazione.agi={turno.evocazione.agi}; '
                   'turno.evocazione.danno_zombie={turno.evocazione.danno_zombie}; turno.evocazione.raggio_min={turno.evocazione.raggio_min}; '
                   'turno.evocazione.raggio_max={turno.evocazione.raggio_max}; assalto.raggio_lunare.denominatore={assalto.raggio_lunare.denominatore}; '
                   'assalto.raggio_lunare.random_min={assalto.raggio_lunare.random_min}; assalto.raggio_lunare.random_max={assalto.raggio_lunare.random_max}.',
 'Accolito': 'Dopo aver inflitto almeno {turno.potere.danno_fatto_min} danni, il sacrificio ti premia con {turno.potere.atk:signed} attacco, '
             '{turno.potere.def:signed} difesa e {turno.potere.agi:signed} agilità. Quando difendi hai anche il {turno.difesa_cura.proc:pct} di curarti. '
             'PARAMETRI COMPLETI — turno.potere.hp={turno.potere.hp}; turno.difesa_cura.divisore={turno.difesa_cura.divisore}; '
             'turno.difesa_cura.base={turno.difesa_cura.base}.',
 'Esperto di animali': 'Scegli la creatura giusta e lascia che combatta con te. Il Dragone delle stelle ha il {turno.dragone_stelle.proc:pct} di portare il '
                       'tuo danno a {turno.dragone_stelle.dps_mul:x}, la Balena territoriale ha il {turno.balena_territoriale.proc:pct} di darti '
                       '{turno.balena_territoriale.def:signed} difesa e il Silvantropo ha il {turno.silvantropo.proc:pct} di curarti di '
                       '{turno.silvantropo.cura} HP. PARAMETRI COMPLETI — turno.fantasma_ritorno.proc={turno.fantasma_ritorno.proc}; '
                       'turno.fantasma_ritorno.dps_mul={turno.fantasma_ritorno.dps_mul}; turno.ratto_tombe.hp_target_max={turno.ratto_tombe.hp_target_max}; '
                       'turno.orsodruido.proc={turno.orsodruido.proc}; turno.orsodruido.random_min={turno.orsodruido.random_min}; '
                       'turno.orsodruido.random_max={turno.orsodruido.random_max}.',
 'Sanguinolento': "Quando difendi hai il {turno.sangue_difesa.proc:pct} di trasformare il sangue perso in potere. In assalto l'effetto ha il "
                  '{assalto.sangue.proc:pct} e usa una parte del tuo attacco e della tua difesa. PARAMETRI COMPLETI — '
                  'turno.sangue_difesa.divisore={turno.sangue_difesa.divisore}; assalto.sangue.divisore_atk={assalto.sangue.divisore_atk}; '
                  'assalto.sangue.divisore_def={assalto.sangue.divisore_def}.',
 "Ufficiale dell'oltretomba": 'Hai il {turno.marchio.proc_aggiungi:pct} di marchiare il nemico e il {turno.demoni_difesa.proc:pct} di lasciare che siano i '
                              'demoni a occuparsi del resto. PARAMETRI COMPLETI — turno.demoni_difesa.random_min={turno.demoni_difesa.random_min}; '
                              'turno.demoni_difesa.random_max={turno.demoni_difesa.random_max}.',
 'Cercatore': "Quando difendi hai il {turno.demoni_difesa.proc:pct} di richiamare i demoni in tuo aiuto. ASSALTO — HARD COUNTER dell'Accampamento: quando lo "
              'incontri, al {assalto.accampamento.proc:pct} neutralizzi il suo attacco e guadagni {assalto.accampamento.atk:signed} ATK, che resta per il '
              "resto dell'assalto. PARAMETRI COMPLETI — turno.demoni_difesa.random_min={turno.demoni_difesa.random_min}; "
              'turno.demoni_difesa.random_max={turno.demoni_difesa.random_max}.',
 'Cavaliere delle spine': 'Quando difendi hai il {turno.spine_difesa.proc:pct} di rimandare indietro parte del colpo. ASSALTO — HARD COUNTER dello Spuntone '
                          'malefico: se lo eviti, al {assalto.spuntone_schivato.proc:pct} guadagni {assalto.spuntone_schivato.atk:signed} ATK e '
                          '{assalto.spuntone_schivato.def:signed} DEF; se ti colpisce, al {assalto.spuntone_colpito.proc:pct} guadagni '
                          "{assalto.spuntone_colpito.def:signed} DEF. I bonus restano per il resto dell'assalto. PARAMETRI COMPLETI — "
                          'turno.spine_difesa.random_min={turno.spine_difesa.random_min}; turno.spine_difesa.random_max={turno.spine_difesa.random_max}.',
 'Mariachi': 'La musica può letteralmente rimetterti in piedi: quando difendi hai il {turno.resurrezione_difesa.proc:pct} di tornare con '
             '{turno.resurrezione_difesa.hp} HP e {turno.resurrezione_difesa.atk:signed} attacco. In assalto la resurrezione ha il '
             '{assalto.resurrezione.proc:pct}. PARAMETRI COMPLETI — turno.resurrezione_difesa.def={turno.resurrezione_difesa.def}; '
             'assalto.resurrezione.hp={assalto.resurrezione.hp}.',
 'Regina golgari': 'Hai il {turno.pietrifica.proc:pct} di pietrificare il nemico in sfida. ASSALTO — HARD COUNTER del Clone: quando lo incontri, al '
                   '{assalto.clone.proc:pct} lo pietrifichi e neutralizzi completamente il suo attacco. PARAMETRI COMPLETI — '
                   'turno.pietrifica.def_main={turno.pietrifica.def_main}; turno.pietrifica.atk_main={turno.pietrifica.atk_main}; '
                   'turno.pietrifica.agi_main={turno.pietrifica.agi_main}.',
 'Guerriero 3D': "In sfida il tuo stile altera anche l'atterraggio dei colpi. ASSALTO — HARD COUNTER del Sedimento del cucciolo: quando lo incontri, al "
                 '{assalto.cucciolo.proc:pct} neutralizzi completamente il suo attacco. PARAMETRI COMPLETI — '
                 'turno.atterraggio.mod_delta={turno.atterraggio.mod_delta}.',
 'Elfo silvano': 'La schivata diventa il tuo terreno di gioco: aumenti il bonus schivata di {turno.evasione.dogebonus}. In assalto hai il '
                 '{assalto.evasione.proc:pct} di dimezzare il bonus agilità della difesa nemica. PARAMETRI COMPLETI — '
                 'assalto.evasione.moltiplicatore_bonus_agi={assalto.evasione.moltiplicatore_bonus_agi}.',
 'Ombra silenziosa': 'In sfida puoi silenziare numerose abilità avversarie. ASSALTO — HARD COUNTER della Centrale di cura centralizzata: quando la incontri, '
                     'al {assalto.centrale.proc:pct} la silenzi prima del suo impulso e guadagni {assalto.centrale.atk:signed} ATK, che resta per il resto '
                     "dell'assalto. PARAMETRI COMPLETI — turno.silenzio_spumeggiante.proc={turno.silenzio_spumeggiante.proc}; "
                     'turno.silenzio_druido.proc={turno.silenzio_druido.proc}; turno.silenzio_crescita.proc={turno.silenzio_crescita.proc}; '
                     'turno.silenzio_fanghiglia.proc={turno.silenzio_fanghiglia.proc}; turno.silenzio_elsa.proc={turno.silenzio_elsa.proc}; '
                     'turno.silenzio_vincastro.proc={turno.silenzio_vincastro.proc}; turno.silenzio_corna.proc={turno.silenzio_corna.proc}; '
                     'turno.silenzio_ali.proc={turno.silenzio_ali.proc}; turno.silenzio_portatore.proc={turno.silenzio_portatore.proc}; '
                     'turno.silenzio_pazzoide.proc={turno.silenzio_pazzoide.proc}; turno.silenzio_sanguinolento.proc={turno.silenzio_sanguinolento.proc}; '
                     'turno.silenzio_adrenalina.proc={turno.silenzio_adrenalina.proc}; turno.silenzio_occulto.proc={turno.silenzio_occulto.proc}.',
 'Sopravvissuto': "Hai il {assalto.sopravvive.proc:pct} di resistere meglio durante l'assalto e, quando vinci, aumenti del "
                  '{ricompense.exp.bonus_probabilita_pct:pct} la possibilità di ottenere esperienza extra. PARAMETRI COMPLETI — '
                  'assalto.sopravvive.atk_divisore={assalto.sopravvive.atk_divisore}.',
 'Bug Abuser': 'Hai il {turno.bug.proc:pct} di rompere le regole e pescare un effetto da altri set: Golem, Druido, Tartaruga, Vigilante o Chip fuoco. Il Chip, '
               'per esempio, può aggiungere {turno.chip_fuoco.dps:signed} danni, mentre il Golem può darti {turno.golem_fuoco.agi:signed} agilità. PARAMETRI '
               'COMPLETI — turno.golem_fuoco.proc={turno.golem_fuoco.proc}; turno.golem_fuoco.dps_da_def_divisore={turno.golem_fuoco.dps_da_def_divisore}; '
               'turno.druido.proc={turno.druido.proc}; turno.druido.atk={turno.druido.atk}; turno.druido.def={turno.druido.def}; '
               'turno.druido.agi={turno.druido.agi}; turno.tartaruga.proc={turno.tartaruga.proc}; '
               'turno.tartaruga.riduzione_difesa={turno.tartaruga.riduzione_difesa}; turno.vigilante.proc={turno.vigilante.proc}; '
               'turno.chip_fuoco.proc={turno.chip_fuoco.proc}; assalto.target.proc={assalto.target.proc}; assalto.target.s1={assalto.target.s1}; '
               'assalto.target.s2={assalto.target.s2}; assalto.target.s3={assalto.target.s3}; assalto.target.s4={assalto.target.s4}; '
               'assalto.target.dps1={assalto.target.dps1}; assalto.target.dps2={assalto.target.dps2}; assalto.target.percento_hp={assalto.target.percento_hp}; '
               'assalto.target.dps4={assalto.target.dps4}; assalto.target.dps5={assalto.target.dps5}.',
 'Spacca Mostri': 'Più vita ha il nemico, più male gli fai: in sfida aggiungi al colpo un quarto dei suoi HP. ASSALTO — HARD COUNTER del Clone: se lo scegli '
                  'come bersaglio, al {assalto.clone.proc:pct} aggiungi {assalto.clone.dps:signed} DPS al colpo. PARAMETRI COMPLETI — '
                  'turno.mostro_enorme.hp_divisore={turno.mostro_enorme.hp_divisore}.',
 'Cultista pazzo': 'Ogni turno il veleno decide se amarti o odiarti: hai il {turno.veleno_folle.proc:pct} di guadagnare {turno.veleno_folle.bonus_dps:signed} '
                   "danni, altrimenti ne perdi {turno.veleno_folle.malus_dps}. In assalto l'ultimo colpo ha il {assalto.ultimo_colpo.proc:pct} di fare "
                   '{assalto.ultimo_colpo.danno} danni. PARAMETRI COMPLETI — assalto.ultimo_colpo.hp_min={assalto.ultimo_colpo.hp_min}.',
 'Thunderlord': "In assalto hai l'{assalto.tuono.proc:pct} di scatenare {assalto.tuono.colpi} fulmini da {assalto.tuono.danno} danni ciascuno sulla struttura "
                'nemica. PARAMETRI COMPLETI — assalto.tuono.hp_min={assalto.tuono.hp_min}.',
 'Cacciatore della feccia': 'Finché il nemico non ha fatto più di {turno.difesa_sotto_soglia.fatto_max} danni, difendi con '
                            '{turno.difesa_sotto_soglia.agi_difesa:signed} agilità e {turno.difesa_sotto_soglia.def_difesa:signed} difesa in più. In assalto '
                            'hai il {assalto.massa_nemici.proc:pct} di crescere con il numero dei nemici. PARAMETRI COMPLETI — '
                            'assalto.massa_nemici.atk_per_nemico={assalto.massa_nemici.atk_per_nemico}; '
                            'assalto.massa_nemici.def_per_nemico={assalto.massa_nemici.def_per_nemico}.',
 'Pescatore': 'Oltre a darti {bonus.atk:signed} attacco e {bonus.def:signed} difesa, migliora di {pesca.rarita.bonus_rarita:signed} la rarità della pesca. '
              'PARAMETRI COMPLETI — dungeon.armeria.compatibile={dungeon.armeria.compatibile}.',
 'Piccolo kraken': 'Il suo vero vantaggio sta negli approcci migliorati: non aggiunge altri effetti casuali durante la sfida. PARAMETRI COMPLETI — '
                   'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Inferno risvegliato': 'Il fuoco non fa preferenze: in sfida aumenta il tuo attacco di {turno.inferno.atk_main} e anche quello del nemico di '
                        '{turno.inferno.atk_target}. In assalto guadagni altri {assalto.inferno.atk_player:signed} punti attacco. PARAMETRI COMPLETI — '
                        'assalto.inferno.atk_bonus={assalto.inferno.atk_bonus}.',
 'Serial killer': 'Il tuo avversario inizia la sfida con solo il {generale.inizio.hp_target_percento:pct} dei suoi HP. ASSALTO — se il Bersaglio enorme riesce '
                  'a deviare il tuo assalto su di sé, guadagni {assalto.bersaglio_enorme.agi:signed} AGI per affrontarlo. PARAMETRI COMPLETI — '
                  'dungeon.contro_serial.danno={dungeon.contro_serial.danno}.',
 'Operatore di classe': 'Niente trucchi: il set ti dà direttamente {bonus.atk:signed} attacco e {bonus.def:signed} difesa. PARAMETRI COMPLETI — '
                        'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Combattente diretto': 'Poche parole, molti numeri: parti con {bonus.hp:signed} HP, {bonus.atk:signed} attacco, {bonus.def:signed} difesa e '
                        '{bonus.agi:signed} agilità. PARAMETRI COMPLETI — generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Paladino': 'Lo scudo ti segue ovunque: vale {boss.scudo.hp_scudo} HP contro i boss, {dungeon.scudo.hp_scudo} nei dungeon e {arena.scudo.hp_scudo} in arena. '
             'Finché regge, assorbe parte del colpo al posto tuo. PARAMETRI COMPLETI — turno.scudo.mod_bonus={turno.scudo.mod_bonus}.',
 'Cavaliere del passaggio': 'Sei fatto per tenere la posizione: il set ti dà {bonus.atk:signed} attacco e soprattutto {bonus.def:signed} difesa. PARAMETRI '
                            'COMPLETI — generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'MusicoSciamano': 'La tua musica spegne le abilità dei set: durante la sfida né tu né il tuo avversario potete attivare gli effetti del set. PARAMETRI '
                   'COMPLETI — turno.blocco_set.blocca_set_avversario={turno.blocco_set.blocca_set_avversario}.',
 'Taglialegna schivo': 'Taglia e sparisci: il set ti dà {bonus.def:signed} difesa e {bonus.agi:signed} agilità. PARAMETRI COMPLETI — '
                       'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Cultista oscuro': 'Nessun compromesso: il rituale ti concede direttamente {bonus.atk:signed} attacco. PARAMETRI COMPLETI — '
                    'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Dolce mietitore': "Sotto il mantello c'è molta più resistenza di quanto sembri: guadagni {bonus.def:signed} difesa. PARAMETRI COMPLETI — "
                    'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Pyromante': 'Tutto brucia meglio con più potere: il set ti dà direttamente {bonus.atk:signed} attacco. PARAMETRI COMPLETI — '
              'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Armaliere': 'Sai esattamente dove mettere il metallo: guadagni {bonus.atk:signed} attacco e {bonus.def:signed} difesa. PARAMETRI COMPLETI — '
              'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 "Controllore del'entrata": 'Nessuno passa senza essere visto: guadagni {bonus.hp:signed} HP e {bonus.agi:signed} agilità. PARAMETRI COMPLETI — '
                            'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 "Cavaliere d'argento": 'Se il tuo colpo esce troppo debole, recuperi fino a {turno.recupero_colpo.mod_bonus:signed} sul modificatore. In assalto, quando il '
                        'colpo va a segno, aggiungi danno diretto pari al maggiore tra {assalto.danno_fisso.danno_minimo} e un centesimo dei tuoi HP massimi. '
                        'PARAMETRI COMPLETI — turno.recupero_colpo.mod_massimo={turno.recupero_colpo.mod_massimo}; '
                        'assalto.danno_fisso.hp_massimi_divisore={assalto.danno_fisso.hp_massimi_divisore}.',
 'Selvaggio': 'Non hai bisogno di magie: il vantaggio del set arriva dagli approcci, che diventano molto più aggressivi. PARAMETRI COMPLETI — '
              'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Combattente della taverna': 'Birra, salsiccia e statistiche: guadagni {bonus.atk:signed} attacco e {bonus.def:signed} difesa. PARAMETRI COMPLETI — '
                              'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Medievalista': 'Armatura solida e passo leggero: guadagni {bonus.def:signed} difesa e {bonus.agi:signed} agilità. PARAMETRI COMPLETI — '
                 'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Macellaio': 'La tua stessa vita diventa armatura: in sfida aggiungi alla difesa un decimo dei tuoi HP; in assalto ne usi un ventesimo. PARAMETRI COMPLETI — '
              'turno.difesa_sangue.hp_divisore={turno.difesa_sangue.hp_divisore}; assalto.carne.hp_divisore={assalto.carne.hp_divisore}.',
 'Spaccatesta': 'Il nome dice già abbastanza: parti con {bonus.atk:signed} attacco e {bonus.def:signed} difesa. PARAMETRI COMPLETI — '
                'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Piarata': "Un po' di tutto, come un vero pirata: {bonus.atk:signed} attacco, {bonus.def:signed} difesa e {bonus.agi:signed} agilità. PARAMETRI COMPLETI — "
            'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Teppistello duro': 'Non sarà elegante, ma funziona: guadagni direttamente {bonus.def:signed} difesa. PARAMETRI COMPLETI — '
                     'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Apprendista delle paludi': 'La palude ti rende decisamente più difficile da buttare giù: guadagni {bonus.hp:signed} HP. PARAMETRI COMPLETI — '
                             'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Incubo dei cieli': "Scendi dall'alto già pronto a fare male: guadagni {bonus.atk:signed} attacco e {bonus.def:signed} difesa. PARAMETRI COMPLETI — "
                     'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Difensore del popolo': 'Se un compagno sta per cadere nel dungeon, puoi salvarlo lasciandolo ad almeno {dungeon.salvataggio_supporto.hp_salvato_min} HP e '
                         'recuperando per lui metà della vita disponibile. PARAMETRI COMPLETI — '
                         'dungeon.salvataggio_supporto.hp_supporto_fallback={dungeon.salvataggio_supporto.hp_supporto_fallback}; '
                         'dungeon.salvataggio_supporto.cura_divisore={dungeon.salvataggio_supporto.cura_divisore}; '
                         'dungeon.salvataggio_supporto.hp_supporto_consumato={dungeon.salvataggio_supporto.hp_supporto_consumato}.',
 'Re dei pirati': 'Durante gli assalti dei tuoi compagni puoi cannonare da fuori: il colpo fa almeno {assalto.supporto_ciurma.danno_min} danni e cresce con il '
                  'tuo attacco. PARAMETRI COMPLETI — assalto.supporto_ciurma.atk_divisore={assalto.supporto_ciurma.atk_divisore}.',
 'Dannato primordiale': 'Sfida/Assalto: converte il 100% della DEF posseduta in ATK e porta la DEF a 0. PARAMETRI COMPLETI — '
                        'sfida.conversione.proc={sfida.conversione.proc}; assalto.conversione.proc={assalto.conversione.proc}.',
 'Amletico': 'Bonus base: +50 HP. Sfida/Assalto: {sfida.sacrificio.proc:pct} per sacrificare il {sfida.sacrificio.percento_hp:pct} degli HP correnti e '
             "aggiungerlo all'ATK del colpo. PARAMETRI COMPLETI — assalto.sacrificio.proc={assalto.sacrificio.proc}; "
             'assalto.sacrificio.percento_hp={assalto.sacrificio.percento_hp}.',
 'Accumulatore di meraviglie': "Sfida: ogni turno {sfida.evocazione.proc:pct} di evocare un oggetto. Il valore dell'oggetto aumenta il danno del proprio colpo "
                               'o riduce quello nemico; gli oggetti di valore alto sono più rari. PARAMETRI COMPLETI — sfida.evocazione.oggetti.Un '
                               'vaso={sfida.evocazione.oggetti.Un vaso}; sfida.evocazione.oggetti.Un sasso di medie dimensioni={sfida.evocazione.oggetti.Un '
                               'sasso di medie dimensioni}; sfida.evocazione.oggetti.Un idropulitrice={sfida.evocazione.oggetti.Un idropulitrice}; '
                               'sfida.evocazione.oggetti.cento fiammiferi={sfida.evocazione.oggetti.cento fiammiferi}; sfida.evocazione.oggetti.una '
                               'mustang={sfida.evocazione.oggetti.una mustang}; sfida.evocazione.oggetti.Sei cammelli={sfida.evocazione.oggetti.Sei cammelli}; '
                               'sfida.evocazione.oggetti.LA LUNA={sfida.evocazione.oggetti.LA LUNA}.',
 'Anima della festa': 'Sfida: +1 seguace per turno e +{sfida.seguaci.percento_stat_per_seguace:pct} HP/ATK/DEF/AGI per ogni seguace. Assalto: il contributo '
                      'degli aiutanti recenti è moltiplicato per {assalto.last.moltiplicatore:x}. PARAMETRI COMPLETI — '
                      'sfida.seguaci.seguaci_per_turno={sfida.seguaci.seguaci_per_turno}.',
 'Zanno': 'Bonus base permanente del set: +300 ATK. PARAMETRI COMPLETI — generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Uditore del profondo': 'Sfida/Assalto: entrando esattamente a {sfida.richiamo.hp_trigger} HP infligge {sfida.richiamo.danno} danni al bersaglio. PARAMETRI '
                         'COMPLETI — assalto.richiamo.hp_trigger={assalto.richiamo.hp_trigger}; assalto.richiamo.danno={assalto.richiamo.danno}.',
 'Monarca della tempesta di fuoco': 'Sfida: possiede sempre Iridescente, Minimista, Primo impatto e Icore come incantamenti innati. Assalto: nessun effetto. '
                                    'PARAMETRI COMPLETI — sfida.incantamenti.nomi={sfida.incantamenti.nomi}.',
 'Evocatore delle maree': "Assalto: attiva sempre Onde dell'abisso; alla morte infligge a tutte le strutture il {assalto.tsunami.percento_atk:pct} del proprio "
                          'ATK. Sfida: nessun effetto. PARAMETRI COMPLETI — assalto.onda.incantesimo={assalto.onda.incantesimo}.',
 'Il comico': "COMBATTIMENTO (vale anche in dungeon e boss): all'inizio compare un sonoro CLAP! A ogni turno l'avversario ha il "
              '{combattimento.confusione.proc:pct} di provare a colpirsi da solo; se non schiva, subisce il proprio colpo. ASSALTO: compare CLAP!, senza altri '
              'effetti. PARAMETRI COMPLETI — assalto.clap.solo_testo={assalto.clap.solo_testo}.',
 'Survival medievale': 'Bonus base sempre attivo in qualunque modalità: {bonus.hp:signed} HP. PARAMETRI COMPLETI — '
                       'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Duellista vermico': 'COMBATTIMENTO e ASSALTO: il primo verme è garantito; poi hai il {combattimento.vermi.proc:pct} di mangiarne un altro, ripetendo finché '
                      'fallisci. Ogni verme dà {combattimento.vermi.atk:signed} ATK, {combattimento.vermi.def:signed} DEF e {combattimento.vermi.hp:signed} '
                      'HP. PARAMETRI COMPLETI — combattimento.vermi.primo_garantito={combattimento.vermi.primo_garantito}; '
                      'assalto.vermi.proc={assalto.vermi.proc}; assalto.vermi.primo_garantito={assalto.vermi.primo_garantito}; '
                      'assalto.vermi.atk={assalto.vermi.atk}; assalto.vermi.def={assalto.vermi.def}; assalto.vermi.hp={assalto.vermi.hp}.',
 'Duro a morire': 'Bonus base sempre attivo in qualunque modalità: {bonus.def:signed} DEF. PARAMETRI COMPLETI — '
                  'generale.set_base.solo_bonus_base={generale.set_base.solo_bonus_base}.',
 'Pazzo temporale': 'COMBATTIMENTO (vale anche in dungeon e boss): a inizio scontro compare Snap! e hai il {combattimento.seed.proc:pct} di fissare il seed a '
                    '{combattimento.seed.seed} per tutta la sequenza casuale dello scontro. ASSALTO: stessa logica con il {assalto.seed.proc:pct}. PARAMETRI '
                    'COMPLETI — assalto.seed.seed={assalto.seed.seed}.',
 'Big Game Hunter': "COMBATTIMENTO (vale anche in dungeon e boss): all'inizio dello scontro imposti la tua AGI uguale all'AGI corrente dell'avversario. "
                    'PARAMETRI COMPLETI — combattimento.copia_agilita.attivo={combattimento.copia_agilita.attivo}.',
 "Nucleo dell'uragano": "COMBATTIMENTO (anche dungeon/boss): ogni volta che un anello avversario procca, il vento infligge al proprietario dell'anello danni "
                        'puliti pari al {combattimento.proc_anello_avversario.percento_atk_proprio:pct} del tuo ATK. ASSALTO: non subisci danni dallo '
                        '{assalto.immunita.struttura}. PARAMETRI COMPLETI — assalto.immunita.messaggio={assalto.immunita.messaggio}.',
 'Tormento di fuoco': "COMBATTIMENTO (anche dungeon/boss): ogni volta che un anello avversario procca, il proprietario dell'anello subisce danni puliti pari "
                      'al {combattimento.proc_anello_avversario.percento_atk_avversario:pct} del proprio ATK. ASSALTO: non subisci danni dal '
                      '{assalto.immunita.struttura}. PARAMETRI COMPLETI — assalto.immunita.messaggio={assalto.immunita.messaggio}.',
 'Girarrosto': 'COMBATTIMENTO (anche dungeon/boss): la prima volta che scendi sotto il {combattimento.salvezza.hp_soglia_percento:pct} degli HP iniziali torni '
               'al {combattimento.salvezza.hp_ripristino_percento:pct}. ASSALTO: stessa salvezza, una volta per assalto. PARAMETRI COMPLETI — '
               'combattimento.salvezza.usi={combattimento.salvezza.usi}; assalto.salvezza.hp_soglia_percento={assalto.salvezza.hp_soglia_percento}; '
               'assalto.salvezza.hp_ripristino_percento={assalto.salvezza.hp_ripristino_percento}; assalto.salvezza.usi={assalto.salvezza.usi}.',
 "Rosso D'ossidina": 'COMBATTIMENTO (anche dungeon/boss): dopo ogni colpo riuscito riapplichi il tuo approccio e il log mostra in cosa stai diventando più '
                     'estremo. ASSALTO: non subisci danni dal {assalto.immunita.struttura}. PARAMETRI COMPLETI — '
                     'combattimento.riuso_approccio.attivo={combattimento.riuso_approccio.attivo}; assalto.immunita.messaggio={assalto.immunita.messaggio}.',
 'Oltraggioso': 'COMBATTIMENTO (anche dungeon/boss): finché partecipi allo scontro, ogni singola perdita di HP o Scudo di entrambi i combattenti è limitata a '
                'un massimo di {combattimento.cap_danno.massimo} danni. ASSALTO: non subisci danni dalla {assalto.immunita.struttura}. PARAMETRI COMPLETI — '
                'assalto.immunita.messaggio={assalto.immunita.messaggio}.',
 'Festante oscuro': "COMBATTIMENTO (anche dungeon/boss): i fantasmi assorbono al posto tuo ogni perdita di HP; all'inizio di ogni tuo turno subisci il "
                    '{combattimento.fantasmi.percento_ritorno:pct} del danno ancora accumulato nei fantasmi e quel valore viene rimosso dal loro accumulo. '
                    'ASSALTO: non subisci danni dal {assalto.immunita.struttura}. PARAMETRI COMPLETI — '
                    'assalto.immunita.messaggio={assalto.immunita.messaggio}.',
 'Legionaro di Evelin': 'COMBATTIMENTO (anche dungeon/boss): nei tuoi turni {combattimento.danno_turno.parita}, se il colpo non viene schivato e va a segno, '
                        "infliggi altri {combattimento.danno_turno.danno} danni puliti. ASSALTO: non subisci danni dall'{assalto.immunita.struttura}. "
                        'PARAMETRI COMPLETI — assalto.immunita.messaggio={assalto.immunita.messaggio}.',
 'Neo Genesi': 'COMBATTIMENTO (anche dungeon/boss): nei tuoi turni {combattimento.danno_turno.parita}, se il colpo non viene schivato e va a segno, infliggi '
               'altri {combattimento.danno_turno.danno} danni puliti. ASSALTO: non subisci danni dallo {assalto.immunita.struttura}. PARAMETRI COMPLETI — '
               'assalto.immunita.messaggio={assalto.immunita.messaggio}.',
 'Intermezzo': 'COMBATTIMENTO (anche dungeon/boss): ogni schivata concede una carica. Da {combattimento.cariche_schivata.soglia_1} cariche aggiungi '
               '{combattimento.cariche_schivata.bonus_1} danni; da {combattimento.cariche_schivata.soglia_2} aggiungi anche altri '
               '{combattimento.cariche_schivata.bonus_2}; da {combattimento.cariche_schivata.soglia_3} il danno risultante viene inoltre moltiplicato '
               '×{combattimento.cariche_schivata.moltiplicatore}. ASSALTO: non subisci danni dal {assalto.immunita.struttura}. PARAMETRI COMPLETI — '
               'assalto.immunita.messaggio={assalto.immunita.messaggio}.',
 'Obscurio': "COMBATTIMENTO (anche dungeon/boss): l'avversario non può aumentare i propri HP tramite cure finché è vivo; le resurrezioni da 0 HP o meno "
             'restano possibili. ASSALTO: non subisci danni dalla {assalto.immunita.struttura}. PARAMETRI COMPLETI — '
             'combattimento.anti_cura.attivo={combattimento.anti_cura.attivo}; assalto.immunita.messaggio={assalto.immunita.messaggio}.',
 'Primo al comando': 'COMBATTIMENTO (anche dungeon/boss): ogni proc di qualsiasi anello nello scontro ti cura di {combattimento.proc_anello.cura} HP. ASSALTO: '
                     'non subisci danni dal {assalto.immunita.struttura}. PARAMETRI COMPLETI — assalto.immunita.messaggio={assalto.immunita.messaggio}.',
 'Luce persa': 'COMBATTIMENTO (anche dungeon/boss): a inizio scontro calcoli AGI ×{combattimento.conversione.agi_mul}; il '
               '{combattimento.conversione.quota_atk:pct_mul} va in ATK e il {combattimento.conversione.quota_def:pct_mul} in DEF, poi AGI diventa 0. ASSALTO: '
               "stessa conversione prima dell'assalto. PARAMETRI COMPLETI — assalto.conversione.agi_mul={assalto.conversione.agi_mul}; "
               'assalto.conversione.quota_atk={assalto.conversione.quota_atk}; assalto.conversione.quota_def={assalto.conversione.quota_def}.'})
# --- COMPLETEZZA AUTOMATICA FRASI SET: FINE ---

# -*- coding: utf-8 -*-
"""Frasi tecniche custom dei set.

Ogni frase usa placeholder a percorso puntato che leggono i valori da
PROC_CLASSI oppure, con il prefisso ``bonus.``, dai bonus base del set.

Formati supportati dal renderer in nft.py:
- ``:pct`` percentuale già espressa 0..100;
- ``:x`` moltiplicatore;
- ``:signed`` numero con segno esplicito se positivo;
- ``:abs`` valore assoluto;
- ``:bool`` sì/no;
- ``:rid_pct`` riduzione percentuale derivata da un moltiplicatore.
"""

FRASI_SET_TECNICHE = {'Esperto di animali': 'Ogni evocazione ha il suo comportamento: Dragone delle stelle ha {turno.dragone_stelle.proc:pct} di portare il DPS a '
                       '{turno.dragone_stelle.dps_mul:x}; Fantasma del ritorno ha {turno.fantasma_ritorno.proc:pct} e lo porta a {turno.fantasma_ritorno.dps_mul:x}; '
                       'Ratto delle tombe finisce i bersagli a {turno.ratto_tombe.hp_target_max} HP o meno; Balena territoriale ha {turno.balena_territoriale.proc:pct} '
                       'e dà {turno.balena_territoriale.def:signed} DEF; Silvantropo ha {turno.silvantropo.proc:pct} e cura {turno.silvantropo.cura} HP; OrsoDruido ha '
                       '{turno.orsodruido.proc:pct} e restituisce tra {turno.orsodruido.random_min:x} e {turno.orsodruido.random_max:x} del danno.',
 'Pescatore': 'Il set dà {bonus.atk:signed} ATK e {bonus.def:signed} DEF; in pesca aumenta di {pesca.rarita.bonus_rarita:signed} il livello di rarità calcolato. '
              "Compatibilità con l'Armeria del dungeon: {dungeon.armeria.compatibile:bool}.",
 'Re del raaave': 'In assalto amplifica il meteo: Caldo infernale applica {assalto.meteo.caldo_infernale_agi:signed} AGI, Caldo torrido '
                  '{assalto.meteo.caldo_torrido_atk:signed} ATK e Arcobaleno {assalto.meteo.arcobaleno_atk:signed} ATK.',
 'Piccolo kraken': 'Non ha proc numerici aggiuntivi nel database: il profilo base è HP {bonus.hp:signed}, ATK {bonus.atk:signed}, DEF {bonus.def:signed}, AGI '
                   '{bonus.agi:signed}.',
 'Pescatore di balene': 'Parte con HP {bonus.hp:signed}, ATK {bonus.atk:signed} e DEF {bonus.def:signed}; in pesca aumenta di {pesca.rarita.bonus_rarita:signed} il '
                        'livello di rarità calcolato.',
 'Campione del sole': 'Carica il colpo nel tempo: sotto {turno.colpo_caricato.hp_trigger} HP usa una soglia minima di {turno.colpo_caricato.mol_min_hp}, altrimenti '
                      '{turno.colpo_caricato.mol_min_fallback}; il moltiplicatore di crescita è {turno.colpo_caricato.moltiplicatore:x} e il fallback ha '
                      '{turno.colpo_caricato.proc_fallback:pct}. In assalto il Fabbro proccha al {assalto.fabbro.proc:pct} per ATK {assalto.fabbro.atk:signed} e DEF '
                      '{assalto.fabbro.def:signed}.',
 'Cercatore di reliquie': 'Ogni turno ha {turno.reliquia.proc:pct} di trovare una reliquia: gli esiti sono separati dalle soglie {turno.reliquia.soglia1:pct}, '
                          '{turno.reliquia.soglia2:pct} e {turno.reliquia.soglia3:pct}, con possibili bonus AGI {turno.reliquia.agi:signed}, HP '
                          '{turno.reliquia.hp:signed}, DEF {turno.reliquia.def:signed} o ATK {turno.reliquia.atk:signed}. In assalto il Cannoncino ha '
                          '{assalto.cannoncino.proc:pct} per DEF {assalto.cannoncino.def:signed}.',
 'Regina golgari': 'Pietrifica al {turno.pietrifica.proc:pct}: modifica il bersaglio di DEF {turno.pietrifica.def_main:signed}, ATK {turno.pietrifica.atk_main:signed} e '
                   'AGI {turno.pietrifica.agi_main:signed}. In assalto ha {assalto.clone.proc:pct} di interagire col Clone.',
 'Manipolatore di morte': 'Al {turno.scheletri.proc:pct} richiama scheletri in base agli HP mancanti rispetto a {turno.scheletri.hp_riferimento}, uno ogni '
                          '{turno.scheletri.hp_per_scheletro} HP: ogni colpo usa un modificatore tra {turno.scheletri.mod_min:x} e {turno.scheletri.mod_max:x}, con '
                          'crescita danno {turno.scheletri.crescita_danno_scudo} sullo scudo e {turno.scheletri.crescita_danno_hp} sugli HP. In assalto la distrazione '
                          'ha {assalto.distrazione.proc:pct} e dà AGI {assalto.distrazione.agi:signed}.',
 'Inferno risvegliato': 'In sfida aumenta di {turno.inferno.atk_main:signed} ATK sia te sia il bersaglio ({turno.inferno.atk_target:signed}); in assalto aggiunge '
                        '{assalto.inferno.atk_bonus:signed} ATK alle difese e {assalto.inferno.atk_player:signed} ATK al giocatore.',
 'Fiamma pura': 'In sfida ha {turno.arena_brucia.proc:pct} di bruciare entrambi per {turno.arena_brucia.danno_main} e {turno.arena_brucia.danno_oppo} danni. In assalto, '
                'alla morte, ha {assalto.esplosione_morte.proc:pct} di infliggere {assalto.esplosione_morte.danno_struttura} danni a una struttura senza portarla sotto '
                '{assalto.esplosione_morte.hp_min_struttura} HP.',
 'Mago mentale': 'Showtime proccha al {turno.showtime.proc:pct}: genera da {turno.showtime.colpi_min} a {turno.showtime.colpi_max} colpi con modificatore tra '
                 '{turno.showtime.mod_min:x} e {turno.showtime.mod_max:x}; ogni sequenza può causare autodanno al {turno.showtime.autodanno_proc:pct} e la crescita '
                 'danno è {turno.showtime.crescita_danno}.',
 'Illusionista': 'In difesa crea copie al {turno.copie_difesa.proc:pct}; il bersaglio originale viene individuato al {turno.copie_difesa.proc_originale:pct}. In assalto '
                 'le copie procchano al {assalto.copie.proc:pct} e modificano AGI difensiva di {assalto.copie.agi_difesa:signed}.',
 'Assassino delle ombre': 'In assalto contro la Centrale proccha al {assalto.centrale.proc:pct}; dopo il primo passaggio usa un secondo controllo al '
                          '{assalto.centrale.proc_post:pct}. Il danno scala di {assalto.centrale.danno_per_livello} per livello e la struttura resta ad almeno '
                          '{assalto.centrale.hp_min} HP.',
 'Cercatore': 'In difesa ha {turno.demoni_difesa.proc:pct} di richiamare demoni con modificatore casuale tra {turno.demoni_difesa.random_min:x} e '
              '{turno.demoni_difesa.random_max:x}. In assalto contro l’Accampamento ha {assalto.accampamento.proc:pct} per ATK {assalto.accampamento.atk:signed}.',
 'Scudiero del boschetto': 'Finché il danno fatto non supera {turno.recupero.fatto_max}, ogni attivazione concede HP {turno.recupero.hp:signed}, ATK '
                           '{turno.recupero.atk:signed}, DEF {turno.recupero.def:signed} e AGI {turno.recupero.agi:signed}. In assalto contro lo Spaventapasseri '
                           'aggiunge ATK {assalto.spaventapasseri.atk:signed} e DEF {assalto.spaventapasseri.def:signed}.',
 'Contrabbandiere': 'Piazza una carica al {turno.piazza_carica.proc:pct} ({turno.piazza_carica.cariche:signed} carica). La detonazione ha {turno.detonazione.proc:pct}, '
                    'richiede almeno {turno.detonazione.cariche_trigger} cariche o la condizione HP {turno.detonazione.hp_trigger}, e infligge '
                    '{turno.detonazione.danno_per_carica} danni per carica. In assalto il Laser ha {assalto.laser.proc:pct}.',
 'Bug Abuser': 'Ogni bug pesca meccaniche diverse: bug generico {turno.bug.proc:pct}; Golem {turno.golem_fuoco.proc:pct} con AGI {turno.golem_fuoco.agi:signed} e DPS da '
               'DEF/{turno.golem_fuoco.dps_da_def_divisore}; Druido {turno.druido.proc:pct} con ATK {turno.druido.atk:signed}, DEF {turno.druido.def:signed}, AGI '
               '{turno.druido.agi:signed}; Tartaruga {turno.tartaruga.proc:pct} con DEF bersaglio {turno.tartaruga.riduzione_difesa:signed}; Vigilante '
               '{turno.vigilante.proc:pct}; Chip fuoco {turno.chip_fuoco.proc:pct} per DPS {turno.chip_fuoco.dps:signed}. In assalto il bug bersaglio parte al '
               '{assalto.target.proc:pct} e usa le soglie {assalto.target.s1:pct}/{assalto.target.s2:pct}/{assalto.target.s3:pct}/{assalto.target.s4:pct}.',
 'Serial killer': 'All’inizio porta gli HP del bersaglio al {generale.inizio.hp_target_percento:pct}. In assalto, se insiste sul Bersaglio enorme, ottiene AGI '
                  '{assalto.bersaglio_enorme.agi:signed}; nel particolare scontro dungeon contro un altro Serial killer il contraccolpo vale '
                  '{dungeon.contro_serial.danno} danni.',
 'Fire lord': 'Muori insetto proccha al {turno.muori_insetto.proc:pct} per {turno.muori_insetto.danno} danni; la smaterializzazione associata usa '
              '{turno.muori_insetto.smateriabile_proc:pct}. In assalto la catena tenta fino a {assalto.catena.tentativi} volte, con stop al '
              '{assalto.catena.stop_proc:pct}, {assalto.catena.danno} danni e HP struttura minimi {assalto.catena.hp_min}.',
 'Forma terra': 'Il Chip terra ha {turno.chip_difesa.proc:pct} di attivarsi in difesa e modifica il DPS di {turno.chip_difesa.dps:signed}.',
 'Forma fuoco': 'Il Chip fuoco ha {turno.chip.proc:pct} di attivarsi e aggiunge DPS {turno.chip.dps:signed}.',
 'Forma lunare': 'Il Chip lunare ha {turno.chip_difesa.proc:pct}: modifica la tua AGI di {turno.chip_difesa.agi_main:signed} e quella avversaria di '
                 '{turno.chip_difesa.agi_oppo:signed}.',
 'Forma elettro': 'Il Chip elettro ha {turno.chip.proc:pct}: porta il bonus AGI a {turno.chip.agi} e aggiunge DPS {turno.chip.dps:signed}.',
 'Operatore di classe': 'Nessun proc aggiuntivo: il set lavora sui bonus base, con ATK {bonus.atk:signed} e DEF {bonus.def:signed} (HP {bonus.hp:signed}, AGI '
                        '{bonus.agi:signed}).',
 'Shogun moderno': 'Doppio colpo proccha al {turno.doppio_colpo.proc:pct} e usa un moltiplicatore casuale tra {turno.doppio_colpo.moltiplicatore_min:x} e '
                   '{turno.doppio_colpo.moltiplicatore_max:x}. In assalto ha ancora {assalto.doppio_colpo.proc:pct}, denominatore {assalto.doppio_colpo.denominatore} e '
                   'random tra {assalto.doppio_colpo.random_min:x} e {assalto.doppio_colpo.random_max:x}.',
 'Vigilante': 'In attacco cambia proiettili al {turno.cambio_proiettili_attacco.proc:pct} e usa un bonus DEF di {turno.cambio_proiettili_attacco.bonus_difesa:signed}; '
              'in difesa il cambio proiettili ha {turno.cambio_proiettili_difesa.proc:pct}.',
 'Uomo di un tempo': 'Rigenera passivamente {turno.vitalita.hp} HP per turno in sfida e {assalto.vitalita.hp} HP durante l’assalto.',
 'Pazzoide glamour': 'La pazzia in sfida proccha al {turno.pazzia.proc:pct}; in assalto la cura del bersaglio ha {assalto.cura_target.proc:pct}.',
 'Combattente diretto': 'È un set puramente statistico: HP {bonus.hp:signed}, ATK {bonus.atk:signed}, DEF {bonus.def:signed} e AGI {bonus.agi:signed}, senza proc '
                        'aggiuntivi.',
 'Lupo di mare': 'Nei duelli modifica il furto di punti di {ricompense.duello.punti_malus:signed}; non ha altri proc numerici centralizzati.',
 'Cacciatore della feccia': 'In assalto la massa di nemici proccha al {assalto.massa_nemici.proc:pct} e vale ATK {assalto.massa_nemici.atk_per_nemico:signed} e DEF '
                            '{assalto.massa_nemici.def_per_nemico:signed} per nemico. In sfida, finché il nemico ha fatto al massimo '
                            '{turno.difesa_sotto_soglia.fatto_max} danni, aggiunge AGI difensiva {turno.difesa_sotto_soglia.agi_difesa:signed} e DEF '
                            '{turno.difesa_sotto_soglia.def_difesa:signed}.',
 'Sopravvissuto': 'In assalto Sopravvive ha {assalto.sopravvive.proc:pct} e scala con ATK/{assalto.sopravvive.atk_divisore}; inoltre aumenta di '
                  '{ricompense.exp.bonus_probabilita_pct:pct} la probabilità di ottenere EXP.',
 'Paladino': 'Lo scudo parte da {boss.scudo.hp_scudo} HP contro i boss, {dungeon.scudo.hp_scudo} nei dungeon e {arena.scudo.hp_scudo} in arena; quando assorbe un colpo '
             'usa un bonus al modificatore di {turno.scudo.mod_bonus:signed}.',
 'Accolito': 'Dopo almeno {turno.potere.danno_fatto_min} danni fatti attiva il Potere: ATK {turno.potere.atk:signed}, DEF {turno.potere.def:signed}, HP '
             '{turno.potere.hp:signed}, AGI {turno.potere.agi:signed}. In difesa ha {turno.difesa_cura.proc:pct} di curarsi usando divisore {turno.difesa_cura.divisore} '
             'più base {turno.difesa_cura.base}.',
 'Spacca Mostri': 'In sfida aggiunge al DPS un quarto degli HP del bersaglio tramite divisore {turno.mostro_enorme.hp_divisore}; in assalto il Clone proccha al '
                  '{assalto.clone.proc:pct} per {assalto.clone.dps} DPS.',
 'Cavaliere del passaggio': 'Difende il passaggio solo con statistiche certe: ATK {bonus.atk:signed} e DEF {bonus.def:signed}, senza proc numerici aggiuntivi.',
 'Primo alla bandiera': 'Quando viene colpito ha {turno.colpito.proc:pct}: divide il bonus per {turno.colpito.divisore_bonus} e cura in funzione del divisore '
                        '{turno.colpito.cura_divisore}. In assalto il Cannoncino ha {assalto.cannoncino.proc:pct} per {assalto.cannoncino.dps} DPS.',
 'Ice and fire': 'Calore ha {turno.calore.proc:pct} per ATK {turno.calore.atk:signed}; Gelo ha {turno.gelo.proc:pct} per DEF {turno.gelo.def:signed}. In assalto il '
                 'drago scaccia-drago ha {assalto.drago_scaccia_drago.proc:pct} e {assalto.drago_scaccia_drago.dps} DPS.',
 'MusicoSciamano': 'In sfida forza la meccanica specchio e usa il set dell’avversario: copia-set attiva = {turno.specchio.copia_set_avversario:bool}.',
 'Arciere di prima linea': 'Sfinimento proccha al {turno.sfinimento.proc:pct}: DEF bersaglio {turno.sfinimento.def_target:signed}, senza scendere sotto '
                           '{turno.sfinimento.def_min}. In assalto il Fabbro ha {assalto.fabbro.proc:pct} e aggiunge per livello ATK '
                           '{assalto.fabbro.atk_per_livello:signed}, DEF {assalto.fabbro.def_per_livello:signed}.',
 'Ghoul': 'Pressione proccha al {turno.pressione.proc:pct} e riduce ATK di {turno.pressione.atk_target:abs} e DEF di {turno.pressione.def_target:abs}. In assalto '
          'Terrore clone ha {assalto.terrore_clone.proc:pct}, con ATK clone {assalto.terrore_clone.atk_clone:signed} e DEF clone '
          '{assalto.terrore_clone.def_clone:signed}.',
 'Difensore delle mareggiate': 'Fauna proccha al {turno.fauna.proc:pct}: Sogliola sotto {turno.fauna.soglia_sogliola:pct} usa '
                               '{turno.fauna.sogliola_min:x}–{turno.fauna.sogliola_max:x}; Scorpione sotto {turno.fauna.soglia_scorpione:pct} usa '
                               '{turno.fauna.scorpione_min:x}–{turno.fauna.scorpione_max:x}; Pesce spada sotto {turno.fauna.soglia_spada:pct} usa '
                               '{turno.fauna.spada_min:x}–{turno.fauna.spada_max:x}; Balena usa {turno.fauna.balena_min:x}–{turno.fauna.balena_max:x}. In assalto ha '
                               '{assalto.fauna.proc:pct} per ATK {assalto.fauna.atk:signed}.',
 'Taglialegna schivo': 'La sua forza è tutta nel profilo base: DEF {bonus.def:signed} e AGI {bonus.agi:signed}; non ha proc numerici aggiuntivi.',
 'Cultista oscuro': 'Nessun proc: il culto converte tutto in pressione offensiva con ATK base {bonus.atk:signed}.',
 'Dolce mietitore': 'Nessun proc: il set investe tutto nella resistenza con DEF base {bonus.def:signed}.',
 'Sanguinolento': 'In difesa il sangue proccha al {turno.sangue_difesa.proc:pct} e scala con divisore {turno.sangue_difesa.divisore}. In assalto ha '
                  '{assalto.sangue.proc:pct} e usa divisore ATK {assalto.sangue.divisore_atk} e DEF {assalto.sangue.divisore_def}.',
 'Portatore di morte': 'Crescita ha {turno.crescita.proc:pct} e concede ATK {turno.crescita.atk:signed}, DEF {turno.crescita.def:signed}, AGI '
                       '{turno.crescita.agi:signed}; il debuff difensivo ha {turno.debuff_difesa.proc:pct} e applica ATK {turno.debuff_difesa.atk:signed}, DEF '
                       '{turno.debuff_difesa.def:signed}, AGI {turno.debuff_difesa.agi:signed}. In assalto il gadget usa moltiplicatore '
                       '{assalto.bonus_gadget.moltiplicatore:x}.',
 'Orrido': 'Sghignolo in sfida ha {turno.sgignolo.proc:pct}, denominatore {turno.sgignolo.denominatore} e moltiplicatore {turno.sgignolo.moltiplicatore:x}. In assalto '
           'proccha al {assalto.sgignolo.proc:pct} e infligge {assalto.sgignolo.danno} danni; il danno target configurato è {assalto.danno_target}.',
 'Guardiano del passaggio': 'In sfida la resurrezione ha {turno.resurrezione.proc:pct} e riporta a {turno.resurrezione.hp_base} HP; in assalto ha '
                            '{assalto.resurrezione.proc:pct} e riporta a {assalto.resurrezione.hp} HP.',
 'Pyromante': 'Nessun proc aggiuntivo: il fuoco è già nel bonus base, con ATK {bonus.atk:signed}.',
 'Uomo di classe': 'Spumeggiante in attacco ha {turno.spumeggiante_attacco.proc:pct}; in difesa {turno.spumeggiante_difesa.proc:pct}. In assalto proccha al '
                   '{assalto.spumeggiante.proc:pct} e modifica AGI difensiva di {assalto.spumeggiante.agi_difesa:signed}.',
 'Incantatore di controparte': 'Potere cosmico ha {turno.potere_cosmico.proc:pct} di attivarsi durante il turno.',
 'Proiettile': 'Quando è il difensore riduce il modificatore del colpo di {turno.difesa.mod_delta:abs}; in assalto aggiunge DEF {assalto.difesa.def:signed}.',
 'Cacciatore': 'Junior proccha al {turno.junior.proc:pct}, usa denominatore {turno.junior.denominatore} e moltiplicatore {turno.junior.moltiplicatore:x}. In assalto il '
               'Draghetto ha {assalto.draghetto.proc:pct} per {assalto.draghetto.dps} DPS.',
 'Pilota': 'Aumenta di {ricompense.exp.bonus_probabilita_pct:pct} la probabilità EXP e aggiunge {ricompense.duello.punti_bonus:signed} punti nel calcolo del duello.',
 'Marines': 'L’armatura proccha al {turno.armatura.proc:pct}, riduce il danno del {turno.armatura.riduzione_danno_percento:pct} e garantisce almeno '
            '{turno.armatura.danno_min} danno residuo.',
 'Armaliere': 'È un set senza proc: ATK {bonus.atk:signed} e DEF {bonus.def:signed} sono applicati direttamente come bonus base.',
 "Controllore del'entrata": 'Nessun proc: il set punta su HP {bonus.hp:signed} e AGI {bonus.agi:signed}, con ATK {bonus.atk:signed} e DEF {bonus.def:signed}.',
 'Mariachi': 'In difesa la resurrezione ha {turno.resurrezione_difesa.proc:pct}: HP {turno.resurrezione_difesa.hp}, ATK {turno.resurrezione_difesa.atk:signed}, DEF '
             '{turno.resurrezione_difesa.def:signed}. In assalto la resurrezione ha {assalto.resurrezione.proc:pct} e riporta a {assalto.resurrezione.hp} HP.',
 'Abitante': 'Radice proccha al {turno.radice.proc:pct} e moltiplica la DEF per {turno.radice.moltiplicatore_def:x}. In assalto gli alberelli hanno '
             '{assalto.alberelli.proc:pct} e modificano l’ATK nemico di {assalto.alberelli.bonus_atk_nemici:signed}.',
 "Cavaliere d'argento": 'Se il modificatore del colpo è al massimo {turno.recupero_colpo.mod_massimo:x}, aggiunge {turno.recupero_colpo.mod_bonus:signed}; in assalto '
                        'aggiunge {assalto.danno_fisso.danno:signed} danni fissi.',
 'Medico improvvisato': 'Dopo una schivata ha {turno.cura_schivata.proc:pct} di curarsi: usa DPS/{turno.cura_schivata.divisore_dps} con random tra '
                        '{turno.cura_schivata.random_min:x} e {turno.cura_schivata.random_max:x}. In assalto ha {assalto.cura.proc:pct} di curare {assalto.cura.cura} '
                        'HP.',
 'Cavaliere delle spine': 'In difesa le spine hanno {turno.spine_difesa.proc:pct} e riflettono con random '
                          '{turno.spine_difesa.random_min:x}–{turno.spine_difesa.random_max:x}. In assalto, se lo spuntone viene schivato, ha '
                          '{assalto.spuntone_schivato.proc:pct} per DEF {assalto.spuntone_schivato.def:signed} e ATK {assalto.spuntone_schivato.atk:signed}; se viene '
                          'colpito ha {assalto.spuntone_colpito.proc:pct} per DEF {assalto.spuntone_colpito.def:signed}.',
 'Selvaggio': 'Il database non registra proc numerici extra: bonus base HP {bonus.hp:signed}, ATK {bonus.atk:signed}, DEF {bonus.def:signed}, AGI {bonus.agi:signed}; le '
              'interazioni con gli approcci restano nel comportamento base.',
 'Maestro delle tartarughe': 'Insegnamenti proccha al {turno.insegnamenti.proc:pct} e riduce la DEF bersaglio di {turno.insegnamenti.riduzione_difesa_target}; in '
                             'assalto Carapace ha {assalto.carapace.proc:pct} e dà DEF {assalto.carapace.def:signed}.',
 'Combattente 2D': 'Evocazione proccha al {turno.evocazione.proc:pct}: Occhio sotto {turno.evocazione.soglia_occhio:pct}, Zombie sotto '
                   '{turno.evocazione.soglia_zombie:pct}, Raggio sotto {turno.evocazione.soglia_raggio:pct}; i bonus sono ATK {turno.evocazione.atk:signed}, DEF '
                   '{turno.evocazione.def:signed}, AGI {turno.evocazione.agi:signed}, Zombie {turno.evocazione.danno_zombie} danni e Raggio '
                   '{turno.evocazione.raggio_min:x}–{turno.evocazione.raggio_max:x}. In assalto Raggio lunare ha {assalto.raggio_lunare.proc:pct}, denominatore '
                   '{assalto.raggio_lunare.denominatore} e random {assalto.raggio_lunare.random_min:x}–{assalto.raggio_lunare.random_max:x}.',
 'Guerriero 3D': 'Quando difende da un atterraggio modifica il moltiplicatore di {turno.atterraggio.mod_delta:signed}; in assalto il Cucciolo ha '
                 '{assalto.cucciolo.proc:pct}.',
 'Guaritore da campo': 'Rinsana proccha al {turno.rinsana.proc:pct} e usa divisore {turno.rinsana.divisore}; in assalto la cura ha {assalto.cura.proc:pct} e vale '
                       '{assalto.cura.cura} HP.',
 'Combattente della taverna': 'Nessun proc: porta direttamente ATK {bonus.atk:signed} e DEF {bonus.def:signed} come bonus base.',
 'Ricercatore del pericolo': 'Dopo una schivata il contrattacco ha {turno.contrattacco_schivata.proc:pct} e aggiunge {turno.contrattacco_schivata.mod:signed} al '
                             'modificatore. In assalto Adrenalina ha {assalto.adrenalina.proc:pct} e dà ATK {assalto.adrenalina.atk:signed}.',
 'Ultima speranza': 'Parte con HP {bonus.hp:signed}, ATK {bonus.atk:signed}, DEF {bonus.def:signed}; in assalto Paura ha {assalto.paura.proc:pct} e modifica la DEF '
                    'nemica di {assalto.paura.bonus_def_nemico:signed}.',
 'Elfo silvano': 'In sfida aggiunge {turno.evasione.dogebonus:signed} al bonus schivata; in assalto Evasione ha {assalto.evasione.proc:pct} e moltiplica il bonus AGI '
                 'per {assalto.evasione.moltiplicatore_bonus_agi:x}.',
 'Juggernaut': 'In sfida porta l’AGI usata dalla difesa a {turno.peso.agi_difesa_mul:x}; in assalto l’interazione col Cane ha {assalto.cane.proc:pct}.',
 'Ombra silenziosa': 'Le chance di silenzio sono specifiche per effetto: Spumeggiante {turno.silenzio_spumeggiante.proc:pct}, Druido {turno.silenzio_druido.proc:pct}, '
                     'Crescita {turno.silenzio_crescita.proc:pct}, Fanghiglia {turno.silenzio_fanghiglia.proc:pct}, Elsa {turno.silenzio_elsa.proc:pct}, Vincastro '
                     '{turno.silenzio_vincastro.proc:pct}, Corna {turno.silenzio_corna.proc:pct}, Ali {turno.silenzio_ali.proc:pct}, Portatore '
                     '{turno.silenzio_portatore.proc:pct}, Pazzoide {turno.silenzio_pazzoide.proc:pct}, Sanguinolento {turno.silenzio_sanguinolento.proc:pct}, '
                     'Adrenalina {turno.silenzio_adrenalina.proc:pct}, Occulto {turno.silenzio_occulto.proc:pct}. In assalto la Centrale ha {assalto.centrale.proc:pct} '
                     'e concede ATK {assalto.centrale.atk:signed}.',
 'Crociato': 'Dopo una schivata Punizione ha {turno.punizione_schivata.proc:pct}: DPS/{turno.punizione_schivata.divisore_dps}, random '
             '{turno.punizione_schivata.random_min:x}–{turno.punizione_schivata.random_max:x}, minimo {turno.punizione_schivata.danno_min} danni. In assalto il '
             'Muraglione ha {assalto.muraglione.proc:pct} e usa moltiplicatore extra {assalto.muraglione.moltiplicatore_extra:x}.',
 'Drago': 'Scaglie proccha al {turno.scaglie.proc:pct} e riduce il modificatore a {turno.scaglie.riduzione_mod:x}; ha inoltre {turno.scaglie.proc_rottura_arma:pct} di '
          'rompere l’arma, applicando ATK bersaglio {turno.scaglie.atk_target:signed}. In assalto il Cucciolo ha {assalto.cucciolo.proc:pct} e dà ATK '
          '{assalto.cucciolo.atk:signed}.',
 'Maledetto': 'Maledizione in sfida ha {turno.maledizione.proc:pct}, usa come riferimento {turno.maledizione.hp_riferimento} HP e garantisce almeno '
              '{turno.maledizione.danno_min} danni. In assalto ha {assalto.maledizione.proc:pct} e colpisce per il {assalto.maledizione.percento_hp:pct} degli HP.',
 'Medievalista': 'Nessun proc: il set concede DEF {bonus.def:signed} e AGI {bonus.agi:signed} direttamente.',
 'Anima oscura': 'Parry proccha al {turno.parry.proc:pct} e moltiplica l’ATK per {turno.parry.moltiplicatore_atk:x}; in assalto il Fabbro ha {assalto.fabbro.proc:pct}.',
 'Macellaio': 'In sfida la difesa aggiuntiva usa HP/{turno.difesa_sangue.hp_divisore}; in assalto usa HP/{assalto.carne.hp_divisore}.',
 'Chierico': 'Cura automatica al {turno.cura.proc:pct} finché gli HP non superano {turno.cura.hp_max}: cura {turno.cura.cura_percento_hp:pct} degli HP più '
             '{turno.cura.cura_base}. In assalto ha {assalto.cura.proc:pct} di curare {assalto.cura.cura} HP.',
 'Betatester': 'La Spada beta proccha al {turno.spada_beta.proc:pct} per {turno.spada_beta.danno} danni in sfida; in assalto ha {assalto.spada_beta.proc:pct} per '
               '{assalto.spada_beta.dps} DPS.',
 'Cacciatore di bestie': 'Previsione in attacco ha {turno.previsione_attacco.proc:pct} e porta AGI a {turno.previsione_attacco.agi}; in difesa ha '
                         '{turno.previsione_difesa.proc:pct} e AGI {turno.previsione_difesa.agi}. In assalto Previsione ha {assalto.previsione.proc:pct} e AGI '
                         '{assalto.previsione.agi:signed}.',
 'Cacciatore di uomini': 'Trappola proccha al {turno.trappola.proc:pct} e modifica l’AGI bersaglio di {turno.trappola.agi_target:signed}.',
 'Cultista pazzo': 'Veleno folle proccha al {turno.veleno_folle.proc:pct}: può aggiungere DPS {turno.veleno_folle.bonus_dps:signed} oppure applicare il malus '
                   '{turno.veleno_folle.malus_dps}. In assalto Ultimo colpo ha {assalto.ultimo_colpo.proc:pct}, infligge {assalto.ultimo_colpo.danno} danni e lascia '
                   'almeno {assalto.ultimo_colpo.hp_min} HP.',
 'Druido della selva': 'Inselvatichisce proccha al {turno.inselvatichisce.proc:pct} e dà ATK {turno.inselvatichisce.atk:signed}, DEF {turno.inselvatichisce.def:signed}, '
                       'AGI {turno.inselvatichisce.agi:signed}. In assalto Natura ha {assalto.natura.proc:pct} e dà ATK {assalto.natura.atk:signed}, DEF '
                       '{assalto.natura.def:signed}, AGI {assalto.natura.agi:signed}.',
 'Spaccatesta': 'È un set di statistiche pure: ATK {bonus.atk:signed} e DEF {bonus.def:signed}, senza proc numerici aggiuntivi.',
 'Piarata': 'Nessun proc: il profilo base concede ATK {bonus.atk:signed}, DEF {bonus.def:signed} e AGI {bonus.agi:signed}.',
 'Vampiro': 'Morso proccha al {turno.morso.proc:pct}, usa divisore {turno.morso.divisore}, ha cap cura {turno.morso.cura_cap} quando supera il trigger '
            '{turno.morso.cap_trigger}. In assalto Pipistrello ha {assalto.pipistrello.proc:pct} e dà AGI {assalto.pipistrello.agi:signed}.',
 'Teppistello duro': 'Nessun proc: il set concentra tutto in DEF base {bonus.def:signed}.',
 'Segna ombre': 'Mimica difesa proccha al {turno.mimica_difesa.proc:pct}, obbligando il calcolo difensivo a usare la statistica copiata.',
 'PiroIncantatore': 'Golem di fuoco proccha al {turno.golem_fuoco.proc:pct}, dà AGI {turno.golem_fuoco.agi:signed} e calcola il DPS dalla '
                    'DEF/{turno.golem_fuoco.dps_da_def_divisore}. In assalto il Cucciolo di drago ha {assalto.cucciolo_drago.proc:pct} e dà ATK '
                    '{assalto.cucciolo_drago.atk:signed}.',
 'IppoFan': 'Copia attacco proccha al {turno.copia_attacco.proc:pct}; in assalto l’interazione col Cannoncino ha {assalto.cannoncino.proc:pct}.',
 'Corvo': 'Parte con AGI {bonus.agi:signed}; in sfida modifica il bonus schivata avversario di {turno.pressione_evasiva.dogebonus:signed}.',
 'Apprendista delle paludi': 'Nessun proc numerico: il set vive del suo grande bonus base, HP {bonus.hp:signed}.',
 'Eroe della rivolta': 'In assalto di gruppo moltiplica il contributo dei compagni per {assalto.supporto_clan.serv_mul:x}.',
 'Guardiano della bestie': 'Guadagna {turno.powe_per_turno} POWE per turno. Volpe: da {turno.volpe.powe_min} POWE, {turno.volpe.proc:pct}, DEF {turno.volpe.def:signed}; '
                           'Lupo: da {turno.lupo.powe_min}, {turno.lupo.proc:pct}, ATK {turno.lupo.atk:signed}; Ratti: da {turno.ratti.powe_min}, '
                           '{turno.ratti.proc:pct}, AGI {turno.ratti.agi:signed}; Orsi: da {turno.orsi.powe_min}, {turno.orsi.proc:pct}, ATK {turno.orsi.atk:signed}; '
                           'Serpenti: da {turno.serpenti.powe_min}, {turno.serpenti.proc:pct}, AGI bersaglio {turno.serpenti.agi_target:signed}; Presenza lunare: da '
                           '{turno.presenza_lunare.powe_min}, {turno.presenza_lunare.proc:pct}, DEF a {turno.presenza_lunare.def_mul:x}.',
 'Incubo dei cieli': 'Non ha proc numerici centralizzati: il profilo aggressivo dà ATK {bonus.atk:signed} e DEF {bonus.def:signed}.',
 'Cecchino modulare': 'Guadagna {turno.powa_per_turno} POWA per turno. A {turno.colpo_caricato.powa_min} POWA: Colpo caricato {turno.colpo_caricato.proc:pct}, DPS '
                      '{turno.colpo_caricato.dps:signed}; a {turno.colpo_preciso.powa_min}: Colpo preciso {turno.colpo_preciso.proc:pct}, AGI '
                      '{turno.colpo_preciso.agi:signed}; a {turno.colpo_possente.powa_min}: Colpo possente {turno.colpo_possente.proc:pct}, DPS '
                      '{turno.colpo_possente.dps:signed}; a {turno.cura_rapida.powa_min}: Cura rapida {turno.cura_rapida.proc:pct}, cura {turno.cura_rapida.cura}; a '
                      '{turno.colpo_perforante.powa_min}: Colpo perforante {turno.colpo_perforante.proc:pct}, DEF bersaglio impostata a '
                      '{turno.colpo_perforante.difesa_target}.',
 'Spadaccino Musashi': 'In sfida porta il danno subito a {turno.riduzione_danno.danno_mul:x}, cioè una riduzione del {turno.riduzione_danno.danno_mul:rid_pct}; in '
                       'assalto moltiplica la difesa per {assalto.difesa.def_mul:x}.',
 'Eroe caduto': 'Quando assalti con meno di {assalto.supporto_clan.compagni_soglia} compagni, il set aumenta il contributo virtuale: '
                '{assalto.supporto_clan.serv_bonus_nft:signed} nel percorso assalto di nft.py e {assalto.supporto_clan.serv_bonus_bot:signed} nel percorso gestito dal '
                'bot.',
 'Lanciatore olimpico': 'In assalto il Tridente proccha al {assalto.tridente.proc:pct}, infligge {assalto.tridente.danno} danni e non porta la struttura sotto '
                        '{assalto.tridente.hp_min} HP.',
 'Gangster': 'Lega proccha al {turno.lega.proc:pct}, bloccando la normale sequenza del bersaglio secondo la logica del set.',
 'Avventuriero delle praterie': 'Respira proccha al {turno.respira.proc:pct}: invece del normale attacco concede ATK {turno.respira.atk:signed}, DEF '
                                '{turno.respira.def:signed}, AGI {turno.respira.agi:signed} e azzera il colpo di quel turno.',
 'Difensore del popolo': 'Nel supporto dungeon, quando sacrifica il proprio intervento, se è già sotto zero viene riportato a '
                         '{dungeon.salvataggio_supporto.hp_supporto_fallback} HP; cura l’alleato di HP supporto/{dungeon.salvataggio_supporto.cura_divisore}, garantisce '
                         'almeno {dungeon.salvataggio_supporto.hp_salvato_min} HP e poi porta il supporto a {dungeon.salvataggio_supporto.hp_supporto_consumato} HP.',
 'Terrore delle ombre': 'Il database prevede {turno.marchio.proc_aggiungi:pct} per aggiungere un marchio e {turno.marchio.proc_effetto:pct} per convertirli in ATK '
                        '{turno.marchio.atk_per_marchio:signed}, DEF {turno.marchio.def_per_marchio:signed} e AGI {turno.marchio.agi_per_marchio:signed} per marchio. '
                        'Nota tecnica: nel flusso attuale i due rami condividono lo stesso roll e il {turno.marchio.proc_aggiungi:pct} viene valutato prima, quindi il '
                        'ramo effetto più basso non è raggiungibile.',
 'Oracolo del buio': 'Il database prevede {turno.marchio.proc_aggiungi:pct} per aggiungere un marchio e {turno.marchio.proc_effetto:pct} per applicare per marchio ATK '
                     '{turno.marchio.atk_per_marchio:signed}, DEF {turno.marchio.def_per_marchio:signed}, AGI {turno.marchio.agi_per_marchio:signed}. Nota tecnica: con '
                     'lo stesso roll il ramo al {turno.marchio.proc_aggiungi:pct} viene valutato prima, quindi il ramo effetto non è raggiungibile nell’ordine attuale.',
 "Ufficiale dell'oltretomba": 'Aggiunge marchi al {turno.marchio.proc_aggiungi:pct}; in difesa i demoni hanno {turno.demoni_difesa.proc:pct} e usano un modificatore '
                              'casuale tra {turno.demoni_difesa.random_min:x} e {turno.demoni_difesa.random_max:x}.',
 'Sciamano della verità': 'Il database prevede {turno.marchio.proc_aggiungi:pct} per aggiungere marchi e {turno.marchio.proc_effetto:pct} per curare '
                          '{turno.marchio.cura_per_marchio} HP per marchio. Nota tecnica: il ramo al {turno.marchio.proc_aggiungi:pct} usa lo stesso roll ed è valutato '
                          'prima, quindi il ramo cura non è raggiungibile nell’ordine attuale.',
 'Dannato': 'Il database prevede {turno.marchio.proc_aggiungi:pct} per aggiungere marchi e {turno.marchio.proc_effetto:pct} per infliggere '
            '{turno.marchio.danno_per_marchio} danni per marchio. Nota tecnica: con lo stesso roll il ramo al {turno.marchio.proc_aggiungi:pct} viene prima, quindi il '
            'ramo danno non è raggiungibile nell’ordine attuale.',
 'Dipper': "Il database prevede {turno.marchio.proc_aggiungi:pct} per aggiungere marchi e {turno.marchio.proc_effetto:pct} per l'effetto finale da almeno "
           '{turno.marchio.marchi_min} marchi, che usa divisore HP {turno.marchio.divisore_hp}. Nota tecnica: con lo stesso roll il ramo al '
           "{turno.marchio.proc_aggiungi:pct} viene prima, quindi il ramo effetto non è raggiungibile nell'ordine attuale.",
 'Re dei pirati': "Parte con ATK {bonus.atk:signed} e DEF {bonus.def:signed}; durante l'assalto dei compagni il colpo di supporto vale almeno "
                  '{assalto.supporto_ciurma.danno_min} danni oppure ATK alleato/{assalto.supporto_ciurma.atk_divisore}, scegliendo il valore maggiore.',
 'Thunderlord': 'In assalto Tuono proccha al {assalto.tuono.proc:pct}: esegue {assalto.tuono.colpi} colpi da {assalto.tuono.danno} danni e lascia ogni struttura ad '
                'almeno {assalto.tuono.hp_min} HP.'}

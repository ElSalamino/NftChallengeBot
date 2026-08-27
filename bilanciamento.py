# -*- coding: utf-8 -*-
"""
Configurazione centralizzata del bilanciamento di NftChallengeBot.

Contiene esclusivamente dati di tuning per classi, anelli e dungeon.
La logica applicativa resta in nft.py.
"""

# ============================================================
# DATABASE HARDCODATO PROC CLASSI
# Tutto il tuning delle classi deve stare qui: probabilita' in %,
# soglie e valori numerici. Le funzioni di combattimento leggono
# questo dizionario invece di contenere magic number sparsi.
# ============================================================
PROC_CLASSI = {'Cecchino modulare': {'turno': {'powa_per_turno': 1,
                                 'colpo_caricato': {'proc': 50, 'powa_min': 3, 'dps': 50},
                                 'colpo_preciso': {'proc': 50, 'powa_min': 8, 'agi': 50},
                                 'colpo_possente': {'proc': 50, 'powa_min': 16, 'dps': 150},
                                 'cura_rapida': {'proc': 50, 'powa_min': 24, 'cura': 60},
                                 'colpo_perforante': {'proc': 50, 'powa_min': 32, 'difesa_target': 5}}},
 'Uomo di classe': {'turno': {'spumeggiante_attacco': {'proc': 85}, 'spumeggiante_difesa': {'proc': 88}},
                    'assalto': {'spumeggiante': {'proc': 35, 'agi_difesa': -40}}},
 'Chierico': {'turno': {'cura': {'proc': 50, 'hp_max': 3000, 'cura_percento_hp': 1.5, 'cura_base': 2}},
              'assalto': {'cura': {'proc': 10, 'cura': 15}}},
 'Vigilante': {'turno': {'cambio_proiettili_attacco': {'proc': 40, 'bonus_difesa': 10}, 'cambio_proiettili_difesa': {'proc': 30}}},
 'Maestro delle tartarughe': {'turno': {'insegnamenti': {'proc': 20, 'riduzione_difesa_target': 100}},
                              'assalto': {'carapace': {'proc': 10, 'def': 35}}},
 'Druido della selva': {'turno': {'inselvatichisce': {'proc': 45, 'atk': 3, 'def': 4, 'agi': 2}},
                        'assalto': {'natura': {'proc': 30, 'atk': 15, 'def': 15, 'agi': 7}}},
 'Incantatore di controparte': {'turno': {'potere_cosmico': {'proc': 80}}},
 'PiroIncantatore': {'turno': {'golem_fuoco': {'proc': 30, 'agi': 200, 'dps_da_def_divisore': 5}},
                     'assalto': {'cucciolo_drago': {'proc': 12, 'atk': 33}}},
 'Arciere di prima linea': {'turno': {'sfinimento': {'proc': 25, 'def_target': -60, 'def_min': 1}},
                            'assalto': {'fabbro': {'proc': 30, 'atk_per_livello': 5, 'def_per_livello': 5}}},
 'Forma elettro': {'turno': {'chip': {'proc': 16, 'agi': 1000001, 'dps': 50}}},
 'Forma fuoco': {'turno': {'chip': {'proc': 16, 'dps': 350}}},
 'Forma terra': {'turno': {'chip_difesa': {'proc': 16, 'dps': -350}}},
 'Forma lunare': {'turno': {'chip_difesa': {'proc': 16, 'agi_main': -20, 'agi_oppo': 20}}},
 'Ghoul': {'turno': {'pressione': {'proc': 44, 'atk_target': -10, 'def_target': -10}},
           'assalto': {'terrore_clone': {'proc': 15, 'atk_clone': -30, 'def_clone': -50}}},
 'Portatore di morte': {'turno': {'crescita': {'proc': 45, 'atk': 2, 'def': 2, 'agi': 2},
                                  'debuff_difesa': {'proc': 40, 'atk': -2, 'def': -2, 'agi': -2}},
                        'assalto': {'bonus_gadget': {'moltiplicatore': 2}}},
 'Contrabbandiere': {'turno': {'detonazione': {'proc': 20, 'hp_trigger': 250, 'cariche_trigger': 10, 'danno_per_carica': 30},
                               'piazza_carica': {'proc': 50, 'cariche': 1}},
                     'assalto': {'laser': {'proc': 80}}},
 'Terrore delle ombre': {'turno': {'marchio': {'proc_aggiungi': 40,
                                               'proc_effetto': 20,
                                               'atk_per_marchio': 5,
                                               'def_per_marchio': 5,
                                               'agi_per_marchio': 1}}},
 'Oracolo del buio': {'turno': {'marchio': {'proc_aggiungi': 40,
                                            'proc_effetto': 20,
                                            'atk_per_marchio': -5,
                                            'def_per_marchio': -5,
                                            'agi_per_marchio': -1}}},
 'Sciamano della verità': {'turno': {'marchio': {'proc_aggiungi': 40, 'proc_effetto': 30, 'cura_per_marchio': 10}}},
 'Dannato': {'turno': {'marchio': {'proc_aggiungi': 40, 'proc_effetto': 20, 'danno_per_marchio': 5}}},
 'Dipper': {'turno': {'marchio': {'proc_aggiungi': 40, 'proc_effetto': 30, 'marchi_min': 10, 'divisore_hp': 2}}},
 'Cacciatore di bestie': {'turno': {'previsione_attacco': {'proc': 30, 'agi': 5600}, 'previsione_difesa': {'proc': 20, 'agi': 800}},
                          'assalto': {'previsione': {'proc': 30, 'agi': 60}}},
 'Ice and fire': {'turno': {'calore': {'proc': 20, 'atk': 30}, 'gelo': {'proc': 15, 'def': 30}},
                  'assalto': {'drago_scaccia_drago': {'proc': 50, 'dps': 700}}},
 'Cacciatore di uomini': {'turno': {'trappola': {'proc': 22, 'agi_target': -15}}},
 'Ricercatore del pericolo': {'turno': {'contrattacco_schivata': {'proc': 60, 'mod': 0.3}},
                              'assalto': {'adrenalina': {'proc': 30, 'atk': 20}}},
 'IppoFan': {'turno': {'copia_attacco': {'proc': 66}}, 'assalto': {'cannoncino': {'proc': 50}}},
 'Maledetto': {'turno': {'maledizione': {'proc': 15, 'hp_riferimento': 1000, 'danno_min': 10}},
               'assalto': {'maledizione': {'proc': 40, 'percento_hp': 8}}},
 'Campione del sole': {'turno': {'colpo_caricato': {'proc_fallback': 70,
                                                    'hp_trigger': 300,
                                                    'mol_min_hp': 4,
                                                    'mol_min_fallback': 5,
                                                    'moltiplicatore': 0.55}},
                       'assalto': {'fabbro': {'proc': 90, 'atk': 30, 'def': 20}}},
 'Segna ombre': {'turno': {'mimica_difesa': {'proc': 66}}},
 'Drago': {'turno': {'scaglie': {'proc': 33, 'riduzione_mod': 0.5, 'proc_rottura_arma': 50, 'atk_target': -22}},
           'assalto': {'cucciolo': {'proc': 10, 'atk': 50}}},
 'Anima oscura': {'turno': {'parry': {'proc': 12, 'moltiplicatore_atk': 1.1}}, 'assalto': {'fabbro': {'proc': 30}}},
 'Abitante': {'turno': {'radice': {'proc': 12, 'moltiplicatore_def': 1.1}},
              'assalto': {'alberelli': {'proc': 20, 'bonus_atk_nemici': -20}}},
 'Gangster': {'turno': {'lega': {'proc': 10}}},
 'Marines': {'turno': {'armatura': {'proc': 30, 'riduzione_danno_percento': 40, 'danno_min': 1}}},
 'Illusionista': {'turno': {'copie_difesa': {'proc': 50, 'proc_originale': 33}}, 'assalto': {'copie': {'proc': 15, 'agi_difesa': -30}}},
 'Betatester': {'turno': {'spada_beta': {'proc': 20, 'danno': 175}}, 'assalto': {'spada_beta': {'proc': 20, 'dps': 1033}}},
 'Avventuriero delle praterie': {'turno': {'respira': {'proc': 90, 'atk': 50, 'def': 30, 'agi': 4}}},
 'Shogun moderno': {'turno': {'doppio_colpo': {'proc': 20, 'moltiplicatore_min': 0.8, 'moltiplicatore_max': 1.2}},
                    'assalto': {'doppio_colpo': {'proc': 20, 'denominatore': 55, 'random_min': 0.7, 'random_max': 1.3}}},
 'Manipolatore di morte': {'turno': {'scheletri': {'proc': 20,
                                                   'hp_riferimento': 1200,
                                                   'hp_per_scheletro': 100,
                                                   'mod_min': 0.2,
                                                   'mod_max': 0.3,
                                                   'crescita_danno_scudo': 15,
                                                   'crescita_danno_hp': 5}},
                           'assalto': {'distrazione': {'proc': 10, 'agi': 10}}},
 'Mago mentale': {'turno': {'showtime': {'proc': 20,
                                         'colpi_min': 1,
                                         'colpi_max': 7,
                                         'mod_min': 0.1,
                                         'mod_max': 0.4,
                                         'autodanno_proc': 20,
                                         'crescita_danno': 25}}},
 'Guardiano della bestie': {'turno': {'powe_per_turno': 1,
                                      'volpe': {'proc': 30, 'powe_min': 3, 'def': 10},
                                      'lupo': {'proc': 30, 'powe_min': 9, 'atk': 10},
                                      'ratti': {'proc': 30, 'powe_min': 17, 'agi': 5},
                                      'orsi': {'proc': 30, 'powe_min': 25, 'atk': 50},
                                      'serpenti': {'proc': 30, 'powe_min': 33, 'agi_target': -10},
                                      'presenza_lunare': {'proc': 50, 'powe_min': 65, 'def_mul': 2}}},
 'Fiamma pura': {'turno': {'arena_brucia': {'proc': 65, 'danno_main': 100, 'danno_oppo': 100}},
                 'assalto': {'esplosione_morte': {'proc': 60, 'danno_struttura': 45, 'hp_min_struttura': 45}}},
 'Crociato': {'turno': {'punizione_schivata': {'proc': 50, 'divisore_dps': 3, 'random_min': 0.9, 'random_max': 1.4, 'danno_min': 30}},
              'assalto': {'muraglione': {'proc': 50, 'moltiplicatore_extra': 4}}},
 'Medico improvvisato': {'turno': {'cura_schivata': {'proc': 50, 'divisore_dps': 2.2, 'random_min': 0.7, 'random_max': 1.1}},
                         'assalto': {'cura': {'proc': 10, 'cura': 50}}},
 'Vampiro': {'turno': {'morso': {'proc': 20, 'divisore': 12, 'cura_cap': 142, 'cap_trigger': 150}},
             'assalto': {'pipistrello': {'proc': 20, 'agi': 30}}},
 'Guaritore da campo': {'turno': {'rinsana': {'proc': 75, 'divisore': 9}}, 'assalto': {'cura': {'proc': 20, 'cura': 7}}},
 'Cacciatore': {'turno': {'junior': {'proc': 20, 'denominatore': 70, 'moltiplicatore': 0.75}},
                'assalto': {'draghetto': {'proc': 50, 'dps': 1000}}},
 'Orrido': {'turno': {'sgignolo': {'proc': 70, 'denominatore': 140, 'moltiplicatore': 0.5}},
            'assalto': {'sgignolo': {'proc': 42, 'danno': 33}, 'danno_target': 33}},
 'Pazzoide glamour': {'turno': {'pazzia': {'proc': 90}}, 'assalto': {'cura_target': {'proc': 70}}},
 'Primo alla bandiera': {'turno': {'colpito': {'proc': 35, 'divisore_bonus': 2, 'cura_divisore': 12}},
                         'assalto': {'cannoncino': {'proc': 30, 'dps': 1400}}},
 'Difensore delle mareggiate': {'turno': {'fauna': {'proc': 24,
                                                    'soglia_sogliola': 10,
                                                    'sogliola_min': 0.1,
                                                    'sogliola_max': 0.4,
                                                    'soglia_scorpione': 50,
                                                    'scorpione_min': 0.3,
                                                    'scorpione_max': 0.5,
                                                    'soglia_spada': 80,
                                                    'spada_min': 0.6,
                                                    'spada_max': 0.8,
                                                    'balena_min': 0.8,
                                                    'balena_max': 1.2}},
                                'assalto': {'fauna': {'proc': 10, 'atk': 35}}},
 'Cercatore di reliquie': {'turno': {'reliquia': {'proc': 24,
                                                  'agi': 15,
                                                  'hp': 150,
                                                  'def': 60,
                                                  'atk': 250,
                                                  'soglia1': 10,
                                                  'soglia2': 50,
                                                  'soglia3': 80}},
                           'assalto': {'cannoncino': {'proc': 50, 'def': 70}}},
 'Fire lord': {'turno': {'muori_insetto': {'proc': 8, 'danno': 80, 'smateriabile_proc': 10}},
               'assalto': {'catena': {'tentativi': 20, 'stop_proc': 60, 'danno': 80, 'hp_min': 80}}},
 'Combattente 2D': {'turno': {'evocazione': {'proc': 33,
                                             'soglia_occhio': 30,
                                             'soglia_zombie': 50,
                                             'soglia_raggio': 92,
                                             'atk': 8,
                                             'def': 5,
                                             'agi': 8,
                                             'danno_zombie': 40,
                                             'raggio_min': 0.7,
                                             'raggio_max': 1.2}},
                    'assalto': {'raggio_lunare': {'proc': 20, 'denominatore': 75, 'random_min': 1, 'random_max': 1.7}}},
 'Accolito': {'turno': {'potere': {'danno_fatto_min': 1100, 'atk': 180, 'def': 180, 'hp': 10, 'agi': 15},
                        'difesa_cura': {'proc': 10, 'divisore': 1.8, 'base': 10}}},
 'Esperto di animali': {'turno': {'dragone_stelle': {'proc': 20, 'dps_mul': 1.5},
                                  'fantasma_ritorno': {'proc': 20, 'dps_mul': 0.5},
                                  'ratto_tombe': {'hp_target_max': 100},
                                  'balena_territoriale': {'proc': 20, 'def': 44},
                                  'silvantropo': {'proc': 20, 'cura': 120},
                                  'orsodruido': {'proc': 25, 'random_min': 0.3, 'random_max': 0.8}}},
 'Sanguinolento': {'turno': {'sangue_difesa': {'proc': 40, 'divisore': 3}},
                   'assalto': {'sangue': {'proc': 12, 'divisore_atk': 8, 'divisore_def': 8}}},
 "Ufficiale dell'oltretomba": {'turno': {'marchio': {'proc_aggiungi': 40},
                                         'demoni_difesa': {'proc': 25, 'random_min': 0.5, 'random_max': 1.0}}},
 'Cercatore': {'turno': {'demoni_difesa': {'proc': 40, 'random_min': 0.1, 'random_max': 1.5}},
               'assalto': {'accampamento': {'proc': 10, 'atk': 20}}},
 'Cavaliere delle spine': {'turno': {'spine_difesa': {'proc': 50, 'random_min': 0.6, 'random_max': 1.0}},
                           'assalto': {'spuntone_schivato': {'proc': 30, 'def': 22, 'atk': 22},
                                       'spuntone_colpito': {'proc': 30, 'def': 33}}},
 'Mariachi': {'turno': {'resurrezione_difesa': {'proc': 40, 'hp': 250, 'atk': 200, 'def': 200}},
              'assalto': {'resurrezione': {'proc': 12, 'hp': 1000}}},
 'Scudiero del boschetto': {'assalto': {'spaventapasseri': {'atk': 30, 'def': 20}},
                            'turno': {'recupero': {'fatto_max': 300, 'hp': 30, 'atk': 10, 'def': 10, 'agi': 3}}},
 'Regina golgari': {'turno': {'pietrifica': {'proc': 30, 'def_main': 35, 'atk_main': -35, 'agi_main': -5}},
                    'assalto': {'clone': {'proc': 20}}},
 'Juggernaut': {'assalto': {'cane': {'proc': 10}}, 'turno': {'peso': {'agi_difesa_mul': 0.3}}},
 'Guerriero 3D': {'assalto': {'cucciolo': {'proc': 15}}, 'turno': {'atterraggio': {'mod_delta': -0.55}}},
 'Elfo silvano': {'assalto': {'evasione': {'proc': 95, 'moltiplicatore_bonus_agi': 0.5}}, 'turno': {'evasione': {'dogebonus': 40}}},
 'Ombra silenziosa': {'turno': {'silenzio_spumeggiante': {'proc': 20},
                                'silenzio_druido': {'proc': 20},
                                'silenzio_crescita': {'proc': 20},
                                'silenzio_fanghiglia': {'proc': 10},
                                'silenzio_elsa': {'proc': 10},
                                'silenzio_vincastro': {'proc': 2},
                                'silenzio_corna': {'proc': 20},
                                'silenzio_ali': {'proc': 10},
                                'silenzio_portatore': {'proc': 20},
                                'silenzio_pazzoide': {'proc': 20},
                                'silenzio_sanguinolento': {'proc': 5},
                                'silenzio_adrenalina': {'proc': 90},
                                'silenzio_occulto': {'proc': 90}},
                      'assalto': {'centrale': {'proc': 90, 'atk': 150}}},
 'Assassino delle ombre': {'assalto': {'centrale': {'proc': 80, 'proc_post': 70, 'danno_per_livello': 3, 'hp_min': 50}}},
 'Sopravvissuto': {'assalto': {'sopravvive': {'proc': 82, 'atk_divisore': 20}}, 'ricompense': {'exp': {'bonus_probabilita_pct': 25}}},
 'Bug Abuser': {'turno': {'bug': {'proc': 30},
                          'golem_fuoco': {'proc': 30, 'agi': 200, 'dps_da_def_divisore': 5},
                          'druido': {'proc': 20, 'atk': 3, 'def': 4, 'agi': 2},
                          'tartaruga': {'proc': 20, 'riduzione_difesa': 100},
                          'vigilante': {'proc': 20},
                          'chip_fuoco': {'proc': 20, 'dps': 350}},
                'assalto': {'target': {'proc': 20,
                                       's1': 3,
                                       's2': 33,
                                       's3': 53,
                                       's4': 83,
                                       'dps1': 500,
                                       'dps2': 1400,
                                       'percento_hp': 8,
                                       'dps4': 1333,
                                       'dps5': 800}}},
 'Spacca Mostri': {'assalto': {'clone': {'proc': 50, 'dps': 1000}}, 'turno': {'mostro_enorme': {'hp_divisore': 4}}},
 'Cultista pazzo': {'turno': {'veleno_folle': {'proc': 50, 'bonus_dps': 250, 'malus_dps': 100}},
                    'assalto': {'ultimo_colpo': {'proc': 8, 'danno': 100, 'hp_min': 100}}},
 'Guardiano del passaggio': {'turno': {'resurrezione': {'proc': 30, 'hp_base': 500}},
                             'assalto': {'resurrezione': {'proc': 12, 'hp': 1000}}},
 'Thunderlord': {'assalto': {'tuono': {'proc': 80, 'colpi': 3, 'danno': 60, 'hp_min': 80}}},
 'Lanciatore olimpico': {'assalto': {'tridente': {'proc': 50, 'danno': 80, 'hp_min': 80}}},
 'Cacciatore della feccia': {'assalto': {'massa_nemici': {'proc': 30, 'atk_per_nemico': 5, 'def_per_nemico': 5}},
                             'turno': {'difesa_sotto_soglia': {'fatto_max': 300, 'agi_difesa': 45, 'def_difesa': 375}}},
 'Ultima speranza': {'assalto': {'paura': {'proc': 30, 'bonus_def_nemico': -10}}},
 'Pescatore': {'pesca': {'rarita': {'bonus_rarita': 1}}, 'dungeon': {'armeria': {'compatibile': False}}},
 'Re del raaave': {'assalto': {'meteo': {'caldo_infernale_agi': -30, 'caldo_torrido_atk': -100, 'arcobaleno_atk': 100}}},
 'Piccolo kraken': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Pescatore di balene': {'pesca': {'rarita': {'bonus_rarita': 2}}},
 'Inferno risvegliato': {'turno': {'inferno': {'atk_main': 200, 'atk_target': 200}},
                         'assalto': {'inferno': {'atk_bonus': 100, 'atk_player': 100}}},
 'Serial killer': {'generale': {'inizio': {'hp_target_percento': 75}},
                   'assalto': {'bersaglio_enorme': {'agi': 30}},
                   'dungeon': {'contro_serial': {'danno': 150}}},
 'Operatore di classe': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Uomo di un tempo': {'turno': {'vitalita': {'hp': 22}}, 'assalto': {'vitalita': {'hp': 5}}},
 'Combattente diretto': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Lupo di mare': {'ricompense': {'duello': {'punti_malus': -2}}},
 'Paladino': {'boss': {'scudo': {'hp_scudo': 1000}},
              'dungeon': {'scudo': {'hp_scudo': 200}},
              'arena': {'scudo': {'hp_scudo': 800}},
              'turno': {'scudo': {'mod_bonus': 0.5}}},
 'Cavaliere del passaggio': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'MusicoSciamano': {'turno': {'specchio': {'copia_set_avversario': True}}},
 'Taglialegna schivo': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Cultista oscuro': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Dolce mietitore': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Pyromante': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Proiettile': {'turno': {'difesa': {'mod_delta': -0.3}}, 'assalto': {'difesa': {'def': 40}}},
 'Pilota': {'ricompense': {'exp': {'bonus_probabilita_pct': 10}, 'duello': {'punti_bonus': 2}}},
 'Armaliere': {'generale': {'set_base': {'solo_bonus_base': True}}},
 "Controllore del'entrata": {'generale': {'set_base': {'solo_bonus_base': True}}},
 "Cavaliere d'argento": {'turno': {'recupero_colpo': {'mod_massimo': 0.8, 'mod_bonus': 0.2}}, 'assalto': {'danno_fisso': {'danno': 15}}},
 'Selvaggio': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Combattente della taverna': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Medievalista': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Macellaio': {'turno': {'difesa_sangue': {'hp_divisore': 10}}, 'assalto': {'carne': {'hp_divisore': 20}}},
 'Spaccatesta': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Piarata': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Teppistello duro': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Corvo': {'turno': {'pressione_evasiva': {'dogebonus': -10}}},
 'Apprendista delle paludi': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Eroe della rivolta': {'assalto': {'supporto_clan': {'serv_mul': 1.2}}},
 'Incubo dei cieli': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Spadaccino Musashi': {'turno': {'riduzione_danno': {'danno_mul': 0.7}}, 'assalto': {'difesa': {'def_mul': 1.2}}},
 'Eroe caduto': {'assalto': {'supporto_clan': {'compagni_soglia': 2, 'serv_bonus_nft': 1, 'serv_bonus_bot': 2}}},
 'Difensore del popolo': {'dungeon': {'salvataggio_supporto': {'hp_supporto_fallback': 100,
                                                               'cura_divisore': 2,
                                                               'hp_salvato_min': 1,
                                                               'hp_supporto_consumato': -1000}}},
 'Re dei pirati': {'assalto': {'supporto_ciurma': {'danno_min': 20, 'atk_divisore': 15}}}}


# ============================================================
# DATABASE HARDCODATO DEGLI ANELLI
# ============================================================
# Tutto il tuning degli anelli usato da turno()/assedio() vive qui:
# - proc: probabilita' percentuale (0..100)
# - soglie/requisiti: hp_min, hp_max, limiti_stat, ecc.
# - valori: danno, cura, modificatori, bonus/malus statistiche
#
# La logica delle funzioni applica gli effetti, ma non contiene piu'
# i numeri di bilanciamento degli anelli.
PROC_ANELLI = {
    "Anello perfezionista": {
        "generale": {"seed": "Anello perfezionista"},
    },
    "Un frammento del potere": {
        "turno": {
            "attacco": {"proc": 3, "trasforma_in": "Anello superfortissimo ma proprio rotto sgravatissimo"},
            "difesa": {"proc": 2, "trasforma_in": "Anello superfortissimo ma proprio rotto sgravatissimo"},
        },
    },
    "Aura pessima": {
        "turno": {"aura": {"moltiplicatore_difesa_target": 0.8}},
    },
    "Effige della tribe": {
        "turno": {
            "cura_spettrale": {
                "proc": 20,
                "hp_max": 3500,
                "cura_percento_hp": 10,
                "equivalenti": ["Anello superfortissimo ma proprio rotto sgravatissimo"],
                "speciali": {"Ipposciamano indemoniato": {"proc": 80, "hp_max": 5500}},
            },
        },
    },
    "Fanghiglia della palude": {
        "turno": {"fango": {"proc": 50, "hp_min": 450, "atk": 11, "def": 11, "hp": -25}},
    },
    "Elsa vitale": {
        "turno": {"crescita": {"proc": 60, "hp_divisore": 10, "agi_divisore": 2}},
    },
    "Veleno del folle": {
        "turno": {"veleno": {"proc": 50, "bonus_dps": 250, "malus_dps": 100}},
    },
    "Guanto del falco": {
        "turno": {"falcon_punch": {"proc": 20, "difesa_base": 100}},
    },
    "Campanellina concentrante": {
        "turno": {"concentrazione": {"proc": 30, "agi": 1000001, "nomi_equivalenti": ["Cerbero sdentato"]}},
    },
    "Roccia viva": {
        "turno": {"golem": {"proc": 20, "bonus_def": 5}},
    },
    "Vincastro": {
        "turno": {
            "attacco": {"proc": 7, "difesa_base": 45},
            "difesa": {"proc": 7, "dps": 35},
        },
    },
    "Proteina brullicanti": {
        "turno": {"massa": {"proc": 18, "moltiplicatore_extra_dps": 1.8}},
    },
    "Corna da toro": {
        "turno": {
            "terrore": {
                "proc": 50,
                "hp_divisore": 10,
                "agi_divisore": 3,
                "nomi_equivalenti": ["Cerbero sdentato"],
            },
        },
    },
    "Corteccia naturale": {
        "turno": {"crescita": {"proc": 45, "atk_base": 8, "def_base": 8, "agi": 3}},
    },
    "Muschio Selvaggio": {
        "turno": {
            "selvaggio": {
                "proc": 22,
                "limiti_stat": {"agi": 525, "hp": 2200, "def": 3500, "atk": 3500},
            },
        },
    },
    "Pozione di furia": {
        "turno": {"furia": {"proc": 25, "atk_base": 35}},
    },
    "Cinta del comandante": {
        "turno": {"comando": {"proc": 25, "atk_target_base": 35}},
    },
    "Fantasmino luminoso": {
        "turno": {
            "debuff": {
                "proc": 44,
                "agi": -4,
                "atk_base": -8,
                "def_base": -8,
                "nomi_equivalenti": ["Carl, il becchino"],
            },
        },
    },
    "Ali di luminite": {
        "turno": {"volo": {"proc": 35, "agi_difesa": 260}},
    },
    "Amuleto del protettore": {
        "turno": {"protezione": {"proc": 18, "moltiplicatore_bonus": 1}},
    },
    "Guanto titanico": {
        "turno": {"difesa": {"proc": 20, "dps_base": 100}},
    },
    "Stemma della rocca": {
        "turno": {"rocca": {"proc": 25, "def_base": 35}},
    },
    "Coda demoniaca": {
        "turno": {
            "schivata": {"lastD_reset": 0},
            "dolore": {"divisore_chance": 1000, "bonus_speciale": 0.2, "nome_speciale": "Demone spezza-ossa", "danno": 0, "mod": 0},
        },
    },
    "Testuggine del vecchio saggio": {
        "turno": {"atterraggio": {"moltiplicatore_mod": 0.7}},
    },
    "Fascette luminose": {
        "turno": {"atterraggio": {"proc": 60, "mod": 0.3}},
    },
    "Compasso": {
        "turno": {"bilanciamento": {"proc": 88, "mod": 1.2}},
    },
    "Bilanciere": {
        "turno": {"bilanciamento": {"proc": 88, "mod": 1.2}},
    },
    "Pegno di amicizia": {
        "turno": {"difesa": {"moltiplicatore_danno": 0.9, "sottrai_int": True}},
    },
    "Tasto B": {
        "turno": {"roll": {"proc": 15, "mod": 0}},
    },
    "Tasto X": {
        "turno": {"obliteratore": {"proc": 12, "divisore_mod": 5, "bonus_stat_base": 7}},
    },
    "Scudiero fidato": {
        "turno": {"blocco": {"proc": 25, "danno": 0}},
    },
    "Aureola": {
        "turno": {"salvezza": {"proc": 35, "moltiplicatore_danno": 0.45, "danno_min": 1}},
    },
    "Ricordo straziante": {
        "turno": {"intangibile": {"proc": 15, "danno": 0, "mod": 0, "nomi_equivalenti": ["Fantasma del rimorso"]}},
    },
    "Spuntoni": {
        "turno": {"danno_extra": {"proc": 55, "mod": 0.4}},
    },
    "Scarica di adrenalina": {
        "turno": {"adrenalina": {"proc": 40, "offset_danno": 2, "divisore": 2, "bonus_finale": 1}},
    },
    "Lapsus vitale": {
        "turno": {"cura_danno": {"proc": 40, "offset_danno": 2, "divisore": 2, "nomi_equivalenti": ["Ipposciamano indemoniato"]}},
    },
    "Vasetto all'orlo": {
        "turno": {"contrattacco": {"proc": 25, "random_min": 0.5, "random_max": 1}},
    },
    "Chiavi dell'aldilà": {
        "turno": {"resurrezione": {"proc": 30, "hp_base": 500}},
    },
    "Benedizione sanguinolenta": {
        "turno": {"cura_danno": {"proc": 22, "divisore": 2, "nomi_equivalenti": ["Ipposciamano indemoniato"]}},
    },
    "Anello dell'occulto": {
        "turno": {"trascinamento": {"proc": 20, "dps_divisore": 3, "random_min": 0.3, "random_max": 1.5}},
    },
    "Anello di totano": {
        "turno": {
            "cura": {
                "proc": 45,
                "cura_colpito": 15,
                "cura_schivato": 25,
                "random_min": 0.8,
                "random_max": 1.8,
                "moltiplicatore_mod_schivato": 1.3,
            },
        },
    },
    "Cuffia da boia": {
        "turno": {"esecuzione": {"hp_target_base": 100, "hp_finale": 0}},
    },
    "Cuore delle sabbie": {
        "turno": {"insabbiato": {"proc": 25, "lv": 2, "dur": 1, "lv_incremento": 1, "nomi_equivalenti": ["Leviatano delle sabbi"]}},
    },
    "Chiavi": {
        "turno": {"batmobile": {"proc": 33, "danno": 35}},
    },
    "Scudo levitante": {
        "assalto": {"aura": {"stat": "def", "valore": 20}},
    },
    "Stemma del leader": {
        "assalto": {"aura": {"stat": "atk", "valore": 20}},
    },
    "Occhio del falco": {
        "assalto": {"aura": {"stat": "agi", "valore": 5}},
    },
    "Carica mobile": {
        "assalto": {"esplosione": {"proc": 20, "danno_min": 20, "danno_max": 150}},
    },
}


# ============================================================
# DATABASE HARDCODATO DUNGEON
# ============================================================
# Tutto il tuning del dungeon vive qui, soprattutto quello delle stanze.
# Percentuali espresse 0..100.
#
# Convenzioni:
# - *_pct = probabilita' effettiva dell'evento.
# - *_soglia_pct = soglia cumulativa sullo stesso roll casuale (serve per
#   mantenere IDENTICO il comportamento delle vecchie catene if/elif).
# - difficolta = coefficiente delle prove STAT >= difficolta * roll.
# - danno positivo aumenta il danno accumulato; cura positiva lo riduce.
#
# Alcune vecchie catene hanno soglie sovrapposte/irraggiungibili: sono
# mantenute tali apposta durante questo refactor, per non cambiare balance.
DUNGEON_CONFIG = {
    "generale": {
        "cooldown_stanza": 35,
        "cooldown_scelta": 1.1,
        "mod_stop_dg": -5,
        "mod_piu_dg": 5,
        "mod_nop": -60,
        "cura_fine_scelta": 20,
        "grado_fine_scelta": 1,
    },
    "generazione": {
        "stanze_min": 2,
        "stanze_max": 8,
        "visibilita_min": 1,
        "visibilita_max": 9,
        "stanze_extra_per_piano": 1,
    },
    "boss": {
        "exp_pct": 80,
        "exp": 3,
        "grado": 2,
        "gloria": 20,
        "lv_divisore_piano": 2.6,
        "lv_max_normale": 4,
        "lv_alto_pct": 50,
        "lv_alto": "4",
        "lv_basso": "3",
    },
    "mostro": {
        "exp_pct": 50,
        "exp": 2,
        "grado": 2,
    },
    "stanze": {
        "Crepaccio": {
            "Tocchi la crepa": {"espansione_pct": 50},
        },
        "Stanza": {
            "Sali": {"click_inerte_pct": 10, "cura": 450, "piani": -1},
            "Scendi": {"click_inerte_pct": 10, "danno": 500, "piani": 1},
        },
        "Spada conficcata": {
            "Estrai la spada": {
                "giorni_validi": [17, 21],
                "stat_base": {"hp": 1000, "atk": 100, "def": 100, "agi": 20},
            },
        },
        "Distributore": {
            "Metti monetina": {
                "gloria_min": 2,
                "costo_gloria": 1,
                "fragola_soglia_pct": 20,
                "kiwi_soglia_pct": 30,
                "stanza_soglia_pct": 40,
                "nemico_soglia_pct": 50,
                "pesce_soglia_pct": 60,
                "latte_soglia_pct": 70,
                "gloria_soglia_pct": 80,
                "cura_fragola": 20,
                "cura_kiwi": 25,
                "cura_pesce": 5,
                "danno_latte": 35,
                "premio_gloria": 4,
            },
        },
        "Bisca": {
            "Scommetti": {"puntata": 150, "carta_min": 1, "carta_max": 15},
        },
        "Fabbro": {
            "Avvicinati": {
                "interazione_pct": 98,
                "base_gloria": 150,
                "quantita_grande": 5,
                "quantita_minima": 2,
            },
        },
        "Fattoria": {
            "Mungi le mucche": {"latte": 2},
        },
        "Stanza del sonno": {
            "Immergitici": {
                "perdi_oggetto_soglia_pct": 10,
                "danno_soglia_pct": 50,
                "cura_soglia_pct": 70,
                "duplica_soglia_pct": 90,
                "danno": 100,
                "cura": 200,
            },
        },
        "Chiesa": {
            "Prega": {
                "classi_gradite": [
                    "Crociato", "Chierico", "Forma terra", "Forma fuoco",
                    "Forma lunare", "Forma elettro", "Cultista oscuro",
                    "Dolce mietitore", "Medievalista", "Cultista pazzo", "IppoFan",
                ],
                "guardie_fermano_pct": 60,
                "danno_cacciata": 123,
            },
        },
        "Bar": {
            "Gira per la locanda": {
                "acqua_soglia_pct": 50,
                "latte_soglia_pct": 80,
                "loop_soglia_pct": 90,
                "boss_soglia_pct": 10,
                "acqua": 5,
                "latte": 2,
                "stanze_loop": 2,
                "nemici_crew": 3,
            },
            "Bevi": {
                "salta_stanza_soglia_pct": 40,
                "randomizza_danno_soglia_pct": 20,
                "danno_random_min": -501,
                "danno_random_max": 1500,
            },
        },
        "Piedistallo": {
            "Subito": {"successo_pct": 50, "quantita_premio": 2},
        },
        "Cucina": {
            "Ne prendo una": {"successo_pct": 70, "incapacita_pct": 10, "spezie": 1},
            "Ne prendo 5": {"successo_pct": 50, "incapacita_pct": 20, "spezie": 5},
            "Ne prendo 10": {"successo_pct": 20, "incapacita_pct": 30, "spezie": 10},
            "Prendo il tavolo intero": {"successo_pct": 5, "spezie": 15},
        },
        "Stagno": {
            "Peschiamo!": {"difficolta": 4000, "gloria_per_kg": 0.4, "morte_soglia_pct": 20},
        },
        "Locanda spettrale": {
            "Entraci": {
                "evento_negativo_pct": 50,
                "fantasmi_soglia_pct": 2,
                "moltiplicatore_danno_fantasmi": 2,
                "danno_caduta": 100,
                "cura_riposo": 300,
            },
            "Svegliati": {"scaglione_soglia_pct": 1, "conferma_soglia_pct": 1},
        },
        "Pilastri": {
            "Ti ci avvicini": {"fulmine_pct": 50, "danno_fulmine": 999, "danno_premio": -300},
        },
        "Parco": {
            "Fuggi": {
                "difficolta": 200,
                "lv1_soglia_pct": 20,
                "lv2_soglia_pct": 55,
                "incapacita_soglia_pct": 50,
            },
            "Fermali": {"difficolta": 1300, "lv1_soglia_pct": 20, "lv2_soglia_pct": 55},
            "Parlaci": {"incapacita_pct": 60, "scaglione_soglia_pct": 1},
        },
        "Arena": {
            "Disco ricurvo": {"difficolta": 4000},
            "Disco acuminato": {"difficolta": 4000},
            "Disco bilanciato": {"difficolta": 4000},
        },
        "Tempio azteco": {
            "Un mattone ancestrale": {"difficolta": 45},
            "Una piuma azteca": {"difficolta": 150},
            "Un cappello da esploratore": {"difficolta": 5000},
        },
        "Fonte magica": {
            "evento": {"cura_pct": 40, "cura": 200},
        },
        "Lupo solitario": {
            "evento": {
                "nessun_lupo_soglia_pct": 40,
                "attacco_lupo_soglia_pct": 40,
                "cura": 50,
                "danno": 70,
            },
        },
        "Segreta abbandonata": {
            "evento": {
                "loot_pct": 40,
                "loot": ["Un fune di fuga", "Uno stimpak", "Candela blu", "Ultimo barlore"],
            },
        },
        "Luci ed ombre": {
            "evento": {
                "punizione_pct": 80,
                "approcci_oscuri": ["Base", "Agile", "Spinto", "Statico", "Aggressivo", "Rabbioso", "Spavaldo", "Malevolo"],
            },
        },
        "Armeria": {"evento": {"nessun_evento_pct": 30}},
        "MetaMusicoteca": {"evento": {"crack_musica_pct": 1}},
        "Biblioteca": {"evento": {"vuota_pct": 70}},
        "Cunicolo": {
            "evento": {
                "scaglione_soglia_pct": 1,
                "conferma_scaglione_soglia_pct": 1,
                "crollo_pct": 2,
                "piani_crollo": -1,
            },
        },
        "Sabbie mobili": {
            "evento": {
                "caduta_pct": 80,
                "pat_min": 666,
                "salvataggio_pet_soglia_pct": 40,
                "scaglione_soglia_pct": 1,
            },
        },
    },
}

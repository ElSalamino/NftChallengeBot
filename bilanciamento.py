# -*- coding: utf-8 -*-
"""
Configurazione centralizzata del bilanciamento di NftChallengeBot.

Contiene esclusivamente dati di tuning per classi, anelli, dungeon, incantesimi ed effetti temporanei.
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
                    'assalto': {'spumeggiante': {'proc': 50, 'agi_difesa': -40}}},
 'Chierico': {'turno': {'cura': {'proc': 50, 'hp_max': 3000, 'cura_percento_hp': 1.5, 'cura_base': 2}},
              'assalto': {'cura': {'proc': 100, 'cura': 150}}},
 'Vigilante': {'turno': {'cambio_proiettili_attacco': {'proc': 40, 'bonus_difesa': 10}, 'cambio_proiettili_difesa': {'proc': 30}}},
 'Maestro delle tartarughe': {'turno': {'insegnamenti': {'proc': 20, 'riduzione_difesa_target': 100}},
                              'assalto': {'carapace': {'proc': 50, 'def': 35}}},
 'Druido della selva': {'turno': {'inselvatichisce': {'proc': 45, 'atk': 3, 'def': 4, 'agi': 2}},
                        'assalto': {'natura': {'proc': 80, 'atk': 15, 'def': 15, 'agi': 7}}},
 'Incantatore di controparte': {'turno': {'potere_cosmico': {'proc': 80}}},
 'PiroIncantatore': {'turno': {'golem_fuoco': {'proc': 30, 'agi': 200, 'dps_da_def_divisore': 5}},
                     'assalto': {'cucciolo_drago': {'proc': 100, 'atk': 3300}}},
 'Arciere di prima linea': {'turno': {'sfinimento': {'proc': 25, 'def_target': -60, 'def_min': 1}},
                            'assalto': {'fabbro': {'proc': 100, 'atk_per_livello': 5, 'def_per_livello': 5}}},
 'Forma elettro': {'turno': {'chip': {'proc': 16, 'agi': 1000001, 'dps': 50}}},
 'Forma fuoco': {'turno': {'chip': {'proc': 16, 'dps': 350}}},
 'Forma terra': {'turno': {'chip_difesa': {'proc': 16, 'dps': -350}}},
 'Forma lunare': {'turno': {'chip_difesa': {'proc': 16, 'agi_propria': 20, 'agi_nemico': -20}}},
 'Ghoul': {'turno': {'pressione': {'proc': 44, 'atk_target': -10, 'def_target': -10}},
           'assalto': {'terrore_clone': {'proc': 100, 'atk_clone': -3000, 'def_clone': -5000}}},
 'Portatore di morte': {'turno': {'crescita': {'proc': 45, 'atk': 2, 'def': 2, 'agi': 2},
                                  'debuff_difesa': {'proc': 40, 'atk': -2, 'def': -2, 'agi': -2}},
                        'assalto': {'bonus_gadget': {'moltiplicatore': 2}}},
 'Contrabbandiere': {'turno': {'detonazione': {'proc': 20, 'hp_trigger': 250, 'cariche_trigger': 10, 'danno_per_carica': 30},
                               'piazza_carica': {'proc': 50, 'cariche': 1}},
                     'assalto': {'laser': {'proc': 100}}},
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
                          'assalto': {'previsione': {'proc': 100, 'agi': 60}}},
 'Ice and fire': {'turno': {'calore': {'proc': 20, 'atk': 30}, 'gelo': {'proc': 15, 'def': 30}},
                  'assalto': {'drago_scaccia_drago': {'proc': 100, 'dps': 7000}}},
 'Cacciatore di uomini': {'turno': {'trappola': {'proc': 22, 'agi_target': -15}}},
 'Ricercatore del pericolo': {'turno': {'contrattacco_schivata': {'proc': 60, 'mod': 0.3}},
                              'assalto': {'adrenalina': {'proc': 100, 'atk': 20}}},
 'IppoFan': {'turno': {'copia_attacco': {'proc': 66}}, 'assalto': {'cannoncino': {'proc': 100}}},
 'Maledetto': {'turno': {'maledizione': {'proc': 15, 'hp_riferimento': 1000, 'danno_min': 10}},
               'assalto': {'maledizione': {'proc': 100, 'percento_hp': 8}}},
 'Campione del sole': {'turno': {'colpo_caricato': {'proc_fallback': 70,
                                                    'hp_trigger': 300,
                                                    'mol_min_hp': 4,
                                                    'mol_min_fallback': 5,
                                                    'moltiplicatore': 0.55}},
                       'assalto': {'fabbro': {'proc': 100, 'atk': 3000, 'def': 2000}}},
 'Segna ombre': {'turno': {'mimica_difesa': {'proc': 66}}},
 'Drago': {'turno': {'scaglie': {'proc': 33, 'riduzione_mod': 0.5, 'proc_rottura_arma': 50, 'atk_target': -22}},
           'assalto': {'cucciolo': {'proc': 100, 'atk': 5000}}},
 'Anima oscura': {'turno': {'parry': {'proc': 12, 'moltiplicatore_atk': 1.1}}, 'assalto': {'fabbro': {'proc': 100}}},
 'Abitante': {'turno': {'radice': {'proc': 12, 'moltiplicatore_def': 1.1}},
              'assalto': {'alberelli': {'proc': 100, 'bonus_atk_nemici': -20}}},
 'Gangster': {'turno': {'lega': {'proc': 10}}},
 'Marines': {'turno': {'armatura': {'proc': 30, 'riduzione_danno_percento': 40, 'danno_min': 1}}},
 'Illusionista': {'turno': {'copie_difesa': {'proc': 50, 'proc_originale': 33}}, 'assalto': {'copie': {'proc': 50, 'agi_difesa': -30}}},
 'Betatester': {'turno': {'spada_beta': {'proc': 20, 'danno': 175}}, 'assalto': {'spada_beta': {'proc': 20, 'dps': 1333}}},
 'Avventuriero delle praterie': {'turno': {'respira': {'proc': 90, 'atk': 50, 'def': 30, 'agi': 4}}},
 'Shogun moderno': {'turno': {'doppio_colpo': {'proc': 20, 'moltiplicatore_min': 0.8, 'moltiplicatore_max': 1.2}},
                    'assalto': {'doppio_colpo': {'proc': 100, 'denominatore': 55, 'random_min': 0.7, 'random_max': 1.3}}},
 'Manipolatore di morte': {'turno': {'scheletri': {'proc': 20,
                                                   'hp_riferimento': 1200,
                                                   'hp_per_scheletro': 100,
                                                   'mod_min': 0.2,
                                                   'mod_max': 0.3,
                                                   'crescita_danno_scudo': 15,
                                                   'crescita_danno_hp': 5}},
                           'assalto': {'distrazione': {'proc': 100, 'agi': 10}}},
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
                 'assalto': {'esplosione_morte': {'proc': 1000, 'hp_massimi_divisore': 100, 'danno_minimo': 45}}},
 'Crociato': {'turno': {'punizione_schivata': {'proc': 50, 'divisore_dps': 3, 'random_min': 0.9, 'random_max': 1.4, 'danno_min': 30}},
              'assalto': {'muraglione': {'proc': 100, 'moltiplicatore_extra': 9}}},
 'Medico improvvisato': {'turno': {'cura_schivata': {'proc': 50, 'divisore_dps': 2.2, 'random_min': 0.7, 'random_max': 1.1}},
                         'assalto': {'cura': {'proc': 100, 'cura': 500}}},
 'Vampiro': {'turno': {'morso': {'proc': 20, 'divisore': 12, 'cura_cap': 142, 'cap_trigger': 150}},
             'assalto': {'pipistrello': {'proc': 100, 'agi': 30}}},
 'Guaritore da campo': {'turno': {'rinsana': {'proc': 75, 'divisore': 9}}, 'assalto': {'cura': {'proc': 100, 'cura': 70}}},
 'Cacciatore': {'turno': {'junior': {'proc': 20, 'denominatore': 70, 'moltiplicatore': 0.75}},
                'assalto': {'draghetto': {'proc': 100, 'dps': 10000}}},
 'Orrido': {'turno': {'sgignolo': {'proc': 70, 'denominatore': 140, 'moltiplicatore': 0.5}},
            'assalto': {'sgignolo': {'proc': 42, 'danno': 33}, 'danno_target': 33}},
 'Pazzoide glamour': {'turno': {'pazzia': {'proc': 90}}, 'assalto': {'cura_target': {'proc': 80}}},
 'Primo alla bandiera': {'turno': {'colpito': {'proc': 35, 'divisore_bonus': 2, 'cura_divisore': 12}},
                         'assalto': {'cannoncino': {'proc': 100, 'dps': 14000}}},
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
                                'assalto': {'fauna': {'proc': 50, 'atk': 35}}},
 'Cercatore di reliquie': {'turno': {'reliquia': {'proc': 24,
                                                  'agi': 15,
                                                  'hp': 150,
                                                  'def': 60,
                                                  'atk': 250,
                                                  'soglia1': 10,
                                                  'soglia2': 50,
                                                  'soglia3': 80}},
                           'assalto': {'cannoncino': {'proc': 100, 'def': 7000}}},
 'Fire lord': {'turno': {'muori_insetto': {'proc': 8, 'danno': 80}},
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
                    'assalto': {'raggio_lunare': {'proc': 100, 'denominatore': 75, 'random_min': 1, 'random_max': 1.7}}},
 'Accolito': {'turno': {'potere': {'danno_fatto_min': 1100, 'atk': 180, 'def': 180, 'hp': 10, 'agi': 15},
                        'difesa_cura': {'proc': 10, 'divisore': 1.8, 'base': 10}}},
 'Esperto di animali': {'turno': {'dragone_stelle': {'proc': 20, 'dps_mul': 1.5},
                                  'fantasma_ritorno': {'proc': 20, 'dps_mul': 0.5},
                                  'ratto_tombe': {'hp_target_max': 100},
                                  'balena_territoriale': {'proc': 20, 'def': 44},
                                  'silvantropo': {'proc': 20, 'cura': 120},
                                  'orsodruido': {'proc': 25, 'random_min': 0.3, 'random_max': 0.8}}},
 'Sanguinolento': {'turno': {'sangue_difesa': {'proc': 40, 'divisore': 3}},
                   'assalto': {'sangue': {'proc': 80, 'divisore_atk': 8, 'divisore_def': 8}}},
 "Ufficiale dell'oltretomba": {'turno': {'marchio': {'proc_aggiungi': 40},
                                         'demoni_difesa': {'proc': 25, 'random_min': 0.5, 'random_max': 1.0}}},
 'Cercatore': {'turno': {'demoni_difesa': {'proc': 40, 'random_min': 0.1, 'random_max': 1.5}},
               'assalto': {'accampamento': {'proc': 100, 'atk': 2000}}},
 'Cavaliere delle spine': {'turno': {'spine_difesa': {'proc': 50, 'random_min': 0.6, 'random_max': 1.0}},
                           'assalto': {'spuntone_schivato': {'proc': 100, 'def': 2200, 'atk': 2200},
                                       'spuntone_colpito': {'proc': 100, 'def': 3300}}},
 'Mariachi': {'turno': {'resurrezione_difesa': {'proc': 40, 'hp': 250, 'atk': 200, 'def': 200}},
              'assalto': {'resurrezione': {'proc': 12, 'hp': 1000}}},
 'Scudiero del boschetto': {'assalto': {'spaventapasseri': {'atk': 3000, 'def': 2000}},
                            'turno': {'recupero': {'fatto_max': 300, 'hp': 30, 'atk': 10, 'def': 10, 'agi': 3}}},
 'Regina golgari': {'turno': {'pietrifica': {'proc': 30, 'def_main': 35, 'atk_main': -35, 'agi_main': -5}},
                    'assalto': {'clone': {'proc': 100}}},
 'Juggernaut': {'assalto': {'cane': {'proc': 100}}, 'turno': {'peso': {'agi_difesa_mul': 0.3}}},
 'Guerriero 3D': {'assalto': {'cucciolo': {'proc': 100}}, 'turno': {'atterraggio': {'mod_delta': -0.55}}},
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
                      'assalto': {'centrale': {'proc': 100, 'atk': 15000}}},
 'Assassino delle ombre': {'assalto': {'centrale': {'proc': 80, 'proc_post': 70, 'danno_per_livello': 3, 'hp_min': 50}}},
 'Sopravvissuto': {'assalto': {'sopravvive': {'proc': 82, 'atk_divisore': 20}}, 'ricompense': {'exp': {'bonus_probabilita_pct': 25}}},
 'Bug Abuser': {'turno': {'bug': {'proc': 30},
                          'golem_fuoco': {'proc': 30, 'agi': 200, 'dps_da_def_divisore': 5},
                          'druido': {'proc': 20, 'atk': 3, 'def': 4, 'agi': 2},
                          'tartaruga': {'proc': 20, 'riduzione_difesa': 100},
                          'vigilante': {'proc': 20},
                          'chip_fuoco': {'proc': 20, 'dps': 350}},
                'assalto': {'target': {'proc': 80,
                                       's1': 3,
                                       's2': 33,
                                       's3': 53,
                                       's4': 83,
                                       'dps1': 500,
                                       'dps2': 1400,
                                       'percento_hp': 8,
                                       'dps4': 1333,
                                       'dps5': 800}}},
 'Spacca Mostri': {'assalto': {'clone': {'proc': 100, 'dps': 10000}}, 'turno': {'mostro_enorme': {'hp_divisore': 4}}},
 'Cultista pazzo': {'turno': {'veleno_folle': {'proc': 50, 'bonus_dps': 250, 'malus_dps': 100}},
                    'assalto': {'ultimo_colpo': {'proc': 80, 'danno': 100, 'hp_min': 100}}},
 'Guardiano del passaggio': {'turno': {'resurrezione': {'proc': 30, 'hp_base': 500}},
                             'assalto': {'resurrezione': {'proc': 12, 'hp': 1000}}},
 'Thunderlord': {'assalto': {'tuono': {'proc': 80, 'colpi': 3, 'danno': 60, 'hp_min': 80}}},
 'Lanciatore olimpico': {'assalto': {'tridente': {'proc': 80, 'danno': 80, 'decremento': 10, 'hp_min': 80}}},
 'Cacciatore della feccia': {'assalto': {'massa_nemici': {'proc': 100, 'atk_per_nemico': 5, 'def_per_nemico': 5}},
                             'turno': {'difesa_sotto_soglia': {'fatto_max': 300, 'agi_difesa': 45, 'def_difesa': 375}}},
 'Ultima speranza': {'assalto': {'paura': {'proc': 50, 'bonus_def_nemico': -150}}},
 'Pescatore': {'pesca': {'rarita': {'bonus_rarita': 1}}, 'dungeon': {'armeria': {'compatibile': False}}},
 'Re del raaave': {'assalto': {'meteo': {'caldo_infernale_agi': -30, 'caldo_torrido_atk': -100, 'arcobaleno_atk': 100}}},
 'Piccolo kraken': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Pescatore di balene': {'pesca': {'rarita': {'bonus_rarita': 2}}},
 'Inferno risvegliato': {'turno': {'inferno': {'atk_main': 200, 'atk_target': 200}},
                         'assalto': {'inferno': {'atk_bonus': 100, 'atk_player': 100}}},
 'Serial killer': {'generale': {'inizio': {'hp_target_percento': 75}},
                   'assalto': {'bersaglio_enorme': {'agi': 130}},
                   'dungeon': {'contro_serial': {'danno': 150}}},
 'Operatore di classe': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Uomo di un tempo': {'turno': {'vitalita': {'hp': 22}}, 'assalto': {'vitalita': {'hp': 55}}},
 'Combattente diretto': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Lupo di mare': {'ricompense': {'duello': {'punti_malus': -2}}},
 'Paladino': {'boss': {'scudo': {'hp_scudo': 1000}},
              'dungeon': {'scudo': {'hp_scudo': 200}},
              'arena': {'scudo': {'hp_scudo': 800}},
              'turno': {'scudo': {'mod_bonus': 0.5}}},
 'Cavaliere del passaggio': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'MusicoSciamano': {'turno': {'blocco_set': {'blocca_set_avversario': True}}},
 'Taglialegna schivo': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Cultista oscuro': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Dolce mietitore': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Pyromante': {'generale': {'set_base': {'solo_bonus_base': True}}},
 'Proiettile': {'turno': {'difesa': {'mod_delta': -0.3}}, 'assalto': {'difesa': {'def': 40}}},
 'Pilota': {'ricompense': {'exp': {'bonus_probabilita_pct': 10}, 'duello': {'punti_bonus': 2}}},
 'Armaliere': {'generale': {'set_base': {'solo_bonus_base': True}}},
 "Controllore del'entrata": {'generale': {'set_base': {'solo_bonus_base': True}}},
 "Cavaliere d'argento": {'turno': {'recupero_colpo': {'mod_massimo': 0.8, 'mod_bonus': 0.2}}, 'assalto': {'danno_fisso': {'hp_massimi_divisore': 100, 'danno_minimo': 75}}},
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
        "assalto": {"aura": {"stat": "def", "minimo": 20, "percento_stat": 1}},
    },
    "Stemma del leader": {
        "assalto": {"aura": {"stat": "atk", "minimo": 20, "percento_stat": 1}},
    },
    "Occhio del falco": {
        "assalto": {"aura": {"stat": "agi", "minimo": 20, "percento_stat": 1}},
    },
    "Carica mobile": {
        "assalto": {"esplosione": {"proc": 50, "danno_min": 20, "danno_max": 150}},
    },
    "Polimerizzazione": {
        "assalto": {"polimerizzazione": {"proc": 100, "percento_stat": 20, "stats": ["atk", "def", "agi"]}},
    },
    "Valvola da 4\"": {
        "sfida": {"inizio": {"proc": 100, "atk": 100, "def": 100, "agi": 1}},
    },
    "Roulette russa": {
        "turno": {"roulette": {"proc": 16.6666666667, "lati": 6, "danno": 100}},
    },
    "Roulette tibetana": {
        "turno": {"roulette": {"proc": 16.6666666667, "lati": 6, "cura": 100}},
    },
    "Sasso rotolante": {
        "turno": {"valanga": {"proc": 10, "carica_per_turno": 1, "danno_per_carica": 2, "reset_dopo_proc": True}},
    },
    "WuWuWuuurm": {
        "turno": {"presa_schivata": {"proc": 30, "atk_base": 144, "danno_min": 20, "aggiungi_int": True}},
    },
    "Dance Dance Revolution": {
        "turno": {"combo": {"proc": 100, "incremento": 1, "bonus_danno_per_combo_pct": 10, "reset_su_mancata_schivata": True}},
    },
    "GDR semplificato": {
        "turno": {"formula": {"proc": 100, "attivo_per_entrambi": True, "danno_min": 0}},
    },
}


# ============================================================
# DATABASE HARDCODATO DEI NUCLEI
# ============================================================
NUCLEI_CONFIG = {
    "Nucleo elettrico instabile": {"assalto": {"stat_per_membro": {"agi": 30}}},
    "Nucleo marittimo instabile": {"assalto": {"stat_per_membro": {"hp": 300}}},
    "Nucleo demoniaco instabile": {"assalto": {"stat_per_membro": {"atk": 80}}},
    "Nucleo terrestre instabile": {"assalto": {"stat_per_membro": {"def": 80}}},
    "Nucleo selvaggio instabile": {
        "assalto": {"stat_per_membro": {"hp": 30, "atk": 30, "def": 30, "agi": 5}}
    },
    "Nucleo di bacon instabile": {"assalto": {"cura_per_struttura": 11}},
    "Nucleo Necron instabile": {"assalto": {"resurrezione": {"proc": 8, "hp": 1000}}},
}


# ============================================================
# MODIFICATORI WEEKEND
# ============================================================
# Chiavi macchina stabili; nome/descrizione sono ciò che vede il giocatore.
# Il pool mantiene circa un terzo di weekend senza modificatore.
WEEKEND_MOD_CONFIG = {
    "punti_extra": {
        "nome": "Punti extra",
        "descrizione": "Le sfide PvP assegnano 5 punti extra al vincitore.",
        "punti_extra": 5,
    },
    "calma": {
        "nome": "Calma",
        "descrizione": "Hai 55 secondi per rispondere a una sfida invece di 35.",
        "tempo_sfida": 55,
    },
    "sfide assurde": {
        "nome": "Sfide assurde",
        "descrizione": "Hai 28 secondi per rispondere a una sfida invece di 35.",
        "tempo_sfida": 28,
    },
    "stop_dg": {
        "nome": "Dungeon scialli",
        "descrizione": "Le azioni del dungeon richiedono 5 secondi in più.",
        "mod_dungeon": -5,
    },
    "più_dg": {
        "nome": "Più dungeon",
        "descrizione": "Le azioni del dungeon richiedono 5 secondi in meno.",
        "mod_dungeon": 5,
    },
    "flexville": {
        "nome": "Flexville",
        "descrizione": "Il tempo base per riprendersi dalla morte passa da 900 a 450 secondi.",
        "recupero_secondi": 450,
    },
    "ricchezze_sparse": {
        "nome": "Ricchezze sparse",
        "descrizione": "Quando una sfida PvP droppa un oggetto, ne ricevi 2 copie.",
        "quantita_drop_pvp": 2,
    },
    "senza_frontiere": {
        "nome": "Senza frontiere",
        "descrizione": "Spostarsi tra le zone richiede soltanto 5 secondi.",
        "tempo_movimento": 5,
    },
    "dungeon_brutti_sporti_cattivi": {
        "nome": "Dungeon brutti, sporti e cattivi",
        "descrizione": "I premi positivi del dungeon sono x2, ma le statistiche dei nemici e dei boss del dungeon sono x3.",
        "moltiplicatore_premi_dungeon": 2,
        "moltiplicatore_stat_dungeon": 3,
    },
    "piovono_incantesimi": {
        "nome": "Piovono incantesimi",
        "descrizione": "Ogni giocatore riceve 3 copie di un libro casuale all'inizio dell'evento e di nuovo a mezzanotte.",
        "quantita_libri": 3,
        "ripeti_mezzanotte": True,
    },
    "grazie_partecipato": {
        "nome": "Grazie di aver partecipato",
        "descrizione": "Ogni giocatore riceve 20 usabili comuni casuali.",
        "quantita_usabili": 20,
    },
}

WEEKEND_MOD_POOL = [
    "punti_extra",
    "calma",
    "sfide assurde",
    "stop_dg",
    "più_dg",
    "flexville",
    "ricchezze_sparse",
    "senza_frontiere",
    "dungeon_brutti_sporti_cattivi",
    "piovono_incantesimi",
    "grazie_partecipato",
    None, None, None, None, None, None,
]


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


# ============================================================
# INCANTESIMI
# Valori numerici usati dagli incantesimi. Le probabilità sono
# sempre espresse in percentuale 0..100.
# ============================================================
INCANTESIMI_CONFIG = {
    "Icore": {
        "turno": {"penetrazione": {"proc": 5, "difesa_target_mul": 0.6}},
    },
    "Ingrossamento": {
        "turno": {
            "crescita": {
                "proc": 2,
                "atk_min": 20,
                "atk_max": 100,
                "agi_min": -20,
                "agi_max": -2,
            }
        },
    },
    "Predominio": {
        "turno": {
            "difesa": {
                "dps_attaccante_mul": 0.8,
                "agi_attaccante": 30,
            }
        },
    },
    "Duraturo": {
        "turno": {"difesa": {"proc": 10, "difesa_mul": 1.7}},
    },
    "Smateriabile": {
        "turno": {
            "annulla_colpo": {"proc": 10},
            "tempesta_sabbia": {"proc": 30},
        },
        "interazioni": {
            "fire_lord": {"blocca": True},
        },
    },
    "Tocco fantasma": {
        "turno": {
            "colpo_schivato": {
                "proc": 2,
                "dps_percento_min": 5,
                "dps_percento_max": 10,
                "danno_min": 30,
            }
        },
    },
    "Leggiadra": {
        "turno": {
            "neutralizza_gadget": {
                "proc": 90,
                "blocca_anello_attaccante": True,
                "blocca_anello_difensore": True,
            }
        },
    },
    "Speranza": {
        "turno": {"salvezza": {"hp_min": 1, "hp_max": 60, "hp_porta_a": 100}},
    },
    "Velenoso": {
        "turno": {"veleno": {"proc": 5, "stack": 1, "danno_per_stack": 5}},
    },
    "Iridescente": {
        "turno": {"cura": {"proc": 5, "cura": 85}},
    },
    "Minimista": {
        "turno": {"danno_minimo": {"mod_min": 0.1, "danno_base_min": 10}},
    },
    "Mimico": {
        "turno": {"copia": {"attivo": True}},
    },
    "Affilatezza": {
        "turno": {"affila": {"proc": 10, "atk_mul": 1.2}},
    },
    "Legione": {
        "turno": {"duello_legione": {"dps_mul": 10}},
    },
    "Critico": {
        "turno": {"critico": {"proc": 8, "danno_mul": 1.5}},
    },
    "Primo impatto": {
        "turno": {"primo_colpo": {"danno_mul": 1.7}},
    },
    "Multiplo": {
        "turno": {"difesa": {"proc": 10, "agi": 8}},
    },
    "Legaccio": {
        "turno": {"lega": {"proc": 5, "agi_target_mul": 0.75}},
    },
    "Urlo di drago": {
        "turno": {"terrore": {"proc": 5}},
    },
    "Evocabilità": {
        "dungeon": {"supporto": {"atk": 40, "def": 40, "agi": 10}},
    },
    "Cangiante": {
        "generale": {
            "selezione_set": {"escludi_solo_bonus_base": True},
        },
        "turno": {
            "attacco": {"proc": 99},
            "difesa": {"proc": 99},
        },
    },
    "Inevitabile": {
        "turno": {"difesa": {"proc": 100, "danno_attaccante": 5, "danno_difensore": 5}},
    },
    "Spumeggiante": {
        "turno": {
            "attacco": {"proc": 8},
            "difesa": {"proc": 8},
        },
    },
    "Onde dell'abisso": {
        "assalto": {"onda": {"proc": 100, "atk_pct_min": 30, "atk_pct_max": 70}},
    },
    "Armadillibilità": {
        "assalto": {"morte": {"proc": 100, "def_pct": 100}},
    },
    "Giallo": {
        "assalto": {"aiutanti": {"proc": 50, "aiutanti_extra": 10}},
    },
    "Dominio semplice": {
        "turno": {
            "attacco": {"proc": 50, "costo_hp": 3},
            "difesa": {"proc": 50, "costo_hp": 3},
        },
    },
    "Caricato": {
        "turno": {
            "attacco": {
                "proc": 10,
                "cariche_per_proc": 1,
                "hp_sotto": 100,
                "danno_per_carica": 5,
                "reset_cariche": 0,
            }
        },
    },
    "Unione dello spirito": {
        "assalto": {
            "unione": {
                "proc": 100,
                "percento_stat": 20,
                "stats": ["atk", "def", "agi"],
            }
        },
    },

}


# Effetti temporanei non legati agli incantesimi.
EFFETTI_CONFIG = {
    "Fortunello": {
        "sfida": {
            "premio_oggetto": {
                "bonus_probabilita_per_livello_pct": 5,
            }
        }
    }
}

# --- SET EROI DELLA TEMPESTA: BILANCIAMENTO ---
PROC_CLASSI.update({
    "Guerriero Temporale": {
        "sfida": {"ciclo_temporale": {"hp": 100, "resurrezioni": 5}},
    },
    "Dannato primordiale": {
        "sfida": {"conversione": {"proc": 100}},
        "assalto": {"conversione": {"proc": 100}},
    },
    "Macellatore": {
        "sfida": {"presa_schivata": {"proc": 50, "moltiplicatore_danno": 2}},
    },
    "Mente centrale": {
        "assalto": {"alieno": {"proc": 50, "divisore_atk": 20}},
    },
    "Amletico": {
        "sfida": {"sacrificio": {"proc": 50, "percento_hp": 50}},
        "assalto": {"sacrificio": {"proc": 50, "percento_hp": 50}},
    },
    "Accumulatore di meraviglie": {
        "sfida": {
            "evocazione": {
                "proc": 50,
                "oggetti": {
                    "Un vaso": 5,
                    "Un sasso di medie dimensioni": 10,
                    "Un idropulitrice": 15,
                    "cento fiammiferi": 20,
                    "una mustang": 30,
                    "Sei cammelli": 40,
                    "LA LUNA": 100,
                },
            }
        },
    },
    "Anima della festa": {
        "sfida": {"seguaci": {"seguaci_per_turno": 1, "percento_stat_per_seguace": 2}},
        "assalto": {"last": {"moltiplicatore": 1.5}},
    },
    "Zanno": {
        "generale": {"set_base": {"solo_bonus_base": True}},
    },
    "Uditore del profondo": {
        "sfida": {"richiamo": {"hp_trigger": 1, "danno": 1000000000}},
        "assalto": {"richiamo": {"hp_trigger": 1, "danno": 1000000000}},
    },
    "Monarca della tempesta di fuoco": {
        "sfida": {"incantamenti": {"nomi": ["Iridescente", "Minimista", "Primo impatto", "Icore"]}},
    },
    "Evocatore delle maree": {
        "assalto": {
            "onda": {"incantesimo": "Onde dell'abisso"},
            "tsunami": {"percento_atk": 10},
        },
    },
    "Mecha sciamano": {
        "sfida": {"riuso_approccio": {"danno_hp": 10}},
    },
})


# --- SECONDA ONDATA SET: BILANCIAMENTO ---
PROC_CLASSI.update({
    "Anima persa": {"sfida": {"schivata_negata": {"hp": 200}}},
    "Disabilitatore provetto": {"assalto": {"muraglione": {"atk_mul": 4}}},
    "Controllore del cielo": {"sfida": {"cura_in_potere": {"atk_divisore": 2, "def_divisore": 2}}},
    "Eterna sventura": {"sfida": {"sventura": {"proc": 20, "atk_target": -10, "def_target": -10, "agi_target": -10}}},
    "Pescatore alternativo": {"sfida": {"azzardo": {"proc": 50, "atk_mul": 2, "def_mul": 0.5}}},
    "Esca vivente": {"sfida": {"esca": {"def": 0}}, "assalto": {"esca": {"def": 0}}},
    "Giustiziere a V": {"sfida": {"giudizio": {"turno_min": 4, "agi_mul": 2}}, "assalto": {"accampamento": {"atk_mul": 6}}},
})


# --- TERZA ONDATA SET: NOVE SET ---
PROC_CLASSI.update({
    "Monarca oscuro": {
        "combattimento": {"inizio": {"hp_target_percento": 60}},
        "assalto": {"last": {"danno_per_last": 10, "finestra_secondi": 301}},
    },
    "Oscurato": {
        "combattimento": {"riflesso": {"percento": 5}},
        "assalto": {"riflesso": {"percento": 5}},
    },
    "Demone delle lame": {
        "combattimento": {"danno_extra": {"percento": 20}},
        "assalto": {"danno_extra": {"percento": 30}},
    },
    "Re dei gadget": {
        "combattimento": {"intelletto": {"int": 200}},
    },
    "Il comico": {
        "combattimento": {"confusione": {"proc": 15}},
        "assalto": {"clap": {"solo_testo": True}},
    },
    "Survival medievale": {
        "generale": {"set_base": {"solo_bonus_base": True}},
    },
    "Duellista vermico": {
        "combattimento": {"vermi": {"proc": 11, "primo_garantito": True, "atk": 1, "def": 1, "hp": 20}},
        "assalto": {"vermi": {"proc": 11, "primo_garantito": True, "atk": 1, "def": 1, "hp": 20}},
    },
    "Cacciatore d'esce": {
        "combattimento": {"secondo_colpo": {"proc": 40, "percento_danno": 50}},
        "assalto": {"secondo_colpo": {"proc": 40, "percento_danno": 50}},
    },
    "Duro a morire": {
        "generale": {"set_base": {"solo_bonus_base": True}},
    },
})


# --- QUARTA ONDATA SET: SEI SET ---
PROC_CLASSI.update({
    "Primo alla torre": {
        "combattimento": {"primo_colpo": {"moltiplicatore_danno": 2}},
        "assalto": {"clone": {"atk_mul": 4}},
    },
    "Pazzo temporale": {
        "combattimento": {"seed": {"proc": 90, "seed": "Anello perfezionista"}},
        "assalto": {"seed": {"proc": 90, "seed": "Anello perfezionista"}},
    },
    "Evocatore del vero potere": {
        "combattimento": {"canto": {"proc": 1, "anello": "Anello superfortissimo ma proprio rotto sgravatissimo"}},
    },
    "GunSlingher": {
        "combattimento": {"raffica": {"colpi_min": 1, "colpi_max": 6, "danno_per_colpo": 20}},
        "assalto": {"raffica_clone": {"colpi_min": 1, "colpi_max": 6, "danno_per_colpo": 60}},
    },
    "Arcidemone": {
        "combattimento": {"cura_nemica": {"atk": 4000}},
    },
    "Big Game Hunter": {
        "combattimento": {"copia_agilita": {"attivo": True}},
    },
})


# --- QUINTA ONDATA SET: TREDICI SET ---
PROC_CLASSI.update({
    "Nucleo dell'uragano": {
        "combattimento": {"proc_anello_avversario": {"percento_atk_proprio": 10}},
        "assalto": {"immunita": {"struttura": "Spuntone malefico", "messaggio": "🌪 Il vento spazza via la trappola dello Spuntone malefico!"}},
    },
    "Tormento di fuoco": {
        "combattimento": {"proc_anello_avversario": {"percento_atk_avversario": 10}},
        "assalto": {"immunita": {"struttura": "Fabbro incantaspade", "messaggio": "🔥 Il Fabbro incantaspade non riesce a scalfirti: il tormento di fuoco lo sovrasta!"}},
    },
    "Girarrosto": {
        "combattimento": {"salvezza": {"hp_soglia_percento": 50, "hp_ripristino_percento": 100, "usi": 1}},
        "assalto": {"salvezza": {"hp_soglia_percento": 50, "hp_ripristino_percento": 100, "usi": 1}},
    },
    "Venere di ferro": {
        "combattimento": {"riduzione_danno": {"percento": 20}},
        "assalto": {"riduzione_danno": {"percento": 30}},
    },
    "Rosso D'ossidina": {
        "combattimento": {"riuso_approccio": {"attivo": True}},
        "assalto": {"immunita": {"struttura": "Sedimento del cucciolo", "messaggio": "🔴 Il drago è troppo arrabbiato per riuscire a farti del male!"}},
    },
    "Oltraggioso": {
        "combattimento": {"cap_danno": {"massimo": 50}},
        "assalto": {"immunita": {"struttura": "Chiesa", "messaggio": "⛪ L'oltraggio è tale che perfino la Chiesa rinuncia a danneggiarti!"}},
    },
    "Festante oscuro": {
        "combattimento": {"fantasmi": {"percento_ritorno": 50}},
        "assalto": {"immunita": {"struttura": "Cane da guardia", "messaggio": "👻 Il Cane da guardia si perde tra le ombre e non riesce a colpirti!"}},
    },
    "Legionaro di Evelin": {
        "combattimento": {"danno_turno": {"parita": "dispari", "danno": 50}},
        "assalto": {"immunita": {"struttura": "Accampamento", "messaggio": "🦅 Nessuno nell'Accampamento vuole mettersi contro Evelin!"}},
    },
    "Neo Genesi": {
        "combattimento": {"danno_turno": {"parita": "pari", "danno": 50}},
        "assalto": {"immunita": {"struttura": "Spaventapasseri ornamentale", "messaggio": "✨ Lo Spaventapasseri ornamentale non osa muoversi davanti a cotanta potenza!"}},
    },
    "Intermezzo": {
        "combattimento": {"cariche_schivata": {"soglia_1": 3, "bonus_1": 5, "soglia_2": 5, "bonus_2": 15, "soglia_3": 8, "moltiplicatore": 2}},
        "assalto": {"immunita": {"struttura": "Muraglione extra", "messaggio": "🪽 Fluttui oltre il Muraglione extra in completa tranquillità!"}},
    },
    "Obscurio": {
        "combattimento": {"anti_cura": {"attivo": True}},
        "assalto": {"immunita": {"struttura": "Stazione laser di sicurezza", "messaggio": "🌑 La luce compressa della Stazione laser non riesce a illuminarti!"}},
    },
    "Primo al comando": {
        "combattimento": {"proc_anello": {"cura": 30}},
        "assalto": {"immunita": {"struttura": "Clone", "messaggio": "🫡 Il Clone riconosce il Primo al comando e non riesce a danneggiarlo!"}},
    },
    "Luce persa": {
        "combattimento": {"conversione": {"agi_mul": 4, "quota_atk": 0.5, "quota_def": 0.5}},
        "assalto": {"conversione": {"agi_mul": 4, "quota_atk": 0.5, "quota_def": 0.5}},
    },
})


# --- FARO E GENERATORE INCARTATO ---
PROC_ANELLI.setdefault("Un generatore incartato", {})["ricompense"] = {
    "incartato": {"proc": 66, "quantita": 1},
}
DUNGEON_CONFIG.setdefault("stanze", {})["Faro"] = {
    "Vedere": {"livello_premio": 2},
    "Essere visto": {"boss_aggiunti": 2},
}

# ============================================================
# CONFIGURAZIONE STRUTTURE D'ASSALTO
# ============================================================
# I valori base HP/statistiche e le modalita' disponibili restano in liste.py
# (hps, starmi, spec, frasispec). Qui vive tutto il tuning numerico che prima
# era hardcodato dentro assedio(), cosi' runtime e wiki leggono la stessa fonte.
STRUTTURE_CONFIG = {
    "generale": {
        "scaling": {"divisore_livello": 10},
        "ultima_struttura": {"atk_delta": -100, "agi_delta": -10, "def_delta": -300},
        "tiro": {"agi_difensore_divisore": 2, "bonus": 1, "random_max": 102},
        "danno": {
            "difesa": {"numeratore": 100, "difesa_base": 1, "random_min": 0.7, "random_max": 1.5},
            "spuntone": {"numeratore": 100, "difesa_base": 50, "random_min": 0.7, "random_max": 1.5},
            "attaccante": {"numeratore": 100, "difesa_base": 1, "random_min": 0.7, "random_max": 1.3},
        },
        "danno_minimo": 5,
    },
    "Bersaglio enorme": {
        "generale": {"distrazione_proc": 20},
        "modalita": {
            "Classico": {},
            "Movibile": {"colpito_proc": 30, "danno_mul": 4},
        },
    },
    "Muraglione extra": {
        "generale": {
            "def_attaccante_mul": 0.5,
            "bonus_def_per_livello": 5,
            "bonus_def_strutture_divisore": 4,
            "infezione_proc": 10,
            "infezione_def_delta": -50,
        },
        "modalita": {
            "Possente": {},
            "Infiammato": {"danno_bonus": 250, "autodanno": 100},
        },
    },
    "Spaventapasseri ornamentale": {
        "modalita": {
            "Magico": {"attacco_diretto": False, "corvi_proc": 10},
            "Animato": {"attacco_diretto": True},
        },
    },
    "Clone": {
        "generale": {"bonus_atk_difese_su_mancato_colpo": 20},
        "modalita": {
            "Aggressivo": {},
            "Difensivo": {"agi_delta": -40},
        },
    },
    "Chiesa": {
        "modalita": {
            "Credente": {"attacco_diretto": True},
            "Orribile": {
                "attacco_diretto": False,
                "creatura_proc": 10,
                "bonus_atk": 250,
                "bonus_def": 250,
                "bonus_agi": 25,
            },
        },
    },
    "Accampamento": {
        "modalita": {
            "Trappole danneggianti": {},
            "Trappole demoralizzanti": {"danno_divisore": 1.3, "bonus_atk_difese": 50},
        },
    },
    "Cane da guardia": {
        "generale": {"rincorsa_proc": 30, "rincorsa_danno_divisore": 2},
        "modalita": {
            "Cane possente": {},
            "Cane rapido": {"danno_divisore": 1.3, "rincorse_extra_max": 4, "rincorsa_extra_proc": 50},
            "Orso": {"danno_mul": 1.5, "rincorsa_disabilitata": True},
        },
    },
    "Stazione laser di sicurezza": {
        "generale": {"bonus_def_proc": 10, "bonus_def_per_livello": 10},
        "modalita": {
            "Mitragliatrice laser": {},
            "Difesa laser": {"atk_da_def_mul": 2, "def_da_atk_divisore": 2},
            "Suicidio laser": {"autodanno": 55, "atk_mul": 2.5, "agi_delta": -26},
        },
    },
    "Spuntone malefico": {
        "generale": {"stop_proc": 60, "bonus_def_per_livello": 2},
        "modalita": {
            "Palese": {"roll_bonus_pct": 0},
            "Sotterraneo": {"agi_delta": -25, "roll_bonus_pct": 20},
        },
    },
    "Cannoncino": {
        "generale": {"bonus_agi_difese": 5, "drago_proc": 10, "drago_bonus_agi": 20},
        "modalita": {
            "Rumoroso": {},
            "Danneggiante": {"danno_mul": 2},
        },
    },
    "Sedimento del cucciolo": {
        "generale": {"mamma_proc": 10, "mamma_hp_min": -2, "mamma_hp_max": 10},
        "modalita": {
            "Assonnato": {},
            "Affamato": {"agi_delta": 55, "atk_divisore": 1.5},
        },
    },
    "Centrale di cura centralizzata": {
        "generale": {"valore_per_livello": 3, "hp_minimo_modifica": 50},
        "modalita": {
            "Sparsa": {"bersagli": "tutti"},
            "Concentrata": {"bersagli": 1},
        },
    },
    "Fabbro incantaspade": {
        "generale": {"bonus_atk_per_livello": 25, "bonus_def_per_livello": 25},
        "modalita": {
            "Malevolo": {"attacco_diretto": True},
            "Curativo": {"attacco_diretto": False, "cura": True},
        },
    },
}

# --- PODIO DUNGEON / IMBOSCATE ---
DUNGEON_CONFIG.setdefault("generale", {}).update({
    "podio_livello_base": 4,
    "podio_gloria_base": 6,
    "podio_gloria_moltiplicatore": 2,
    "imboscata": {"proc": 0.5, "nemici": 2},
})
DUNGEON_CONFIG.setdefault("stanze", {})["Podio"] = {
    "1° posto": {"posizione": 1},
    "2° posto": {"posizione": 2},
    "3° posto": {"posizione": 3},
}

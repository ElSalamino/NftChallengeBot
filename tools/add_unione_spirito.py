from pathlib import Path

# 1) Config incantesimo
p = Path('bilanciamento.py')
s = p.read_text(encoding='utf-8')
needle = '''    "Caricato": {
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

}'''
replacement = '''    "Caricato": {
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

}'''
if needle not in s:
    raise SystemExit('Punto INCANTESIMI_CONFIG non trovato')
s = s.replace(needle, replacement, 1)
p.write_text(s, encoding='utf-8')

# 2) Frase tecnica
p = Path('frasi_incantesimi.py')
s = p.read_text(encoding='utf-8')
needle = '''    "Caricato": "A ogni attacco hai il {turno.attacco.proc:pct} di ottenere {turno.attacco.cariche_per_proc} carica. Se dopo il controllo hai meno di {turno.attacco.hp_sotto} HP e almeno una carica, le scarichi tutte infliggendo {turno.attacco.danno_per_carica} danni diretti per carica, poi il contatore torna a {turno.attacco.reset_cariche}.",

}'''
replacement = '''    "Caricato": "A ogni attacco hai il {turno.attacco.proc:pct} di ottenere {turno.attacco.cariche_per_proc} carica. Se dopo il controllo hai meno di {turno.attacco.hp_sotto} HP e almeno una carica, le scarichi tutte infliggendo {turno.attacco.danno_per_carica} danni diretti per carica, poi il contatore torna a {turno.attacco.reset_cariche}.",
    "Unione dello spirito": "ASSALTO — se possiedi Unione dello spirito, ogni altro membro del clan che possiede lo stesso incantesimo ti trasferisce il {assalto.unione.percento_stat:pct} del proprio ATK, DEF e AGI all'inizio dell'assalto. I contributi di più compagni si sommano.",

}'''
if needle not in s:
    raise SystemExit('Punto frasi_incantesimi non trovato')
s = s.replace(needle, replacement, 1)
p.write_text(s, encoding='utf-8')

# 3) Libro / lore
p = Path('liste.py')
s = p.read_text(encoding='utf-8')
needle = '''           "Cerficato della nuova ombra": {"ef": "Dominio semplice", "descrizione": "Nuova ombra acquisita, per poca forza vitale blocca tecniche strane nemiche"},
           "Manuale di meccanica pt 3": {"ef": "Caricato", "descrizione": "Prepara il colpo e assicurati di finire il lavoro"}
}'''
replacement = '''           "Cerficato della nuova ombra": {"ef": "Dominio semplice", "descrizione": "Nuova ombra acquisita, per poca forza vitale blocca tecniche strane nemiche"},
           "Manuale di meccanica pt 3": {"ef": "Caricato", "descrizione": "Prepara il colpo e assicurati di finire il lavoro"},
           "Fumetto hot degli anni 70": {"ef": "Unione dello spirito", "descrizione": "Unisci il tuo spirito a quello dei compagni e diventa più forte insieme a loro."}
}'''
if needle not in s:
    raise SystemExit('Punto libri non trovato')
s = s.replace(needle, replacement, 1)
p.write_text(s, encoding='utf-8')

# 4) Logica assalto: stessa semantica di Polimerizzazione, ma sugli incantesimi
p = Path('nft.py')
s = p.read_text(encoding='utf-8')
needle = '''                text += (
                    f"La polimerizzazione di {pl} eccheggia, dandoti "
                    f"{_numero_placeholder_tecnico(bonus_poly['atk'])} atk "
                    f"{_numero_placeholder_tecnico(bonus_poly['def'])} def e "
                    f"{_numero_placeholder_tecnico(bonus_poly['agi'])} agilità!\\n"
                )

            if aniel in PROC_ANELLI and "aura" in PROC_ANELLI[aniel].get("assalto", {}):'''
replacement = '''                text += (
                    f"La polimerizzazione di {pl} eccheggia, dandoti "
                    f"{_numero_placeholder_tecnico(bonus_poly['atk'])} atk "
                    f"{_numero_placeholder_tecnico(bonus_poly['def'])} def e "
                    f"{_numero_placeholder_tecnico(bonus_poly['agi'])} agilità!\\n"
                )

            if (
                "Unione dello spirito" in player.get("incantamenti", [])
                and pl != nome
                and "Unione dello spirito" in get_ench(playerg[pl])
            ):
                cfg_unione = incantesimo_cfg("Unione dello spirito", "assalto", "unione")
                bonus_unione = {}
                for stat_unione in cfg_unione["stats"]:
                    valore_unione = scheda_membro.get(stat_unione, 0) * cfg_unione["percento_stat"] / 100
                    player[stat_unione] += valore_unione
                    bonus_unione[stat_unione] = valore_unione
                text += (
                    f"L'unione dello spirito di {pl} risuona, dandoti "
                    f"{_numero_placeholder_tecnico(bonus_unione['atk'])} atk "
                    f"{_numero_placeholder_tecnico(bonus_unione['def'])} def e "
                    f"{_numero_placeholder_tecnico(bonus_unione['agi'])} agilità!\\n"
                )

            if aniel in PROC_ANELLI and "aura" in PROC_ANELLI[aniel].get("assalto", {}):'''
if needle not in s:
    raise SystemExit('Punto Polimerizzazione in nft.py non trovato')
s = s.replace(needle, replacement, 1)
p.write_text(s, encoding='utf-8')

print('Unione dello spirito aggiunta.')

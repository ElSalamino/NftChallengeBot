#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit wiki: usabili e descrizioni leggibili dell'assalto."""
import run_wiki
from frasi_usabili import FRASI_USABILI_TECNICHE

wiki = run_wiki.wiki

# Compatibilità con l'audit v3 già esistente.
wiki.bilanciamento = wiki.v3.bilanciamento
wiki.liste = wiki.v3.liste
wiki.v2 = wiki.v3.v2
import validate_wiki  # noqa: F401,E402  - esegue l'audit v3 all'import


data = wiki.build_data()
errors = []
wiki_version = int(data.get("meta", {}).get("wiki_version", 4))

# --- Usabili --------------------------------------------------------------
expected_usables = set(wiki.v3.liste.usabili)
technical_usables = set(FRASI_USABILI_TECNICHE)
if expected_usables != technical_usables:
    missing = sorted(expected_usables - technical_usables)
    extra = sorted(technical_usables - expected_usables)
    if missing:
        errors.append(f"descrizioni tecniche usabili mancanti: {missing}")
    if extra:
        errors.append(f"descrizioni tecniche usabili senza voce in liste.usabili: {extra}")

items = {item["name"]: item for item in data["items"]}
for name in sorted(expected_usables):
    item = items.get(name)
    if not item:
        errors.append(f"usabile non esposto come item: {name}")
        continue
    if "Usabile" not in item.get("types", []):
        errors.append(f"item usabile senza tipologia Usabile: {name}")
    if not (item.get("description") or "").strip():
        errors.append(f"usabile senza descrizione narrativa: {name}")
    if not (item.get("usable_technical") or "").strip():
        errors.append(f"usabile senza descrizione tecnica: {name}")

if ".replace(/'/g,'%27')" not in wiki.HTML:
    errors.append("router wiki senza escape %27 per apostrofi")
if "Effetto tecnico dell’usabile" not in wiki.HTML:
    errors.append("pagina item senza sezione tecnica degli usabili")

# --- Assalto --------------------------------------------------------------
if "modeTechnical" not in wiki.HTML:
    errors.append("cambio modalità non aggiorna il testo dell'effetto")
if 'id="modeConfig"' in wiki.HTML:
    errors.append("pagina assalto espone ancora la configurazione grezza")

if wiki_version >= 5:
    if "Effetto della modalità" not in wiki.HTML:
        errors.append("pagina struttura senza sezione Effetto della modalità")
    if 'id="modeDesc"' in wiki.HTML:
        errors.append("pagina struttura mostra ancora la descrizione duplicata della modalità")
    if "Funzionamento tecnico completo" in wiki.HTML:
        errors.append("pagina struttura usa ancora il vecchio blocco tecnico ridondante")
else:
    if "Funzionamento tecnico completo" not in wiki.HTML:
        errors.append("pagina struttura v4 senza testo tecnico completo")

for structure in data["assault"]:
    for mode in structure["modes"]:
        expected_text, expected_rows = wiki._structure_technical(structure["name"], mode["name"])
        actual_rows = mode.get("technical_params", [])
        actual_text = mode.get("technical", "")

        expected_pairs = [(r["path"], r["value"]) for r in expected_rows]
        actual_pairs = [(r["path"], r["value"]) for r in actual_rows]
        if actual_pairs != expected_pairs:
            errors.append(f"{structure['name']} / {mode['name']}: lista parametri incompleta")

        if actual_text != expected_text:
            errors.append(f"{structure['name']} / {mode['name']}: testo effetto non sincronizzato")

        lowered = actual_text.lower()
        if "true" in lowered or "false" in lowered:
            errors.append(f"{structure['name']} / {mode['name']}: contiene True/False nel testo")
        if "=" in actual_text:
            errors.append(f"{structure['name']} / {mode['name']}: contiene assegnazioni grezze nel testo")

        if wiki_version >= 5:
            # Lo scaling globale resta nel JSON e nelle tabelle, ma non deve
            # essere ripetuto nelle frasi giocatore.
            if "Le statistiche base della struttura aumentano" in actual_text:
                errors.append(f"{structure['name']} / {mode['name']}: ripete lo scaling globale per livello")
        else:
            # Compatibilità v4: ogni parametro aveva la sua frase dedicata.
            for row in expected_rows:
                phrase = wiki._human_param(row["path"], row["value"])
                if phrase not in actual_text:
                    errors.append(f"{structure['name']} / {mode['name']}: manca la frase per {row['path']}")

# Regressioni esplicite sulle frasi che devono essere comprensibili.
bersaglio = next((x for x in data["assault"] if x["name"] == "Bersaglio enorme"), None)
if not bersaglio:
    errors.append("Bersaglio enorme mancante")
else:
    for mode in bersaglio["modes"]:
        text = mode.get("technical", "")
        if wiki_version >= 5:
            if "20%" not in text or "forzare l'attaccante a colpire il Bersaglio enorme" not in text:
                errors.append(f"Bersaglio enorme / {mode['name']}: distrazione non spiegata chiaramente")
        elif "20%" not in text or "distrarre l'attaccante" not in text:
            errors.append(f"Bersaglio enorme / {mode['name']}: non spiega il 20% di distrazione")

muraglione = next((x for x in data["assault"] if x["name"] == "Muraglione extra"), None)
if not muraglione:
    errors.append("Muraglione extra mancante")
else:
    general_paths = {
        r["path"]
        for r in wiki._prefixed_flatten(
            "generale",
            wiki.v3.bilanciamento.STRUTTURE_CONFIG.get("Muraglione extra", {}).get("generale", {}),
        )
    }
    for mode in muraglione["modes"]:
        shown = {r["path"] for r in mode.get("technical_params", [])}
        missing = general_paths - shown
        if missing:
            errors.append(f"Muraglione extra / {mode['name']}: variabili generali mancanti {sorted(missing)}")

if wiki_version >= 5:
    sedimento = next((x for x in data["assault"] if x["name"] == "Sedimento del cucciolo"), None)
    if not sedimento:
        errors.append("Sedimento del cucciolo mancante")
    else:
        for mode in sedimento["modes"]:
            text = mode.get("technical", "")
            if not all(token in text for token in ("10%", "HP dell'attaccante", "tra -2 e 10")):
                errors.append(f"Sedimento del cucciolo / {mode['name']}: intervento della madre non spiegato")

    cannoncino = next((x for x in data["assault"] if x["name"] == "Cannoncino"), None)
    if not cannoncino:
        errors.append("Cannoncino mancante")
    else:
        for mode in cannoncino["modes"]:
            text = mode.get("technical", "")
            if "drago" not in text.lower() or "+20 AGI" not in text:
                errors.append(f"Cannoncino / {mode['name']}: effetto del drago non spiegato")

if errors:
    print("ERRORI WIKI:")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

print("Integrità wiki OK")
print(f"{len(expected_usables)} usabili con descrizione tecnica completa")
if wiki_version >= 5:
    print("Assalto: un solo testo per modalità, effetti raggruppati e scaling globale non ripetuto.")
else:
    print("Assalto v4 compatibile: parametri completi e frasi leggibili.")

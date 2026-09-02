#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit aggiuntivo wiki v4: usabili e descrizioni leggibili dell'assalto."""
import run_wiki
from frasi_usabili import FRASI_USABILI_TECNICHE

wiki = run_wiki.wiki

# Compatibilità con l'audit v3 già esistente: prima lo facciamo girare
# integralmente anche sulla v4, poi aggiungiamo i vincoli nuovi.
wiki.bilanciamento = wiki.v3.bilanciamento
wiki.liste = wiki.v3.liste
wiki.v2 = wiki.v3.v2
import validate_wiki  # noqa: F401,E402  - esegue l'audit v3 all'import


data = wiki.build_data()
errors = []

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

# encodeURIComponent non codifica l'apostrofo: il fix %27 deve essere presente
# per rendere navigabili Dell'ambrosia e tutti i nomi analoghi negli onclick.
if ".replace(/'/g,'%27')" not in wiki.HTML:
    errors.append("router wiki senza escape %27 per apostrofi")
if "Effetto tecnico dell’usabile" not in wiki.HTML:
    errors.append("pagina item senza sezione tecnica degli usabili")

# --- Assalto --------------------------------------------------------------
if "Funzionamento tecnico completo" not in wiki.HTML:
    errors.append("pagina struttura senza testo tecnico completo")
if "modeTechnical" not in wiki.HTML:
    errors.append("cambio modalità non aggiorna il testo tecnico")

# I parametri grezzi devono restare nel JSON per audit, ma non essere mostrati
# nella pagina struttura.
if 'id="modeConfig"' in wiki.HTML:
    errors.append("pagina assalto espone ancora la configurazione grezza")

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
            errors.append(f"{structure['name']} / {mode['name']}: testo tecnico non sincronizzato")

        # Vietiamo esplicitamente la resa da sviluppatore nel testo giocatore.
        lowered = actual_text.lower()
        if "true" in lowered or "false" in lowered:
            errors.append(f"{structure['name']} / {mode['name']}: contiene True/False nel testo")
        if "=" in actual_text:
            errors.append(f"{structure['name']} / {mode['name']}: contiene assegnazioni grezze nel testo")

        # Ogni parametro configurato deve produrre una frase comprensibile.
        for row in expected_rows:
            phrase = wiki._human_param(row["path"], row["value"])
            if phrase not in actual_text:
                errors.append(
                    f"{structure['name']} / {mode['name']}: manca la frase per {row['path']}"
                )

# Regressioni esplicite segnalate dall'utente.
bersaglio = next((x for x in data["assault"] if x["name"] == "Bersaglio enorme"), None)
if not bersaglio:
    errors.append("Bersaglio enorme mancante")
else:
    for mode in bersaglio["modes"]:
        if "20%" not in mode.get("technical", "") or "distrarre l'attaccante" not in mode.get("technical", ""):
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

if errors:
    print("ERRORI WIKI V4:")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

print("Integrità wiki v4 OK")
print(f"{len(expected_usables)} usabili con descrizione tecnica completa")
print("Tutte le modalità d'assalto mantengono i parametri per audit e mostrano solo frasi leggibili.")

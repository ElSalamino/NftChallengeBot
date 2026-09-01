import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from bilanciamento import PROC_CLASSI
from frasi_set import FRASI_SET_TECNICHE

FORMAT_RE = re.compile(r"\{([^{}]+)\}")


def leaf_paths(value, prefix=""):
    out = []
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            out.extend(leaf_paths(child, path))
    else:
        out.append(prefix)
    return out


def placeholders(text):
    result = set()
    for raw in FORMAT_RE.findall(text or ""):
        path = raw.split(":", 1)[0]
        result.add(path)
    return result

missing_by_set = {}
for nome_set, cfg in PROC_CLASSI.items():
    frase = FRASI_SET_TECNICHE.get(nome_set, "")
    refs = placeholders(frase)
    leaves = set(leaf_paths(cfg))
    missing = sorted(leaves - refs)
    if missing:
        missing_by_set[nome_set] = missing

phrases_without_config = sorted(set(FRASI_SET_TECNICHE) - set(PROC_CLASSI))
configs_without_phrase = sorted(set(PROC_CLASSI) - set(FRASI_SET_TECNICHE))

print(f"SET IN PROC_CLASSI: {len(PROC_CLASSI)}")
print(f"FRASI TECNICHE: {len(FRASI_SET_TECNICHE)}")
print(f"SET CON VARIABILI MANCANTI: {len(missing_by_set)}")
print(f"CONFIG SENZA FRASE: {len(configs_without_phrase)}")
print(f"FRASI SENZA CONFIG: {len(phrases_without_config)}")
print()

for nome_set in sorted(missing_by_set, key=str.lower):
    print(f"[{nome_set}]")
    for path in missing_by_set[nome_set]:
        print(f"  - {path}")

if configs_without_phrase:
    print("\n[CONFIG SENZA FRASE]")
    for nome in configs_without_phrase:
        print(f"  - {nome}")

if phrases_without_config:
    print("\n[FRASI SENZA CONFIG]")
    for nome in phrases_without_config:
        print(f"  - {nome}")

raise SystemExit(1 if missing_by_set or configs_without_phrase else 0)

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

# Riparti esattamente dai tre sorgenti di main, eliminando rumore whitespace/pyc dei run precedenti.
for path in ("bilanciamento.py", "nft.py", "turno_assalto.py"):
    subprocess.run(["git", "checkout", "origin/main", "--", path], cwd=ROOT, check=True)

# Recupera ed esegue lo script di refactor validato dal commit precedente.
script = subprocess.check_output(
    ["git", "show", "3c85581e26804e9777f86ed0c071d0d54e396934:.github/refactor_strutture.py"],
    cwd=ROOT,
    text=True,
)
namespace = {"__file__": str(ROOT / ".github" / "refactor_strutture.py"), "__name__": "__main__"}
exec(compile(script, namespace["__file__"], "exec"), namespace, namespace)

# Pulisce esclusivamente whitespace introdotto sulle nuove righe data-driven.
ta = ROOT / "turno_assalto.py"
lines = ta.read_text(encoding="utf-8").splitlines(keepends=True)
cleaned = []
for line in lines:
    if "struttura_" in line:
        newline = "\n" if line.endswith("\n") else ""
        line = line.rstrip(" \t\r\n") + newline
    cleaned.append(line)
ta.write_text("".join(cleaned), encoding="utf-8")

# Una sola newline finale nel nuovo dizionario.
bil = ROOT / "bilanciamento.py"
b = bil.read_text(encoding="utf-8").rstrip() + "\n"
bil.write_text(b, encoding="utf-8")

print("Refactor strutture ripulito dalla base main")

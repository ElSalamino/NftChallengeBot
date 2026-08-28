from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]

nft_path = ROOT / "nft.py"
init_path = ROOT / "__init__.py"

nft = nft_path.read_text(encoding="utf-8")
ini = init_path.read_text(encoding="utf-8")

if "def tempo_movimento_corrente(" not in nft:
    anchor = '''def set_weekend_mod(mod):
    global _WEEKEND_MOD_ATTIVO
    _WEEKEND_MOD_ATTIVO = mod


'''
    helper = '''def set_weekend_mod(mod):
    global _WEEKEND_MOD_ATTIVO
    _WEEKEND_MOD_ATTIVO = mod


def tempo_movimento_corrente(player, username, trader):
    """Cooldown reale per il movimento, condiviso tra UI e callback."""
    ccc = 3600
    if _WEEKEND_MOD_ATTIVO == "senza_frontiere":
        return weekend_mod_val(_WEEKEND_MOD_ATTIVO, "tempo_movimento", 5)
    if player[username]["setta"]["benedizione"] == "Verme delle sabbie":
        a = round(
            trader["sette"][player[username]["setta"]["loc"]]["power"]
            * (trader["sette"][player[username]["setta"]["loc"]]["%"] / 100)
        )
        ccc *= 1 - (a / 100)
    return ccc


'''
    if anchor not in nft:
        raise RuntimeError("Anchor set_weekend_mod non trovato")
    nft = nft.replace(anchor, helper, 1)

old = '''        ccc = 3600
        if _WEEKEND_MOD_ATTIVO == "senza_frontiere":
            ccc = weekend_mod_val(_WEEKEND_MOD_ATTIVO, "tempo_movimento", 5)
        elif player[username]["setta"]["benedizione"] == "Verme delle sabbie":
            a = round(trader["sette"][player[username]["setta"]["loc"]]["power"] * (trader["sette"][player[username]["setta"]["loc"]]["%"]/100))
            ccc *= 1 - (a/100)
'''
new = '''        ccc = tempo_movimento_corrente(player, username, trader)
'''
if old in nft:
    nft = nft.replace(old, new, 1)
elif new not in nft:
    raise RuntimeError("Blocco cooldown movimento non trovato")

old_ui = '''    if ora - player[message.from_user.username]["last"] >= 3600:
        text += "🚩 Ci si può spostare\\n"
'''
new_ui = '''    if ora - player[message.from_user.username]["last"] >= nft.tempo_movimento_corrente(player, message.from_user.username, trader):
        text += "🚩 Ci si può spostare\\n"
'''
numero_ui = ini.count(old_ui)
if numero_ui:
    ini = ini.replace(old_ui, new_ui)
elif new_ui not in ini:
    raise RuntimeError("Indicatori movimento menu non trovati")

nft_path.write_text(nft, encoding="utf-8")
init_path.write_text(ini, encoding="utf-8")

ast.parse(nft, filename="nft.py")
assert "def tempo_movimento_corrente(" in nft
assert "ccc = tempo_movimento_corrente(player, username, trader)" in nft
assert ini.count('nft.tempo_movimento_corrente(player, message.from_user.username, trader)') >= 2
assert old_ui not in ini
print(f"Movimento weekend allineato; indicatori aggiornati: {numero_ui or 'gia presenti'}")

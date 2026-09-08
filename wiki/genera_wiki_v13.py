#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wiki v13: interfaccia e contenuti localizzati in italiano, inglese e spagnolo."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import genera_wiki_v12 as v12

ROOT = v12.ROOT
v11 = v12.v11
v10 = v12.v10
v9 = v12.v9
v8 = v12.v8
v7 = v12.v7
v6 = v12.v6
v5 = v12.v5
v4 = v12.v4
v3 = v12.v3
v2 = v12.v2
bilanciamento = v12.bilanciamento
liste = v12.liste
_prefixed_flatten = v12._prefixed_flatten
_structure_technical = v12._structure_technical


def build_data():
    data = v12.build_data()
    data["meta"]["wiki_version"] = 13
    data["meta"]["languages"] = ["it", "en", "es"]
    return data


def build_html():
    html = v12.HTML
    html = v3._must_replace(
        html,
        "button,input{font:inherit}",
        "button,input,select{font:inherit}.language{width:auto;background:#111827;border:1px solid var(--line);color:var(--text);padding:8px 10px;border-radius:10px}",
        "Wiki v13 stile selettore lingua",
    )
    html = v3._must_replace(
        html,
        '<span class="commit" id="commit"></span></div><main id="app"></main>',
        '<select id="languageSelect" class="language" data-i18n-skip aria-label="Lingua">'
        '<option value="it">🇮🇹 Italiano</option><option value="en">🇬🇧 English</option>'
        '<option value="es">🇪🇸 Español</option></select>'
        '<span class="commit" id="commit"></span></div><main id="app"></main>',
        "Wiki v13 selettore lingua",
    )
    html = v3._must_replace(
        html,
        '<script id="wiki-data" type="application/json">__DATA__</script>',
        '<script src="assets/i18n.js"></script>'
        '<script id="wiki-data" type="application/json">__DATA__</script>',
        "Wiki v13 client i18n",
    )
    html = v3._must_replace(
        html,
        "window.addEventListener('hashchange',render);render();",
        "window.addEventListener('hashchange',render);"
        "NFTI18n.init().then(render).catch(error=>{console.error(error);render()});",
        "Wiki v13 avvio localizzato",
    )
    return html


HTML = build_html()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="_site")
    args = parser.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        out = ROOT / out
    out.mkdir(parents=True, exist_ok=True)
    data = build_data()
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (out / "index.html").write_text(HTML.replace("__DATA__", payload), encoding="utf-8")
    (out / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    assets = ROOT / "wiki" / "assets"
    if assets.exists():
        shutil.copytree(assets, out / "assets", dirs_exist_ok=True)
    (out / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "i18n_web.js", out / "assets" / "i18n.js")
    shutil.copytree(ROOT / "locales", out / "locales", dirs_exist_ok=True)
    print("Wiki v13 generata:", out)
    print(json.dumps(data["meta"]["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

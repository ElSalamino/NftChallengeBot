#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entry point robusto per la wiki navigabile."""
import genera_wiki_v2 as wiki


def set_names_validi():
    nomi = (
        set(getattr(wiki.liste, "classi", {}))
        | set(getattr(wiki.liste, "bonus", {}))
        | set(getattr(wiki.bilanciamento, "PROC_CLASSI", {}))
        | set(wiki.FRASI_SET_TECNICHE)
    )
    return sorted((nome for nome in nomi if isinstance(nome, str) and nome.strip()), key=str.lower)


wiki.set_names = set_names_validi

if __name__ == "__main__":
    wiki.main()

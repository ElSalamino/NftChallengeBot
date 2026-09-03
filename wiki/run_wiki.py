#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entry point della wiki procedurale pubblicata su GitHub Pages."""
import genera_wiki_v7 as wiki

# I generatori successivi riusano raccolte del v2: forza anche lì l'elenco
# dei set già filtrato, così eventuali chiavi storiche None non entrano
# nell'ordinamento del catalogo.
wiki.v3.v2.set_names = wiki.v3._valid_set_names


if __name__ == "__main__":
    wiki.main()

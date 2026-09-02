#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entry point della wiki procedurale pubblicata su GitHub Pages."""
import genera_wiki_v3 as wiki

# Il generatore v3 riusa alcune raccolte del v2: forza anche lì l'elenco
# dei set già filtrato, così eventuali chiavi storiche None non entrano
# nell'ordinamento del catalogo.
wiki.v2.set_names = wiki._valid_set_names


if __name__ == "__main__":
    wiki.main()

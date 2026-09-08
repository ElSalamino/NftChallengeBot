#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Estrae le frasi visibili e prepara i cataloghi IT/EN/ES.

È uno strumento di manutenzione: il gioco non dipende dal traduttore usato per
il bootstrap. Le traduzioni già presenti vengono conservate, così le revisioni
umane non vengono mai sovrascritte da un'esecuzione successiva.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
from collections import Counter
from html import unescape
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCALES = ROOT / "locales"
RUNTIME_FILES = (
    "__init__.py",
    "nft.py",
    "turno_assalto.py",
    "liste.py",
    "bilanciamento.py",
    "frasi_set.py",
    "frasi_anelli.py",
    "frasi_incantesimi.py",
    "frasi_usabili.py",
    "settimanale.py",
    "dungeon_extra.py",
    "playtest_web.py",
)

ITALIAN_HINTS = {
    "a", "ad", "al", "alla", "anche", "che", "chi", "come", "con", "contro",
    "da", "dal", "dalla", "dei", "del", "della", "delle", "di", "dopo", "e",
    "gli", "hai", "il", "in", "la", "le", "lo", "ma", "mentre", "nel", "nella",
    "non", "ogni", "o", "per", "più", "prima", "puoi", "quando", "se", "sei",
    "senza", "sono", "su", "tra", "tu", "tua", "tuo", "un", "una", "uno", "viene",
}
SHORT_UI = {
    "accetta", "aiuto", "annamoo", "attacca", "avanti", "chiudi", "dettagli",
    "fatta", "fatto", "indietro", "inizia", "io", "lingua", "menu", "mio",
    "passo", "pesca", "riprova", "salva", "sfida", "stordisci", "tolto", "unito",
}
PROTECTED_WORDS = (
    "NFT", "NftChallengeBot", "ElSalamino", "Ermenegildo", "ATK", "DEF", "AGI",
    "HP", "DPS", "INT", "PAT", "POWA", "POWE", "LVX", "LVMAX", "LV0",
)

EXPLICIT = {
    "language.choose": {
        "it": "Scegli la lingua. Puoi cambiarla in qualsiasi momento con /lingua.",
        "en": "Choose your language. You can change it at any time with /language.",
        "es": "Elige tu idioma. Puedes cambiarlo en cualquier momento con /idioma.",
    },
    "language.changed": {
        "it": "Lingua impostata su Italiano 🇮🇹",
        "en": "Language set to English 🇬🇧",
        "es": "Idioma configurado en Español 🇪🇸",
    },
    "language.current": {
        "it": "Lingua attuale: {name}",
        "en": "Current language: {name}",
        "es": "Idioma actual: {name}",
    },
    "language.name.it": {"it": "Italiano", "en": "Italian", "es": "Italiano"},
    "language.name.en": {"it": "Inglese", "en": "English", "es": "Inglés"},
    "language.name.es": {"it": "Spagnolo", "en": "Spanish", "es": "Español"},
    "ui.button.language": {"it": "Lingua 🌐", "en": "Language 🌐", "es": "Idioma 🌐"},
    "ui.button.close": {"it": "Chiudi", "en": "Close", "es": "Cerrar"},
    "ui.button.back": {"it": "Indietro", "en": "Back", "es": "Atrás"},
    "ui.button.details": {"it": "Dettagli", "en": "Details", "es": "Detalles"},
    "ui.menu.challenge": {"it": "Sfida ⚔️", "en": "Challenge ⚔️", "es": "Desafío ⚔️"},
    "ui.menu.arena": {"it": "Arena ☠️", "en": "Arena ☠️", "es": "Arena ☠️"},
    "ui.menu.dungeon": {"it": "Dungeon 🏃‍♂️", "en": "Dungeon 🏃‍♂️", "es": "Mazmorra 🏃‍♂️"},
    "ui.menu.assault": {"it": "Assalto 📯", "en": "Assault 📯", "es": "Asalto 📯"},
    "ui.menu.clan": {"it": "Clan 🔱", "en": "Clan 🔱", "es": "Clan 🔱"},
    "ui.menu.boss": {"it": "Boss 👹", "en": "Boss 👹", "es": "Jefe 👹"},
    "ui.menu.move": {"it": "Muoviti 🚩", "en": "Move 🚩", "es": "Muévete 🚩"},
    "ui.menu.sect": {"it": "Setta ©️", "en": "Sect ©️", "es": "Secta ©️"},
    "ui.menu.trader": {"it": "Trafficante 🥷", "en": "Trader 🥷", "es": "Mercader 🥷"},
    "ui.menu.shop": {"it": "Negozio 🛒", "en": "Shop 🛒", "es": "Tienda 🛒"},
    "ui.menu.fisherman": {"it": "Pescatore 🎣", "en": "Fisherman 🎣", "es": "Pescador 🎣"},
    "ui.menu.me": {"it": "Me 👤", "en": "Me 👤", "es": "Yo 👤"},
    "ui.menu.other": {"it": "Altro 🧩", "en": "More 🧩", "es": "Más 🧩"},
    "ui.menu.info": {"it": "Info 🗞", "en": "Info 🗞", "es": "Info 🗞"},
    "ui.menu.close": {"it": "Chiudi🚫", "en": "Close 🚫", "es": "Cerrar 🚫"},
    "ui.menu.fishing": {"it": "Pesca 🎣", "en": "Fishing 🎣", "es": "Pesca 🎣"},
    "ui.menu.questions": {"it": "Domande ❔", "en": "Questions ❔", "es": "Preguntas ❔"},
    "ui.menu.top": {"it": "Top 🔝", "en": "Top 🔝", "es": "Clasificación 🔝"},
    "ui.menu.achievements": {"it": "Obbiettivi 🎖", "en": "Achievements 🎖", "es": "Logros 🎖"},
    "ui.menu.notifications": {"it": "Notifiche 🛎", "en": "Notifications 🛎", "es": "Notificaciones 🛎"},
    "ui.menu.invite": {"it": "Invita 📮", "en": "Invite 📮", "es": "Invitar 📮"},
    "ui.menu.switch": {"it": "Switch 🪖", "en": "Switch 🪖", "es": "Cambiar 🪖"},
    "ui.menu.main": {"it": "menu", "en": "menu", "es": "menú"},
    "ui.keyboard.closed": {"it": "Tastiera chiusa", "en": "Keyboard closed", "es": "Teclado cerrado"},
    "ui.label.name": {"it": "Nome", "en": "Name", "es": "Nombre"},
    "ui.label.approach": {"it": "Approccio", "en": "Approach", "es": "Enfoque"},
    "ui.label.weapon": {"it": "Arma", "en": "Weapon", "es": "Arma"},
    "ui.label.protection": {"it": "Protezione", "en": "Protection", "es": "Protección"},
    "ui.label.ring": {"it": "Anello", "en": "Ring", "es": "Anillo"},
    "ui.label.opponent": {"it": "Avversario", "en": "Opponent", "es": "Oponente"},
    "ui.label.type": {"it": "Tipo", "en": "Type", "es": "Tipo"},
    "ui.label.enemy": {"it": "Nemico", "en": "Enemy", "es": "Enemigo"},
    "ui.label.boss_level": {"it": "Livello boss", "en": "Boss level", "es": "Nivel del jefe"},
    "ui.label.glory": {"it": "Gloria", "en": "Glory", "es": "Gloria"},
    "ui.label.result": {"it": "Risultato", "en": "Result", "es": "Resultado"},
    "ui.label.exploration": {"it": "Esplorazione", "en": "Exploration", "es": "Exploración"},
    "ui.label.location": {"it": "Location", "en": "Location", "es": "Ubicación"},
    "ui.label.set": {"it": "Set", "en": "Set", "es": "Set"},
    "ui.label.last_catch": {"it": "Ultima pesca", "en": "Latest catch", "es": "Última pesca"},
    "ui.label.boss": {"it": "Boss", "en": "Boss", "es": "Jefe"},
    "ui.label.marine_boss": {"it": "Boss marino", "en": "Marine boss", "es": "Jefe marino"},
    "playtest.tab.character": {"it": "🧍 Scheda", "en": "🧍 Character", "es": "🧍 Personaje"},
    "playtest.tab.challenge": {"it": "⚔️ Sfida", "en": "⚔️ Challenge", "es": "⚔️ Desafío"},
    "playtest.tab.dungeon": {"it": "🗝 Dungeon", "en": "🗝 Dungeon", "es": "🗝 Mazmorra"},
    "playtest.tab.fishing": {"it": "🎣 Pesca", "en": "🎣 Fishing", "es": "🎣 Pesca"},
    "playtest.tab.data": {"it": "🧪 Dati", "en": "🧪 Data", "es": "🧪 Datos"},
    "playtest.button.calculate": {"it": "Calcola scheda", "en": "Calculate stats", "es": "Calcular ficha"},
    "playtest.button.save": {"it": "Salva nel browser", "en": "Save in browser", "es": "Guardar en el navegador"},
    "playtest.button.reset": {"it": "Reset", "en": "Reset", "es": "Reiniciar"},
    "playtest.button.start_challenge": {"it": "Inizia sfida", "en": "Start challenge", "es": "Iniciar desafío"},
    "playtest.button.play_turn": {"it": "Gioca 1 turno", "en": "Play 1 turn", "es": "Jugar 1 turno"},
    "playtest.button.auto_finish": {"it": "Auto fino alla fine", "en": "Auto to finish", "es": "Auto hasta el final"},
    "playtest.button.visit_room": {"it": "Visita una stanza", "en": "Visit a room", "es": "Visitar una sala"},
    "playtest.button.podium_1": {"it": "🥇 Sali al 1°", "en": "🥇 Climb to 1st", "es": "🥇 Subir al 1.º"},
    "playtest.button.podium_2": {"it": "🥈 Sali al 2°", "en": "🥈 Climb to 2nd", "es": "🥈 Subir al 2.º"},
    "playtest.button.podium_3": {"it": "🥉 Sali al 3°", "en": "🥉 Climb to 3rd", "es": "🥉 Subir al 3.º"},
    "playtest.button.cast_line": {"it": "Lancia la canna", "en": "Cast the line", "es": "Lanzar la caña"},
    "playtest.subtitle": {
        "it": "Sandbox locale per provare build, sfide, dungeon e pesca sui dati reali del repository.",
        "en": "Local sandbox for testing builds, challenges, dungeons, and fishing with real repository data.",
        "es": "Entorno local para probar configuraciones, desafíos, mazmorras y pesca con los datos reales del repositorio.",
    },
    "playtest.runtime.checking": {"it": "Controllo runtime…", "en": "Checking runtime…", "es": "Comprobando el runtime…"},
    "playtest.label.hp_base": {"it": "HP base", "en": "Base HP", "es": "HP base"},
    "playtest.label.atk_base": {"it": "ATK base", "en": "Base ATK", "es": "ATK base"},
    "playtest.label.def_base": {"it": "DEF base", "en": "Base DEF", "es": "DEF base"},
    "playtest.label.agi_base": {"it": "AGI base", "en": "Base AGI", "es": "AGI base"},
    "playtest.label.enchantments": {"it": "Incantamenti", "en": "Enchantments", "es": "Encantamientos"},
    "playtest.label.comma_separated": {"it": "separati da virgola", "en": "comma-separated", "es": "separados por comas"},
    "playtest.enchantments.example": {
        "it": "es. Critico, Affilatezza", "en": "e.g. Critico, Affilatezza", "es": "p. ej., Critico, Affilatezza",
    },
    "playtest.runtime.notice_start": {
        "it": "Quando il runtime del bot è importabile viene chiamato direttamente",
        "en": "When the bot runtime can be imported, the playtest directly calls",
        "es": "Cuando se puede importar el runtime del bot, el playtest llama directamente a",
    },
    "playtest.runtime.name": {"it": "nft.turno", "en": "nft.turno", "es": "nft.turno"},
    "playtest.runtime.notice_end": {
        "it": ". Se manca una dipendenza Telegram, la UI resta attiva ma usa un fallback indicato chiaramente nel log.",
        "en": ". If a Telegram dependency is missing, the UI remains available and uses a fallback clearly identified in the log.",
        "es": ". Si falta una dependencia de Telegram, la interfaz sigue disponible y usa un modo alternativo claramente indicado en el registro.",
    },
    "playtest.challenge.empty": {"it": "Inizia una sfida.", "en": "Start a challenge.", "es": "Inicia un desafío."},
    "playtest.dungeon.ambush_note": {
        "it": "Ogni visita tira anche la nuova imboscata allo 0,5%; se scatta vengono scelti 2 mostri fuori dalla location.",
        "en": "Each visit also rolls the new 0.5% ambush; if triggered, 2 monsters from outside the location are selected.",
        "es": "Cada visita también comprueba la nueva emboscada del 0,5 %; si se activa, se eligen 2 monstruos ajenos a la ubicación.",
    },
    "playtest.podium.title": {"it": "Podio — test rapido", "en": "Podium — quick test", "es": "Podio — prueba rápida"},
    "playtest.achievements.done": {"it": "Obiettivi completati", "en": "Achievements completed", "es": "Logros completados"},
    "playtest.achievements.total": {"it": "Obiettivi totali", "en": "Total achievements", "es": "Logros totales"},
    "playtest.fishing.power": {"it": "Potere di pesca", "en": "Fishing Power", "es": "Poder de pesca"},
    "playtest.fishing.note": {
        "it": "Questa prima versione usa già il pool reale per location e lo sblocco specie tramite Potere di pesca.",
        "en": "This version already uses each location's real pool and unlocks species through Fishing Power.",
        "es": "Esta versión ya usa el grupo real de cada ubicación y desbloquea especies mediante Poder de pesca.",
    },
    "playtest.fishing.empty": {"it": "Nessun pesce pescato.", "en": "No fish caught.", "es": "Aún no has pescado nada."},
    "playtest.data.title": {"it": "Dati caricati dal gioco", "en": "Data loaded from the game", "es": "Datos cargados del juego"},
    "playtest.data.note": {
        "it": "La web app non mantiene una seconda copia dei cataloghi: legge gli stessi moduli Python e la stessa pipeline dati della Wiki.",
        "en": "The web app does not maintain a second copy of the catalogues: it reads the same Python modules and data pipeline as the Wiki.",
        "es": "La aplicación web no mantiene una segunda copia de los catálogos: lee los mismos módulos de Python y la misma canalización de datos que la Wiki.",
    },
    "playtest.guide.empty": {"it": "Nessuna guida disponibile.", "en": "No guide available.", "es": "No hay ninguna guía disponible."},
    "playtest.raw_score": {"it": "Punteggio raw", "en": "Raw score", "es": "Puntuación raw"},
    "playtest.value.set": {"it": "Set: {0}", "en": "Set: {0}", "es": "Set: {0}"},
    "playtest.value.approach": {"it": "Approccio: {0}", "en": "Approach: {0}", "es": "Enfoque: {0}"},
    "playtest.value.ring": {"it": "Anello: {0}", "en": "Ring: {0}", "es": "Anillo: {0}"},
    "playtest.value.none": {"it": "nessuno", "en": "none", "es": "ninguno"},
    "playtest.value.base": {"it": "Base", "en": "Base", "es": "Base"},
    "playtest.option.choose": {"it": "— scegli —", "en": "— choose —", "es": "— elige —"},
    "playtest.option.none": {"it": "— nessuno —", "en": "— none —", "es": "— ninguno —"},
    "playtest.fighter.player": {"it": "Player", "en": "Player", "es": "Jugador"},
    "playtest.fighter.enemy": {"it": "Enemy", "en": "Enemy", "es": "Enemigo"},
    "playtest.fight.outcome": {"it": "=== {0} ===", "en": "=== {0} ===", "es": "=== {0} ==="},
    "playtest.fight.turn_limit": {
        "it": "STOP: 100 turni raggiunti.", "en": "STOP: 100 turns reached.", "es": "ALTO: se alcanzaron 100 turnos.",
    },
    "playtest.room": {"it": "Stanza", "en": "Room", "es": "Sala"},
    "playtest.room.chance": {
        "it": "Probabilità/check: {0}", "en": "Chance/check: {0}", "es": "Probabilidad/comprobación: {0}",
    },
    "playtest.room.next_enemies": {
        "it": "Prossimi mostri: {0}", "en": "Next monsters: {0}", "es": "Próximos monstruos: {0}",
    },
    "playtest.kpi.equipment": {"it": "Equip", "en": "Equipment", "es": "Equipo"},
    "playtest.kpi.enemies": {"it": "Nemici", "en": "Enemies", "es": "Enemigos"},
    "playtest.kpi.rooms": {"it": "Stanze", "en": "Rooms", "es": "Salas"},
    "playtest.kpi.rings": {"it": "Anelli", "en": "Rings", "es": "Anillos"},
    "playtest.kpi.wiki_items": {"it": "Wiki items", "en": "Wiki items", "es": "Objetos de la Wiki"},
    "playtest.runtime.active": {
        "it": "● Runtime 1:1 nft.turno attivo", "en": "● Exact nft.turno runtime active", "es": "● Runtime exacto nft.turno activo",
    },
    "playtest.runtime.fallback": {
        "it": "● Fallback: runtime Telegram non importato",
        "en": "● Fallback: Telegram runtime not imported",
        "es": "● Modo alternativo: runtime de Telegram no importado",
    },
    "playtest.saved": {"it": "Salvato ✓", "en": "Saved ✓", "es": "Guardado ✓"},
    "playtest.startup_error": {
        "it": "Errore avvio: {0}", "en": "Startup error: {0}", "es": "Error de inicio: {0}",
    },
    "technical.set.details": {
        "it": "⚙️ Dettagli del set", "en": "⚙️ Set details", "es": "⚙️ Detalles del set",
    },
    "technical.ring.details": {
        "it": "⚙️ Dettagli dell'anello", "en": "⚙️ Ring details", "es": "⚙️ Detalles del anillo",
    },
    "technical.spell.details": {
        "it": "⚙️ Dettagli dell'incantesimo", "en": "⚙️ Spell details", "es": "⚙️ Detalles del hechizo",
    },
    "technical.base_bonus": {
        "it": "• Bonus base: {bonus}", "en": "• Base bonus: {bonus}", "es": "• Bonificación base: {bonus}",
    },
    "common.yes": {"it": "sì", "en": "yes", "es": "sí"},
    "common.no": {"it": "no", "en": "no", "es": "no"},
    "time.seconds_remaining": {
        "it": "Mancano {0} secondi!",
        "en": "{0} seconds remaining!",
        "es": "¡Quedan {0} segundos!",
    },
    "time.rooms_remaining": {
        "it": "Mancano {0} stanze!",
        "en": "{0} rooms remaining!",
        "es": "¡Quedan {0} salas!",
    },
    "sets.catalog.title": {
        "it": "🧩 **SET E COMPONENTI**",
        "en": "🧩 **SETS AND COMPONENTS**",
        "es": "🧩 **SETS Y COMPONENTES**",
    },
    "sets.catalog.empty": {
        "it": "• _Nessun componente definito_",
        "en": "• _No components defined_",
        "es": "• _No hay componentes definidos_",
    },
    "dungeon.no_spikes": {
        "it": "No, nessuno spuntone!",
        "en": "No, there are no spikes!",
        "es": "¡No, no hay pinchos!",
    },
    "combat.charged_strike": {
        "it": "**{0} rilascia il colpo caricato e infligge {1} danni a {2} ({3} HP)! ({4} cariche)**",
        "en": "**{0} releases the charged strike and deals {1} damage to {2} ({3} HP)! ({4} charges)**",
        "es": "**{0} libera el golpe cargado e inflige {1} de daño a {2} ({3} HP). ({4} cargas)**",
    },
    "wiki.enemy_pool_weight": {
        "it": "Peso nel pool generico: {0} ({0}%). Le location aggiungono inoltre due copie del proprio pool nemici alla generazione.",
        "en": "Generic pool weight: {0} ({0}%). Locations also add two copies of their own enemy pool to generation.",
        "es": "Peso en el grupo genérico: {0} ({0}%). Cada ubicación también añade dos copias de su propio grupo de enemigos a la generación.",
    },
    "wiki.enemy_pool_weight_distinct": {
        "it": "Peso nel pool generico: {0} ({1}%). Le location aggiungono inoltre due copie del proprio pool nemici alla generazione.",
        "en": "Generic pool weight: {0} ({1}%). Locations also add two copies of their own enemy pool to generation.",
        "es": "Peso en el grupo genérico: {0} ({1}%). Cada ubicación también añade dos copias de su propio grupo de enemigos a la generación.",
    },
    "wiki.enemy_pool_weight_quote": {
        "it": ">Peso nel pool generico: {0} ({0}%). Le location aggiungono inoltre due copie del proprio pool nemici alla generazione.",
        "en": ">Generic pool weight: {0} ({0}%). Locations also add two copies of their own enemy pool to generation.",
        "es": ">Peso en el grupo genérico: {0} ({0}%). Cada ubicación también añade dos copias de su propio grupo de enemigos a la generación.",
    },
    "clan.appoint.help": {
        "it": "-`Nomina` - Scegli chi vuoi siano `Sarto`,`Architetto`, `Sacrificio` e `Gestore` o addirittura `Creatore` del clan!",
        "en": "-`Nomina` — Choose who should be the clan's `Sarto`, `Architetto`, `Sacrificio`, `Gestore`, or even `Creatore`!",
        "es": "-`Nomina` — Elige quién ocupará los roles `Sarto`, `Architetto`, `Sacrificio`, `Gestore` o incluso `Creatore` del clan.",
    },
    "clan.invite.help": {
        "it": "-`Invita` - Invita altri membri nel clan (Solo per il comandante)",
        "en": "-`Invita` — Invite other members to the clan (commander only)",
        "es": "-`Invita` — Invita a otros miembros al clan (solo el comandante)",
    },
    "clan.defense.help": {
        "it": "-`Difesa` - Scruta il villaggio nelle guerre altrui",
        "en": "-`Difesa` — Inspect the village during other clans' wars",
        "es": "-`Difesa` — Inspecciona la aldea durante las guerras de otros clanes",
    },
    "clan.menu.help": {
        "it": "-`Help` - Questo menù",
        "en": "-`Help` — This menu",
        "es": "-`Help` — Este menú",
    },
    "top.allowed_fields": {
        "it": "/top accetta solo `livello`,`zaino`,`oggi`,`sfide`,`win`,`lose`,`boss`,`clan`,`inviti`, `perdenti`,`set`,`obbiettivi` o `gloria`",
        "en": "/top only accepts `livello`, `zaino`, `oggi`, `sfide`, `win`, `lose`, `boss`, `clan`, `inviti`, `perdenti`, `set`, `obbiettivi`, or `gloria`",
        "es": "/top solo acepta `livello`, `zaino`, `oggi`, `sfide`, `win`, `lose`, `boss`, `clan`, `inviti`, `perdenti`, `set`, `obbiettivi` o `gloria`",
    },
    "combat.headbutt.fragment": {
        "it": "tira na testata assurda a",
        "en": "lands an absurd headbutt on",
        "es": "le da un cabezazo absurdo a",
    },
    "combat.boom": {
        "it": "**BOOOOM({0})!**",
        "en": "**BOOOOM ({0})!**",
        "es": "**¡BOOOOM ({0})!**",
    },
    "item.fish_name": {
        "it": "Pesce {0}",
        "en": "Fish {0}",
        "es": "Pez {0}",
    },
    "item.level_short": {
        "it": "{0} - lv {1}",
        "en": "{0} - lv. {1}",
        "es": "{0} - niv. {1}",
    },
    "action.face": {
        "it": "Affronta {0}",
        "en": "Face {0}",
        "es": "Enfréntate a {0}",
    },
    "action.choose": {
        "it": "Scegli {0}",
        "en": "Choose {0}",
        "es": "Elige {0}",
    },
    "item.equipped": {
        "it": "{0} equipaggiato!",
        "en": "{0} equipped!",
        "es": "¡{0} equipado!",
    },
    "playtest.fishing.result": {
        "it": "Indice {0}/{1} sbloccato dal Potere {2}. {3}",
        "en": "Index {0}/{1}, unlocked by Fishing Power {2}. {3}",
        "es": "Índice {0}/{1}, desbloqueado por Poder de pesca {2}. {3}",
    },
    "playtest.podium.won": {
        "it": "VINTO LV{0} ({1}%)",
        "en": "WON LV{0} ({1}%)",
        "es": "GANADO LV{0} ({1}%)",
    },
    "playtest.podium.lost": {
        "it": "Persi {0} Gloria ({1}%)",
        "en": "Lost {0} Glory ({1}%)",
        "es": "Perdiste {0} de Gloria ({1}%)",
    },
    "playtest.fight.victory": {"it": "VITTORIA", "en": "VICTORY", "es": "VICTORIA"},
    "playtest.fight.defeat": {"it": "SCONFITTA", "en": "DEFEAT", "es": "DERROTA"},
    "achievement.micro_fisher": {
        "it": "Pesca un pesce con PesoKg <= 2: nel formato attuale significa un peso inferiore a 3 kg.",
        "en": "Catch a fish with PesoKg <= 2; in the current format, this means a weight below 3 kg.",
        "es": "Pesca un pez con PesoKg <= 2; en el formato actual, significa un peso inferior a 3 kg.",
    },
    "achievement.macro_fisher": {
        "it": "Pesca un pesce con PesoKg >= 52.",
        "en": "Catch a fish with PesoKg >= 52.",
        "es": "Pesca un pez con PesoKg >= 52.",
    },
    "dungeon.pet_quicksand": {
        "it": "Sabbie mobili: serve affetto del pet > 666; poi il tiro deve rientrare nella soglia dello scaglione.",
        "en": "Quicksand: your pet needs affection > 666; then the roll must fall within the tier threshold.",
        "es": "Arenas movedizas: tu mascota necesita afecto > 666; después, la tirada debe entrar en el umbral del nivel.",
    },
    "dungeon.pet_rescue": {
        "it": "Con PAT > 666, nei casi compatibili il pet può salvarti; nel ramo più raro puoi ottenere Uno scaglione nero.",
        "en": "With PAT > 666, your pet can save you in compatible cases; the rarest outcome can grant Uno scaglione nero.",
        "es": "Con PAT > 666, tu mascota puede salvarte en los casos compatibles; el resultado más raro puede otorgar Uno scaglione nero.",
    },
    "dungeon.damage_over_500": {
        "it": "Se il danno è già >500, aggiunge altri 500 senza aumentare il piano.",
        "en": "If the damage is already >500, it adds another 500 without increasing the floor.",
        "es": "Si el daño ya es >500, añade otros 500 sin aumentar el piso.",
    },
    "set.dodge_punishment.technical": {
        "it": "Se il nemico schiva, hai il {turno.punizione_schivata.proc:pct} di punirlo comunque. ASSALTO — HARD COUNTER del Muraglione extra: se scegli il Muraglione come bersaglio, al {assalto.muraglione.proc:pct} aggiungi altre {assalto.muraglione.moltiplicatore_extra} volte il DPS originale al colpo, oltre al colpo normale. PARAMETRI COMPLETI — turno.punizione_schivata.divisore_dps={turno.punizione_schivata.divisore_dps}; turno.punizione_schivata.random_min={turno.punizione_schivata.random_min}; turno.punizione_schivata.random_max={turno.punizione_schivata.random_max}; turno.punizione_schivata.danno_min={turno.punizione_schivata.danno_min}.",
        "en": "If the enemy dodges, you still have a {turno.punizione_schivata.proc:pct} chance to punish them. ASSAULT — HARD COUNTER to Muraglione extra: if you target Muraglione, with a {assalto.muraglione.proc:pct} chance you add {assalto.muraglione.moltiplicatore_extra} times the original DPS to the hit, in addition to the normal hit. FULL PARAMETERS — turno.punizione_schivata.divisore_dps={turno.punizione_schivata.divisore_dps}; turno.punizione_schivata.random_min={turno.punizione_schivata.random_min}; turno.punizione_schivata.random_max={turno.punizione_schivata.random_max}; turno.punizione_schivata.danno_min={turno.punizione_schivata.danno_min}.",
        "es": "Si el enemigo esquiva, aún tienes un {turno.punizione_schivata.proc:pct} de probabilidad de castigarlo. ASALTO — HARD COUNTER de Muraglione extra: si eliges Muraglione como objetivo, con un {assalto.muraglione.proc:pct} añades {assalto.muraglione.moltiplicatore_extra} veces el DPS original al golpe, además del golpe normal. PARÁMETROS COMPLETOS — turno.punizione_schivata.divisore_dps={turno.punizione_schivata.divisore_dps}; turno.punizione_schivata.random_min={turno.punizione_schivata.random_min}; turno.punizione_schivata.random_max={turno.punizione_schivata.random_max}; turno.punizione_schivata.danno_min={turno.punizione_schivata.danno_min}.",
    },
    "dungeon.ambush.message": {
        "it": "Mentre giravi per il dungeon un gruppo di loschi figuri si avvicina, è un imboscata!",
        "en": "While you wander through the dungeon, a group of shady figures approaches: it's an ambush!",
        "es": "Mientras recorres la mazmorra, un grupo de tipos sospechosos se acerca: ¡es una emboscada!",
    },
}


def _is_docstring(node, parents):
    parent = parents.get(node)
    owner = parents.get(parent)
    return (
        isinstance(parent, ast.Expr)
        and isinstance(owner, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and bool(owner.body)
        and owner.body[0] is parent
    )


def _joined_template(node: ast.JoinedStr) -> str:
    chunks = []
    index = 0
    for value in node.values:
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            chunks.append(value.value)
        else:
            chunks.append("{" + str(index) + "}")
            index += 1
    return "".join(chunks)


def _strings_in_expression(node: ast.AST):
    """Estrae stringhe senza duplicare i frammenti interni delle f-string."""
    if isinstance(node, ast.JoinedStr):
        yield _joined_template(node)
        return
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        yield node.value
        return
    for child in ast.iter_child_nodes(node):
        yield from _strings_in_expression(child)


def _visible_call_expressions(call: ast.Call) -> list[ast.AST]:
    """Individua gli argomenti realmente mostrati da Telegram e dalle tastiere."""
    name = getattr(call.func, "attr", None) or getattr(call.func, "id", None)
    keyword = {item.arg: item.value for item in call.keywords if item.arg}
    expressions: list[ast.AST] = []

    positional = {
        "send_message": 1,
        "edit_message_text": 2,
        "reply": 0,
        "reply_text": 0,
        "edit": 0,
        "edit_text": 0,
        "answer": 0,
        "InlineKeyboardButton": 0,
        "ReplyKeyboardMarkup": 0,
    }
    text_keyword = {
        "send_message": "text",
        "edit_message_text": "text",
        "reply": "text",
        "reply_text": "text",
        "edit": "text",
        "edit_text": "text",
        "answer": "text",
        "InlineKeyboardButton": "text",
        "ReplyKeyboardMarkup": "keyboard",
    }
    if name in positional:
        key = text_keyword[name]
        if key in keyword:
            expressions.append(keyword[key])
        elif len(call.args) > positional[name]:
            expressions.append(call.args[positional[name]])

    if name in {"send_photo", "send_document", "reply_photo", "reply_document"}:
        if "caption" in keyword:
            expressions.append(keyword["caption"])
        elif len(call.args) > 2:
            expressions.append(call.args[2])
    return expressions


def _looks_like_code(text: str) -> bool:
    lower = text.lower()
    if text.startswith("^") or text.endswith("$"):
        return True
    if re.search(r"[\w,.#-]+\{[\w-]+:", text):
        return True
    if lower.startswith((
        "http://", "https://", "./", "../", "select ", "with ",
        "text/html", "application/json", "<!doctype",
    )):
        return True
    if "<html" in lower or "function " in lower or "def " in lower:
        return True
    if any(
        token in text
        for token in (
            "=>", ".map(", ".forEach(", "document.", "${", "===", "&&", "||", "</",
            "<div", "<span", "<table", "class=", "onclick=", "location.hash", "JSON.stringify",
            "\\s*", "(?:", "(?P", "`).", "`;", "));", "}));", ":''", "sectionTitle(",
            "}if(", "find(D.", "special+=",
        )
    ):
        return True
    if lower.startswith(("return ", "const ", "let ", "var ", "lambda ")):
        return True
    if re.fullmatch(r"[\w./:@*?=+\-{}\[\]\\]+", text, re.ASCII) and " " not in text:
        return True
    if re.fullmatch(r"(?:mon|tue|wed|thu|fri|sat|sun)(?:,(?:mon|tue|wed|thu|fri|sat|sun))+", lower):
        return True
    if text.count("{") > 14 or text.count("}") > 14:
        return True
    return False


def is_phrase(text: object, protected_terms: set[str] | None = None) -> bool:
    if not isinstance(text, str):
        return False
    text = unescape(text).strip()
    if len(text) < 2 or _looks_like_code(text):
        return False
    if protected_terms and text in protected_terms:
        return False
    words = re.findall(r"[A-Za-zÀ-ÿ']+", re.sub(r"\{[^{}]+\}", " ", text).lower())
    if not words:
        return False
    if "{" in text and "}" in text:
        return len(text) >= 4
    if len(words) == 1:
        return words[0] in SHORT_UI or any(ord(char) > 0xFFFF for char in text)
    return len(text) >= 7 and (
        any(word in ITALIAN_HINTS for word in words)
        or any(char in text for char in ".!?:;,…")
        or any(ord(char) > 0xFFFF for char in text)
    )


def python_phrases(path: Path, protected_terms: set[str]) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    phrases: set[str] = set()
    for call in (node for node in ast.walk(tree) if isinstance(node, ast.Call)):
        for expression in _visible_call_expressions(call):
            for raw in _strings_in_expression(expression):
                for line in raw.splitlines():
                    line = line.strip()
                    if (
                        len(line) >= 2
                        and re.search(r"[A-Za-zÀ-ÿ]", line)
                        and not _looks_like_code(line)
                        and line not in protected_terms
                    ):
                        phrases.add(line)
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            raw = _joined_template(node)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            if isinstance(parents.get(node), ast.JoinedStr) or _is_docstring(node, parents):
                continue
            raw = node.value
        else:
            continue
        for line in raw.splitlines():
            line = line.strip()
            if is_phrase(line, protected_terms):
                phrases.add(line)
    return phrases


class _VisibleHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.values: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.skip += 1
        if not self.skip:
            for key, value in attrs:
                if key in {"alt", "placeholder", "title", "aria-label"} and value:
                    self.values.append(value)

    def handle_endtag(self, tag):
        if tag in {"script", "style"} and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.values.append(data)


JS_QUOTED = re.compile(r"(?P<q>['\"])(?P<body>(?:\\.|(?!\1).)*)(?P=q)", re.DOTALL)
JS_TEMPLATE = re.compile(r"`(?P<body>(?:\\.|[^`])*)`", re.DOTALL)


def _clean_embedded(value: str) -> list[str]:
    value = re.sub(r"<[^>]+>", "\n", value)
    placeholder_index = 0

    def replace_placeholder(match):
        nonlocal placeholder_index
        replacement = "{" + str(placeholder_index) + "}"
        placeholder_index += 1
        return replacement

    value = re.sub(r"\$\{[^{}]*\}", replace_placeholder, value)
    value = value.replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"')
    cleaned = []
    for line in value.splitlines():
        line = unescape(line).strip()
        # I template JavaScript annidati possono lasciare il `>` del tag
        # appena rimosso davanti al testo realmente visibile.
        if line.startswith(">") and len(line) > 1:
            line = line[1:].lstrip()
        field_map: dict[str, str] = {}

        def renumber(match):
            old = match.group(1)
            field_map.setdefault(old, str(len(field_map)))
            return "{" + field_map[old] + "}"

        line = re.sub(r"\{(\d+)\}", renumber, line)
        cleaned.append(line)
    return cleaned


def html_phrases(path: Path, protected_terms: set[str]) -> set[str]:
    source = path.read_text(encoding="utf-8")
    parser = _VisibleHTML()
    parser.feed(source)
    out = set()
    # Quello che HTMLParser trova fuori da script/style è certamente testo UI:
    # includere anche etichette di una sola parola (Nome, Arma, Tipo...).
    for raw in parser.values:
        for line in str(raw).splitlines():
            line = line.strip()
            if (
                len(line) >= 2
                and re.search(r"[A-Za-zÀ-ÿ]", line)
                and not line.lower().startswith(("http://", "https://"))
            ):
                out.add(line)
    candidates = []
    for regex in (JS_QUOTED, JS_TEMPLATE):
        for match in regex.finditer(source):
            candidates.extend(_clean_embedded(match.group("body")))
    for raw in candidates:
        for line in str(raw).splitlines():
            line = line.strip()
            if is_phrase(line, protected_terms):
                out.add(line)
    return out


def json_phrases(path: Path, protected_terms: set[str]) -> set[str]:
    with path.open(encoding="utf-8") as stream:
        root = json.load(stream)
    out: set[str] = set()

    def walk(value):
        if isinstance(value, dict):
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
        elif isinstance(value, str):
            for line in value.splitlines():
                line = line.strip()
                if is_phrase(line, protected_terms):
                    out.add(line)

    walk(root)
    return out


def gameplay_terms() -> set[str]:
    sys.path.insert(0, str(ROOT))
    import liste

    names: set[str] = set(PROTECTED_WORDS)
    dict_names = (
        "spec", "hps", "descri", "libri", "starmi", "shop", "Nautici", "Boss",
        "casa_nemici", "classi", "decoro", "pool", "move", "anelli", "usabili",
        "eventi", "nemici", "frasi_set", "premi_boss", "armi", "protezioni",
        "armiextra", "protezioniextra",
    )
    list_names = (
        "order", "strutture", "location", "anellic", "animaletti", "nuclei", "pesci",
        "ingredienti", "spceciali", "bloccati", "usabilitutti",
    )
    for attr in dict_names:
        value = getattr(liste, attr, {})
        if isinstance(value, dict):
            names.update(str(key) for key in value if isinstance(key, str))
    for attr in list_names:
        value = getattr(liste, attr, [])
        if isinstance(value, (list, tuple, set)):
            names.update(str(item) for item in value if isinstance(item, str))
    return names


def collect_phrases(wiki_dir: Path | None = None) -> tuple[set[str], set[str]]:
    protected = gameplay_terms()
    phrases: set[str] = set()
    for relative in RUNTIME_FILES:
        phrases.update(python_phrases(ROOT / relative, protected))
    for path in sorted((ROOT / "wiki").glob("genera_wiki_v*.py")):
        phrases.update(python_phrases(path, protected))
    phrases.update(html_phrases(ROOT / "playtest" / "index.html", protected))
    if wiki_dir:
        html = wiki_dir / "index.html"
        data = wiki_dir / "data.json"
        if html.exists():
            phrases.update(html_phrases(html, protected))
        if data.exists():
            phrases.update(json_phrases(data, protected))
    phrases.update(values["it"] for values in EXPLICIT.values())
    return phrases, protected


PROTECTED_LITERAL_RE = re.compile(
    r"https?://\S+|/[A-Za-z][\w@-]*|"
    r"(?:turno|assalto|combattimento|sfida|dungeon|boss|arena|generale|sistema)\.[\w.]+|"
    r"<=|>=|(?<!\w)[<>](?=\s*\d)|ʕ[^ʔ\n]{0,20}ʔ|"
    r"`[^`\n]+`|\*{1,3}|_{1,3}|~{2}|`+|"
    r"([A-Za-z])\1{5,}|"
    r"[\U0001F000-\U0001FAFF\u2190-\u2BFF\uFE0F\u200D┬─ノ゜]+"
)
FORMAT_PLACEHOLDER_RE = re.compile(r"\{[^{}]+\}")
STABLE_PRESENTATION_RE = re.compile(
    r"https?://\S+|`[^`\n]+`|"
    r"(?:turno|assalto|combattimento|sfida|dungeon|boss|arena|generale|sistema)\.[\w.]+|<=|>="
)
SUSPICIOUS_MODEL_MARKERS = ("ZXQHOLD", "⁇", "♪", "√")


def translation_is_safe(source: str, target: str) -> bool:
    if Counter(FORMAT_PLACEHOLDER_RE.findall(source)) != Counter(
        FORMAT_PLACEHOLDER_RE.findall(target)
    ):
        return False
    if len(target) > max(320, int(len(source) * 2.7)):
        return False
    if Counter(STABLE_PRESENTATION_RE.findall(source)) != Counter(
        STABLE_PRESENTATION_RE.findall(target)
    ):
        return False
    if any(source.count(token) != target.count(token) for token in ("**", "__", "`")):
        return False
    if any(marker in target and marker not in source for marker in SUSPICIOUS_MODEL_MARKERS):
        return False
    for match in re.finditer(r"([^\w\s])\1{7,}", target):
        if match.group(0) not in source:
            return False
    return True


class OfflineTranslator:
    def __init__(self, root: Path, inter_threads: int = 2, intra_threads: int = 4):
        try:
            import ctranslate2
            import sentencepiece as spm
        except ImportError as exc:
            raise SystemExit("Installa ctranslate2 e sentencepiece nel PYTHONPATH per il bootstrap") from exc
        self.sp = spm.SentencePieceProcessor(model_file=str(root / "sentencepiece.model"))
        self.engine = ctranslate2.Translator(
            str(root / "model"), device="cpu", inter_threads=inter_threads, intra_threads=intra_threads
        )

    def batch(self, values: list[str]) -> list[str]:
        tokenized = [self.sp.encode(value, out_type=str) for value in values]
        results = self.engine.translate_batch(tokenized, beam_size=1, max_batch_size=64)
        return [self.sp.decode(result.hypotheses[0]).strip() for result in results]


def _term_pattern(terms: set[str]):
    useful = [term for term in terms if len(term) >= 3]
    return re.compile("|".join(re.escape(term) for term in sorted(useful, key=len, reverse=True)))


def _protect(text: str, term_re) -> tuple[str, dict[str, str]]:
    stored: dict[str, str] = {}

    def hold(value: str) -> str:
        # Le parentesi graffe vengono copiate fedelmente dai modelli Argos.
        token = "{ZXQHOLD" + str(len(stored)) + "}"
        stored[token] = value
        return token

    # I placeholder applicativi sono opachi: non vanno mai tradotti (anche se
    # contengono parole italiane, ad esempio {assalto.turno}).
    text = FORMAT_PLACEHOLDER_RE.sub(lambda match: hold(match.group(0)), text)
    text = PROTECTED_LITERAL_RE.sub(lambda match: hold(match.group(0)), text)
    text = term_re.sub(lambda match: hold(match.group(0)), text)
    return text, stored


def _restore(text: str, stored: dict[str, str]) -> str:
    for token, value in stored.items():
        text = text.replace(token, value)
    return text


def translate_many(values: list[str], translator: OfflineTranslator, terms: set[str]) -> list[str]:
    term_re = _term_pattern(terms)
    protected_values = []
    stores = []
    for value in values:
        safe, stored = _protect(value, term_re)
        protected_values.append(safe)
        stores.append(stored)

    # I vecchi modelli Argos hanno una finestra corta. Spezzare i testi lunghi
    # evita che l'ultima frase (e i relativi placeholder) venga troncata.
    batches: list[str] = []
    spans: list[tuple[int, int]] = []
    for value in protected_values:
        chunks = _model_chunks(value)
        start = len(batches)
        batches.extend(chunks)
        spans.append((start, len(batches)))
    translated_chunks = translator.batch(batches)
    translated = [" ".join(translated_chunks[start:end]).strip() for start, end in spans]

    # Se il modello ha omesso o duplicato un parametro, traduce separatamente
    # i soli frammenti letterali e ricompone i placeholder nell'ordine esatto.
    broken = [
        index
        for index, (source, target) in enumerate(zip(protected_values, translated))
        if (
            Counter(FORMAT_PLACEHOLDER_RE.findall(source))
            != Counter(FORMAT_PLACEHOLDER_RE.findall(target))
            or len(target) > max(320, int(len(source) * 2.7))
        )
    ]
    for index in broken:
        pieces = FORMAT_PLACEHOLDER_RE.split(protected_values[index])
        placeholders = FORMAT_PLACEHOLDER_RE.findall(protected_values[index])
        literal_parts = [piece for piece in pieces if piece.strip()]
        translated_pieces = translator.batch([piece.strip() for piece in literal_parts])
        translated_iter = iter(translated_pieces)
        rebuilt = []
        for piece_index, piece in enumerate(pieces):
            if piece.strip():
                leading = piece[: len(piece) - len(piece.lstrip())]
                trailing = piece[len(piece.rstrip()):]
                rebuilt.append(leading + next(translated_iter) + trailing)
            else:
                rebuilt.append(piece)
            if piece_index < len(placeholders):
                rebuilt.append(placeholders[piece_index])
        translated[index] = "".join(rebuilt).strip()

    # Ultima rete di sicurezza: una rara degenerazione del modello non deve
    # produrre centinaia di simboli ripetuti. In quel caso resta il fallback
    # italiano, esplicitamente supportato dal runtime.
    for index, (source, target) in enumerate(zip(protected_values, translated)):
        placeholders_ok = Counter(FORMAT_PLACEHOLDER_RE.findall(source)) == Counter(
            FORMAT_PLACEHOLDER_RE.findall(target)
        )
        if not placeholders_ok or len(target) > max(320, int(len(source) * 2.7)):
            translated[index] = source

    restored = []
    for source, target, stored in zip(values, translated, stores):
        target = _restore(target, stored)
        if not translation_is_safe(source, target):
            target = source
        restored.append(target)
    return restored


def _model_chunks(text: str, limit: int = 240) -> list[str]:
    sentences = re.split(r"(?<=[.!?;:])\s+", text.strip())
    chunks: list[str] = []
    for sentence in sentences:
        sentence = sentence.strip()
        while len(sentence) > limit:
            cut = max(sentence.rfind(mark, 0, limit) for mark in (", ", " "))
            if cut < limit // 2:
                cut = limit
            # Mai spezzare una chiave {placeholder} a metà.
            if sentence.rfind("{", 0, cut) > sentence.rfind("}", 0, cut):
                closing = sentence.find("}", cut)
                if closing >= 0:
                    cut = closing + 1
            chunks.append(sentence[:cut].strip())
            sentence = sentence[cut:].strip()
        if sentence:
            chunks.append(sentence)
    return chunks or [text]


def auto_key(source: str) -> str:
    return "auto." + hashlib.sha256(source.encode("utf-8")).hexdigest()[:20]


def apply_glossary(text: str, language: str) -> str:
    """Uniforma la terminologia di gioco che i modelli piccoli tendono a lasciare in italiano."""
    replacements = {
        "en": {
            "PARAMETRI COMPLETI": "FULL PARAMETERS",
            "COMBATTIMENTO": "COMBAT",
            "ASSALTO": "ASSAULT",
            "Assalto": "Assault",
        },
        "es": {
            "PARAMETRI COMPLETI": "PARÁMETROS COMPLETOS",
            "COMBATTIMENTO": "COMBATE",
            "ASSALTO": "ASALTO",
            "Assalto": "Asalto",
        },
    }
    for source, target in replacements.get(language, {}).items():
        text = re.sub(rf"(?<!\w){re.escape(source)}(?!\w)", target, text)
    return text


def read_existing(language: str) -> dict[str, str]:
    path = LOCALES / f"{language}.json"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as stream:
        return {key: value for key, value in json.load(stream).items() if not key.startswith("_")}


def write_catalog(language: str, values: dict[str, str]) -> None:
    LOCALES.mkdir(parents=True, exist_ok=True)
    payload = {
        "_meta": {
            "language": language,
            "fallback": "it",
            "generated": "bootstrap + human review",
        },
        **dict(sorted(values.items())),
    }
    with (LOCALES / f"{language}.json").open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki-dir", type=Path)
    parser.add_argument("--it-en-model", type=Path, required=True)
    parser.add_argument("--en-es-model", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    phrases, protected = collect_phrases(args.wiki_dir)
    explicit_sources = {values["it"] for values in EXPLICIT.values()}
    sources = sorted(phrases - explicit_sources, key=lambda value: (value.casefold(), value))
    valid_keys = set(EXPLICIT) | {auto_key(source) for source in sources}

    catalogs = {language: read_existing(language) for language in ("it", "en", "es")}
    for language in catalogs:
        catalogs[language] = {
            key: value for key, value in catalogs[language].items() if key in valid_keys
        }
    for key, translations in EXPLICIT.items():
        for language in catalogs:
            catalogs[language][key] = translations[language]

    pending = []
    for source in sources:
        key = auto_key(source)
        catalogs["it"][key] = source
        if args.force or key not in catalogs["en"] or key not in catalogs["es"]:
            pending.append((key, source))

    if pending:
        it_en = OfflineTranslator(args.it_en_model)
        en_values = translate_many([source for _, source in pending], it_en, protected)
        en_es = OfflineTranslator(args.en_es_model)
        es_values = translate_many(en_values, en_es, protected)
        for (key, _), english, spanish in zip(pending, en_values, es_values):
            catalogs["en"][key] = apply_glossary(english, "en")
            catalogs["es"][key] = apply_glossary(spanish, "es")

    for language in ("en", "es"):
        for key in valid_keys:
            source = catalogs["it"][key]
            target = catalogs[language].get(key, source)
            if not translation_is_safe(source, target):
                catalogs[language][key] = source

    for language in ("it", "en", "es"):
        write_catalog(language, catalogs[language])
    print(f"Cataloghi generati: {len(valid_keys)} chiavi; {len(pending)} traduzioni nuove")


if __name__ == "__main__":
    main()

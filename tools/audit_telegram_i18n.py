#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke test dell'adattatore locale Pyrogram (richiede requirements-playtest)."""
from types import SimpleNamespace

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from telegram_i18n import (
    bind_players,
    language_for_recipient,
    language_from_update,
    localize_markup,
    normalize_update_input,
)


players = {
    "alice": {"id": 123, "lang": "en"},
    "bea": {"id": 456, "lang": "es"},
}
bind_players(lambda: players)

for username, shown, expected in (
    ("alice", "Language 🌐", "Lingua 🌐"),
    ("bea", "Idioma 🌐", "Lingua 🌐"),
):
    message = SimpleNamespace(
        from_user=SimpleNamespace(username=username, language_code="it"),
        text=shown,
    )
    assert language_from_update(message) == players[username]["lang"]
    normalize_update_input(message)
    assert message.text == expected

assert language_for_recipient(123) == "en"
players["alice"]["lang"] = "es"
assert language_for_recipient(123) == "es"  # la cache conserva l'identità, non la lingua

inline = InlineKeyboardMarkup([[InlineKeyboardButton("Chiudi", callback_data="close")]])
reply = ReplyKeyboardMarkup([["Lingua 🌐", "Indietro"]])
english = localize_markup(inline, "en")
spanish = localize_markup(reply, "es")

assert english.inline_keyboard[0][0].text == "Close"
assert english.inline_keyboard[0][0].callback_data == "close"
assert spanish.keyboard[0] == ["Idioma 🌐", "Atrás"]
assert inline.inline_keyboard[0][0].text == "Chiudi"  # la tastiera sorgente non viene mutata

print("Telegram i18n OK: profili, pulsanti e callback stabili")

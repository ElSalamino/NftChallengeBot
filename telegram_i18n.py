# -*- coding: utf-8 -*-
"""Adattatore Pyrogram che localizza messaggi e pulsanti in uscita."""
from __future__ import annotations

import contextvars
import copy
from collections.abc import Callable, Mapping

from i18n import DEFAULT_LANGUAGE, normalize_input, normalize_language, translate_text

try:
    from pyrogram import Client
except ImportError:  # La Wiki può importare i moduli senza dipendenze Telegram.
    Client = object  # type: ignore[assignment,misc]


_current_language = contextvars.ContextVar("nft_language", default=DEFAULT_LANGUAGE)
_players_provider: Callable[[], Mapping[str, object]] = lambda: {}
_recipient_users: dict[str, str] = {}


def bind_players(provider: Callable[[], Mapping[str, object]]) -> None:
    global _players_provider
    _players_provider = provider
    _recipient_users.clear()


def language_from_update(update, persist: bool = True) -> str:
    user = getattr(update, "from_user", None)
    if user is None and getattr(update, "message", None) is not None:
        user = getattr(update.message, "from_user", None)
    username = getattr(user, "username", None)
    user_id = getattr(user, "id", None)
    telegram_language = getattr(user, "language_code", None)
    players = _players_provider() or {}
    record = players.get(username) if username else None
    if isinstance(record, dict):
        language = normalize_language(record.get("lang") or telegram_language)
        if persist:
            record.setdefault("lang", language)
        if username:
            _recipient_users[str(username)] = username
            _recipient_users["@" + str(username)] = username
        if user_id is not None and username:
            _recipient_users[str(user_id)] = username
    else:
        language = normalize_language(telegram_language)
    _current_language.set(language)
    return language


def set_current_language(language: str) -> str:
    language = normalize_language(language)
    _current_language.set(language)
    return language


def current_language() -> str:
    return normalize_language(_current_language.get())


def language_for_recipient(recipient) -> str:
    players = _players_provider() or {}
    recipient_text = str(recipient or "")
    direct_username = recipient_text.lstrip("@")
    direct = players.get(direct_username)
    if isinstance(direct, dict):
        _recipient_users[recipient_text] = direct_username
        return normalize_language(direct.get("lang"))
    cached_username = _recipient_users.get(recipient_text)
    cached = players.get(cached_username) if cached_username else None
    if isinstance(cached, dict):
        return normalize_language(cached.get("lang"))
    for username, raw in players.items():
        if not isinstance(raw, dict):
            continue
        if recipient_text == str(username) or recipient_text == str(raw.get("id", "")):
            _recipient_users[recipient_text] = str(username)
            return normalize_language(raw.get("lang"))
    return current_language()


def normalize_update_input(update) -> str:
    language = language_from_update(update)
    target = getattr(update, "message", None) or update
    text = getattr(target, "text", None)
    normalized = normalize_input(text, language)
    if isinstance(text, str) and normalized != text:
        try:
            target.text = normalized
        except (AttributeError, TypeError):
            pass
    return language


def localize_markup(markup, language: str):
    if markup is None:
        return None
    try:
        localized = copy.deepcopy(markup)
    except Exception:
        localized = markup
    rows = getattr(localized, "inline_keyboard", None)
    if rows is None:
        rows = getattr(localized, "keyboard", None)
    if rows is None:
        return localized
    for row_index, row in enumerate(rows):
        for column_index, button in enumerate(row):
            if isinstance(button, str):
                row[column_index] = translate_text(button, language)
                continue
            if hasattr(button, "text"):
                try:
                    button.text = translate_text(button.text, language)
                except (AttributeError, TypeError):
                    pass
    return localized


class LocalizedClient(Client):
    """Client compatibile con Pyrogram che traduce soltanto la presentazione."""

    async def send_message(self, chat_id, text, *args, **kwargs):
        language = language_for_recipient(chat_id)
        kwargs["reply_markup"] = localize_markup(kwargs.get("reply_markup"), language)
        return await super().send_message(chat_id, translate_text(text, language), *args, **kwargs)

    async def edit_message_text(self, chat_id, message_id, text, *args, **kwargs):
        language = language_for_recipient(chat_id)
        kwargs["reply_markup"] = localize_markup(kwargs.get("reply_markup"), language)
        return await super().edit_message_text(
            chat_id, message_id, translate_text(text, language), *args, **kwargs
        )

    async def send_photo(self, chat_id, photo, *args, **kwargs):
        language = language_for_recipient(chat_id)
        if kwargs.get("caption") is not None:
            kwargs["caption"] = translate_text(kwargs["caption"], language)
        kwargs["reply_markup"] = localize_markup(kwargs.get("reply_markup"), language)
        return await super().send_photo(chat_id, photo, *args, **kwargs)

    async def send_document(self, chat_id, document, *args, **kwargs):
        language = language_for_recipient(chat_id)
        if kwargs.get("caption") is not None:
            kwargs["caption"] = translate_text(kwargs["caption"], language)
        kwargs["reply_markup"] = localize_markup(kwargs.get("reply_markup"), language)
        return await super().send_document(chat_id, document, *args, **kwargs)

    async def answer_callback_query(self, callback_query_id, text=None, *args, **kwargs):
        localized = translate_text(text, current_language()) if text is not None else None
        return await super().answer_callback_query(callback_query_id, localized, *args, **kwargs)

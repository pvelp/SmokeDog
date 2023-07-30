from typing import List

from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)


def create_buttons(text: list):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
    buttons = []
    for i in range(len(text)):
        btn = KeyboardButton(text[i])
        buttons.append(btn)
    kb.add(*buttons)
    return kb


def create_inline_buttons(text: list, callback: List[str] = None):
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []
    for i in range(len(text)):
        btn = InlineKeyboardButton(text[i], callback_data=text[i] if callback is None else callback[i])
        buttons.append(btn)
    kb.add(*buttons)
    return kb

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class CancelBtnName:
    cancel_btn = "Отменить"
    miss = "Пропустить"


def cancel():
    kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    btn = KeyboardButton(CancelBtnName.cancel_btn)
    kb.add(btn)
    return kb


def cancel_send_phone():
    kb = cancel()
    btn = KeyboardButton("Поделиться номером", request_contact=True)
    kb.add(btn)
    return kb


def cancel_or_miss():
    kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    btn = KeyboardButton(CancelBtnName.miss)
    kb.add(btn)
    btn = KeyboardButton(CancelBtnName.cancel_btn)
    kb.add(btn)
    return kb


back_btn = "⬅️Назад"

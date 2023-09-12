import os

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from loguru import logger

from bot.config import bot
from bot.core.keyboards.admin_keyboards.admin_keyboard import (
    MainAdminMenuBtnName,
    main_admin_kb,
)
from bot.core.keyboards.cancel_keyboard import CancelBtnName, cancel_or_miss, cancel
from bot.core.states.admin_state import AdminState
from bot.core.utils import get_clients_id


async def main_admin_menu(message: types.Message):
    msg = message.text

    if msg == MainAdminMenuBtnName.events:
        await message.answer("Events", reply_markup=main_admin_kb())
    elif msg == MainAdminMenuBtnName.mailing:
        await message.answer(
            "*Шаг [1/2]*\nВведите ваше сообщение",
            reply_markup=cancel_or_miss(),
            parse_mode="Markdown",
        )
        await AdminState.enter_message.set()
    elif msg == MainAdminMenuBtnName.database:
        await message.answer("DB", reply_markup=main_admin_kb())
    elif msg == MainAdminMenuBtnName.personal:
        await message.answer("Personal", reply_markup=main_admin_kb())


async def enter_message(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили ввод сообщения", reply_markup=main_admin_kb())
        await state.reset_state()
        await AdminState.start.set()
    elif msg == CancelBtnName.miss:
        await message.answer(
            "*Шаг [2/2]*\nОтправьте фотографию, если это необходимо",
            reply_markup=cancel(),
            parse_mode="Markdown",
        )
        await AdminState.enter_photo.set()
    else:
        await state.update_data(text=msg)
        await message.answer(
            "*Шаг [2/2]*\nОтправьте фотографию, если это необходимо",
            reply_markup=cancel(),
            parse_mode="Markdown",
        )
        await AdminState.enter_photo.set()


async def enter_photo(message: types.Message, state: FSMContext):
    dest = f"pictures/mailing/{message.chat.id}.jpeg"
    await message.photo[-1].download(dest)
    await state.update_data(photo=dest)
    clients_id = get_clients_id()
    data = await state.get_data()
    msg = ""
    try:
        msg = data["text"]
    except Exception as e:
        logger.error(e)

    for id_ in clients_id:
        try:
            await bot.send_photo(chat_id=id_, photo=types.InputFile(dest), caption=msg)
        except Exception as e:
            logger.error(e)
    await message.answer("Ваше сообщение отправлено", reply_markup=main_admin_kb())
    await AdminState.start.set()
    try:
        os.remove(dest)
    except Exception as e:
        logger.error(e)


async def cancel_enter_photo(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer(
            "Вы отменили создание сообщения", reply_markup=main_admin_kb()
        )
        await state.reset_state()
        await AdminState.start.set()


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(main_admin_menu, state=AdminState.start)
    dp.register_message_handler(cancel_enter_photo, state=AdminState.enter_photo)
    dp.register_message_handler(
        enter_photo, state=AdminState.enter_photo, content_types=["photo"]
    )
    dp.register_message_handler(enter_message, state=AdminState.enter_message)

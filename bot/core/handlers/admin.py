import os

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from loguru import logger

from bot.config import bot
from bot.core.db.client_actions import (
    set_is_banned,
    get_client_by_tg_id,
    delete_user_by_tg_id,
)
from bot.core.keyboards.admin_keyboards.admin_keyboard import (
    MainAdminMenuBtnName,
    main_admin_kb,
    DataBaseMenuBtnName,
    database_kb,
)
from bot.core.keyboards.cancel_keyboard import (
    CancelBtnName,
    cancel_or_miss,
    cancel,
    back_btn,
)
from bot.core.states.admin_state import AdminState
from bot.core.utils import get_clients_id, get_excel_from_db


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
        await message.answer(
            "Меню управлением базой клиентов", reply_markup=database_kb()
        )
        await AdminState.database.set()
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
            reply_markup=cancel_or_miss(),
            parse_mode="Markdown",
        )
        await AdminState.enter_photo.set()


async def enter_photo(message: types.Message, state: FSMContext):
    dest = f"sources/mailing/{message.chat.id}.jpeg"
    await message.photo[-1].download(dest)
    await state.update_data(photo=dest)
    data = await state.get_data()
    msg = ""
    try:
        msg = data["text"]
    except Exception as e:
        logger.error(e)

    clients_id = get_clients_id()
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
    elif msg == CancelBtnName.miss:
        clients_id = get_clients_id()
        data = state.get_data()
        msg = ""

        try:
            msg = data["text"]
        except Exception as e:
            logger.error(e)

        if len(msg) != 0:
            for id_ in clients_id:
                try:
                    await bot.send_message(chat_id=id_, text=msg)
                except Exception as e:
                    logger.error(e)

        await message.answer("Ваше сообщение отправлено", reply_markup=main_admin_kb())
        await AdminState.start.set()
        await state.reset_state()


async def database_menu(message: types.Message):
    msg = message.text
    if msg == back_btn:
        await message.answer(
            "Вы вернулись в главное меню", reply_markup=main_admin_kb()
        )
    elif msg == DataBaseMenuBtnName.get_db:
        get_excel_from_db("users")
        await bot.send_document(
            chat_id=message.from_user.id, document=types.InputFile("users.xlsx")
        )
        os.remove("users.xlsx")
    elif msg == DataBaseMenuBtnName.ban_client:
        await message.answer(
            "Введите id клиента, которого необходимо заблокировать", cancel()
        )
        await AdminState.ban.set()
    elif msg == DataBaseMenuBtnName.delete_client:
        await message.answer("Введите id клиента, которого необходимо удалить", cancel())
        await AdminState.delete_user.set()


async def enter_id_for_banning(message: types.Message):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer(
            "Вы отменили ввод id пользователя для блокировки",
            reply_markup=main_admin_kb(),
        )
    else:
        set_is_banned(msg)
        client = get_client_by_tg_id(telegram_id=msg)
        new_msg = (
            f"Вы заблокировали пользователя с данными\n\nId: {client.telegram_id}\nИмя: "
            f"{client.name}\nЮзернейм: {client.username}\nТелефон:"
            f" {client.phone}\nСтатус блокировки: {client.is_banned}"
        )
        await message.answer(new_msg, reply_markup=main_admin_kb())
    await AdminState.start.set()


async def enter_id_for_delete_user(message: types.Message):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer(
            "Вы отменили ввод id пользователя для удаления",
            reply_markup=main_admin_kb(),
        )
    else:
        client = get_client_by_tg_id(telegram_id=msg)
        new_msg = (
            f"Вы удалили пользователя с данными\n\nId: {client.telegram_id}\nИмя: "
            f"{client.name}\nЮзернейм: {client.username}\nТелефон:"
            f" {client.phone}\nСтатус блокировки: {client.is_banned}"
        )
        delete_user_by_tg_id(msg)
        await message.answer(new_msg, reply_markup=main_admin_kb())
    await AdminState.start.set()


async def answer_on_report(callback: types.CallbackQuery):
    pass


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(main_admin_menu, state=AdminState.start)
    dp.register_message_handler(cancel_enter_photo, state=AdminState.enter_photo)
    dp.register_message_handler(
        enter_photo, state=AdminState.enter_photo, content_types=["photo"]
    )
    dp.register_message_handler(enter_message, state=AdminState.enter_message)
    dp.register_message_handler(database_menu, state=AdminState.database)
    dp.register_message_handler(enter_id_for_banning, state=AdminState.ban)

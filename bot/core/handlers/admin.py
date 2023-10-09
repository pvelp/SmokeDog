import os

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from loguru import logger

from bot.config import bot, storage
from bot.core.consts import MAX_EVENTS
from bot.core.db.admin_actions import add_admin, delete_admin, get_admin_by_id
from bot.core.db.client_actions import (
    set_is_banned,
    get_client_by_tg_id,
    delete_user_by_tg_id,
)
from bot.core.db.event_actions import add_event, delete_event_by_date, get_events, get_event_by_date
from bot.core.keyboards.admin_keyboards.admin_keyboard import (
    MainAdminMenuBtnName,
    main_admin_kb,
    DataBaseMenuBtnName,
    database_kb,
    AdminDatabaseMenuBtnName,
    weekend_kb,
    personal_kb, event_kb, EventBtnName,
)
from bot.core.keyboards.cancel_keyboard import (
    CancelBtnName,
    cancel_or_miss,
    cancel,
    back_btn,
)
from bot.core.keyboards.user_keyboards.user_keyboard import main_menu_kb, choose_date_kb
from bot.core.states.admin_state import AdminState
from bot.core.states.user_state import UserState
from bot.core.utils import get_clients_id, get_excel_from_db, get_admins_id


async def main_admin_menu(message: types.Message):
    msg = message.text
    if msg == MainAdminMenuBtnName.events:
        await message.answer("Вы вошли в меню управления афишами", reply_markup=event_kb())
        await AdminState.choose_event_date.set()
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
        await message.answer("Вы вошли в меню управления персоналом", reply_markup=personal_kb())
        # await message.answer(
        #     "Меню управления персоналом скоро заработает!", reply_markup=main_admin_kb()
        # )
        await AdminState.personal.set()


async def enter_message(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили ввод сообщения", reply_markup=main_admin_kb())
        await state.reset_data()
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
        await state.reset_data()
        await AdminState.start.set()
    elif msg == CancelBtnName.miss:
        clients_id = get_clients_id()
        data = await state.get_data()
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
        await state.reset_data()


async def database_menu(message: types.Message):
    msg = message.text
    if msg == back_btn:
        await message.answer(
            "Вы вернулись в главное меню", reply_markup=main_admin_kb()
        )
        await AdminState.start.set()
    elif msg == DataBaseMenuBtnName.get_db:
        get_excel_from_db("users")
        await bot.send_document(
            chat_id=message.from_user.id, document=types.InputFile("users.xlsx")
        )
        os.remove("users.xlsx")
    elif msg == DataBaseMenuBtnName.ban_client:
        await message.answer(
            "Введите id клиента, которого необходимо заблокировать", reply_markup=cancel()
        )
        await AdminState.ban.set()
    elif msg == DataBaseMenuBtnName.delete_client:
        await message.answer(
            "Введите id клиента, которого необходимо удалить", reply_markup=cancel()
        )
        await AdminState.delete_user.set()


async def enter_id_for_banning(message: types.Message):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer(
            "Вы отменили ввод id пользователя для блокировки",
            reply_markup=database_kb(),
        )
    else:
        set_is_banned(msg)
        client = get_client_by_tg_id(telegram_id=msg)
        new_msg = (
            f"Вы заблокировали пользователя с данными\n\nId: {client.telegram_id}\nИмя: "
            f"{client.name}\nЮзернейм: {client.username}\nТелефон:"
            f" {client.phone}\nСтатус блокировки: {client.is_banned}"
        )
        await message.answer(new_msg, reply_markup=database_kb())
    await AdminState.database.set()


async def enter_id_for_delete_user(message: types.Message):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer(
            "Вы отменили ввод id пользователя для удаления",
            reply_markup=database_kb(),
        )
    else:
        client = get_client_by_tg_id(telegram_id=msg)
        new_msg = (
            f"Вы удалили пользователя с данными\n\nId: {client.telegram_id}\nИмя: "
            f"{client.name}\nЮзернейм: {client.username}\nТелефон:"
            f" {client.phone}\nСтатус блокировки: {client.is_banned}"
        )
        delete_user_by_tg_id(msg)
        await message.answer(new_msg, reply_markup=database_kb())
    await AdminState.database.set()


async def personal_menu(message: types.Message):
    msg = message.text
    if msg == back_btn:
        await message.answer("Вы вернулись в главное меню", reply_markup=main_admin_kb())
        await AdminState.start.set()
    elif msg == AdminDatabaseMenuBtnName.get_admins:
        get_excel_from_db("admins")
        await bot.send_document(
            chat_id=message.from_user.id, document=types.InputFile("admins.xlsx")
        )
        os.remove("admins.xlsx")
    elif msg == AdminDatabaseMenuBtnName.add_admin:
        await message.answer("Введите Id и имя человека, которого нужно назначить админом в формате:"
                             "\nID:ИМЯ\n\nПример:\n12345678:Иван",
                             reply_markup=cancel())
        await AdminState.enter_admin_id.set()
    elif msg == AdminDatabaseMenuBtnName.delete_admin:
        await message.answer("Введите Id админа, которого нужно удалить", reply_markup=cancel())
        await AdminState.enter_admin_id_for_del.set()


async def add_admin_menu(message: types.Message):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили добавление администратора", reply_markup=personal_kb())
    else:
        try:
            data = msg.split(":")
            id_ = data[0]
            name = data[1]
            add_admin(telegram_id=id_, name=name)
            await message.answer(f"Вы добавили администратора с id={id_} и именем {name}", reply_markup=personal_kb())
        except Exception as e:
            logger.error(e)
            await message.answer("Невозможно добавить админа, обратитесь в поддержку", reply_markup=personal_kb())
    await AdminState.personal.set()


async def delete_admin_menu(message: types.Message):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили удаление админа", reply_markup=personal_kb())
    else:
        admin = get_admin_by_id(msg)
        if admin is None:
            await message.answer("Администратора с таким id не существует", reply_markup=personal_kb())
        else:
            delete_admin(telegram_id=msg)
            await storage.set_state(user=msg, state=None)
            await message.answer(f"Вы удалили администратора с id={admin.telegram_id} и именем {admin.name}",
                                 reply_markup=personal_kb())
    await AdminState.personal.set()


async def answer_on_report(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split("_")
    # if data[0] == "delete":
    # await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    if data[0] == "complete":
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=callback.message.text + "\n\n*РЕШЕНО*",
            reply_markup=None,
            parse_mode="Markdown",
        )
        await state.reset_data()
        await callback.answer("Обращение обработано!")
    else:
        client_id = data[1]
        await callback.message.answer(
            "Напишите ответ пользователю", reply_markup=cancel()
        )
        await callback.answer("")
        await AdminState.enter_support_message.set()
        await state.update_data(client_id=client_id)


async def enter_msg_for_answer_support(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer(
            "Вы отменили ответ на обращение клиента", reply_markup=main_admin_kb()
        )
        await AdminState.start.set()
        await state.reset_data()
    else:
        data = await state.get_data()
        client_id = data["client_id"]
        try:
            await bot.send_message(chat_id=client_id, text=msg)
            await message.answer(
                "Ваше сообщение было отправлено", reply_markup=main_admin_kb()
            )
        except Exception as e:
            logger.error(e)
            await message.answer(
                "Ваше сообщение не было отправлено из-за серверной ошибки, обратитесь "
                "к команде разработчиков или попробуйте ответить вручную",
                main_admin_kb(),
            )
        await AdminState.start.set()


async def event_menu(message: types.Message):
    msg = message.text
    if msg == back_btn:
        await message.answer("Вы вернулись в главное меню", reply_markup=main_admin_kb())
        await AdminState.start.set()
    elif msg == EventBtnName.create:
        events = get_events()
        if len(events) == MAX_EVENTS:
            await message.answer("Вы достигли максимального количества афиш", reply_markup=event_kb())
        else:
            await message.answer("*Шаг [1/3]*\nВведите дату афиши в формате:\n01-01-2023", reply_markup=cancel(),
                                 parse_mode="Markdown")
            await AdminState.choose_event_date.set()
    elif msg == EventBtnName.delete:
        await message.answer("Введите дату афиши, которую надо удалить, в формате:\n01-01-2023", reply_markup=cancel())
        await AdminState.delete_event.set()
    elif msg == EventBtnName.get:
        kb = choose_date_kb()
        if kb is not None:
            await message.answer("Выберите дату", reply_markup=choose_date_kb())
        else:
            await message.answer("Вы не загрузили ни одной афиши")


async def choose_event_date(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили создание афиши", reply_markup=event_kb())
        await AdminState.events.set()
    else:
        await state.update_data(date=msg)
        await message.answer(
            "*Шаг [2/3]*\nВведите текст к афише",
            parse_mode="Markdown",
            reply_markup=cancel_or_miss(),
        )
        await AdminState.enter_event_message.set()


async def enter_event_message(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили создание афишы", reply_markup=event_kb())
        await AdminState.events.set()
    elif msg == CancelBtnName.miss:
        await message.answer(
            "*Шаг [3/3]*\nПришлите медиафайл к афише",
            parse_mode="Markdown",
            reply_markup=cancel(),
        )
        await AdminState.enter_event_picture.set()
    else:
        await state.update_data(text=msg)
        await message.answer(
            "*Шаг [3/3]*\nПришлите медиафайл к афише",
            parse_mode="Markdown",
            reply_markup=cancel_or_miss(),
        )
        await AdminState.enter_event_picture.set()


async def enter_event_picture(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили создание афишы", reply_markup=event_kb())
    elif msg == CancelBtnName.miss:
        data = await state.get_data()
        date = data["date"]
        text = data["text"]
        delete_event_by_date(date)
        add_event(date=date, text=text)
        await message.answer(f"Афиша на дату {date} создана", reply_markup=event_kb())
        await state.reset_data()
    else:
        data = await state.get_data()
        date = data["date"]
        try:
            text = data["text"]
        except Exception as e:
            text = ""
        dest = f"sources/events/{date}.jpeg"
        video_dest = f"sources/events/{date}.mp4"
        try:
            os.remove(dest)
            os.remove(video_dest)
        except Exception as e:
            logger.info(e)
        delete_event_by_date(date)
        await message.photo[-1].download(dest)
        add_event(date=date, text=text, media_path=dest)
        await message.answer(f"Афиша на дату {date} создана", reply_markup=event_kb())
        await state.reset_data()
    await AdminState.events.set()


async def enter_event_video(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили создание афишы", reply_markup=event_kb())
    elif msg == CancelBtnName.miss:
        data = await state.get_data()
        date = data["date"]
        text = data["text"]
        delete_event_by_date(date)
        add_event(date=date, text=text)
        await message.answer(f"Афиша на дату {date} создана", reply_markup=event_kb())
        await state.reset_data()
    else:
        data = await state.get_data()
        date = data["date"]
        text = data["text"]
        pic_dest = f"sources/events/{date}.jpeg"
        dest = f"sources/events/{date}.mp4"
        try:
            os.remove(pic_dest)
        except Exception as e:
            logger.info(e)
        delete_event_by_date(date)
        file_id = message.video.file_id
        file = await bot.get_file(file_id)
        await bot.download_file(file.file_path, dest)
        add_event(date=date, text=text, media_path=dest)
        await message.answer(f"Афиша на дату {date} создана", reply_markup=event_kb())
        await state.reset_data()
    await AdminState.events.set()


async def delete_event(message: types.Message):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили удаление афиши", reply_markup=event_kb())
    else:
        delete_event_by_date(msg)
        await message.answer(f"Вы удалили афишу на {msg}", reply_markup=event_kb())
    await AdminState.events.set()


async def choose_date(callback: types.CallbackQuery):
    data = callback.data.split("_")
    date = data[1]
    event = get_event_by_date(date)
    if event["text"] is None:
        text = ""
    else:
        text = event["text"]
    if event["media"] is None:
        await bot.send_message(chat_id=callback.message.chat.id, text=text)
    if "jpeg" in event["media"]:
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=types.InputFile(event["media"]),
            caption=text,
        )
    if "mp4" in event["media"]:
        await bot.send_video(chat_id=callback.message.chat.id,
                             video=types.InputFile(event["media"]),
                             caption=text)


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(main_admin_menu, state=AdminState.start)
    dp.register_message_handler(cancel_enter_photo, state=AdminState.enter_photo)
    dp.register_message_handler(
        enter_photo, state=AdminState.enter_photo, content_types=["photo"]
    )
    dp.register_message_handler(enter_message, state=AdminState.enter_message)
    dp.register_message_handler(database_menu, state=AdminState.database)
    dp.register_message_handler(personal_menu, state=AdminState.personal)
    dp.register_message_handler(enter_id_for_banning, state=AdminState.ban)
    dp.register_message_handler(enter_id_for_delete_user, state=AdminState.delete_user)
    dp.register_message_handler(add_admin_menu, state=AdminState.enter_admin_id)
    dp.register_message_handler(delete_admin_menu, state=AdminState.enter_admin_id_for_del)
    dp.register_callback_query_handler(answer_on_report, state=[*AdminState.all_states])
    dp.register_message_handler(
        enter_msg_for_answer_support, state=AdminState.enter_support_message
    )
    dp.register_message_handler(event_menu, state=AdminState.events)
    dp.register_message_handler(choose_event_date, state=AdminState.choose_event_date)
    dp.register_message_handler(enter_event_message, state=AdminState.enter_event_message)
    dp.register_message_handler(enter_event_picture, state=AdminState.enter_event_picture, content_types=["photo"])
    dp.register_message_handler(enter_event_video, state=AdminState.enter_event_picture, content_types=["video"])
    dp.register_message_handler(delete_event, state=AdminState.delete_event)
    dp.register_callback_query_handler(choose_date, state="*")

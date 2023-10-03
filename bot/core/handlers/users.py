from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from loguru import logger

from bot.config import bot, storage
from bot.core.consts import (
    CONTACTS,
    LATITUDE,
    LONGITUDE,
    SALES,
    MENU,
    YANDEX_MAP_URL,
    PHOTO_URL,
    DEVELOPER_INFO,
)
from bot.core.db.client_actions import (
    update_client_by_tg_id,
    get_start_client_by_tg_id,
    add_client,
)
from bot.core.db.event_actions import get_event_by_day
from bot.core.keyboards.admin_keyboards.admin_keyboard import (
    main_admin_kb,
    WeekendBtnName,
)
from bot.core.keyboards.cancel_keyboard import cancel, cancel_send_phone, CancelBtnName
from bot.core.keyboards.user_keyboards.user_keyboard import (
    main_menu_kb,
    MainMenuBtnName,
    LoyaltyProgramBtnName,
    choose_weekend_day_kb,
    WeekendDayBtnName,
    report_menu_kb,
    back_btn,
    ReportBtnName,
)
from bot.core.logic.user_logic import client_send_msg_to_admin
from bot.core.states.admin_state import AdminState
from bot.core.states.user_state import UserState, Registration
from bot.core.utils import get_admins_id


async def start_command(message: types.Message):
    await storage.set_state(user=message.chat.id, state=None)
    user = get_start_client_by_tg_id(message.from_user.id)

    if user is None:
        data = {"telegram_id": message.from_user.id}
        try:
            data["name"] = message.from_user.first_name
            data["username"] = message.from_user.username
            data["phone"] = message.contact.phone_number
        except AttributeError as e:
            logger.error(e)
        logger.info(f"{data} was added to database")
        add_client(data)
    await message.answer("Рады снова вас видеть", reply_markup=main_menu_kb())
    await UserState.start.set()


async def become_admin(message: types.Message):
    admins_id = get_admins_id()

    if str(message.from_user.id) in admins_id:
        await message.answer("Вы вошли как админ", reply_markup=main_admin_kb())
        await AdminState.start.set()
    else:
        await message.answer("У вас нет доступа")


async def become_user(message: types.Message):
    admins_id = get_admins_id()
    if str(message.chat.id) in admins_id:
        await storage.set_state(user=message.chat.id, state=None)
        await UserState.start.set()
        await message.answer("Вы зашли как пользователь", reply_markup=main_menu_kb())
    else:
        await message.answer("У вас нет доступа")


async def sign_up_start_stage(message: types.Message):
    msg = message.text
    if msg == LoyaltyProgramBtnName.registration:
        await message.answer(
            "*Шаг [1/7]*\nВведите вашe имя",
            reply_markup=cancel(),
            parse_mode="Markdown",
        )
        await Registration.name_stage.set()
    elif msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили регистрацию", reply_markup=main_menu_kb())
        await UserState.start.set()


async def sign_up_name_stage(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили регистрацию", reply_markup=main_menu_kb())
        await UserState.start.set()
        await state.reset_data()
    else:
        await message.answer(
            "*Шаг [2/7]*\nВведите вашу фамилию",
            reply_markup=cancel(),
            parse_mode="Markdown",
        )
        await state.update_data(name=msg)
        await state.update_data(nickname=message.from_user.username)
        await state.update_data(telegram_id=message.from_user.id)
        await Registration.surname_stage.set()


async def sign_up_surname_stage(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили регистрацию", reply_markup=main_menu_kb())
        await UserState.start.set()
        await state.reset_data()
    else:
        await message.answer(
            "*Шаг [3/7]*\nВведите ваше отчество",
            reply_markup=cancel(),
            parse_mode="Markdown",
        )
        await state.update_data(surname=msg)
        await Registration.patronymic_stage.set()


async def sign_up_patronymic_stage(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили регистрацию", reply_markup=main_menu_kb())
        await UserState.start.set()
        await state.reset_data()
    else:
        await message.answer(
            "*Шаг [4/7]*\nВведите вашу дату рождения",
            reply_markup=cancel(),
            parse_mode="Markdown",
        )
        await state.update_data(patronymic=msg)
        await Registration.birthday_stage.set()


async def sign_up_bday_stage(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили регистрацию", reply_markup=main_menu_kb())
        await UserState.start.set()
        await state.reset_data()
    else:
        await message.answer(
            "*Шаг [5/7]*\nПоделитесь номером телефона",
            reply_markup=cancel_send_phone(),
            parse_mode="Markdown",
        )
        await state.update_data(bday=msg)
        await Registration.phone_stage.set()


async def cancel_sign_up_phone_stage(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили регистрацию", reply_markup=main_menu_kb())
        await UserState.start.set()
        await state.reset_data()


# async def sign_up_phone_stage(message: types.Message, state: FSMContext):
#     await state.update_data(phone=message.contact.phone_number)
#     await message.answer(
#         "*Шаг [6/7]*\nВыберите ваш пол", reply_markup=gender_kb(), parse_mode="Markdown"
#     )
#     await Registration.sex_stage.set()
#
#
# async def sign_up_gender_stage(message: types.Message, state: FSMContext):
#     msg = message.text
#     if msg == CancelBtnName.cancel_btn:
#         await message.answer("Вы отменили регистрацию", reply_markup=main_menu_kb())
#         await UserState.start.set()
#         await state.reset_data()
#     else:
#         await message.answer(
#             "*Шаг [7/7]*\nВведите ваш адрес электронной почты",
#             reply_markup=cancel(),
#             parse_mode="Markdown",
#         )
#         await state.update_data(gender=get_gender(msg))
#         await Registration.email_stage.set()


async def sign_up_email_stage(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили регистрацию", reply_markup=main_menu_kb())
        await UserState.start.set()
        await state.reset_data()
    else:
        await state.update_data(email=msg)
        data = await state.get_data()
        try:
            # prime_hill_client = PrimeHillModel(
            #     lastName=data.get("name"),
            #     firstName=data.get("surname"),
            #     patronymic=data.get("patronymic"),
            #     birthday=data.get("bday"),
            #     sex=data.get("gender"),
            #     email=data.get("email"),
            #     phone=data.get("phone"),
            # )
            # prime_hill_card = create_client(prime_hill_client)
            # await state.update_data(prime_hill_card=prime_hill_card)
            update_client_by_tg_id(message.from_user.id, data)
            await message.answer(
                # f"Вы успешно прошли регистрацию, вот ваша карта: {prime_hill_card}",
            )
        except Exception as e:
            print(f"Error on adding new client {e}")
        await state.reset_data()
        await UserState.start.set()


async def main_menu_handler(message: types.Message):
    msg = message.text
    if msg == MainMenuBtnName.menu:
        await message.answer(MENU, reply_markup=main_menu_kb())
    elif msg == MainMenuBtnName.sales:
        await message.answer(SALES, reply_markup=main_menu_kb())
    elif msg == MainMenuBtnName.events:
        await message.answer("Выберите день", reply_markup=choose_weekend_day_kb())
    elif msg == MainMenuBtnName.photos:
        await message.answer(
            f"Фотографии с наших мероприятий!❤️\n\n{PHOTO_URL}",
            reply_markup=main_menu_kb(),
        )
    elif msg == MainMenuBtnName.contacts:
        await message.answer(
            text=CONTACTS, reply_markup=main_menu_kb(), parse_mode="Markdown"
        )
        await message.answer_location(
            latitude=LATITUDE, longitude=LONGITUDE, reply_markup=main_menu_kb()
        )
    elif msg == MainMenuBtnName.feedback:
        await message.answer(
            "Вы можете оставить отзыв на Яндекс картах или написать обращение администрации",
            reply_markup=report_menu_kb(),
        )
        await UserState.report.set()
    elif msg == MainMenuBtnName.developer:
        await message.answer(text=DEVELOPER_INFO, reply_markup=main_menu_kb())
    elif msg == MainMenuBtnName.booking:
        await message.answer("*Шаг [1/5]*\nВведите ваше имя", reply_markup=cancel(), parse_mode="Markdown")
        await UserState.enter_name.set()


async def enter_name_for_booking(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили бронирование", reply_markup=main_menu_kb())
        await UserState.start.set()
        await state.reset_data()
    else:
        await message.answer(
            "*Шаг [2/5]*\nПоделитесь номером телефона",
            reply_markup=cancel_send_phone(),
            parse_mode="Markdown",
        )
        await state.update_data(name=msg)
        await state.update_data(telegram_link=f'tg://user?id={message.from_user.id}')
        await UserState.enter_phone.set()


async def cancel_enter_phone(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили бронирование", reply_markup=main_menu_kb())
        await UserState.start.set()
        await state.reset_data()


async def enter_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer(
        "*Шаг [3/5]*\nВведите количество гостей", reply_markup=cancel(), parse_mode="Markdown"
    )
    await UserState.enter_persons.set()


async def enter_persons(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили бронирование", reply_markup=main_menu_kb())
        await UserState.start.set()
        await state.reset_data()
    else:
        await message.answer(
            "*Шаг [4/5]*\nУкажите дату, на которую нужно забронировать в формате: 01-01-2023",
            reply_markup=cancel(),
            parse_mode="Markdown",
        )
        await state.update_data(persons=msg)
        await UserState.enter_date.set()


async def enter_date(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили бронирование", reply_markup=main_menu_kb())
        await UserState.start.set()
        await state.reset_data()
    else:
        await message.answer(
            "*Шаг [5/5]*\nУкажите время, на которое нужно забронировать",
            reply_markup=cancel(),
            parse_mode="Markdown",
        )
        await state.update_data(date=msg)
        await UserState.enter_time.set()


async def enter_time(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили бронирование", reply_markup=main_menu_kb())
        await state.reset_data()
    else:
        await message.answer(
            "*Ваша заявка принята!* Скоро с вами свяжется наш сотрудник!",
            reply_markup=main_menu_kb(),
            parse_mode="Markdown",
        )
        await state.update_data(time=msg)

        data = await state.get_data()
        booking_msg = (f"Имя: {data['name']}\n"
                       f"Телефон: {data['phone']}\n"
                       f"Гостей: {data['persons']}\n"
                       f"Дата: {data['date']}\n"
                       f"Время: {data['time']}\n"
                       f"Ссылка: {data['telegram_link']}")
        chat_id = "-950716402"
        await bot.send_message(text=booking_msg, chat_id=chat_id)
    await UserState.start.set()


async def choose_day(callback: types.CallbackQuery):
    day = WeekendBtnName.friday if WeekendBtnName.friday in callback.data else WeekendBtnName.saturday
    event = get_event_by_day(day)
    if event is not None:
        if event["text"] is None:
            text = "Афиша скоро будет опубликована🤩"
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
    else:
        await callback.message.answer("Афиша на этот день пока еще не выложена🥹")
    await callback.answer("")


async def report_menu(message: types.Message):
    msg = message.text
    if msg == back_btn:
        await message.answer("Вы вернулись в главное меню", reply_markup=main_menu_kb())
        await UserState.start.set()
    elif msg == ReportBtnName.yandex:
        await message.answer(
            f"Переходите по ссылке и оставляйте отзыв на Яндекс картах🗺️\n\n{YANDEX_MAP_URL}"
        )
    elif msg == ReportBtnName.to_admin:
        await message.answer("Введите ваше сообщение: ", reply_markup=cancel())
        await UserState.enter_report.set()


async def enter_report_menu(message: types.Message):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer(
            "Вы отменили ввод сообщения", reply_markup=report_menu_kb()
        )
        await UserState.report.set()
    else:
        await client_send_msg_to_admin(message.from_user.id, msg, message.message_id)
        await message.answer(
            "Ваше обращение отправлено, скоро вернемся с обратной связью!",
            reply_markup=report_menu_kb(),
        )
        await UserState.report.set()


def register_users_handlers(dp: Dispatcher):
    dp.register_message_handler(become_admin, state="*", commands=["admin"])
    dp.register_message_handler(
        become_user, commands=["user"], state=[*AdminState.all_states]
    )
    dp.register_message_handler(start_command, commands=["start"], state=[None, *UserState.all_states,
                                                                          *AdminState.all_states])
    dp.register_message_handler(main_menu_handler, state=UserState.start)
    dp.register_callback_query_handler(choose_day, state="*")
    dp.register_message_handler(report_menu, state=UserState.report)
    dp.register_message_handler(enter_name_for_booking, state=UserState.enter_name)
    dp.register_message_handler(enter_phone, state=UserState.enter_phone, content_types=types.ContentType.CONTACT)
    dp.register_message_handler(cancel_enter_phone, state=UserState.enter_phone)
    dp.register_message_handler(enter_persons, state=UserState.enter_persons)
    dp.register_message_handler(enter_date, state=UserState.enter_date)
    dp.register_message_handler(enter_time, state=UserState.enter_time)
    dp.register_message_handler(enter_report_menu, state=UserState.enter_report)


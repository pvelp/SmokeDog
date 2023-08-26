from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot.core.db.actions import get_client_by_tg_id, add_client, add_new_client
from bot.core.models import ClientModel, PrimeHillModel
from bot.core.keyboards.cancel_keyboard import cancel, cancel_send_phone, CancelBtnName
from bot.core.keyboards.user_keyboard import (
    main_menu_kb,
    MainMenuBtnName,
    loyalty_kb,
    LoyaltyProgramBtnName,
    get_gender,
    gender_kb,
)
from bot.core.states.user_state import UserState, Registration
from bot.service.prime_hill_service.request_card import create_client


async def start_command(message: types.Message):
    user = get_client_by_tg_id(message.from_user.id)
    if user is None:
        await message.answer(
            "Вы можете зарегестрироваться в программе лояльности",
            reply_markup=main_menu_kb()
        )
    else:
        await message.answer("Рады снова вас видеть", reply_markup=main_menu_kb())
    await UserState.start.set()


async def sign_up_start_stage(message: types.Message):
    msg = message.text
    if msg == LoyaltyProgramBtnName.registration:
        await message.answer(
            "*Шаг [1/7]*\nВведите вашe имя",
            reply_markup=cancel(),
            parse_mode="Markdown"
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
            parse_mode="Markdown"
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
            parse_mode="Markdown"
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
            parse_mode="Markdown"
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
            parse_mode="Markdown"
        )
        await state.update_data(bday=msg)
        await Registration.phone_stage.set()


async def cancel_sign_up_phone_stage(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили регистрацию", reply_markup=main_menu_kb())
        await UserState.start.set()
        await state.reset_data()


async def sign_up_phone_stage(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer(
        "*Шаг [6/7]*\nВыберите ваш пол", reply_markup=gender_kb(), parse_mode="Markdown"
    )
    await Registration.sex_stage.set()


async def sign_up_gender_stage(message: types.Message, state: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили регистрацию", reply_markup=main_menu_kb())
        await UserState.start.set()
        await state.reset_data()
    else:
        await message.answer(
            "*Шаг [7/7]*\nВведите ваш адрес электронной почты",
            reply_markup=cancel(),
            parse_mode="Markdown"
        )
        await state.update_data(gender=get_gender(msg))
        await Registration.email_stage.set()


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
            prime_hill_client = PrimeHillModel(
                lastName=data.get("name"),
                firstName=data.get("surname"),
                patronymic=data.get("patronymic"),
                birthday=data.get("bday"),
                sex=data.get("gender"),
                email=data.get("email"),
                phone=data.get("phone")
            )
            prime_hill_card = create_client(prime_hill_client)
            await state.update_data(prime_hill_card=prime_hill_card)
            add_client(data)
            # user = ClientModel(
            #     telegram_id=data.get("telegram_id"),
            #     name=data.get("name"),
            #     username=data.get("nickname"),
            #     phone=data.get("phone"),
            #     birthday=data.get("dbay"),
            #     is_banned=False,
            #     card=prime_hill_card
            # )
            await message.answer(
                f"Вы успешно прошли регистрацию, вот ваша карта: {prime_hill_card}",
            )
        except Exception as e:
            print(f"Error on adding new client {e}")
        await state.reset_data()
        await UserState.start.set()


async def main_menu_handler(message: types.Message):
    msg = message.text
    if msg == MainMenuBtnName.menu:
        await message.answer("Меню", reply_markup=main_menu_kb())
    elif msg == MainMenuBtnName.tips:
        await message.answer("Чаевые", reply_markup=main_menu_kb())
    elif msg == MainMenuBtnName.sales:
        await message.answer("Акции", reply_markup=main_menu_kb())
    elif msg == MainMenuBtnName.events:
        await message.answer("Афмша", reply_markup=main_menu_kb())
    elif msg == MainMenuBtnName.photos:
        await message.answer("Фотоотчет", reply_markup=main_menu_kb())
    elif msg == MainMenuBtnName.contacts:
        await message.answer("Контакты", reply_markup=main_menu_kb())
    elif msg == MainMenuBtnName.feedback:
        await message.answer("Оставить отзыв", reply_markup=main_menu_kb())
    elif msg == MainMenuBtnName.loyalty_program:
        await message.answer("Программа лояльности", reply_markup=loyalty_kb())
        await UserState.sign_up.set()


# TODO: сделать клавиатуру для программы лояльности, отзывы, сделать модель для сервиса создания клиента


def register_users_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"], state=["*"])
    dp.register_message_handler(sign_up_start_stage, state=UserState.sign_up)
    dp.register_message_handler(sign_up_name_stage, state=Registration.name_stage)
    dp.register_message_handler(sign_up_bday_stage, state=Registration.birthday_stage)
    dp.register_message_handler(sign_up_surname_stage, state=Registration.surname_stage)
    dp.register_message_handler(sign_up_email_stage, state=Registration.email_stage)
    dp.register_message_handler(sign_up_gender_stage, state=Registration.sex_stage)
    dp.register_message_handler(
        sign_up_patronymic_stage, state=Registration.patronymic_stage
    )
    dp.register_message_handler(
        cancel_sign_up_phone_stage, state=Registration.phone_stage
    )
    dp.register_message_handler(
        sign_up_phone_stage,
        state=Registration.phone_stage,
        content_types=types.ContentType.CONTACT,
    )
    dp.register_message_handler(main_menu_handler, state=UserState.start)

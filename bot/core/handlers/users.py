from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from bot.core.models import ClientModel
from base.db_models.models import Client
from bot.keyboards.utils import create_buttons
from bot.keyboards.cancel_keyboard import cancel, cancel_send_phone, CancelBtnName
from bot.core.db.actions import get_client_by_tg_id, add_new_client
from bot.core.states.user_state import UserState, Registration


async def start_command(message: types.Message):
    user = get_client_by_tg_id(message.from_user.id)
    if user is None:
        kb = create_buttons(["Зарегистрироваться"])
        await message.answer("Пройдите регистрацию", reply_markup=kb)
        await UserState.sign_up.set()
    else:
        await message.answer("Рады снова вас видеть")


async def sign_up_start_stage(message: types.Message):
    msg = message.text
    if msg == "Зарегистрироваться":
        await message.answer("*Шаг [1/3]*\nВведите вашe имя", reply_markup=cancel(), parse_mode="Markdown")
        await Registration.name_stage.set()
    elif msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили регистрацию")
        await UserState.default_state.set()


async def sign_up_name_stage(message: types.Message, ctx: FSMContext):
    msg = message.text
    if msg == CancelBtnName.cancel_btn:
        await message.answer("Вы отменили регистрацию")
        await UserState.default_state.set()
    else:
        await message.answer("*Шаг [2/3]*\nВведите дату вашего рождения")
        await ctx.update_data(name=msg)
        await Registration.birthday_stage.set()


def register_users_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'], state=["*"])
    dp.register_message_handler(sign_up_start_stage, state=UserState.sign_up)
    dp.register_message_handler(sign_up_name_stage, state=Registration.name_stage)

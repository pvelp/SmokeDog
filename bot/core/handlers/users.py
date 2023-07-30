from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from core.models import ClientModel
from base.db_models.models import Client
from bot.core.db.actions import get_client_by_id, add_new_client
from bot.core.states.user_state import UserState


async def start_command(message: types.Message):
    user = get_client_by_id(message.from_user.id)
    if user is None:
        await message.answer("Пройдите регистрацию")
        await UserState.sign_up.set()
    else:
        await message.answer("Рады снова вас видеть")


async def start_menu(message: types.Message):
    await message.answer("Hello world")


def register_users_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(start_menu, state="*")

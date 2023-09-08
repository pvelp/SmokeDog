from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot.core.keyboards.admin_keyboards.admin_keyboard import main_admin_kb
from bot.core.states.admin_state import AdminState
from bot.settings import settings


async def start_admin(message: types.Message):
    if message.from_user.id == settings.admin_id:
        await message.answer("Вы вошли как админ", reply_markup=main_admin_kb())
        await AdminState.start.set()


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(start_admin, commands=["admin"], state=["*"])



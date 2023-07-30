from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    start = State()
    sign_up = State()

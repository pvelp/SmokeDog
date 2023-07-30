from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    default_state = State()
    start = State()
    sign_up = State()


class Registration(StatesGroup):
    name_stage = State()
    birthday_stage = State()
    phone_stage = State()

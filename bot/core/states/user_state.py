from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    default_state = State()
    start = State()
    sign_up = State()
    loaylty = State()


class Registration(StatesGroup):
    name_stage = State()
    surname_stage = State()
    patronymic_stage = State()
    email_stage = State()
    birthday_stage = State()
    phone_stage = State()
    sex_stage = State()


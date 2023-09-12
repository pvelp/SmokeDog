from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminState(StatesGroup):
    start = State()
    enter_message = State()
    enter_photo = State()
    database = State()

from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminState(StatesGroup):
    start = State()
    enter_message = State()
    enter_photo = State()
    database = State()
    ban = State()
    delete_user = State()
    personal = State()
    enter_support_message = State()
    enter_event_message = State()
    enter_event_picture = State()
    choose_event_date = State()
    enter_admin_id = State()
    enter_admin_id_for_del = State()
    events = State()
    delete_event = State()
    choose_event = State()
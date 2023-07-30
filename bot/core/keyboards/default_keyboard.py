from bot.core.keyboards.utils import create_buttons


class DefaultKeyboardBtnName:
    registration = "Регистрация"
    info = "Информация о боте"


DefaultButtons = [DefaultKeyboardBtnName.registration, DefaultKeyboardBtnName.info]


def default_kb():
    kb = create_buttons(DefaultButtons)
    return kb

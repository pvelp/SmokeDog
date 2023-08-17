from bot.core.keyboards.cancel_keyboard import CancelBtnName
from bot.core.keyboards.utils import create_buttons


class MainMenuBtnName:
    loyalty_program = "Программа лояльности"
    menu = "Меню"
    tips = "Чаевые"
    sales = "Акции"
    photos = "Фотоотчет"
    events = "Афиша"
    feedback = "Оставить отзыв"
    contacts = "Контакты"


class LoyaltyProgramBtnName:
    registration = "Регистрация"


main_menu_btns = [
    MainMenuBtnName.loyalty_program,
    MainMenuBtnName.menu,
    MainMenuBtnName.tips,
    MainMenuBtnName.sales,
    MainMenuBtnName.photos,
    MainMenuBtnName.events,
    MainMenuBtnName.feedback,
    MainMenuBtnName.contacts,
]

loyalty_program_btns = [LoyaltyProgramBtnName.registration, CancelBtnName.cancel_btn]


def main_menu_kb():
    return create_buttons(main_menu_btns)


def loyalty_kb():
    return create_buttons(loyalty_program_btns)

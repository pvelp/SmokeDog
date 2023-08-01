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


main_menu_btns = [
    MainMenuBtnName.loyalty_program,
    MainMenuBtnName.menu,
    MainMenuBtnName.tips,
    MainMenuBtnName.sales,
    MainMenuBtnName.photos,
    MainMenuBtnName.events,
    MainMenuBtnName.feedback,
    MainMenuBtnName.contacts
]


def main_menu_kb():
    return create_buttons(main_menu_btns)

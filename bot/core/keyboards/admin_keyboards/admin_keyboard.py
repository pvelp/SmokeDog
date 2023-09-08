from bot.core.keyboards.utils import create_buttons


class MainAdminMenuBtnsName:
    mailing = "Рассылка"
    events = "Афиша"


main_admin_menu_btns = [
    MainAdminMenuBtnsName.mailing,
    MainAdminMenuBtnsName.events
]


def main_admin_kb():
    return create_buttons(main_admin_menu_btns)

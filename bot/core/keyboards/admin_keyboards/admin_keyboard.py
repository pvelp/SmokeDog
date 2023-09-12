from bot.core.keyboards.utils import create_buttons


class MainAdminMenuBtnName:
    mailing = "Рассылка"
    events = "Изменить афишу"
    database = "База клиентов"
    personal = "Персонал"


class DataBaseMenuBtnName:
    get_db = "Получить базу"
    ban_client = "Заблокировать клиента"
    delete_client = "Удалить клиента"


main_admin_menu_btns = [
    MainAdminMenuBtnName.mailing,
    MainAdminMenuBtnName.events,
    MainAdminMenuBtnName.database,
    MainAdminMenuBtnName.personal
]

database_menu_btns = [
    DataBaseMenuBtnName.get_db,
    DataBaseMenuBtnName.ban_client,
    DataBaseMenuBtnName.delete_client
]


def main_admin_kb():
    return create_buttons(main_admin_menu_btns)


def database_kb():
    return create_buttons(database_menu_btns)
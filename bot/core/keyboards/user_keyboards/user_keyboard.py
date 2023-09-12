from bot.core.consts import TIPS_URL, BOOKING_URL
from bot.core.keyboards.cancel_keyboard import CancelBtnName, back_btn
from bot.core.keyboards.utils import create_buttons, create_inline_buttons


class MainMenuBtnName:
    loyalty_program = "Программа лояльности"
    menu = "🍾Меню"
    tips = "☕️Чаевые"
    booking = "🍽️Забронировать"
    sales = "🤑Акции"
    photos = "📸Фотоотчет"
    events = "💃🏻Афиша"
    feedback = "📢Оставить отзыв"
    contacts = "📞Контакты"


class WeekendDayBtnName:
    friday = "🍻Пятница"
    saturday = "🎸Суббота"


class LoyaltyProgramBtnName:
    registration = "Регистрация"


class ReportBtnName:
    to_admin = "👮🏻‍Обращение для администрации"
    yandex = "📍Яндекс"


main_menu_btns = [
    MainMenuBtnName.menu,
    MainMenuBtnName.tips,
    MainMenuBtnName.booking,
    MainMenuBtnName.sales,
    MainMenuBtnName.photos,
    MainMenuBtnName.events,
    MainMenuBtnName.feedback,
    MainMenuBtnName.contacts,
]


report_btns = [ReportBtnName.yandex, ReportBtnName.to_admin, back_btn]


def main_menu_kb():
    return create_buttons(
        main_menu_btns,
        {MainMenuBtnName.tips: TIPS_URL, MainMenuBtnName.booking: BOOKING_URL},
    )


def choose_weekend_day_kb():
    return create_inline_buttons([WeekendDayBtnName.friday, WeekendDayBtnName.saturday])


def report_menu_kb():
    return create_buttons(report_btns)

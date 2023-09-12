from bot.core.db.admin_actions import get_all_admins
from bot.core.models import AdminModel
from bot.settings import settings


def get_admins_id() -> list[str]:
    admins = get_all_admins()
    result = [settings.admin_id]
    for admin in admins:
        result.append(admin.telegram_id)
    return result

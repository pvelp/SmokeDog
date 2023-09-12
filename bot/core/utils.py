from bot.core.db.admin_actions import get_all_admins
from bot.core.db.client_actions import get_all_clients
from bot.core.models import AdminModel
from bot.settings import settings


def get_admins_id() -> list[str]:
    admins = get_all_admins()
    result = [settings.admin_id]
    for admin in admins:
        result.append(admin.telegram_id)
    return result


def get_clients_id() -> list[str]:
    clients = get_all_clients()
    result = []
    for client in clients:
        result.append(client.telegram_id)
    return result

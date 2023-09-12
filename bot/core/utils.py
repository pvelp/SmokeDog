from bot.core.db.admin_actions import get_all_admins
from bot.core.db.client_actions import get_all_clients
from bot.settings import settings
import pandas as pd
from sqlalchemy import create_engine


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


def get_excel_from_db(db_name: str):
    dest = f"{db_name}.xlsx"
    my_conn = create_engine(settings.db_url)
    q = f"SELECT * FROM {db_name}"
    df = pd.read_sql(q, my_conn)
    df.to_excel(dest)


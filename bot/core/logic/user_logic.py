from aiogram import types
from loguru import logger

from bot.config import bot
from bot.core.db.client_actions import get_client_by_tg_id
from bot.core.utils import get_admins_id


async def client_send_msg_to_admin(client_id, msg: str, message_id):
    client = get_client_by_tg_id(client_id)
    client_id = client.telegram_id

    msg_for_admin = f"""
*Новое обращение от клиента*❗

*Id клиента*: {client_id}
*Его сообщение*:

{msg}

После ответа на обращение нажмите кнопку *"Решено"*.
"""

    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardMarkup(text="Ответить вручную", url=f'tg://user?id={client_id}'))
    markup.row(types.InlineKeyboardMarkup(text="Ответить через бота", callback_data=f'report_{client_id}'))
    # markup.row(types.InlineKeyboardMarkup(text="Решено", callback_data=f"delete_msg"))
    markup.row(types.InlineKeyboardMarkup(text="Решено", callback_data=f"complete_msg"))

    admins_id = get_admins_id()
    for id_ in admins_id:
        try:
            await bot.send_message(text=msg_for_admin, chat_id=id_, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"{e}, chat_id={id_}")





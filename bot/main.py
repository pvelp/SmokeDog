import sys

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from loguru import logger

from config import dp, loop

sys.path.insert(0, '.')
from settings import settings
from base.db_connection import set_settings_file_for_db
from bot.core.handlers.users import register_users_handlers

if __name__ == "__main__":
    set_settings_file_for_db(settings)
    logger.info('database connected successfully')
    register_users_handlers(dp)
    dp.middleware.setup(LoggingMiddleware())
    executor.start_polling(dp, loop=loop)


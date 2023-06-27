import asyncio
import datetime
from loguru import logger
from aiogram.utils import executor
import sys

sys.path.insert(0, '.')
from bot.settings import settings
from base.db_connection import set_settings_file_for_db

if __name__ == "__main__":
    set_settings_file_for_db(settings)
    logger.info('database connected successfully')


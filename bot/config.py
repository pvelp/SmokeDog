import asyncio

from aiogram import Bot

from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.dispatcher import Dispatcher

from settings import settings

bot = Bot(token=settings.token)
# storage = MemoryStorage()
storage = MongoStorage(host='localhost', port=27017, db_name='aiogram_fsm')
dp = Dispatcher(bot, storage=storage)
loop = asyncio.get_event_loop()

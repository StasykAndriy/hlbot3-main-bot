from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from data.config import TOKEN
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    ) 

__all__ = ['bot', 'dp']
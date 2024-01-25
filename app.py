from aiogram import executor
from handlers import dp
from loader import Dispatcher
from data.config import POSTGRES_URL
from aiogram import Dispatcher
from data.config import db
from utils.db_api.user import create_users_db
import middlewares

async def on_startup(dispatcher: Dispatcher):
    print('Установка связи с PostgreSQL')
    await create_users_db()

async def start(_dp):
    await on_startup(dp)
    print('Подключение бд')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start)




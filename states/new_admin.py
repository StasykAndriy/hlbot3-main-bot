from aiogram.dispatcher.filters.state import StatesGroup, State


class NewAdmin(StatesGroup):
    user_id= State()

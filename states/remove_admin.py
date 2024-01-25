from aiogram.dispatcher.filters.state import StatesGroup, State


class DeleteAdmin(StatesGroup):
    user_id= State()

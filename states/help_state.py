from aiogram.dispatcher.filters.state import StatesGroup, State


class helpstate(StatesGroup):
    user_id= State()
    send_message= State()
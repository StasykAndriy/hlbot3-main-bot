from aiogram.dispatcher.filters.state import StatesGroup, State

class balance(StatesGroup):
    amount = State()
    user_id = State()
    confirm1 = State()
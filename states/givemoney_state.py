from aiogram.dispatcher.filters.state import StatesGroup, State


class Givemoney(StatesGroup):
    amount = State()
    carddata = State()
    confirm = State()
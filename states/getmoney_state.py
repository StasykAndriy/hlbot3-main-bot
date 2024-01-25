from aiogram.dispatcher.filters.state import StatesGroup, State


class Getmoney(StatesGroup):
    amount = State()
    carddata = State()
    confirm = State()
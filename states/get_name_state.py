from aiogram.dispatcher.filters.state import StatesGroup, State


class GetName(StatesGroup):
    username = State()
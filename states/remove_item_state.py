from aiogram.dispatcher.filters.state import StatesGroup, State


class RemoveItem(StatesGroup):
    Item_name= State()
    Confirm= State()
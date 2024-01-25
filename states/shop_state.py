from aiogram.dispatcher.filters.state import StatesGroup, State

class NewItem(StatesGroup):
    Name = State()
    Price = State()
    Confirm = State()

class Purchase(StatesGroup):
    cost = State()
    name = State()
    approval = State()
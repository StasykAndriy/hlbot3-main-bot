from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db_api import quick_commands as commands
from utils.db_api.user import Item
from aiogram.utils.callback_data import CallbackData

buy_item = CallbackData("buy", "item_id")

async def get_items():
    markup = InlineKeyboardMarkup()
    markup.add(
    InlineKeyboardButton(text="Назад", callback_data="inform")
    )
    for i in await commands.show_items():

        button_text = f"{i.name}"

        callback_data = callback_data = buy_item.new(item_id=i.id)

        markup.add(
            InlineKeyboardButton(text=button_text, callback_data=callback_data),
        )
    return markup
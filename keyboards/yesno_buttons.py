from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

yesnobtn = InlineKeyboardMarkup()

yes = InlineKeyboardButton(text='Так', callback_data="yes")
no = InlineKeyboardButton(text='Ні', callback_data="no")

yesnobtn.row(yes, no)
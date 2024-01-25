from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

adminbackbtn = InlineKeyboardMarkup()

adminbackbuton = InlineKeyboardButton(text='Назад', callback_data='previous')

adminbackbtn.insert(adminbackbuton)
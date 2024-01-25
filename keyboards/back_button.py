from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

backbtn = InlineKeyboardMarkup()

backbuton = InlineKeyboardButton(text='Назад', callback_data='inform')

backbtn.insert(backbuton)
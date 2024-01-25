from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

gethlpbtn = InlineKeyboardMarkup()

gethelp = InlineKeyboardButton(text='Надіслати повідомлення до адміністрації', callback_data='get')
backbuton = InlineKeyboardButton(text='Назад', callback_data='inform')

gethlpbtn.insert(gethelp)
gethlpbtn.add(backbuton)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.balance_state import balance

adminbtn = InlineKeyboardMarkup()

getid = InlineKeyboardButton(text='Дістати ID', callback_data='getid')
new_balance = InlineKeyboardButton(text='Поставити новий баланс', callback_data='new_balance')
new_item = InlineKeyboardButton(text='Створити новий продукт', callback_data='new_item')
delete_item = InlineKeyboardButton(text='Видалити продукт', callback_data='remove_item')
add_admin = InlineKeyboardButton(text='Додати адміна', callback_data='add_admin')
remove_admin = InlineKeyboardButton(text='Видалити адміна', callback_data='remove_admin')
backbuton = InlineKeyboardButton(text='Назад', callback_data='inform')
getname = InlineKeyboardButton(text='Дістати Нік', callback_data='getname')

adminbtn.row(getid, getname)
adminbtn.row(new_item, delete_item)
adminbtn.add(add_admin, remove_admin)
adminbtn.add(new_balance)
adminbtn.add(backbuton)
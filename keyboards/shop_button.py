from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


shopbtns = InlineKeyboardMarkup()

products = InlineKeyboardButton(text='Замовити Послугу', callback_data='products')
back = InlineKeyboardButton(text="Назад", callback_data="inform" )
givemoney = InlineKeyboardButton(text='Продати дінеро', callback_data='givemoney')
getmoney = InlineKeyboardButton(text='Купити дінеро', callback_data='sellmoney')

shopbtns.add(products)
shopbtns.add(back)
shopbtns.row(getmoney, givemoney)

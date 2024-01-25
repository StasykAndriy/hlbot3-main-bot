from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

starty = InlineKeyboardMarkup()

inform = InlineKeyboardButton(text='Інформація про чат', callback_data="about")
rules = InlineKeyboardButton(text='Правила чату', callback_data="rules")
admin = InlineKeyboardButton(text='Адміністрація', callback_data="support")
rearward = InlineKeyboardButton(text='Повернутися в чат', callback_data="rearward")
shop = InlineKeyboardButton(text='Магазин', callback_data="shop")
help = InlineKeyboardButton(text='Донат', callback_data="help")

starty.row(inform, rules)
starty.row(admin, rearward)
starty.add(shop)
starty.add(help)


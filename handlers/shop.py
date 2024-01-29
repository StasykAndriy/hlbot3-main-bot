from loader import dp, bot
from keyboards.start_buttons import starty
from aiogram import types
from aiogram.types import Message, CallbackQuery
from keyboards.back_button import backbtn
from utils.db_api import quick_commands as commands
from keyboards.shop_button import shopbtns
from utils.db_api.user import Item
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.products_button import get_items
from keyboards.products_button import buy_item
from aiogram.dispatcher import FSMContext
from keyboards.yesno_buttons import yesnobtn
from utils.db_api.user import users
from states.shop_state import Purchase
from data.config import admin_id
from keyboards.start_buttons import starty
from states.getmoney_state import Getmoney
from states.givemoney_state import Givemoney

@dp.callback_query_handler(text_contains="shop")
async def shop (call: CallbackQuery):
    newuser_id = int(call.from_user.id)
    user = await commands.select_user(user_id=newuser_id)

    await call.message.edit_text(f'Ваш баланс - {user.balance} дінеро',
                              reply_markup=shopbtns)

@dp.callback_query_handler(text_contains="products")
async def products(call: CallbackQuery, state=FSMContext):
    markup = await get_items()
    newuser_id = int(call.from_user.id)
    user = await commands.select_user(user_id=newuser_id)
    items = await commands.show_items()
    await call.message.edit_text("Список товарів нижче", reply_markup=markup)
    await Purchase.name.set()

@dp.callback_query_handler(text_contains="inform", state=Purchase.name)
async def cally(call: CallbackQuery, state=FSMContext):
    await state.finish()
    await call.message.edit_text(text=f"\n{'<b>'}Guerrera - з іспанської перекладається як Воїн, чит. [Ґеррера] {'</b>'}"
                                    "\n\nЧат був заснований 8 листопада 2021 р.", parse_mode = 'HTML',
                                     reply_markup= starty)

@dp.callback_query_handler(buy_item.filter(), state=Purchase.name)
async def buying(call: CallbackQuery, callback_data: dict, state= FSMContext):
    item_id = int(callback_data.get("item_id"))
    await call.message.edit_reply_markup()

    item = await Item.get(item_id)
    text = ("Ви бажаєте купити {name} за: {price} дінеро\n"
             "Все правильно?").format(name=item.name,
                            price=item.price)
    markup2 = InlineKeyboardMarkup(
        inline_keyboard=
            [
                [InlineKeyboardButton(text=("Так"), callback_data="shopgood")],
                [InlineKeyboardButton(text=("Ні"), callback_data="shopbad")],
            ]
        )
    await call.message.answer('Прибираємо адміна?', reply_markup=markup2)
    await call.message.edit_text(text, reply_markup=yesnobtn)
    await state.update_data(name=item.name, cost=item.price)
    await Purchase.approval.set()


@dp.callback_query_handler(text_contains="shopbad", state=Purchase.approval)
async def said_no(call: CallbackQuery, state= FSMContext):
    await call.message.delete()
    newuser_id = int(call.from_user.id)
    user = await commands.select_user(user_id=newuser_id)
    await call.message.answer(f'Ваш баланс - {user.balance} дінеро',
                              reply_markup=shopbtns)
    await state.finish()


@dp.callback_query_handler(text_contains="shopgood", state=Purchase.approval)
async def said_yes(call: CallbackQuery, state= FSMContext):
    data = await state.get_data()
    user = await commands.select_user(user_id = call.from_user.id)
    name: Purchase = data.get("name")
    cost: Purchase = data.get("cost")
    new_balance = int(user.balance) - int(cost)
    if user.balance >= cost :
        await user.update(balance=new_balance).apply()
        chat_id = -1001786747206
        await bot.send_message(chat_id, f"{user.first_name} (ID: {call.from_user.id} )\n\nКупив: {name}", )
        await call.message.edit_text(f"Ви купили {name}, скоро адміни вам його додадуть",
                                    reply_markup=backbtn)
        await state.finish()
    else: 
        await call.message.edit_text(f'У вас недостатьно дінеро на рахунку', reply_markup=backbtn)
        await state.finish()


@dp.callback_query_handler(text_contains='sellmoney')
async def getmoney(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    markup2 = InlineKeyboardMarkup(
    inline_keyboard=
        [
            [InlineKeyboardButton(text=("Так"), callback_data="money")],
            [InlineKeyboardButton(text=("Ні"), callback_data="dont")],
        ]
    )
    await call.message.answer('Ви бажаєте купити дінеро?\n(курс 1 грн - 1 дінеро)', reply_markup=markup2)
    await Getmoney.amount.set()


@dp.callback_query_handler(text_contains='dont', state=Getmoney.amount)
async def getmoney2(call: CallbackQuery, state=FSMContext):
    await state.finish()
    newuser_id = int(call.from_user.id)
    user = await commands.select_user(user_id=newuser_id)
    await call.message.edit_text(f'Ваш баланс - {user.balance} дінеро',
                                    reply_markup=shopbtns)
                        

@dp.callback_query_handler(text_contains='money', state=Getmoney.amount)
async def getmoney3(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    await call.message.answer('Введіть кількість дінеро')
    await Getmoney.confirm.set()


@dp.message_handler(state=Getmoney.confirm)
async def getmoney5(message: types.Message, state=FSMContext):
    answer = int(message.text)
    await state.update_data(amount=answer)
    data = await state.get_data()
    amount: Getmoney = data.get('amount')
    carddata: Getmoney = data.get('carddata')
    await message.answer('Ваш баланс скоро буде поповнено', reply_markup=backbtn)
    chat_id = -1001786747206
    newuser_id = int(message.from_user.id)
    user = await commands.select_user(user_id=newuser_id)
    await bot.send_message(chat_id, f'{user.first_name} ID( {newuser_id} )\nБажає купити {amount} дінеро')
    await state.finish()


@dp.callback_query_handler(text_contains='turn', state=Getmoney.carddata)
async def getmoney6(call: CallbackQuery, state=FSMContext):
    await state.finish()
    newuser_id = int(call.message.from_user.id)
    user = await commands.select_user(user_id=newuser_id)
    await call.message.edit_text(f'Ваш баланс - {user.balance} дінеро',
                                    reply_markup=shopbtns)


@dp.callback_query_handler(text_contains='givemoney')
async def givemoney(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    markup2 = InlineKeyboardMarkup(
    inline_keyboard=
        [
            [InlineKeyboardButton(text=("Так"), callback_data="diner")],
            [InlineKeyboardButton(text=("Ні"), callback_data="negative")],
        ]
    )
    await call.message.answer('Ви бажаєте продати дінеро?\n(курс 10 дінеро - 1 грн)', reply_markup=markup2)
    await Givemoney.amount.set()

@dp.callback_query_handler(text_contains='negative', state=Givemoney.amount)
async def givemoney2(call: CallbackQuery, state=FSMContext):
    await state.finish()
    newuser_id = int(call.from_user.id)
    user = await commands.select_user(user_id=newuser_id)
    await call.message.edit_text(f'Ваш баланс - {user.balance} дінеро',
                                    reply_markup=shopbtns)
                        

@dp.callback_query_handler(text_contains='diner', state=Givemoney.amount)
async def givemoney3(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    await call.message.answer('Введіть кількість дінеро')
    await Givemoney.carddata.set()


@dp.message_handler(state=Givemoney.carddata)
async def givemoney4(message: types.Message, state=FSMContext):
    answer = int(message.text)
    await state.update_data(amount=answer)
    await message.delete()
    await message.answer('Введіть номер карти')
    await Givemoney.confirm.set()


@dp.message_handler(state=Givemoney.confirm)
async def givemoney5(message: types.Message, state=FSMContext):
    answer = int(message.text)
    await state.update_data(carddata=answer)
    data = await state.get_data()
    amount: Givemoney = data.get('amount')
    carddata: Givemoney = data.get('carddata')
    await message.answer('Ваш баланс скоро буде поповнено', reply_markup=backbtn)
    chat_id = -1001786747206
    newuser_id = int(message.from_user.id)
    user = await commands.select_user(user_id=newuser_id)
    await bot.send_message(chat_id, f'{user.first_name} ID( {newuser_id} )\nБажає продати {amount} дінеро, на карту-\n{carddata}')
    await state.finish()
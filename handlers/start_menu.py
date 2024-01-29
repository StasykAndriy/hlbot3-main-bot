from loader import dp 
from keyboards.start_buttons import starty
from aiogram import types
import logging
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards.back_button import backbtn
from utils.db_api import quick_commands as commands
from sqlalchemy import false
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=['my'])
async def my(message: types.Message):
    user_id = message.from_user.id
    user = await commands.select_user(user_id=user_id)
    if user == user:
        await message.answer(f' Стан користувача \n👤 Нік: {user.first_name} \nId: {user.user_id} \nОсобистий баланс : {user.balance}')
    else:
        await message.answer('Такого користувача немає в БД', reply_markup=backbtn)


@dp.message_handler(commands=['menu', 'start'])
async def command_menu(message: types.Message):
    user_id=message.from_user.id
    await message.answer_video('https://telegra.ph/file/81fea9a2c1d8c4854f268.mp4')
    await message.answer(f'Buenos días {message.from_user.full_name}! \n\nРаді вас вітати в Botas de Guerrera!',
                                    reply_markup= starty )
    await commands.add_user(user_id=message.from_user.id,
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.first_name,
                            username=message.from_user.username,
                            status='active',
                            balance=0,
                            admin=0)


@dp.callback_query_handler(text_contains="inform")
async def cally(call: CallbackQuery):
    await call.message.delete_reply_markup()
    await call.message.edit_text(f'Buenos días {call.from_user.full_name}! \n\nРаді вас вітати в Botas de Guerrera!',
                                    reply_markup= starty )


@dp.callback_query_handler(text_contains="about")
async def cally(call: CallbackQuery):
    await call.message.edit_text(text=f"\n{'<b>'}Guerrera - з іспанської перекладається як Воїн, чит. [Ґеррера] {'</b>'}"
                                    "\n\nЧат був заснований 8 листопада 2021 р.", parse_mode = 'HTML',
                                     reply_markup= starty)


@dp.callback_query_handler(text_contains="rules")
async def cally (call: CallbackQuery):
    await call.message.edit_text('Правила поведінки в чаті\n\nhttps://teletype.in/@pprovokatorr/MGrules' ,
                                reply_markup= backbtn)


@dp.callback_query_handler(text_contains="rearward")
async def cally (call: CallbackQuery):
    await call.message.edit_text('Повернутися в чат - https://t.me/+wDiS3QYPR5k4N2I6',
                                 reply_markup= backbtn)


@dp.callback_query_handler(text_contains="help")
async def cally (call: CallbackQuery):
    await call.message.edit_text(text='Якщо вам подобається наш чат і ви бажаєте щоб він розвивався далі.\n\nВи можете підтримати нас невеликим донатом🔥\n\nhttps://send.monobank.ua/jar/AP3PZNUsKA',
                                reply_markup= backbtn)


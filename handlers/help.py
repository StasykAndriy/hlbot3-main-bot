from handlers.start_menu import command_menu
from loader import dp, bot
from keyboards.start_buttons import starty
from aiogram import types
from aiogram.types import Message, CallbackQuery
from keyboards.back_button import backbtn
from utils.db_api import quick_commands as commands
from keyboards.shop_button import shopbtns
from data.config import admin_id
from states.help_state import helpstate
from keyboards.get_help import gethlpbtn
from aiogram.dispatcher import FSMContext

@dp.callback_query_handler(text_contains='support')
async def process_start_command(call: CallbackQuery, state=FSMContext):
    newuser_id = call.from_user.id
    user = await commands.select_user(user_id=newuser_id)
    if user.admin == 1:
        await call.message.edit_text(f"Адмін!", reply_markup=backbtn)
    else:
        await call.message.edit_text(f"{call['from'].first_name}, якщо ти хочеш поділитися якоюсь інформацією з адмінами, пиши мені",
                                        reply_markup=gethlpbtn)

@dp.callback_query_handler(text_contains="get")
async def gethelp(call: CallbackQuery, state=FSMContext):
    await call.message.edit_text('Напиши своє повідомлення і я передам його адмінам')
    await helpstate.user_id.set()

@dp.message_handler(state=helpstate.user_id)
async def process_start_command(message: types.Message, state=FSMContext):
    chat_id = -1001786747206
    newuser_id = message.from_user.id
    user = await commands.select_user(user_id=newuser_id)
    if message.reply_to_message == None:
        if 'support' not in message.text:
            await bot.forward_message(chat_id, message.from_user.id, message.message_id)
            await message.answer('Інформація буде передана адмінам!', reply_markup=backbtn)
            await state.finish()
    else:
        if chat_id == -1001786747206:
            if message.reply_to_message.forward_from.id:
                await bot.send_message(message.reply_to_message.forward_from.id, message.text)
                await state.finish()
        else:
            await message.answer('Не можна реплаїти!') 
            await state.finish()

@dp.callback_query_handler(text_contains='replay')
async def answering(call: CallbackQuery, state=FSMContext):
    await call.message.edit_text('Напиши своє повідомлення і я передам його юзеру')
    await helpstate.user_id.set()

@dp.message_handler(content_types=['photo'], state=helpstate.user_id) 
async def handle_docs_photo(message: types.Message, state=FSMContext):
    await bot.forward_message(admin_id, message.from_user.id, message.message_id)
    await message.answer('Фото було передане', reply_markup=backbtn)
    await state.finish()


@dp.message_handler(content_types=['document'], state=helpstate.user_id) 
async def handle_docs_photo(message: types.Message, state=FSMContext):
    await bot.forward_message(admin_id, message.from_user.id, message.message_id)
    await message.answer('Документ був переданий', reply_markup=backbtn)
    await state.finish()
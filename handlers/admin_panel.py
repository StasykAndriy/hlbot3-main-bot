from loader import dp, bot 
from data.config import admin_id
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.admin_button import adminbtn
from aiogram.types import CallbackQuery
from keyboards.adminback import adminbackbtn
from aiogram import types
from loader import dp 
from states.balance_state import balance
from states.get_name_state import GetName 
from utils.db_api import quick_commands as commands
from states.get_id_state import GetId
from utils.db_api import user
from utils.db_api.user import Item
from states.shop_state import NewItem
from states.remove_item_state import RemoveItem
from utils.db_api.user import users
from states.new_admin import NewAdmin
from handlers.start_menu import command_menu
from keyboards.products_button import get_items
from keyboards.products_button import buy_item
from states.remove_admin import DeleteAdmin
from states.get_name_state import GetName



@dp.message_handler(commands=["hyh135"])
async def cancel(message: types.Message):
    await message.delete()
    newuser_id = message.from_user.id
    user = await commands.select_user(user_id=newuser_id)
    if user.admin == 1:
        await message.answer(f'Запрошуємо до адмінпанелі, {message.from_user.full_name}',
                            reply_markup=adminbtn)
    else:
        await message.answer('Немає доступу')

@dp.message_handler(commands=["alladmin"])
async def alladmin(message: types.Message):
    user = await commands.select_user(user_id=message.from_user.id)
    if user.admin == 1:
        user = await commands.select_all_admins()
        await message.answer(user)
    else:
        await message.answer('Немає доступу')

@dp.message_handler(commands=["alluser"])
async def alladmin(message: types.Message):
    user = await commands.select_user(user_id=message.from_user.id)
    if user.admin == 1:
        user = await commands.select_all_users()
        print(*user, sep=',')
    else:
        await message.answer('Немає доступу')

@dp.callback_query_handler(text_contains="getname", state=None)
async def getname(call: CallbackQuery, state: FSMContext):
    user = await commands.select_user(user_id=call.message.from_user.id)
    if user.admin == 1:
        await call.message.delete()
        await call.message.answer(f'Введіть ID необхідного юзера')
        await GetName.username.set()
    else:
        await call.message.answer('Немає доступу')

@dp.message_handler(state=GetName.username)
async def getname(message:types.Message, state:FSMContext):
    user = await commands.select_user(user_id=message.from_user.id)
    if user.admin == 1:
        await message.delete()
        user_id = int(message.text)
        if '/' not in message.text:
            user = await commands.select_user(user_id=user_id)
            if user == user:
                await message.answer(f' Стан користувача \n👤 Нік: {user.first_name} \nId: {user.user_id} \nОсобистий баланс : {user.balance}')
                await state.finish()
            else:
                await message.answer('Такого користувача немає в БД', reply_markup=adminbackbtn)
                await state.finish()
        else: 
            await message.answer('Спробуйте заново', reply_markup=adminbackbtn)
            await state.finish()
    else: 
        await message.answer('Немає доступу')


@dp.callback_query_handler(text_contains="getid", state=None)
async def getid(call: CallbackQuery, state: FSMContext):
    user = await commands.select_user(user_id=call.message.from_user.id)
    if user.admin == 1:
        await call.message.delete()
        await call.message.answer(f'Введіть нік необхідного юзера')
        await GetId.username.set()
    else: 
        await call.message.answer('Немає доступу')

@dp.message_handler(state=GetId.username)
async def getid(message:types.Message, state:FSMContext):
    user = await commands.select_user(user_id=message.from_user.id)
    if user.admin == 1:
        await message.delete()
        first_name = message.text
        if '/' not in message.text:
                user = await commands.select_user_by_name(first_name=first_name)
                if user == user:
                    await message.answer(f' Стан користувача \n👤 Нік: {user.first_name} \nId: {user.user_id} \nОсобистий баланс : {user.balance}')
                    await state.finish()
                else:
                    await message.answer('Такого користувача немає в БД', reply_markup=adminbackbtn)
                    await state.finish()
        else: 
            await message.answer('Спробуйте заново', reply_markup=adminbackbtn)
            await state.finish()
    else: 
            await message.answer('Немає доступу')

@dp.callback_query_handler(text_contains="previous", state=None)
async def adminback(call: CallbackQuery, state: FSMContext):
    user = await commands.select_user(user_id=call.message.from_user.id)
    if user.admin == 1:
        await call.message.answer(f'Запрошуємо до адмінпанелі, {message.from_user.full_name}',
                                reply_markup=adminbtn)
        await state.finish()
    else: 
            await call.message.answer('Немає доступу')

@dp.callback_query_handler(text_contains="new_balance", state = None)
async def change_balance(call: CallbackQuery, state=FSMContext):
    user = await commands.select_user(user_id=call.message.from_user.id)
    if user.admin == 1:
        await call.message.delete_reply_markup()
        markup2 = InlineKeyboardMarkup(
        inline_keyboard=
            [
                [InlineKeyboardButton(text=("Так"), callback_data="yes")],
                [InlineKeyboardButton(text=("Ні"), callback_data="previous")],
            ]
        )
        await call.message.answer('Змінюємо баланс?', reply_markup=markup2)
    else: 
            await call.message.answer('Немає доступу')


@dp.callback_query_handler(text_contains="yes", state = None)
async def change_balance(call: CallbackQuery, state=FSMContext):
    user = await commands.select_user(user_id=call.message.from_user.id)
    if user.admin == 1:
        if '/' not in call.message.text:
            markup2 = InlineKeyboardMarkup(
            inline_keyboard=
                [
                    [InlineKeyboardButton(text=("Назад"), callback_data="nooo")],
                ]
            )
            await call.message.answer('Введіть кількість дінеро ', reply_markup=markup2)
            await balance.amount.set()
        else:
            await call.message.answer('Спробуйте заново', reply_markup=adminbackbtn)
            await state.finish()
    else: 
        await call.message.answer('Немає доступу')


@dp.message_handler(state=balance.amount)
async def change_balance(message:types.Message, state: FSMContext):
    answer = message.text
    if '/' in answer:
        await message.answer('Спробуйте заново', reply_markup=adminbackbtn)
        await state.finish()
    else:
        await state.update_data(amount=answer)
        markup2 = InlineKeyboardMarkup(
        inline_keyboard=
            [
                [InlineKeyboardButton(text=("Назад"), callback_data="noo")],
            ]
        )
        await message.answer("Введіть ID користувача", reply_markup=markup2)
        await balance.user_id.set()


@dp.message_handler(state=balance.user_id)
async def set_id(message: types.Message, state: FSMContext):
    if '/' in message.text:
        await message.answer('Спробуйте заново', reply_markup=adminbackbtn)
        await state.finish()
    else:
        newuser_id = int(message.text)
        data = await state.get_data()
        answer: balance = data.get("amount")
        user = await commands.select_user(user_id=newuser_id)
        await state.update_data(user_id=newuser_id)
        markup2 = InlineKeyboardMarkup(
        inline_keyboard=
            [
                [InlineKeyboardButton(text=("Так"), callback_data="confirm_balance")],
                [InlineKeyboardButton(text=("Ні"), callback_data="un")],
            ]
        )
        answer: balance = data.get("amount")
        if '-' in answer:
             await message.answer((f"Ви зменшуєте баланс на: {answer} \nКористувачу: {user.first_name}"
                            "\nВсе правильно?"),
                            reply_markup=markup2)
        else:
            await message.answer((f"Ви поповнюєте баланс на: {answer} \nКористувачу: {user.first_name}"
                                "\nВсе правильно?"),
                                reply_markup=markup2)
        await state.update_data(user_id=newuser_id)
        await balance.confirm1.set()

@dp.callback_query_handler(text_contains="un", state = balance.confirm1)
async def chang_balance(call: CallbackQuery, state=FSMContext):
    user = await commands.select_user(user_id=call.message.from_user.id)
    if user.admin == 1:
        await call.message.delete_reply_markup()
        markup2 = InlineKeyboardMarkup(
        inline_keyboard=
            [
                [InlineKeyboardButton(text=("Так"), callback_data="yes")],
                [InlineKeyboardButton(text=("Ні"), callback_data="previous")],
            ]
        )
        await call.message.answer('Змінюємо баланс?', reply_markup=markup2)
        await state.finish()
    else: 
        await call.message.answer('Немає доступу')

@dp.callback_query_handler(state=balance.confirm1, text_contains="confirm_balance")
async def confirm1(call: CallbackQuery, state: FSMContext):
    if '/' in call.message.text:
        await call.message.answer('Спробуйте заново', reply_markup=adminbackbtn)
        await state.finish()
    else:
        await call.message.delete()
        data = await state.get_data()
        answer: balance = data.get("amount")
        newuser_id: balance = data.get('user_id')
        await commands.change_balance(user_id=newuser_id, amount=answer)
        await call.message.answer('Баланс поповнено', reply_markup=adminbackbtn)
        if '-' in answer:
            await bot.send_message(newuser_id, f"Ваш баланс зменшився на {answer}")
        else:
            await bot.send_message(newuser_id, f"Ваш баланс поповнено на {answer}")
        chat_id = -1001786747206
        if '-' in answer:
            await bot.send_message(chat_id, f" Адмін {message.from_user.full_name} зменшив \n Баланс {user.first_name} (ID: {newuser_id})  на {answer}")
        else:
            await bot.send_message(chat_id, f"Адмін {message.from_user.full_name} поповнив \n Баланс {user.first_name} (ID: {newuser_id})  на {answer}")
        await state.finish()


@dp.callback_query_handler(text_contains="new_item")
async def add_item(call: CallbackQuery):
    markup2 = InlineKeyboardMarkup(
    inline_keyboard=
        [
            [InlineKeyboardButton(text=("Так"), callback_data="create")],
            [InlineKeyboardButton(text=("Ні"), callback_data="previous")],
        ]
    )
    await call.message.answer('Створюємо товар?', reply_markup=markup2)

@dp.callback_query_handler(text_contains="create")
async def add_item(call: CallbackQuery):
    await call.message.edit_text(("Введіть назву нового товару"))
    await NewItem.Name.set()

@dp.message_handler(state=NewItem.Name)
async def enter_name(message: types.Message, state: FSMContext):
    if '/' in message.text:
        await message.answer('Спробуйте заново', reply_markup=adminbackbtn)
        await state.finish()
    else:
        name = message.text
        item = Item()
        item.name = name

        await message.answer(f"Назва: {name},\nВведіть ціну")
        await state.update_data(item=item)
        await NewItem.Price.set()


@dp.message_handler(state=NewItem.Price)
async def enter_price(message: types.Message, state: FSMContext):
    if '/' in message.text:
        await message.answer('Спробуйте заново', reply_markup=adminbackbtn)
        await state.finish()
    else:
        data = await state.get_data()
        item: Item = data.get("item")
        try:
            price = int(message.text)
        except ValueError:
            await message.answer(("Введіть число"))
            return

        item.price = price
        markup = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [InlineKeyboardButton(text=("Так"), callback_data="confirm")],
                [InlineKeyboardButton(text=("Ні"), callback_data="change")],
            ]
        )
        await message.answer(("Ціна: {price:}\n"
                            "Правильно?").format(price=price),
                            reply_markup=markup)
        await state.update_data(item=item)
        await NewItem.Confirm.set()


@dp.callback_query_handler(text_contains="change", state=NewItem.Confirm)
async def enter_price(call: types.CallbackQuery, state=FSMContext):
    if '/' in call.message.text:
        await call.message.answer('Спробуйте заново', reply_markup=adminbackbtn)
        await state.finish()
    else:
        await call.message.delete()
        await call.message.edit_reply_markup()
        await call.message.answer(("Введіть ціну заново"))
        await NewItem.Price.set()


@dp.callback_query_handler(text_contains="confirm", state=NewItem.Confirm)
async def enter_price(call: types.CallbackQuery, state: FSMContext):
    if '/' in call.message.text:
        await call.message.answer('Спробуйте заново', reply_markup=adminbackbtn)
        await state.finish()
    else:
        data = await state.get_data()
        item: Item = data.get("item")
        await item.create()
        await call.message.edit_text(("Товар був створенний"),reply_markup=adminbackbtn)
        await state.finish()


@dp.callback_query_handler(text_contains="remove_item")
async def remove(call:types.CallbackQuery, state:FSMContext):
    if '/' in call.message.text:
        await call.message.answer('Спробуйте заново', reply_markup=adminbackbtn)
        await state.finish()
    else:
        await call.message.edit_reply_markup()
        markup = await get_items()
        markup.add(
            InlineKeyboardButton(text="Назад", callback_data="gramazekademon")
        )
        await call.message.edit_text("Список товарів нижче", reply_markup=markup)
        await RemoveItem.Item_name.set()

@dp.callback_query_handler(text_contains="gramazekademon", state=RemoveItem.Item_name)
async def remove(call:types.CallbackQuery, state:FSMContext):
    user = await commands.select_user(user_id=call.message.from_user.id)
    if user.admin == 1:
        await state.finish()
        await call.message.answer(f'Запрошуємо до адмінпанелі, {message.from_user.full_name}',
                                reply_markup=adminbtn)
    else: 
        await call.message.answer('Немає доступу')


@dp.callback_query_handler(buy_item.filter(), state=RemoveItem.Item_name)
async def remove(call:types.CallbackQuery ,callback_data: dict, state:FSMContext):
    if '/' in call.message.text:
        await call.message.answer('Спробуйте заново', reply_markup=adminbackbtn)
        await state.finish()
    else:
        item_id = int(callback_data.get("item_id"))
        await call.message.edit_reply_markup()
        item = await Item.get(item_id)
        text = ("Ви бажаєте прибрати {name}"
                "Все правильно?").format(name=item.name)
        markup2 = InlineKeyboardMarkup(
        inline_keyboard=
            [
                [InlineKeyboardButton(text=("Так"), callback_data="ok")],
                [InlineKeyboardButton(text=("Ні"), callback_data="goglabzavr")],
            ]
        )
        await call.message.edit_text(text, reply_markup=markup2)
        name= item.name
        await state.update_data(Item_name=name)
        await RemoveItem.Confirm.set()

@dp.callback_query_handler(text_contains="goglabzavr", state=RemoveItem.Confirm)
async def remove(call:types.CallbackQuery, state:FSMContext):
    user = await commands.select_user(user_id=call.message.from_user.id)
    if user.admin == 1:
        await state.finish()
        await call.message.answer(f'Запрошуємо до адмінпанелі, {message.from_user.full_name}',
                                reply_markup=adminbtn)
    else: 
        await call.message.answer('Немає доступу')

@dp.callback_query_handler(text_contains="ok", state=RemoveItem.Confirm)
async def remove(call:types.CallbackQuery, state:FSMContext):
    await call.message.delete()
    if '/' in call.message.text:
        await call.message.answer('Спробуйте заново', reply_markup=adminbackbtn)
        await state.finish()
    else:
        data = await state.get_data()
        itemname: RemoveItem = data.get('Item_name')
        item = await commands.select_item(name=itemname)
        await item.delete()
        await call.message.answer('Товар було видалено',reply_markup=adminbackbtn)
        await state.finish()


@dp.callback_query_handler(text_contains="add_admin")
async def admini(call:types.CallbackQuery, state:FSMContext):
    if '/' in call.message.text:
        await call.message.answer('Спробуйте заново', reply_markup=adminbackbtn)
        await state.finish()
    else:
        markup2 = InlineKeyboardMarkup(
        inline_keyboard=
            [
                [InlineKeyboardButton(text=("Так"), callback_data="new")],
                [InlineKeyboardButton(text=("Ні"), callback_data="previous")],
            ]
        )
        await call.message.answer('Добавляємо адміна?', reply_markup=markup2)

@dp.callback_query_handler(text_contains="new")
async def admini(call:types.CallbackQuery, state:FSMContext):
    if '/' in call.message.text:
        await call.message.answer('Спробуйте заново', reply_markup=adminbackbtn)
        await state.finish()
    else:
        await call.message.answer('Введіть ID нового адміна')
        await NewAdmin.user_id.set()


@dp.message_handler(state=NewAdmin.user_id)
async def admini(message: types.Message, state:FSMContext):
    if '/' in message.text:
        await message.answer('Спробуйте заново', reply_markup=adminbackbtn)
        await state.finish()
    else:
        newuser_id = int(message.text)
        user = await commands.select_user(user_id=newuser_id)
        await user.update(admin = 1).apply()
        await message.answer(f'{user.first_name} став Адміном!')
        await state.finish()

@dp.message_handler(commands=['reg'])
async def reg(message: types.Message):
    if message.from_user.id == 5763984902:
        newuser_id = 5763984902
        user = await commands.select_user(user_id=newuser_id)
        await user.update(admin=1).apply()
    else:
        await message.answer('Немає доступу')

@dp.callback_query_handler(text_contains="remove_admin")
async def noadmini(call:types.CallbackQuery, state:FSMContext):
    if '/' in call.message.text:
        await call.message.answer('Спробуйте заново', reply_markup=adminbackbtn)
        await state.finish()
    else:
        markup2 = InlineKeyboardMarkup(
        inline_keyboard=
            [
                [InlineKeyboardButton(text=("Так"), callback_data="old")],
                [InlineKeyboardButton(text=("Ні"), callback_data="previous")],
            ]
        )
        await call.message.answer('Прибираємо адміна?', reply_markup=markup2)

@dp.callback_query_handler(text_contains="old")
async def noadmini(call:types.CallbackQuery, state:FSMContext):
    if '/' in call.message.text:
        await call.message.answer('Спробуйте заново', reply_markup=adminbackbtn)
        await state.finish()
    else:
        await call.message.delete()
        await call.message.answer('Введіть ID адміна, якого треба видалити')
        await DeleteAdmin.user_id.set()

@dp.message_handler(state=DeleteAdmin.user_id)
async def noadmini(message: types.Message, state:FSMContext):
    if '/' in message.text:
        await message.answer('Спробуйте заново', reply_markup=adminbackbtn)
        await state.finish()
    else:
        await message.delete()
        newuser_id = int(message.text)
        user = await commands.select_user(user_id=newuser_id)
        await user.update(admin = 0).apply()
        await message.answer(f'{user.first_name} більше не Адмін!')
        await state.finish()





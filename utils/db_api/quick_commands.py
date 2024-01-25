from hashlib import new
from sqlalchemy import Boolean
from asyncpg import UniqueViolationError
from utils.db_api.user import users
import asyncio
from typing import List
from utils.db_api.user import Item
from sqlalchemy import and_
from data.config import db 



async def add_user(user_id: int, first_name: str, last_name: str, username: str, status: str, balance: float, admin: float):
    try:
        user = users(user_id=user_id, first_name=first_name, last_name=last_name, username=username, status=status, balance=balance, admin=admin)
        await user.create()
    except UniqueViolationError:
        print('Помилка')

async def select_user(user_id):
    user = await users.query.where(users.user_id == user_id).gino.first()
    return user


async def select_user_by_name(first_name):
    user = await users.query.where(users.first_name == first_name).gino.all()
    return user



async def select_all_users():
    user = await users.select('first_name', 'balance').gino.all()
    return user

async def select_all_admins():
    user = await users.select('first_name').where(users.admin == 1).gino.all()
    return user

async def change_balance(user_id: int, amount: int):
    user = await select_user(user_id)
    new_balance = int(user.balance) + int(amount)
    await user.update(balance=new_balance).apply()

async def show_items():
    items = await Item.query.gino.all()

    return items

async def select_item(name):
    item = await Item.query.where(Item.name == name).gino.first()
    return item 





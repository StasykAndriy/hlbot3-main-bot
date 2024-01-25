from sqlalchemy import BigInteger
from sqlalchemy import Column,sql
from .base import TimedBaseModel
from data.config import db 
from gino.schema import GinoSchemaVisitor
from data.config import POSTGRES_URL
from sqlalchemy import (Column, Integer, BigInteger, String, Float,
                        Sequence, TIMESTAMP, Boolean, JSON)


class users(TimedBaseModel):
    __tablename__ = "users"
    query: sql.Select

    user_id = Column(BigInteger, primary_key =True)
    first_name = Column(String(200))
    last_name = Column(String(50))
    username = Column(String(50))
    status = Column(String(50))
    balance = Column(Float)
    admin = Column(Float)

    def __repr__(self):
        return "<users(user_id='{}', first_name='{}', last_name='{}', username='{}', status='{}', balance='{}', admin='{}')>".format(
            self.user_id, self.first_name, self.last_name, self.username, self.status, self.balance, self.admin)

class Item(db.Model):
    __tablename__ = 'items'
    query: sql.Select

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    price = Column(Integer)  # Цена в копейках (потом делим на 100)

    def __repr__(self):
        return "<Item(id='{}', name='{}', price='{}')>".format(
            self.id, self.name, self.price)

async def create_users_db():
    await db.set_bind(POSTGRES_URL)

    # Create tables
    db.gino: GinoSchemaVisitor
    await db.gino.create_all()
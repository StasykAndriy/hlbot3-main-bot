from sqlalchemy import Column,sql
from data.config import db
from gino.schema import GinoSchemaVisitor
from sqlalchemy import (Column, Integer, BigInteger, String,
                        Sequence, TIMESTAMP, Boolean, JSON)
from sqlalchemy import sql
from data.config import POSTGRES_URL

class Item(db.Model):
    __tablename__ = 'items'
    query: sql.Select

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    price = Column(Integer)

    def __repr__(self):
        return "<Item(id='{}', name='{}', price='{}')>".format(
            self.id, self.name, self.price)



async def create_items_db():
    await db.set_bind(POSTGRES_URL)

    # Create tables
    db.gino: GinoSchemaVisitor
    await db.gino.drop_all()
    await db.gino.create_all()


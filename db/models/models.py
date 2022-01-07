from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (Column, String, DateTime, Boolean, BigInteger, ForeignKey, JSON,
                        Integer, ForeignKey, UniqueConstraint, PrimaryKeyConstraint,
                        ForeignKeyConstraint, Text, Float)


from datetime import datetime
from uuid import uuid4

Base = declarative_base()
# ------------ Examples -------------------

class Client(Base):
    __tablename__ = 'clients'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now)

    orders = relationship('Order', back_populates='clients')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now)

    items = relationship('Item', back_populates='products')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    client_id = Column(UUID(as_uuid=True),
                             ForeignKey('clients.id', ondelete='cascade', onupdate='cascade'),
                             index=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now)

    clients = relationship('Client', back_populates='orders')
    items = relationship('Item', back_populates='orders')




class Item(Base):
    __tablename__ = 'items'

    product_id = Column(Integer,
                             ForeignKey('products.id', ondelete='cascade', onupdate='cascade'),
                             index=True)
    order_id = Column(Integer,
                             ForeignKey('orders.id', ondelete='cascade', onupdate='cascade'),
                             index=True)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now)

    orders = relationship('Order', back_populates='items')
    products = relationship('Product', back_populates='items')

    __table_args__ = (PrimaryKeyConstraint('product_id', 'order_id'),)
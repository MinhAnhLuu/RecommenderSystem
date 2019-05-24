import datetime

from sqlalchemy import (
    DECIMAL, Column, DateTime, ForeignKey, Integer,
    String
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Base(object):
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow(),
        nullable=False
    )
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow(),
        onupdate=datetime.datetime.utcnow(),
        nullable=False
    )


DeclarativeBase = declarative_base(cls=Base)


class Order(DeclarativeBase):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, default="CREATED", nullable=False)
    customer_id = Column(String, nullable=False)

class OrderDetail(DeclarativeBase):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(
        Integer,
        ForeignKey("orders.id", name="fk_order_details_orders"),
        nullable=False
    )
    product_id = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    price = Column(DECIMAL(18, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    order = relationship("Order", backref="order_details")


DeclarativeOrderDetail = declarative_base(OrderDetail)

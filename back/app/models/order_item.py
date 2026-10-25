from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id", ondelete="CASCADE"),
        primary_key=True,
    )
    product_id = Column(
        Integer,
        ForeignKey("products.product_id", ondelete="RESTRICT"),
        primary_key=True,
    )
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable=False) 

    __table_args__ = (
        CheckConstraint("quantity > 0", name="quantity_check"),
        CheckConstraint("unit_price > 0", name="unit_price_check"),
    )

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
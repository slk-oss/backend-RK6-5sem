from sqlalchemy import CheckConstraint, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(100), nullable=False)
    product_description = Column(Text)
    image_url = Column(String(255))
    product_price = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("product_price > 0", name="product_price_check"),
    )

    order_items = relationship("OrderItem", back_populates="product")
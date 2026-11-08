from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship
import enum 
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from app.database import Base

class OrderStatus(str, enum.Enum):
    PENDING   = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(
        PgEnum(OrderStatus, name='order_status', create_type=False,
               values_callable=lambda e: [m.value for m in e]),
        nullable=False,
        default=OrderStatus.PENDING,
        server_default='pending',
    )

    user = relationship("User", back_populates="orders")

    order_items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

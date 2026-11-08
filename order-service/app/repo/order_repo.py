from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order import OrderStatus

class OrderRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, order_id: int) -> Order | None:
        return self.db.get(Order, order_id)

    def get_by_user(self, user_id: int) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
        )
        return list(self.db.execute(stmt).scalars())

    def create(self, user_id: int) -> Order:
        order = Order(user_id=user_id)
        self.db.add(order)
        self.db.flush()
        return order

    def get_pending(self, user_id: int) -> Order | None:
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .where(Order.status == OrderStatus.PENDING)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_all(self) -> list[Order]:
        stmt = select(Order).order_by(
            Order.created_at.desc(),
            Order.order_id.desc(),
        )

        return list(self.db.execute(stmt).scalars())   
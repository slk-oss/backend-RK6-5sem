from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.order import Order


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
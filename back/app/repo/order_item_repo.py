from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.order_item import OrderItem


class OrderItemRepo:

    def __init__(self, db: Session):
        self.db = db

    def get(self, order_id: int, product_id: int) -> OrderItem | None:
        return self.db.get(OrderItem, (order_id, product_id))

    def get_by_order(self, order_id: int) -> list[OrderItem]:
        stmt = (
            select(OrderItem)
            .where(OrderItem.order_id == order_id)
            .order_by(OrderItem.product_id)
        )
        return list(self.db.execute(stmt).scalars())

    def get_by_product(self, product_id: int) -> list[OrderItem]:
        stmt = (
            select(OrderItem)
            .where(OrderItem.product_id == product_id)
        )
        return list(self.db.execute(stmt).scalars())

    def exists(self, order_id: int, product_id: int) -> bool:
        return self.get(order_id, product_id) is not None

    def add(
            self,
            order_id: int,
            product_id: int,
            quantity: int,
            unit_price: int,
    ) -> OrderItem:
        item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
        )
        self.db.add(item)
        self.db.flush()
        return item

    def set_quantity(
            self,
            order_id: int,
            product_id: int,
            quantity: int,
    ) -> OrderItem | None:
        item = self.get(order_id, product_id)
        if item is None:
            return None
        item.quantity = quantity
        self.db.flush()
        return item

    def delete(self, order_id: int, product_id: int) -> bool:
        item = self.get(order_id, product_id)
        if item is None:
            return False
        self.db.delete(item)
        self.db.flush()
        return True
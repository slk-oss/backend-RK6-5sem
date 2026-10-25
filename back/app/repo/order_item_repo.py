from sqlalchemy import select
from app.database import db
from app.models.order_item import OrderItem


class OrderItemRepo:

    def get(self, order_item_id: int) -> OrderItem | None:
        return db.session.get(OrderItem.order_id, OrderItem.product_id)

    def get_by_order(self, order_id: int) -> list[OrderItem]:
        stmt = (
            select(OrderItem)
            .where(OrderItem.order_id == order_id)
            .order_by(OrderItem.product_id)
        )
        return list(db.session.execute(stmt).scalars().all())

    def get_by_product(self, product_id: int) -> list[OrderItem]:
        stmt = (
            select(OrderItem)
            .where(OrderItem.product_id == product_id)
        )
        return list(db.session.execute(stmt).scalars().all())

    def exists(self, order_id: int, product_id: int) -> bool:
        stmt = (
            select(OrderItem.order_id)
            .where(OrderItem.order_id == order_id)
            .where(OrderItem.product_id == product_id)
        )
        return db.session.execute(stmt).first() is not None


    def add(
            self,
            order_id: int,
            product_id: int,
            quantity: int,
            unit_price: int
    ) -> OrderItem:
        item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
        )
        db.session.add(item)
        return item


    def set_quantity(
            self, 
            order_id: int,
            product_id: int,
            quantity: int
    ) -> OrderItem | None:
        item = self.get(order_id, product_id)
        if item is None:
            return None 
        item.quantity = quantity
        return item

    def delete(
            self,
            order_id: int,
            product_id: int,
    ) -> bool:
        item = self.get(order_id, product_id)
        if item is None:
            return True
        db.session.delete(item)
        return True

    def delete_by_order(self, order_id: int) -> int:
        items = self.get_by_order(order_id)
        for it in items:
            db.session.delete(it)
        return len(items)
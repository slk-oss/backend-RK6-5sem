from app.repo.order_repo import OrderRepo
from app.repo.order_item_repo import OrderItemRepo
from app.repo.product_repo import ProductRepo
from app.models.order import Order
from app.models.order_item import OrderItem
from sqlalchemy.orm import Session



class OrderService:
    def __init__(self, db: Session):
        self.order_repo = OrderRepo(db)
        self.item_repo = OrderItemRepo(db)
        self.product_repo = ProductRepo(db)

    def get_or_create_cart(self, user_id: int) -> Order:
        cart = self.order_repo.get_pending(user_id)
        if cart is not None:
            return cart
        return self.order_repo.create(user_id)

    def add_to_cart(self, user_id: int, product_id: int, quantity: int) -> OrderItem:
        cart = self.get_or_create_cart(user_id)
        product = self.product_repo.get_by_id(product_id)
        if product is None:
            raise ValueError(f"Product with id {product_id} not found")
        if self.item_repo.exists(cart.order_id, product_id):
            item = self.item_repo.get(cart.order_id, product_id)
            return self.item_repo.set_quantity(
                cart.order_id,
                product_id,
                item.quantity + quantity,
        )
        return self.item_repo.add(
            order_id=cart.order_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=product.product_price,
        )

    def get_cart_total(self, order_id: int) -> int:
        pass

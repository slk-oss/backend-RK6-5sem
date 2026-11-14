from dataclasses import dataclass

import requests
from redis import Redis
from sqlalchemy.orm import Session

from app.repo.order_repo import OrderRepo


class CartError(Exception):
    pass


class CatalogUnavailable(CartError):
    pass


@dataclass
class CartItem:
    product_id: int
    product_name: str | None
    quantity: int
    unit_price: int | None

    @property
    def subtotal(self) -> int | None:
        if self.unit_price is None:
            return None
        return self.quantity * self.unit_price


class OrderService:
    def __init__(self, db: Session, redis: Redis, product_service_url: str):
        self.order_repo = OrderRepo(db)
        self.redis = redis
        self.product_service_url = product_service_url.rstrip("/")

    def _cart_key(self, user_id: int) -> str:
        return f"cart:{user_id}"

    def _get_product(self, product_id: int) -> tuple[str, int] | None:
        try:
            response = requests.get(
                f"{self.product_service_url}/products/api/{product_id}",
                timeout=(1, 3),
            )
            if response.status_code == 404:
                return None

            response.raise_for_status()
            data = response.json()
            name = data["product_name"]
            price = data["product_price"]
        except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
            raise CatalogUnavailable("Каталог временно недоступен.") from exc

        if not isinstance(name, str) or type(price) is not int or price <= 0:
            raise CatalogUnavailable("Каталог вернул некорректные данные.")

        return name, price

    def get_cart(self, user_id: int) -> list[CartItem]:
        quantities = self.redis.hgetall(self._cart_key(user_id))
        items = []

        for raw_id, raw_quantity in quantities.items():
            product_id = int(raw_id)
            quantity = int(raw_quantity)
            product = self._get_product(product_id)

            if product is None:
                items.append(CartItem(product_id, None, quantity, None))
                continue

            name, price = product
            items.append(CartItem(product_id, name, quantity, price))

        return items

    def add_to_cart(self, user_id: int, product_id: int, quantity: int) -> None:
        if quantity < 1:
            raise CartError("Количество должно быть больше нуля.")

        if self._get_product(product_id) is None:
            raise CartError("Товар не найден.")

        self.redis.hincrby(self._cart_key(user_id), str(product_id), quantity)
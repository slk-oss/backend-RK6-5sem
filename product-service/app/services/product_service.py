import json

from flask import current_app
from redis.exceptions import RedisError

from app import db
from app.models.product import Product
from app.repo.product_repo import ProductRepo


MENU_CACHE_KEY = "product:menu"
MENU_CACHE_TTL = 60


class ProductService:
    def __init__(self):
        self.product_repo = ProductRepo(db.session)

    def get_menu(self) -> list[dict]:
        redis_client = current_app.extensions["redis"]

        try:
            cached_menu = redis_client.get(MENU_CACHE_KEY)
            if cached_menu is not None:
                return json.loads(cached_menu)
        except RedisError:
            current_app.logger.warning("Could not read menu cache")

        menu = [
            {
                "product_id": product.product_id,
                "product_name": product.product_name,
                "product_description": product.product_description,
                "image_url": product.image_url,
                "product_price": product.product_price,
            }
            for product in self.product_repo.get_all()
        ]

        try:
            redis_client.set(MENU_CACHE_KEY, json.dumps(menu), ex=MENU_CACHE_TTL)
        except RedisError:
            current_app.logger.warning("Could not write menu cache")

        return menu

    def get_product(self, product_id: int) -> Product | None:
        return self.product_repo.get_by_id(product_id)
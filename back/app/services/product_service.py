from app.repo.product_repo import ProductRepo
from app.models.product import Product
from app import db

class ProductService:
    def __init__(self):
        self.product_repo = ProductRepo(db.session)

    def get_menu(self) -> list[Product]:
        return self.product_repo.get_all()

    def get_product(self, product_id: int) -> Product | None:
        return self.product_repo.get_by_id(product_id)
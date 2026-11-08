from flask import Blueprint, abort, render_template
from app.services.product_service import ProductService

bp = Blueprint("products", __name__, url_prefix="/products")

@bp.get("/")
def list_products():
    products = ProductService().get_menu()
    return render_template("products/list.html", products=products)

@bp.get("/<int:product_id>")
def detail(product_id):
    product = ProductService().get_product(product_id)
    if product is None:
        return abort(404)
    else:
        return render_template("products/detail.html", product=product)

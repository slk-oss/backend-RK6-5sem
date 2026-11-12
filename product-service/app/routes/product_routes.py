from flask import Blueprint, abort, render_template, jsonify
from app.services.product_service import ProductService
from app.serializers.product import product_to_dict

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

@bp.get("/api/")
def list_products_api():
    products = ProductService().get_menu()
    return jsonify(products)

@bp.get("/api/<int:product_id>")
def detail_api(product_id):
    product = ProductService().get_product(product_id)

    if product is None:
        return jsonify({"error": "Товар не найден"}), 404

    return jsonify(product_to_dict(product))

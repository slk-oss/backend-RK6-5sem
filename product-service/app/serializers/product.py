from app.models.product import Product


def product_to_dict(product: Product) -> dict:
    return {
        "product_id": product.product_id,
        "product_name": product.product_name,
        "product_description": product.product_description,
        "image_url": product.image_url,
        "product_price": product.product_price,
    }
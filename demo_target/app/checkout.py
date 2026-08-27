from .database import get_products
from .shipping import calculate_shipping


def checkout(cart):
    product_ids = cart["product_ids"]

    products = get_products(product_ids)

    shipping = calculate_shipping(cart)

    total = sum(
        product["price"]
        for product in products
    )

    return {
        "items": products,
        "shipping": shipping,
        "total": total,
    }

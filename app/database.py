import time


def get_product(product_id: int) -> dict:
    # Simulated slow database query.
    time.sleep(0.08)

    return {
        "id": product_id,
        "price": 25.00,
    }


def get_products(product_ids: list[int]) -> list[dict]:
    """
    Simulated batched database query.

    One database round trip replaces one round trip per product.
    """
    time.sleep(0.08)

    return [
        {
            "id": product_id,
            "price": 25.00,
        }
        for product_id in product_ids
    ]

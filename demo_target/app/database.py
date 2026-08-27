import time


def get_products(product_ids: list[int]) -> list[dict]:
    # Simulate one batched database query.
    time.sleep(0.08)

    return [
        {
            "id": product_id,
            "price": 25.00,
        }
        for product_id in product_ids
    ]

from app.checkout import checkout


def test_checkout():
    result = checkout(
        {
            "product_ids": [1, 2, 3],
        }
    )

    assert result["total"] == 75.00
    assert result["shipping"] == 12.00
    assert len(result["items"]) == 3
